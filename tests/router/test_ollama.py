import os
import sys
from dotenv import load_dotenv

# Load env variables from the Aergia directory
load_dotenv()

# Add the current directory to sys.path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from intelligence_router import router, TaskType

def test_ollama_integration():
    print("--- Starting Local Ollama (Edge AI) Integration Check ---")
    
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model = os.getenv("OLLAMA_MODEL", "gemma2:2b")
    
    print(f"Targeting Local Ollama Url: {ollama_url}")
    print(f"Targeting Local Ollama Model: {ollama_model}")
    
    prompt = "State 'OLLAMA SYSTEM ONLINE' in exactly 3 words."
    
    print("\nAttempting to route request through intelligence router using task_type='edge'...")
    try:
        # Route specifically to local agent via the edge task type
        response = router.generate(prompt, task_type="edge")
        print("\n--- SUCCESS! ---")
        print(f"Response: {response}")
        print("----------------")
    except Exception as e:
        print("\n--- ROUTING FAIL / OFFLINE ---")
        print(f"Error detail: {e}")
        print("Note: This is expected if Ollama is not currently running on your local machine.")
        print("Make sure Ollama is open and you have the model loaded (e.g. running 'ollama run gemma2:2b').")

if __name__ == "__main__":
    test_ollama_integration()
