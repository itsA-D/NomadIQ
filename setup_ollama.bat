@echo off
echo Setting up Ollama for HotelFinder Pro...
echo.

REM Check if Ollama is installed
where ollama >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Ollama is already installed and in PATH
    goto :check_running
) else (
    echo Ollama is installed but not in PATH. Adding to PATH...
    setx PATH "%PATH%;C:\Users\%USERNAME%\AppData\Local\Programs\Ollama" /M
    echo PATH updated. Please restart your terminal and run this script again.
    pause
    exit /b 1
)

:check_running
REM Check if Ollama is already running
curl -s http://localhost:11434/api/tags >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Ollama is already running
    goto :pull_model
) else (
    echo Starting Ollama server...
    start "" ollama serve
    echo Waiting for Ollama to start...
    timeout /t 5 /nobreak >nul
)

:pull_model
REM Check if any llama3 model is already downloaded
curl -s http://localhost:11434/api/tags | findstr "llama3" >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo A llama3 model is already downloaded
    goto :done
) else (
    echo Downloading llama3.2 model (this may take a while)...
    ollama pull llama3.2
)

:done
echo.
echo Setup complete! Ollama is ready to use.
echo You can now run the HotelFinder Pro application.
pause
