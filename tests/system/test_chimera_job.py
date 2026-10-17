import sqlite3
import os

DB_PATH = os.path.join("Project Chimera", "data", "chimera.db")

def add_test_job():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables if they don't exist (just in case)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS storyboards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT DEFAULT 'pending',
            video_path TEXT,
            error_message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scenes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            storyboard_id INTEGER,
            scene_number INTEGER,
            script TEXT,
            prompt TEXT,
            FOREIGN KEY(storyboard_id) REFERENCES storyboards(id)
        )
    ''')

    # Insert Job
    cursor.execute("INSERT INTO storyboards (status) VALUES ('pending')")
    storyboard_id = cursor.lastrowid
    
    # Insert Scenes
    scenes = [
        (1, "Welcome to Project Chimera local test.", "A futuristic computer interface with glowing blue lines"),
        (2, "This is a test of the emergency broadcast system.", "A retro TV screen showing static")
    ]
    
    for s in scenes:
        cursor.execute("INSERT INTO scenes (storyboard_id, scene_number, script, prompt) VALUES (?, ?, ?, ?)", 
                       (storyboard_id, s[0], s[1], s[2]))
    
    conn.commit()
    conn.close()
    print(f"Test job submitted with ID: {storyboard_id}")

if __name__ == "__main__":
    add_test_job()
