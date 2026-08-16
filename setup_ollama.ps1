# PowerShell script to set up Ollama for HotelFinder Pro
Write-Host "Setting up Ollama for HotelFinder Pro..." -ForegroundColor Green
Write-Host ""

# Check if Ollama is in PATH
$ollamaPath = Get-Command ollama -ErrorAction SilentlyContinue
if ($ollamaPath) {
    Write-Host "Ollama is already installed and in PATH" -ForegroundColor Green
} else {
    Write-Host "Ollama is installed but not in PATH. Adding to PATH..." -ForegroundColor Yellow
    $ollamaInstallPath = "$env:LOCALAPPDATA\Programs\Ollama"
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($currentPath -notlike "*$ollamaInstallPath*") {
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$ollamaInstallPath", "User")
        Write-Host "PATH updated. Please restart your terminal and run this script again." -ForegroundColor Yellow
        Write-Host "Or refresh your environment with: `$env:Path = [System.Environment]::GetEnvironmentVariable(`"Path`",`"User`")" -ForegroundColor Cyan
        pause
        exit 1
    }
}

# Check if Ollama is already running
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -UseBasicParsing -TimeoutSec 2
    if ($response.StatusCode -eq 200) {
        Write-Host "Ollama is already running" -ForegroundColor Green
    }
} catch {
    Write-Host "Starting Ollama server..." -ForegroundColor Yellow
    Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Write-Host "Waiting for Ollama to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
}

# Check if a llama3.x model is already downloaded
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -UseBasicParsing
    $tags = $response.Content | ConvertFrom-Json
    $hasLlama = $false
    foreach ($m in $tags.models) {
        if ($m.name -like "llama3*") { $hasLlama = $true; break }
    }

    if ($hasLlama) {
        Write-Host "Llama3 model is already downloaded" -ForegroundColor Green
        foreach ($m in $tags.models) {
            Write-Host "  - $($m.name)" -ForegroundColor White
        }
    } else {
        Write-Host "Downloading llama3.2 model (this may take a while)..." -ForegroundColor Yellow
        ollama pull llama3.2
    }
} catch {
    Write-Host "Downloading llama3.2 model (this may take a while)..." -ForegroundColor Yellow
    ollama pull llama3.2
}

Write-Host ""
Write-Host "Setup complete! Ollama is ready to use." -ForegroundColor Green
Write-Host "You can now run the HotelFinder Pro application." -ForegroundColor Green
pause
