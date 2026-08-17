from datetime import date
import unittest

from models.search_request import SearchRequest
from providers.base import HotelProvider
from providers.mock_provider import DeterministicMockHotelProvider
from services.search_service import SearchService


class EmptyProvider(HotelProvider):
    source = "empty"

    def search(self, request): return []
    def get_hotel(self, hotel_id): return None
    def check_availability(self, hotel_id, request): return False


class SearchPipelineAuditTests(unittest.TestCase):
    def setUp(self):
        self.service = SearchService(DeterministicMockHotelProvider())
        self.base = dict(location="Paris", check_in=date(2026, 8, 17), check_out=date(2026, 8, 20), adults=2, rooms=1)

    def search(self, **changes):
        return self.service.search(SearchRequest(**(self.base | changes)))

    def test_another_city_is_not_mixed_with_previous_city(self):
        paris = self.search()
        london = self.search(location="London")
        self.assertTrue(all(h.city == "Paris" for h in paris.hotels))
        self.assertTrue(all(h.city == "London" for h in london.hotels))
        self.assertTrue({h.hotel_id for h in paris.hotels}.isdisjoint({h.hotel_id for h in london.hotels}))

    def test_each_implemented_filter_is_satisfied(self):
        result = self.search(max_price=200, min_star_rating=4, min_guest_rating=8.5, amenities=("wifi", "breakfast"), breakfast_included=True, free_cancellation=True, property_types=("hotel",))
        self.assertTrue(result.hotels)
        for hotel in result.hotels:
            self.assertLessEqual(hotel.price_per_night, 200)
            self.assertGreaterEqual(hotel.star_rating, 4)
            self.assertGreaterEqual(hotel.guest_rating, 8.5)
            self.assertTrue({"wifi", "breakfast"}.issubset(hotel.amenities))
            self.assertTrue(hotel.breakfast_included)
            self.assertTrue(hotel.free_cancellation)
            self.assertEqual(hotel.property_type, "hotel")
            self.assertTrue(hotel.availability)

    def test_sort_modes_use_hotel_values(self):
        for mode, key in (("price_asc", lambda h: h.price_per_night), ("price_desc", lambda h: -h.price_per_night), ("rating_desc", lambda h: -(h.guest_rating or 0)), ("stars_desc", lambda h: (-(h.star_rating or 0), -(h.guest_rating or 0)))):
            hotels = self.search(sort_by=mode).hotels
            self.assertEqual(list(hotels), sorted(hotels, key=key))

    def test_comparison_input_is_the_same_canonical_search_objects(self):
        result = self.search()
        selected_ids = {result.hotels[0].hotel_id, result.hotels[1].hotel_id}
        selected = [hotel for hotel in result.hotels if hotel.hotel_id in selected_ids]
        self.assertIs(selected[0], result.hotels[0])
        self.assertIs(selected[1], result.hotels[1])

    def test_provider_no_results_is_a_real_empty_result(self):
        request = SearchRequest(**self.base)
        result = SearchService(EmptyProvider()).search(request)
        self.assertEqual(result.hotels, ())
        self.assertEqual(result.total_matches, 0)
        self.assertEqual(result.source, "empty")

