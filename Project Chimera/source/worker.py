import os
import sys
import logging
import sqlite3
import time
from datetime import datetime
from dotenv import load_dotenv
# from google.cloud import texttospeech
# import vertexai
# from vertexai.preview.generative_models import GenerativeModel
import fal_client
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips
import requests

# Add Aergia Studio Root to Path
current_dir = os.path.dirname(os.path.abspath(__file__))
aergia_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
if aergia_root not in sys.path:
    sys.path.append(aergia_root)

from intelligence_router import router, TaskType

# --- App Initialization ---
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(funcName)s] %(message)s',
    handlers=[
        logging.FileHandler("chimera_worker.log"),
        logging.StreamHandler()
    ]
)

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "chimera.db")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")

# Ensure directories exist
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize Clients
tts_client = None

def initialize_worker():
    """Initializes AI clients."""
    global tts_client
    if tts_client:
        return

    logging.info("Initializing Worker service...")
    try:
        # if not PROJECT_ID:
        #    logging.warning("GOOGLE_CLOUD_PROJECT not set. Vertex AI features (Image Generation) will be unavailable.")
        # else:
        #    # Init clients
        #    pass
        
        logging.info("Worker config: Using EdgeTTS (Audio) and Pollinations.ai (Video). No Google Cloud Billing required.")
            
        # Initialize SQLite DB if needed
        init_db()

        logging.info("Worker clients and database initialized successfully.")

    except Exception as e:
        logging.error(f"Worker Initialization Warning: {e}")
        # raise # Don't crash, allow limited functionality

def init_db():
    """Creates the SQLite table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS storyboards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT DEFAULT 'pending',
            video_path TEXT,
            error_message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scenes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            storyboard_id INTEGER,
            scene_number INTEGER,
            script TEXT,
            prompt TEXT,
            FOREIGN KEY(storyboard_id) REFERENCES storyboards(id)
        )
    ''')
    conn.commit()
    conn.close()

    conn.commit()
    conn.close()

def Image_Generation_via_router(prompt, image_size="landscape_16_9"):
    """
    Replaces direct fal_client calls. 
    Uses the Aergia Orchestrator to handle generation and fallbacks.
    """
    logging.info(f"🎨 Orchestrating image generation for: {prompt[:50]}...")
    
    try:
        # The router now handles the FAL logic, API keys, and error catching
        image_url = router.generate(
            prompt=prompt,
            task_type=TaskType.IMAGE_GEN,
            image_size=image_size # Passed into the FAL provider via kwargs
        )
        return image_url
    except Exception as e:
        logging.error(f"❌ Router Image Gen Failed: {e}")
        # Fallback to a placeholder or a secondary method if desired
        return None

def Video_Generation_via_router(prompt, image_url=None):
    """
    Generates dynamic video using FAL.ai via Intelligence Router (e.g. Minimax or Kling).
    """
    logging.info(f"🎥 Orchestrating video generation for: {prompt[:50]}...")
    
    try:
        kwargs = {}
        if image_url:
            kwargs["image_url"] = image_url
            
        video_url = router.generate(
            prompt=prompt,
            task_type=TaskType.VIDEO_GEN,
            **kwargs
        )
        return video_url
    except Exception as e:
        logging.error(f"❌ Router Video Gen Failed: {e}")
        return None

def process_task(storyboard_id):
    """Processes a video generation task for a given storyboard ID."""
    logging.info(f"Job {storyboard_id}: Processing started.")
    
    final_video_filename = f"storyboard_{storyboard_id}.mp4"
    final_video_path = os.path.join(OUTPUT_DIR, final_video_filename)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    temp_files = []

    try:
        # Update status
        cursor.execute("UPDATE storyboards SET status = 'processing' WHERE id = ?", (storyboard_id,))
        conn.commit()

        # Fetch ALL scenes
        cursor.execute("SELECT scene_number, script, prompt FROM scenes WHERE storyboard_id = ? ORDER BY scene_number", (storyboard_id,))
        scenes = cursor.fetchall()
        
        if not scenes:
            raise Exception(f"No scenes found for storyboard_id {storyboard_id}")
        
        logging.info(f"Job {storyboard_id}: Found {len(scenes)} scenes.")
        
        video_clips = []

        for scene in scenes:
            scene_num, script_text, video_prompt = scene
            logging.info(f"Job {storyboard_id}: Processing Scene {scene_num}...")

            scene_audio_path = f"temp_{storyboard_id}_scene_{scene_num}.mp3"
            scene_image_path = f"temp_{storyboard_id}_scene_{scene_num}.png"
            temp_files.extend([scene_audio_path, scene_image_path])

            # 2. Text Substitution (Time/Date)
            current_time = datetime.now().strftime("%I:%M %p")
            current_date = datetime.now().strftime("%B %d, %Y")
            script_text = script_text.replace("{{TIME}}", current_time).replace("{{DATE}}", current_date)
            logging.info(f"  - Final Script: {script_text}")

            # 3. Generate Audio (Edge TTS - Free)
            logging.info(f"  - Generating audio (Edge TTS)...")
            
            # Escape text for CLI (basic)
            safe_text = script_text.replace('"', '\\"').replace('\n', ' ')
            voice_name = "en-US-ChristopherNeural" # High quality male voice
            
            scene_vtt_path = f"temp_{storyboard_id}_scene_{scene_num}.vtt"
            temp_files.append(scene_vtt_path)

            # Run edge-tts via CLI to avoid async compatibility headeraches in this sync worker
            # Command: edge-tts --text "Hello" --write-media output.mp3 --write-subtitles output.vtt --voice en-US-ChristopherNeural
            cmd = f'edge-tts --text "{safe_text}" --write-media "{scene_audio_path}" --write-subtitles "{scene_vtt_path}" --voice {voice_name}'
            
            import subprocess
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"Edge TTS failed: {result.stderr}")
            
            if not os.path.exists(scene_audio_path):
                 raise Exception("Edge TTS did not produce an audio file.")

            
            # 4. Generate Video (Fal.ai - Minimax/Kling)
            if video_prompt.startswith("RESOURCE:"):
                # ... resource handling remains same ...
                resource_filename = video_prompt.split("RESOURCE:")[1].strip()
                resource_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", resource_filename)
                logging.info(f"  - Using local resource: {resource_path}")
                if not os.path.exists(resource_path):
                     raise FileNotFoundError(f"Resource file not found: {resource_path}")
                final_video_source = resource_path
            else:
                logging.info(f"  - Generating VIDEO with prompt: '{video_prompt}'")
                
                # Check for Key
                if not os.getenv("FAL_KEY"):
                    raise Exception("FAL_KEY not found in .env! Cannot generate video.")

                # Router Video Generation (Minimax via Intelligence Router)
                # Appending stylistic keywords for Faceless Shorts
                enhanced_prompt = f"{video_prompt}, cinematic, 9:16 aspect ratio, high quality, 4k"
                video_url = Video_Generation_via_router(enhanced_prompt)
                
                if not video_url:
                     raise Exception("Failed to generate video via Router.")

                logging.info(f"    - Video Generated: {video_url}")
                
                # Download Video (use scene_image_path but make it .mp4)
                scene_video_path = f"temp_{storyboard_id}_scene_{scene_num}.mp4"
                temp_files.append(scene_video_path)
                
                response = requests.get(video_url)
                with open(scene_video_path, "wb") as f:
                    f.write(response.content)
                    
                final_video_source = scene_video_path

            # 5. Create Clip
            logging.info(f"  - Creating clip...")
            audioclip = AudioFileClip(scene_audio_path)
            
            # Load Video 
            video_clip_raw = VideoFileClip(final_video_source)
            
            # Loop or trim video to match audio length
            if video_clip_raw.duration < audioclip.duration:
                # Loop if too short
                n_loops = int(audioclip.duration / video_clip_raw.duration) + 1
                video_clip = video_clip_raw.loop(n=n_loops)
            else:
                video_clip = video_clip_raw
                
            # Set duration explicitly to audio length
            video_clip = video_clip.with_duration(audioclip.duration)
            
            # Replace audio with our narrative TTS
            video_clip = video_clip.with_audio(audioclip)
                
            video_clips.append(video_clip)

        # 4. Concatenate All Clips
        logging.info(f"Job {storyboard_id}: Concatenating {len(video_clips)} clips...")
        final_clip = concatenate_videoclips(video_clips, method="compose")
        
        final_clip.write_videofile(final_video_path, codec='libx264', audio_codec='aac', fps=24, logger=None)

        # Update status to complete
        cursor.execute("UPDATE storyboards SET status = 'complete', video_url = ? WHERE id = ?", (final_video_path, storyboard_id))
        conn.commit()

        logging.info(f"SUCCESS: Job {storyboard_id} finished. Video saved to: {final_video_path}")

    except Exception as e:
        logging.error(f"FAILURE: Error processing job {storyboard_id}: {e}", exc_info=True)
        cursor.execute("UPDATE storyboards SET status = 'failed', error_message = ? WHERE id = ?", (str(e), storyboard_id))
        conn.commit()

    finally:
        conn.close()
        # Cleanup temp files
        time.sleep(2) # Give OS time to release file handles (Fix WinError 32)
        for f in temp_files:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except OSError as e:
                    logging.warning(f"Job {storyboard_id}: Could not remove temp file {f}: {e}")

def main():
    initialize_worker()
    
    # Simple polling loop for demonstration
    logging.info("Worker started. Polling for pending jobs...")
    while True:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM storyboards WHERE status = 'pending' LIMIT 1")
            row = cursor.fetchone()
            conn.close()

            if row:
                process_task(row[0])
            else:
                time.sleep(5) # Wait before checking again
        except KeyboardInterrupt:
            logging.info("Worker stopped by user.")
            break
        except Exception as e:
            logging.error(f"Error in polling loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()