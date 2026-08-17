"""Streamlit presentation layer for the deterministic hotel search demo."""
from __future__ import annotations

from datetime import date, timedelta

import streamlit as st

from models.search_request import SearchRequest
from providers.mock_provider import DeterministicMockHotelProvider
from services.search_service import SearchService, SearchValidationError


st.set_page_config(page_title="HotelFinder Pro", layout="wide")

if "provider" not in st.session_state:
    st.session_state.provider = DeterministicMockHotelProvider()
    st.session_state.search_service = SearchService(st.session_state.provider)
    st.session_state.result = None
    st.session_state.last_request = None
    st.session_state.compared = set()


def build_request() -> SearchRequest:
    return SearchRequest(
        location=st.session_state.location,
        check_in=st.session_state.check_in,
        check_out=st.session_state.check_out,
        adults=st.session_state.adults,
        children=st.session_state.children,
        rooms=st.session_state.rooms,
        currency=st.session_state.currency,
        min_price=st.session_state.min_price or None,
        max_price=st.session_state.max_price or None,
        min_star_rating=st.session_state.min_stars or None,
        min_guest_rating=st.session_state.min_guest_rating or None,
        amenities=tuple(st.session_state.amenities),
        property_types=tuple(st.session_state.property_types),
        free_cancellation=True if st.session_state.free_cancellation else None,
        breakfast_included=True if st.session_state.breakfast else None,
        landmark=st.session_state.landmark.strip() or None,
        radius_km=st.session_state.radius_km if st.session_state.landmark.strip() else None,
        sort_by=st.session_state.sort_by,
    )


def run_search() -> None:
    try:
        request = build_request()
        st.session_state.result = st.session_state.search_service.search(request)
        st.session_state.last_request = request
        st.session_state.compared = set()
    except SearchValidationError as exc:
        for message in exc.errors.values():
            st.error(message)


st.title("HotelFinder Pro")
st.caption("Deterministic hotel search and ranking demo")
st.info("Demo inventory only — prices and availability are generated for testing, not live supplier data.")

with st.form("hotel-search"):
    first, second, third = st.columns(3)
    with first:
        st.text_input("Location", placeholder="e.g. Paris", key="location")
        st.date_input("Check-in", min_value=date.today(), value=date.today(), key="check_in")
        st.number_input("Adults", min_value=1, max_value=16, value=2, key="adults")
        st.number_input("Children", min_value=0, max_value=12, value=0, key="children")
    with second:
        st.date_input("Check-out", min_value=date.today(), value=date.today() + timedelta(days=1), key="check_out")
        st.number_input("Rooms", min_value=1, max_value=4, value=1, key="rooms")
        st.selectbox("Currency", ["EUR", "USD", "GBP", "INR"], key="currency")
        st.selectbox("Sort", ["recommended", "price_asc", "price_desc", "rating_desc", "stars_desc", "distance_asc"], format_func=lambda v: v.replace("_", " ").title(), key="sort_by")
    with third:
        st.number_input("Minimum price / night", min_value=0.0, value=0.0, step=10.0, key="min_price")
        st.number_input("Maximum price / night", min_value=0.0, value=0.0, step=10.0, key="max_price")
        st.selectbox("Minimum star rating", [0, 1, 2, 3, 4, 5], key="min_stars")
        st.number_input("Minimum guest rating", min_value=0.0, max_value=10.0, value=0.0, step=0.5, key="min_guest_rating")
    filters, proximity = st.columns(2)
    with filters:
        st.multiselect("Amenities", ["wifi", "breakfast", "pool", "spa", "gym", "parking", "pet-friendly", "air conditioning"], key="amenities")
        st.multiselect("Property type", ["hotel", "resort", "aparthotel", "boutique"], key="property_types")
        st.checkbox("Free cancellation", key="free_cancellation")
        st.checkbox("Breakfast included", key="breakfast")
    with proximity:
        st.text_input("Landmark (optional)", key="landmark")
        st.number_input("Radius from landmark (km)", min_value=0.1, value=3.0, step=0.5, key="radius_km")
    submitted = st.form_submit_button("Search hotels", type="primary")

if submitted:
    run_search()

result = st.session_state.result
if result is not None:
    request = st.session_state.last_request
    st.subheader(f"{result.total_matches} hotel(s) found in {request.location.strip()}")
    st.caption(f"Request {result.request_id} · {result.source.replace('_', ' ')} · {result.latency_ms} ms")
    nights = (request.check_out - request.check_in).days
    if not result.hotels:
        st.warning("No exact matches found. Relax a filter to broaden the deterministic demo inventory.")
    for hotel in result.hotels:
        with st.container(border=True):
            title, compare = st.columns([5, 1])
            with title:
                st.markdown(f"### {hotel.name}")
                st.write(f"{hotel.city} · {'★' * int(hotel.star_rating or 0)} · Guest rating {hotel.guest_rating}/10")
            with compare:
                st.checkbox("Compare", key=f"compare-{hotel.hotel_id}", value=hotel.hotel_id in st.session_state.compared, on_change=lambda h=hotel.hotel_id: st.session_state.compared.symmetric_difference_update({h}))
            st.write(f"**{hotel.currency} {hotel.price_per_night:.0f} / night** · {hotel.currency} {hotel.price_per_night * nights:.0f} for {nights} night(s) (taxes and fees unavailable)")
            st.write(f"{hotel.room_type} · {'Breakfast included' if hotel.breakfast_included else 'No breakfast'} · {'Free cancellation' if hotel.free_cancellation else 'Non-refundable'}")
            st.write("Amenities: " + ", ".join(hotel.amenities))
            if hotel.distance_from_landmark_km is not None: st.write(f"{hotel.distance_from_landmark_km:.1f} km from {request.landmark}")
            if hotel.labels: st.caption(" · ".join(hotel.labels))

    selected = [hotel for hotel in result.hotels if hotel.hotel_id in st.session_state.compared]
    if selected:
        st.subheader("Comparison")
        if len(selected) > 3: st.warning("Choose up to three hotels for a readable comparison.")
        else:
            st.dataframe({"Hotel": [h.name for h in selected], "Price/night": [f"{h.currency} {h.price_per_night:.0f}" for h in selected], "Total": [f"{h.currency} {h.price_per_night * nights:.0f}" for h in selected], "Guest rating": [h.guest_rating for h in selected], "Stars": [h.star_rating for h in selected], "Breakfast": [h.breakfast_included for h in selected], "Free cancellation": [h.free_cancellation for h in selected], "Amenities": [", ".join(h.amenities) for h in selected]}, hide_index=True, use_container_width=True)
