from __future__ import annotations

import logging
import time
import uuid

from models.search_result import SearchResult
from models.search_request import SearchRequest
from providers.base import HotelProvider
from .filter_service import apply_filters
from .ranking_service import rank_hotels
from .recommendation_service import add_recommendation_labels
from .validation import validate_search_request

logger = logging.getLogger(__name__)


class SearchValidationError(ValueError):
    def __init__(self, errors: dict[str, str]) -> None:
        super().__init__("Invalid search request")
        self.errors = errors


class SearchService:
    def __init__(self, provider: HotelProvider) -> None:
        self.provider = provider

    def search(self, request: SearchRequest) -> SearchResult:
        errors = validate_search_request(request)
        if errors: raise SearchValidationError(errors)
        started = time.perf_counter()
        request_id = str(uuid.uuid4())
        retrieved = self.provider.search(request)
        # A defensive location check prevents a provider from leaking unrelated results.
        location = request.location.strip().casefold()
        normalized = [hotel for hotel in retrieved if hotel.city.casefold() == location and hotel.price_per_night >= 0]
        filtered = apply_filters(normalized, request)
        hotels = tuple(add_recommendation_labels(rank_hotels(filtered, request)))
        latency_ms = round((time.perf_counter() - started) * 1000)
        logger.info("hotel_search", extra={"request_id": request_id, "search_request": request.log_fields(), "provider": self.provider.source, "retrieved_count": len(retrieved), "filtered_count": len(filtered), "returned_count": len(hotels), "total_latency_ms": latency_ms})
        return SearchResult(request_id, hotels, len(hotels), request.log_fields(), self.provider.source, latency_ms)
