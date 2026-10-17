
import yfinance as yf
import pandas as pd
import pandas_ta as ta # Optional, but we can do manual math to avoid extra deps if needed.
# Let's do manual math to keep dependencies low: pandas is enough.

def get_technical_summary(ticker):
    """
    Performs a 'Quant' analysis on the ticker.
    Returns a dictionary with technical levels and a generated recommendation.
    """
    try:
        # 1. Fetch Data
        df = yf.download(ticker, period="1y", interval="1d", progress=False)
        if df.empty:
            return {"error": "No data found."}
        
        # Ensure Close is 1D Series
        close = df['Close']
        if isinstance(close, pd.DataFrame):
             close = close.iloc[:, 0] # Fix for new yfinance return shape

        current_price = float(close.iloc[-1])
        
        # 2. Moving Averages
        sma_50 = close.rolling(window=50).mean().iloc[-1]
        sma_200 = close.rolling(window=200).mean().iloc[-1]
        
        # 3. RSI (14)
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs)).iloc[-1]
        
        # 4. Fibonacci Retracement (High/Low of last 6 months approx 126 days)
        lookback = 126
        recent_high = float(close.tail(lookback).max())
        recent_low = float(close.tail(lookback).min())
        diff = recent_high - recent_low
        
        fib_levels = {
            "0.0% (High)": recent_high,
            "23.6%": recent_high - 0.236 * diff,
            "38.2%": recent_high - 0.382 * diff,
            "50.0%": recent_high - 0.5 * diff,
            "61.8%": recent_high - 0.618 * diff,
            "100.0% (Low)": recent_low
        }
        
        # 5. Volatility (ATR-ish approximation: High-Low average)
        # We'll simple check average daily range %
        daily_range = (df['High'] - df['Low']) / df['Close']
        if isinstance(daily_range, pd.DataFrame): daily_range = daily_range.iloc[:, 0]
        avg_vol = daily_range.tail(14).mean() * 100 # percentage
        
        # 6. Recommendation Logic (Simple Rule-Based Quant)
        trend = "BULLISH" if current_price > sma_200 else "BEARISH"
        condition = "NEUTRAL"
        
        if rsi > 70: condition = "OVERBOUGHT"
        elif rsi < 30: condition = "OVERSOLD"
        
        # Signal Generation
        signal = "HOLD"
        reason = "Market is choppy."
        
        # Strategies
        # A. Pullback to Value (Bullish Trend + Oversold or Fib Bounce)
        if trend == "BULLISH":
            if rsi < 40:
                signal = "BUY"
                reason = "Bullish Trend + RSI Oversold (Dip Buy)."
            elif abs(current_price - fib_levels["50.0%"]) < (current_price * 0.02):
                signal = "BUY"
                reason = "Price retesting 50% Fib Support."
            elif abs(current_price - fib_levels["61.8%"]) < (current_price * 0.02):
                signal = "BUY"
                reason = "Golden Pocket Retest (61.8% Fib)."
        
        # B. Trend Reversal / Overextension
        elif trend == "BEARISH":
            if rsi > 60:
                signal = "SELL"
                reason = "Bearish Trend + RSI Overbought (Fade)."
            elif current_price < recent_low:
                signal = "SELL"
                reason = "Breakdown below 6-month lows."

        return {
            "ticker": ticker,
            "price": current_price,
            "trend": trend,
            "condition": condition,
            "rsi": rsi,
            "fib_levels": fib_levels,
            "signal": signal,
            "reason": reason,
            "sma_200": sma_200,
            "volatility": avg_vol
        }

    except Exception as e:
        return {"error": str(e)}

def format_quant_response(data):
    """Formats the quant data into a chat-friendly string."""
    if "error" in data:
        return f"Quant Error: {data['error']}"
        
    fib_text = "\n".join([f"   - {k}: ${v:.2f}" for k, v in data['fib_levels'].items() if k in ["38.2%", "50.0%", "61.8%"]])
    
    msg = (
        f"📊 **QUANT ANALYSIS: {data['ticker']}**\n"
        f"Price: ${data['price']:.2f}\n"
        f"Primary Trend: **{data['trend']}** (v. SMA200)\n"
        f"Status: {data['condition']} (RSI: {data['rsi']:.1f})\n\n"
        f"📐 **Fibonacci Levels (6mo):**\n"
        f"{fib_text}\n\n"
        f"🤖 **Recommendation:** **{data['signal']}**\n"
        f"Why: {data['reason']}\n"
    )
    return msg

if __name__ == "__main__":
    # Test
    res = get_technical_summary("AMD")
    print(format_quant_response(res))
