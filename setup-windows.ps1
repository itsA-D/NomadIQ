# Complete Setup Script for Windows + Conda
# Run this in PowerShell

Write-Host "🚀 Setting up HotelFinder Pro..." -ForegroundColor Cyan

# 1. Navigate to project directory
Write-Host "`n📁 Step 1: Navigating to project directory..." -ForegroundColor Yellow
Set-Location "a:\shinobi no shuriken\github repo\agentic system_\hotel-booking-crew"

# 2. Create conda environment (if not exists)
Write-Host "`n🐍 Step 2: Creating conda environment 'hotelbai'..." -ForegroundColor Yellow
conda create -n hotelbai python=3.12 -y

# 3. Activate environment
Write-Host "`n✅ Step 3: Activating conda environment..." -ForegroundColor Yellow
conda activate hotelbai

# 4. Install dependencies
Write-Host "`n📦 Step 4: Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# 5. Install Playwright browsers
Write-Host "`n🌐 Step 5: Installing Playwright browsers..." -ForegroundColor Yellow
playwright install chromium

# 6. Verify .env file exists
Write-Host "`n🔑 Step 6: Checking .env file..." -ForegroundColor Yellow
if (Test-Path .env) {
    Write-Host "✅ .env file found!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "📝 Please edit .env and add your API keys!" -ForegroundColor Red
}

# 7. Display next steps
Write-Host "`n✅ Setup Complete!" -ForegroundColor Green
Write-Host "`n📋 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file and add your API keys:" -ForegroundColor White
Write-Host "   notepad .env" -ForegroundColor Gray
Write-Host "`n2. Run the application:" -ForegroundColor White
Write-Host "   conda activate hotelbai" -ForegroundColor Gray
Write-Host "   streamlit run app.py" -ForegroundColor Gray
Write-Host "`n3. Open your browser at the URL shown (usually http://localhost:8501)" -ForegroundColor White
Write-Host "`n🎉 Happy hotel hunting!" -ForegroundColor Cyan
