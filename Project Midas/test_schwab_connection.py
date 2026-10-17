from schwab_api.client import SchwabClient
import json

def test_connection():
    print("Initializing Schwab Client...")
    try:
        client = SchwabClient()
        print("Success! Client initialized.")
        
        print("\nFetching Account Numbers...")
        accounts = client.get_account_numbers()
        print(f"Accounts Retrieved: {len(accounts)}")
        print(json.dumps(accounts, indent=2))
        
    except Exception as e:
        print(f"\nFAILED: {e}")

if __name__ == "__main__":
    test_connection()
