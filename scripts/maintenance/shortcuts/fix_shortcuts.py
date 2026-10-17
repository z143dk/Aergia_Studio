import os
import sys
import win32com.client

def create_shortcut(name, target, working_dir, arguments="", icon_path=None):
    desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
    path = os.path.join(desktop, name + ".lnk")
    
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(path)
    shortcut.TargetPath = target
    shortcut.WorkingDirectory = working_dir
    shortcut.Arguments = arguments
    if icon_path and os.path.exists(icon_path):
        shortcut.IconLocation = icon_path
    
    shortcut.Save()
    print(f"Created shortcut: {path} -> {target}")

def main():
    base_dir = r"C:\Users\z143d\Desktop\Aergia_Studio"
    python_exe = r"C:\Users\z143d\AppData\Local\Programs\Python\Python312\pythonw.exe"
    
    # 1. Project Aergia OS (Launch Studio Loop)
    create_shortcut(
        "Project Aergia OS",
        os.path.join(base_dir, "launch_studio.bat"),
        base_dir,
        icon_path=os.path.join(base_dir, "Project Aergia OS", "system_icon.ico") 
    )

    # 2. Hyperion (Direct Link)
    hyperion_script = os.path.join(base_dir, "Project Hyperion", "hyperion_gui.py")
    create_shortcut(
        "Hyperion",
        python_exe,
        base_dir,
        arguments=f'"{hyperion_script}"',
        icon_path=os.path.join(base_dir, "Project Hyperion", "hyperion.ico")
    )

    # 3. Antigravity Studio (Open Codebase)
    vscode_exe = r"C:\Users\z143d\AppData\Local\Programs\Microsoft VS Code\Code.exe"
    if os.path.exists(vscode_exe):
        create_shortcut(
            "Antigravity Studio",
            vscode_exe,
            base_dir,
            arguments=f'"{base_dir}"',
            icon_path=os.path.join(base_dir, "Project Aergia OS", "system_icon.ico")
        )

    print("Shortcuts updated successfully.")

if __name__ == "__main__":
    main()
