# 🏨 HotelFinder Pro - Project Guide (P-Guide)

<div align="center">

**A Multi-Agent AI System for Intelligent Hotel Search and Booking**

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-green.svg)
![Browserbase](https://img.shields.io/badge/Browserbase-Headless%20Browser-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)

</div>

---

## 📑 Table of Contents

1. [Project Overview](#-project-overview)
2. [Problem Statement & Motivation](#-problem-statement--motivation)
3. [System Architecture](#-system-architecture)
4. [Core Components](#-core-components)
5. [Technology Stack](#-technology-stack)
6. [Multi-Agent Workflow](#-multi-agent-workflow)
7. [Installation & Setup](#-installation--setup)
8. [Configuration Guide](#-configuration-guide)
9. [Usage Instructions](#-usage-instructions)
10. [Project Structure](#-project-structure)
11. [Implementation Details](#-implementation-details)
12. [How It Works](#-how-it-works)
13. [Key Features](#-key-features)
14. [Troubleshooting](#-troubleshooting)
15. [Future Enhancements](#-future-enhancements)
16. [Contributing](#-contributing)
17. [License](#-license)

---

## 🎯 Project Overview

**HotelFinder Pro** is an intelligent, multi-agent AI system designed to automate hotel search and booking processes. Built using **CrewAI** for multi-agent orchestration and **Browserbase** for headless browser automation, this application leverages the power of Large Language Models (LLMs) to provide users with comprehensive hotel recommendations, pricing comparisons, and booking options.

### What Does This Project Do?

The system acts as an intelligent travel assistant that:
- Searches for hotels based on user-specified criteria (location, dates, number of guests)
- Scrapes real-time data from Kayak.com using headless browser automation
- Analyzes and compares hotel options across multiple booking providers
- Presents detailed recommendations with pricing, amenities, and booking links
- Operates either fully locally (using DeepSeek-R1 via Ollama) or with cloud-based LLMs (OpenAI)

---

## 💡 Problem Statement & Motivation

### The Problem

Finding the best hotel deals online is a time-consuming and fragmented process:

1. **Information Overload**: Users must manually browse multiple booking platforms (Kayak, Hotels.com, Booking.com, etc.)
2. **Price Comparison Complexity**: Comparing prices across different providers requires opening multiple tabs and manual tracking
3. **Time-Intensive Research**: Evaluating amenities, locations, ratings, and reviews takes significant effort
4. **Dynamic Pricing**: Hotel prices fluctuate constantly, making it difficult to find the best deal
5. **Decision Fatigue**: Too many options without intelligent filtering leads to poor decision-making

### The Solution

HotelFinder Pro solves these problems by:

- **Automating Web Scraping**: Uses Browserbase to navigate and extract data from booking sites automatically
- **Intelligent Agent Collaboration**: Employs multiple AI agents that specialize in different tasks (searching, summarizing, comparing)
- **Real-Time Data Aggregation**: Gathers live pricing and availability information
- **Structured Recommendations**: Presents organized, easy-to-digest hotel options with all relevant details
- **Local-First Approach**: Offers 100% local execution using DeepSeek-R1, ensuring privacy and zero API costs

### Why This Project Matters

1. **Time Savings**: Reduces hours of manual research to minutes
2. **Cost Efficiency**: Helps users find the best deals by comparing multiple providers
3. **Privacy-Focused**: Local LLM option ensures user data never leaves their machine
4. **Scalability**: Multi-agent architecture can be extended to flights, car rentals, and more
5. **Educational Value**: Demonstrates practical implementation of agentic AI systems

---

## 🏗️ System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│                    (Streamlit Web App)                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                           │
│                        (CrewAI)                                  │
│  ┌──────────────────┐         ┌──────────────────┐             │
│  │  Hotels Agent    │◄───────►│ Summarize Agent  │             │
│  │  - Search Task   │         │ - Analysis Task  │             │
│  │  - Provider Task │         │                  │             │
│  └────────┬─────────┘         └──────────────────┘             │
└───────────┼──────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      TOOL LAYER                                  │
│  ┌──────────────────┐         ┌──────────────────┐             │
│  │  Kayak Tool      │         │ Browserbase Tool │             │
│  │  - URL Generator │         │ - Web Scraper    │             │
│  └──────────────────┘         └──────────────────┘             │
└───────────┬──────────────────────────┬───────────────────────────┘
            │                          │
            ▼                          ▼
┌─────────────────────┐    ┌─────────────────────────────┐
│   Kayak.com API     │    │  Browserbase Cloud Service  │
│   (URL Construction)│    │  (Headless Browser)         │
└─────────────────────┘    └─────────────────────────────┘
            │                          │
            └──────────┬───────────────┘
                       ▼
            ┌─────────────────────┐
            │   LLM Engine        │
            │  - DeepSeek-R1      │
            │  - Groq/Llama       │
            │  - OpenAI GPT-4     │
            └─────────────────────┘
```

### Architecture Layers Explained

#### 1. **User Interface Layer (Streamlit)**
- Provides an intuitive web-based interface
- Captures user inputs (location, dates, number of guests)
- Displays search results in a structured format
- Manages API key configuration

#### 2. **Orchestration Layer (CrewAI)**
- Coordinates multiple AI agents
- Manages task delegation and execution flow
- Implements planning and reasoning capabilities
- Handles inter-agent communication

#### 3. **Tool Layer**
- **Kayak Tool**: Generates properly formatted Kayak URLs
- **Browserbase Tool**: Executes headless browser automation to scrape data

#### 4. **External Services**
- **Browserbase**: Cloud-based headless browser infrastructure
- **LLM Providers**: DeepSeek-R1 (local), Groq, or OpenAI

---

## 🧩 Core Components

### 1. **Multi-Agent System**

The application uses two specialized AI agents:

#### **Hotels Agent**
- **Role**: Primary search and data collection
- **Responsibilities**:
  - Generate Kayak URLs based on user criteria
  - Execute web scraping via Browserbase
  - Extract hotel information (names, prices, ratings, amenities)
  - Identify booking provider options
- **Tools**: `kayak_hotels`, `browserbase`

#### **Summarize Agent**
- **Role**: Data analysis and presentation
- **Responsibilities**:
  - Analyze raw hotel data
  - Summarize key information
  - Format results for user consumption
  - Highlight best deals and options
- **Tools**: None (pure reasoning)

### 2. **Custom Tools**

#### **Kayak Hotel Tool** (`kayak.py`)
```python
def kayak_hotel_search(location_query, check_in_date, check_out_date, num_adults)
```
- Constructs Kayak-compatible URLs
- Parameters: location, dates, guest count
- Returns: Formatted URL string

#### **Browserbase Tool** (`browserbase.py`)
```python
def browserbase(url: str)
```
- Connects to Browserbase headless browser
- Navigates to specified URL
- Waits for dynamic content to load (25 seconds)
- Extracts and converts HTML to markdown text
- Returns: Cleaned text content

### 3. **Task Workflow**

#### **Task 1: Search Task**
- **Description**: Search hotels according to user criteria
- **Agent**: Hotels Agent
- **Output**: Top 5 hotels with ratings, prices, locations, amenities, and booking links

#### **Task 2: Search Booking Providers Task**
- **Description**: Load hotel details and find available booking providers
- **Agent**: Hotels Agent
- **Output**: Detailed information including room types, price ranges, special offers, and provider comparisons

---

## 🛠️ Technology Stack

### **Core Technologies**

| Technology        | Version    | Purpose                             |
| ----------------- | ---------- | ----------------------------------- |
| **Python**        | 3.12+      | Primary programming language        |
| **CrewAI**        | 0.38.1+    | Multi-agent orchestration framework |
| **Browserbase**   | 1.2.0+     | Headless browser automation service |
| **Streamlit**     | 1.44.1+    | Web UI framework                    |
| **Playwright**    | 1.51.0+    | Browser automation library          |
| **html2text**     | 2024.2.26+ | HTML to markdown conversion         |
| **python-dotenv** | 1.1.0+     | Environment variable management     |

### **LLM Options**

1. **DeepSeek-R1** (Local via Ollama) - Default in `app.py`
   - 100% local execution
   - Zero API costs
   - Privacy-focused
   
2. **Groq/Llama-4-Scout** - Default in `app.py`
   - Fast inference
   - Cloud-based
   - Cost-effective

3. **OpenAI GPT-4** - Used in `app_openai.py`
   - High-quality responses
   - Cloud-based
   - Requires API key

### **Development Tools**

- **uv**: Fast Python package manager
- **Git**: Version control
- **dotenv**: Environment configuration

---

## 🔄 Multi-Agent Workflow

### Execution Flow

```
1. USER INPUT
   ├─ Location: "New York"
   ├─ Check-in: "2024-09-21"
   ├─ Check-out: "2024-09-22"
   └─ Adults: 2

2. CREW INITIALIZATION
   ├─ Load LLM (DeepSeek-R1 / Groq / OpenAI)
   ├─ Initialize Hotels Agent
   ├─ Initialize Summarize Agent
   └─ Create Tasks

3. TASK 1: SEARCH HOTELS
   ├─ Hotels Agent receives request
   ├─ Uses Kayak Tool to generate URL
   │   └─ URL: https://www.kayak.co.in/hotels/New-York/2024-09-21/2024-09-22/2adults
   ├─ Uses Browserbase Tool to scrape data
   │   ├─ Connect to headless browser
   │   ├─ Navigate to URL
   │   ├─ Wait 25 seconds for content load
   │   └─ Extract HTML → Convert to text
   └─ Returns: Raw hotel data

4. TASK 2: ANALYZE PROVIDERS
   ├─ Hotels Agent processes scraped data
   ├─ Identifies booking providers
   ├─ Extracts pricing from each provider
   └─ Returns: Structured provider comparison

5. SUMMARIZATION
   ├─ Summarize Agent receives all data
   ├─ Analyzes and formats information
   └─ Returns: User-friendly recommendations

6. DISPLAY RESULTS
   └─ Streamlit renders formatted output
```

### Agent Collaboration Pattern

The agents use a **sequential hierarchical** collaboration pattern:

1. **Planning Phase**: CrewAI's planning feature creates an execution strategy
2. **Execution Phase**: Tasks execute in sequence
3. **Delegation**: Hotels Agent can delegate subtasks if needed
4. **Summarization**: Summarize Agent processes all collected data

---

## 📦 Installation & Setup

### Prerequisites

- **Python 3.12 or higher**
- **Git** (for cloning the repository)
- **Package Manager**: Choose one:
  - **uv** (fastest, recommended for new projects)
  - **conda** (recommended if you already use Anaconda/Miniconda)
  - **pip** (standard Python package manager)
- **Browserbase Account** ([Sign up here](https://browserbase.ai))
- **Ollama** (optional, for local LLM) - [Installation guide](https://ollama.com/library/deepseek-r1)

### Step-by-Step Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/hotel-booking-crew.git
cd hotel-booking-crew
```

#### 2. Set Up Environment & Install Dependencies

Choose **ONE** of the following methods based on your preference:

---

##### **Option A: Using conda (Recommended for Anaconda Users)**

```bash
# Create a new conda environment with Python 3.12
conda create -n hotel-booking-crew python=3.12 -y

# Activate the environment
conda activate hotel-booking-crew

# Install dependencies using pip (within conda environment)
pip install -r requirements.txt
```

**Why use conda?**
- ✅ Better for managing Python versions
- ✅ Handles system-level dependencies
- ✅ Isolated environments
- ✅ Works well with existing conda workflows

---

##### **Option B: Using uv (Fastest)**

```bash
# Install uv if you don't have it
pip install uv

# Sync dependencies (creates .venv automatically)
uv sync
```

**Why use uv?**
- ⚡ 10-100x faster than pip
- 🔒 Automatic dependency resolution
- 📦 Built-in lock file support

---

##### **Option C: Using pip + venv (Standard)**

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

**All methods install:**
- `browserbase>=1.2.0`
- `crewai-tools>=0.38.1`
- `html2text>=2024.2.26`
- `playwright>=1.51.0`
- `python-dotenv>=1.1.0`
- `streamlit>=1.44.1`

#### 3. Install Playwright Browsers

```bash
playwright install chromium
```

#### 4. Set Up Local LLM (Optional)

If using DeepSeek-R1 locally:

**Windows:**
```powershell
# Download and install Ollama for Windows
# Visit: https://ollama.com/download/windows
# Or use winget:
winget install Ollama.Ollama

# After installation, open a new terminal and pull the model
ollama pull deepseek-r1

# Verify installation
ollama list

# Start Ollama service (runs automatically on Windows, but if needed:)
ollama serve
```

**macOS/Linux:**
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull DeepSeek-R1 model
ollama pull deepseek-r1

# Verify installation
ollama list
```

---

## ⚙️ Configuration Guide

### Environment Variables

Create a `.env` file in the project root:

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**Windows (Command Prompt):**
```cmd
copy .env.example .env
```

**macOS/Linux:**
```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Required for all versions
BROWSERBASE_API_KEY=your_browserbase_api_key_here
BROWSERBASE_PROJECT_ID=your_browserbase_project_id_here

# Required only for app_openai.py
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL_NAME=gpt-4o-mini
```

### Getting API Keys

#### Browserbase API Key
1. Visit [https://browserbase.ai](https://browserbase.ai)
2. Sign up for an account
3. Navigate to Settings → API Keys
4. Generate a new API key
5. Copy and paste into `.env`

#### OpenAI API Key (Optional)
1. Visit [https://platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new secret key
5. Copy and paste into `.env`

### LLM Configuration

The project supports multiple LLM backends:

#### Option 1: Local DeepSeek-R1 (app.py)
```python
# No API key needed
# Ensure Ollama is running: ollama serve
# Model is loaded automatically
```

#### Option 2: Groq (app.py)
```python
llm = LLM(model="groq/meta-llama/llama-4-scout-17b-16e-instruct")
# Requires GROQ_API_KEY in environment
```

#### Option 3: OpenAI (app_openai.py)
```python
# Uses default OpenAI configuration
# Requires OPENAI_API_KEY in .env
```

---

## 🚀 Usage Instructions

### Running the Application

#### Using Local LLM (DeepSeek-R1 or Groq)

```bash
streamlit run app.py
```

#### Using OpenAI

```bash
streamlit run app_openai.py
```

### Using the Web Interface

1. **Launch the app**: The browser will open automatically at `http://localhost:8501`

2. **Configure Browserbase**:
   - Enter your Browserbase API Key in the sidebar
   - Or set it in `.env` file beforehand

3. **Enter Search Criteria**:
   - **Location**: City, area, or landmark (e.g., "New York", "Times Square")
   - **Check-in Date**: Select from date picker
   - **Check-out Date**: Must be after check-in date
   - **Number of Adults**: 1-10 guests

4. **Click "Search Hotels"**:
   - The system will display a loading spinner
   - Processing typically takes 1-3 minutes
   - Progress is shown in the terminal

5. **Review Results**:
   - Top 5 hotel recommendations
   - Detailed information for each hotel
   - Booking provider comparisons
   - Direct booking links

### Example Search

**Input:**
- Location: `Paris, France`
- Check-in: `2024-10-15`
- Check-out: `2024-10-18`
- Adults: `2`

**Expected Output:**
```
Here are our top 5 hotels in Paris for October 15-18, 2024:

1. Hotel Le Marais
   - Rating: 4.7/5
   - Price: €189/night
   - Location: Le Marais District
   - Amenities: Free WiFi, Breakfast included, Air conditioning
   - Booking Options:
     * Kayak: €189/night
     * Booking.com: €195/night
     * Hotels.com: €199/night
   - Book Now: https://www.kayak.com/hotels/...

2. Montmartre Boutique Hotel
   ...
```

---

## 📁 Project Structure

```
hotel-booking-crew/
│
├── app.py                  # Main application (Groq/Local LLM)
├── app_openai.py           # OpenAI variant
├── browserbase.py          # Browserbase tool implementation
├── kayak.py                # Kayak URL generator tool
│
├── pyproject.toml          # Project dependencies (uv format)
├── uv.lock                 # Dependency lock file
├── .env.example            # Environment variable template
├── .env                    # Your environment variables (not in git)
│
├── README.md               # Quick start guide
├── P-GUIDE.md              # This comprehensive guide
│
├── .venv/                  # Virtual environment (auto-generated)
│
└── assets/                 # Static assets (if any)
    └── browser-base.png    # Browserbase logo
```

### File Descriptions

| File             | Purpose                                         | Key Components                               |
| ---------------- | ----------------------------------------------- | -------------------------------------------- |
| `app.py`         | Main Streamlit application using Groq/Local LLM | UI, agent initialization, task orchestration |
| `app_openai.py`  | Alternative version using OpenAI                | Same as app.py but with OpenAI backend       |
| `browserbase.py` | Headless browser automation tool                | Playwright integration, HTML scraping        |
| `kayak.py`       | Kayak URL construction tool                     | URL formatting for hotel searches            |
| `pyproject.toml` | Project metadata and dependencies               | Package requirements, Python version         |
| `.env.example`   | Environment variable template                   | API key placeholders                         |

---

## 🔍 Implementation Details

### How the Browserbase Tool Works

```python
@tool("Browserbase tool")
def browserbase(url: str):
    """
    1. Establishes WebSocket connection to Browserbase cloud
    2. Connects to a remote Chromium browser instance
    3. Navigates to the specified URL
    4. Waits 25 seconds for JavaScript to load dynamic content
    5. Extracts full page HTML
    6. Converts HTML to clean markdown text
    7. Closes browser connection
    8. Returns text content to agent
    """
```

**Why Browserbase?**
- Handles JavaScript-heavy sites like Kayak
- Bypasses bot detection mechanisms
- Provides reliable, cloud-based browser infrastructure
- No need to manage local browser drivers

### How the Kayak Tool Works

```python
@tool("Kayak Hotel Tool")
def kayak_hotel_search(location_query, check_in_date, check_out_date, num_adults):
    """
    Constructs a Kayak URL following their specific format:
    https://www.kayak.co.in/hotels/{location}/{check_in}/{check_out}/{num_adults}adults
    
    Example:
    Input: "Paris", "2024-10-15", "2024-10-18", 2
    Output: https://www.kayak.co.in/hotels/Paris/2024-10-15/2024-10-18/2adults
    """
```

**Why This Approach?**
- Kayak doesn't provide a public API
- URL construction is predictable and reliable
- Combined with Browserbase, it enables full data extraction

### Agent Task Execution

#### Search Task Flow

```python
search_task = Task(
    description="Search hotels according to criteria {request}. Current year: {current_year}",
    expected_output=output_search_example,
    agent=hotels_agent,
)
```

**What Happens:**
1. Agent receives formatted request (e.g., "hotels in Paris from October 15 to October 18 for 2 adults")
2. Agent decides to use `kayak_hotels` tool
3. Tool generates URL
4. Agent uses `browserbase` tool with the URL
5. Browserbase returns scraped content
6. Agent processes content using LLM reasoning
7. Agent formats output according to expected structure

#### Provider Search Task Flow

```python
search_booking_providers_task = Task(
    description="Load hotel details and find available booking providers with their rates",
    expected_output=output_providers_example,
    agent=hotels_agent,
)
```

**What Happens:**
1. Agent receives hotel data from previous task
2. Agent identifies individual hotel URLs
3. Agent uses `browserbase` to visit each hotel's detail page
4. Agent extracts provider-specific pricing
5. Agent compares rates across providers
6. Agent formats comprehensive comparison

### CrewAI Planning Feature

```python
crew = Crew(
    agents=[hotels_agent, summarize_agent],
    tasks=[search_task, search_booking_providers_task],
    max_rpm=1,  # Rate limiting
    verbose=True,  # Show execution logs
    planning=True,  # Enable autonomous planning
    llm=load_llm(),
)
```

**Planning Benefits:**
- Crew creates an execution strategy before running tasks
- Optimizes task order and dependencies
- Handles edge cases and errors intelligently
- Improves overall result quality

---

## 🎯 How It Works

### End-to-End Execution Example

Let's trace a complete search for "Hotels in Tokyo":

#### **Step 1: User Input**
```
Location: Tokyo, Japan
Check-in: 2024-11-01
Check-out: 2024-11-03
Adults: 2
```

#### **Step 2: Request Formatting**
```python
request = "hotels in Tokyo, Japan from November 01 to November 03 for 2 adults"
```

#### **Step 3: Crew Planning**
CrewAI analyzes the request and creates a plan:
```
Plan:
1. Use Kayak tool to generate search URL
2. Use Browserbase to scrape Kayak results
3. Extract top 5 hotels with key details
4. For each hotel, visit detail page
5. Extract booking provider options
6. Summarize and format results
```

#### **Step 4: Task 1 Execution (Search)**

**Hotels Agent Reasoning:**
```
Thought: I need to search for hotels in Tokyo for the specified dates.
Action: Use kayak_hotel_search tool
Action Input: {
  "location_query": "Tokyo,Japan",
  "check_in_date": "2024-11-01",
  "check_out_date": "2024-11-03",
  "num_adults": 2
}
```

**Tool Output:**
```
https://www.kayak.co.in/hotels/Tokyo,Japan/2024-11-01/2024-11-03/2adults
```

**Hotels Agent Next Action:**
```
Thought: I have the URL, now I need to scrape the page
Action: Use browserbase tool
Action Input: {
  "url": "https://www.kayak.co.in/hotels/Tokyo,Japan/2024-11-01/2024-11-03/2adults"
}
```

**Browserbase Output:**
```markdown
# Hotels in Tokyo

## Hotel Gracery Shinjuku
Rating: 4.5/5
Price: ¥18,500/night
Location: Shinjuku
Amenities: Free WiFi, Restaurant, Godzilla View

## Park Hyatt Tokyo
Rating: 4.8/5
Price: ¥45,000/night
...
```

**Hotels Agent Final Output:**
```
Here are our top 5 hotels in Tokyo for November 1-3, 2024:

1. Hotel Gracery Shinjuku:
   - Rating: 4.5/5
   - Price: ¥18,500/night
   - Location: Shinjuku
   - Amenities: Free WiFi, Restaurant, Godzilla View
   - Booking: https://www.kayak.com/hotels/...
...
```

#### **Step 5: Task 2 Execution (Providers)**

Hotels Agent visits each hotel's detail page and extracts provider pricing:

```
Detailed information for hotels in Tokyo (November 1-3, 2024):

1. Hotel Gracery Shinjuku:
   - Room Types: Standard Double, Deluxe Twin
   - Price Range: ¥18,500-¥25,000/night
   - Special Offers: Free cancellation until Oct 25
   - Booking Options:
     * Kayak: ¥18,500/night
     * Booking.com: ¥19,200/night
     * Agoda: ¥18,800/night
     * Direct: ¥22,000/night
...
```

#### **Step 6: Display Results**

Streamlit renders the formatted output in the web interface.

---

## ✨ Key Features

### 1. **Multi-Agent Collaboration**
- Specialized agents for different tasks
- Autonomous task delegation
- Intelligent planning and reasoning

### 2. **Real-Time Web Scraping**
- Headless browser automation
- JavaScript rendering support
- Anti-bot detection bypass

### 3. **Multiple LLM Support**
- Local execution (DeepSeek-R1)
- Cloud-based options (Groq, OpenAI)
- Easy switching between providers

### 4. **Comprehensive Hotel Data**
- Ratings and reviews
- Pricing from multiple providers
- Amenities and features
- Location information
- Direct booking links

### 5. **User-Friendly Interface**
- Clean, intuitive Streamlit UI
- Real-time search progress
- Structured result presentation
- API key management

### 6. **Privacy-Focused**
- Option for 100% local execution
- No data sent to external APIs (when using local LLM)
- Secure API key handling

### 7. **Extensible Architecture**
- Easy to add new tools
- Simple to integrate new agents
- Modular design for customization

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### **Issue 1: "Browserbase API Key not found"**

**Symptoms:**
```
Error: Please enter your Browserbase API Key in the sidebar first!
```

**Solutions:**
1. Enter API key in the sidebar
2. Or add to `.env` file:
   ```env
   BROWSERBASE_API_KEY=your_key_here
   ```
3. Restart the Streamlit app

---

#### **Issue 2: "Check-out date must be after check-in date"**

**Symptoms:**
```
Error: Check-out date must be after check-in date!
```

**Solution:**
- Ensure check-out date is at least 1 day after check-in date
- Use the date picker to select valid dates

---

#### **Issue 3: Playwright browser not installed**

**Symptoms:**
```
Error: Executable doesn't exist at /path/to/chromium
```

**Solution:**
```bash
playwright install chromium
```

---

#### **Issue 4: Local LLM not responding (DeepSeek-R1)**

**Symptoms:**
- App hangs during search
- No results returned

**Solutions:**
1. Verify Ollama is running:
   ```bash
   ollama serve
   ```
2. Check model is installed:
   ```bash
   ollama list
   ```
3. Pull model if missing:
   ```bash
   ollama pull deepseek-r1
   ```

---

#### **Issue 5: "An error occurred during the search"**

**Symptoms:**
```
Error: An error occurred during the search: [error message]
```

**Solutions:**
1. Check internet connection
2. Verify Browserbase API key is valid
3. Check Browserbase account has available credits
4. Review terminal logs for detailed error messages
5. Try a different location or date range

---

#### **Issue 6: Slow search performance**

**Symptoms:**
- Search takes more than 5 minutes
- App appears frozen

**Solutions:**
1. **Reduce wait time in browserbase.py**:
   ```python
   sleep(15)  # Instead of 25
   ```
2. **Use faster LLM**:
   - Switch to Groq instead of local DeepSeek
   - Use GPT-4o-mini instead of GPT-4

3. **Check Browserbase status**:
   - Visit [Browserbase Status Page](https://status.browserbase.com)

---

#### **Issue 7: Dependencies not installing**

**Symptoms:**
```
Error: Could not find a version that satisfies the requirement...
```

**Solutions:**
1. **Update uv**:
   ```bash
   pip install --upgrade uv
   ```
2. **Clear cache**:
   ```bash
   uv cache clean
   ```
3. **Use pip instead**:
   ```bash
   pip install -r requirements.txt
   ```

---

#### **Issue 8: Streamlit not launching**

**Symptoms:**
```
Command 'streamlit' not found
```

**Solutions:**
1. **Activate virtual environment**:
   ```bash
   source .venv/bin/activate  # macOS/Linux
   .venv\Scripts\activate     # Windows
   ```
2. **Install Streamlit**:
   ```bash
   pip install streamlit
   ```

---

### Debug Mode

Enable verbose logging to diagnose issues:

```python
# In app.py, set verbose=True
crew = Crew(
    agents=[hotels_agent, summarize_agent],
    tasks=[search_task, search_booking_providers_task],
    verbose=True,  # Shows detailed execution logs
    ...
)
```

Check terminal output for detailed agent reasoning and tool calls.

---

## 🚀 Future Enhancements

### Planned Features

1. **Multi-City Search**
   - Compare hotels across multiple cities
   - Find best value destinations

2. **Advanced Filtering**
   - Filter by amenities (pool, gym, spa)
   - Price range constraints
   - Star rating requirements
   - Distance from landmarks

3. **Price Tracking**
   - Monitor price changes over time
   - Alert users when prices drop
   - Historical pricing data

4. **User Preferences**
   - Save favorite hotels
   - Remember search history
   - Personalized recommendations

5. **Booking Integration**
   - Direct booking through the app
   - Payment processing
   - Confirmation management

6. **Additional Data Sources**
   - Integrate Booking.com, Hotels.com, Expedia
   - Aggregate reviews from TripAdvisor
   - Include Airbnb options

7. **Mobile App**
   - Native iOS/Android apps
   - Push notifications for deals
   - Offline access to saved searches

8. **Multi-Language Support**
   - Support for 10+ languages
   - Localized pricing and dates

9. **Flight + Hotel Packages**
   - Extend to flight search
   - Bundle deals
   - Complete trip planning

10. **AI-Powered Recommendations**
    - Learn from user behavior
    - Suggest hotels based on past preferences
    - Predict best booking times

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### How to Contribute

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/hotel-booking-crew.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   ```bash
   streamlit run app.py
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "Add: your feature description"
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Describe your changes
   - Reference any related issues
   - Wait for review

### Contribution Guidelines

- **Code Quality**: Follow PEP 8 style guidelines
- **Documentation**: Update README and P-GUIDE for significant changes
- **Testing**: Ensure your changes don't break existing functionality
- **Commits**: Use clear, descriptive commit messages

### Areas for Contribution

- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🎨 UI/UX enhancements
- 🧪 Test coverage
- 🌐 Internationalization

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2024 HotelFinder Pro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Support & Contact

### Get Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/hotel-booking-crew/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/hotel-booking-crew/discussions)
- **Email**: support@hotelfinderpro.com

### Stay Updated

- **Newsletter**: [Subscribe to Daily Dose of Data Science](https://join.dailydoseofds.com)
- **Twitter**: [@HotelFinderPro](https://twitter.com/hotelfinderpro)
- **Blog**: [HotelFinder Pro Blog](https://blog.hotelfinderpro.com)

---

## 🙏 Acknowledgments

This project was built using amazing open-source technologies:

- **CrewAI**: Multi-agent orchestration framework
- **Browserbase**: Headless browser infrastructure
- **Streamlit**: Web application framework
- **Playwright**: Browser automation library
- **DeepSeek**: Open-source LLM
- **Ollama**: Local LLM runtime

Special thanks to the open-source community for making projects like this possible!

---

## 📊 Project Statistics

- **Lines of Code**: ~500
- **Number of Agents**: 2
- **Number of Tools**: 2
- **Number of Tasks**: 2
- **Supported LLMs**: 3 (DeepSeek, Groq, OpenAI)
- **Dependencies**: 6 core packages
- **Python Version**: 3.12+

---

## 🎓 Learning Resources

### Understanding Multi-Agent Systems
- [CrewAI Documentation](https://docs.crewai.com)
- [Multi-Agent Systems: A Modern Approach](https://www.multiagent.com)

### Web Scraping & Automation
- [Playwright Documentation](https://playwright.dev)
- [Browserbase Guides](https://docs.browserbase.com)

### Large Language Models
- [DeepSeek-R1 Paper](https://arxiv.org/abs/deepseek-r1)
- [Ollama Documentation](https://ollama.com/docs)
- [OpenAI API Reference](https://platform.openai.com/docs)

### Streamlit Development
- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Gallery](https://streamlit.io/gallery)

---

<div align="center">

**Built with ❤️ using CrewAI and Browserbase**

[⭐ Star this repo](https://github.com/yourusername/hotel-booking-crew) | [🐛 Report Bug](https://github.com/yourusername/hotel-booking-crew/issues) | [✨ Request Feature](https://github.com/yourusername/hotel-booking-crew/issues)

</div>
