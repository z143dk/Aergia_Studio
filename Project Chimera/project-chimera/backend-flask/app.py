import os
from dotenv import load_dotenv

# Load environment variables from .env or .env.local
load_dotenv()
load_dotenv(".env.local")

import logging
import sqlalchemy
import requests
import threading
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps

# --- App Initialization ---
app = Flask(__name__)
CORS(app)
db_pool = None

# Default to local worker if not set
WORKER_URL = os.environ.get("WORKER_URL", "http://localhost:5001")
API_KEY = os.environ.get("API_KEY", "local-dev-key")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(funcName)s] %(message)s')

def initialize_app():
    """Initializes the database connection pool."""
    global db_pool
    if db_pool:
        return

    logging.info("Initializing API service...")
    try:
        # Use local SQLite database
        # Use local SQLite database
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        db_path = os.path.join(base_dir, "data", "chimera.db")
        db_pool = sqlalchemy.create_engine(f"sqlite:///{db_path}")
        logging.info(f"Database initialized at {db_path}")

        # Create tables if they don't exist
        with db_pool.connect() as conn:
            conn.execute(sqlalchemy.text("""
                CREATE TABLE IF NOT EXISTS storyboards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    status TEXT DEFAULT 'pending',
                    video_url TEXT,
                    error_message TEXT
                )
            """))
            conn.execute(sqlalchemy.text("""
                CREATE TABLE IF NOT EXISTS scenes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    storyboard_id INTEGER,
                    scene_number INTEGER,
                    script TEXT,
                    prompt TEXT,
                    FOREIGN KEY(storyboard_id) REFERENCES storyboards(id)
                )
            """))
            conn.commit()

    except Exception as e:
        logging.critical(f"FATAL: Could not initialize API service: {e}", exc_info=True)
        raise

# Initialize everything when the application starts
initialize_app()

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if API_KEY is None:
            logging.error("API Key is not configured on the server.")
            return jsonify({"status": "error", "message": "Server configuration error"}), 500
        
        provided_key = request.headers.get('X-API-KEY')
        if not provided_key or provided_key != API_KEY:
            logging.warning("Forbidden: Invalid or missing API Key provided.")
            return jsonify({"status": "error", "message": "Forbidden: Invalid or missing API Key"}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/add_storyboard_job', methods=['POST'])
@require_api_key
def add_storyboard_job():
    if db_pool is None:
        return jsonify({"status": "error", "message": "API not initialized"}), 500

    try:
        with db_pool.connect() as conn:
            stmt = sqlalchemy.text("INSERT INTO storyboards (status) VALUES ('pending') RETURNING id")
            result = conn.execute(stmt).fetchone()
            if not result:
                raise Exception("Failed to create storyboard entry in the database.")
            storyboard_id = result[0] 

            scenes = []
            for key in request.form:
                if key.startswith('scene_'):
                    scene_number = int(key.split('_')[1])
                    
                    raw_data = request.form[key]
                    script = ""
                    prompt = ""
                    
                    # Sanitation: Check if data is JSON (legacy/cached frontend)
                    import json
                    if raw_data.strip().startswith('{'):
                        try:
                            json_data = json.loads(raw_data)
                            script = json_data.get('script', '')
                            # Use prompt from JSON, or script only if prompt missing? 
                            # If prompt key is missing in JSON, let's assume script is prompt for now
                            prompt = json_data.get('prompt', '') or script 
                            
                            # Correction: If prompt is empty string in JSON, we might want to default it
                            if not prompt and script: prompt = script
                        except json.JSONDecodeError:
                            # Fallback if looks like JSON but isn't
                            script = raw_data
                            prompt = ""
                    else:
                        # Standard Pipe Format
                        script, prompt = raw_data.split('|', 1) if '|' in raw_data else (raw_data, "")
                        # If prompt is missing from pipe split (e.g. "text|"), default to script?
                        # No, keep empty string if explicit. But if "text" (no pipe), prompt is empty.
                        if not prompt and script: prompt = script # Ensure we always have a prompt for AI

                    scenes.append({
                        "scene_number": scene_number,
                        "script": script.strip(),
                        "prompt": prompt.strip()
                    })
            
            scenes.sort(key=lambda x: x['scene_number'])

            for scene in scenes:
                conn.execute(
                    sqlalchemy.text("INSERT INTO scenes (storyboard_id, scene_number, script, prompt) VALUES (:storyboard_id, :scene_number, :script, :prompt)"),
                    {"storyboard_id": storyboard_id, "scene_number": scene['scene_number'], "script": scene['script'], "prompt": scene['prompt']}
                )
            
            conn.commit()

            # Trigger worker directly
            def trigger_worker(sid):
                try:
                    requests.post(WORKER_URL, json={"storyboard_id": sid}, timeout=1)
                except requests.exceptions.RequestException:
                    # Ignore timeout/connection errors as we just want to trigger it
                    pass

            # Run in a separate thread to not block the API response
            threading.Thread(target=trigger_worker, args=(storyboard_id,)).start()
            
            status_url = f"/api/storyboard/{storyboard_id}"
            
            return jsonify({
                "status": "success",
                "message": f"Storyboard job {storyboard_id} created and queued.",
                "storyboard_id": storyboard_id,
                "status_url": status_url
            })

    except Exception as e:
        logging.error(f"Error creating storyboard job: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/storyboard/<int:job_id>', methods=['GET'])
@require_api_key
def get_job_status(job_id):
    if db_pool is None:
        return jsonify({"status": "error", "message": "API not initialized"}), 500

    try:
        with db_pool.connect() as conn:
            stmt = sqlalchemy.text("SELECT status, video_url, error_message FROM storyboards WHERE id = :job_id")
            result = conn.execute(stmt, {"job_id": job_id}).fetchone()
            
            if not result:
                return jsonify({"status": "error", "message": "Job not found"}), 404

            status, video_url, error_message = result
            return jsonify({ "job_id": job_id, "status": status, "video_url": video_url, "error_message": error_message })

    except Exception as e:
        logging.error(f"Error getting job status for {job_id}: {e}", exc_info=True)
        return jsonify({"status": "error", "message": "Server error while fetching job status"}), 500

@app.route('/api/storyboard/<int:job_id>', methods=['DELETE'])
@require_api_key
def delete_storyboard_job(job_id):
    if db_pool is None:
        return jsonify({"status": "error", "message": "API not initialized"}), 500

    try:
        with db_pool.connect() as conn:
            # Delete related scenes first
            conn.execute(sqlalchemy.text("DELETE FROM scenes WHERE storyboard_id = :job_id"), {"job_id": job_id})
            # Delete the storyboard itself
            result = conn.execute(sqlalchemy.text("DELETE FROM storyboards WHERE id = :job_id"), {"job_id": job_id})
            conn.commit()

            if result.rowcount == 0:
                return jsonify({"status": "error", "message": "Job not found"}), 404

            return jsonify({"status": "success", "message": f"Job {job_id} deleted successfully"})

    except Exception as e:
        logging.error(f"Error deleting job {job_id}: {e}", exc_info=True)
        return jsonify({"status": "error", "message": "Server error while deleting job"}), 500

@app.route('/api/storyboards', methods=['GET'])
@require_api_key
def list_storyboards():
    if db_pool is None:
        return jsonify({"status": "error", "message": "API not initialized"}), 500

    try:
        with db_pool.connect() as conn:
            # Fetch latest 20 jobs, ordered by newest first
            stmt = sqlalchemy.text("SELECT id, status, video_url, error_message FROM storyboards ORDER BY id DESC LIMIT 20")
            result = conn.execute(stmt).fetchall()
            
            jobs = []
            for row in result:
                jobs.append({
                    "id": row[0],
                    "status": row[1],
                    "video_url": row[2],
                    "error_message": row[3]
                })

            return jsonify({"status": "success", "jobs": jobs})

    except Exception as e:
        logging.error(f"Error listing storyboards: {e}", exc_info=True)
        return jsonify({"status": "error", "message": "Server error while fetching jobs"}), 500

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint for Cloud Run."""
    return "API Service is running.", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=False, host='0.0.0.0', port=port)