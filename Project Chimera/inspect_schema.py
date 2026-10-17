import sqlite3
import os

db_path = "data/chimera.db"
if not os.path.exists(db_path):
    print("DB not found")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='storyboards'")
    row = cursor.fetchone()
    if row:
        print(row[0])
    else:
        print("Table storyboards not found")
    conn.close()
