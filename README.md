# 🏨 HotelFinder Pro: Intelligent Multi-Agent Travel Assistant

<div align="center">

**Mastering Travel Research through Agentic AI and Headless Automation.**

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg?style=for-the-badge&logo=python)
![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-green.svg?style=for-the-badge)
![Browserbase](https://img.shields.io/badge/Browserbase-Headless--Scraping-orange.svg?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Web--UI-red.svg?style=for-the-badge&logo=streamlit)

---

### "Stop browsing, start discovering. Let AI agents do the research for you."

</div>

## 📑 Table of Contents

1.  [🎯 Project Overview](#-project-overview)
2.  [💡 Problem Statement](#-problem-statement--motivation)
3.  [🚀 Quick Start](#-quick-start)
4.  [📦 Detailed Installation & Setup](#-detailed-installation--setup)
    - [Option A: Conda (Windows Recommended)](#option-a-using-conda-recommended-for-windows)
    - [Option B: uv (Performance Choice)](#option-b-using-uv-fastest)
    - [Option C: Standard Virtualenv](#option-c-using-python-venv)
5.  [🏗️ System Architecture](#-system-architecture)
6.  [⚙️ Configuration & Environment](#-configuration--environment)
7.  [🔍 Multi-Agent Workflow](#-multi-agent-workflow)
8.  [🛠️ Implementation Details](#-implementation-details)
9.  [🧪 Usage & Examples](#-usage--examples)
10. [🚨 Troubleshooting & FAQ](#-troubleshooting)
11. [📈 Professional Repair Log](#-professional-repair-log-summary)

---

## 🎯 Project Overview

**HotelFinder Pro** is a state-of-the-art multi-agent AI system designed to automate the complex process of hotel search and pricing comparison. By orchestrating specialized agents powered by **CrewAI**, the system navigates real-time travel data via **Browserbase** headless browsers, evaluates offers, and synthesizes the best results into a clean, actionable report.

---

## 💡 Problem Statement & Motivation

### The Problem
Finding the best hotel deals online is a time-consuming and fragmented process:
1.  **Information Overload**: Users manually browse multiple booking platforms.
2.  **Price Comparison Complexity**: Comparing prices across providers requires manual tracking.
3.  **Time-Intensive Research**: Evaluating amenities, ratings, and locations takes significant effort.

### The Solution
HotelFinder Pro centralizes this entire workflow using **Agentic AI**. It acts as a digital travel assistant that searches, scrapes, analyzes, and presents structured recommendations in minutes.

---

## 🚀 Quick Start

Follow these three steps to be up and running in 2 minutes:

```powershell
# 1. Clone & Enter
git clone https://github.com/itsA-D/NomadIQ.git
cd hotel-booking-crew

# 2. Setup (Windows/Conda)
conda create -n hotelbai python=3.12 -y
conda activate hotelbai
pip install -r requirements.txt
playwright install chromium

# 3. Run
streamlit run app.py
```

---

## 📦 Detailed Installation & Setup

### Option A: Using Conda (Recommended for Windows)
Perfect for managing Python versions and system-level dependencies.
```powershell
# Create environment
conda create -n hotelbai python=3.12 -y
conda activate hotelbai

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Useful Conda Commands:
# conda env list          # List all environments
# conda env export > env.yml # For sharing
```

### Option B: Using uv (Fastest)
Modern dependency manager that is 10-100x faster than pip.
```powershell
pip install uv
uv sync
playwright install chromium
```

### Option C: Using Python venv
Standard built-in virtual environment.
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

---

## 🏗️ System Architecture

HotelFinder Pro uses a **Sequential Hierarchical** architecture.

### Architecture Layers:
1.  **User Interface Layer (Streamlit)**: Captures input and renders formatted markdown results.
2.  **Orchestration Layer (CrewAI)**: Coordinates roles, tasks, and inter-agent communication.
3.  **Tool Layer**: 
    - **Kayak Tool**: Predictable URL construction logic.
    - **Browserbase Tool**: Secure, cloud-based headless browser automation.
4.  **LLM Layer**: Reasoning engine (DeepSeek-R1, Groq, or OpenAI).

---

## ⚙️ Configuration & Environment

Create a `.env` file in the project root:
```env
# REQUIRED: https://browserbase.ai
BROWSERBASE_API_KEY=your_key
BROWSERBASE_PROJECT_ID=your_id

# LLM BACKENDS (Pick One)
GROQ_API_KEY=your_key    # Fast/Free (Default)
OPENAI_API_KEY=your_key  # High Quality (Paid)
```

### LLM Engine Configuration:
The app supports multiple backends. Update `load_llm()` in `app.py`:
- **Groq**: `LLM(model="groq/llama-3.3-70b-versatile")`
- **Ollama**: `LLM(model="ollama/deepseek-r1")`
- **OpenAI**: `LLM(model="gpt-4o-mini")`

---

## 🔍 Multi-Agent Workflow

### 🤵 Agent 1: The Hotels Specialist
- **Role**: Search and data collection.
- **Goal**: Find top hotels based on pricing, ratings, and location.
- **Tools**: `kayak_hotels`, `browserbase`.

### 🤵 Agent 2: The Travel Summarizer
- **Role**: Data analysis and presentation.
- **Goal**: Synthesize raw data into a user-friendly report with clear booking links.
- **Output**: 5 best recommendations.

---

## 🛠️ Implementation Details

### Browserbase Tool (`browserbase.py`)
Connects to a remote Chromium instance to handle JavaScript-heavy sites. It extracts full-page HTML and converts it to Markdown, ensuring the LLM receives clean, context-rich data without the noise of raw code.

### Kayak Tool (`kayak.py`)
Uses deterministic URL patterns to bypass search field interactions.
`Input: Paris, 2024-10-15, 2adults` → `Output: https://www.kayak.co.in/hotels/Paris/2024-10-15/...`

---

## 🧪 Usage & Examples

1. Launch: `streamlit run app.py`
2. Configure: Paste Browserbase API Key in sidebar.
3. Input: Location (**London**), Dates (**Oct 12-15**), Guests (**2**).
4. Observe: Progress logs in the terminal show agents browsing and reasoning.
5. Results: View pricing, amenities, and "Book Now" links.

---

## 🚨 Troubleshooting

### 1. "UnserializableReturnValueError"
Fixed by using `@st.cache_resource` instead of `@st.cache_data` for LLM objects.

### 2. "ImportError: LiteLLM not found"
Run `pip install litellm`. This is required for most advanced CrewAI integrations.

### 3. OpenAI Quota (429 Error)
Switch to **Groq** in `app.py` or use **Ollama** for local free inference.

### 4. Playwright Brower Issues
Run `playwright install chromium` explicitly in your active environment.

---

## 📈 Professional Repair Log Summary

- ✅ **Assets Fixed**: Restored `/assets` directory for UI stability.
- ✅ **Validation Added**: Date and location sanity checks prevent infinite loops.
- ✅ **Conda Reparation**: Fixed environment corruption issues.
- ✅ **UI Optimized**: Added feedback icons and time estimates.

---

**Happy Travels! 🛫🏨**  
*Maintained by ANKAN (NomadIQ Team)*
