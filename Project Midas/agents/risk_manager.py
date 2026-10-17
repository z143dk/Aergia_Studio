class RiskManager:
    def __init__(self):
        self.max_trade_cost = 25.00 # Hard limit: $25 per trade
        self.account_balance = 100.00
        
    def evaluate_trade(self, ticker, entry_price, contract_price):
        """
        The Gatekeeper. Enforces hard rules for $100 Account.
        """
        cost_per_contract = contract_price * 100
        # Aggressive 30% risk per trade for "Double Up" strategy
        max_position_size = self.account_balance * 0.30 
        
        print(f"[RISK MANAGER] Evaluating {ticker} Call @ ${contract_price} (Total: ${cost_per_contract})...")
        
        # Rule 1: Affordability
        if cost_per_contract > self.account_balance:
             return False, f"REJECTED: Insufficient Funds (${self.account_balance} vs ${cost_per_contract})"

        # Rule 2: Max Allocation
        if cost_per_contract > max_position_size:
            # Exception for Micro-Account: Allow 1 contract if it's < 50% of account
            if cost_per_contract < (self.account_balance * 0.5):
                pass # Allow "Sniper Shot"
            else:
                return False, f"REJECTED: Position Size ${cost_per_contract} > Limit ${max_position_size}"
        
        # Rule 3: Stop Loss Calculation (20% of Premium)
        stop_price = round(contract_price * 0.80, 2)
            
        return True, f"APPROVED. STOP LOSS SET AT ${stop_price} (Premium Value)"

if __name__ == "__main__":
    risk = RiskManager()
    allowed, msg = risk.evaluate_trade("F", 10.50, 0.20) # $20 cost
    print(msg)
    allowed, msg = risk.evaluate_trade("PLTR", 25.00, 0.50) # $50 cost
    print(msg)
