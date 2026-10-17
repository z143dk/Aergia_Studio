import os
import subprocess
import sys

def reset_shortcut_to_studio():
    desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
    name = "Project Aergia OS"
    link_path = os.path.join(desktop, name + ".lnk")
    
    base_dir = r"C:\Users\z143d\Desktop\Aergia_Studio"
    target_script = "launch_studio.bat"
    target_path = os.path.join(base_dir, target_script)
    
    icon_path = os.path.join(base_dir, "Project Aergia OS", "system_icon.ico")
    if not os.path.exists(icon_path):
        icon_path = os.path.join(base_dir, "assets", "aergia_icon.ico")
    
    print(f"Resetting Shortcut: {link_path}")
    print(f"Target: {target_path} (Studio Launcher)")

    ps_script = f"""
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut('{link_path}')
    $Shortcut.TargetPath = '{target_path}'
    $Shortcut.WorkingDirectory = '{base_dir}'
    $Shortcut.Description = 'Project Aergia OS - Studio'
    """
    
    if os.path.exists(icon_path):
        ps_script += f"\n$Shortcut.IconLocation = '{icon_path}'"
    
    ps_script += "\n$Shortcut.Save()"
    
    try:
        subprocess.run(["powershell", "-Command", ps_script], check=True)
        print("SUCCESS: Shortcut reset to launch_studio.bat")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    reset_shortcut_to_studio()
