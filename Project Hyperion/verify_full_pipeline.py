
import sys
import os
import requests
import json
import time
import subprocess
import sqlite3

# Import Director
sys.path.append(os.path.dirname(__file__))
from hyperion_director import HyperionDirector

# Config
BASE_DIR = r"c:\Users\z143d\OneDrive\Desktop\Project Aergia\Project Chimera\project-chimera\backend-flask"
APP_PATH = os.path.join(BASE_DIR, "app.py")
DB_PATH = os.path.join(BASE_DIR, "chimera.db")
API_URL = "http://localhost:5001/api/add_storyboard_job"
API_KEY = "local-dev-key"
PYTHON_EXE = sys.executable

def start_server():
    print(f"Starting API Server: {APP_PATH}")
    process = subprocess.Popen(
        [PYTHON_EXE, APP_PATH],
        cwd=BASE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )
    time.sleep(5)
    return process

def run_test():
    print("🎬 Initializing AI Director...")
    director = HyperionDirector()
    concept = "A cyberpunk city at night with neon lights"
    
    print(f"🎬 Directing: '{concept}'...")
    scenes = director.direct_movie(concept)
    
    if not scenes:
        print("❌ Director returned no scenes")
        return False
        
    print(f"✅ Generated {len(scenes)} scenes.")
    
    # Build Payload
    payload = {}
    for scene in scenes:
        key = f"scene_{scene['scene_number']}"
        value = f"{scene['script']}|{scene['prompt']}"
        payload[key] = value
        
    print("🚀 Sending to Chimera API...")
    headers = {"X-API-KEY": API_KEY}
    
    try:
        response = requests.post(API_URL, data=payload, headers=headers, timeout=10)
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            job_id = data.get("storyboard_id")
            print(f"✅ Job Created: ID {job_id}")
            return job_id
            
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return False
        
    return False

def verify_db(job_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scenes WHERE storyboard_id = ?", (job_id,))
    rows = cursor.fetchall()
    conn.close()
    
    print(f"DB Verification: Found {len(rows)} scenes for Job {job_id}")
    return len(rows) > 0

def main():
    server_proc = start_server()
    try:
        job_id = run_test()
        if job_id:
            if verify_db(job_id):
                print("✅ FULL PIPELINE SUCCESS")
            else:
                print("❌ DB VERIFICATION FAILED")
        else:
            print("❌ TEST FAILED")
    finally:
        server_proc.kill()

if __name__ == "__main__":
    main()
