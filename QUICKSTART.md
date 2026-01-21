# 🚀 Quick Start Guide - Your Setup

## ✅ What's Already Done

1. ✅ Conda environment `hotelbai` created
2. ✅ All dependencies installed (including litellm)
3. ✅ Playwright browsers installed
4. ✅ `.env` file configured with API keys
5. ✅ Browserbase logo added
6. ✅ Error handling added to app

## 🎯 Run the App Right Now

### Option 1: Simple Command
```powershell
conda activate hotelbai
streamlit run app.py
```

### Option 2: Using the Setup Script
```powershell
.\setup-windows.ps1
```

## 🌐 Access the App

After running, open your browser at:
- **Local:** http://localhost:8501
- Or use the URL shown in the terminal

## 🔑 Your API Keys (Already Configured)

Your `.env` file has:
- ✅ **OpenAI API Key** - For GPT-4o-mini
- ✅ **Browserbase API Key** - For web scraping
- ✅ **Browserbase Project ID** - For browser sessions

## 📝 How to Use the App

1. **Open the app** in your browser
2. **Enter search criteria:**
   - Location (e.g., "New York", "Paris", "Tokyo")
   - Check-in date
   - Check-out date
   - Number of adults
3. **Click "Search Hotels"**
4. **Wait 1-3 minutes** for results
5. **Review recommendations** with prices and booking links

## 🛠️ Troubleshooting

### If you see "Module not found" errors:
```powershell
conda activate hotelbai
pip install -r requirements.txt
```

### If Streamlit doesn't start:
```powershell
conda activate hotelbai
pip install streamlit
streamlit run app.py
```

### If browser doesn't open automatically:
```powershell
start http://localhost:8501
```

### If you get Playwright errors:
```powershell
conda activate hotelbai
playwright install chromium
```

## 🔄 Restart the App

If the app is already running and you need to restart:

1. **Stop current process:** Press `Ctrl+C` in the terminal
2. **Restart:** Run `streamlit run app.py` again

## 📊 Example Search

Try this to test the app:

**Input:**
- Location: `New York`
- Check-in: Tomorrow
- Check-out: Day after tomorrow
- Adults: `2`

**Expected:** List of 5 hotels with prices, ratings, and booking links

## 🎨 App Features

- ✨ Clean, modern UI
- 🔍 Real-time hotel search
- 💰 Price comparison across providers
- ⭐ Ratings and reviews
- 🏨 Amenities information
- 🔗 Direct booking links

## 📚 Documentation

- **P-GUIDE.md** - Complete project documentation
- **WINDOWS-SETUP.md** - Windows-specific setup
- **CONDA-SETUP.md** - Conda-specific setup
- **LITELLM-FIX.md** - LiteLLM troubleshooting
- **ISSUE-FIXED.md** - Logo issue resolution

## 🚨 Important Notes

1. **API Costs:** Using OpenAI GPT-4o-mini costs money. Monitor your usage at https://platform.openai.com/usage

2. **Browserbase Credits:** Free tier has limited sessions. Check your usage at https://browserbase.ai

3. **Search Time:** Each search takes 1-3 minutes due to web scraping

4. **Rate Limits:** Don't run multiple searches simultaneously

## 🆓 Free Alternatives

### Use Groq (Free Tier)
1. Get API key from https://console.groq.com
2. Add to `.env`: `GROQ_API_KEY=your_key`
3. Update `app.py` line 22:
   ```python
   return LLM(model="groq/llama-3.3-70b-versatile")
   ```

### Use Ollama (100% Local, Free)
1. Install: `winget install Ollama.Ollama`
2. Pull model: `ollama pull llama3.1`
3. Update `app.py` line 22:
   ```python
   return LLM(model="ollama/llama3.1")
   ```

## 🎯 Your Current Configuration

```
Environment: hotelbai (conda)
Python: 3.12
LLM: OpenAI GPT-4o-mini
Browser: Browserbase (cloud)
UI: Streamlit
```

## ✅ Final Checklist

Before running the app, verify:

- [ ] Conda environment `hotelbai` is activated
- [ ] All dependencies installed (`pip list` shows crewai, streamlit, etc.)
- [ ] Playwright browsers installed
- [ ] `.env` file has valid API keys
- [ ] No other Streamlit instances running on port 8501

## 🚀 Ready to Go!

Everything is set up! Just run:

```powershell
conda activate hotelbai
streamlit run app.py
```

Then open http://localhost:8501 and start searching for hotels! 🏨

---

**Need help?** Check the documentation files or open an issue on GitHub.
