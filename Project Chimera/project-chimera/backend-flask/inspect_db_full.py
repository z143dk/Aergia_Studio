import sqlite3
import os
import sys

# Default to CWD if not specified
db_filename = "chimera.db"
if len(sys.argv) > 1:
    db_filename = sys.argv[1]

DB_PATH = os.path.abspath(db_filename)

print(f"--- DB INSPECTION ---")
print(f"Checking DB File: {DB_PATH}")

if not os.path.exists(DB_PATH):
    print(f"❌ ERROR: File does not exist.")
    sys.exit(1)
    
print(f"File Size: {os.path.getsize(DB_PATH)} bytes")

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. List Tables
    print("\n[TABLES]")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for t in tables:
        print(f" - {t[0]}")
        
    # 2. Check storyboards
    if ('storyboards',) in tables:
        print("\n[STORYBOARDS (Last 5)]")
        cursor.execute("SELECT * FROM storyboards ORDER BY id DESC LIMIT 5")
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print(" - Table is empty.")
            
        print("\n[Total Count]")
        cursor.execute("SELECT COUNT(*) FROM storyboards")
        print(f" - {cursor.fetchone()[0]} rows")
    else:
        print("\n❌ Table 'storyboards' NOT found.")

    conn.close()

except Exception as e:
    print(f"❌ SQL Error: {e}")
