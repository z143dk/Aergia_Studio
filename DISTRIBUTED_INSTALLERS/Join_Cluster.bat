@echo off
TITLE Connect to Aergia Exo Cluster
COLOR 0A
CLS

ECHO ==================================================
ECHO    CONNECTING TO EXCO CLUSTER
ECHO ==================================================
ECHO.
ECHO NOTE: Exo requires Linux or macOS.
ECHO On Windows, you MUST run this within WSL (Windows Subsystem for Linux),
ECHO or Python 3.12+ environment if supported.
ECHO.
ECHO The Mac Studio (daniels-macbook-pro) is configured to automatically 
ECHO discover this machine via Tailscale IP: 100.111.220.42 (or 100.88.136.43)
ECHO.
ECHO Please ensure 'exo' is installed and run:
ECHO.
ECHO   uv run exo
ECHO   (or python3 -m exo)
ECHO.
ECHO Press any key to attempt running 'exo' directly...
PAUSE

exo
PAUSE
