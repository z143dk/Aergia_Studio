@echo off
TITLE Launch Aergia Pantheon
echo Starting Aergia Dashboard...
cd /d "C:\Users\z143d\Desktop\Aergia_Studio"
"C:\Users\z143d\AppData\Local\Programs\Python\Python312\python.exe" "aergia_dashboard.py"
if %errorlevel% neq 0 pause
