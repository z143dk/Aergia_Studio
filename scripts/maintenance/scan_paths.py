import os
import glob
root = r"C:\Users\z143d\Desktop\Aergia_Studio"
patterns = [
    "**/midas_home.py",
    "**/hyperion_director.py",
    "**/hyperion_gui.py",
    "**/project-chimera/**/app.py",
    "**/project-chimera/**/worker.py"
]
print(f"ROOT: {root}\n")
for p in patterns:
    matches = glob.glob(os.path.join(root, p), recursive=True)
    found = matches[0] if matches else "NOT FOUND"
    print(f"{p} => {found}")
