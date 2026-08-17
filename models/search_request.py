from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Any


@dataclass(frozen=True)
class SearchRequest:
    location: str
    check_in: date
    check_out: date
    adults: int = 1
    children: int = 0
    rooms: int = 1
    currency: str = "EUR"
    min_price: float | None = None
    max_price: float | None = None
    min_star_rating: float | None = None
    min_guest_rating: float | None = None
    amenities: tuple[str, ...] = field(default_factory=tuple)
    property_types: tuple[str, ...] = field(default_factory=tuple)
    free_cancellation: bool | None = None
    breakfast_included: bool | None = None
    landmark: str | None = None
    radius_km: float | None = None
    sort_by: str = "recommended"

    def log_fields(self) -> dict[str, Any]:
        """Safe, serializable representation for logs and cache keys."""
        data = asdict(self)
        data["check_in"] = self.check_in.isoformat()
        data["check_out"] = self.check_out.isoformat()
        return data

