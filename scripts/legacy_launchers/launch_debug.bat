@echo off
TITLE Aergia Dashboard Debugger
echo Launching Dashboard in Debug Mode...
echo Python: "C:\Users\z143d\AppData\Local\Programs\Python\Python312\python.exe"
echo Script: aergia_dashboard.py
echo.

"C:\Users\z143d\AppData\Local\Programs\Python\Python312\python.exe" "aergia_dashboard.py"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo CRASHED with Error Level %ERRORLEVEL%
)

echo.
echo Closing in 30 seconds...
timeout /t 30
