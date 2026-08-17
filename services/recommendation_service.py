from __future__ import annotations

from dataclasses import replace

from models.hotel import Hotel


def add_recommendation_labels(hotels: list[Hotel]) -> list[Hotel]:
    if not hotels: return []
    labels: dict[str, list[str]] = {hotel.hotel_id: [] for hotel in hotels}
    labels[hotels[0].hotel_id].append("Best Overall")
    labels[min(hotels, key=lambda h: h.price_per_night).hotel_id].append("Lowest Price")
    labels[max(hotels, key=lambda h: h.guest_rating or 0).hotel_id].append("Highest Rated")
    distance_candidates = [h for h in hotels if h.distance_from_landmark_km is not None]
    if distance_candidates: labels[min(distance_candidates, key=lambda h: h.distance_from_landmark_km or 0).hotel_id].append("Closest")
    best_value = max(hotels, key=lambda h: ((h.guest_rating or 0) * 10) / h.price_per_night)
    labels[best_value.hotel_id].append("Best Value")
    return [replace(hotel, labels=tuple(labels[hotel.hotel_id])) for hotel in hotels]
