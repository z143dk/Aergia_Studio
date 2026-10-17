import os
import fal_client
from dotenv import load_dotenv

load_dotenv()

def test_fal_direct():
    print("Testing FAL Client Direct Connection...")
    key = os.getenv("FAL_KEY")
    if not key:
        print("Error: FAL_KEY not found in env.")
        return

    print(f"Using Key: {key[:5]}...")
    
    try:
        print("Submitting to fal-ai/minimax-video...")
        # Note: Using 'fal-ai/minimax/video' which is often the robust one, or the one I used 'fal-ai/minimax-video'
        # Let's try the one I put in worker.py first.
        handler = fal_client.submit(
            "fal-ai/minimax-video",
            arguments={
                "prompt": "A cinematic shot of a cyberpunk city, rain, neon lights.",
                "aspect_ratio": "16:9"
            },
        )
        
        print("Job submitted. Waiting for result (this can take 2+ minutes)...")
        result = handler.get() # Blocks until done
        
        print("Result received!")
        print(result)
        
        if result and 'video' in result:
            print(f"Video URL: {result['video']['url']}")
        else:
            print("No video in result.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_fal_direct()
