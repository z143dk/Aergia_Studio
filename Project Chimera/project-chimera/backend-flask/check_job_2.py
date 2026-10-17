import sqlite3
import os

DB_PATH = os.path.abspath("chimera.db")

def check_job(job_id):
    if not os.path.exists(DB_PATH):
        print("Database not found.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check storyboard status
        cursor.execute("SELECT id, status, video_url, error_message FROM storyboards WHERE id = ?", (job_id,))
        row = cursor.fetchone()
        
        if row:
            print(f"Job ID: {row[0]}")
            print(f"Status: {row[1]}")
            print(f"Video URL: {row[2]}")
            print(f"Error Message: {row[3]}")
            
            # Check scenes
            cursor.execute("SELECT scene_number, script, prompt FROM scenes WHERE storyboard_id = ? ORDER BY scene_number", (job_id,))
            scenes = cursor.fetchall()
            print(f"\nScenes ({len(scenes)}):")
            for scene in scenes:
                print(f"  Scene {scene[0]}: {scene[1][:50]}... | {scene[2][:50]}...")
        else:
            print(f"Job {job_id} not found in database.")
            
        conn.close()

    except Exception as e:
        print(f"Error reading DB: {e}")

if __name__ == "__main__":
    check_job(2)
