import os
import time
import vertexai
from vertexai.preview.generative_models import GenerativeModel
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
from dotenv import load_dotenv

# Load env variables
load_dotenv(".env.local")

# 1. Setup The Brain (Vertex AI)
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
try:
    if PROJECT_ID:
        vertexai.init(project=PROJECT_ID, location="us-central1")
        model = GenerativeModel("gemini-1.5-flash-001")
    else:
        print("Warning: GOOGLE_CLOUD_PROJECT not set in .env.local")
        model = None
except Exception as e:
    print(f"Vertex AI Init Error: {e}")
    model = None

# 2. Setup The Voice (ElevenLabs)
api_key = os.getenv("ELEVEN_LABS_API_KEY")
client = ElevenLabs(api_key=api_key) if api_key else None

def chat_turn(user_input):
    if not model or not client:
        print("(!) Check functionality: Vertex AI model or ElevenLabs client not initialized.")
        return

    print(f"\nUser: {user_input}")
    
    # --- Step 1: Think (Gemini) ---
    start_time = time.time()
    try:
        response = model.generate_content(
            f"You are a helpful, empathetic AI assistant. Respond conversationally to: {user_input}",
            stream=True # Stream text for faster time-to-first-byte
        )
    except Exception as e:
        print(f"Gemini Error: {e}")
        return
    
    full_text = ""
    print("Agent: ", end="", flush=True)
    
    # We yield text chunks for the voice engine to consume immediately
    def text_stream():
        nonlocal full_text
        for chunk in response:
            try:
                text_chunk = chunk.text
                full_text += text_chunk
                print(text_chunk, end="", flush=True)
                yield text_chunk
            except Exception:
                pass

    # --- Step 2: Speak (ElevenLabs) ---
    # Streaming audio output directly from the text stream
    try:
        # Note: 'convert_as_stream' is hypothetical for the specific 1.50.0 SDK structure
        # The standard way often is client.generate(stream=True)
        # We will use the standard 'generate' with the iterator input.
        
        audio_stream = client.generate(
            text=text_stream(),
            voice="Rachel", 
            model="eleven_monolingual_v1",
            stream=True
        )
        
        # Play it locally
        stream(audio_stream)
        
    except Exception as e:
        print(f"\n[Voice Error]: {e}")
        if "API key" in str(e) or not api_key:
            print("(!) PLEASE ADD VALID ELEVEN_LABS_API_KEY TO .env.local")

    print(f"\n[Latency]: {time.time() - start_time:.2f}s")

if __name__ == "__main__":
    print("--- Conversational Agent Demo ---")
    print("Type 'quit' to exit.")
    while True:
        u_in = input("\nYou: ")
        if u_in.lower() in ['exit', 'quit']:
            break
        chat_turn(u_in)
