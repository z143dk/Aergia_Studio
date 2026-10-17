import os
import requests
import json
from dotenv import load_dotenv

# Load Env
load_dotenv()

def check_openrouter():
    print("--- OpenRouter Connectivity Check ---")
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("CRITICAL: OPENROUTER_API_KEY is missing from .env")
        return

    print(f"Key found: {api_key[:10]}...")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://aergia.ai", # Optional, for including your app on openrouter.ai rankings.
        "X-Title": "Project Aergia",
    }
    
    # Check key status & credits
    try:
        auth_resp = requests.get("https://openrouter.ai/api/v1/auth/key", headers={"Authorization": f"Bearer {api_key}"})
        if auth_resp.status_code == 200:
            key_data = auth_resp.json().get("data", {})
            print(f"Key Label: {key_data.get('label')}")
            print(f"Usage: ${key_data.get('usage', 0):.4f} / Limit: {key_data.get('limit')}")
    except Exception:
        pass

    data = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "user", "content": "Say 'System Online' if you can hear me."}
        ]
    }
    
    try:
        print("Sending request to DeepSeek via OpenRouter...")
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"SUCCESS! Response: {content}")
            print("Credit Status: ACTIVE")
        else:
            print(f"FAILURE: Status {response.status_code}")
            print(response.text)
            print("ACTION: You likely need to enable credit on OpenRouter.")
            
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    check_openrouter()
