import os
import sys
import logging

# Add parent directory to path to find intelligence_router
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from intelligence_router import router, TaskType
except ImportError:
    print("CRITICAL: Intelligence Router not found. Run from Project Aergia root.")
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format='[HESTIA] %(message)s')

class HestiaHealth:
    def __init__(self):
        self.router = router
        self.epic_id = os.getenv("EPIC_CLIENT_ID")
        logging.info("Hestia Health Dashboard Initialized.")

    def ask_hestia(self, question):
        """
        Chat interface for health questions. uses Gemini (Context) via Router.
        """
        # In future: Get context from FHIR API
        health_context = "[MyChart Context Placeholder: No Labs Loaded]"
        
        system_prompt = (
            "You are Hestia, a compassionate AI Health Assistant. "
            "Answer questions based on the provided Medical Context. "
            "Disclaimer: You are not a doctor."
        )
        
        prompt = f"CONTEXT: {health_context}\nUSER QUESTION: {question}"
        
        return self.router.generate(prompt, task_type=TaskType.CONTEXT, system_prompt=system_prompt)

    def fetch_labs(self):
        """
        Placeholder for Epic FHIR API call
        """
        if not self.epic_id:
            return "Error: No Epic Client ID configured."
        return "Connecting to MyChart... (requires OAuth flow)"

    def scan_homekit(self):
        """
        Scans for Apple HomeKit devices on the local network.
        """
        try:
            import homekit
            logging.info("Scanning for HomeKit devices...")
            # In a real scenario, this involves discovery and pairing.
            # controller = homekit.Controller()
            # devices = controller.discover(10)
            return "HomeKit Scan Complete (See logs for devices)"
        except ImportError:
            return "Error: 'homekit' library not installed."
        except Exception as e:
            return f"HomeKit Error: {e}"

if __name__ == "__main__":
    hestia = HestiaHealth()
    print("\n--- Ask Hestia ---")
    q = input("Question: ")
    if q:
        print(hestia.ask_hestia(q))
