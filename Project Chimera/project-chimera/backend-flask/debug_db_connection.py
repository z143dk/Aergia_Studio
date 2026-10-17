import os
import sqlalchemy
import sys

# Replicate logic from app.py
try:
    print(f"__file__: {__file__}")
    abs_file = os.path.abspath(__file__)
    print(f"abs_file: {abs_file}")
    
    # app.py logic:
    # base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    dir1 = os.path.dirname(abs_file)
    print(f"Dir 1 (backend-flask): {dir1}")
    
    dir2 = os.path.dirname(dir1)
    print(f"Dir 2 (project-chimera): {dir2}")
    
    dir3 = os.path.dirname(dir2)
    print(f"Dir 3 (Project Chimera - Root): {dir3}")
    
    base_dir = dir3
    db_path = os.path.join(base_dir, "data", "chimera.db")
    print(f"Calculated DB Path: {db_path}")
    
    if os.path.exists(db_path):
        print("✅ File exists.")
    else:
        print("❌ File does NOT exist.")
        
    print("\nAttempting connection...")
    db_pool = sqlalchemy.create_engine(f"sqlite:///{db_path}")
    with db_pool.connect() as conn:
        print("✅ Connection successful.")
        result = conn.execute(sqlalchemy.text("SELECT count(*) FROM storyboards")).fetchone()
        print(f"✅ Query successful. Count: {result[0]}")

except Exception as e:
    print(f"❌ Error: {e}")
