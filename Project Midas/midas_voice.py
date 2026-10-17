import asyncio
import edge_tts
import pygame
import os
import time
import uuid

# Voice Options:
# en-US-ChristopherNeural (Male, Deep)
VOICE = "en-US-ChristopherNeural"

async def _generate_audio(text, filename):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(filename)

def save_to_file(text, filename):
    """
    Generates audio from text and saves it to the specified filename.
    """
    try:
        asyncio.run(_generate_audio(text, filename))
        return True
    except Exception as e:
        print(f"Error generating audio file: {e}")
        return False

def speak(text):
    """
    Generates audio from text and plays it immediately.
    """
    print(f"[Voice] Midas Speaking: {text[:50]}...")
    
    # Generate unique filename to avoid locking collisions
    unique_file = f"midas_speech_{uuid.uuid4().hex}.mp3"
    
    try:
        # 1. Generate Audio (Async wrapper)
        asyncio.run(_generate_audio(text, unique_file))
        
        # 2. Play Audio
        pygame.mixer.init()
        pygame.mixer.music.load(unique_file)
        pygame.mixer.music.play()
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        # Cleanup
        pygame.mixer.music.unload()
        # Give system a moment to release handle
        time.sleep(0.1) 
        if os.path.exists(unique_file):
            os.remove(unique_file)
        
    except Exception as e:
        print(f"Error in Voice Module: {e}")
        # Attempt emergency cleanup if something failed
        if os.path.exists(unique_file):
            try:
                os.remove(unique_file)
            except:
                pass

if __name__ == "__main__":
    speak("Hello! I am Midas. Your trading assistant is now online and ready to make money.")
