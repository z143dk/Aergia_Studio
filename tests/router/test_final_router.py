from intelligence_router import router

try:
    print("--- Running Final Router Test ---")
    out = router.plan_and_execute("Generate 2 storyboard scenes and one image for scene 1.")
    
    print("\n[GOAL]:", out["goal"])
    print("\n[STEPS]:")
    for s in out["steps"]:
        # Safety: handle case where 'provider_id' might not be in the step record (though planner.py puts it there)
        pid = s.get("provider_id", "UNKNOWN")
        print(f"Step {s['step_id']}: {s['task_type']} -> {pid}")
        
    print("\n--- Test Passed ---")

except Exception as e:
    print(f"❌ Test Failed: {e}")
