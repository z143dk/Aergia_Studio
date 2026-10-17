import pandas as pd
import sys
import os

# Path Hacking
sys.path.append(r"c:\Users\z143d\OneDrive\Desktop\Project Aergia")
sys.path.append(r"c:\Users\z143d\OneDrive\Desktop\Project Aergia\Project Midas")

from schwab_api.client import SchwabClient

class DataIngestionAgent:
    def __init__(self):
        try:
            self.client = SchwabClient()
        except:
            print("Warning: Schwab Client not initialized in DataIngestionAgent (Live Data Disabled)")
            self.client = None

    def get_market_snapshot(self, ticker):
        """
        Aggregates Price, Volume, and Volatility into a single snapshot.
        """
        print(f"--- Data Ingestion: Fetching Snapshot for {ticker} ---")
        
        snapshot = {
            "ticker": ticker,
            "current_price": 0.0,
            "daily_candles": None, # DataFrame
            "iv_rank": "N/A",
            "volume_avg_ratio": 1.0, # Relative Volume
            "raw_iv": 0.0
        }

        if ticker in ["BTC", "ETH", "SOL", "DOGE"] or ticker.endswith("USDT"):
            return self._get_crypto_snapshot(ticker)

        if not self.client:
            return self._get_mock_snapshot(ticker)

        try:
            # 1. Fetch Price History (Candles)
            # Get 20 days for SMA/Bollinger calc
            history = self.client.get_price_history(ticker, period_type='month', period=1, frequency_type='daily', frequency=1)
            if history and 'candles' in history:
                df = pd.DataFrame(history['candles'])
                # Schwab keys: open, high, low, close, volume, datetime
                # Convert datetime if needed
                snapshot['daily_candles'] = df
                snapshot['current_price'] = df.iloc[-1]['close']
                
                # Calc Volume Ratio (Simulated for now if logic is complex)
                # Last vol / Avg vol last 10 days
                if len(df) > 10:
                    avg_vol = df['volume'].tail(10).mean()
                    curr_vol = df.iloc[-1]['volume']
                    snapshot['volume_avg_ratio'] = round(curr_vol / avg_vol, 2)

            # 2. Fetch Options Chain for Implied Volatility (IV)
            chain = self.client.get_option_chain(ticker, strike_count=1)
            
            # Simple IV Extraction (ATM Proxy)
            extracted_iv = 0.0
            if 'callExpDateMap' in chain:
                first_date = next(iter(chain['callExpDateMap']))
                first_strike = next(iter(chain['callExpDateMap'][first_date]))
                option_data = chain['callExpDateMap'][first_date][first_strike][0]
                extracted_iv = option_data.get('volatility', 0)
            
            snapshot['raw_iv'] = extracted_iv
            # IV Rank would require 52-week IV history, which we don't have yet.
            # We'll use Raw IV for now.
            
            return snapshot

        except Exception as e:
            print(f"Data Fetch Error: {e}")
            return self._get_mock_snapshot(ticker)

    def _get_crypto_snapshot(self, ticker):
        """
        Fetches Crypto Data via Binance Public API.
        """
        import requests
        
        # Normalize symbol
        symbol = ticker + "USDT" if not ticker.endswith("USDT") else ticker
        
        print(f"--- Data Ingestion: Fetching Binance Data for {symbol} ---")
        
        snapshot = {
            "ticker": ticker,
            "current_price": 0.0,
            "daily_candles": None,
            "iv_rank": "HIGH (Crypto)", # Default assumption
            "volume_avg_ratio": 1.0,
            "raw_iv": 80.0 # Placeholder for Crypto IV
        }
        
        try:
            # Binance K-Lines (Candles)
            # [Time, Open, High, Low, Close, Volume, ...]
            url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1d&limit=30"
            resp = requests.get(url)
            
            if resp.status_code == 200:
                data = resp.json()
                columns = ['datetime', 'open', 'high', 'low', 'close', 'volume', 
                           'close_time', 'q_vol', 'trades', 'tbb', 'tbq', 'ignore']
                df = pd.DataFrame(data, columns=columns)
                
                # Type Conversion
                df['close'] = df['close'].astype(float)
                df['open'] = df['open'].astype(float)
                df['high'] = df['high'].astype(float)
                df['low'] = df['low'].astype(float)
                df['volume'] = df['volume'].astype(float)
                
                snapshot['daily_candles'] = df
                snapshot['current_price'] = df.iloc[-1]['close']
                
                # Volume Logic
                if len(df) > 10:
                    avg_vol = df['volume'].tail(10).mean()
                    curr_vol = df.iloc[-1]['volume']
                    snapshot['volume_avg_ratio'] = round(curr_vol / avg_vol, 2)
                    
            return snapshot
            
        except Exception as e:
            print(f"Binance Error: {e}")
            return self._get_mock_snapshot(ticker)

    def _get_mock_snapshot(self, ticker):
        """
        Fallback for testing without API limits.
        """
        return {
            "ticker": ticker,
            "current_price": 100.00,
            "daily_candles": pd.DataFrame(),
            "iv_rank": "LOW (Simulated)",
            "volume_avg_ratio": 1.5,
            "raw_iv": 25.0
        }

if __name__ == "__main__":
    agent = DataIngestionAgent()
    data = agent.get_market_snapshot("F")
    print("\nSnapshot Summary:")
    print(f"Price: {data['current_price']}")
    print(f"Volume Ratio: {data['volume_avg_ratio']}")
    print(f"IV: {data['raw_iv']}")
