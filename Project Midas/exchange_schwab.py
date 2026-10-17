import sys, os
from urllib.parse import urlparse, parse_qs
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from schwab_api import auth, config

if len(sys.argv) < 2:
    print("Usage: python exchange_schwab.py <redirected_url_or_code>")
    sys.exit(1)

input_val = sys.argv[1].strip()

if "code=" in input_val:
    parsed = urlparse(input_val)
    code = parse_qs(parsed.query).get("code", [input_val])[0]
else:
    code = input_val

print(f"Exchanging code: {code[:15]}...")
try:
    token_data = auth.exchange_code_for_token(code)
    auth.save_tokens(token_data)
    print("\n[SUCCESS] Fresh Schwab tokens retrieved and saved to schwab_tokens.json!")
    print(f"Access token valid for: {token_data.get('expires_in')}s")
    print(f"Refresh token active: {bool(token_data.get('refresh_token'))}")
except Exception as e:
    print(f"\n[ERROR] Token exchange failed: {e}")
