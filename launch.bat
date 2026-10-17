@echo off
setlocal
cd /d "%~dp0"
set PYTHON_EXE=python
if exist "C:\Users\z143d\AppData\Local\Programs\Python\Python312\python.exe" (
    set "PYTHON_EXE=C:\Users\z143d\AppData\Local\Programs\Python\Python312\python.exe"
)
"%PYTHON_EXE%" "scripts\launch.py" %*
if %ERRORLEVEL% neq 0 (
    echo.
    pause
)
