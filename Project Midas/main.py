import time
import sys
import os
import datetime

# Path Hacking MUST happen before imports
# Path Hacking MUST happen before imports
# Determine paths dynamically based on this file's location
current_file_path = os.path.abspath(__file__)
midas_dir = os.path.dirname(current_file_path) # .../Project Midas
project_root = os.path.dirname(midas_dir)      # .../Aergia_Studio
agents_dir = os.path.join(midas_dir, "agents")

sys.path.append(project_root)
sys.path.append(midas_dir)
sys.path.append(agents_dir)

# Now we can import directly because 'agents' is in path
from strategy_coordinator import StrategyCoordinator

def main():
    print(f"--- Midas 2.0 'Sniper' Started at {datetime.datetime.now()} ---")
    print("Mode: Infinite Loop (60s Interval)")
    
    coordinator = StrategyCoordinator()
    
    try:
        while True:
            current_time = datetime.datetime.now()
            
            # Simple Market Hours Check (9:30 AM - 4:00 PM EST)
            # For now, we run 24/7 for testing/crypto/futures readiness
            # if 9 <= current_time.hour < 16: ...
            
            try:
                print(f"\n[LOOP] Starting Cycle at {current_time.strftime('%H:%M:%S')}")
                coordinator.run_daily_cycle()
            except Exception as e:
                print(f"CRITICAL ERROR in Cycle: {e}")
                # Don't crash the loop, just log and wait
            
            print("[LOOP] Sleeping for 60 seconds...")
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\n--- Midas 2.0 Stopped by User ---")

if __name__ == "__main__":
    main()
