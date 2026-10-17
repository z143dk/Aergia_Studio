import sqlite3
import os

DB_PATH = os.path.abspath("chimera.db")

def cancel_pending_jobs():
    if not os.path.exists(DB_PATH):
        print("Database not found.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check for pending jobs
        cursor.execute("SELECT id FROM storyboards WHERE status IN ('pending', 'processing')")
        rows = cursor.fetchall()
        
        if not rows:
            print("No pending jobs found.")
            conn.close()
            return

        print(f"Found {len(rows)} pending jobs. Cancelling...")
        
        cursor.execute("UPDATE storyboards SET status = 'cancelled', error_message = 'Cancelled by user request to avoid billing' WHERE status IN ('pending', 'processing')")
        conn.commit()
        print("All pending jobs have been cancelled.")
            
        conn.close()

    except Exception as e:
        print(f"Error updating DB: {e}")

if __name__ == "__main__":
    cancel_pending_jobs()
