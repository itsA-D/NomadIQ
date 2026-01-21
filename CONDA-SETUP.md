# 🐍 Conda Setup Guide for HotelFinder Pro

This guide is specifically for users who prefer **conda** (Anaconda/Miniconda) over uv.

---

## Quick Start with Conda

### 1. Create Conda Environment

```bash
# Create a new environment with Python 3.12
conda create -n hotel-booking-crew python=3.12 -y
```

### 2. Activate Environment

```bash
conda activate hotel-booking-crew
```

You should see `(hotel-booking-crew)` in your terminal prompt.

### 3. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

**Note:** We use `pip` inside the conda environment because some packages (like `crewai-tools`) are not available on conda channels.

### 4. Install Playwright Browsers

```bash
playwright install chromium
```

### 5. Set Up Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API keys
# Use notepad, vim, or any text editor
notepad .env  # Windows
nano .env     # macOS/Linux
```

Add your keys:
```env
BROWSERBASE_API_KEY=your_key_here
BROWSERBASE_PROJECT_ID=your_project_id_here
```

### 6. Run the Application

```bash
streamlit run app.py
```

---

## Conda vs uv: Which Should You Use?

### Use **conda** if:
- ✅ You already have Anaconda/Miniconda installed
- ✅ You work with data science projects (NumPy, Pandas, etc.)
- ✅ You need to manage multiple Python versions
- ✅ You prefer a familiar workflow
- ✅ You need system-level dependencies (C libraries, etc.)

### Use **uv** if:
- ⚡ You want the fastest package installation
- 🔒 You need reproducible builds (lock files)
- 🚀 You're starting a new project from scratch
- 📦 You only work with Python packages

---

## Managing Your Conda Environment

### Activate Environment
```bash
conda activate hotel-booking-crew
```

### Deactivate Environment
```bash
conda deactivate
```

### List All Environments
```bash
conda env list
```

### Remove Environment (if needed)
```bash
conda remove -n hotel-booking-crew --all
```

### Export Environment (for sharing)
```bash
conda env export > environment.yml
```

### Create from environment.yml
```bash
conda env create -f environment.yml
```

---

## Updating Dependencies

### Update a specific package
```bash
conda activate hotel-booking-crew
pip install --upgrade streamlit
```

### Update all packages
```bash
pip install --upgrade -r requirements.txt
```

---

## Troubleshooting Conda Issues

### Issue: "conda: command not found"

**Solution:**
1. Make sure Anaconda/Miniconda is installed
2. Restart your terminal
3. Or manually activate conda:
   ```bash
   # Windows
   C:\Users\YourName\anaconda3\Scripts\activate.bat
   
   # macOS/Linux
   source ~/anaconda3/bin/activate
   ```

### Issue: "Package not found in conda channels"

**Solution:**
Use pip instead (it's fine to use pip inside conda):
```bash
conda activate hotel-booking-crew
pip install package-name
```

### Issue: Conflicts between conda and pip

**Solution:**
Install conda packages first, then pip packages:
```bash
# Install what's available via conda
conda install python=3.12 -y

# Then install the rest via pip
pip install -r requirements.txt
```

---

## Why We Use pip Inside Conda

For this project, we use `pip install -r requirements.txt` inside the conda environment because:

1. **CrewAI** is not available on conda channels
2. **Browserbase** is a newer package only on PyPI
3. **Mixing is safe** when done correctly (conda environment + pip packages)

This is a **recommended practice** by Anaconda for packages not available via conda.

---

## Complete Setup Example

Here's the complete setup from scratch:

```bash
# 1. Navigate to project directory
cd "a:\shinobi no shuriken\github repo\agentic system_\hotel-booking-crew"

# 2. Create conda environment
conda create -n hotel-booking-crew python=3.12 -y

# 3. Activate environment
conda activate hotel-booking-crew

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install Playwright browsers
playwright install chromium

# 6. Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# 7. Run the app
streamlit run app.py
```

---

## Next Steps

After setup, check out:
- **P-GUIDE.md** - Complete project documentation
- **README.md** - Quick start guide
- **.env.example** - Environment variable template

---

## Need Help?

- Check the main **P-GUIDE.md** for detailed troubleshooting
- Visit [Conda Documentation](https://docs.conda.io)
- Open an issue on GitHub

---

**Happy Coding! 🚀**
