import requests
import sys

API_URL = "http://127.0.0.1:5002/api/add_storyboard_job"
API_KEY = "local-dev-key"

def test_pipeline():
    print("Testing Connection to Live Server (Port 5002)...")
    try:
        # 1. Check Health
        resp = requests.get("http://127.0.0.1:5002/")
        print(f"Health Check: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"CRITICAL: Cannot connect to server: {e}")
        return

    # 2. Submit a dummy job
    print("\nSubmitting Test Job...")
    headers = {"X-API-KEY": API_KEY}
    payload = {
        "scene_1": "Test Script|Test Prompt"
    }
    
    try:
        resp = requests.post(API_URL, data=payload, headers=headers)
        print(f"Job Submission: {resp.status_code}")
        print(resp.text)
        
        if resp.status_code == 200:
            data = resp.json()
            job_id = data.get('storyboard_id')
            print(f"PASS: Job Created with ID {job_id}")
        else:
            print("FAIL: Job submission failed")
            
    except Exception as e:
        print(f"FAIL: Submission Error: {e}")

if __name__ == "__main__":
    test_pipeline()
