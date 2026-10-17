import pandas as pd
import pandas_ta as ta

class MomentumBreakout:
    """
    Blueprint Section 5: 'Hyper-focused, directional momentum/breakout strategies'
    Goal: High Growth ($100 -> $50k)
    """
    def __init__(self):
        self.min_volume_ratio = 1.2  # 120% of average volume
        self.max_iv_rank = 50.0      # Don't buy expensive options
        self.trend_sma = 20          # Must be above 20 SMA
        
    def evaluate(self, snapshot):
        ticker = snapshot['ticker']
        price = snapshot['current_price']
        df = snapshot['daily_candles']
        vol_ratio = snapshot['volume_avg_ratio']
        raw_iv = snapshot['raw_iv']
        
        print(f"--- Strategy: Evaluating {ticker} for Momentum Breakout ---")
        
        # 1. Data Validation
        if df is None or df.empty:
            return {"action": "WAIT", "reason": "No candle data"}
            
        # 2. Trend Check (SMA 20)
        # Calculate SMA
        sma_20 = df.ta.sma(length=20).iloc[-1] if len(df) >= 20 else 0
        if price < sma_20:
             return {"action": "WAIT", "reason": f"Price ${price} below SMA20 ${sma_20:.2f} (Downtrend)"}
             
        # 3. Momentum Check (Volume)
        if vol_ratio < self.min_volume_ratio:
            return {"action": "WAIT", "reason": f"Volume Ratio {vol_ratio}x < {self.min_volume_ratio}x (Weak Conviction)"}
            
        # 4. Volatility Check (Cheap Options?)
        # For now using raw IV check > 50 as 'expensive' proxy until we have Rank
        if raw_iv > 60.0: # Arbitrary "High" cutoff for Blue Chips
             return {"action": "WAIT", "reason": f"IV {raw_iv}% is too high (Premium Risk)"}
             
        # 5. Signal Generation (The "Sniper Shot")
        # If we passed all filters, it's a GO.
        
        # Target Strike: First Strike OTM or ITM?
        # Blueprint says: "Delta 0.70 Calls" -> Usually slightly ITM
        target_strike = round(price) # Simplified ATM/ITM selection
        
        return {
            "action": "BUY_CALL",
            "ticker": ticker,
            "strike_target": target_strike,
            "expiry_target": "30-45 DTE", # Swing Trade sweet spot
            "confidence": 85.0,
            "reason": f"Breakout! Vol {vol_ratio}x, Price > SMA20, IV {raw_iv}% (Cheap)"
        }

if __name__ == "__main__":
    # Test Stub
    mock_snapshot = {
        "ticker": "TSLA",
        "current_price": 250.00,
        "daily_candles": pd.DataFrame({'close': [240]*19 + [250], 'volume': [100]*19 + [200]}), # Mock Breakout
        "volume_avg_ratio": 2.0,
        "raw_iv": 35.0
    }
    strat = MomentumBreakout()
    print(strat.evaluate(mock_snapshot))
