import midas_agent
import os
import sys
import glob

# Ensure we can find the .env
sys.path.append(os.getcwd())

try:
    # Find latest snapshot
    list_of_files = glob.glob('snap_*.png') 
    if not list_of_files:
        print("No snapshots found, capturing new one...")
        latest_file = midas_agent.capture_screen()
    else:
        latest_file = max(list_of_files, key=os.path.getctime)
        print(f"Using latest snapshot: {latest_file}")

    prompt = (
        "Look at the screen. The user is checking a 'paper money' or 'what if' trade from yesterday, Dec 23rd. "
        "No actual real-money trade was placed. "
        "Please look for any 'Simulated Trading', 'Paper Money', or hypothetical trade analysis markers. "
        "IMPORTANT: The user pays $0.55 commission per option contract (buy or sell). Factor this into any P/L calculations. "
        "Analyze the P/L or hypothetical performance shown for yesterday. "
        "If you see a chart, analyze how a trade would have performed based on the price action yesterday."
    )
    
    print("Analyzing for Paper/Simulated context...")
    result = midas_agent.analyze_market(latest_file, prompt)
    print("\nFINAL RESULT:")
    print(result)

except Exception as e:
    print(f"Error: {e}")
