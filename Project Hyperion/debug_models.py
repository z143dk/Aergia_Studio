import os
import sys
from dotenv import load_dotenv
from google import genai

# --- Configuration (Copied from Hyperion Director) ---
MIDAS_ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Project Midas", ".env.local")
load_dotenv(MIDAS_ENV_PATH)
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    MIDAS_ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Project Midas", ".env")
    load_dotenv(MIDAS_ENV_PATH)
    API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    load_dotenv()
    API_KEY = os.getenv("GOOGLE_API_KEY")

print(f"DEBUG: Key found: {str(API_KEY)[:5]}...")

try:
    client = genai.Client(api_key=API_KEY)
    print("\n--- Listing Available Models ---")
    try:
        for m in client.models.list():
            print(f"- {m.name}")
    except Exception as e:
        print(f"Error listing models: {e}")
            
    print("\n--- Testing Generation with 'gemini-2.0-flash-exp' ---")
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents="Test."
        )
        print("SUCCESS! 'gemini-2.0-flash-exp' works.")
    except Exception as e:
        print(f"FAILED 'gemini-2.0-flash-exp': {e}")

    print("\n--- Testing Generation with 'gemini-1.5-flash' ---")
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents="Test."
        )
        print("SUCCESS! 'gemini-1.5-flash' works.")
    except Exception as e:
        print(f"FAILED 'gemini-1.5-flash': {e}")
        
except Exception as e:
    print(f"CRITICAL CLIENT ERROR: {e}")
