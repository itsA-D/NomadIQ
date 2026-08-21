from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import date

from .hotel import Hotel
from .search_request import SearchRequest


@dataclass(frozen=True)
class BookingGuest:
    first_name: str
    last_name: str
    email: str
    phone: str = ""


@dataclass(frozen=True)
class Booking:
    booking_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12].upper())
    hotel: Hotel | None = None
    request: SearchRequest | None = None
    guest: BookingGuest | None = None
    check_in: date | None = None
    check_out: date | None = None
    nights: int = 0
    price_per_night: float = 0.0
    total_price: float = 0.0
    currency: str = "EUR"
    status: str = "pending"
    created_at: str = ""

    @staticmethod
    def create(hotel: Hotel, request: SearchRequest, guest: BookingGuest) -> Booking:
        from datetime import datetime
        nights = (request.check_out - request.check_in).days
        total = hotel.price_per_night * nights
        return Booking(
            hotel=hotel,
            request=request,
            guest=guest,
            check_in=request.check_in,
            check_out=request.check_out,
            nights=nights,
            price_per_night=hotel.price_per_night,
            total_price=total,
            currency=hotel.currency,
            status="confirmed",
            created_at=datetime.now().isoformat(timespec="seconds"),
        )
