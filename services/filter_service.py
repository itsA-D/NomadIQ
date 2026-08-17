from __future__ import annotations

from collections.abc import Iterable

from models.hotel import Hotel
from models.search_request import SearchRequest


def filter_by_price(hotels: Iterable[Hotel], request: SearchRequest) -> list[Hotel]:
    return [h for h in hotels if (request.min_price is None or h.price_per_night >= request.min_price) and (request.max_price is None or h.price_per_night <= request.max_price)]

def filter_by_star_rating(hotels: Iterable[Hotel], request: SearchRequest) -> list[Hotel]:
    return [h for h in hotels if request.min_star_rating is None or (h.star_rating or 0) >= request.min_star_rating]

def filter_by_guest_rating(hotels: Iterable[Hotel], request: SearchRequest) -> list[Hotel]:
    return [h for h in hotels if request.min_guest_rating is None or (h.guest_rating or 0) >= request.min_guest_rating]

def filter_by_amenities(hotels: Iterable[Hotel], request: SearchRequest) -> list[Hotel]:
    wanted = {a.casefold() for a in request.amenities}
    return [h for h in hotels if wanted.issubset({a.casefold() for a in h.amenities})]

def filter_by_property_type(hotels: Iterable[Hotel], request: SearchRequest) -> list[Hotel]:
    wanted = {p.casefold() for p in request.property_types}
    return [h for h in hotels if not wanted or h.property_type.casefold() in wanted]

def filter_by_cancellation(hotels: Iterable[Hotel], request: SearchRequest) -> list[Hotel]:
    return [h for h in hotels if request.free_cancellation is not True or h.free_cancellation]

def filter_by_breakfast(hotels: Iterable[Hotel], request: SearchRequest) -> list[Hotel]:
    return [h for h in hotels if request.breakfast_included is not True or h.breakfast_included]

def filter_by_distance(hotels: Iterable[Hotel], request: SearchRequest) -> list[Hotel]:
    return [h for h in hotels if request.radius_km is None or (h.distance_from_landmark_km is not None and h.distance_from_landmark_km <= request.radius_km)]

def filter_by_availability(hotels: Iterable[Hotel], request: SearchRequest) -> list[Hotel]:
    return [h for h in hotels if h.availability]

def apply_filters(hotels: Iterable[Hotel], request: SearchRequest) -> list[Hotel]:
    result = filter_by_availability(hotels, request)
    for operation in (filter_by_price, filter_by_star_rating, filter_by_guest_rating, filter_by_amenities, filter_by_property_type, filter_by_cancellation, filter_by_breakfast, filter_by_distance):
        result = operation(result, request)
    return result
