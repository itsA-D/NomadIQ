"""Planner agent: converts natural language to structured SearchRequest via LLM.

Uses litellm for provider-agnostic LLM calls (Groq, OpenAI, Ollama, etc.).
The LLM extracts intent — it never invents hotel data.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import date, timedelta

import litellm

logger = logging.getLogger(__name__)

EXTRACTION_PROMPT = """You are a hotel search planner. Convert the user's message into a JSON object for hotel search.

Return ONLY a JSON object with these fields (omit any field the user did not specify):

{{
  "location": "string (city name, required if mentioned)",
  "check_in": "YYYY-MM-DD (required if mentioned)",
  "check_out": "YYYY-MM-DD (required if mentioned)",
  "adults": integer,
  "children": integer,
  "rooms": integer,
  "currency": "EUR | USD | GBP | INR",
  "min_price": number or null,
  "max_price": number or null,
  "min_star_rating": integer 1-5 or null,
  "min_guest_rating": number 0-10 or null,
  "amenities": ["list of amenity strings"],
  "free_cancellation": true or null,
  "breakfast_included": true or null,
  "landmark": "string or null",
  "sort_by": "recommended | price_asc | price_desc | rating_desc | stars_desc | distance_asc",
  "intent": "search | refine | compare | book | general",
  "missing_fields": ["list of required fields that are missing: location, check_in, check_out"]
}}

Rules:
- "cheap" or "budget" → max_price=150, sort_by=price_asc
- "luxury" or "high-end" → min_star_rating=4, min_guest_rating=8
- "near X" → landmark=X
- "breakfast" → breakfast_included=true
- "cancel" or "flexible" → free_cancellation=true
- "best" or "top" or "recommended" → sort_by=recommended
- "cheapest" → sort_by=price_asc
- "highest rated" → sort_by=rating_desc
- Today's date is {today}.
- If the user is refining a previous search, only include fields they are changing.
- Never fabricate location, dates, or any field the user did not mention.
- "intent" = "refine" if user is modifying an existing search.
- "intent" = "compare" if user wants to compare hotels.
- "intent" = "book" if user wants to book/confirm a hotel.
- "missing_fields" lists required fields (location, check_in, check_out) that are absent.

Return ONLY the JSON object, no explanation."""

REFINEMENT_PROMPT = """You are a hotel search assistant. The user wants to refine their current search.

Current search parameters:
{current_request}

User says: "{user_message}"

Return ONLY a JSON object with the fields to update. Only include fields the user is changing:

{{
  "location": "string or null",
  "check_in": "YYYY-MM-DD or null",
  "check_out": "YYYY-MM-DD or null",
  "adults": integer or null,
  "max_price": number or null,
  "min_star_rating": integer or null,
  "breakfast_included": true or null,
  "free_cancellation": true or null,
  "amenities": ["list"] or null,
  "sort_by": "string or null",
  "intent": "refine",
  "missing_fields": []
}}

Rules:
- Only return fields the user is changing.
- "only 4 star" → min_star_rating=4
- "with breakfast" → breakfast_included=true
- "under 200" → max_price=200
- "cheapest first" → sort_by=price_asc
- Return ONLY the JSON, no explanation."""


def _get_model() -> str:
    """Determine which LLM model to use from environment."""
    if os.environ.get("OPENAI_API_KEY"):
        return os.environ.get("OPENAI_MODEL_NAME", "gpt-4o-mini")
    if os.environ.get("GROQ_API_KEY"):
        return "groq/llama-3.3-70b-versatile"
    return "ollama/deepseek-r1:1.5b"


def _call_llm(prompt: str) -> str:
    """Call the LLM via litellm and return raw response text."""
    model = _get_model()
    logger.info("LLM call: model=%s", model)
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=800,
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        logger.error("LLM call failed: %s", e)
        raise


def _parse_json(text: str) -> dict:
    """Extract JSON from LLM response, handling markdown code blocks."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        cleaned = "\n".join(lines)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(cleaned[start:end])
        raise ValueError(f"No valid JSON in LLM response: {text[:200]}")


def extract_intent(user_message: str, current_request: dict | None = None) -> dict:
    """Extract search intent from natural language using LLM.

    Returns structured dict with search parameters and metadata.
    Never returns hotel data — only intent/constraints.
    """
    today = date.today().isoformat()

    if current_request:
        prompt = REFINEMENT_PROMPT.format(
            current_request=json.dumps(current_request, indent=2, default=str),
            user_message=user_message,
        )
    else:
        prompt = EXTRACTION_PROMPT.format(today=today)
        prompt += f"\n\nUser message: {user_message}"

    raw = _call_llm(prompt)
    return _parse_json(raw)


def build_search_request_from_intent(intent: dict, defaults: dict | None = None) -> dict:
    """Merge extracted intent with defaults to produce complete search params."""
    today = date.today()
    params = {
        "location": "",
        "check_in": (today + timedelta(days=1)).isoformat(),
        "check_out": (today + timedelta(days=2)).isoformat(),
        "adults": 2,
        "children": 0,
        "rooms": 1,
        "currency": "EUR",
        "sort_by": "recommended",
    }
    if defaults:
        params.update({k: v for k, v in defaults.items() if v is not None})

    for key in ("location", "check_in", "check_out", "adults", "children", "rooms",
                "currency", "min_price", "max_price", "min_star_rating",
                "min_guest_rating", "free_cancellation", "breakfast_included",
                "landmark", "sort_by"):
        val = intent.get(key)
        if val is not None:
            params[key] = val

    amenities = intent.get("amenities")
    if amenities:
        params["amenities"] = ",".join(amenities)

    missing = intent.get("missing_fields", [])
    return {"params": params, "missing_fields": missing, "intent": intent.get("intent", "search")}


def generate_clarification(missing_fields: list[str]) -> str:
    """Generate a natural clarification question for missing required fields."""
    questions = []
    if "location" in missing_fields:
        questions.append("What city or destination are you looking for?")
    if "check_in" in missing_fields:
        questions.append("What check-in date would you like?")
    if "check_out" in missing_fields:
        questions.append("What check-out date would you like?")
    if not questions:
        return ""
    return "I need a few more details:\n" + "\n".join(f"- {q}" for q in questions)


def generate_response(intent: dict, search_result_json: str) -> str:
    """Use LLM to explain search results in natural language."""
    model = _get_model()
    prompt = f"""You are a helpful hotel search assistant. Summarize these search results for the user.
Be concise and helpful. Highlight the best options. Do NOT invent any data.

Search criteria: {json.dumps({k: v for k, v in intent.items() if k not in ('missing_fields',)}, default=str)}

Results:
{search_result_json}

Provide a brief, friendly summary (3-5 sentences). Mention the top options by name and price."""

    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=400,
        )
        return response.choices[0].message.content or "Here are your results."
    except Exception:
        return "Here are the hotels matching your criteria. Use the filters to refine further."
