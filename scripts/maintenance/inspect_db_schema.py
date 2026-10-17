import sqlite3
import os

DB_PATH = os.path.join("Project Chimera", "data", "chimera.db")

def inspect_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA table_info(storyboards)")
    columns = c.fetchall()
    print("Columns:")
    for col in columns:
        print(f" - {col[1]}")
    conn.close()

if __name__ == "__main__":
    inspect_db()
