import sys
import datetime
import streamlit as st
import os
from crewai import Crew, Process, Task, Agent, LLM
from browserbase import browserbase
from kayak import kayak_hotels
from dotenv import load_dotenv

# Page configuration
st.set_page_config(page_title="🏨 HotelFinder Pro", layout="wide")

# Title and subtitle with custom HTML for blue color
st.markdown("<h1 style='color: #0066cc;'>🏨 HotelFinder Pro</h1>", unsafe_allow_html=True)
st.subheader("Powered by Browserbase and CrewAI")

def load_llm():
    """Initialize and return LLM"""
    # Using Groq (free, fast, cloud-based)
    # Get API key from https://console.groq.com and add to .env as GROQ_API_KEY
    # 
    # Alternative: Use Ollama (100% free, local)
    # Install: winget install Ollama.Ollama
    # Pull model: ollama pull llama3.1
    # Then use: LLM(model="ollama/llama3.1", base_url="http://localhost:11434")
    return LLM(model="groq/llama-3.3-70b-versatile")

# Sidebar for API key input
with st.sidebar:
    # Add Browserbase logo and Configuration header in the same line
    col1, col2 = st.columns([1, 3])
    with col1:
        # Add vertical space to align with header
        st.write("")
        # Try to load logo, but don't crash if it's missing
        try:
            st.image("./assets/browser-base.png", width=65)
        except:
            st.write("🌐")  # Fallback emoji if image not found
    with col2:
        st.header("Browserbase Configuration")
    
    # Add hyperlink to get API key
    st.markdown("[Get your API key](https://browserbase.ai)", unsafe_allow_html=True)
    
    browserbase_api_key = st.text_input("Enter your Browserbase API Key", type="password")
    
    # Store API key as environment variable
    if browserbase_api_key:
        os.environ["BROWSERBASE_API_KEY"] = browserbase_api_key
        st.success("API Key stored successfully!")

# Load environment variables
load_dotenv()  # take environment variables from .env.

# Main content
st.markdown("---")

# Hotel search form
st.header("Search for Hotels")
col1, col2 = st.columns(2)

with col1:
    location = st.text_input("Location", value="", placeholder="e.g., New York, Paris, Tokyo")
    num_adults = st.number_input("Number of Adults", min_value=1, max_value=10, value=2)

with col2:
    check_in_date = st.date_input("Check-in Date", datetime.date.today())
    check_out_date = st.date_input("Check-out Date", datetime.date.today() + datetime.timedelta(days=1))
    # Add more options if needed

search_button = st.button("Search Hotels")

# Load the LLM to be shared across all components
shared_llm = load_llm()

# Initialize agents
hotels_agent = Agent(
    role="Hotels",
    goal="Search hotels",
    backstory="I am an agent that can search for hotels and find the best accommodations.",
    tools=[kayak_hotels, browserbase],
    allow_delegation=False,
    llm=shared_llm,
)

summarize_agent = Agent(
    role="Summarize",
    goal="Summarize hotel information",
    backstory="I am an agent that can summarize hotel details and amenities.",
    allow_delegation=False,
    llm=shared_llm,
)

output_search_example = """
Here are our top 5 hotels in New York for September 21-22, 2024:
1. Hilton Times Square:
   - Rating: 4.5/5
   - Price: $299/night
   - Location: Times Square
   - Amenities: Pool, Spa, Restaurant
   - Booking: https://www.kayak.com/hotels/hilton-times-square
"""

search_task = Task(
    description=(
        "Search hotels according to criteria {request}. Current year: {current_year}"
    ),
    expected_output=output_search_example,
    agent=hotels_agent,
)

output_providers_example = """
Detailed information for hotels in New York (September 21-22, 2024):
1. Hilton Times Square:
   - Room Types: Deluxe King, Double Queen
   - Price Range: $299-$499/night
   - Special Offers: Free breakfast, Free cancellation
   - Booking Options:
     * Kayak: $299/night
     * Hotels.com: $315/night
     * Direct: $325/night
"""

search_booking_providers_task = Task(
    description="Load hotel details and find available booking providers with their rates",
    expected_output=output_providers_example,
    agent=hotels_agent,
)

# Search functionality
if search_button:
    # Validation checks
    if not os.environ.get("BROWSERBASE_API_KEY"):
        st.error("❌ Please enter your Browserbase API Key in the sidebar first!")
    elif not location or location.strip() == "" or location == "Enter city, area, or landmark":
        st.error("❌ Please enter a valid location!")
    elif check_out_date <= check_in_date:
        st.error("❌ Check-out date must be after check-in date!")
    elif num_adults < 1 or num_adults > 10:
        st.error("❌ Number of adults must be between 1 and 10!")
    else:
        with st.spinner("🔍 Searching for hotels... This may take 2-3 minutes."):
            try:
                # Format the request
                request = f"hotels in {location.strip()} from {check_in_date.strftime('%B %d')} to {check_out_date.strftime('%B %d')} for {num_adults} adults"
                
                crew = Crew(
                    agents=[hotels_agent, summarize_agent],
                    tasks=[search_task, search_booking_providers_task],
                    max_rpm=1,
                    verbose=True,
                    planning=True,
                    llm=shared_llm,
                    planning_llm=shared_llm, # This explicitly stops the planner from using OpenAI!
                )
                
                # Execute the search
                result = crew.kickoff(
                    inputs={
                        "request": request,
                        "current_year": datetime.date.today().year,
                    }
                )
                
                # Display results
                st.success("✅ Search completed!")
                st.markdown("## 🏨 Hotel Results")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"❌ An error occurred during the search")
                st.exception(e)
                st.info("💡 Common fixes:")
                st.info("1. Make sure Ollama is running: `ollama serve`")
                st.info("2. Make sure llama3.1 is installed: `ollama pull llama3.1`")
                st.info("3. Check your Browserbase API key is valid")
                st.info("4. Try a different location or date range")

# Add some information about the app
st.markdown("---")
st.markdown("""
### About HotelFinder Pro
This application uses AI agents to search for hotels and find the best accommodations for you.
Simply enter your desired location, dates, and number of guests to get started.

Features:
- Real-time hotel availability
- Comprehensive price comparison
- Detailed hotel information and amenities
- Multiple booking options
""")