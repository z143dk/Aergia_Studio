import shutil
import os

# Use absolute paths based on where we know the project is
base_dir = "/Users/macbookprom213/Desktop/Aergia_Studio"
src = os.path.join(base_dir, "assets", "intro")
dst = os.path.join(base_dir, "Aergia_Web", "static", "assets", "intro")

print(f"Copying from {src} to {dst}")
if os.path.exists(src):
    shutil.copytree(src, dst, dirs_exist_ok=True)
    print("Done")
else:
    print(f"Source not found: {src}")
