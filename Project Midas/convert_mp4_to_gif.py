from moviepy import VideoFileClip
import os
import glob

def convert():
    # Look for MP4s in assets or main dir
    mp4s = glob.glob("assets/*.mp4") + glob.glob("*.mp4")
    
    if not mp4s:
        print("❌ No MP4 files found in 'Project Midas' or 'Project Midas/assets'.")
        print("👉 Please drop your video file here and run this script again.")
        return

    source = mp4s[0]
    target = os.path.join("assets", "startup.gif")
    
    print(f"🎬 Found video: {source}")
    print("⏳ Converting to GIF (this might take a minute)...")
    
    try:
        clip = VideoFileClip(source)
        
        # Optimize for Splash Screen (Resize if too big, e.g., width 600px)
        if clip.size[0] > 600:
            clip = clip.resized(width=600)
            
        # Optional: Speed up if it's long? Let's keep 1.0x for now unless requested.
        
        clip.write_gif(target, fps=15) # 15 fps is good for UI
        print(f"✅ Created: {target}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    convert()
