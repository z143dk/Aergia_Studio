import os
import time
import midas_agent
from datetime import datetime

# --- Market Context from Search (Static for now, but could be dynamic) ---
MARKET_NEWS = """
DATE: December 30, 2025
CONTEXT:
- US Futures: Flat/Slightly Down (S&P -0.1%, Nasdaq -0.1%).
- Catalysts: Fed Minutes releasing later today. Tech profit-taking ongoing (Nvidia -1.3%).
- Gold/Silver: Sharp decline (-4%) from highs.
- Stocks to Watch: DigitalBridge (+34% on buyout rumors), Energy Fuels (+5.3%).
"""

def night_owl_scan():
    # Initialize Agent
    midas_agent.init_midas()
    
    print("🦉 Night Owl: Starting Analysis...")
    
    # 1. Capture Screen (Assuming ToS is open)
    # Give user a moment if running manually
    print("Capturing screen in 5 seconds...")
    time.sleep(5)
    
    img_path = midas_agent.capture_screen(mask_privacy=True)
    print(f"Captured: {img_path}")
    
    # 2. Deep Analysis Prompt
    prompt = f"""
    You are the 'Night Owl' module of Midas.
    
    {MARKET_NEWS}
    
    TASK:
    1.  Analyze the provided CHART/SCREEN for any technical setups (Support/Resistance, Patterns).
    2.  Combine with the Market News above.
    3.  Suggest ONE high-probability trade for tomorrow.
    4.  Estimate Cost:
        *   If Option: Price * 100 * Qty.
        *   If Stock: Price * Qty.
    5.  Required Deposit: Buying Power needed (approx 50% for margin, 100% for cash).
    
    OUTPUT FORMAT:
    *   **Market Sentiment**: (Based on News + Chart)
    *   **The Trade**: (Clear instruction)
    *   **Rationale**: (Why?)
    *   **Est. Cost**: $X
    *   **Min Deposit**: $Y
    """
    
    # 3. Generate
    try:
        response = midas_agent.analyze_market(img_path, prompt, model_name="gemini-2.0-flash")
        
        # 4. Save Report
        report_path = "nightly_analysis.txt"
        with open(report_path, "w", encoding='utf-8') as f:
            f.write(f"--- NIGHT OWL REPORT ({datetime.now().strftime('%Y-%m-%d')}) ---\n")
            f.write(response)
            
        print(f"✅ Analysis Saved to {report_path}")
        return response
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if os.path.exists(img_path):
            os.remove(img_path)

if __name__ == "__main__":
    night_owl_scan()
