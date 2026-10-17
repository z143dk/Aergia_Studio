import os
import json
import win32com.client

path = r"C:\Users\z143d\Desktop\Aergia_Studio\Project Aergia OS.lnk"
info = {}

try:
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(path)
    info = {
        "Target": shortcut.TargetPath,
        "WorkingDir": shortcut.WorkingDirectory,
        "Arguments": shortcut.Arguments,
        "IconLocation": shortcut.IconLocation
    }
except Exception as e:
    info = {"Error": str(e)}

with open("shortcut_info.json", "w", encoding="utf-8") as f:
    json.dump(info, f, indent=2)
