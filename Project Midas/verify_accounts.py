import json
from schwab_api.client import SchwabClient

try:
    client = SchwabClient()
    print("Fetching account numbers...")
    accounts = client.get_account_numbers()
    print(json.dumps(accounts, indent=2))
    
    for acct in accounts:
        hash_val = acct.get('hashValue')
        print(f"\nFetching balance for hash: {hash_val}")
        balance = client.get_account_balance(hash_val)
        print(json.dumps(balance, indent=2))

except Exception as e:
    print(f"Error: {e}")
