from intelligence_router import router
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

print("--- Testing Finance Agent Scenario ---")
goal = "Create 3 viral TikTok hooks for a faceless AI finance channel and generate 1 thumbnail image prompt."
print(f"Goal: {goal}")

try:
    # Orchestrate
    out = router.plan_and_execute(goal)
    
    print("\n--- Orchestration Result ---")
    print(f"Goal Achieved: {out['goal']}")
    print("Context Keys (Outputs):", out["context"].keys())
    
    # Print content details
    for step_data in out['steps']:
        print(f"\nStep {step_data['step_id']} ({step_data['task_type']}):")
        content = step_data['content']
        display = content if len(str(content)) < 400 else content[:400] + "..."
        print(f"Output ({step_data['output_key']}): {display}")

except Exception as e:
    print(f"❌ Failed: {e}")
