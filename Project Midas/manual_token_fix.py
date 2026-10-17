from schwab_api import auth
import sys
import os

# Ensure we can import from local package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# The URL provided by the user
redirected_url = "https://127.0.0.1/?code=C0.b2F1dGgyLmJkYy5zY2h3YWIuY29t.B92h8q0oM05isJC7mnDcZfJ9Jsy1DAk6SOCceTgVA3Y%40&session=dcae8443-b309-4113-be8b-70d31f936ad5"

print("Extracting code from URL...")
try:
    from urllib.parse import urlparse, parse_qs
    parsed_url = urlparse(redirected_url)
    query_params = parse_qs(parsed_url.query)
    
    if 'code' in query_params:
        code = query_params['code'][0]
        print(f"Code found: {code}")
        
        print("Exchanging for tokens...")
        token_data = auth.exchange_code_for_token(code)
        auth.save_tokens(token_data)
        print("SUCCESS: Tokens saved manually.")
    else:
        print("Error: No code found in that URL.")

except Exception as e:
    print(f"Error: {e}")
