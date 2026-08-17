from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Hotel:
    hotel_id: str
    name: str
    city: str
    country: str
    latitude: float | None
    longitude: float | None
    star_rating: float | None
    guest_rating: float | None
    price_per_night: float
    currency: str
    room_type: str
    amenities: tuple[str, ...] = field(default_factory=tuple)
    property_type: str = "hotel"
    free_cancellation: bool = False
    breakfast_included: bool = False
    availability: bool = True
    distance_from_center_km: float | None = None
    distance_from_landmark_km: float | None = None
    booking_options: tuple[str, ...] = field(default_factory=tuple)
    recommendation_score: float | None = None
    recommendation_reason: str | None = None
    labels: tuple[str, ...] = field(default_factory=tuple)

