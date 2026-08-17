from __future__ import annotations

from abc import ABC, abstractmethod

from models.hotel import Hotel
from models.search_request import SearchRequest


class HotelProvider(ABC):
    """A provider supplies inventory; business rules stay outside this layer."""

    source: str

    @abstractmethod
    def search(self, request: SearchRequest) -> list[Hotel]: ...

    @abstractmethod
    def get_hotel(self, hotel_id: str) -> Hotel | None: ...

    @abstractmethod
    def check_availability(self, hotel_id: str, request: SearchRequest) -> bool: ...

