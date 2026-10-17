@echo off
setlocal
set "PY=python.exe"
set "ROOT=C:\Users\z143d\Desktop\Aergia_Studio"

cd /d "%ROOT%" || (echo ROOT missing & pause & exit /b 1)

"%PY%" -c "import os; import glob; root=r'%ROOT%'; patterns=['**/midas_home.py','**/hyperion_director.py','**/hyperion_gui.py','**/project-chimera/**/app.py','**/project-chimera/**/worker.py']; print('ROOT:',root); print(); [print(p, '=>', (glob.glob(os.path.join(root,p), recursive=True)[:10] or ['NOT FOUND'])[0]) for p in patterns]"
REM Removed pause to allow automated capture, output is captured via run_command
endlocal
