import os
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
import sqlite3

JOB_ID = 2
OUTPUT_FILE = f"storyboard_{JOB_ID}.mp4"
FINAL_OUTPUT_DIR = "c:\\Users\\z143d\\OneDrive\\Desktop\\Project Aergia\\Project Chimera\\output"

print(f"🚑 STARTING RESCUE OF JOB {JOB_ID}...")

# 1. Create missing image for Scene 3 (Index 2)
if not os.path.exists("temp_image_2_2.png"):
    print("Creating placeholder for missing Scene 3 image...")
    img = Image.new('RGB', (1024, 576), color='black')
    d = ImageDraw.Draw(img)
    d.text((50,250), "Scene 3: Image Generation Timeout\n(This frame manually rescued)", fill=(255,255,255))
    img.save("temp_image_2_2.png")

# 2. Assemble Clips
clips = []
for i in range(3):
    audio_path = f"temp_audio_{JOB_ID}_{i}.mp3"
    image_path = f"temp_image_{JOB_ID}_{i}.png"
    
    print(f"Processing Scene {i+1}...")
    
    # Audio
    audioclip = AudioFileClip(audio_path)
    
    # Image + Ken Burns
    img_clip = ImageClip(image_path, duration=audioclip.duration)
    
    # Fix for MoviePy 2.0 (The user wants the 'twitch' free version)
    try:
        zoomed_clip = img_clip.resized(lambda t: 1 + 0.05 * (t / audioclip.duration))
    except AttributeError:
        # Fallback if older moviepy installed (unlikely based on logs)
        zoomed_clip = img_clip.resize(lambda t: 1 + 0.05 * (t / audioclip.duration))
        
    zoomed_clip = zoomed_clip.with_position('center')
    
    final_scene_clip = CompositeVideoClip([zoomed_clip], size=(1024, 576))
    final_scene_clip = final_scene_clip.with_audio(audioclip)
    clips.append(final_scene_clip)

# 3. Stitch
print("Stitching...")
final_video = concatenate_videoclips(clips, method="compose")
final_video.write_videofile(OUTPUT_FILE, codec='libx264', audio_codec='aac', fps=24)

# 4. Move to Output
print("Copying to output...")
final_path = os.path.join(FINAL_OUTPUT_DIR, OUTPUT_FILE)
import shutil
shutil.copy(OUTPUT_FILE, final_path)

# 5. Update DB
print("Updating Database...")
db_path = "../../data/chimera.db"
conn = sqlite3.connect(db_path)
conn.execute("UPDATE storyboards SET status='complete', video_url=? WHERE id=?", (f"/static/videos/{OUTPUT_FILE}", JOB_ID))
conn.commit()
conn.close()

print(f"✅ RESCUE COMPLETE. Video at: {final_path}")
