import sqlalchemy
import os
import sys

# Force UTF-8 for output
sys.stdout.reconfigure(encoding='utf-8')

db_path = os.path.abspath(r"c:\Users\z143d\OneDrive\Desktop\Project Aergia\Project Chimera\project-chimera\backend-flask\chimera.db")
engine = sqlalchemy.create_engine(f"sqlite:///{db_path}")

try:
    with engine.connect() as conn:
        print("Checking latest job...")
        latest_job = conn.execute(sqlalchemy.text("SELECT id, status, video_url, error_message FROM storyboards ORDER BY id DESC LIMIT 1")).fetchone()
        
        if not latest_job:
            print("No jobs found.")
        else:
            job_id, status, url, error = latest_job
            print(f"ID: {job_id}")
            print(f"Status: {status}")
            print(f"URL: {url}")
            print(f"Error: {error}")
            
            scenes = conn.execute(sqlalchemy.text("SELECT script, prompt FROM scenes WHERE storyboard_id = :id"), {"id": job_id}).fetchall()
            for i, (script, prompt) in enumerate(scenes):
                print(f"Scene {i+1} Script: {script}")
                print(f"Scene {i+1} Prompt: {prompt}")

except Exception as e:
    print(f"Error: {e}")
