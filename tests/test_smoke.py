"""Smoke test for new feature modules."""
import json
from datetime import date

from models.search_request import SearchRequest
from models.search_session import SearchSession
from models.booking import Booking, BookingGuest
from agents.tools import search_hotels, compare_hotels, calculate_price
from services.booking_service import BookingService
from providers.mock_provider import DeterministicMockHotelProvider


class TestAgentTools:
    def test_search_hotels(self):
        result = search_hotels("Paris", "2026-08-17", "2026-08-20", adults=2)
        data = json.loads(result)
        assert data["total_matches"] > 0
        assert len(data["hotels"]) == 6

    def test_compare_hotels(self):
        result = search_hotels("Paris", "2026-08-17", "2026-08-20")
        data = json.loads(result)
        ids = ",".join(h["hotel_id"] for h in data["hotels"][:2])
        comp = json.loads(compare_hotels(ids))
        assert len(comp["compared_hotels"]) == 2

    def test_calculate_price(self):
        result = search_hotels("Paris", "2026-08-17", "2026-08-20")
        data = json.loads(result)
        hid = data["hotels"][0]["hotel_id"]
        price = json.loads(calculate_price(hid, "2026-08-17", "2026-08-20"))
        assert price["nights"] == 3
        assert price["total_price"] > 0


class TestSearchSession:
    def test_session_lifecycle(self):
        session = SearchSession()
        assert session.conversation_id
        session.update_request(location="London")
        session.select_hotel("abc")
        assert "abc" in session.selected_hotel_ids
        session.select_hotel("abc")  # toggle off
        assert "abc" not in session.selected_hotel_ids
        session.add_message("user", "hello")
        assert len(session.history) == 1


class TestBookingService:
    def test_booking_lifecycle(self):
        provider = DeterministicMockHotelProvider()
        bs = BookingService(provider)
        req = SearchRequest("Paris", date(2026, 8, 17), date(2026, 8, 20), adults=2)
        result = provider.search(req)
        hid = result[0].hotel_id
        avail = bs.check_availability(hid, req)
        assert avail["available"]
        guest = BookingGuest("John", "Doe", "john@test.com", "+1234")
        booking = bs.create_booking(hid, req, guest)
        assert booking.status == "confirmed"
        assert booking.nights == 3
        summary = bs.get_booking_summary(booking)
        assert "John Doe" in summary
        assert booking.booking_id in summary
