from flask import Flask, request, jsonify
import sqlalchemy
import os
from google.cloud import tasks_v2
from google.cloud.sql.connector import Connector
import logging

# --- App Initialization ---
app = Flask(__name__)
db_pool = None
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(funcName)s] %(message)s')

# --- Configuration from Environment Variables ---
# These are set in your deploy-api.bat script
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
LOCATION_ID = os.environ.get("GCP_REGION")
QUEUE_ID = "chimera-jobs-queue"
WORKER_URL = os.environ.get("WORKER_URL")
SERVICE_ACCOUNT_EMAIL = os.environ.get("SERVICE_ACCOUNT_EMAIL")

tasks_client = tasks_v2.CloudTasksClient()

# --- Database Connection Pool ---
# This function is called once to set up the connection.
def init_connection_pool():
    global db_pool
    if db_pool: return

    logging.info("Initializing Cloud SQL connection pool for API service...")
    try:
        # These variables are securely injected by Cloud Run from Secret Manager
        instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]
        db_pass = os.environ["DB_PASS"]
        db_name = os.environ["DB_NAME"]
        db_user = os.environ.get("DB_USER", "postgres")
        
        connector = Connector()

        def getconn():
            return connector.connect(
                instance_connection_name, "pg8000",
                user=db_user, password=db_pass, db=db_name
            )

        db_pool = sqlalchemy.create_engine("postgresql+pg8000://", creator=getconn)
        logging.info("Database pool for API service initialized successfully.")
    except Exception as e:
        # This logging helps debug if a secret is missing
        for var in ["INSTANCE_CONNECTION_NAME", "DB_PASS", "DB_NAME"]:
            if not os.environ.get(var):
                logging.critical(f"FATAL: Missing a required secret environment variable: '{var}'")
        logging.critical(f"FATAL: Could not initialize database pool: {e}", exc_info=True)
        raise

# --- API Endpoint to Create a New Job ---
@app.route('/api/add_storyboard_job', methods=['POST'])
def add_storyboard_job():
    if db_pool is None: init_connection_pool()

    scenes_data = request.form.to_dict()
    if not scenes_data:
        return jsonify({"status": "error", "message": "No scene data provided."}), 400

    storyboard_id = None
    try:
        # --- Database Transaction: Create Storyboard and Scenes ---
        with db_pool.connect() as conn:
            stmt_storyboard = sqlalchemy.text("INSERT INTO storyboards (status) VALUES ('pending') RETURNING id")
            result = conn.execute(stmt_storyboard).fetchone()
            storyboard_id = result[0]

            for key, script in scenes_data.items():
                if key.startswith("scene_"):
                    scene_number = int(key.split("_")[1])
                    prompt = f"A cinematic, photorealistic shot for the scene: {script}"
                    stmt_scene = sqlalchemy.text("INSERT INTO scenes (storyboard_id, scene_number, script, prompt) VALUES (:sid, :s_num, :script, :prompt)")
                    conn.execute(stmt_scene, {"sid": storyboard_id, "s_num": scene_number, "script": script, "prompt": prompt})
            conn.commit() # Commit the transaction
            logging.info(f"Successfully created storyboard {storyboard_id} in database.")
    except Exception as e:
        logging.error(f"Database error while creating storyboard: {e}", exc_info=True)
        return jsonify({"status": "error", "message": f"Database error: {e}"}), 500

    # --- Task Creation: Send Job to Worker ---
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
        logging.info(f"Created Cloud Task: {response.name}")
        status_url = f"/api/storyboard/{storyboard_id}"
        return jsonify({"status": "success", "message": f"Storyboard job {storyboard_id} created and queued.", "storyboard_id": storyboard_id, "status_url": status_url}), 201
    except Exception as e:
        logging.error(f"Error creating Cloud Task for storyboard {storyboard_id}: {e}", exc_info=True)
        # Here you might want to mark the DB job as 'failed_to_queue'
        return jsonify({"status": "error", "message": f"Failed to queue job: {e}"}), 500

# --- API Endpoint to Check Job Status ---
@app.route('/api/storyboard/<int:storyboard_id>', methods=['GET'])
def get_storyboard_status(storyboard_id):
    if db_pool is None: init_connection_pool()
    try:
        with db_pool.connect() as conn:
            stmt = sqlalchemy.text("SELECT status, video_url, error_message FROM storyboards WHERE id = :job_id")
            result = conn.execute(stmt, {"job_id": storyboard_id}).fetchone()
            if result:
                status, video_url, error_message = result
                return jsonify({"storyboard_id": storyboard_id, "status": status, "video_url": video_url, "error_message": error_message})
            else:
                return jsonify({"status": "error", "message": "Storyboard not found."}), 404
    except Exception as e:
        logging.error(f"Database error while fetching status for storyboard {storyboard_id}: {e}", exc_info=True)
        return jsonify({"status": "error", "message": f"Database error: {e}"}), 500

# This part is for running the app locally, which Gunicorn doesn't use in Cloud Run.
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # When running locally, you need to set the environment variables yourself.
    init_connection_pool()
    app.run(debug=True, host='0.0.0.0', port=port)

