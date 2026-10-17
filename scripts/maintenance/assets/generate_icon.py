import fal_client
import requests
import os
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

def generate_aergia_icon():
    print("Generating Premium Icon for Project Aergia using FAL AI...")
    
    try:
        # 1. Generate Image
        handler = fal_client.submit(
            "fal-ai/flux/schnell",
            arguments={
                "prompt": "A futuristic hexagonal logo for an AI Operating System called AERGIA, glowing cyan and neon green circuitry, centered, minimal, 8k resolution, black background, high tech style",
                "image_size": "square_hd"
            },
        )
        result = handler.get()
        
        if result and 'images' in result and len(result['images']) > 0:
            image_url = result['images'][0]['url']
            print(f"Icon valid. Downloading from {image_url}...")
            
            # 2. Download
            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                # Save Raw
                base_dir = r"C:\Users\z143d\Desktop\Aergia_Studio\Project Aergia OS"
                os.makedirs(base_dir, exist_ok=True)
                raw_path = os.path.join(base_dir, "generated_icon.png")
                
                with open(raw_path, "wb") as f:
                    f.write(img_response.content)
                
                # 3. Convert to ICO
                print("Converting to ICO...")
                img = Image.open(raw_path)
                ico_path = os.path.join(base_dir, "system_icon.ico")
                img.save(ico_path, format='ICO', sizes=[(256, 256)])
                
                print(f"SUCCESS: Icon saved to {ico_path}")
            else:
                print("Failed to download image.")
        else:
            print("FAL returned no images.")
            
    except Exception as e:
        print(f"Error generating icon: {e}")

if __name__ == "__main__":
    generate_aergia_icon()
