@echo off
echo ==========================================
echo Starting Project Chimera Ecosystem
echo ==========================================

:: Set the Python Path explicitly since it's not in the system PATH
set PYTHON_EXE="C:\Users\z143d\AppData\Local\Programs\Python\Python312\python.exe"

echo.
echo 1. Starting React Frontend (Studio Dashboard)...
start "Chimera Frontend" cmd /k "cd /d "%~dp0Project Chimera\project-chimera\studio-dashboard-react" && set BROWSER=none && set HOST=0.0.0.0 && npm start"

echo.
echo 2. Starting API Server (Port 5001)...
start "Chimera API Server" cmd /k "cd /d "%~dp0Project Chimera\project-chimera\backend-flask" && set PORT=5001 && %PYTHON_EXE% app.py"

echo.
echo 3. Starting Background Worker (Port 8081)...
start "Chimera Worker" cmd /k "cd /d "%~dp0Project Chimera\project-chimera\backend-flask" && set PORT=8081 && %PYTHON_EXE% worker.py"

echo.
echo ==========================================
echo Waiting for services to initialize...
timeout /t 10
echo Launching Chimera Studio (App Mode)...
start chrome --app=http://localhost:3000
echo ==========================================
echo You can close this window now.
echo ==========================================
pause
