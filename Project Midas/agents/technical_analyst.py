import sys
import os
import logging
import json
import pandas as pd
import pandas_ta as ta

# Add root to path
# Dynamic Pathing
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
midas_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(midas_dir)
sys.path.append(project_root)
sys.path.append(midas_dir)

from intelligence_router import router, TaskType
from schwab_api.client import SchwabClient

class TechnicalAnalyst:
    def __init__(self):
        self.role = "Technical Analyst"
        try:
            self.client = SchwabClient()
            logging.info("Technical Analyst Connected to Schwab Data.")
        except:
            self.client = None
            logging.warning("Technical Analyst running in OFFLINE mode.")

    def get_market_data(self, ticker):
        """
        Fetches daily candles and calculates indicators (RSI, MACD) using pandas-ta.
        """
        if not self.client:
            return "Simulated Data: RSI 30, Price $10"
            
        try:
            # Fetch 1 month of daily data
            history = self.client.get_price_history(ticker, period_type='month', period=1, frequency_type='daily')
            candles = history.get('candles', [])
            
            if not candles: 
                return "Error: No data found."
                
            # Create DataFrame
            df = pd.DataFrame(candles)
            # Ensure numeric
            df['close'] = pd.to_numeric(df['close'])
            df['high'] = pd.to_numeric(df['high'])
            df['low'] = pd.to_numeric(df['low'])
            df['open'] = pd.to_numeric(df['open'])
            df['volume'] = pd.to_numeric(df['volume'])
            
            # Calculate Indicators
            # RSI (14)
            df.ta.rsi(length=14, append=True)
            # MACD (12, 26, 9)
            df.ta.macd(fast=12, slow=26, signal=9, append=True)
            # Bollinger Bands (20, 2)
            df.ta.bbands(length=20, std=2, append=True)
            
            # Get latest complete candle
            latest = df.iloc[-1]
            
            # Formatting for LLM
            # Note: Column names from pandas-ta are specific (e.g., RSI_14, MACD_12_26_9, MACDs_12_26_9)
            rsi = latest.get('RSI_14', 0)
            macd = latest.get('MACD_12_26_9', 0)
            macd_sig = latest.get('MACDs_12_26_9', 0)
            bb_upper = latest.get('BBU_20_2.0', 0)
            bb_lower = latest.get('BBL_20_2.0', 0)
            
            summary = f"**Calculated Indicators (Daily)**:\n"
            summary += f"- RSI(14): {rsi:.2f}\n"
            summary += f"- MACD: {macd:.4f} | Signal: {macd_sig:.4f} (Hist: {latest.get('MACDh_12_26_9', 0):.4f})\n"
            summary += f"- Bollinger: Upper {bb_upper:.2f} | Lower {bb_lower:.2f}\n\n"
            
            summary += "Recent Daily Candles (Open/Close/Vol):\n"
            for index, c in df.tail(5).iterrows():
                 # Use .get with default just in case
                date_val = str(c.get('datetime', 'N/A'))
                # Handle timestamp conversion if needed, but usually Schwab sends epoch or int
                # If it's epoch ms:
                if isinstance(c.get('datetime'), int):
                    date_val = pd.to_datetime(c.get('datetime'), unit='ms').strftime('%Y-%m-%d')
                    
                summary += f"Date: {date_val} | Open: {c['open']} | Close: {c['close']} | Vol: {c['volume']}\n"
                
            return summary
        except Exception as e:
            logging.error(f"Pandas-TA Error: {e}")
            return f"Data Error: {e}"

    
    def get_iv_data(self, ticker):
        """
        Fetches Implied Volatility (IV) from Schwab Option Chain.
        """
        if not self.client:
            return "Simulated IV: 25.0 (Moderate)"
            
        try:
            # Fetch minimal chain to get underlying stats
            chain = self.client.get_option_chain(ticker, strike_count=1)
            
            if 'underlying' in chain:
                 # Schwab often puts 'mark' or 'totalVolume' here. 
                 # 'volatility' might be implicit or mapped. 
                 # Let's check common keys or assume we might need to calc from ATM if missing.
                 # However, Schwab API usually provides 'volatility' or 'variability' in underlying block.
                 # If not, we look at the first option's volatility as a proxy.
                 pass
            
            # Extract IV
            # Strategy: Try to find "volatility" in underlying, else ATM average.
            # Simplified for now: Inspecting 'underlying' map
            und = chain.get('underlying', {})
            # Some APIs use 'annualizedVolatility' or similar
            # If not available directly, we might need a backup
            
            # For this MVP, we will extract what we can or return "N/A"
            # Real Schwab JSON often has "currentDayVolatility" or similar
            # Let's attempt to use a safe getter
            
            # Placeholder until we see real JSON structure in logs:
            # But let's look for callExpDateMap to find ATM option vol
            market_iv = "N/A"
            
            # Fallback: Look at the first option in the chain
            # (Crude approximation but better than nothing for "cheap/expensive" check)
            if 'callExpDateMap' in chain:
                # Digging deep: date -> strike -> [0] -> volatility
                first_date = next(iter(chain['callExpDateMap']))
                first_strike = next(iter(chain['callExpDateMap'][first_date]))
                option_data = chain['callExpDateMap'][first_date][first_strike][0]
                market_iv = option_data.get('volatility', 0)
            
            return f"Implied Volatility (ATM Proxy): {market_iv}"
            
        except Exception as e:
            return f"IV Error: {e}"

    def analyze_ticker(self, ticker):
        """
        Fetches REAL data + INDICATORS + IV and Uses DeepSeek V3 to analyze.
        """
        data_summary = self.get_market_data(ticker)
        iv_summary = self.get_iv_data(ticker)
        
        system_prompt = (
            "You are a sophisticated Technical Analyst for a hedge fund. "
            "Analyze the provided market data (Calculated Indicators + Candles + IV). "
            "1. **Trend**: RSI/MACD/Bollinger. "
            "2. **Volatility (IV)**: Is it Cheap or Expensive? (Low IV = Buy Options, High IV = Sell/Credit Spreads). "
            "   - Note: For $100 account, we mostly BUY options (Debit), so we prefer Low/Medium IV. "
            "3. **Setup**: Reversal vs Breakout. "
            "Output a JSON decision: { 'signal': 'BUY' | 'SELL' | 'WAIT', 'confidence': 0-100, 'reasoning': '...' }"
        )
        
        prompt = f"Ticker: {ticker}\n{data_summary}\n{iv_summary}"
        
        response = router.generate(prompt, task_type=TaskType.CODING, system_prompt=system_prompt)
        return response

if __name__ == "__main__":
    analyst = TechnicalAnalyst()
    print(analyst.analyze_ticker("F"))
