import os
import sys
import logging
from typing import Dict, Any
from router.schemas import ProviderMetadata, ProviderCapability, ExecutionMode

logger = logging.getLogger(__name__)

class SchwabProvider:
    """
    Schwab API provider using 'schwab_api' from Project Midas.
    """
    
    def __init__(self):
        self.client = None
        
        # Add Project Midas to path to import schwab_api
        # Aergia_Studio/router/providers/ -> ../../../Project Midas
        current_dir = os.path.dirname(os.path.abspath(__file__))
        midas_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))), "Aergia_Studio", "Project Midas")
        
        # Robust path finding
        if not os.path.exists(midas_dir):
            # Try relative to CWD if running from Aergia_Studio root
            midas_dir = os.path.abspath("Project Midas")
            
        if midas_dir not in sys.path and os.path.exists(midas_dir):
            sys.path.append(midas_dir)
            
        try:
            from schwab_api.client import SchwabClient
            # SchwabClient handles auth internally via token file/playwright
            self.client = SchwabClient()
            logger.info("SchwabClient initialized")
        except ImportError:
            logger.error(f"Could not import schwab_api from {midas_dir}")
        except Exception as e:
            logger.error(f"Schwab init error: {e}")

    def get_metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            name="Charles Schwab (Midas)",
            capabilities=[
                ProviderCapability.FINANCIAL_ANALYSIS,
                ProviderCapability.TRADING
            ],
            execution_mode=ExecutionMode.SYNC,
            max_context=0,
            cost_per_1k_tokens=0.0,
            avg_latency_ms=1000,
            supports_streaming=False,
        )

    def generate(self, prompt: str, system_prompt: str = "", **kwargs) -> Dict[str, Any]:
        if not self.client:
             return {"error": "Schwab client not available"}

        content = "No action taken."
        raw_data = {}
        
        try:
            prompt_lower = prompt.lower()
            
            if "balance" in prompt_lower or "portfolio" in prompt_lower:
                # Similar logic to midas_home.py
                account_hashes = self.client.get_account_numbers()
                summary_lines = []
                total_liq = 0.0
                
                for acct in account_hashes:
                    h = acct.get('hashValue')
                    bal = self.client.get_account_balance(h)
                    val = bal.get('securitiesAccount', {}).get('currentBalances', {}).get('liquidationValue', 0)
                    total_liq += val
                    summary_lines.append(f"Account ..{acct.get('accountNumber', 'xxxx')[-4:]}: ${val:,.2f}")
                
                content = f"Total Liquidation Value: ${total_liq:,.2f}\n" + "\n".join(summary_lines)
                raw_data = account_hashes
            
            elif "quote" in prompt_lower or "price" in prompt_lower:
                # Extract symbol
                words = prompt.split()
                symbol = "SPY" # Default
                for word in words:
                    if word.isupper() and len(word) <= 5 and word not in ["GET", "THE", "FOR", "PRICE", "QUOTE"]:
                        symbol = word
                        break
                
                quote = self.client.quote(symbol)
                # Quote structure varies, simple accessor
                try:
                    price = quote.get(symbol, {}).get('quote', {}).get('lastPrice', 'Unknown')
                    content = f"{symbol} Last Price: ${price}"
                    raw_data = quote
                except:
                   content = f"Could not parse quote for {symbol}"

            else:
                 content = "Schwab Provider: Command not understood. Try 'check portfolio' or 'quote AAPL'."

        except Exception as e:
            logger.error(f"Schwab execution error: {e}")
            content = f"Error executing financial task: {str(e)}"

        return {
            "content": content,
            "provider": "schwab",
            "model": "midas_api",
            "raw": raw_data
        }

    def submit_job(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("Schwab is synchronous")
