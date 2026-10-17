import os
import sys
import glob
import time
import google.generativeai as genai
from dotenv import load_dotenv

# Setup to fix path issues
sys.path.append(os.getcwd())
load_dotenv(".env.local", override=True)
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: No API Key found.")
    sys.exit(1)

genai.configure(api_key=api_key)

def one_shot_analysis():
    # Find latest snapshot
    list_of_files = glob.glob('snap_*.png') 
    latest_file = max(list_of_files, key=os.path.getctime)
    print(f"Analyzing snapshot: {latest_file} with gemini-2.0-flash-exp")

    with open(latest_file, "rb") as f:
        image_bytes = f.read()

    prompt = (
        "Look at the screen. The user is checking a 'paper money' or 'what if' trade from yesterday, Dec 23rd. "
        "No actual real-money trade was placed. "
        "Please look for any 'Simulated Trading', 'Paper Money', or hypothetical trade analysis markers. "
        "IMPORTANT: The user pays $0.55 commission per option contract (buy or sell). Factor this into any P/L calculations. "
        "Analyze the P/L or hypothetical performance shown for yesterday. "
        "If you see a chart, analyze how a trade would have performed based on the price action yesterday."
    )

    try:
        # Using the experimental model as it's often smarter, but catching 429s
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content([
            {"mime_type": "image/png", "data": image_bytes},
            prompt
        ])
        print("SUCCESS_OUTPUT_START")
        print(response.text)
        print("SUCCESS_OUTPUT_END")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    one_shot_analysis()
