@echo off
REM Document Summarizer - Startup Script for Windows
REM This script automatically starts both Ollama and Flask

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║      Document Summarizer - Startup Script                   ║
echo ║      Powered by AI - Made with ❤️                            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check if this is the first run
if not exist ".venv" (
    echo ⚠️  Virtual environment not found!
    echo Please run: python -m venv .venv
    echo Then run: .venv\Scripts\activate
    echo Then run: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment activated

REM Check if Ollama is installed
where ollama >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ⚠️  Ollama not found in PATH!
    echo Please install Ollama from: https://ollama.ai
    echo And make sure it's added to your system PATH
    pause
    exit /b 1
)

echo ✅ Ollama is installed

REM Check if required models are available
echo.
echo 🔍 Checking for required models...
ollama list | findstr "llama3.2:latest" >nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 📥 Pulling llama3.2 model (first time only, ~4GB)...
    call ollama pull llama3.2
)

ollama list | findstr "nomic-embed-text" >nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 📥 Pulling nomic-embed-text model (first time only, ~2GB)...
    call ollama pull nomic-embed-text
)

echo ✅ All models are available

REM Start Ollama server
echo.
echo 🚀 Starting Ollama server...
start "" cmd /k ollama serve

REM Wait for Ollama to start
timeout /t 5 /nobreak

REM Start Simple HTTP Server (no external dependencies!)
echo.
echo 🚀 Starting backend server...
timeout /t 2 /nobreak

start "" python server.py

REM Wait for Flask to start
timeout /t 3 /nobreak

REM Open browser
echo.
echo 🌐 Opening browser...
timeout /t 2 /nobreak

REM Try to open in default browser
start http://localhost:5000

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║  ✅ Document Summarizer is starting!                        ║
echo ║                                                              ║
echo ║  📍 URL: http://localhost:5000                              ║
echo ║                                                              ║
echo ║  Two windows should have opened:                            ║
echo ║  1. Ollama server (port 11434)                              ║
echo ║  2. Flask backend (port 5000)                               ║
echo ║                                                              ║
echo ║  ⚠️  Keep both windows open while using the app             ║
echo ║                                                              ║
echo ║  📖 For help, see QUICKSTART.md or README.md                ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Keep this window open
echo Press any key to exit and close both servers...
pause
