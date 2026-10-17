@echo off
TITLE Aergia Studio Launcher
COLOR 0A

:: Ensure we are in the correct directory (Script Directory)
cd /d "%~dp0"

:: Set Python Path WITHOUT quotes here
set PYTHON="C:\Users\z143d\AppData\Local\Programs\Python\Python312\python.exe"

echo ===================================================
echo       PROJECT AERGIA: AI CONTENT STUDIO
echo ===================================================
echo.

:: 1. Start Chimera Backend (API)
echo [1/3] Launching Chimera Backend (Port 5001)...
start "Chimera Backend" cmd /k "set PORT=5001 && "%PYTHON%" "Project Chimera\project-chimera\backend-flask\app.py""

:: 2. Start Chimera Worker (Video Renderer)
echo [2/3] Launching Chimera Worker (Renderer)...
start "Chimera Worker" cmd /k ""%PYTHON%" "Project Chimera\source\worker.py""

:: 3. Start Hyperion Director (GUI)
echo [3/3] Launching Hyperion Interface...
start "Hyperion Director" cmd /k ""%PYTHON%" "Project Hyperion\hyperion_gui.py""

echo.
echo ===================================================
echo       STUDIO IS LIVE. GOOD LUCK, DIRECTOR.
echo ===================================================
pause
