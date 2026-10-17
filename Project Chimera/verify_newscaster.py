import sqlite3
import os
import sys

# Add source to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'source'))
from worker import process_task, DB_PATH, initialize_worker

def create_test_job():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create job
    cursor.execute("INSERT INTO storyboards (status) VALUES ('pending')")
    job_id = cursor.lastrowid
    
    # Create scene with News Caster params
    script = "This is a test of the News Caster system. The time is {{TIME}} on {{DATE}}."
    prompt = "RESOURCE:newscaster_avatar.png"
    
    cursor.execute("INSERT INTO scenes (storyboard_id, scene_number, script, prompt) VALUES (?, ?, ?, ?)", 
                   (job_id, 1, script, prompt))
    
    conn.commit()
    conn.close()
    print(f"Created Test Job ID: {job_id}")
    return job_id

if __name__ == "__main__":
    initialize_worker()
    job_id = create_test_job()
    print("Processing job...")
    try:
        process_task(job_id)
        print("Job processed.")
        
        # Verify output
        output_path = os.path.join(os.path.dirname(__file__), "output", f"storyboard_{job_id}.mp4")
        if os.path.exists(output_path):
            print(f"SUCCESS: Video generated at {output_path}")
        else:
            print("FAILURE: Video file not found.")
            
    except Exception as e:
        print(f"Error: {e}")
