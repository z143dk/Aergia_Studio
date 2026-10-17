from intelligence_router import router
import json
import logging
import time

# Setup basic logging to see the planner in action
logging.basicConfig(level=logging.INFO)

print("--- Generating 'Aergia Rising' Poster ---")
goal = "Create a movie poster for a sci-fi film called 'Aergia Rising'"
print(f"Goal: {goal}")

start_time = time.time()
try:
    # This triggers the Planner -> Router -> Executor chain
    results = router.plan_and_execute(goal)
    
    print("\n--- Orchestration Complete ---")
    print(f"Total Time: {time.time() - start_time:.2f}s")
    print("Results:")
    for step_id, content in results.items():
        # Truncate long content (like image URLs or scripts) for display
        display_content = content
        if len(str(content)) > 300:
             display_content = content[:300] + "..."
        print(f"Step {step_id}: {display_content}")

except Exception as e:
    print(f"❌ Orchestration Failed: {e}")
