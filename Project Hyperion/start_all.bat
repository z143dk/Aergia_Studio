@echo off
title Hyperion System Launcher

echo ===================================================
echo   PROJECT HYPERION - AI DIRECTOR SYSTEM STARTUP
echo ===================================================
echo.

echo [1/3] Starting Chimera Backend API (Port 5001)...
start "Chimera API" cmd /k "cd /d "%~dp0..\Project Chimera\project-chimera\backend-flask" && python app.py"

echo [2/3] Starting Chimera Worker (Port 8081)...
start "Chimera Worker" cmd /k "cd /d "%~dp0..\Project Chimera\project-chimera\backend-flask" && python worker.py"

echo Waiting 5 seconds for services to initialize...
timeout /t 5 /nobreak >nul

echo [3/3] Launching Hyperion Director App...
start "Hyperion Director" cmd /k "cd /d "%~dp0" && python hyperion_gui.py"

echo.
echo ===================================================
echo   SYSTEM IS LIVE.
echo   You can close this window, but keep the others open.
echo ===================================================
pause
