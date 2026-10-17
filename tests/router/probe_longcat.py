import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LONGCAT_API_KEY")

# Revised URL based on search result [1]
BASE_URL = "https://api.longcat.chat/openai/v1"

def probe():
    print(f"🕵️ Probing LongCat (OpenAI Path) at {BASE_URL}...")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        print("\n--- GET /models ---")
        res = requests.get(f"{BASE_URL}/models", headers=headers, timeout=10)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text[:300]}")
    except Exception as e:
        print(f"Models Failed: {e}")

if __name__ == "__main__":
    probe()
