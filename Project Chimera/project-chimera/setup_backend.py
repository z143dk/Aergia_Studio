import os
import subprocess
import pathlib
import sys
import time

# --- Configuration ---
GCP_PROJECT_ID = "project-chimera-backend"
GCP_REGION = "us-central1"
SERVICE_ACCOUNT_EMAIL = f"prometheus-backend-sa@{GCP_PROJECT_ID}.iam.gserviceaccount.com"
REPO_NAME = "chimera-repo"
API_IMAGE_NAME = "chimera-api"
WORKER_IMAGE_NAME = "chimera-worker"
API_SERVICE_NAME = "chimera-api-service"
WORKER_SERVICE_NAME = "chimera-worker-service"
QUEUE_ID = "chimera-jobs-queue"

# --- Define File Contents ---

REQUIREMENTS_CONTENT = """\
flask
gunicorn
moviepy>=2.0.0
google-cloud-storage
google-cloud-tasks
Werkzeug>=2.0.0,<3.0.0
"""

DOCKERFILE_API_CONTENT = """\
# Use an official lightweight Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY src/ .

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run the application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
"""

DOCKERFILE_WORKER_CONTENT = """\
# Use an official lightweight Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the worker application code into the container at /app
COPY src/worker.py .

# Make port 8080 available
EXPOSE 8080

# Run the application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "worker:app"]
"""

APP_PY_CONTENT = """\
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
"""

WORKER_PY_CONTENT = """\
import os
import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/run-task', methods=['POST'])
def run_task():
    try:
        payload = json.loads(request.data)
        print(f"Received task with payload: {payload}")
        message = payload.get("message", "No message received.")
        print(f"Processing task: {message}")
        return "Task received and processed successfully.", 200
    except Exception as e:
        print(f"Error processing task: {e}")
        return f"Error processing task: {e}", 500

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=PORT, debug=True)
"""

# --- Helper Functions ---

def run_command(command, cwd=None):
    """Runs a command in a subprocess and handles errors."""
    print(f"\\n--- Running Command ---\\n{command}\\n----------------------")
    try:
        process = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
            cwd=cwd
        )
    except subprocess.CalledProcessError as e:
        print(f"\\n--- ERROR: Command failed with exit code {e.returncode} ---")
        sys.exit(1)

def main():
    """Main function to set up the backend."""
    # Create directory structure
    print("--- Creating directory structure ---")
    base_path = pathlib.Path("./backend-flask")
    src_path = base_path / "src"
    src_path.mkdir(parents=True, exist_ok=True)
    print(f"Created directory: {src_path}")

    # Write files
    print("--- Writing configuration and source files ---")
    (base_path / "requirements.txt").write_text(REQUIREMENTS_CONTENT)
    (base_path / "Dockerfile").write_text(DOCKERFILE_API_CONTENT)
    (base_path / "Dockerfile.worker").write_text(DOCKERFILE_WORKER_CONTENT)
    (src_path / "__init__.py").touch()
    (src_path / "app.py").write_text(APP_PY_CONTENT)
    (src_path / "worker.py").write_text(WORKER_PY_CONTENT)
    print("All files written successfully.")

    # --- Build, Push, and Deploy Worker Service ---
    print("\\n--- Deploying Worker Service ---")
    worker_image_uri = f"{GCP_REGION}-docker.pkg.dev/{GCP_PROJECT_ID}/{REPO_NAME}/{WORKER_IMAGE_NAME}:latest"
    run_command(f'docker build -f Dockerfile.worker -t {WORKER_IMAGE_NAME} .', cwd=base_path)
    run_command(f'docker tag {WORKER_IMAGE_NAME} {worker_image_uri}', cwd=base_path)
    run_command(f'docker push {worker_image_uri}', cwd=base_path)
    run_command(
        f"gcloud run deploy {WORKER_SERVICE_NAME} "
        f"--image={worker_image_uri} "
        f"--region={GCP_REGION} "
        f"--service-account={SERVICE_ACCOUNT_EMAIL} "
        f"--no-allow-unauthenticated"
    )

    # Get the worker URL with retries to handle propagation delay
    worker_url = None
    for i in range(5): # Retry up to 5 times
        try:
            worker_url_command = f"gcloud run services describe {WORKER_SERVICE_NAME} --region={GCP_REGION} --format='value(status.url)'"
            print(f"\\n--- Attempt {i+1}/5: Getting Worker URL ---")
            worker_url_process = subprocess.run(worker_url_command, shell=True, capture_output=True, text=True, check=True)
            worker_url = worker_url_process.stdout.strip() + "/run-task"
            print(f"Success! Worker URL: {worker_url}")
            break # Exit loop on success
        except subprocess.CalledProcessError:
            print("--- Failed to get worker URL, waiting 10 seconds to retry... ---")
            time.sleep(10)
    
    if not worker_url:
        print("--- ERROR: Could not get worker URL after multiple retries. Exiting. ---")
        sys.exit(1)
        
    # --- Build, Push, and Re-deploy API Service with Worker URL ---
    print("\\n--- Deploying API Service with Worker URL ---")
    api_image_uri = f"{GCP_REGION}-docker.pkg.dev/{GCP_PROJECT_ID}/{REPO_NAME}/{API_IMAGE_NAME}:latest"
    run_command(f'docker build -t {API_IMAGE_NAME} .', cwd=base_path)
    run_command(f'docker tag {API_IMAGE_NAME} {api_image_uri}', cwd=base_path)
    run_command(f'docker push {api_image_uri}', cwd=base_path)
    run_command(
        f"gcloud run deploy {API_SERVICE_NAME} "
        f"--image={api_image_uri} "
        f"--region={GCP_REGION} "
        f"--service-account={SERVICE_ACCOUNT_EMAIL} "
        f"--allow-unauthenticated "
        f"--set-env-vars=WORKER_URL='{worker_url}',SERVICE_ACCOUNT_EMAIL='{SERVICE_ACCOUNT_EMAIL}'"
    )

    print("\\n\\n--- SETUP COMPLETE! ---")
    api_url_process = subprocess.run(f"gcloud run services describe {API_SERVICE_NAME} --region={GCP_REGION} --format='value(status.url)'", shell=True, capture_output=True, text=True)
    api_url = api_url_process.stdout.strip()
    print(f"\\nYour API service is available at: {api_url}")
    print("\\nYou can now run the end-to-end test.")

if __name__ == "__main__":
    main()
