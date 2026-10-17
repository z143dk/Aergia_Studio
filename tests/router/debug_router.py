import sys
import os

# Add current directory to path so we can import intelligence_router
sys.path.append(os.getcwd())

from intelligence_router import router, TaskType

print("--- Testing Intelligence Router (DeepSeek V3) ---")
prompt = "Create a 3 scene script about a robot finding a flower."
system_prompt = "You are an AI Movie Director. Create a 3 scene script. Format: Scene X: [Visual] | [Audio]"

try:
    response = router.generate(prompt, task_type=TaskType.CREATIVE, system_prompt=system_prompt)
    print("\n--- RAW RESPONSE FROM ROUTER ---")
    print(response)
    print("--------------------------------")
except Exception as e:
    print(f"Error: {e}")
