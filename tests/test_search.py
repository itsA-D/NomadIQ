from datetime import date
import unittest

from models.search_request import SearchRequest
from providers.mock_provider import DeterministicMockHotelProvider
from services.search_service import SearchService, SearchValidationError


class SearchServiceTests(unittest.TestCase):
    def setUp(self): self.service = SearchService(DeterministicMockHotelProvider())

    def test_paris_request_never_returns_another_city(self):
        request = SearchRequest("Paris", date(2026, 8, 17), date(2026, 8, 18), adults=2)
        result = self.service.search(request)
        self.assertGreater(result.total_matches, 1)
        self.assertTrue(all(hotel.city == "Paris" for hotel in result.hotels))
        self.assertEqual(result.applied_filters["check_in"], "2026-08-17")
        self.assertEqual(result.applied_filters["adults"], 2)

    def test_combined_filters_are_applied(self):
        request = SearchRequest("Paris", date(2026, 8, 17), date(2026, 8, 20), adults=2, max_price=200, min_star_rating=4, breakfast_included=True, free_cancellation=True)
        result = self.service.search(request)
        self.assertTrue(result.hotels)
        self.assertTrue(all(h.star_rating >= 4 and h.price_per_night <= 200 and h.breakfast_included and h.free_cancellation for h in result.hotels))

    def test_invalid_dates_return_structured_errors(self):
        request = SearchRequest("Paris", date(2026, 8, 18), date(2026, 8, 18))
        with self.assertRaises(SearchValidationError) as raised: self.service.search(request)
        self.assertIn("dates", raised.exception.errors)

