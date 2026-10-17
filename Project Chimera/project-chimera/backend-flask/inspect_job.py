import sqlalchemy
import os

db_path = os.path.abspath(r"c:\Users\z143d\OneDrive\Desktop\Project Aergia\Project Chimera\project-chimera\backend-flask\chimera.db")
print(f"Connecting to DB at: {db_path}")
engine = sqlalchemy.create_engine(f"sqlite:///{db_path}")

try:
    with engine.connect() as conn:
        # Get latest storyboard
        latest_job = conn.execute(sqlalchemy.text("SELECT id, status, video_url, error_message FROM storyboards ORDER BY id DESC LIMIT 1")).fetchone()
        
        if not latest_job:
            print("No jobs found in database.")
        else:
            job_id, status, url, error = latest_job
            print(f"\n--- Latest Job ID: {job_id} ---")
            print(f"Status: {status}")
            print(f"Video URL: {url}")
            print(f"Error Message: {error}")
            
            print(f"\n--- Scenes for Job {job_id} ---")
            result = conn.execute(sqlalchemy.text("SELECT scene_number, script, prompt FROM scenes WHERE storyboard_id = :id"), {"id": job_id}).fetchall()
            
            if not result:
                print("No scenes found!")
            else:
                for row in result:
                    print(f"Scene {row[0]}:")
                    print(f"  Script: '{row[1]}'")
                    print(f"  Prompt: '{row[2]}'")
                    print("-" * 20)
except Exception as e:
    print(f"Error: {e}")
