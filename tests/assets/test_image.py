from intelligence_router import router, TaskType
import os

print("--- Sending Image Gen Request ---")
try:
    if not os.getenv("FAL_KEY"):
         print("WARNING: FAL_KEY not found in env. This test is expected to fail or fallback.")
         
    # Generate
    result = router.generate("A cinematic cyberpunk forge, glowing embers, wide shot.", task_type=TaskType.IMAGE_GEN)
    
    print("\n--- Response (URL) ---")
    print(result)

except Exception as e:
    print(f"Error: {e}")
