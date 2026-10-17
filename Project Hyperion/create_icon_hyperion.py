
from PIL import Image
import os

source_path = "C:/Users/z143d/.gemini/antigravity/brain/95053e2f-e5d2-4fe9-9778-d6b19b268f2e/uploaded_image_1766464581757.jpg"
target_path = "hyperion.ico"

try:
    img = Image.open(source_path)
    # Resize to standard icon sizes
    img.save(target_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print(f"Successfully created {os.path.abspath(target_path)}")
except Exception as e:
    print(f"Error creating icon: {e}")
