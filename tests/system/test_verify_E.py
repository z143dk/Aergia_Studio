from intelligence_router import router

print("--- Verification Snippet E ---")
try:
    result = router.plan_and_execute("Create a movie poster concept called 'Aergia Rising' and generate one image.")
    print("GOAL:", result["goal"])
    print("STEPS:")
    for s in result["steps"]:
        print(s["step_id"], s["task_type"], s.get("provider_id"))
    print("Context keys:", result["context"].keys())
except Exception as e:
    print(f"FAILED: {e}")
