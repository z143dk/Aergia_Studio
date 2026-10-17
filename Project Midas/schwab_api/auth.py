import base64
import requests
import time
import json
import os
from . import config

def generate_auth_url():
    """
    Generates the URL for the user to log in and approve the app.
    """
    return f"https://api.schwabapi.com/v1/oauth/authorize?client_id={config.APP_KEY}&redirect_uri={config.REDIRECT_URI}"

def exchange_code_for_token(auth_code):
    """
    Exchanges the authorization code for access and refresh tokens.
    """
    # Ensure keys are stripped of whitespace
    app_key = config.APP_KEY.strip()
    app_secret = config.APP_SECRET.strip()
    
    from requests.auth import HTTPBasicAuth
    basic_auth = HTTPBasicAuth(app_key, app_secret)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': config.REDIRECT_URI
    }
    
    print(f"DEBUG: Code being sent: {auth_code}")
    print(f"DEBUG: Redirect URI: {config.REDIRECT_URI}")
    print(f"DEBUG: Key Len: {len(app_key)}, Secret Len: {len(app_secret)}")
    print(f"DEBUG: Key Start: {app_key[:5]}...")
    
    # Log to file for deep debug
    with open('auth_debug_detailed.log', 'w') as f:
        f.write(f"Key: {app_key[:5]}...{app_key[-5:]}\n")
        f.write(f"Secret: {app_secret[:5]}...{app_secret[-5:]}\n")
        f.write(f"Redirect: {config.REDIRECT_URI}\n")

    # Attempt 1: Basic Auth (Standard)
    
    # Attempt 1: Basic Auth (Standard)
    print("DEBUG: Attempting Basic Auth...")
    response = requests.post('https://api.schwabapi.com/v1/oauth/token', auth=basic_auth, headers=headers, data=data)
    
    if response.status_code != 200:
        print(f"DEBUG: Basic Auth Failed: {response.status_code} - {response.text}")
        print("DEBUG: Attempting Body Auth (Fallback)...")
        # Attempt 2: Credentials in Body
        data['client_id'] = app_key
        data['client_secret'] = app_secret
        # Remove Basic Auth header if present (requests.post with auth=... adds it, so we make a new call without auth=)
        response = requests.post('https://api.schwabapi.com/v1/oauth/token', headers=headers, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        error_msg = f"Status: {response.status_code}\nBody: {response.text}"
        print(f"DEBUG: Final Response Status: {response.status_code}")
        print(f"DEBUG: Final Response Body: {response.text}")
        
        # Log to file for persistence
        with open('auth_debug.log', 'w') as f:
            f.write(error_msg)
            
        raise Exception(f"Failed to obtain token: {response.text}")

def save_tokens(token_data):
    """
    Saves the token data to a local file.
    """
    # Add timestamp to help track expiration
    token_data['retrieved_at'] = time.time()
    with open(config.TOKEN_FILE, 'w') as f:
        json.dump(token_data, f)
    print(f"Tokens saved to {config.TOKEN_FILE}")

def load_tokens():
    """
    Loads tokens from the local file.
    """
    if os.path.exists(config.TOKEN_FILE):
        with open(config.TOKEN_FILE, 'r') as f:
            return json.load(f)
    return None

def refresh_access_token():
    """
    Uses the refresh token to get a new access token.
    """
    tokens = load_tokens()
    if not tokens or 'refresh_token' not in tokens:
        raise Exception("No refresh token available.")

    app_key = config.APP_KEY.strip()
    app_secret = config.APP_SECRET.strip()
    
    # Basic Auth
    from requests.auth import HTTPBasicAuth
    basic_auth = HTTPBasicAuth(app_key, app_secret)
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': tokens['refresh_token']
    }
    
    print("DEBUG: Refreshing Access Token...")
    response = requests.post('https://api.schwabapi.com/v1/oauth/token', auth=basic_auth, headers=headers, data=data)
    
    if response.status_code == 200:
        new_data = response.json()
        # Preserve the old refresh token if the new one isn't returned (sometimes it isn't)
        # Usually checking 'refresh_token' in new_data is enough.
        # Merge with old data to keep other fields if needed, but important is to update access_token
        tokens.update(new_data)
        save_tokens(tokens)
        return tokens
    else:
        raise Exception(f"Failed to refresh token: {response.text}")
