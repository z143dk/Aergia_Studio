import sqlite3
import os

DB_PATH = os.path.abspath("chimera.db")

def check_latest_job():
    if not os.path.exists(DB_PATH):
        print("Database not found.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get latest job
        cursor.execute("SELECT id, status, video_url, error_message FROM storyboards ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        
        if row:
            print(f"Latest Job ID: {row[0]}")
            print(f"Status: {row[1]}")
            print(f"Video URL: {row[2]}")
            print(f"Error Message: {row[3]}")
        else:
            print("No jobs found in database.")
            
        conn.close()

    except Exception as e:
        print(f"Error reading DB: {e}")

if __name__ == "__main__":
    check_latest_job()
