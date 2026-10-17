import os
import time
import pyautogui
import base64
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables (local first/override)
load_dotenv(".env.local", override=True)
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

# Global Client
CLIENT = None
MODEL_NAME = "gemini-1.5-flash"

def init_midas():
    global CLIENT
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env")
    CLIENT = genai.Client(api_key=api_key)
    print("Midas Agent Initialized (New SDK)")

def list_available_models():
    """Fetches list of models that support content generation."""
    try:
        global CLIENT
        if not CLIENT:
            return []
        
        models = []
        # New SDK listing
        for m in CLIENT.models.list():
            if 'generateContent' in m.supported_generation_methods:
                name = m.name.replace("models/", "")
                if 'gemini' in name.lower() and 'robotics' not in name.lower():
                    models.append(name)
        
        # Smart Sort
        def sort_key(name):
            if "flash" in name and "exp" not in name: return 0
            if "pro" in name and "exp" not in name: return 1
            if "flash" in name: return 2
            return 3
            
        return sorted(models, key=sort_key)
    except Exception as e:
        print(f"Error listing models: {e}")
        return []

from PIL import Image, ImageDraw

def capture_screen(mask_privacy=False):
    print("Capturing screen...")
    try:
        screenshot = pyautogui.screenshot()
    except Exception as e:
        print(f"Screen Capture Error: {e}")
        # Mac Fallback Hint
        if sys.platform == 'darwin':
            print("MAC PERMISSION ERROR: Go to System Settings > Privacy & Security > Screen Recording and allow your Terminal/IDE.")
        raise e
    
    if mask_privacy:
        # Redact Top 80 Pixels (ThinkOrSwim Header with Account Info)
        draw = ImageDraw.Draw(screenshot)
        width, height = screenshot.size
        # Draw black box across top
        draw.rectangle([0, 0, width, 80], fill="black")
        print("Privacy Mask Applied: Account Header Redacted.")

    timestamp = int(time.time())
    # Use absolute path to avoid CWD confusion
    save_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(save_dir, f"snap_{timestamp}.png")
    screenshot.save(path)
    return path

def get_system_prompt():
    """Loads system prompt from external text file if available."""
    try:
        prompt_path = os.path.join(os.path.dirname(__file__), "midas_public_prompt.txt")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r") as f:
                return f.read()
    except Exception as e:
        print(f"Warning: Could not load external prompt: {e}")
    
    # Fallback Prompt
    return """
    You are 'Midas', an elite Options Trading Architect integrated with ThinkOrSwim.
    
    CORE OBJECTIVES:
    1.  **Analyze Balance**: If asked, look at the top header (Account Info). Extract "Net Liq" and "Day Trades Left" (if visible).
    2.  **Analyze Scans (Option Hacker)**:
        *   Identify the "Highest Probability" setup. Look for High IV Rank, defined risk (Vertical Spreads/Iron Condors), and Liquid strikes.
        *   **Swing Criteria**: Delta ~0.30, Theta positive (selling premium) or low decay (buying deep ITM).
    3.  **Execute (Instruction)**: provide precise entry instructions.
        *   Format: "ACTION [Buy/Sell] [Qty] [Symbol] [Expiration] [Strike] [Type] @ [Limit Price]"
    4.  **Risk Management (CRITICAL)**:
        *   **PDT Rule**: Check if user has < $25k. If so, WARN if this is a Day Trade.
        *   **Size**: Never risk > 2-5% of Net Liq per trade.
        *   **Greeks**: Recommend trades with Edge. (e.g. Sell High IV).

    OUTPUT FORMAT:
    *   **Observation**: "I see the Option Hacker results..."
    *   **Analysis**: "The best setup is XYZ because..."
    *   **The Trade**: (Bold logic)
    *   **Greeks**: "Delta: X, Theta: Y"
    *   **PDT Status**: "Monitor this trade."
    """

def analyze_market(image_path, prompt, model_name=None):
    global CLIENT
    if not CLIENT:
         raise ValueError("Client not initialized")
    
    # Use provided model or fall back to default global
    target_model = model_name if model_name else MODEL_NAME
    print(f"Using Model: {target_model}")

    system_instruction = get_system_prompt()
    
    # Read image bytes
    with open(image_path, "rb") as f:
        image_bytes = f.read()
        
    print("Midas is thinking...")
    start = time.time()
    
    try:
        # New SDK Generation call
        response = CLIENT.models.generate_content(
            model=target_model,
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
                prompt
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.4,
                top_p=1.0,
                max_output_tokens=2048
            )
        )

        print("\n--- MIDAS ANALYSIS ---")
        print(response.text)
        print("\n----------------------")
        print(f"(Latency: {time.time() - start:.2f}s)")
        
        return response.text
        
    except Exception as e:
        error_str = str(e)
        if "429" in error_str and target_model != "gemini-1.5-flash":
            print(f"Quota exceeded on {target_model}. Retrying with 'gemini-1.5-flash'...")
            try:
                response = CLIENT.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[
                        types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
                        prompt
                    ],
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.4,
                        max_output_tokens=2048
                    )
                )
                print("\n--- MIDAS ANALYSIS (Fallback) ---")
                print(response.text)
                return response.text
            except Exception as e2:
                print(f"Fallback Failed: {e2}")
                return str(e2)
        else:
            print(f"Analysis Failed: {e}")
            return str(e)

def main():
    try:
        init_midas()
        print("\n--- Project Midas: Visual Agent ---")
        print("Point your screen at text, charts, or option chains.")
        
        while True:
            query = input("\nAsk Midas (or 'q' to quit): ")
            if query.lower() in ['q', 'quit', 'exit']:
                break
            
            # 1. Capture
            img_path = capture_screen()
            
            # 2. Analyze
            try:
                analyze_market(img_path, query)
            except Exception as e:
                print(f"Analysis Failed: {e}")
            
            # Cleanup
            if os.path.exists(img_path):
                os.remove(img_path)

    except Exception as e:
        print(f"Critical Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
