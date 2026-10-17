import subprocess
import time
import threading
from flask import Flask, request
import logging
import sys
import os

# Ensure we can import from the local package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from schwab_api import auth, config
except ImportError:
    print("Error: Could not import schwab_api. Make sure you are running this script from the Project Midas directory.")
    sys.exit(1)

# Suppress Flask logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
auth_code = None
server_thread = None

@app.route('/')
def handle_redirect():
    global auth_code
    auth_code = request.args.get('code')
    if auth_code:
        return """
        <html>
        <body style="font-family: sans-serif; text-align: center; padding-top: 50px; background-color: #1a1a1a; color: #00ff00;">
            <h1>Authentication Successful!</h1>
            <p>Midas has received the authorization code.</p>
            <p>You can close this window now.</p>
        </body>
        </html>
        """
    else:
        return "Error: No code received.", 400

def run_server():
    app.run(port=8080)

def main():
    global auth_code
    print("\n" + "="*50)
    print("      MIDAS - WEEKLY SCHWAB API RE-CONNECTOR")
    print("="*50)
    
    if not config.APP_KEY or not config.APP_SECRET:
        print("\n[ERROR] SCHWAB_APP_KEY and SCHWAB_APP_SECRET must be set in your .env file.")
        return

    print("\n[INFO] Starting local callback server on port 8080...")
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_server, daemon=True)
    flask_thread.start()
    
    # Give server a moment to start
    time.sleep(1)

    print("[INFO] Generating Authorization URL...")
    # Ensure config points to localhost:8080
    # Note: If your .env REDIRECT_URI is different, this might fail unless you update it or the App Settings on Schwab.
    # Assuming standard localhost setup.
    print(f"[INFO] Configured Redirect URI: {config.REDIRECT_URI}")
    
    auth_url = auth.generate_auth_url()
    print(f"\n[ACTION] Opening browser to: {auth_url}")
    print("Please log in and approve the application.")
    
    try:
        subprocess.Popen(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--profile-directory=Default", auth_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        import webbrowser
        webbrowser.open(auth_url)

    print("\n[WAITING] Listening for callback...")
    print("NOTE: If you see a 'Connection Refused' or 'Site can't be reached' error in your browser:")
    print("      THIS IS NORMAL! Just copy the URL from the address bar (it starts with https://127.0.0.1...)")
    print("      and paste it right here below.")
    print("-" * 60)
    
    # Wait for code in a non-blocking way so we can accept input
    import select
    
    start_time = time.time()
    
    while auth_code is None:
        # Check if user typed something (Manual Fallback)
        if sys.platform != 'win32':
             # Unix non-blocking input check
             dr, dw, de = select.select([sys.stdin], [], [], 0.1)
             if dr:
                 redirected_url = sys.stdin.readline().strip()
                 if "code=" in redirected_url:
                     try:
                        from urllib.parse import urlparse, parse_qs
                        parsed = urlparse(redirected_url)
                        auth_code = parse_qs(parsed.query)['code'][0]
                        print("[MANUAL] Code detected from input.")
                        break
                     except:
                        pass
        else:
             # On Windows this simple select might not work for stdin, 
             # so we just rely on the user hitting Enter if we use msvcrt or similar?
             # For simplicity on Windows we might just timeout and ASK.
             if time.time() - start_time > 60:
                 print("\n[TIMEOUT] Automatic detection timed out.")
                 redirected_url = input("Please paste the full URL from your browser address bar here: ").strip()
                 if "code=" in redirected_url:
                     try:
                        from urllib.parse import urlparse, parse_qs
                        parsed = urlparse(redirected_url)
                        auth_code = parse_qs(parsed.query)['code'][0]
                     except:
                        print("Invalid URL format.")
                 break
        
        if time.time() - start_time > 180: # 3 min global timeout
            print("\n[TIMEOUT] Creating manual fallback...")
            redirected_url = input("Please paste the full URL from your browser address bar here: ").strip()
            if "code=" in redirected_url:
                 try:
                    from urllib.parse import urlparse, parse_qs
                    parsed = urlparse(redirected_url)
                    auth_code = parse_qs(parsed.query)['code'][0]
                 except:
                    print("Invalid URL format.")
            break
            
        time.sleep(1)
        
    print(f"\n[SUCCESS] Authorization Code received!")
    print(f"Code: {auth_code[:15]}...")
    
    print("[INFO] Exchanging code for tokens...")
    try:
        token_data = auth.exchange_code_for_token(auth_code)
        auth.save_tokens(token_data)
        print("\n" + "="*50)
        print("      CONNECTION UPDATED SUCCESSFULLY")
        print("="*50)
        print("Midas is now re-connected for another 7 days.")
    except Exception as e:
        print(f"\n[ERROR] Failed to exchange token: {e}")

if __name__ == "__main__":
    main()
