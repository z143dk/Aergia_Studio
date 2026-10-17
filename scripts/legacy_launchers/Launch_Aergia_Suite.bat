@echo off
TITLE AERGIA OS v2.0 - MASTER LAUNCH SEQUENCE
cd /d "%~dp0"

echo.
echo ========================================================
echo        🏛️  AERGIA OS v2.0 - INITIALIZING SUITE  🏛️
echo ========================================================
echo.

echo [1/3] 🧠 Starting API Server (The Brain)...
start "Aergia API" /MIN cmd /c "Launch_Aergia_API.bat"

echo.
echo [*] Checking local AI engine (Ollama)...
tasklist /fi "imagename eq ollama.exe" 2>nul | find /i "ollama.exe" >nul
if errorlevel 1 (
    echo     Ollama not running. Initializing local service...
    start "" "ollama"
) else (
    echo     Ollama service is already active.
)

echo       Waiting 5 seconds for neurons to fire...
timeout /t 5 /nobreak >nul

echo.
echo [2/3] 🖥️  Launching Desktop Orchestrator...
start "" "Launch_Aergia_Orchestrator.bat"

echo.
echo [3/3] 🌐 Opening Web Command Center...
start "" "http://127.0.0.1:5050"

echo.
echo ========================================================
echo                🚀  SYSTEMS ONLINE  🚀
echo ========================================================
echo.
echo You may close this window.
timeout /t 10
exit
