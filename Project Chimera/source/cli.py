import sqlite3
import os
import sys

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "chimera.db")

def init_db():
    """Ensures the DB exists (same as worker.py)."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
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
    conn.commit()
    conn.close()

def add_job():
    print("--- Project Chimera Job Submitter ---")
    print("Enter scenes. Type 'DONE' when finished.")
    
    scenes = []
    scene_num = 1
    
    while True:
        print(f"\n[Scene {scene_num}]")
        script = input("  Script (what is said): ").strip()
        if script.upper() == 'DONE':
            break
        if not script:
            print("  Script cannot be empty.")
            continue
            
        prompt = input("  Visual Prompt (what is seen): ").strip()
        if not prompt:
            print("  Prompt cannot be empty.")
            continue
            
        scenes.append((scene_num, script, prompt))
        scene_num += 1
    
    if not scenes:
        print("No scenes added. Exiting.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create Storyboard
    cursor.execute("INSERT INTO storyboards (status) VALUES ('pending')")
    storyboard_id = cursor.lastrowid
    
    # Create Scenes
    for s in scenes:
        cursor.execute("INSERT INTO scenes (storyboard_id, scene_number, script, prompt) VALUES (?, ?, ?, ?)", 
                       (storyboard_id, s[0], s[1], s[2]))
    
    conn.commit()
    conn.close()
    
    print(f"\nJob submitted! Storyboard ID: {storyboard_id}")
    print(f"Run 'python worker.py' to process it.")

if __name__ == "__main__":
    init_db()
    add_job()
