@echo off
set "PY=python.exe"
set "APP=C:\Users\z143d\Desktop\Aergia_Studio\Project Chimera\project-chimera\backend-flask\app.py"
set "CWD=C:\Users\z143d\Desktop\Aergia_Studio\Project Chimera\project-chimera\backend-flask"

cd /d "%CWD%"
"%PY%" "%APP%" > chimera_debug.log 2>&1

if %errorlevel% neq 0 (
    echo Launch failed.
    type chimera_debug.log
) else (
    echo Launch success (but it should be a server so this might not return immediately).
)
