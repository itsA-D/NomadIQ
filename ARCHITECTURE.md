# Architecture

## Overview
AI-powered hotel search application using CrewAI agents to find accommodations via Kayak and Browserbase. Users interact through a Streamlit web UI to search hotels by location, dates, and guest count; agents use web scraping tools to retrieve and summarize hotel options.

## Tech Stack
- Python 3.12+
- Streamlit (web UI framework)
- CrewAI (multi-agent orchestration)
- Groq/LLM (language model provider)
- Browserbase (headless browser automation)
- Playwright (browser automation)
- html2text (HTML to text conversion)
- python-dotenv (environment configuration)

## Folder Structure
```
hotel-booking-crew/
├── app.py                 # Main entry point (Groq LLM)
├── app_openai.py          # Alternative entry point (OpenAI LLM)
├── browserbase.py         # CrewAI tool: headless browser via Browserbase
├── kayak.py               # CrewAI tool: Kayak hotel search URL generator
├── assets/                # Static assets (logos, images)
├── pyproject.toml         # Project metadata and dependencies
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
└── README.md              # Project documentation
```
