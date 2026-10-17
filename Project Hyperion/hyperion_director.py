
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import time

# --- Configuration ---
# Load API Key from Project Midas (Shared Key)
MIDAS_ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Project Midas", ".env.local")
load_dotenv(MIDAS_ENV_PATH)

API_KEY = os.getenv("GOOGLE_API_KEY")

# 2. Check .env (Fallback)
if not API_KEY:
    MIDAS_ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Project Midas", ".env")
    load_dotenv(MIDAS_ENV_PATH)
    API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    # 3. Last Resort: local .env
    load_dotenv()
    API_KEY = os.getenv("GOOGLE_API_KEY")

class HyperionDirector:
    def __init__(self):
        if not API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in Project Midas/.env.local or environment.")
        
        self.client = genai.Client(api_key=API_KEY)
        self.model_name = "gemini-2.0-flash-exp"
        print(f"🎬 Hyperion Director initialized with {self.model_name} (New SDK)")

    def direct_movie(self, user_concept):
        """
        Takes a user concept and returns a list of scenes (dict with script/prompt).
        """
        system_prompt = self._load_system_prompt()
        full_prompt = f"{system_prompt}\n\nUSER REQUEST: {user_concept}\n\nOUTPUT:"
        
        try:
            # We need to add the parent directory to sys.path to import intelligence_router
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from intelligence_router import router, TaskType
            
            print("🎬 Director: Delegating generation to Intelligence Router...")
            
            # The router handles retries, fallbacks (OpenRouter -> Google), and model selection
            response_text = router.generate(
                prompt=full_prompt,
                task_type=TaskType.CREATIVE,
                system_prompt=system_prompt
            )
            
            if "Error" in response_text and len(response_text) < 100:
                print(f"❌ Director Failed: {response_text}")
                return []
                
            return self._parse_response(response_text)

        except Exception as e:
            print(f"Router Error: {e}")
            import traceback
            traceback.print_exc()
            return []


    def _load_system_prompt(self):
        try:
            prompt_path = os.path.join(os.path.dirname(__file__), "hyperion_public_prompt.txt")
            with open(prompt_path, "r") as f:
                return f.read()
        except:
            return "You are an AI Movie Director. Create a 3 scene script."

    def _parse_response(self, text):
        """
        Parses the text output into a structured list.
        Expected format lines: 'Scene X: [Visual] | [Audio]'
        """
        scenes = []
        lines = text.split('\n')
        scene_count = 1
        
        import re
        for line in lines:
            print(f"DEBUG: Raw Response Length: {len(text)}")
            if len(text) < 500:
                print(f"DEBUG: Raw Response: {text}")

            # Match "Scene X", "**Scene X**", "Simple Header: Scene X", etc.
            # Removed ^ start anchor to handle markdown bullets or reasoning text
            match = re.search(r"\**Scene\s+(\d+)", line.strip(), re.IGNORECASE)
            
            if match:
                parts = line.split(':', 1)
                if len(parts) > 1:
                    content = parts[1].strip()
                    # Remove trailing ** if present (from **Scene 1**: format)
                    content = content.replace("**", "") 
                    
                    # Split Visual | Audio
                    if '|' in content:
                        visual, audio = content.split('|', 1)
                        # We use Visual as Prompt, and Audio (or combined) as Script
                        # Actually worker.py expects: Script | Prompt
                        # Let's make the Script be the Audio/Voiceover description and Prompt be the Visual
                        script = audio.strip()
                        prompt = visual.strip()
                    else:
                        script = content
                        prompt = content
                    
                    scenes.append({
                        "scene_number": int(match.group(1)),
                        "script": script,
                        "prompt": prompt
                    })
        return scenes

if __name__ == "__main__":
    # Test
    print("🎬 Hyperion Director: Initializing...")
    try:
        director = HyperionDirector()
        print("🎬 Action! Directing 'A cyberpunk detective in the rain'...")
        scenes = director.direct_movie("A cyberpunk detective in the rain")
        
        for scene in scenes:
            print(f"Scene {scene['scene_number']}:")
            print(f"  Prompt: {scene['prompt']}")
            print(f"  Script: {scene['script']}")
            print("-" * 20)
            
    except Exception as e:
        print(f"Error: {e}")
