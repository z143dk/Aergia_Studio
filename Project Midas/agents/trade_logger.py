import json
import os
from datetime import datetime

class TradeLogger:
    def __init__(self, log_file="trade_history.json"):
        # Log saved in Project Midas root
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.log_path = os.path.join(base_dir, log_file)
        self._ensure_log_exists()

    def _ensure_log_exists(self):
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w') as f:
                json.dump([], f)

    def log_trade_attempt(self, ticker, signal_data, risk_data, researcher_data, execution_status):
        """
        Logs a full cycle attempt, whether successful or rejected.
        """
        entry = {
            "id": f"{ticker}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "ticker": ticker,
            "analyst_signal": signal_data,
            "risk_evaluation": risk_data,
            "researcher_debate": researcher_data,
            "execution_status": execution_status,
            "outcome": "PENDING" # To be filled by post-trade analysis
        }
        
        self._append_entry(entry)
        return entry

    def _append_entry(self, entry):
        try:
            with open(self.log_path, 'r') as f:
                history = json.load(f)
            
            history.append(entry)
            
            with open(self.log_path, 'w') as f:
                json.dump(history, f, indent=4)
                
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Trade Logged: {entry['ticker']}")
        except Exception as e:
            print(f"Logging Error: {e}")

    def get_recent_trades(self, limit=5):
        try:
            with open(self.log_path, 'r') as f:
                history = json.load(f)
            return history[-limit:]
        except:
            return []
