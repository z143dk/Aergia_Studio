import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env or .env.local
load_dotenv()
load_dotenv(".env.local")

import logging
import sqlalchemy
from flask import Flask, request, jsonify
from gtts import gTTS
import vertexai
from vertexai.preview.generative_models import GenerativeModel
from vertexai.preview.vision_models import ImageGenerationModel
import requests # Added for Pollinations
import fal_client # Added for FAL AI
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, VideoFileClip
import moviepy.video.fx as vfx
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# --- App Initialization ---
app = Flask(__name__)
db_pool = None
tts_client = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(funcName)s] %(message)s')

def initialize_worker():
    """Initializes all clients and the database pool ONCE at startup."""
    global db_pool, tts_client
    if db_pool and tts_client:
        return

    logging.info("Initializing Worker service...")
    try:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        region = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")
        
        # Init clients
        # Note: Requires GOOGLE_APPLICATION_CREDENTIALS to be set
        # tts_client = texttospeech.TextToSpeechClient() # Removed for gTTS
        if project_id:
            vertexai.init(project=project_id, location=region)
        else:
            logging.warning("GOOGLE_CLOUD_PROJECT not set. Vertex AI might fail.")

        # Use local SQLite database
        # Use local SQLite database
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        db_path = os.path.join(base_dir, "data", "chimera.db")
        db_pool = sqlalchemy.create_engine(f"sqlite:///{db_path}")
        logging.info(f"Worker initialized. DB: {db_path}")
        
        # Ensure static videos directory exists
        os.makedirs("static/videos", exist_ok=True)

    except Exception as e:
        logging.critical(f"FATAL: Could not initialize Worker service: {e}", exc_info=True)
        raise

# Initialize everything when the application starts
initialize_worker()

@app.route('/', methods=['POST'])
def process_task():
    """Main endpoint to process a video generation task."""
    if db_pool is None:
        logging.error("Worker not initialized, database pool is unavailable.")
        return "Internal Server Error: Worker not initialized", 500

    data = request.get_json()
    if not data or "storyboard_id" not in data:
        logging.error("Received invalid task data: %s", data)
        return "Invalid task data", 400

    storyboard_id = data["storyboard_id"]
    logging.info(f"Job {storyboard_id}: Received job.")

    # Save final video to static/videos
    final_video_filename = f"storyboard_{storyboard_id}.mp4"
    final_video_path = os.path.join("static", "videos", final_video_filename)
    
    temp_files_to_cleanup = []

    try:
        with db_pool.connect() as conn:
            logging.info(f"Job {storyboard_id}: Setting status to 'processing'.")
            conn.execute(sqlalchemy.text("UPDATE storyboards SET status = 'processing' WHERE id = :id"), {"id": storyboard_id})
            conn.commit()

            # Fetch ALL scenes
            scenes = conn.execute(sqlalchemy.text("SELECT scene_number, script, prompt FROM scenes WHERE storyboard_id = :id ORDER BY scene_number"), {"id": storyboard_id}).fetchall()
            
            if not scenes:
                raise Exception(f"No scenes found for storyboard_id {storyboard_id}")
            
            video_clips = []

            for i, scene in enumerate(scenes):
                scene_num, script_text, video_prompt = scene
                logging.info(f"Job {storyboard_id} - Scene {scene_num}: Processing...")

                temp_audio_path = f"temp_audio_{storyboard_id}_{i}.mp3"
                temp_image_path = f"temp_image_{storyboard_id}_{i}.png"
                temp_files_to_cleanup.extend([temp_audio_path, temp_image_path])

                # --- Audio Generation ---
                if not script_text.strip():
                    script_text = " " # Silence/Empty
                
                eleven_api_key = os.environ.get("ELEVEN_LABS_API_KEY")
                
                try:
                    if eleven_api_key:
                        logging.info(f"Job {storyboard_id}: Using ElevenLabs for Scene {scene_num}")
                        client = ElevenLabs(api_key=eleven_api_key)
                        
                        # Generate audio using 'Rachel' (pre-made voice)
                        audio_generator = client.text_to_speech.convert(
                            voice_id="21m00Tcm4TlvDq8ikWAM",
                            optimize_streaming_latency="0",
                            output_format="mp3_44100_128",
                            text=script_text,
                            model_id="eleven_monolingual_v1",
                            voice_settings=VoiceSettings(
                                stability=0.5,
                                similarity_boost=0.75,
                                style=0.0,
                                use_speaker_boost=True,
                            ),
                        )
                        
                        with open(temp_audio_path, "wb") as f:
                            for chunk in audio_generator:
                                if chunk:
                                    f.write(chunk)
                    else:
                        raise Exception("ELEVEN_LABS_API_KEY not set")

                except Exception as audio_e:
                    logging.warning(f"Job {storyboard_id}: ElevenLabs usage failed ({audio_e}). Fallback to gTTS.")
                    tts = gTTS(text=script_text, lang='en')
                    tts.save(temp_audio_path)

                # --- Intelligence Router Integration ---
                try:
                    import sys
                    from pathlib import Path
                    # Insert root Aergia Studio path
                    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
                    
                    from intelligence_router import router, TaskType
                    
                    enhancement_prompt = f"Rewrite this video scene description to be more vivid, cinematic, and detailed for an AI image generator. Keep it under 40 words. Description: {video_prompt}"
                    
                    # Use Gemini Studio (Creative) via Router
                    response_text = router.generate(enhancement_prompt, task_type=TaskType.CREATIVE)
                    
                    if response_text and "Error" not in response_text:
                        video_prompt = response_text.strip()
                        logging.info(f"Router Enhanced Prompt: {video_prompt}")
                    else:
                        logging.warning(f"Router skipped enhancement: {response_text}")

                except ImportError:
                    logging.warning("Intelligence Router not found. Skipping prompt enhancement.")
                except Exception as e:
                    logging.warning(f"Router Enhancement failed: {e}")

                # --- Image Generation ---
                image_url = None # Track URL for Video Gen
                ai_provider = os.environ.get("AI_PROVIDER", "pollinations").lower()
                
                try:
                    if ai_provider == "vertex":
                        # Vertex AI
                        logging.info(f"Job {storyboard_id}: Using Vertex AI for Scene {scene_num}")
                        model = ImageGenerationModel.from_pretrained("imagegeneration@006")
                        images = model.generate_images(
                            prompt=video_prompt,
                            number_of_images=1,
                            aspect_ratio="16:9",
                            safety_filter_level="block_some",
                            person_generation="allow_adult"
                        )
                        if images: images[0].save(location=temp_image_path)
                        else: raise Exception("No image from Vertex AI")

                    elif ai_provider == "pollinations":
                        # Pollinations.ai
                        logging.info(f"Job {storyboard_id}: Using Pollinations for Scene {scene_num}")
                        encoded_prompt = requests.utils.quote(video_prompt)
                        pollinations_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&model=flux"
                        image_url = pollinations_url # Capture for Video Gen
                        response = requests.get(pollinations_url, timeout=120)
                        if response.status_code == 200:
                            with open(temp_image_path, "wb") as f: f.write(response.content)
                        else:
                            raise Exception(f"Pollinations API failed: {response.status_code}")

                    elif ai_provider == "fal":
                        # FAL AI (Flux Schnell) VIA ROUTER
                        logging.info(f"Job {storyboard_id}: Using FAL AI (Flux Schnell) via Router for Scene {scene_num}")
                        
                        # Use the router to handle provider selection and execution
                        try:
                            # task_type="image_gen" routes to FALProvider by default in Policy
                            image_url = router.generate(
                                prompt=video_prompt, 
                                task_type="image_gen",
                                # Optional: pass specific args if needed, e.g.
                                # image_size="landscape_16_9"
                            )
                            
                            if not image_url or not image_url.startswith("http"):
                                raise Exception(f"Router did not return a valid URL: {image_url}")

                            logging.info(f"Router returned image URL: {image_url}")
                            
                            img_response = requests.get(image_url)
                            if img_response.status_code == 200:
                                with open(temp_image_path, "wb") as f:
                                    f.write(img_response.content)
                            else:
                                raise Exception(f"Failed to download Router image: {img_response.status_code}")

                        except Exception as router_e:
                            raise Exception(f"Router Image Gen Failed: {router_e}")

                    else:
                        raise Exception("Placeholder requested")

                except Exception as ai_e:
                    logging.error(f"Job {storyboard_id} Scene {scene_num}: Gen failed: {ai_e}")
                    # Fallback Image
                    img = Image.new('RGB', (1024, 576), color = 'black')
                    d = ImageDraw.Draw(img)
                    try: font = ImageFont.truetype("DejaVuSans.ttf", 40)
                    except IOError: font = ImageFont.load_default()
                    d.text((50,250), f"Scene {scene_num}: {str(ai_e)[:50]}", fill=(255,255,255), font=font)
                    img.save(temp_image_path)

                # --- Audio Clip (Shared) ---
                audioclip = AudioFileClip(temp_audio_path)

                # --- Google Flow: AI Video Generation ---
                final_scene_clip = None
                
                # Try to generate video if we have a URL from the image step
                if image_url and "http" in image_url:
                    try:
                        logging.info(f"Job {storyboard_id}: Generating AI Video for Scene {scene_num} using {image_url}")
                        video_url = router.generate(
                            prompt=video_prompt,
                            task_type="video_gen", # Routable to FAL_VIDEO_MINIMAX
                            image_url=image_url
                        )
                        
                        if video_url and video_url.startswith("http"):
                            # Download the video
                            temp_video_path = f"temp_video_{storyboard_id}_{i}.mp4"
                            temp_files_to_cleanup.append(temp_video_path)
                            
                            vid_response = requests.get(video_url)
                            if vid_response.status_code == 200:
                                with open(temp_video_path, "wb") as f:
                                    f.write(vid_response.content)
                                # Load clip
                                vid_clip_raw = VideoFileClip(temp_video_path)
                                
                                # Loop or trim to match audio duration
                                if vid_clip_raw.duration < audioclip.duration:
                                     # Loop video to fill audio time
                                     final_scene_clip = vid_clip_raw.with_effects([vfx.Loop(duration=audioclip.duration)])
                                else:
                                     # Trim video to match audio
                                     final_scene_clip = vid_clip_raw.subclipped(0, audioclip.duration)
                                
                                final_scene_clip = final_scene_clip.with_audio(audioclip)
                                # Resize to standard 1024x576
                                final_scene_clip = final_scene_clip.resized(new_size=(1024, 576))
                                logging.info(f"Job {storyboard_id}: AI Video generated successfully for Scene {scene_num}")
                                
                            else:
                                logging.warning(f"Failed to download AI Video: {vid_response.status_code}")
                    except Exception as vid_e:
                        logging.warning(f"AI Video Gen Failed: {vid_e}. Falling back to Ken Burns.")

                # Fallback to Ken Burns if Video Gen failed or skipped
                if not final_scene_clip:
                    # --- Ken Burns Effect (Zoom In) ---
                    # 1. Create Base Image Clip
                    img_clip = ImageClip(temp_image_path, duration=audioclip.duration)
                    
                    # 2. Simple Zoom
                    w, h = img_clip.size
                    zoomed_clip = img_clip.resized(lambda t: 1 + 0.05 * (t / audioclip.duration)) 
                    zoomed_clip = zoomed_clip.with_position('center')
                    
                    final_scene_clip = CompositeVideoClip([zoomed_clip], size=(w, h))
                    final_scene_clip = final_scene_clip.with_audio(audioclip)
                
                video_clips.append(final_scene_clip)

            logging.info(f"Job {storyboard_id}: Stitching {len(video_clips)} clips...")
            
            # Combine all scenes
            from moviepy import concatenate_videoclips
            final_clip = concatenate_videoclips(video_clips, method="compose") # compose handles different sizes if needed
            
            final_clip.write_videofile(final_video_path, codec='libx264', audio_codec='aac', fps=24, logger=None)

            # Local URL
            final_url = f"/static/videos/{final_video_filename}"

            conn.execute(sqlalchemy.text("UPDATE storyboards SET status = 'complete', video_url = :url WHERE id = :id"), {"url": final_url, "id": storyboard_id})
            conn.commit()

            logging.info(f"SUCCESS: Job {storyboard_id} finished. URL: {final_url}")
            return "Task processed successfully.", 200

    except Exception as e:
        logging.error(f"FAILURE: Error processing job {storyboard_id}: {e}", exc_info=True)
        try:
            with db_pool.connect() as conn:
                error_message = str(e)[:1023]
                conn.execute(sqlalchemy.text("UPDATE storyboards SET status = 'failed', error_message = :error WHERE id = :id"), {"error": error_message, "id": storyboard_id})
                conn.commit()
        except Exception as db_err:
            logging.error(f"CRITICAL: could not mark job failed: {db_err}")
        return "Task failed", 500

    finally:
        # Cleanup all temp files
        for f in temp_files_to_cleanup:
            if os.path.exists(f):
                try: os.remove(f)
                except OSError: pass

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return "Worker Service is running.", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8081)) # Default to 8081 for worker
    app.run(debug=False, host='0.0.0.0', port=port)