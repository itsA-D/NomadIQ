# ⚡ QUICK FIX - Use Groq (Free & Fast)

## 🚨 Problem
- OpenAI quota exceeded ❌
- Ollama llama3.1 download takes 3+ hours ⏳

## ✅ Solution: Use Groq (Free, No Download)

Groq provides **free API access** to fast LLMs. No waiting, no downloads!

---

## 🚀 Setup Groq (5 Minutes)

### Step 1: Get Groq API Key
1. Visit https://console.groq.com
2. Sign up (free)
3. Go to "API Keys"
4. Create a new API key
5. Copy the key

### Step 2: Add to .env
```powershell
notepad .env
```

Add this line:
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
```

Save and close.

### Step 3: Update app.py

Open `app.py` and find line 17-23 (the `load_llm()` function).

**Replace with:**
```python
def load_llm():
    """Initialize and return LLM"""
    # Using Groq (free, fast, cloud-based)
    # Get API key from https://console.groq.com
    return LLM(model="groq/llama-3.3-70b-versatile")
```

### Step 4: Run the App
```powershell
conda activate hotelbai
streamlit run app.py
```

---

## ✅ Done!

Your app now uses Groq:
- ✅ **Free** (generous free tier)
- ✅ **Fast** (faster than OpenAI)
- ✅ **No downloads** (cloud-based)
- ✅ **No quota issues** (for reasonable usage)

---

## 📊 Groq vs Ollama

| Feature | Groq               | Ollama            |
| ------- | ------------------ | ----------------- |
| Cost    | Free tier          | 100% free         |
| Speed   | ⚡⚡⚡ Very fast      | 🐢 Slower (CPU)    |
| Setup   | 5 minutes          | 3+ hours download |
| Privacy | Cloud              | Local             |
| Quota   | Generous free tier | Unlimited         |

**Recommendation:** Use Groq now, switch to Ollama later if you want 100% local.

---

## 🔧 Complete Fix (Copy-Paste)

### 1. Edit .env
```env
GROQ_API_KEY=gsk_your_actual_key_here
BROWSERBASE_API_KEY=bb_live_OVmsLZxJqijTnivAOi_xJQSVBhw
BROWSERBASE_PROJECT_ID=bb4be6c6-e340-4f08-8845-3b5fabb5840c
```

### 2. Edit app.py (lines 17-23)
```python
def load_llm():
    """Initialize and return LLM"""
    # Using Groq (free, fast, cloud-based)
    # Get API key from https://console.groq.com
    return LLM(model="groq/llama-3.3-70b-versatile")
```

### 3. Run
```powershell
conda activate hotelbai
streamlit run app.py
```

---

## 🎯 Test It

1. Open http://localhost:8501
2. Enter: Location = "New York"
3. Click "Search Hotels"
4. Wait ~2 minutes
5. See results! 🏨

---

## 💡 Groq Free Tier Limits

- **Requests:** 30 requests/minute
- **Tokens:** 6,000 tokens/minute
- **Daily:** Generous (check console.groq.com)

**For this app:** You can do ~10-20 hotel searches per day on free tier.

---

## 🔄 If You Want Ollama Later

Once llama3.1 finishes downloading (check with `ollama list`):

```python
# In app.py, line 17-23:
def load_llm():
    """Initialize and return LLM"""
    return LLM(model="ollama/llama3.1", base_url="http://localhost:11434")
```

Then restart the app.

---

## ✅ Summary

**Before:** OpenAI quota error ❌  
**Now:** Groq (free, fast) ✅  
**Later:** Ollama (free, unlimited) ✅

---

**Get your Groq API key now:** https://console.groq.com

Then update `.env` and `app.py` as shown above! 🚀
