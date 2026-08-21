"""Deterministic backend tools exposed for the agent layer.

Every function here is pure Python — no LLM involvement.
The agent calls these tools and receives structured results.
"""
from __future__ import annotations

import json
from dataclasses import asdict
from datetime import date

from models.hotel import Hotel
from models.search_request import SearchRequest
from models.search_session import SearchSession
from providers.mock_provider import DeterministicMockHotelProvider
from services.search_service import SearchService, SearchValidationError
from services.booking_service import BookingService, BookingGuest


_provider = DeterministicMockHotelProvider()
_search = SearchService(_provider)
_booking = BookingService()


def search_hotels(
    location: str,
    check_in: str,
    check_out: str,
    adults: int = 2,
    children: int = 0,
    rooms: int = 1,
    currency: str = "EUR",
    min_price: float | None = None,
    max_price: float | None = None,
    min_star_rating: float | None = None,
    min_guest_rating: float | None = None,
    amenities: str = "",
    free_cancellation: bool | None = None,
    breakfast_included: bool | None = None,
    landmark: str | None = None,
    sort_by: str = "recommended",
) -> str:
    """Search hotels using deterministic backend. Returns JSON string."""
    amenity_list = tuple(a.strip() for a in amenities.split(",") if a.strip()) if amenities else ()
    request = SearchRequest(
        location=location,
        check_in=date.fromisoformat(check_in),
        check_out=date.fromisoformat(check_out),
        adults=adults,
        children=children,
        rooms=rooms,
        currency=currency,
        min_price=min_price,
        max_price=max_price,
        min_star_rating=min_star_rating,
        min_guest_rating=min_guest_rating,
        amenities=amenity_list,
        free_cancellation=free_cancellation,
        breakfast_included=breakfast_included,
        landmark=landmark,
        sort_by=sort_by,
    )
    try:
        result = _search.search(request)
    except SearchValidationError as e:
        return json.dumps({"error": True, "errors": e.errors})
    hotels_data = []
    for h in result.hotels:
        hotels_data.append({
            "hotel_id": h.hotel_id,
            "name": h.name,
            "city": h.city,
            "star_rating": h.star_rating,
            "guest_rating": h.guest_rating,
            "price_per_night": h.price_per_night,
            "currency": h.currency,
            "room_type": h.room_type,
            "amenities": list(h.amenities),
            "free_cancellation": h.free_cancellation,
            "breakfast_included": h.breakfast_included,
            "distance_from_center_km": h.distance_from_center_km,
            "labels": list(h.labels),
            "recommendation_score": h.recommendation_score,
        })
    return json.dumps({
        "total_matches": result.total_matches,
        "hotels": hotels_data,
        "source": result.source,
        "latency_ms": result.latency_ms,
    })


def get_hotel_details(hotel_id: str) -> str:
    """Get details for a specific hotel."""
    hotel = _provider.get_hotel(hotel_id)
    if hotel is None:
        return json.dumps({"error": "Hotel not found"})
    return json.dumps({
        "hotel_id": hotel.hotel_id,
        "name": hotel.name,
        "city": hotel.city,
        "country": hotel.country,
        "star_rating": hotel.star_rating,
        "guest_rating": hotel.guest_rating,
        "price_per_night": hotel.price_per_night,
        "currency": hotel.currency,
        "room_type": hotel.room_type,
        "amenities": list(hotel.amenities),
        "property_type": hotel.property_type,
        "free_cancellation": hotel.free_cancellation,
        "breakfast_included": hotel.breakfast_included,
        "availability": hotel.availability,
        "distance_from_center_km": hotel.distance_from_center_km,
    })


def compare_hotels(hotel_ids: str) -> str:
    """Compare up to 3 hotels side by side. Comma-separated IDs."""
    ids = [h.strip() for h in hotel_ids.split(",") if h.strip()]
    if len(ids) < 2:
        return json.dumps({"error": "Provide at least 2 hotel IDs"})
    if len(ids) > 3:
        return json.dumps({"error": "Compare up to 3 hotels at a time"})
    hotels = []
    for hid in ids:
        h = _provider.get_hotel(hid)
        if h:
            hotels.append({
                "name": h.name,
                "price_per_night": h.price_per_night,
                "currency": h.currency,
                "star_rating": h.star_rating,
                "guest_rating": h.guest_rating,
                "amenities": list(h.amenities),
                "free_cancellation": h.free_cancellation,
                "breakfast_included": h.breakfast_included,
                "room_type": h.room_type,
                "distance_from_center_km": h.distance_from_center_km,
            })
    return json.dumps({"compared_hotels": hotels})


def calculate_price(hotel_id: str, check_in: str, check_out: str) -> str:
    """Calculate total price for a hotel stay."""
    hotel = _provider.get_hotel(hotel_id)
    if hotel is None:
        return json.dumps({"error": "Hotel not found"})
    nights = (date.fromisoformat(check_out) - date.fromisoformat(check_in)).days
    total = hotel.price_per_night * nights
    return json.dumps({
        "hotel_name": hotel.name,
        "price_per_night": hotel.price_per_night,
        "currency": hotel.currency,
        "nights": nights,
        "total_price": round(total, 2),
    })
