import os
import shutil
import sys
from datetime import datetime

def get_drives():
    drives = []
    bitmask = os.popen('wmic logicaldisk get caption').read()
    for line in bitmask.split('\n'):
        if ':' in line:
            drives.append(line.strip())
    # remove C: as it is likely the OS drive
    return [d for d in drives if d != 'C:']

def create_portable_launcher(drive_root):
    launcher_content = r"""@echo off
setlocal

:: --- Portable Aergia Studio Launcher ---
:: This script sets up a self-contained environment for Aergia.
:: It redirects all temporary files to this drive to leave no trace.

:: 1. Set Root Directory
set "STUDIO_ROOT=%~dp0"
cd /d "%STUDIO_ROOT%"

:: 2. Set Portable Python Path (User must place WinPython here)
:: We look for a folder starting with "python-" or just "Python"
if exist "Python\python.exe" (
    set "PYTHON_EXE=Python\python.exe"
) else (
    echo [ERROR] Portable Python not found!
    echo Please download WinPython or a standard Python embeddable package
    echo and place it in a folder named 'Python' on this drive.
    pause
    exit /b 1
)

:: 3. Configure Trace/Temp isolation
if not exist "tmp" mkdir "tmp"
set "TMP=%STUDIO_ROOT%tmp"
set "TEMP=%STUDIO_ROOT%tmp"

:: 4. Launch Dashboard
echo [AERGIA] Launching Portable Studio...
echo [INFO]  Temp Directory: %TEMP%
echo [INFO]  Python: %PYTHON_EXE%

"%PYTHON_EXE%" "Aergia_Studio\aergia_dashboard.py"

if %errorlevel% neq 0 (
    echo [ERROR] Dashboard crashed or failed to launch.
    pause
)
"""
    launcher_path = os.path.join(drive_root, "Launch_Aergia_Portable.bat")
    with open(launcher_path, 'w') as f:
        f.write(launcher_content)
    print(f"[SUCCESS] Created portable launcher (Windows): {launcher_path}")

def create_portable_web_launcher(drive_root):
    launcher_content = r"""@echo off
setlocal

:: --- Portable Aergia Web Dashboard (iPad/Remote Ready) ---

:: 1. Set Root Directory
set "STUDIO_ROOT=%~dp0"
cd /d "%STUDIO_ROOT%"

:: 2. Find Python
if exist "Python\python.exe" (
    set "PYTHON_EXE=Python\python.exe"
) else (
    echo [ERROR] Portable Python not found!
    exit /b 1
)

:: 3. Configure Temp
if not exist "tmp" mkdir "tmp"
set "TMP=%STUDIO_ROOT%tmp"
set "TEMP=%STUDIO_ROOT%tmp"

:: 4. Launch Web Server
echo [AERGIA] Launching Portable Web Dashboard...
echo [INFO]  Server will run at 0.0.0.0 (Accessible via LAN)
echo [INFO]  To control from iPad, connect to this WiFi and go to:
echo [INFO]  http://[YOUR_PC_IP_ADDRESS]:5000
echo.
echo [INFO]  Opening local browser...
start "" "http://127.0.0.1:5000"

"%PYTHON_EXE%" "Aergia_Studio\aergia_api.py"

pause
"""
    launcher_path = os.path.join(drive_root, "Launch_Portable_Web.bat")
    with open(launcher_path, 'w') as f:
        f.write(launcher_content)
    print(f"[SUCCESS] Created portable Web launcher: {launcher_path}")

def create_mac_launcher(drive_root):
    launcher_content = r"""#!/bin/bash
# --- Portable Aergia Studio Launcher (macOS/Linux) ---

# 1. Set Root Directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# 2. Python Detection
# macOS doesn't support 'Portable Python' .exe files. 
# We try to use the system python3 or a local venv if present.

if [ -f "bin/python3" ]; then
    PYTHON_EXE="bin/python3"  # If user created a portable unix env
elif command -v python3 &> /dev/null; then
    PYTHON_EXE="python3"
else
    echo "[ERROR] Python 3 not found on this system."
    echo "Please install Python 3.10+ (brew install python3)"
    read -p "Press enter to exit"
    exit 1
fi

# 3. Configure Temp
export TMPDIR="$DIR/tmp"
mkdir -p "$TMPDIR"

# 4. Launch
echo "[AERGIA] Launching Portable Studio on macOS..."
echo "[INFO] Using Python: $PYTHON_EXE"

"$PYTHON_EXE" "Aergia_Studio/aergia_dashboard.py"

if [ $? -ne 0 ]; then
    echo "[ERROR] Launch failed. check terminal output."
    echo "You may need to run: pip3 install -r Aergia_Studio/requirements.txt"
    read -p "Press enter to exit"
fi
"""
    launcher_path = os.path.join(drive_root, "Launch_Aergia_Mac.command")
    with open(launcher_path, 'w') as f:
        f.write(launcher_content)
    
    # Make it executable (best effort, though file system might ignore on FAT32)
    try:
        os.chmod(launcher_path, 0o755)
    except:
        pass
        
    print(f"[SUCCESS] Created portable launcher (Mac/Linux): {launcher_path}")

def clone_studio(source_dir, dest_drive):
    fn = "Aergia_Studio"
    dest_dir = os.path.join(dest_drive, fn)
    
    print(f"--- Cloning Aergia Studio ---")
    print(f"Source: {source_dir}")
    print(f"Target: {dest_dir}")
    print("-----------------------------")

    if os.path.exists(dest_dir):
        print("[INFO] Target directory exists. Updating files...")
    else:
        print("[INFO] Creating target directory...")

    # Define what to ignore
    ignore_func = shutil.ignore_patterns(
        '__pycache__', 
        '*.pyc', 
        '.git', 
        '.venv', 
        'venv', 
        'debug_output*.txt',
        '*.tmp'
    )

    try:
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir) # Clean copy to be safe/simple for now
        
        shutil.copytree(source_dir, dest_dir, ignore=ignore_func)
        print(f"[SUCCESS] Copied files to {dest_dir}")
        
        # Create Brainstorm Import Folder (For iPad usage)
        inbox_path = os.path.join(dest_drive, "_BRAINSTORM_INBOX")
        if not os.path.exists(inbox_path):
            os.makedirs(inbox_path)
            # Add a readme
            with open(os.path.join(inbox_path, "READ_ME_IPAD.txt"), "w") as f:
                f.write("SAVE YOUR NOTES HERE FROM IPAD.\n")
                f.write("Aergia will read them when you connect to a PC.")
        
        create_portable_launcher(dest_drive)
        create_mac_launcher(dest_drive)
        create_portable_web_launcher(dest_drive)
        
        print("\n[NEXT STEPS]")
        print("1. WINDOWS (Desktop App): Run 'Launch_Aergia_Portable.bat'")
        print("2. WINDOWS (iPad Control): Run 'Launch_Portable_Web.bat'")
        print("3. Mac/Linux:             Run 'Launch_Aergia_Mac.command'")
        print("   (Uses system python3, may need 'pip install -r requirements.txt')")
        
    except Exception as e:
        print(f"[ERROR] Copy failed: {e}")

if __name__ == "__main__":
    print("--- Aergia Generic Cloner ---")
    
    # 1. Detect Source (Current Directory)
    source_path = os.getcwd()
    if not os.path.exists(os.path.join(source_path, "aergia_dashboard.py")):
        # Fallback if not run from root
        potential_path = r"C:\Users\z143d\Desktop\Aergia_Studio"
        if os.path.exists(potential_path):
            source_path = potential_path
        else:
            print("[ERROR] Could not determine Aergia Studio root.")
            sys.exit(1)

    # Check for arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--drive", help="Target drive letter (e.g. D:)")
    args = parser.parse_args()

    if args.drive:
        target_drive = args.drive
        if not target_drive.endswith(":") and len(target_drive) == 1:
             target_drive += ":"
        if not target_drive.endswith(os.sep):
            target_drive += os.sep
        
        print(f"[AUTO] Cloning to {target_drive}")
        clone_studio(source_path, target_drive)
        sys.exit(0)
            
    # 2. Detect Destination (Interactive)
    drives = get_drives()
    if not drives:
        print("[ERROR] No external drives found! Please plug in your MagHub.")
        sys.exit(1)
        
    print("Available Drives:")
    for i, d in enumerate(drives):
        print(f"[{i}] {d}")
        
    choice = input("Select drive index (e.g. 0): ")
    try:
        idx = int(choice)
        target_drive = drives[idx]
        target_drive = target_drive + os.sep # Ensure it ends with slash
        
        clone_studio(source_path, target_drive)
        
    except (ValueError, IndexError):
        print("[ERROR] Invalid selection.")
