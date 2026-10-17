@echo off
setlocal enableextensions enabledelayedexpansion

REM ---- Hard-pin the real Python (bypass Windows Store alias) ----
set "PY=python.exe"

REM ---- Root folder ----
set "ROOT=C:\Users\z143d\Desktop\Aergia_Studio"

echo.
echo ============================
echo   AERGIA STUDIO LAUNCHER
echo ============================
echo ROOT = %ROOT%
echo PY   = %PY%
echo.

REM ---- Validate ----
if not exist "%PY%" (
  echo [ERROR] Python not found at: %PY%
  echo Fix: update PY in this bat file.
  pause
  exit /b 1
)

if not exist "%ROOT%" (
  echo [ERROR] Root not found at: %ROOT%
  pause
  exit /b 1
)

REM ---- Always run from ROOT ----
cd /d "%ROOT%"

REM ---- Optional: show python identity ----
echo [INFO] Python version:
"%PY%" --version
echo.

REM ---- Launch dashboard ----
if exist "%ROOT%\aergia_dashboard.py" (
  echo [INFO] Launching aergia_dashboard.py ...
  "%PY%" "%ROOT%\aergia_dashboard.py"
) else (
  echo [ERROR] aergia_dashboard.py missing in ROOT.
  echo Expected: %ROOT%\aergia_dashboard.py
)

echo.
echo [INFO] Launcher finished. If there was an error above, copy it back into chat.
pause
endlocal
