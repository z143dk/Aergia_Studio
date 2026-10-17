@echo off
TITLE Launch Aergia Orchestrator
echo Starting Aergia OS Orchestrator Control Center...
cd /d "C:\Users\z143d\Desktop\Aergia_Studio"
"C:\Users\z143d\AppData\Local\Programs\Python\Python312\python.exe" "aergia_orchestrator_gui.py"
if %errorlevel% neq 0 pause
