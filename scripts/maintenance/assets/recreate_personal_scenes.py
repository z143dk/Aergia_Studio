import os
import fal_client
import time
import requests # Move to top to fail fast if missing
from dotenv import load_dotenv
import sys

# Setup logging to file
log_file = open("recreation_debug.txt", "w", encoding="utf-8")
def log(msg):
    print(msg)
    log_file.write(msg + "\n")
    log_file.flush()

# Load environment variables (for FAL_KEY)
load_dotenv()
load_dotenv(".env.local")

# Configuration
# Using uploaded_image_3 which appears to be the clear User close-up based on context
USER_IMAGE_PATH = r"C:/Users/z143d/.gemini/antigravity/brain/29aac132-a7d6-41af-8371-84ba4e2af6f0/uploaded_image_3_1768536324030.jpg"
OUTPUT_DIR = r"C:\Users\z143d\Desktop\Aergia_Studio\assets\clips"
# fallback to Minimax which is verified working
MODEL_ID = "fal-ai/minimax-video" 

SCENES = [
    {
        "name": "meet_girlfriend",
        "filename": "recreated_scene_1_meet_girlfriend.mp4",
        "prompt": "A cinematic shot of a Welsh/Spaniard man (reference image) meeting his Vietnamese girlfriend on a busy street in Asia. She has long dark hair and a warm smile. Emotional, romantic meeting, 8k resolution, photorealistic."
    },
    {
        "name": "sit_daughter",
        "filename": "recreated_scene_2_sit_daughter.mp4",
        "prompt": "A cinematic shot of a Welsh/Spaniard man (reference image) sitting in a comfortable living room in Virginia talking with his mixed-race (Hmong/Laos/European) daughter. She has unique features reflecting her heritage. Warm lighting, home atmosphere, 8k."
    },
    {
        "name": "ancient_mysticism",
        "filename": "recreated_scene_3_ancient_mysticism.mp4",
        "prompt": "A cinematic shot of a Welsh/Spaniard man (reference image) standing in a mysterious ancient temple, surrounded by glowing mystical symbols and ethereal blue and gold lighting. Magical atmosphere, blockbuster movie style, 8k."
    }
]

def generate_scenes():
    log("🎬 Starting Video Regeneration Task...")
    
    if not os.getenv("FAL_KEY"):
        log("❌ Error: FAL_KEY not found in environment.")
        return

    if not os.path.exists(USER_IMAGE_PATH):
        log(f"❌ Error: User image not found at {USER_IMAGE_PATH}")
        return

    # 1. Upload Image
    log(f"📤 Uploading reference image: {USER_IMAGE_PATH}...")
    try:
        image_url = fal_client.upload_file(USER_IMAGE_PATH)
        log(f"✅ Image uploaded: {image_url}")
    except Exception as e:
        log(f"❌ Upload failed: {e}")
        import traceback
        log(traceback.format_exc())
        return

    # 2. Submit Jobs
    jobs = []
    log(f"🚀 Submitting {len(SCENES)} jobs to {MODEL_ID}...")
    
    for scene in SCENES:
        log(f"   - Submitting Scene: {scene['name']}...")
        try:
            handler = fal_client.submit(
                MODEL_ID,
                arguments={
                    "prompt": scene["prompt"],
                    "image_url": image_url,
                    "aspect_ratio": "16:9",
                    "duration": "5" 
                }
            )
            jobs.append({"scene": scene, "handler": handler})
        except Exception as e:
            log(f"   ❌ Failed to submit {scene['name']}: {e}")

    # 3. Wait for Results
    log("⏳ Waiting for generation results (this may take several minutes)...")
    
    for job in jobs:
        scene = job["scene"]
        handler = job["handler"]
        filename = scene["filename"]
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        log(f"   - Polling result for: {scene['name']}...")
        try:
            result = handler.get() # Blocks until done
            
            if result and 'video' in result and 'url' in result['video']:
                video_url = result['video']['url']
                log(f"     ✅ Generated! Downloading video...")
                
                # Download
                response = requests.get(video_url)
                if response.status_code == 200:
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    log(f"     💾 Saved to: {filepath}")
                else:
                    log(f"     ❌ Download failed: {response.status_code}")
            else:
                log(f"     ⚠️ Result format unexpected or empty: {result}")
                
        except Exception as e:
            log(f"     ❌ Error retrieving result for {scene['name']}: {e}")

    log("🏁 Regeneration Task Complete.")
    log_file.close()

if __name__ == "__main__":
    generate_scenes()
