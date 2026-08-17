from __future__ import annotations

from dataclasses import dataclass

from .hotel import Hotel


@dataclass(frozen=True)
class SearchResult:
    request_id: str
    hotels: tuple[Hotel, ...]
    total_matches: int
    applied_filters: dict[str, object]
    source: str
    latency_ms: int

