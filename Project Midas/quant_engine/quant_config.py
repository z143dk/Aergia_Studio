import os
from dotenv import load_dotenv

# Load main Midas env
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env.local"))

class QuantConfig:
    # --- Execution Keys (Schwab) ---
    SCHWAB_API_KEY = os.getenv("SCHWAB_API_KEY")
    SCHWAB_SECRET = os.getenv("SCHWAB_SECRET")
    
    # --- Intelligence Keys ---
    # DeepSeek via OpenRouter (or local URL)
    DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://openrouter.ai/api/v1") 
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY") 
    
    # Long Cat AI (Video/Avatar)
    LONGCAT_API_KEY = os.getenv("LONGCAT_API_KEY") # User to add this later

    # --- Risk Management (The $100 Account Rules) ---
    ACCOUNT_SIZE = 100.0
    MAX_TRADE_RISK = 25.0   # Never risk more than $25 per trade
    MAX_OPEN_TRADES = 2     # Max 2 trades at once
    MIN_DTE = 14            # Minimum Days to Expiration (No 0DTE!)
    MAX_CONTRACT_PRICE = 0.30 # $0.30 ($30.00) max premium
    
    # --- System ---
    PAPER_MODE = True       # Default to Paper Mode for safety
