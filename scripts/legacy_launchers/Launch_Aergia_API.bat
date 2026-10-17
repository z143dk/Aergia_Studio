@echo off
title Aergia API Server
cd /d "%~dp0"

echo.
echo ========================================
echo   AERGIA API SERVER
echo ========================================
echo.
echo Starting Flask API on http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

"C:\Users\z143d\AppData\Local\Programs\Python\Python312\python.exe" aergia_api.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start API server
    echo.
    pause
)
