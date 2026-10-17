@echo off
TITLE Aergia OS - Command Center
COLOR 0B

cd /d "%~dp0"
set PYTHON="C:\Users\z143d\AppData\Local\Programs\Python\Python312\pythonw.exe"

echo Launching Aergia Dashboard...
start "Aergia OS" "%PYTHON%" "aergia_dashboard.py"
exit
