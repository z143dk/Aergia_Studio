@echo off
echo ===================================================
echo PREPARING AERGIA STUDIO FOR TRANSFER
echo ===================================================
echo.
echo 1. Removing Windows Python Cache (__pycache__)...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

echo 2. Removing Mac System Files (.DS_Store)...
del /s /q .DS_Store 2>nul

echo.
echo ===================================================
echo READY FOR TRANSFER
echo ===================================================
echo You can now safely copy this entire folder to your Flash Drive.
echo.
pause
