
from PIL import Image
import os

source_path = "C:/Users/z143d/.gemini/antigravity/brain/5f9a6fa5-24c0-4b30-9355-f7361acc46a3/uploaded_image_1766527826110.jpg"
target_path = "midas.ico"

try:
    img = Image.open(source_path)
    # Resize to standard icon sizes
    img.save(target_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print(f"Successfully created {os.path.abspath(target_path)}")
except Exception as e:
    print(f"Error creating icon: {e}")
