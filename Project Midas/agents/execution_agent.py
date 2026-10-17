import logging
import sys
import os

# Add root to path
# Add root to path
# Dynamic Pathing
current_dir = os.path.dirname(os.path.abspath(__file__))
midas_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(midas_dir)
sys.path.append(project_root)
sys.path.append(midas_dir)

from schwab_api.client import SchwabClient
from coinbase.rest import RESTClient
import uuid

class ExecutionAgent:
    def __init__(self):
        self.role = "Execution Trader"
        
        # 1. Schwab Connection
        try:
            self.client = SchwabClient()
            self.account_hash = self._get_primary_account()
            logging.info("Execution Agent Connected to Schwab.")
        except Exception as e:
            logging.error(f"Execution Agent Failed to Connect (Schwab): {e}")
            self.client = None

        # 2. Coinbase Connection (CDP)
        try:
            api_key = os.getenv("COINBASE_API_KEY")
            api_secret = os.getenv("COINBASE_API_SECRET").replace("\\n", "\n") # Handle env escapes
            
            if api_key and api_secret:
                self.cb_client = RESTClient(api_key=api_key, api_secret=api_secret)
                logging.info("Execution Agent Connected to Coinbase.")
            else:
                self.cb_client = None
                logging.warning("COINBASE_KEY missing in .env")
        except Exception as e:
            logging.error(f"Coinbase Init Error: {try_clean_error(e)}")
            self.cb_client = None

def try_clean_error(e):
    return str(e)

    def _get_primary_account(self):
        """
        Fetches the first available account hash.
        """
        accounts = self.client.get_account_numbers()
        if accounts and len(accounts) > 0:
            return accounts[0]['hashValue']
        raise Exception("No linked accounts found.")

    def execute_order(self, ticker, action, quantity, price, option_symbol=None):
        """
        Places a Limit Order.
        If option_symbol is provided, places an Option Order.
        Otherwise, places an Equity Order (not fully implemented in this snippet).
        """
        logging.info(f"PREPARING ORDER: {action} {quantity}x {ticker} (Opt: {option_symbol}) @ ${price}")
        
        if not self.client:
            # If client is down, we can still simulate Crypto if needed, but let's just warn
            logging.warning("Schwab Client not connected. Equity/Option orders will fail.")

        # --- CRYPTO ROUTING ---
        if ticker in ["BTC", "ETH", "SOL", "DOGE"]:
            if not self.cb_client:
                return {"status": "FAILED", "reason": "Coinbase Client Not Connected"}
            
            logging.info(f"EXECUTING COINBASE ORDER: {action} {quantity} {ticker} @ ${price}")
            product_id = f"{ticker}-USD"
            
            try:
                # Using Market Order for Fill Certainty in MVP
                # Note: Coinbase API uses 'client_order_id' for idempotency
                order_id = str(uuid.uuid4())
                
                if "BUY" in action:
                    # Buy 'quantity' amount of base currency (e.g. 0.001 BTC)
                    order = self.cb_client.market_order_buy(
                        client_order_id=order_id,
                        product_id=product_id,
                        base_size=str(quantity)
                    )
                else:
                    order = self.cb_client.market_order_sell(
                        client_order_id=order_id,
                        product_id=product_id,
                        base_size=str(quantity)
                    )
                
                logging.info(f"COINBASE ORDER SENT: {order}")
                return {"status": "FILLED", "raw": str(order), "source": "Coinbase"}
                
            except Exception as e:
                logging.error(f"Coinbase Order Failed: {e}")
                return {"status": "ERROR", "reason": str(e)}

        # --- SCHWAB OPTION ROUTING ---
        if not option_symbol:
            return {"status": "FAILED", "reason": "Only Option Orders supported for Equity in this MVP"}

        if not self.client:
             return {"status": "FAILED", "reason": "Schwab Client Disconnected"}

        # Construct Schwab Order Payload for Single Leg Option
        instruction = "BUY_TO_OPEN" if "BUY" in action else "SELL_TO_CLOSE"
        
        order_spec = {
            "orderType": "LIMIT",
            "session": "NORMAL",
            "duration": "DAY",
            "orderStrategyType": "SINGLE",
            "price": price,
            "orderLegCollection": [
                {
                    "instruction": instruction,
                    "quantity": quantity,
                    "instrument": {
                        "symbol": option_symbol,
                        "assetType": "OPTION"
                    }
                }
            ]
        }
        
        try:
            result = self.client.place_order(self.account_hash, order_spec)
            logging.info(f"ORDER SUBMITTED: {result}")
            return result
        except Exception as e:
            logging.error(f"ORDER FAILED: {e}")
            return {"status": "ERROR", "reason": str(e)}

if __name__ == "__main__":
    # Test Mode (Requires valid token/account)
    logging.basicConfig(level=logging.INFO)
    try:
        exec_agent = ExecutionAgent()
        # Example Test (Don't run continuously without checks!)
        # exec_agent.execute_order("F", "BUY", 1, 0.05, "F   240119C00012000") 
    except Exception as e:
        print(e)
