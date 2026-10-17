
import pyautogui
import time
import os

print("--- Screen Capture Test ---")
print("1. Open your Trading Platform (ThinkOrSwim / Schwab).")
print("2. Make sure it is visible on the screen.")
print("3. I will take a screenshot in 5 seconds...")

time.sleep(5)

try:
    # Take screenshot
    timestamp = int(time.time())
    filename = f"test_capture_{timestamp}.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    
    print(f"\n[SUCCESS] Saved screenshot to: {os.path.abspath(filename)}")
    print("Please open this image.")
    print("- If you see your trading screen: WE ARE GOOD! (Python bypasses the block)")
    print("- If the window is black/white: The protection is active.")
    
except Exception as e:
    print(f"\n[ERROR] Capture failed: {e}")
