import os
import sys
import logging
import time

# Add parent directory to path to find intelligence_router
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from intelligence_router import router, TaskType
except ImportError:
    print("CRITICAL: Intelligence Router not found. Run from Project Aergia root.")
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format='[HERMES] %(message)s')

class HermesBot:
    def __init__(self):
        self.router = router
        self.google_maps_key = os.getenv("GOOGLE_MAPS_API_KEY")
        self.life360_user = os.getenv("LIFE360_USERNAME")
        logging.info("Hermes Messenger Initialized.")
        
        if not self.google_maps_key:
            logging.warning("Google Maps Key missing. Travel alerts disabled.")

    def send_alert(self, category, message):
        """
        Sends a smart alert. Uses LLM to format it nicely if needed.
        """
        logging.info(f"Processing Alert ({category}): {message}")
        
        try:
            formatted_msg = self.router.generate(
                f"Format this alert for a mobile notification (Keep it under 140 chars): {message}", 
                task_type=TaskType.SPEED
            )
        except Exception as e:
            logging.warning(f"Failed to format alert using LLM: {e}. Falling back to raw message.")
            formatted_msg = message
        
        print(f"\n>>> 🔔 HERMES NOTIFICATION [{category}] <<<")
        print(f"{formatted_msg}")
        print(">>> ----------------------------------- <<<\n")

    def check_travel_conditions(self, destination="Home"):
        """
        Placeholder for Life360 + Google Maps Logic
        """
        if not self.google_maps_key:
            return "Cannot check traffic. API Key missing."
        
        # Logic would go here:
        # 1. Get My Location (Life360)
        # 2. Get Route to Destination (Google Maps)
        # 3. Check Weather/Traffic
        return "Traffic checking logic ready to be implemented."

if __name__ == "__main__":
    bot = HermesBot()
    
    # Test Alert
    bot.send_alert("TRADE", "Midas bought 100 shares of SPY at $450. Profit target hit.")
