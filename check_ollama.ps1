# Quick diagnostic script to check Ollama status
Write-Host "Checking Ollama status..." -ForegroundColor Cyan
Write-Host ""

# Check if Ollama is in PATH
$ollamaPath = Get-Command ollama -ErrorAction SilentlyContinue
if ($ollamaPath) {
    Write-Host "✓ Ollama found in PATH: $($ollamaPath.Source)" -ForegroundColor Green
} else {
    Write-Host "✗ Ollama not found in PATH" -ForegroundColor Red
    Write-Host "  Run: `$env:Path = [System.Environment]::GetEnvironmentVariable('Path','User')" -ForegroundColor Yellow
}

# Check if Ollama is running
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -UseBasicParsing -TimeoutSec 2
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Ollama server is running" -ForegroundColor Green
        
        # List available models
        $tags = $response.Content | ConvertFrom-Json
        Write-Host "  Available models:" -ForegroundColor Cyan
        foreach ($model in $tags.models) {
            Write-Host "    - $($model.name)" -ForegroundColor White
        }
    }
} catch {
    Write-Host "✗ Ollama server is not running" -ForegroundColor Red
    Write-Host "  Start it with: ollama serve" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "If Ollama is not in PATH, close and reopen your terminal." -ForegroundColor Yellow
pause
