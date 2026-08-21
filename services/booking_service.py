"""Booking workflow service.

Handles room selection, availability re-check, price calculation,
guest details, and booking confirmation.
"""
from __future__ import annotations

import logging
from datetime import date

from models.booking import Booking, BookingGuest
from models.hotel import Hotel
from models.search_request import SearchRequest
from providers.base import HotelProvider
from providers.mock_provider import DeterministicMockHotelProvider

logger = logging.getLogger(__name__)


class BookingService:
    def __init__(self, provider: HotelProvider | None = None) -> None:
        self._provider = provider or DeterministicMockHotelProvider()
        self._bookings: dict[str, Booking] = {}

    def _ensure_hotel(self, hotel_id: str, request: SearchRequest) -> Hotel | None:
        """Get hotel from cache or re-search to populate provider cache."""
        hotel = self._provider.get_hotel(hotel_id)
        if hotel is not None:
            return hotel
        # Provider cache miss — run a search to populate it
        self._provider.search(request)
        return self._provider.get_hotel(hotel_id)

    def check_availability(self, hotel_id: str, request: SearchRequest) -> dict:
        """Re-check availability and price before booking."""
        hotel = self._ensure_hotel(hotel_id, request)
        if hotel is None:
            return {"available": False, "reason": "Hotel not found"}
        available = self._provider.check_availability(hotel_id, request)
        nights = (request.check_out - request.check_in).days
        return {
            "available": available,
            "hotel_id": hotel.hotel_id,
            "hotel_name": hotel.name,
            "price_per_night": hotel.price_per_night,
            "currency": hotel.currency,
            "nights": nights,
            "total_price": round(hotel.price_per_night * nights, 2),
            "room_type": hotel.room_type,
            "free_cancellation": hotel.free_cancellation,
            "breakfast_included": hotel.breakfast_included,
        }

    def create_booking(
        self, hotel_id: str, request: SearchRequest, guest: BookingGuest
    ) -> Booking:
        """Create a confirmed booking record."""
        hotel = self._ensure_hotel(hotel_id, request)
        if hotel is None:
            raise ValueError(f"Hotel {hotel_id} not found")

        avail = self._provider.check_availability(hotel_id, request)
        if not avail:
            raise ValueError("Hotel is no longer available for the requested dates")

        booking = Booking.create(hotel=hotel, request=request, guest=guest)
        self._bookings[booking.booking_id] = booking
        logger.info("Booking created: %s for %s", booking.booking_id, hotel.name)
        return booking

    def get_booking(self, booking_id: str) -> Booking | None:
        return self._bookings.get(booking_id)

    def get_booking_summary(self, booking: Booking) -> str:
        """Format a booking confirmation as readable text."""
        if booking.hotel is None or booking.guest is None:
            return "Incomplete booking"
        h = booking.hotel
        g = booking.guest
        return (
            f"Booking Confirmed — {booking.booking_id}\n\n"
            f"Hotel: {h.name} ({h.room_type})\n"
            f"Location: {h.city}\n"
            f"Check-in: {booking.check_in}\n"
            f"Check-out: {booking.check_out}\n"
            f"Nights: {booking.nights}\n"
            f"Price: {booking.currency} {booking.price_per_night:.0f}/night\n"
            f"Total: {booking.currency} {booking.total_price:.0f}\n"
            f"{'Free cancellation' if h.free_cancellation else 'Non-refundable'}\n"
            f"{'Breakfast included' if h.breakfast_included else 'No breakfast'}\n\n"
            f"Guest: {g.first_name} {g.last_name}\n"
            f"Email: {g.email}\n"
        )
