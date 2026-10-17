
import os
import requests
import base64
from dotenv import load_dotenv

# Load Env
load_dotenv("/Users/macbookprom213/Desktop/Aergia_Studio/Project Midas/.env")

KEY = os.getenv("SCHWAB_APP_KEY")
SECRET = os.getenv("SCHWAB_APP_SECRET")

print(f"Testing Auth with:")
print(f"Key: {KEY[:5]}... ({len(KEY)} chars)")
print(f"Secret: {SECRET[:5]}... ({len(SECRET)} chars)")

# Construct Basic Auth
creds = f"{KEY}:{SECRET}"
b64_creds = base64.b64encode(creds.encode('ascii')).decode('ascii')

headers = {
    'Authorization': f'Basic {b64_creds}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

data = {
    'grant_type': 'authorization_code',
    'code': 'DUMMY_CODE_FOR_TESTING',
    'redirect_uri': 'https://127.0.0.1'
}

print("\nSending Request...")
try:
    response = requests.post('https://api.schwabapi.com/v1/oauth/token', headers=headers, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 401 and "invalid_client" in response.text:
        print("\nCONCLUSION: Credentials are INVALID (invalid_client).")
    elif "invalid_grant" in response.text:
        print("\nCONCLUSION: Credentials are VALID (invalid_grant expected).")
    else:
        print("\nCONCLUSION: Unknown response.")

except Exception as e:
    print(f"Error: {e}")
