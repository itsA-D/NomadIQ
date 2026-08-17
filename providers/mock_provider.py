from __future__ import annotations

import hashlib
from dataclasses import replace

from models.hotel import Hotel
from models.search_request import SearchRequest

from .base import HotelProvider


class DeterministicMockHotelProvider(HotelProvider):
    """Demo inventory derived from the submitted city, never stale sample results.

    It is intentionally not a live supplier: prices and availability are generated
    deterministically for demos/tests and identified as such by ``source``.
    """

    source = "deterministic_demo_inventory"

    _profiles = (
        ("Central", 3.0, 7.8, 79, "Standard Queen", ("wifi", "air conditioning"), False, False, 2.4, "hotel"),
        ("Riverside", 4.0, 8.5, 119, "Deluxe King", ("wifi", "breakfast", "gym", "air conditioning"), True, True, 1.1, "hotel"),
        ("Grand", 5.0, 9.1, 189, "Executive King", ("wifi", "breakfast", "pool", "spa", "gym", "parking"), True, True, 0.7, "resort"),
        ("Garden", 4.0, 8.8, 149, "Family Suite", ("wifi", "breakfast", "parking", "pet-friendly"), True, True, 3.2, "aparthotel"),
        ("Metro", 3.0, 8.1, 99, "Double Room", ("wifi", "gym"), True, False, 1.8, "hotel"),
        ("Boutique", 4.0, 9.0, 169, "Superior Room", ("wifi", "breakfast", "spa", "air conditioning"), False, True, 0.9, "boutique"),
    )

    def __init__(self) -> None:
        self._last_hotels: dict[str, Hotel] = {}

    def search(self, request: SearchRequest) -> list[Hotel]:
        city = " ".join(part.capitalize() for part in request.location.strip().split())
        seed = int(hashlib.sha256(city.casefold().encode()).hexdigest()[:8], 16)
        hotels: list[Hotel] = []
        for index, profile in enumerate(self._profiles):
            prefix, stars, rating, base_price, room, amenities, cancel, breakfast, distance, property_type = profile
            variation = ((seed >> (index * 3)) % 21) - 10
            hotel = Hotel(
                hotel_id=f"demo-{hashlib.sha1(city.casefold().encode()).hexdigest()[:8]}-{index}",
                name=f"{city} {prefix} Hotel",
                city=city,
                country="Demo destination",
                latitude=None,
                longitude=None,
                star_rating=stars,
                guest_rating=rating,
                price_per_night=float(max(45, base_price + variation)),
                currency=request.currency,
                room_type=room,
                amenities=amenities,
                property_type=property_type,
                free_cancellation=cancel,
                breakfast_included=breakfast,
                availability=True,
                distance_from_center_km=distance,
                distance_from_landmark_km=distance if request.landmark else None,
                booking_options=("Demo rate",),
            )
            hotels.append(hotel)
            self._last_hotels[hotel.hotel_id] = hotel
        return hotels

    def get_hotel(self, hotel_id: str) -> Hotel | None:
        return self._last_hotels.get(hotel_id)

    def check_availability(self, hotel_id: str, request: SearchRequest) -> bool:
        hotel = self._last_hotels.get(hotel_id)
        return bool(hotel and hotel.availability and request.adults <= request.rooms * 4)
