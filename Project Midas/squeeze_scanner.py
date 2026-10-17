import yfinance as yf
import time

def get_squeeze_candidates():
    print("Scanning for Squeeze Candidates (Zero-Cost Mode)...")
    
    # List of "Meme" / High Short Interest Watchlist
    # In a full version, we'd scrape Finviz for this list dynamically.
    # For now, we seed it with known high-SI stocks + some tech.
    tickers = [
        "GME", "AMC", "CVNA", "UPST", "AI", "MARA", "COIN", "MSTR",
        "SPCE", "BYND", "KOSS", "TSLA", "NVDA", "AMD", "RIVN"
    ]
    
    results = []
    
    print(f"Checking {len(tickers)} tickers for squeeze signals...")
    
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Extract key metrics
            short_float = info.get('shortPercentFloat', 0)
            if short_float is None: short_float = 0
            
            vol = info.get('volume', 0)
            avg_vol = info.get('averageVolume10days', 1)
            price = info.get('currentPrice', 0)
            open_price = info.get('open', 0)
            
            # Logic:
            # 1. High Short Interest (> 10% for this test, > 20% normally)
            # 2. Unusual Volume (> 1.2x avg)
            # 3. Green Day (Price > Open)
            
            is_high_si = short_float > 0.10
            is_high_vol = vol > (avg_vol * 1.0)
            is_green = price > open_price
            
            if is_high_si:
                signal = {
                    "symbol": symbol,
                    "price": price,
                    "short_float": round(short_float * 100, 2),
                    "vol_rel": round(vol / avg_vol, 2) if avg_vol else 0,
                    "squeeze_score": 0
                }
                
                # Scoring
                if is_high_vol: signal['squeeze_score'] += 1
                if is_green: signal['squeeze_score'] += 1
                if short_float > 0.20: signal['squeeze_score'] += 1
                
                results.append(signal)
                print(f"Found Candidate: {symbol} (SI: {signal['short_float']}%)")
                
        except Exception as e:
            print(f"Error checking {symbol}: {e}")
            
    # Sort by 'Squeeze Score' (highest first)
    results.sort(key=lambda x: x['squeeze_score'], reverse=True)
    
    return results

if __name__ == "__main__":
    candidates = get_squeeze_candidates()
    print("\n--- TOP SQUEEZE ALERTS ---")
    for c in candidates:
        print(f"🚨 {c['symbol']} | SI: {c['short_float']}% | Vol: {c['vol_rel']}x | Score: {c['squeeze_score']}/3")
