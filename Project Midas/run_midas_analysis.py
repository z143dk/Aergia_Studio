import midas_agent
import os
import sys

# Ensure we can find the .env
sys.path.append(os.getcwd())

try:
    print("Starting capture...")
    img_path = midas_agent.capture_screen()
    print(f"Captured: {img_path}")
    
    prompt = "Look at the screen. We are looking for the trade performance from yesterday, Dec 23rd. Please analyze the P/L, trade count, or any other relevant metrics shown for that date. If you see an Account Statement or Trade History, summarize the results for yesterday."
    
    print("Analyzing...")
    result = midas_agent.analyze_market(img_path, prompt)
    print("\nFINAL RESULT:")
    print(result)

except Exception as e:
    print(f"Error: {e}")
