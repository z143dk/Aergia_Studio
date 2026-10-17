import sys
import os
import sqlite3
import logging

# Setup Env
os.environ["GOOGLE_CLOUD_PROJECT"] = "project-chimera-backend"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(r"..\project-chimera\backend-flask\chimera-credentials.json")

# Import worker (ensure source is in path)
sys.path.append(os.getcwd())
from worker import process_task, init_db, DB_PATH

# Setup logging to console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_test():
    print("--- Starting Pipeline Verification Test ---")
    
    # 1. Init DB
    init_db()
    
    # 2. Insert Test Job
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    script = "This is a test of the automatic video generation system."
    prompt = "A futuristic city with flying cars, cyberpunk style, high quality"
    
    cursor.execute("INSERT INTO storyboards (status) VALUES ('pending')")
    job_id = cursor.lastrowid
    
    cursor.execute("INSERT INTO scenes (storyboard_id, scene_number, script, prompt) VALUES (?, ?, ?, ?)", 
                   (job_id, 1, script, prompt))
    
    conn.commit()
    conn.close()
    
    print(f"Test Job ID: {job_id} created.")
    
    # 3. Run Worker Processing
    print(f"Processing Job {job_id}...")
    try:
        from worker import initialize_worker
        initialize_worker()
        process_task(job_id)
        print("Processing complete.")
    except Exception as e:
        print(f"Processing FAILED: {e}")
        sys.exit(1)
        
    # 4. Verify Output
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT status, video_path, error_message FROM storyboards WHERE id = ?", (job_id,))
    status, path, error = cursor.fetchone()
    conn.close()
    
    print(f"Final Status: {status}")
    if status == 'complete':
        if os.path.exists(path):
             print(f"SUCCESS: Video found at {path}")
             sys.exit(0)
        else:
             print(f"FAILURE: Status complete but file missing at {path}")
             sys.exit(1)
    else:
        print(f"FAILURE: Job failed with error: {error}")
        sys.exit(1)

if __name__ == "__main__":
    run_test()
