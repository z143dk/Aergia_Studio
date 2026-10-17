import os
import shutil
import subprocess

def resolve_shortcut(path):
    cmd = f"powershell -NoProfile -Command \"(New-Object -COM WScript.Shell).CreateShortcut('{path}').TargetPath\""
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if result.returncode == 0:
        return result.stdout.strip()
    return None

def main():
    dest_dir = r"C:\Users\z143d\Desktop\Aergia_Studio\Aergia_Web\static\assets\cinema"
    os.makedirs(dest_dir, exist_ok=True)
    
    # 1. Copy Video
    video_src = r"C:\Users\z143d\Desktop\Pics\clips\Aergia_Cinema.mp4"
    if os.path.exists(video_src):
        print(f"Copying video from {video_src}...")
        shutil.copy2(video_src, os.path.join(dest_dir, "cinema_video.mp4"))
    else:
        print(f"Video source not found: {video_src}")

    # 2. Resolve & Copy Audio
    lnk_path = r"C:\Users\z143d\Recent\Rok Nardin, Frank William - 223.mp3.lnk"
    
    # Try direct copy if user mistakenly pointed to a file but called it lnk (unlikely)
    # But for lnk, we resolve:
    print(f"Resolving shortcut: {lnk_path}")
    audio_src = resolve_shortcut(lnk_path)
    
    if audio_src and os.path.exists(audio_src):
        print(f"Found target: {audio_src}")
        shutil.copy2(audio_src, os.path.join(dest_dir, "cinema_audio.mp3"))
        print("Audio copied.")
    else:
        print(f"Could not resolve or find audio target. Raw result: {audio_src}")

if __name__ == "__main__":
    main()
