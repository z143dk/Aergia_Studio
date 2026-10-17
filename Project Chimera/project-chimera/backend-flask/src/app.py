import os
from flask import Flask, request, jsonify
from google.cloud import tasks_v2
import json

app = Flask(__name__)

PROJECT_ID = os.environ.get('GCP_PROJECT', 'project-chimera-backend')
LOCATION_ID = os.environ.get('GCP_REGION', 'us-central1')
QUEUE_ID = 'chimera-jobs-queue'
# The WORKER_URL will be injected as an environment variable by Cloud Run
WORKER_URL = os.environ.get('WORKER_URL')
SERVICE_ACCOUNT_EMAIL = os.environ.get('SERVICE_ACCOUNT_EMAIL')
tasks_client = tasks_v2.CloudTasksClient()

@app.route('/')
def index():
    return "Hello, Project Chimera API Service!"

@app.route('/api/add_storyboard_job', methods=['POST'])
def add_storyboard_job():
    if not (request.form or request.files):
        return jsonify({"status": "error", "message": "No storyboard data received"}), 400
    
    if not WORKER_URL or not SERVICE_ACCOUNT_EMAIL:
        print(f"WORKER_URL or SERVICE_ACCOUNT_EMAIL not set. WORKER_URL: {WORKER_URL}, SA: {SERVICE_ACCOUNT_EMAIL}")
        return jsonify({"status": "error", "message": "Worker service is not configured correctly."}), 500

    payload = {
        "message": "This is a new video generation task.",
        "scene_count": len(request.form),
        "has_files": len(request.files) > 0
    }
    parent = tasks_client.queue_path(PROJECT_ID, LOCATION_ID, QUEUE_ID)
    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": WORKER_URL,
            "headers": {"Content-type": "application/json"},
            "body": json.dumps(payload).encode(),
            "oidc_token": {
                "service_account_email": SERVICE_ACCOUNT_EMAIL
            }
        }
    }
    try:
        response = tasks_client.create_task(request={"parent": parent, "task": task})
        job_id = response.name.split('/')[-1]
        print(f"Successfully created task: {job_id}")
        return jsonify({
            "status": "success",
            "message": f"Job {job_id} successfully submitted for processing.",
            "job_id": job_id
        }), 202
    except Exception as e:
        print(f"Error creating task: {e}")
        return jsonify({"status": "error", "message": f"Failed to submit job to the processing queue: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
