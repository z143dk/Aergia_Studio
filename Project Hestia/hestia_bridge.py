import os
import json
from datetime import datetime

class HestiaBridge:
    """
    The entry point for Project Hestia. 
    Handles data sync from iPhone/iPad (Health/HomeKit) to the Aergia PC.
    """
    def __init__(self, sync_folder=r"C:\Users\z143d\Desktop\Aergia_Studio\Hestia_Sync"):
        self.sync_folder = sync_folder
        if not os.path.exists(self.sync_folder):
            os.makedirs(self.sync_folder)

    def log_health_data(self, data_type, value):
        """Logs incoming health data from mobile shortcuts/apps."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {"timestamp": timestamp, "type": data_type, "value": value}
        
        file_path = os.path.join(self.sync_folder, "health_log.json")
        
        # Append to log
        logs = []
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    logs = json.load(f)
            except json.JSONDecodeError:
                pass # Start fresh if corrupt
        
        logs.append(entry)
        with open(file_path, 'w') as f:
            json.dump(logs, f, indent=4)
        
        print(f"🏠 Hestia: Logged {data_type} - {value}")

if __name__ == "__main__":
    hestia = HestiaBridge()
    hestia.log_health_data("Sleep_Hours", 7.5)
