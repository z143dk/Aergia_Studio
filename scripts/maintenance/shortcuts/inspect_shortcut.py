import os
import subprocess

def inspect():
    # Check the one we just made in the current directory
    link_path = os.path.abspath("Project Aergia OS.lnk")
    
    ps_cmd = f"""
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut('{link_path}')
    Write-Output "Shortcut: {link_path}"
    Write-Output "Target: $($Shortcut.TargetPath)"
    Write-Output "Args:   $($Shortcut.Arguments)"
    Write-Output "WorkDir: $($Shortcut.WorkingDirectory)"
    """
    
    try:
        subprocess.run(["powershell", "-Command", ps_cmd], check=True)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect()
