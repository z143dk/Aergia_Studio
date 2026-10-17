import subprocess
import time
import sqlite3
import os
import sys

# Configuration
PYTHON_EXE = r"C:\Users\z143d\AppData\Local\Programs\Python\Python312\python.exe"
WORKER_PATH = os.path.join("Project Chimera", "source", "worker.py")
DB_PATH = os.path.join("Project Chimera", "data", "chimera.db")

def setup_db_job():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Insert Job
    c.execute("INSERT INTO storyboards (status) VALUES ('pending')")
    job_id = c.lastrowid
    
    # Insert Scene (Short prompt for test)
    c.execute("INSERT INTO scenes (storyboard_id, scene_number, script, prompt) VALUES (?, ?, ?, ?)",
              (job_id, 1, "Quick test of FAL video generation.", "A hyper-realistic golden coin spinning on a wooden table, 4k, cinematic support"))
    conn.commit()
    conn.close()
    return job_id

def monitor_job(job_id, timeout=120):
    start_time = time.time()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print(f"Monitoring Job {job_id}...")
    while time.time() - start_time < timeout:
        c.execute("SELECT status, error_message, video_url FROM storyboards WHERE id = ?", (job_id,))
        row = c.fetchone()
        if not row:
            print("Job disappeared?")
            break
            
        status, error, video = row
        print(f"Status: {status}")
        
        if status == 'complete':
            print(f"SUCCESS! Video at: {video}")
            conn.close()
            return True
        elif status == 'failed':
            print(f"FAILED! Error: {error}")
            conn.close()
            return False
            
        time.sleep(5)
        
    print("Timeout waiting for job completion.")
    conn.close()
    return False

def test_worker():
    print(f"Testing FAL Integration using Python: {PYTHON_EXE}")
    
    # 1. Create Job
    job_id = setup_db_job()
    print(f"Created Pending Job {job_id}")

    # 2. Start Worker
    # We must set FAL_KEY in env if not in system env
    # It reads .env, but we can pass it explicitly if we want safe.
    # Assuming .env is in CWD or loaded by worker
    
    print("Launching Worker subprocess...")
    process = subprocess.Popen([PYTHON_EXE, WORKER_PATH], cwd=os.getcwd())
    
    try:
        # 3. Monitor
        success = monitor_job(job_id)
        
        if success:
             print("Test PASSED.")
        else:
             print("Test FAILED.")
             
    finally:
        print("Terminating worker...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except:
            process.kill()

if __name__ == "__main__":
    test_worker()
