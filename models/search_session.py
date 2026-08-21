from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from .hotel import Hotel
from .search_request import SearchRequest


@dataclass
class SearchSession:
    conversation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    request: SearchRequest | None = None
    results: tuple[Hotel, ...] = ()
    selected_hotel_ids: tuple[str, ...] = ()
    history: list[dict[str, str]] = field(default_factory=list)

    def update_request(self, **overrides) -> None:
        if self.request is None:
            return
        from dataclasses import replace
        self.request = replace(self.request, **overrides)

    def select_hotel(self, hotel_id: str) -> None:
        ids = set(self.selected_hotel_ids)
        if hotel_id in ids:
            ids.discard(hotel_id)
        else:
            ids.add(hotel_id)
        self.selected_hotel_ids = tuple(ids)

    def get_selected_hotels(self) -> list[Hotel]:
        id_set = set(self.selected_hotel_ids)
        return [h for h in self.results if h.hotel_id in id_set]

    def add_message(self, role: str, content: str) -> None:
        self.history.append({"role": role, "content": content})
