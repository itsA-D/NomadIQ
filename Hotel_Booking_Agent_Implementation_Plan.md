# Hotel Booking Agent — Precise Implementation Plan

## 0. Goal

Transform the current hotel-search demo into a reliable **agentic hotel search and booking platform**.

Target user flow:

```text
Natural-language request / UI filters
        ↓
Intent + constraint extraction
        ↓
Canonical SearchRequest
        ↓
Hotel provider / inventory retrieval
        ↓
Deterministic filtering
        ↓
Deterministic ranking
        ↓
Top-N recommendations
        ↓
Conversational refinement / comparison
        ↓
Room availability + price validation
        ↓
Booking workflow
```

### Critical rule

**LLM = intent, planning, clarification, explanation.**

**Backend = search truth, filtering, pricing, availability, ranking, booking.**

Never let the LLM invent hotel inventory, prices, dates, availability, totals, or booking IDs.

---

# 1. Current Problem to Fix First

Current UI accepts inputs such as:

```text
Location: Paris
Check-in: 2026-08-17
Check-out: 2026-08-18
Adults: 2
```

but the displayed result can contain unrelated data such as New York / September 2024.

This means the search parameters are not being preserved or grounded through the full pipeline.

## Required fix

Trace and log this exact path:

```text
UI
 → SearchRequest
 → Agent/tool call
 → Provider request
 → Provider response
 → Normalized hotels
 → Filters
 → Ranking
 → UI/LLM response
```

At every boundary verify:

- location
- check-in
- check-out
- adults
- rooms
- currency
- filters

Remove hardcoded hotel results and prevent stale/mock data from silently appearing in production/demo mode.

---

# 2. Target Architecture

```text
                         ┌───────────────────────┐
                         │       Streamlit       │
                         │      Presentation     │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │   Agent / Planner     │
                         │ intent extraction     │
                         │ clarification         │
                         │ tool selection        │
                         └───────────┬───────────┘
                                     │
                              SearchRequest
                                     │
                                     ▼
                    ┌───────────────────────────────┐
                    │      Hotel Search Service     │
                    │ provider adapter / inventory  │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │       Filtering Engine        │
                    │ dates / price / rating / etc │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │        Ranking Engine         │
                    │ relevance / value / prefs    │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │   Recommendation / Compare    │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                              Streamlit UI

                 Supporting services:
                 ├── Redis cache
                 ├── Persistent DB
                 ├── Availability service
                 └── Booking service
```

---

# 3. Canonical Data Contracts

Create typed models. Every component must use them.

## SearchRequest

```python
class SearchRequest:
    location: str
    check_in: date
    check_out: date
    adults: int
    children: int
    rooms: int

    currency: str
    min_price: float | None
    max_price: float | None

    min_star_rating: float | None
    min_guest_rating: float | None

    amenities: list[str]
    property_types: list[str]

    free_cancellation: bool | None
    breakfast_included: bool | None

    landmark: str | None
    radius_km: float | None

    sort_by: str
```

## Hotel

```python
class Hotel:
    hotel_id: str
    name: str
    city: str
    country: str
    latitude: float | None
    longitude: float | None

    star_rating: float | None
    guest_rating: float | None

    price_per_night: float
    currency: str

    room_type: str
    amenities: list[str]

    free_cancellation: bool
    breakfast_included: bool
    availability: bool

    distance_from_center_km: float | None
    distance_from_landmark_km: float | None

    booking_options: list
```

## SearchResult

```python
class SearchResult:
    request_id: str
    hotels: list[Hotel]
    total_matches: int
    applied_filters: dict
    source: str
    latency_ms: int
```

---

# 4. Provider Abstraction

Do not couple the business logic to one hotel API.

Create:

```text
providers/
├── base.py
├── mock_provider.py
└── real_provider.py
```

Interface:

```python
class HotelProvider:
    def search(self, request: SearchRequest) -> list[Hotel]:
        ...

    def get_hotel(self, hotel_id: str) -> Hotel:
        ...

    def check_availability(self, hotel_id: str, request: SearchRequest):
        ...
```

### Development mode

Use a deterministic mock provider with realistic inventory so the complete system can be tested without depending on an external provider.

### Production mode

Implement a real provider adapter once the provider/API is selected. Do not claim live availability or live pricing unless the provider actually supplies it.

---

# 5. Search Service

Create `services/search_service.py`.

Responsibilities:

1. Validate `SearchRequest`.
2. Call the provider.
3. Normalize provider data.
4. Remove invalid/incomplete records.
5. Return `SearchResult`.

Never generate hotel records using the LLM.

---

# 6. Validation

Before searching, enforce:

```text
check_out > check_in
adults >= 1
children >= 0
rooms >= 1
min_price <= max_price
1 <= star_rating <= 5
0 <= guest_rating <= 10
radius_km > 0
```

Validate:

- missing location
- invalid dates
- past dates when not supported
- impossible occupancy
- unsupported currency
- invalid filter combinations

Return structured validation errors.

---

# 7. Filtering Engine

Create `services/filter_service.py`.

Implement independently testable filters:

```python
filter_by_price()
filter_by_star_rating()
filter_by_guest_rating()
filter_by_amenities()
filter_by_property_type()
filter_by_cancellation()
filter_by_breakfast()
filter_by_distance()
filter_by_availability()
```

Pipeline:

```text
Raw hotels
   ↓
Date/availability
   ↓
Price
   ↓
Star rating
   ↓
Guest rating
   ↓
Amenities
   ↓
Property type
   ↓
Cancellation
   ↓
Distance
```

Filtering must be deterministic Python/application logic.

---

# 8. Initial Filters to Implement

## Required

- location
- check-in
- check-out
- adults
- rooms
- minimum/maximum price
- star rating
- guest rating
- free cancellation
- breakfast

## Next

- Wi-Fi
- pool
- parking
- gym
- spa
- pet-friendly
- air conditioning
- property type

## Advanced

- landmark
- radius
- neighborhood
- family-friendly
- business-friendly
- accessibility

Implement filters incrementally. Do not add UI controls until backend filtering works and is tested.

---

# 9. Ranking Engine

Create `services/ranking_service.py`.

Filtering determines **eligibility**. Ranking determines **priority**.

Supported sort modes:

```text
recommended
price_asc
price_desc
rating_desc
stars_desc
distance_asc
```

For `recommended`, use a deterministic normalized score.

Example:

```text
score =
    0.35 * guest_rating_score
  + 0.20 * price_score
  + 0.20 * preference_match
  + 0.15 * amenity_match
  + 0.10 * location_score
```

Weights must be configurable.

Normalize each component to `[0, 1]` before combining.

Do not allow the LLM to decide raw numerical rankings.

---

# 10. Best-Value Recommendations

Add derived recommendation labels:

```text
Best Overall
Best Value
Lowest Price
Highest Rated
Closest
```

Example:

```text
Best Value = strong rating + reasonable price + high preference match
```

Store the numeric score and recommendation reason for transparency.

---

# 11. Natural-Language Search

Add an agent/planner that converts natural language to `SearchRequest`.

Example user input:

> Find me something cheap near the Eiffel Tower for two people, preferably 4 star with breakfast.

Agent output must be structured JSON, not free-form search prose:

```json
{
  "location": "Paris",
  "landmark": "Eiffel Tower",
  "adults": 2,
  "min_star_rating": 4,
  "breakfast_included": true,
  "price_preference": "budget"
}
```

Resolve relative terms such as `cheap`, `luxury`, `near`, and `highly rated` into deterministic filter/ranking parameters.

The agent must never invent a hotel.

---

# 12. Clarification Logic

Define required fields:

```text
location
check_in
check_out
```

Use safe defaults only where explicitly defined:

```text
adults = 1
rooms = 1
children = 0
```

If required information is missing, ask the user instead of searching with guessed values.

Example:

```text
User: Find me a hotel in Paris.

Agent: Sure. What check-in and check-out dates should I use?
```

Ask only for missing information.

---

# 13. Conversational Refinement

Persist a `SearchSession`:

```python
class SearchSession:
    conversation_id: str
    request: SearchRequest
    results: list[Hotel]
    selected_hotel_id: str | None
```

Examples:

```text
User: Hotels in Paris under €200.

User: Only 4 star or higher.
→ min_star_rating = 4

User: Include breakfast.
→ breakfast_included = true

User: Show cheapest first.
→ sort_by = price_asc
```

Update the existing `SearchRequest`; do not discard conversation state.

---

# 14. Hotel Comparison

Allow selection of 2–3 hotels.

Display:

```text
Price / night
Total price
Guest rating
Star rating
Breakfast
Cancellation
Amenities
Distance
Room type
Availability
```

Provide deterministic comparison values and let the agent summarize the trade-offs.

Example:

> Hotel A is cheaper, while Hotel B has the better guest rating and is closer to the selected landmark.

---

# 15. Hotel Details

Each result card should show:

```text
Hotel name
Location
Star rating
Guest rating
Price/night
Estimated total
Room type
Key amenities
Cancellation policy
Breakfast status
Distance
Availability
Provider/source
```

Add:

```text
View Details
Compare
Select
```

---

# 16. Price Calculation

Never let the LLM calculate totals.

Use:

```python
nights = (check_out - check_in).days
subtotal = price_per_night * nights

total = subtotal + taxes + fees - discounts
```

Display:

```text
€179 × 3 nights = €537
Taxes           = €64
Fees            = €12
----------------------
Total           = €613
```

Only display taxes/fees that actually exist in provider data; otherwise mark them as unavailable/estimated rather than inventing them.

---

# 17. Availability

Distinguish:

```text
hotel exists
```
from:

```text
specific room is available for requested dates/occupancy
```

Model:

```text
Hotel
 └── Room
      ├── occupancy
      ├── availability
      ├── price
      ├── cancellation
      └── meal plan
```

Before booking, perform a fresh availability/price check.

---

# 18. Constraint Relaxation

When zero results are returned, do not fabricate alternatives.

Show the user how constraints can be relaxed.

Example:

```text
No exact matches found.

Possible relaxations:
1. Increase budget to €220 → 8 matches
2. Remove breakfast requirement → 14 matches
3. Expand search radius to 3 km → 21 matches
```

Counts must be calculated by the search engine, not invented by the LLM.

---

# 19. Tool-Based Agent Architecture

Expose deterministic backend operations as agent tools:

```text
search_hotels()
filter_hotels()
rank_hotels()
get_hotel_details()
compare_hotels()
check_room_availability()
calculate_price()
create_booking()
```

Flow:

```text
User
 ↓
Agent
 ↓
extract intent
 ↓
call tools
 ↓
receive structured results
 ↓
reason over results
 ↓
explain to user
```

The agent should call tools instead of generating hotel facts directly.

---

# 20. Booking Workflow

After a hotel/room is selected:

```text
Search
 ↓
Hotel details
 ↓
Room selection
 ↓
Availability re-check
 ↓
Price re-check
 ↓
Guest details
 ↓
Booking review
 ↓
Confirm
 ↓
Booking record
 ↓
Confirmation
```

Create a separate `BookingService`.

Never treat an LLM-generated confirmation number as a real booking ID.

---

# 21. Persistence

Persist at minimum:

```text
users
search_sessions
search_requests
selected_hotels
bookings
```

Suggested relationships:

```text
User
 ├── SearchSession
 │    └── SearchRequest
 │         └── SelectedHotel
 └── Booking
```

Keep provider-specific raw responses separate from normalized application models where useful for debugging/auditing.

---

# 22. Redis Caching

Add Redis for repeat search caching.

Cache key should include all search-affecting fields, for example:

```text
location
check_in
check_out
adults
children
rooms
currency
filters
```

Example:

```text
search:{hash(canonical_search_request)}
```

Flow:

```text
SearchRequest
 ↓
Cache lookup
 ├── HIT  → return cached normalized results
 └── MISS → provider → normalize → cache → return
```

Do not cache indefinitely. Configure TTL.

---

# 23. Observability

Every search should produce structured logs containing:

```text
request_id
conversation_id
user_id
search_request
provider
provider_latency_ms
retrieved_count
filtered_count
returned_count
ranking_latency_ms
llm_latency_ms
total_latency_ms
cache_hit
error
```

Example:

```text
retrieved: 43
filtered: 11
returned: 5
provider: 310ms
filter: 7ms
ranking: 2ms
LLM: 2.8s
total: 3.2s
```

This makes performance bottlenecks measurable.

---

# 24. Error Handling

Handle independently:

```text
provider unavailable
provider timeout
invalid search request
no results
LLM failure
cache failure
database failure
availability changed
price changed
booking failure
```

Core search should not fail completely because Redis or LLM explanation is unavailable.

Example degradation:

```text
Provider works + LLM fails
→ return structured hotel results without AI explanation

Provider fails + cache hit
→ return clearly labelled cached results if acceptable

Provider fails + no cache
→ show a real error; never fabricate hotels
```

---

# 25. UI Plan

## Search panel

```text
Location
Check-in
Check-out
Adults
Children
Rooms
Price range
Star rating
Guest rating
Amenities
Free cancellation
Breakfast
Property type
Sort
```

## Results page

Top summary:

```text
42 hotels found
7 match all filters
```

Each card:

```text
Hotel name
⭐ rating
€ price/night
Total
Key amenities
Cancellation
Distance

[Details] [Compare] [Select]
```

## Comparison page

Side-by-side table for selected hotels.

## Booking page

Room → guests → price review → confirm.

## Conversation panel

Support natural-language refinement:

```text
"Only show 4-star hotels."
"Sort by cheapest."
"Show breakfast included."
"Compare the first two."
```

---

# 26. Testing Strategy

Create unit tests before adding too many features.

## Search tests

```text
valid request
invalid dates
missing location
multiple adults
multiple rooms
```

## Filter tests

```text
price filter
rating filter
amenity filter
cancellation filter
distance filter
combined filters
```

## Ranking tests

```text
price ascending
rating descending
recommended score
best value
```

## Agent tests

```text
extract location
extract dates
extract occupancy
extract price preference
handle missing fields
modify existing search
refine results
```

## Booking tests

```text
availability success
availability failure
price changed
successful booking
booking failure
```

Critical regression test:

```text
Input:
Paris
2026-08-17
2026-08-18
2 adults

Expected:
Every result must correspond to Paris and the requested dates/source data.
```

---

# 27. Recommended Project Structure

```text
hotel-booking-agent/
├── app/
│   ├── main.py
│   ├── config.py
│   └── dependencies.py
│
├── agents/
│   ├── booking_agent.py
│   ├── planner.py
│   └── prompts.py
│
├── tools/
│   ├── hotel_search.py
│   ├── availability.py
│   ├── comparison.py
│   ├── pricing.py
│   └── booking.py
│
├── services/
│   ├── search_service.py
│   ├── filter_service.py
│   ├── ranking_service.py
│   ├── recommendation_service.py
│   └── booking_service.py
│
├── providers/
│   ├── base.py
│   ├── mock_provider.py
│   └── real_provider.py
│
├── models/
│   ├── search_request.py
│   ├── hotel.py
│   ├── room.py
│   ├── booking.py
│   └── search_session.py
│
├── repositories/
│   ├── search_repository.py
│   ├── booking_repository.py
│   └── user_repository.py
│
├── cache/
│   └── redis_cache.py
│
├── ui/
│   ├── search_page.py
│   ├── results_page.py
│   ├── comparison_page.py
│   └── booking_page.py
│
├── tests/
│   ├── test_search.py
│   ├── test_filters.py
│   ├── test_ranking.py
│   ├── test_agent.py
│   └── test_booking.py
│
└── README.md
```

Adapt the names to the existing repository rather than rewriting the entire project at once.

---

# 28. Implementation Order

Do not implement all features simultaneously.

## Phase 1 — Correctness

```text
[ ] Trace current search flow
[ ] Remove hardcoded/stale results
[ ] Introduce SearchRequest
[ ] Validate inputs
[ ] Normalize provider results
[ ] Add Paris/date regression test
```

## Phase 2 — Real Search Engine

```text
[ ] Provider interface
[ ] Multiple hotel results
[ ] Availability-aware results
[ ] Price filter
[ ] Star filter
[ ] Guest-rating filter
[ ] Amenities filter
[ ] Cancellation filter
[ ] Sorting
```

## Phase 3 — Recommendation

```text
[ ] Ranking engine
[ ] Recommended score
[ ] Best-value score
[ ] Recommendation reasons
[ ] Hotel comparison
[ ] Details page
```

## Phase 4 — Agentic Search

```text
[ ] Natural-language intent extraction
[ ] Structured tool calls
[ ] Missing-field clarification
[ ] Conversational refinement
[ ] Search-session state
[ ] Constraint relaxation
```

## Phase 5 — Booking

```text
[ ] Room selection
[ ] Availability re-check
[ ] Price re-check
[ ] Guest details
[ ] Booking service
[ ] Booking confirmation
```

## Phase 6 — Production Engineering

```text
[ ] Redis cache
[ ] Persistent database
[ ] Structured logging
[ ] Metrics
[ ] Error handling
[ ] Test coverage
[ ] Provider abstraction
```

---

# 29. Definition of Done

The project is ready for a strong demo only when all of the following are true:

```text
[ ] Search uses the exact location entered by the user
[ ] Search uses the exact requested dates
[ ] Adult/room occupancy reaches the provider layer
[ ] Results are retrieved from a defined provider/inventory source
[ ] No hotel is invented by the LLM
[ ] Results are normalized into a common Hotel model
[ ] Multiple hotels can be returned
[ ] Filters work independently and in combination
[ ] Sorting works deterministically
[ ] Ranking produces explainable recommendations
[ ] Natural-language requests become structured constraints
[ ] Missing required information triggers clarification
[ ] Follow-up messages refine the existing search
[ ] Users can compare hotels
[ ] Availability can be re-checked before booking
[ ] Price totals are calculated by backend code
[ ] Booking state is persisted
[ ] Provider/API failures are handled gracefully
[ ] Critical search path has automated tests
[ ] Logs expose retrieval/filtering/ranking/LLM latency
```

---

# 30. Final Demo Scenario

Use this as the acceptance demo:

```text
1. User enters:
   Paris
   Aug 17 → Aug 20, 2026
   2 adults

2. Search returns multiple hotels.

3. User says:
   "Only show 4-star hotels with breakfast and free cancellation under €200."

4. Results update without losing the original search context.

5. User says:
   "Sort by best value."

6. Top results are deterministically ranked.

7. User selects two hotels.

8. System shows a comparison table.

9. User selects one hotel.

10. System checks room availability and current price.

11. User proceeds through guest details and booking review.

12. System creates/persists a booking record.
```

---

# 31. Resume-Level Technical Positioning

Only claim functionality that is actually implemented and tested.

A strong final description can be supported by this architecture:

> Built an agentic hotel-booking platform that converts natural-language travel requests into structured search constraints, retrieves and normalizes hotel inventory, applies multi-criteria filtering and deterministic ranking, supports conversational search refinement and hotel comparison, and orchestrates availability and booking workflows through tool-based agents.

Key engineering story:

```text
LLM / Agent
→ understands intent
→ plans / clarifies
→ invokes tools
→ explains results

Backend
→ owns truth
→ searches inventory
→ filters
→ ranks
→ calculates prices
→ validates availability
→ executes booking
```

This separation is the core design principle of the project.
