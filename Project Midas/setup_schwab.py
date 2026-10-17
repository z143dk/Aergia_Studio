import subprocess
import time
from schwab_api import auth, config

def main():
    print("Beginning Schwab API Setup...")
    
    if not config.APP_KEY or not config.APP_SECRET:
        print("Error: SCHWAB_APP_KEY and SCHWAB_APP_SECRET must be set in your .env file.")
        return

    print("\n1. Generating Authorization URL...")
    print(f"Configured Redirect URI: {config.REDIRECT_URI}")
    auth_url = auth.generate_auth_url()
    print(f"URL: {auth_url}")
    
    print("\nOpening browser to authenticate...")
    try:
        subprocess.Popen(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--profile-directory=Default", auth_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        import webbrowser
        webbrowser.open(auth_url)
    
    print("\n2. after logging in and approving the app, you will be redirected to a URL (likely localhost).")
    print("If it fails to load the page (because localhost isn't running a server), that's fine!")
    print("Look at the address bar in your browser.")
    redirected_url = input("Paste the entire full redirected URL here: ").strip()
    
    # Extract code from URL
    # URL format: https://127.0.0.1/?code=...&session=...
    try:
        from urllib.parse import urlparse, parse_qs
        parsed_url = urlparse(redirected_url)
        query_params = parse_qs(parsed_url.query)
        
        if 'code' not in query_params:
             # Try parsing as if it's just the code if user pasted just the code
             if 'https' not in redirected_url and len(redirected_url) > 20:
                 code = redirected_url
             else:
                print("Error: Could not find 'code' in the URL.")
                return
        else:
            code = query_params['code'][0]
            
        print(f"\nAuth Code found: {code[:10]}...")
        
        print("\n3. Exchanging code for tokens...")
        token_data = auth.exchange_code_for_token(code)
        
        print("\n4. Saving tokens...")
        auth.save_tokens(token_data)
        
        print("\nSUCCESS! Schwab API is now authorized.")
        
    except Exception as e:
        print(f"\nERROR: {e}")

if __name__ == "__main__":
    main()
