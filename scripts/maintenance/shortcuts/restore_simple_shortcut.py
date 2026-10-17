import os
import subprocess
import sys

def restore_shortcut_ps():
    desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
    name = "Project Aergia OS"
    link_path = os.path.join(desktop, name + ".lnk")
    
    base_dir = r"C:\Users\z143d\Desktop\Aergia_Studio"
    target_script = "aergia_dashboard.py"
    target_path = os.path.join(base_dir, target_script)
    
    # Python executable (windowless)
    python_exe = r"C:\Users\z143d\AppData\Local\Programs\Python\Python312\pythonw.exe"
    
    icon_path = os.path.join(base_dir, "assets", "aergia_icon.ico")
    
    print(f"Targeting: {link_path}")
    print(f"Script: {target_path}")

    ps_script = f"""
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut('{link_path}')
    $Shortcut.TargetPath = '{python_exe}'
    $Shortcut.Arguments = '"{target_path}"'
    $Shortcut.WorkingDirectory = '{base_dir}'
    $Shortcut.Description = 'Aergia Pantheon - App Family'
    """
    
    if os.path.exists(icon_path):
        ps_script += f"\n$Shortcut.IconLocation = '{icon_path}'"
    
    ps_script += "\n$Shortcut.Save()"
    
    try:
        subprocess.run(["powershell", "-Command", ps_script], check=True)
        print("SUCCESS: Shortcut restored via PowerShell.")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    restore_shortcut_ps()
