import sys
import json
import base64
import requests
from schwab_api import config

def main():
    if len(sys.argv) < 2:
        print("Usage: python exchange_token.py <full_redirect_url_or_code>")
        return

    redirected_url = sys.argv[1]
    print(f"Processing URL/Code: {redirected_url}")

    # Extract code
    try:
        from urllib.parse import urlparse, parse_qs
        parsed_url = urlparse(redirected_url)
        query_params = parse_qs(parsed_url.query)
        
        if 'code' not in query_params:
             if 'https' not in redirected_url and len(redirected_url) > 20:
                 code = redirected_url
             else:
                print("Error: Could not find 'code' in the URL.")
                return
        else:
            code = query_params['code'][0]
    except Exception as e:
        print(f"Error parsing URL: {e}")
        return
            
    print(f"Auth Code: {code[:10]}...")
    
    # Creds
    app_key = config.APP_KEY.strip()
    app_secret = config.APP_SECRET.strip()
    
    print(f"Using Key: {app_key[:5]}...{app_key[-5:]}")
    print(f"Using Secret: {app_secret[:5]}...{app_secret[-5:]}")

    # Prepare Request
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {base64.b64encode(f"{app_key}:{app_secret}".encode()).decode()}'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'https://127.0.0.1' # Hardcoded to match verified config
    }
    
    print("Sending Token Request (Basic Auth)...")
    try:
        response = requests.post('https://api.schwabapi.com/v1/oauth/token', headers=headers, data=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            token_data = response.json()
            from schwab_api import auth
            auth.save_tokens(token_data)
            print("SUCCESS! Tokens saved.")
        else:
            # Try Body Auth
            print("Trying Body Auth...")
            del headers['Authorization']
            data['client_id'] = app_key
            data['client_secret'] = app_secret
            response = requests.post('https://api.schwabapi.com/v1/oauth/token', headers=headers, data=data)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                token_data = response.json()
                from schwab_api import auth
                auth.save_tokens(token_data)
                print("SUCCESS! Tokens saved (Body Auth).")

    except Exception as e:
        print(f"Exception during request: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
