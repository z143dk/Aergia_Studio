import os
import logging
import json
from typing import Dict, Any
from router.schemas import ProviderMetadata, ProviderCapability, ExecutionMode

logger = logging.getLogger(__name__)

class CoinbaseProvider:
    """
    Coinbase Advanced Trade provider.
    Uses CDP API keys for crypto data and trading (Safety: Read-only by default logic).
    """
    
    def __init__(self, api_key: str = None, api_secret: str = None):
        self.api_key = api_key or os.getenv("COINBASE_API_KEY")
        self.api_secret = api_secret or os.getenv("COINBASE_API_SECRET")
        self.client = None
        
        # Lazy import to avoid crash if coinbase-advanced-py is missing
        try:
            from coinbase.rest import RESTClient
            if self.api_key and self.api_secret:
                # Handle CDP key format (organizations/...)
                # The SDK expects the key file or direct string. 
                # If content is a path, it loads it. If string, it uses it.
                # Assuming raw string passed from env.
                
                # IMPORTANT: api_secret might be multiline PEM. 
                # We need to ensure it's handled correctly.
                # For safety, we try-catch the init.
                try:
                    self.client = RESTClient(api_key=self.api_key, api_secret=self.api_secret)
                except Exception as e:
                    logger.error(f"Coinbase client init failed: {e}")
            else:
                logger.warning("Coinbase credentials missing.")
                
        except ImportError:
            logger.error("coinbase library not installed. Run: pip install coinbase-advanced-py")
    
    def get_metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            name="Coinbase (Advanced Trade)",
            capabilities=[
                ProviderCapability.FINANCIAL_ANALYSIS,
                ProviderCapability.TRADING
            ],
            execution_mode=ExecutionMode.SYNC,
            max_context=0,
            cost_per_1k_tokens=0.0,
            avg_latency_ms=500,
            supports_streaming=False,
        )
    
    def generate(self, prompt: str, system_prompt: str = "", **kwargs) -> Dict[str, Any]:
        """
        Execute financial task.
        Prompt analysis (very simple regex/keyword) determines action.
        This is a 'Function Calling' style implementation inside the provider for now.
        """
        if not self.client:
            return {"error": "Coinbase client not available (check keys/dependencies)"}

        content = "No action taken."
        raw_data = {}

        try:
            prompt_lower = prompt.lower()
            
            # Logic: Parse prompt for intent
            if "balance" in prompt_lower or "portfolio" in prompt_lower:
                # Get Accounts
                accounts = self.client.get_accounts()
                # accounts is a ListAccountsResponse object, not dict.
                
                active_accounts = []
                
                # Access .accounts attribute safely
                acct_list = []
                if hasattr(accounts, "accounts"):
                    acct_list = accounts.accounts
                elif isinstance(accounts, dict):
                    acct_list = accounts.get("accounts", [])
                
                for acct in acct_list:
                    # acct is likely an object (Account)
                    val = 0.0
                    curr = "UNKNOWN"
                    
                    # 1. Get Balance Value
                    if hasattr(acct, "available_balance"):
                         bal_obj = acct.available_balance
                         if hasattr(bal_obj, "value"):
                             val = float(bal_obj.value)
                         elif isinstance(bal_obj, dict):
                             val = float(bal_obj.get("value", 0))
                    elif isinstance(acct, dict):
                         val = float(acct.get("available_balance", {}).get("value", 0))
                    
                    # 2. Get Currency
                    if hasattr(acct, "currency"):
                        curr = acct.currency
                    elif isinstance(acct, dict):
                        curr = acct.get("currency")
                        
                    if val > 0:
                        active_accounts.append(f"{curr}: {val}")
                
                if active_accounts:
                    content = "Portfolio Balances:\n" + "\n".join(active_accounts)
                else:
                    content = "Portfolio is empty."
                
                # raw_data = accounts # Cannot serialize object to JSON easily for raw, skip or dict()

            elif "price" in prompt_lower:
                # Extract symbol (e.g., BTC, ETH)
                words = prompt.split()
                symbol = "BTC-USD" # Default
                for word in words:
                    if word.upper() in ["BTC", "ETH", "SOL", "DOGE", "SHIB"]:
                        symbol = f"{word.upper()}-USD"
                        break
                
                product = self.client.get_product(product_id=symbol)
                # product is GetProductResponse object
                
                price = "Unknown"
                if hasattr(product, "price"):
                    price = product.price
                elif isinstance(product, dict):
                    price = product.get("price", "Unknown")
                    
                content = f"Current price of {symbol}: ${price}"
            
            else:
                content = "Coinbase Provider: Command not understood. Try 'check balance' or 'price of BTC'."

        except Exception as e:
            logger.error(f"Coinbase execution error: {e}")
            content = f"Error executing financial task: {str(e)}"

        return {
            "content": content,
            "provider": "coinbase",
            "model": "v3_api",
            "raw": raw_data
        }

    def submit_job(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("Coinbase is synchronous")
