from schwab_api.client import SchwabClient
import json

with open("debug_result.txt", "w", encoding='utf-8') as f:
    try:
        client = SchwabClient()
        f.write("Client init success\n")
        
        f.write("Testing get_price_history for SPY...\n")
        try:
            data = client.get_price_history("SPY", period_type="year", period=1, frequency_type="daily", frequency=1)
            f.write("Success History!\n")
            f.write(json.dumps(data, indent=2)[:500] + "\n")
        except Exception as e:
            f.write(f"Failed get_price_history: {e}\n")

        f.write("\nTesting get_quote for SPY...\n")
        try:
            quote = client.get_quote("SPY")
            f.write("Success Quote!\n")
            f.write(json.dumps(quote, indent=2)[:200] + "\n")
        except Exception as e:
            f.write(f"Failed get_quote: {e}\n")

    except Exception as e:
        f.write(f"Client Init Error: {e}\n")
