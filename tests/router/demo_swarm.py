import sys
import os

# Ensure root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from intelligence_router import router, TaskType

def main():
    print("🐝 Initializing Aergia Hive Mind Demo...")
    
    goal = "Explain the connection between ancient Greek mythology and modern artificial intelligence concepts."
    print(f"\nUser Goal: {goal}\n")
    
    print("--- Swarm Execution Start ---")
    try:
        # This calls the new HiveMind logic using TaskType.SWARM
        result = router.generate(goal, task_type=TaskType.SWARM)
        
        print("\n--- Final Swarm Output ---")
        print(result)
        print("--------------------------")
        
    except Exception as e:
        print(f"Swarm Error: {e}")

if __name__ == "__main__":
    main()
