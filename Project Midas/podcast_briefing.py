import os
import asyncio
import edge_tts
from midas_strategist import MidasStrategist
from morning_briefing import run_briefing

# Configuration
OUTPUT_FILE = "daily_briefing.mp3"
VOICE_DAN = "en-US-ChristopherNeural"
VOICE_EMMA = "en-US-AriaNeural"

async def generate_podcast():
    print("🎙️ Starting Podcast Production...")
    
    # 1. Gather Data
    # Get standard textual briefing first (Balances, Squeezes)
    raw_briefing = run_briefing(output_callback=lambda x: None)
    
    # Get Night Owl Report if exists
    nightly_report = ""
    if os.path.exists("nightly_analysis.txt"):
        with open("nightly_analysis.txt", "r") as f:
            nightly_report = f.read()
            
    # 2. Write Script (Gemini)
    strategist = MidasStrategist()
    prompt = f"""
    DATA:
    {raw_briefing}
    
    NIGHTLY ANALYSIS:
    {nightly_report}
    
    TASK:
    Write a short, energetic podcast script (max 2 minutes) for two hosts: "Dan" (The Analyst) and "Emma" (The Host).
    
    FORMAT:
    Emma: [Intro - Good morning Daniel!]
    Dan: [Market update, specific trade from analysis]
    Emma: [Ask about squeezes or account status]
    Dan: [Details]
    Emma: [Outro]
    
    Make it sound like a real financial show. Use the data provided.
    """
    
    print("Writing Script...")
    script = strategist.ask(prompt, mode="explain") # mode doesn't matter much here, ask handles it
    
    # Clean formatting
    lines = script.split('\n')
    audio_segments = []
    
    print("Generating Audio...")
    
    cnt = 0
    for line in lines:
        line = line.strip()
        if not line: continue
        
        voice = None
        text = ""
        
        if line.startswith("Dan:") or line.startswith("**Dan**:"):
            voice = VOICE_DAN
            text = line.replace("Dan:", "").replace("**Dan**:", "").strip()
        elif line.startswith("Emma:") or line.startswith("**Emma**:"):
            voice = VOICE_EMMA
            text = line.replace("Emma:", "").replace("**Emma**:", "").strip()
            
        if voice and text:
            # Clean text of markdown
            text = text.replace("*", "").replace("#", "")
            
            filename = f"temp_seg_{cnt}.mp3"
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(filename)
            audio_segments.append(filename)
            cnt += 1
            
    # 3. Stitch Files (Simple Concatenation using MoviePy or sequential playback logic)
    # Since we want a single MP3, let's use moviepy audio capabilities
    from moviepy import AudioFileClip, concatenate_audioclips
    
    clips = [AudioFileClip(f) for f in audio_segments]
    final_audio = concatenate_audioclips(clips)
    final_audio.write_audiofile(OUTPUT_FILE, logger=None)
    
    # Cleanup
    for f in audio_segments:
        try:
            os.remove(f)
        except:
            pass
            
    print(f"✅ Podcast Ready: {OUTPUT_FILE}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(generate_podcast())
