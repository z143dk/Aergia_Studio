import os
import sys
import subprocess

# Configuration
PROJECT_DIR = r"C:\Users\z143d\Desktop\Aergia_Studio"
TARGET_BATCH = os.path.join(PROJECT_DIR, "Launch_Aergia_Suite.bat")
ICON_PATH = os.path.join(PROJECT_DIR, "assets", "aergia_icon.ico")
SHORTCUT_NAME = "Project Aergia OS.lnk"

def get_desktop_path():
    """
    Returns the Project Directory so the user can find the shortcut 'here'.
    """
    return PROJECT_DIR

def create_shortcut():
    desktop = get_desktop_path()
    shortcut_path = os.path.join(desktop, SHORTCUT_NAME)
    
    print(f"Creating shortcut at: {shortcut_path}")
    print(f"Targeting: {TARGET_BATCH}")
    print(f"Icon: {ICON_PATH}")

    # Use PowerShell directly, no external Python deps required
    try:
        print("Creating shortcut via PowerShell...")
        ps_script = f"""
        $WshShell = New-Object -comObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut('{shortcut_path}')
        $Shortcut.TargetPath = 'C:\Windows\System32\cmd.exe'
        $Shortcut.Arguments = '/k "{TARGET_BATCH}"'
        $Shortcut.WorkingDirectory = '{PROJECT_DIR}'
        $Shortcut.IconLocation = '{ICON_PATH}'
        $Shortcut.Description = 'Launch Aergia OS Suite'
        $Shortcut.Save()
        """
        subprocess.run(["powershell", "-Command", ps_script], check=True)
        print("✅ Shortcut created successfully!")
    except Exception as e:
        print(f"❌ Failed to create shortcut: {e}")

if __name__ == "__main__":
    if not os.path.exists(ICON_PATH):
        print(f"⚠️ Warning: Icon file not found at {ICON_PATH}")
    
    create_shortcut()
