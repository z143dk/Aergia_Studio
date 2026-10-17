import os
from flask import Flask, request, jsonify
from google.cloud.sql.connector import Connector
import sqlalchemy

# --- Configuration ---
app = Flask(__name__)

# Database connection settings will be read from environment variables
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME", "chimera_db")
INSTANCE_CONNECTION_NAME = os.environ.get("INSTANCE_CONNECTION_NAME")

# --- Database Setup ---
db = None

def init_connection_pool() -> sqlalchemy.engine.base.Engine:
    """Initializes a connection pool for the database."""
    connector = Connector()
    def getconn():
        conn = connector.connect(
            INSTANCE_CONNECTION_NAME,
            "pg8000",
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME
        )
        return conn
    
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )
    return pool

def create_tables(engine):
    """Creates the necessary tables if they don't exist."""
    metadata = sqlalchemy.MetaData()
    
    sqlalchemy.Table('storyboards', metadata,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True),
        sqlalchemy.Column('status', sqlalchemy.String(50), default='pending'),
        sqlalchemy.Column('final_video_file', sqlalchemy.String(255), nullable=True),
        sqlalchemy.Column('created_at', sqlalchemy.DateTime, server_default=sqlalchemy.func.now())
    )
    
    sqlalchemy.Table('scenes', metadata,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True),
        sqlalchemy.Column('storyboard_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('storyboards.id')),
        sqlalchemy.Column('scene_number', sqlalchemy.Integer),
        sqlalchemy.Column('script', sqlalchemy.Text),
        sqlalchemy.Column('style', sqlalchemy.String(100)),
        sqlalchemy.Column('source_file_path', sqlalchemy.String(255), nullable=True),
        sqlalchemy.Column('status', sqlalchemy.String(50), default='pending'),
        sqlalchemy.Column('audio_file', sqlalchemy.String(255), nullable=True),
        sqlalchemy.Column('video_file', sqlalchemy.String(255), nullable=True)
    )
    
    metadata.create_all(engine)
    print("Tables checked and created if necessary.")

# This block runs when the application starts
with app.app_context():
    if not DB_PASS or not INSTANCE_CONNECTION_NAME:
        print("WARNING: Database environment variables not set. API will not be able to connect.")
    else:
        db = init_connection_pool()
        create_tables(db)

# --- API Endpoints ---

@app.route('/')
def index():
    return "Hello, Project Chimera API Service! Now connected to Cloud SQL."

@app.route('/api/add_storyboard_job', methods=['POST'])
def add_storyboard_job():
    if not db:
        return jsonify({"status": "error", "message": "Database is not configured or connected."}), 500
        
    scenes_data = request.form.to_dict()
    if not scenes_data:
        return jsonify({"status": "error", "message": "No scene data provided in the form."}), 400

    try:
        with db.connect() as conn:
            trans = conn.begin()
            # Insert the parent storyboard job
            storyboard_insert = sqlalchemy.text("INSERT INTO storyboards (status) VALUES ('pending') RETURNING id")
            result = conn.execute(storyboard_insert)
            storyboard_id = result.fetchone()[0]
            
            # Insert each scene
            scenes_to_insert = []
            for key, script in scenes_data.items():
                if key.startswith('scene_'):
                    scene_number = int(key.split('_')[1])
                    scenes_to_insert.append({
                        "storyboard_id": storyboard_id,
                        "scene_number": scene_number,
                        "script": script,
                        "style": "default_style", # Placeholder
                        "status": "pending"
                    })
            
            scene_insert_statement = sqlalchemy.text("""
                INSERT INTO scenes (storyboard_id, scene_number, script, style, status) 
                VALUES (:storyboard_id, :scene_number, :script, :style, :status)
            """)
            conn.execute(scene_insert_statement, scenes_to_insert)
            
            trans.commit()
            
            return jsonify({
                "status": "success",
                "message": f"Storyboard job {storyboard_id} created with {len(scenes_to_insert)} scenes.",
                "storyboard_id": storyboard_id
            }), 201

    except Exception as e:
        print(f"Error creating storyboard job: {e}")
        return jsonify({"status": "error", "message": f"An unexpected error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)), debug=True)