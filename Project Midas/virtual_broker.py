import json
import os
import time
from datetime import datetime
from schwab_api.client import SchwabClient

class VirtualBroker:
    def __init__(self, initial_balance=25000.0, state_file="paper_account.json"):
        self.state_file = state_file
        self.client = SchwabClient()
        self.load_state(initial_balance)

    def load_state(self, initial_balance):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                self.account = json.load(f)
        else:
            self.account = {
                "balance": initial_balance,
                "cash": initial_balance,
                "positions": {}, # Symbol -> {qty, avg_price}
                "history": []
            }
            self.save_state()
            
    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.account, f, indent=4)

    def get_live_price(self, symbol):
        # Fetch real-time price from Schwab
        try:
            quote = self.client.get_quote(symbol)
            # Traverse the JSON response. Structure typically:
            # { 'symbol': { 'quote': { 'lastPrice': 123.45, ... } } }
            # But the key might be the symbol string itself.
            if symbol in quote:
                return quote[symbol]['quote']['lastPrice']
            # Sometimes keys are uppercase
            if symbol.upper() in quote:
                return quote[symbol.upper()]['quote']['lastPrice']
            return None
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return None

    def place_order(self, symbol, quantity, action="BUY", order_type="MARKET"):
        """
        Simulate an order execution.
        Action: BUY or SELL
        """
        price = self.get_live_price(symbol)
        if not price:
            print(f"Could not fetch price for {symbol}. Order failed.")
            return False

        cost = price * quantity
        timestamp = datetime.now().isoformat()
        
        # Commission simulation (e.g. 0.65 per contract if it's an option)
        # Assuming symbol represents 1 unit/share for now, but for options symbol usually has specific format
        commission = 0.0 # Simplify for now, or add logic
        
        if action.upper() == "BUY":
            total_cost = cost + commission
            if self.account["cash"] >= total_cost:
                self.account["cash"] -= total_cost
                
                # Update positions
                if symbol not in self.account["positions"]:
                    self.account["positions"][symbol] = {"qty": 0, "avg_price": 0}
                
                pos = self.account["positions"][symbol]
                # Weighted Average Price calculation
                total_value_before = pos["qty"] * pos["avg_price"]
                new_qty = pos["qty"] + quantity
                new_avg = (total_value_before + cost) / new_qty
                
                self.account["positions"][symbol] = {
                    "qty": new_qty,
                    "avg_price": new_avg
                }
                
                print(f"Filled BUY {quantity} {symbol} @ {price}")
            else:
                print("Insufficient Buying Power.")
                return False

        elif action.upper() == "SELL":
            # Check if we have the position
            if symbol in self.account["positions"] and self.account["positions"][symbol]["qty"] >= quantity:
                 revenue = cost - commission
                 self.account["cash"] += revenue
                 
                 self.account["positions"][symbol]["qty"] -= quantity
                 if self.account["positions"][symbol]["qty"] == 0:
                     del self.account["positions"][symbol]
                     
                 print(f"Filled SELL {quantity} {symbol} @ {price}")
            else:
                print("Insufficient Position to Sell.")
                return False

        # Record History
        trade_record = {
            "timestamp": timestamp,
            "symbol": symbol,
            "action": action,
            "quantity": quantity,
            "price": price,
            "commission": commission
        }
        self.account["history"].append(trade_record)
        self.save_state()
        return True

    def get_account_summary(self):
        # Calculate Liquidation Value
        liq_value = self.account["cash"]
        for sym, pos in self.account["positions"].items():
            curr_price = self.get_live_price(sym)
            if curr_price:
                liq_value += pos["qty"] * curr_price
            else:
                # Fallback to last known if live fails? 
                # For now just use cost basis roughly or ignore integration
                liq_value += pos["qty"] * pos["avg_price"] 
        
        return {
            "cash": self.account["cash"],
            "liquidation_value": liq_value,
            "positions": self.account["positions"]
        }

if __name__ == "__main__":
    # Test
    broker = VirtualBroker()
    print("Initial Balance:", broker.get_account_summary())
    # Try a fake trade on a real symbol if possible, or handle error
    # broker.place_order("SPY", 1, "BUY") 
