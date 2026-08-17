from __future__ import annotations

from models.search_request import SearchRequest


SUPPORTED_CURRENCIES = {"EUR", "USD", "GBP", "INR"}
SORT_MODES = {"recommended", "price_asc", "price_desc", "rating_desc", "stars_desc", "distance_asc"}


def validate_search_request(request: SearchRequest) -> dict[str, str]:
    errors: dict[str, str] = {}
    if not request.location.strip(): errors["location"] = "Location is required."
    if request.check_out <= request.check_in: errors["dates"] = "Check-out must be after check-in."
    if request.adults < 1: errors["adults"] = "At least one adult is required."
    if request.children < 0: errors["children"] = "Children cannot be negative."
    if request.rooms < 1: errors["rooms"] = "At least one room is required."
    if request.adults > request.rooms * 4: errors["occupancy"] = "This demo supports at most four guests per room."
    if request.min_price is not None and request.max_price is not None and request.min_price > request.max_price: errors["price"] = "Minimum price cannot exceed maximum price."
    if request.min_star_rating is not None and not 1 <= request.min_star_rating <= 5: errors["star_rating"] = "Star rating must be between 1 and 5."
    if request.min_guest_rating is not None and not 0 <= request.min_guest_rating <= 10: errors["guest_rating"] = "Guest rating must be between 0 and 10."
    if request.radius_km is not None and request.radius_km <= 0: errors["radius"] = "Radius must be greater than zero."
    if request.currency not in SUPPORTED_CURRENCIES: errors["currency"] = "Unsupported currency."
    if request.sort_by not in SORT_MODES: errors["sort"] = "Unsupported sort mode."
    return errors
