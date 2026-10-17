import os
import sys
from dotenv import load_dotenv
from google import genai

# Try loading from Midas .env.local first
midas_local = os.path.join("Project Midas", ".env.local")
load_dotenv(midas_local)
API_KEY = os.getenv("GOOGLE_API_KEY")

# Fallback to .env
if not API_KEY:
    midas_env = os.path.join("Project Midas", ".env")
    load_dotenv(midas_env)
    API_KEY = os.getenv("GOOGLE_API_KEY")

print(f"DEBUG: Checking Key starting with {str(API_KEY)[:4]}...")

if not API_KEY:
    print("STATUS: FAILED - No API Key found")
    sys.exit(1)

try:
    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content(model="gemini-2.0-flash-exp", contents="Hello")
    print("STATUS: SUCCESS")
except Exception as e:
    print(f"STATUS: FAILED - {e}")
