import os
import requests
import json
from dotenv import load_dotenv

# Load the .env file we just created
# Load the .env file (looks in current directory or parents)
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY not found in .env")
    exit(1)

print(f"Testing API Key: {api_key[:10]}...{api_key[-5:]}")

# URL for Gemini 1.5 Flash (Fast & Cheap for testing)
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

headers = {
    'Content-Type': 'application/json'
}

data = {
    "contents": [{
        "parts": [{"text": "Hello! I am verifying my API key. Are you working? Please reply with 'SYSTEM ONLINE'."}]
    }]
}

try:
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        try:
            answer = result['candidates'][0]['content']['parts'][0]['text']
            print("\n--- SUCCESS ---")
            print(f"Model Response: {answer}")
            print("----------------")
        except KeyError:
            print("\n--- ERROR PARSING RESPONSE ---")
            print(json.dumps(result, indent=2))
    else:
        print(f"\n--- API ERROR: {response.status_code} ---")
        print(response.text)

except Exception as e:
    print(f"\n--- CONNECTION ERROR ---")
    print(str(e))
