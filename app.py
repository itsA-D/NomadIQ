"""HotelFinder Pro — Agentic hotel search with NL + form modes."""
from __future__ import annotations

import json
from datetime import date, timedelta

import streamlit as st

from models.search_request import SearchRequest
from models.search_session import SearchSession
from models.booking import BookingGuest
from providers.mock_provider import DeterministicMockHotelProvider
from services.search_service import SearchService, SearchValidationError
from services.booking_service import BookingService
from agents.planner import (
    extract_intent,
    build_search_request_from_intent,
    generate_clarification,
    generate_response,
)
from agents.tools import search_hotels, compare_hotels, calculate_price

st.set_page_config(page_title="HotelFinder Pro", layout="wide")

# ── Session state ──────────────────────────────────────────────────
if "provider" not in st.session_state:
    st.session_state.provider = DeterministicMockHotelProvider()
    st.session_state.search_service = SearchService(st.session_state.provider)
    st.session_state.booking_service = BookingService(st.session_state.provider)
    st.session_state.session = SearchSession()
    st.session_state.result = None
    st.session_state.last_request = None
    st.session_state.compared = set()
    st.session_state.chat_history = []
    st.state_booking = None

ss = st.session_state


# ── Helpers ────────────────────────────────────────────────────────
def build_request(**overrides) -> SearchRequest:
    base = {
        "location": ss.get("location", ""),
        "check_in": ss.get("check_in", date.today()),
        "check_out": ss.get("check_out", date.today() + timedelta(days=1)),
        "adults": ss.get("adults", 2),
        "children": ss.get("children", 0),
        "rooms": ss.get("rooms", 1),
        "currency": ss.get("currency", "EUR"),
        "min_price": ss.get("min_price") or None,
        "max_price": ss.get("max_price") or None,
        "min_star_rating": ss.get("min_stars") or None,
        "min_guest_rating": ss.get("min_guest_rating") or None,
        "amenities": tuple(ss.get("amenities", ())),
        "property_types": tuple(ss.get("property_types", ())),
        "free_cancellation": True if ss.get("free_cancellation") else None,
        "breakfast_included": True if ss.get("breakfast") else None,
        "landmark": (ss.get("landmark") or "").strip() or None,
        "radius_km": ss.get("radius_km") if (ss.get("landmark") or "").strip() else None,
        "sort_by": ss.get("sort_by", "recommended"),
    }
    base.update(overrides)
    return SearchRequest(**base)


def run_search(request: SearchRequest) -> None:
    try:
        ss.result = ss.search_service.search(request)
        ss.last_request = request
        ss.compared = set()
        ss.session.request = request
        ss.session.results = ss.result.hotels
    except SearchValidationError as exc:
        for msg in exc.values():
            st.error(msg)


def run_nl_search(user_message: str) -> None:
    """Process natural language input through the agent pipeline."""
    current = None
    if ss.last_request:
        current = ss.last_request.log_fields()

    with st.spinner("Thinking..."):
        try:
            intent_data = extract_intent(user_message, current)
        except Exception as e:
            st.error(f"Could not understand: {e}")
            return

    missing = intent_data.get("missing_fields", [])
    if missing and not current:
        clarification = generate_clarification(missing)
        ss.chat_history.append({"role": "assistant", "content": clarification})
        return

    merged = build_search_request_from_intent(intent_data, current)
    params = merged["params"]

    if not params.get("location") and current:
        params["location"] = current.get("location", "")

    if not params.get("location"):
        ss.chat_history.append({
            "role": "assistant",
            "content": "What city or destination would you like to search?",
        })
        return

    try:
        request = SearchRequest(
            location=params["location"],
            check_in=date.fromisoformat(params["check_in"]),
            check_out=date.fromisoformat(params["check_out"]),
            adults=params.get("adults", 2),
            children=params.get("children", 0),
            rooms=params.get("rooms", 1),
            currency=params.get("currency", "EUR"),
            min_price=params.get("min_price"),
            max_price=params.get("max_price"),
            min_star_rating=params.get("min_star_rating"),
            min_guest_rating=params.get("min_guest_rating"),
            amenities=tuple(params.get("amenities", "").split(",")) if params.get("amenities") else (),
            free_cancellation=params.get("free_cancellation"),
            breakfast_included=params.get("breakfast_included"),
            landmark=params.get("landmark"),
            sort_by=params.get("sort_by", "recommended"),
        )
    except (ValueError, KeyError) as e:
        st.error(f"Invalid parameters: {e}")
        return

    with st.spinner("Searching hotels..."):
        run_search(request)

    if ss.result:
        result_json = json.dumps({
            "total": ss.result.total_matches,
            "hotels": [
                {"name": h.name, "price": h.price_per_night, "currency": h.currency,
                 "stars": h.star_rating, "rating": h.guest_rating, "labels": list(h.labels)}
                for h in ss.result.hotels
            ],
        }, default=str)
        try:
            summary = generate_response(intent_data, result_json)
        except Exception:
            summary = f"Found {ss.result.total_matches} hotel(s) in {request.location}."
        ss.chat_history.append({"role": "assistant", "content": summary})

    ss.location = params["location"]
    ss.check_in = request.check_in
    ss.check_out = request.check_out
    ss.adults = request.adults


def render_hotel_card(hotel, idx: int, nights: int) -> None:
    with st.container(border=True):
        col1, col2, col3 = st.columns([4, 2, 1])
        with col1:
            stars = "★" * int(hotel.star_rating or 0)
            st.markdown(f"**{hotel.name}**")
            st.caption(f"{hotel.city} · {stars} · Guest {hotel.guest_rating}/10 · {hotel.room_type}")
        with col2:
            st.markdown(f"**{hotel.currency} {hotel.price_per_night:.0f}**/night")
            st.caption(f"Total: {hotel.currency} {hotel.price_per_night * nights:.0f} for {nights} nights")
        with col3:
            st.checkbox("Compare", key=f"cmp-{hotel.hotel_id}",
                        value=hotel.hotel_id in ss.compared,
                        on_change=lambda h=hotel.hotel_id: ss.compared.symmetric_difference_update({h}))

        tags = []
        if hotel.breakfast_included: tags.append("Breakfast")
        if hotel.free_cancellation: tags.append("Free cancel")
        tags.extend(hotel.amenities[:5])
        st.caption(" · ".join(tags))

        if hotel.labels:
            label_text = " · ".join(f"**{l}**" for l in hotel.labels)
            st.markdown(label_text)

        b1, b2 = st.columns(2)
        with b1:
            if st.button("View Details", key=f"det-{hotel.hotel_id}"):
                st.session_state["detail_hotel"] = hotel.hotel_id
        with b2:
            if st.button("Book Now", key=f"book-{hotel.hotel_id}"):
                st.session_state["booking_hotel"] = hotel.hotel_id


def render_comparison() -> None:
    selected = [h for h in ss.result.hotels if h.hotel_id in ss.compared] if ss.result else []
    if not selected:
        return
    st.divider()
    st.subheader("Hotel Comparison")
    if len(selected) > 3:
        st.warning("Select up to 3 hotels for comparison.")
        return
    request = ss.last_request
    if not request:
        return
    nights = (request.check_out - request.check_in).days
    rows = {}
    for h in selected:
        rows[h.name] = {
            "Price/night": f"{h.currency} {h.price_per_night:.0f}",
            "Total": f"{h.currency} {h.price_per_night * nights:.0f}",
            "Stars": h.star_rating,
            "Guest rating": h.guest_rating,
            "Room type": h.room_type,
            "Breakfast": "Yes" if h.breakfast_included else "No",
            "Free cancel": "Yes" if h.free_cancellation else "No",
            "Amenities": ", ".join(h.amenities),
            "Distance": f"{h.distance_from_center_km:.1f} km" if h.distance_from_center_km else "—",
        }
    st.dataframe(rows, use_container_width=True)


def render_detail(hotel_id: str) -> None:
    hotel = ss.provider.get_hotel(hotel_id)
    if hotel is None:
        return
    request = ss.last_request
    nights = (request.check_out - request.check_in).days if request else 1
    st.divider()
    st.subheader(hotel.name)
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"**City:** {hotel.city}, {hotel.country}")
        st.write(f"**Stars:** {'★' * int(hotel.star_rating or 0)}")
        st.write(f"**Guest rating:** {hotel.guest_rating}/10")
        st.write(f"**Room type:** {hotel.room_type}")
        st.write(f"**Property type:** {hotel.property_type}")
    with c2:
        st.write(f"**Price:** {hotel.currency} {hotel.price_per_night:.0f}/night")
        st.write(f"**Total:** {hotel.currency} {hotel.price_per_night * nights:.0f} ({nights} nights)")
        st.write(f"**Breakfast:** {'Included' if hotel.breakfast_included else 'Not included'}")
        st.write(f"**Cancellation:** {'Free' if hotel.free_cancellation else 'Non-refundable'}")
        st.write(f"**Distance from center:** {hotel.distance_from_center_km} km" if hotel.distance_from_center_km else "")
    st.write(f"**Amenities:** {', '.join(hotel.amenities)}")


def render_booking_form(hotel_id: str) -> None:
    hotel = ss.provider.get_hotel(hotel_id)
    if hotel is None or ss.last_request is None:
        return
    request = ss.last_request
    nights = (request.check_out - request.check_in).days

    st.divider()
    st.subheader(f"Book: {hotel.name}")

    avail = ss.booking_service.check_availability(hotel_id, request)
    if not avail["available"]:
        st.error("This hotel is no longer available for your dates.")
        return

    st.info(
        f"**{hotel.currency} {hotel.price_per_night:.0f}**/night × {nights} nights "
        f"= **{hotel.currency} {avail['total_price']:.0f}** total"
    )

    with st.form("booking_form"):
        c1, c2 = st.columns(2)
        with c1:
            first = st.text_input("First name *")
            email = st.text_input("Email *")
        with c2:
            last = st.text_input("Last name *")
            phone = st.text_input("Phone")

        submitted = st.form_submit_button("Confirm Booking", type="primary")
        if submitted:
            if not first.strip() or not last.strip() or not email.strip():
                st.error("First name, last name, and email are required.")
                return
            guest = BookingGuest(first_name=first.strip(), last_name=last.strip(),
                                 email=email.strip(), phone=phone.strip())
            try:
                booking = ss.booking_service.create_booking(hotel_id, request, guest)
                st.success("Booking confirmed!")
                st.code(ss.booking_service.get_booking_summary(booking))
                st.session_state["booking_hotel"] = None
            except ValueError as e:
                st.error(str(e))


# ── UI ─────────────────────────────────────────────────────────────
st.title("HotelFinder Pro")

tab_search, tab_chat = st.tabs(["Search Form", "Chat"])

# ── Tab 1: Form Search ────────────────────────────────────────────
with tab_search:
    with st.form("hotel-search"):
        first_col, second_col, third_col = st.columns(3)
        with first_col:
            st.text_input("Location", placeholder="e.g. Paris", key="location")
            st.date_input("Check-in", min_value=date.today(), value=date.today(), key="check_in")
            st.number_input("Adults", min_value=1, max_value=16, value=2, key="adults")
            st.number_input("Children", min_value=0, max_value=12, value=0, key="children")
        with second_col:
            st.date_input("Check-out", min_value=date.today(),
                          value=date.today() + timedelta(days=1), key="check_out")
            st.number_input("Rooms", min_value=1, max_value=4, value=1, key="rooms")
            st.selectbox("Currency", ["EUR", "USD", "GBP", "INR"], key="currency")
            st.selectbox("Sort", ["recommended", "price_asc", "price_desc", "rating_desc",
                                  "stars_desc", "distance_asc"],
                         format_func=lambda v: v.replace("_", " ").title(), key="sort_by")
        with third_col:
            st.number_input("Min price / night", min_value=0.0, value=0.0, step=10.0, key="min_price")
            st.number_input("Max price / night", min_value=0.0, value=0.0, step=10.0, key="max_price")
            st.selectbox("Min star rating", [0, 1, 2, 3, 4, 5], key="min_stars")
            st.number_input("Min guest rating", min_value=0.0, max_value=10.0, value=0.0,
                            step=0.5, key="min_guest_rating")

        flt, prox = st.columns(2)
        with flt:
            st.multiselect("Amenities", ["wifi", "breakfast", "pool", "spa", "gym",
                                          "parking", "pet-friendly", "air conditioning"],
                           key="amenities")
            st.multiselect("Property type", ["hotel", "resort", "aparthotel", "boutique"],
                           key="property_types")
            st.checkbox("Free cancellation", key="free_cancellation")
            st.checkbox("Breakfast included", key="breakfast")
        with prox:
            st.text_input("Landmark (optional)", key="landmark")
            st.number_input("Radius from landmark (km)", min_value=0.1, value=3.0,
                            step=0.5, key="radius_km")

        if st.form_submit_button("Search hotels", type="primary"):
            run_search(build_request())

# ── Tab 2: Chat Search ────────────────────────────────────────────
with tab_chat:
    st.caption("Type a natural language request, e.g. \"Hotels in Paris near the Eiffel Tower, 4 star with breakfast, under 200 EUR\"")
    for msg in ss.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Describe what you're looking for..."):
        ss.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            run_nl_search(prompt)
            if ss.chat_history and ss.chat_history[-1]["role"] == "assistant":
                st.markdown(ss.chat_history[-1]["content"])

# ── Results Display ────────────────────────────────────────────────
result = ss.result
if result is not None and result.hotels:
    request = ss.last_request
    st.divider()
    st.subheader(f"{result.total_matches} hotel(s) found in {request.location.strip()}")
    st.caption(f"Source: {result.source.replace('_', ' ')} · {result.latency_ms} ms")

    nights = (request.check_out - request.check_in).days

    for idx, hotel in enumerate(result.hotels):
        render_hotel_card(hotel, idx, nights)

    render_comparison()

# ── Detail View ────────────────────────────────────────────────────
detail_id = st.session_state.get("detail_hotel")
if detail_id:
    render_detail(detail_id)
    if st.button("Close details"):
        st.session_state["detail_hotel"] = None
        st.rerun()

# ── Booking Flow ───────────────────────────────────────────────────
booking_id = st.session_state.get("booking_hotel")
if booking_id:
    render_booking_form(booking_id)

st.caption("Demo inventory only — prices and availability are generated for testing, not live supplier data.")
