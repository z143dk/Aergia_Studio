import os
import sqlite3
import time
import traceback
from flask import Flask
import threading
# --- CORRECTED IMPORT for moviepy v2.x ---
from moviepy import VideoFileClip, concatenate_videoclips, ColorClip

# Note: The google.cloud and vertexai imports are kept for future use,
# but are not needed for the current simulation mode.

# --- Configuration ---
DATABASE_FILE = 'database.db'
SIMULATION_MODE = True

# --- Flask App for Health Checks ---
app = Flask(__name__)

@app.route('/')
def health_check():
    """Provides a simple health check endpoint for Cloud Run."""
    return "Worker is running.", 200

# --- Database Functions ---

def get_db_connection():
    """Creates and returns a new database connection."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def check_database_ready():
    """Checks if the database and tables are ready."""
    if not os.path.exists(DATABASE_FILE):
        return False
    try:
        conn = get_db_connection()
        with conn:
            conn.execute("SELECT id FROM storyboards LIMIT 1")
            conn.execute("SELECT id FROM scenes LIMIT 1")
        conn.close()
        return True
    except sqlite3.OperationalError:
        return False

# --- Main Worker Logic ---

def update_job_status(conn, table, job_id, status):
    """Helper function to update the status of a job/scene."""
    with conn:
        conn.execute(f"UPDATE {table} SET status = ? WHERE id = ?", (status, job_id))
    print(f"   🔄 Status for {table} #{job_id} updated to '{status}'.")

def process_storyboard(storyboard):
    """Processes all scenes within a storyboard job."""
    storyboard_id = storyboard['id']
    conn = get_db_connection()
    
    try:
        print(f"✅ Found storyboard job #{storyboard_id}. Processing scenes...")
        update_job_status(conn, 'storyboards', storyboard_id, 'processing')

        scenes = conn.execute("SELECT * FROM scenes WHERE storyboard_id = ? ORDER BY scene_number ASC", (storyboard_id,)).fetchall()
        
        generated_clips = []
        for scene in scenes:
            scene_id = scene['id']
            update_job_status(conn, 'scenes', scene_id, 'processing')
            
            audio_path = generate_audio(scene_id, scene['script'])
            video_path = generate_video(scene_id, scene['script'], scene['style'], scene['source_file_path'])
            
            with conn:
                conn.execute("UPDATE scenes SET audio_file = ?, video_file = ? WHERE id = ?", (audio_path, video_path, scene_id))
            
            generated_clips.append(video_path)
            update_job_status(conn, 'scenes', scene_id, 'complete')

        print(f"   🎬 Stitching {len(generated_clips)} clips together for storyboard #{storyboard_id}...")
        
        final_video_path = os.path.join('static', 'video', f'storyboard_{storyboard_id}_final.mp4')
        
        video_clips = [VideoFileClip(clip) for clip in generated_clips]
        
        final_clip = concatenate_videoclips(video_clips, method="compose")
        final_clip.write_videofile(final_video_path, codec="libx264", audio_codec="aac")

        print(f"   ✅ Final video created: {final_video_path}")

        with conn:
            conn.execute("UPDATE storyboards SET status = ?, final_video_file = ? WHERE id = ?", ('complete', final_video_path, storyboard_id))
        print(f"🎉 Finished processing storyboard #{storyboard_id}.")

    except Exception as e:
        print(f"❌ Failed to process storyboard #{storyboard_id}. Error: {e}")
        traceback.print_exc()
        update_job_status(conn, 'storyboards', storyboard_id, 'failed')
    finally:
        conn.close()


def generate_audio(scene_id, text_to_speak):
    """Generates audio from text and saves it."""
    output_directory = "static/audio"
    os.makedirs(output_directory, exist_ok=True)
    output_filepath = os.path.join(output_directory, f"scene_{scene_id}_audio.mp3")
    if SIMULATION_MODE:
        print(f"      (Sim) TTS for scene #{scene_id}...")
        time.sleep(1)
        with open(output_filepath, 'w') as f: f.write("Simulated audio")
    return output_filepath

def generate_video(scene_id, script, style, source_file_path):
    """Generates a video for a single scene."""
    output_directory = "static/video"
    os.makedirs(output_directory, exist_ok=True)
    output_filepath = os.path.join(output_directory, f"scene_{scene_id}_video.mp4")
    
    if SIMULATION_MODE:
        if source_file_path:
            print(f"      (Sim) Image-to-Video for scene #{scene_id}...")
        else:
            print(f"      (Sim) Text-to-Video for scene #{scene_id}...")
        clip = ColorClip(size=(640, 480), color=(0,0,0), duration=3)
        clip.write_videofile(output_filepath, fps=24)
    return output_filepath

def find_and_process_job():
    """Looks for a pending storyboard job and processes it."""
    conn = get_db_connection()
    storyboard_row = conn.execute("SELECT * FROM storyboards WHERE status = 'pending' ORDER BY id ASC LIMIT 1").fetchone()
    conn.close()

    if storyboard_row:
        process_storyboard(dict(storyboard_row))
    else:
        print(".", end="", flush=True)

def worker_loop():
    """Main loop for the worker to continuously check for jobs."""
    print("🚀 Worker loop started.")
    
    while not check_database_ready():
        print("⏳ Waiting for database... (retrying in 3s)", end="\r")
        time.sleep(3)
    
    print("\n✅ Database found. Watching for jobs...")

    while True:
        find_and_process_job()
        time.sleep(2)

if __name__ == '__main__':
    worker_thread = threading.Thread(target=worker_loop)
    worker_thread.daemon = True
    worker_thread.start()

    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
