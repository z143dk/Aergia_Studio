import os
from dotenv import load_dotenv
from coinbase.rest import RESTClient
import json

# Load env from current directory
load_dotenv()

api_key = os.getenv("COINBASE_API_KEY")
api_secret = os.getenv("COINBASE_API_SECRET")

print(f"API Key present: {bool(api_key)}")
print(f"API Secret present: {bool(api_secret)}")

if not api_key or not api_secret:
    print("❌ Error: Missing COINBASE_API_KEY or COINBASE_API_SECRET in .env")
    exit(1)

try:
    print("Attempting to connect to Coinbase Advanced Trade...")
    client = RESTClient(api_key=api_key, api_secret=api_secret)
    
    # Get Accounts
    print("Fetching accounts...")
    accounts = client.get_accounts()
    
    # print raw for debugging
    # print(json.dumps(accounts, indent=2))
    
    print("\n--- Active Balances ---")
    count = 0
    print(f"Accounts fetched. Type: {type(accounts)}")
    
    # The SDK returns an object, not a dict. 
    # Attempting to convert to dict or access attributes directly.
    # It likely has an 'accounts' attribute which is a list.
    
    count = 0
    # Try accessing .accounts attribute
    if hasattr(accounts, "accounts"):
        acct_list = accounts.accounts
    else:
        # Fallback if it behaves like a dict
        acct_list = accounts.get("accounts", [])

    for acct in acct_list:
        # acct is likely an object too
        # Try object attribute access first, then dict get
        if hasattr(acct, "available_balance"):
             bal_obj = acct.available_balance
             # Check if bal_obj is dict or object
             if isinstance(bal_obj, dict):
                 bal = float(bal_obj.get("value", 0))
             elif hasattr(bal_obj, "value"):
                 bal = float(bal_obj.value)
             else:
                 bal = 0.0
        else:
             bal = float(acct.get("available_balance", {}).get("value", 0))
             
        if hasattr(acct, "currency"):
            currency = acct.currency
        else:
             currency = acct.get("currency")
             
        if bal > 0:
            print(f"[+] {currency}: {bal}")
            count += 1
    
    if count == 0:
        print("[*] No non-zero balances found.")
    else:
        print(f"Found {count} active accounts with balances.")

    # Test Price Check
    print("\n--- Price Check (BTC-USD) ---")
    product = client.get_product("BTC-USD")
    price = getattr(product, "price", None) or (product.get("price") if isinstance(product, dict) else "N/A")
    print(f"BTC Price: ${price}")

    print("\n[SUCCESS] Coinbase API Authentication & Queries Operational!")

except Exception as e:
    print(f"\n[ERROR] CRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
    traceback.print_exc()
