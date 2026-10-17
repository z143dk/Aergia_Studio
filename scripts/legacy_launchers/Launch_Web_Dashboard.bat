@echo off
TITLE Aergia Web Dashboard (WSL Mode)
COLOR 0B

echo ===================================================
echo       AERGIA WEB DASHBOARD - WSL LAUNCHER
echo ===================================================
echo.
echo [INFO] Starting Flask Server inside Ubuntu WSL...
echo [INFO] Opening Browser...
start "" "http://127.0.0.1:5050"

wsl -d Ubuntu -e bash -c "cd ~/Aergia_Studio && source venv/bin/activate && python3 aergia_api.py"

pause
