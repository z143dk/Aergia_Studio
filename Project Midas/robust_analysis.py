import os
import sys
import glob
import google.generativeai as genai
from dotenv import load_dotenv

# Setup
sys.path.append(os.getcwd())
load_dotenv(".env.local", override=True)
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: No API Key found.")
    sys.exit(1)

genai.configure(api_key=api_key)

# Models to try in order of preference/likelihood of working
MODELS_TO_TRY = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-001",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
    "gemini-1.0-pro-vision", # Older vision model
    "gemini-pro-vision",
    "gemini-2.0-flash-exp", # Retry just in case
]

def analyze_with_fallback():
    # Find latest snapshot
    list_of_files = glob.glob('snap_*.png') 
    if not list_of_files:
        print("No snapshots found.")
        return
    
    latest_file = max(list_of_files, key=os.path.getctime)
    print(f"Analyzing snapshot: {latest_file}")

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

    for model_name in MODELS_TO_TRY:
        print(f"\nAttempting model: {model_name}...")
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content([
                {"mime_type": "image/png", "data": image_bytes},
                prompt
            ])
            print("SUCCESS!")
            print("\n" + "="*20 + "\n")
            print(response.text)
            print("\n" + "="*20 + "\n")
            return
        except Exception as e:
            print(f"Failed with {model_name}: {e}")

    print("\nAll models failed.")

if __name__ == "__main__":
    analyze_with_fallback()
