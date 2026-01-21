# 🪟 Windows Setup Guide for HotelFinder Pro

Complete setup guide for **Windows 10/11** users.

---

## 🚀 Quick Start (Windows)

### Prerequisites
- Windows 10 or Windows 11
- Python 3.12+ installed
- PowerShell or Command Prompt
- Internet connection

---

## Step-by-Step Setup

### 1. Clone the Repository

**Using PowerShell:**
```powershell
# Navigate to your desired directory
cd "a:\shinobi no shuriken\github repo\agentic system_\"

# Clone the repository
git clone https://github.com/yourusername/hotel-booking-crew.git
cd hotel-booking-crew
```

---

### 2. Choose Your Environment Manager

#### **Option A: Using Conda (Recommended for Windows)**

```powershell
# Create conda environment
conda create -n hotel-booking-crew python=3.12 -y

# Activate environment
conda activate hotel-booking-crew

# Install dependencies
pip install -r requirements.txt
```

#### **Option B: Using Python venv**

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt
```

#### **Option C: Using uv (Fastest)**

```powershell
# Install uv
pip install uv

# Sync dependencies
uv sync

# Activate the environment
.venv\Scripts\Activate.ps1
```

---

### 3. Install Playwright Browsers

```powershell
playwright install chromium
```

**If you get an error**, try:
```powershell
python -m playwright install chromium
```

---

### 4. Set Up Environment Variables

**Create .env file:**
```powershell
Copy-Item .env.example .env
```

**Edit the .env file:**
```powershell
notepad .env
```

Add your API keys:
```env
BROWSERBASE_API_KEY=your_browserbase_api_key_here
BROWSERBASE_PROJECT_ID=your_browserbase_project_id_here
```

**Get your Browserbase API key:**
1. Visit https://browserbase.ai
2. Sign up for an account
3. Go to Settings → API Keys
4. Copy your API key and paste it in `.env`

---

### 5. Install Ollama (Optional - For Local LLM)

**Method 1: Download Installer (Recommended)**
1. Visit https://ollama.com/download/windows
2. Download `OllamaSetup.exe`
3. Run the installer
4. Open a new PowerShell window

**Method 2: Using winget**
```powershell
winget install Ollama.Ollama
```

**Pull DeepSeek-R1 Model:**
```powershell
# Open a new terminal after installation
ollama pull deepseek-r1
```

**Verify Installation:**
```powershell
ollama list
```

You should see `deepseek-r1` in the list.

**Start Ollama Service (if needed):**
```powershell
ollama serve
```

---

### 6. Run the Application

**Using Local LLM (DeepSeek-R1 or Groq):**
```powershell
streamlit run app.py
```

**Using OpenAI:**
```powershell
streamlit run app_openai.py
```

The browser will automatically open at `http://localhost:8501`

---

## 🛠️ Windows-Specific Troubleshooting

### Issue 1: "Execution Policy" Error

**Error:**
```
cannot be loaded because running scripts is disabled on this system
```

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Issue 2: "python: command not found"

**Solution:**
1. Install Python from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Restart PowerShell

**Verify:**
```powershell
python --version
```

---

### Issue 3: "pip: command not found"

**Solution:**
```powershell
python -m ensurepip --upgrade
```

---

### Issue 4: Long Path Issues

**Error:**
```
The filename or extension is too long
```

**Solution:**
Enable long paths in Windows:
```powershell
# Run as Administrator
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

Or move your project to a shorter path like `C:\Projects\hotel-booking-crew`

---

### Issue 5: Playwright Installation Fails

**Solution:**
```powershell
# Install Visual C++ Redistributable
# Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe

# Then retry:
playwright install chromium
```

---

### Issue 6: Streamlit Not Opening Browser

**Solution:**
```powershell
# Manually open browser
start http://localhost:8501
```

Or add to Streamlit config:
```powershell
# Create config directory
mkdir $env:USERPROFILE\.streamlit

# Create config file
@"
[server]
headless = false
"@ | Out-File -FilePath $env:USERPROFILE\.streamlit\config.toml -Encoding UTF8
```

---

### Issue 7: Ollama Not Starting

**Solution:**
1. Check if Ollama is running:
   ```powershell
   Get-Process ollama
   ```

2. If not running, start it:
   ```powershell
   ollama serve
   ```

3. Check Windows Services:
   - Press `Win + R`
   - Type `services.msc`
   - Look for "Ollama Service"
   - Start it if stopped

---

## 📁 Windows File Paths

When working with paths in Windows:

**PowerShell:**
```powershell
cd "a:\shinobi no shuriken\github repo\agentic system_\hotel-booking-crew"
```

**Command Prompt:**
```cmd
cd /d "a:\shinobi no shuriken\github repo\agentic system_\hotel-booking-crew"
```

**Python (use forward slashes or raw strings):**
```python
# Option 1: Forward slashes
path = "a:/shinobi no shuriken/github repo/agentic system_/hotel-booking-crew"

# Option 2: Raw string
path = r"a:\shinobi no shuriken\github repo\agentic system_\hotel-booking-crew"
```

---

## 🔧 Useful Windows Commands

### Check Python Version
```powershell
python --version
```

### Check Installed Packages
```powershell
pip list
```

### Update pip
```powershell
python -m pip install --upgrade pip
```

### Clear Terminal
```powershell
cls
```

### List Files
```powershell
dir
# or
ls
```

### View Environment Variables
```powershell
Get-ChildItem Env:
```

### Set Environment Variable (Temporary)
```powershell
$env:BROWSERBASE_API_KEY = "your_key_here"
```

---

## 🎯 Complete Setup Example (Windows + Conda)

Here's everything in one go:

```powershell
# 1. Navigate to project
cd "a:\shinobi no shuriken\github repo\agentic system_\hotel-booking-crew"

# 2. Create conda environment
conda create -n hotel-booking-crew python=3.12 -y

# 3. Activate environment
conda activate hotel-booking-crew

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install Playwright
playwright install chromium

# 6. Create .env file
Copy-Item .env.example .env

# 7. Edit .env (add your API keys)
notepad .env

# 8. Install Ollama (optional)
winget install Ollama.Ollama

# 9. Pull DeepSeek model (in new terminal)
ollama pull deepseek-r1

# 10. Run the app
streamlit run app.py
```

---

## 🌐 Opening the App

After running `streamlit run app.py`, the browser should open automatically.

If not, manually open:
```
http://localhost:8501
```

**Or use PowerShell:**
```powershell
start http://localhost:8501
```

---

## 🔄 Updating the Project

```powershell
# Activate environment
conda activate hotel-booking-crew

# Pull latest changes
git pull

# Update dependencies
pip install --upgrade -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 📝 Windows Terminal Tips

### Use Windows Terminal (Recommended)
1. Install from Microsoft Store: "Windows Terminal"
2. Better PowerShell experience
3. Multiple tabs support
4. Better font rendering

### Set PowerShell as Default
1. Open Windows Terminal
2. Settings → Startup
3. Default profile → PowerShell

---

## 🎨 Making PowerShell Better

### Install Oh My Posh (Optional)
```powershell
winget install JanDeDobbeleer.OhMyPosh -s winget
```

### Enable Conda in PowerShell
```powershell
conda init powershell
```

---

## 🆘 Still Having Issues?

1. **Check Python Installation:**
   ```powershell
   python --version
   pip --version
   ```

2. **Check Conda Installation:**
   ```powershell
   conda --version
   ```

3. **Check Git Installation:**
   ```powershell
   git --version
   ```

4. **Restart PowerShell** after installing new software

5. **Run as Administrator** if you get permission errors

6. **Check Antivirus** - Sometimes blocks Python scripts

---

## 📚 Additional Resources

- [Python for Windows](https://www.python.org/downloads/windows/)
- [Conda for Windows](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html)
- [Git for Windows](https://git-scm.com/download/win)
- [Windows Terminal](https://aka.ms/terminal)
- [Ollama for Windows](https://ollama.com/download/windows)

---

## ✅ Verification Checklist

Before running the app, verify:

- [ ] Python 3.12+ installed (`python --version`)
- [ ] Conda or venv environment activated
- [ ] All dependencies installed (`pip list`)
- [ ] Playwright browsers installed
- [ ] `.env` file created with API keys
- [ ] Ollama installed (if using local LLM)
- [ ] DeepSeek-R1 model pulled (`ollama list`)

---

**Ready to go! Run `streamlit run app.py` and start searching for hotels! 🏨**
