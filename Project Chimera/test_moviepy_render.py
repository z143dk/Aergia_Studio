from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
from PIL import Image, ImageDraw
import os
import numpy as np

# Mock assets
print("Generating mock assets...")
img = Image.new('RGB', (1024, 576), color='red')
img.save("test_img.png")

# Create a silent audio clip (1 second) - MoviePy 2.0 handling
# Since we might not have a real mp3, we'll try to generate one or just use a silent clip object if possible,
# but worker uses AudioFileClip. Let's make a dummy mp3 if we can, or just use a ColorClip as proxy?
# No, we need to test AudioFileClip interaction.
# Let's verify we can import AudioFileClip first.

try:
    # Generate dummy audio using gTTS just to be close to prod
    from gtts import gTTS
    tts = gTTS("This is a test audio.", lang='en')
    tts.save("test_audio.mp3")
    print("Dummy audio created.")
except ImportError:
    print("gTTS not installed, skipping audio test or mocking?")
    # If gTTS fails, we can't test exact pipeline.
    # But user has gTTS.
    pass

try:
    print("Loading clips...")
    audioclip = AudioFileClip("test_audio.mp3")
    print(f"Audio Duration: {audioclip.duration}")
    
    img_clip = ImageClip("test_img.png", duration=audioclip.duration)
    
    # TEST: The Ken Burns Logic
    print("Applying resize...")
    # worker.py logic:
    # zoomed_clip = img_clip.resized(lambda t: 1 + 0.05 * (t / audioclip.duration)) 
    
    try:
        zoomed_clip = img_clip.resized(lambda t: 1 + 0.05 * (t / audioclip.duration))
    except AttributeError:
        print("❌ .resized() attribute missing! Trying .resize()...")
        zoomed_clip = img_clip.resize(lambda t: 1 + 0.05 * (t / audioclip.duration))
        
    zoomed_clip = zoomed_clip.with_position('center')
    
    print("Compositing...")
    final_scene_clip = CompositeVideoClip([zoomed_clip], size=(1024, 576))
    final_scene_clip = final_scene_clip.with_audio(audioclip)
    
    print("Writing video...")
    output_file = "test_render.mp4"
    final_scene_clip.write_videofile(
        output_file, 
        codec='libx264', 
        audio_codec='aac', 
        fps=24, 
        logger=None
    )
    
    if os.path.exists(output_file) and os.path.getsize(output_file) > 1000:
        print(f"✅ Success! File created: {os.path.getsize(output_file)} bytes")
    else:
        print("❌ Failure: File too small or missing.")

except Exception as e:
    print(f"❌ CRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
