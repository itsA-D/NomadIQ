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
├── models/                # Data models (currently empty, for future modular structure)
├── services/              # Business logic services (currently empty, for future modular structure)
├── providers/             # Data provider implementations (currently empty, for future modular structure)
├── tests/                 # Test files (currently empty, for future testing)
├── .agents/               # Devin AI agent configuration
├── .cursor/               # Cursor IDE configuration
├── .qodo/                 # Qodo AI configuration
├── pyproject.toml         # Project metadata and dependencies
├── requirements.txt       # Python dependencies
├── uv.lock                # UV package manager lock file
├── .env.example           # Environment variable template
├── .env                   # Environment variables (not committed)
├── .gitignore             # Git ignore rules
├── setup-windows.ps1      # Windows setup script
├── setup_ollama.ps1       # Ollama setup script (PowerShell)
├── setup_ollama.bat       # Ollama setup script (Batch)
├── check_ollama.ps1       # Ollama status check script
├── REPAIR-LOG.md          # Documentation of fixes and repairs
├── ARCHITECTURE.md        # This file - project architecture documentation
└── README.md              # Project documentation
```

## Architecture Layers

### 1. Presentation Layer
- **Streamlit UI** (`app.py`, `app_openai.py`)
  - User interface for hotel search
  - Form inputs for location, dates, guest count
  - Results display and error handling

### 2. Agent Orchestration Layer
- **CrewAI Framework**
  - Multi-agent coordination
  - Task management and execution
  - Agent communication and delegation

### 3. Agent Layer
- **Hotels Agent** (`app.py`)
  - Role: Hotel search specialist
  - Tools: Kayak URL generator, Browserbase web scraper
  - Goal: Find and analyze hotel options

- **Summarize Agent** (`app.py`)
  - Role: Information summarizer
  - Goal: Format and present hotel results

### 4. Tool Layer
- **Kayak Tool** (`kayak.py`)
  - Generates Kayak hotel search URLs
  - Handles search parameter formatting

- **Browserbase Tool** (`browserbase.py`)
  - Headless browser automation
  - Web scraping and content extraction
  - HTML to text conversion

### 5. Infrastructure Layer
- **LLM Providers**
  - Groq (default, fast)
  - OpenAI (alternative, higher quality)
  - Ollama (local, private)

- **Browser Services**
  - Browserbase cloud browsers
  - Playwright local browser fallback

## Data Flow

```
User Input (Streamlit)
    ↓
CrewAI Crew Initialization
    ↓
Hotels Agent + Kayak Tool → Generate Search URL
    ↓
Hotels Agent + Browserbase Tool → Scrape Hotel Data
    ↓
Summarize Agent → Format Results
    ↓
Display Results (Streamlit)
```

## Configuration Management

### Environment Variables (`.env`)
- `BROWSERBASE_API_KEY`: Browserbase authentication
- `BROWSERBASE_PROJECT_ID`: Browserbase project identifier
- `GROQ_API_KEY`: Groq LLM provider (optional)
- `OPENAI_API_KEY`: OpenAI LLM provider (optional)

### Setup Scripts
- **setup-windows.ps1**: Complete Windows environment setup
- **setup_ollama.ps1/bat**: Ollama local LLM installation
- **check_ollama.ps1**: Verify Ollama installation status

## Extension Points

### Modular Structure (Planned)
The following directories are prepared for future modular architecture:
- **models/**: Data models and schemas
- **services/**: Business logic services (search, filtering, ranking)
- **providers/**: Multiple data provider implementations
- **tests/**: Unit and integration tests

### Current Implementation
Currently uses a monolithic approach with agents defined in `app.py`. The modular directories are reserved for future refactoring to support:
- Multiple hotel booking providers
- Advanced filtering and ranking algorithms
- Comprehensive test coverage
- Better separation of concerns
