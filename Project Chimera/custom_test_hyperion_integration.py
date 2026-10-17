import subprocess
import time
import requests
import sys
import os
import signal
import sqlite3

# Configuration
PYTHON_EXE = sys.executable
BASE_DIR = r"c:\Users\z143d\OneDrive\Desktop\Project Aergia\Project Chimera\project-chimera\backend-flask"
APP_PATH = os.path.join(BASE_DIR, "app.py")
DB_PATH = os.path.join(BASE_DIR, "chimera.db")
API_URL = "http://localhost:5001/api/add_storyboard_job"
API_KEY = "local-dev-key"

def start_server():
    print(f"Starting API Server: {APP_PATH}")
    # Run in a new process group so we can kill it easily
    process = subprocess.Popen(
        [PYTHON_EXE, APP_PATH],
        cwd=BASE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )
    time.sleep(5)  # Wait for startup
    return process

def test_api():
    print("Sending Test Payload...")
    payload = {
        "scene_1": "A robot serving coffee|Futuristic robot barista, cinematic lighting"
    }
    headers = {
        "X-API-KEY": API_KEY
    }
    
    try:
        response = requests.post(API_URL, data=payload, headers=headers, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return data.get("storyboard_id")
    except Exception as e:
        print(f"Request failed: {e}")
        return None
    return None

def verify_db(job_id):
    print(f"Verifying Job {job_id} in Database...")
    if not os.path.exists(DB_PATH):
        print("Database not found!")
        return False
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM storyboards WHERE id = ?", (job_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        print(f"DB Entry Found: {row}")
        return True
    else:
        print("Job not found in DB.")
        return False

def main():
    server_proc = start_server()
    try:
        job_id = test_api()
        if job_id:
            print("API Test: PASSED")
            if verify_db(job_id):
                print("DB Verification: PASSED")
            else:
                print("DB Verification: FAILED")
        else:
            print("API Test: FAILED")
            
    finally:
        print("Stopping Server...")
        # Kill the process
        server_proc.kill()
        # os.kill(server_proc.pid, signal.SIGTERM) 
        print("Done.")

if __name__ == "__main__":
    main()
