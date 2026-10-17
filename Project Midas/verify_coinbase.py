import os
import logging
from dotenv import load_dotenv
from coinbase.rest import RESTClient

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Load Env
load_dotenv(r"c:\Users\z143d\OneDrive\Desktop\Project Aergia\.env")

def check_balance():
    print("--- Coinbase Connection Check ---")
    
    api_key = os.getenv("COINBASE_API_KEY")
    api_secret = os.getenv("COINBASE_API_SECRET")
    
    if not api_key:
        print("ERROR: COINBASE_API_KEY not found in .env")
        return

    # Handle Newline in Key (Common .env issue)
    api_secret = api_secret.replace("\\n", "\n")
    
    try:
        client = RESTClient(api_key=api_key, api_secret=api_secret)
        # user = client.get_user() # Not available in this SDK version
        # print(f"Connected as User: {user}")
        
        print("\n--- Checking Accounts ---")
        accounts_response = client.get_accounts()
        # The response is an object, try to access accounts
        accounts = accounts_response.accounts
        
        found_funds = False
        for acct in accounts:
            # Debug: Print first account structure
            # print(acct) 
            
            # SDK v1.8 usually returns objects. 
            # Try accessing value directly or as dict
            try:
                bal_obj = acct.available_balance
                # Check consistency
                if hasattr(bal_obj, 'value'):
                    bal = float(bal_obj.value)
                    currency = bal_obj.currency
                elif isinstance(bal_obj, dict):
                    bal = float(bal_obj.get('value', 0))
                    currency = bal_obj.get('currency', 'UNK')
                else:
                    # Fallback for weird objects
                    print(f"Unknown Balance Object: {bal_obj}")
                    continue
                    
                if bal > 0:
                    found_funds = True
                    print(f"💰 {currency}: {bal}")
            except Exception as loop_e:
                print(f"Error parse acct: {loop_e}")
                
        if not found_funds:
            print("Connection Successful, but no non-zero balances found.")
            
    except Exception as e:
        print(f"CRITICAL FAILURE: {e}")

if __name__ == "__main__":
    check_balance()
