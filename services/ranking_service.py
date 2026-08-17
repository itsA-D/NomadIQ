from __future__ import annotations

from dataclasses import replace

from models.hotel import Hotel
from models.search_request import SearchRequest


def _norm(value: float | None, low: float, high: float) -> float:
    if value is None or high == low: return 0.5
    return max(0.0, min(1.0, (value - low) / (high - low)))

def rank_hotels(hotels: list[Hotel], request: SearchRequest) -> list[Hotel]:
    if not hotels: return []
    if request.sort_by == "price_asc": return sorted(hotels, key=lambda h: (h.price_per_night, h.name))
    if request.sort_by == "price_desc": return sorted(hotels, key=lambda h: (-h.price_per_night, h.name))
    if request.sort_by == "rating_desc": return sorted(hotels, key=lambda h: (-(h.guest_rating or 0), h.price_per_night))
    if request.sort_by == "stars_desc": return sorted(hotels, key=lambda h: (-(h.star_rating or 0), -(h.guest_rating or 0)))
    if request.sort_by == "distance_asc": return sorted(hotels, key=lambda h: (h.distance_from_landmark_km if h.distance_from_landmark_km is not None else float("inf"), h.price_per_night))

    prices = [h.price_per_night for h in hotels]
    distances = [h.distance_from_landmark_km for h in hotels if h.distance_from_landmark_km is not None]
    ranked: list[Hotel] = []
    requested_amenities = {a.casefold() for a in request.amenities}
    for hotel in hotels:
        preference = 0.5 + (0.25 if request.breakfast_included and hotel.breakfast_included else 0) + (0.25 if request.free_cancellation and hotel.free_cancellation else 0)
        amenity_match = 1.0 if not requested_amenities else len(requested_amenities & {a.casefold() for a in hotel.amenities}) / len(requested_amenities)
        score = (0.35 * _norm(hotel.guest_rating, 0, 10) + 0.20 * (1 - _norm(hotel.price_per_night, min(prices), max(prices))) + 0.20 * min(1.0, preference) + 0.15 * amenity_match + 0.10 * (1 - _norm(hotel.distance_from_landmark_km, min(distances), max(distances)) if distances else 0.5))
        ranked.append(replace(hotel, recommendation_score=round(score, 3), recommendation_reason="Balanced guest rating, price, and requested preferences."))
    return sorted(ranked, key=lambda h: (-(h.recommendation_score or 0), h.price_per_night, h.name))
