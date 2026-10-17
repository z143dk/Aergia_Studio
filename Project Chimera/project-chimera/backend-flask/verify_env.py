import os
from dotenv import load_dotenv
import sys

# Try loading from .env.local
load_dotenv(".env.local")

print("--- Environment Verification ---")
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

print(f"Project ID: {project_id}")
print(f"Credentials: {creds}")

if project_id == "project-chimera-backend" and creds and os.path.exists(creds):
    print("SUCCESS: Environment variables loaded and credentials file exists.")
    sys.exit(0)
else:
    print("FAILURE: Environment variables missing or incorrect.")
    if not os.path.exists(creds) if creds else False:
        print(f"Error: Credentials file not found at {creds}")
    sys.exit(1)
