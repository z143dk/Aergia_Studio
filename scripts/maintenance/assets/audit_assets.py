
import os

target_dir = r"C:\Users\z143d\Desktop\Aergia_Studio"
skip_dirs = ["node_modules", "__pycache__", ".git"]
found_files = []

print(f"Scanning {target_dir} for visual assets (.png)...")

for root, dirs, files in os.walk(target_dir):
    # Filter skipped directories
    dirs[:] = [d for d in dirs if d not in skip_dirs]
    
    for file in files:
        if file.lower().endswith(".png"):
            found_files.append(os.path.join(root, file))

# Sort and print
found_files.sort()
print(f"\nFound {len(found_files)} PNG files:")
for f in found_files:
    print(f"{os.path.basename(f)}  ->  {os.path.dirname(f)}")
