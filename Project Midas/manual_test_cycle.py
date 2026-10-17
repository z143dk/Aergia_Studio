import sys
import os

# Ensure paths
sys.path.append(r"c:\Users\z143d\OneDrive\Desktop\Project Aergia")
sys.path.append(r"c:\Users\z143d\OneDrive\Desktop\Project Aergia\Project Midas")

from agents.strategy_coordinator import StrategyCoordinator

if __name__ == "__main__":
    print("--- 🧪 MANUAL TEST CYCLE STARTING ---")
    coord = StrategyCoordinator()
    
    # Run the cycle once
    coord.run_daily_cycle()
    
    print("--- 🧪 TEST CYCLE COMPLETE ---")
