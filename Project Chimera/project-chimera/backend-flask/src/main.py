# main.py for chimera-api-service

from flask import Flask, request, jsonify
import sqlalchemy
import os
from google.cloud import tasks_v2
from google.cloud.sql.connector import Connector

app = Flask(__name__)
db_pool = None

# --- Cloud Tasks Configuration ---
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "project-chimera-backend")
LOCATION_ID = os.environ.get("GCP_REGION", "us-central1")
QUEUE_ID = "chimera-jobs-queue"
# This is the secure URL of your deployed worker service
WORKER_URL = "https://chimera-worker-service-408367094421.us-central1.run.app"
# This is the service account of the API service, which will be invoking the worker
SERVICE_ACCOUNT_EMAIL = "prometheus-backend-sa@project-chimera-backend.iam.gserviceaccount.com" 

tasks_client = tasks_v2.CloudTasksClient()

# --- Database Functions ---
def init_connection_pool():
    global db_pool
    if db_pool: return
    
    instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]
    db_pass = os.environ["DB_PASS"]
    db_user = os.environ.get("DB_USER", "postgres")
    db_name = os.environ.get("DB_NAME", "chimera_db")
    
    connector = Connector()
    
    def getconn():
        return connector.connect(
            instance_connection_name, "pg8000",
            user=db_user, password=db_pass, db=db_name
        )
    
    db_pool = sqlalchemy.create_engine("postgresql+pg8000://", creator=getconn)

# --- API Endpoint Logic ---
@app.route('/api/add_storyboard_job', methods=['POST'])
def add_storyboard_job():
    if db_pool is None: init_connection_pool()

    scenes_data = request.form.to_dict()
    if not scenes_data:
        return jsonify({"status": "error", "message": "No scene data provided."}), 400

    storyboard_id = None
    try:
        with db_pool.connect() as conn:
            # Create a new storyboard entry
            stmt_storyboard = sqlalchemy.text("INSERT INTO storyboards (status) VALUES ('pending') RETURNING id")
            result = conn.execute(stmt_storyboard).fetchone()
            storyboard_id = result[0]

            # Insert scenes
            for key, script in scenes_data.items():
                if key.startswith("scene_"):
                    scene_number = int(key.split("_")[1])
                    # In a real app, you'd generate a more detailed prompt here
                    prompt = f"A cinematic shot for the scene: {script}"
                    stmt_scene = sqlalchemy.text(
                        "INSERT INTO scenes (storyboard_id, scene_number, script, prompt) VALUES (:sid, :s_num, :script, :prompt)"
                    )
                    conn.execute(stmt_scene, {"sid": storyboard_id, "s_num": scene_number, "script": script, "prompt": prompt})
            conn.commit()

    except Exception as e:
        return jsonify({"status": "error", "message": f"Database error: {e}"}), 500

    # --- Create Task in Cloud Tasks ---
    try:
        task_payload = {'storyboard_id': storyboard_id}
        
        task = {
            "http_request": {
                "http_method": tasks_v2.HttpMethod.POST,
                "url": WORKER_URL,
                "oidc_token": {"service_account_email": SERVICE_ACCOUNT_EMAIL},
                "headers": {"Content-type": "application/json"},
                "body": jsonify(task_payload).data,
            }
        }

        parent = tasks_client.queue_path(PROJECT_ID, LOCATION_ID, QUEUE_ID)
        response = tasks_client.create_task(parent=parent, task=task)
        
        print(f"Created task: {response.name}")
        return jsonify({"status": "success", "message": f"Storyboard job {storyboard_id} created and queued.", "storyboard_id": storyboard_id}), 201

    except Exception as e:
        # If queuing fails, we should ideally roll back the database transaction or mark the job as failed.
        # For now, we'll return an error.
        print(f"Error creating task: {e}")
        return jsonify({"status": "error", "message": f"Failed to queue job: {e}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
