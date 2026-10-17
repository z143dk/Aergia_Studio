import customtkinter as ctk
import threading
import os
import time
import requests

# --- Configuration ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green") # Green for "Director's Cut" / "Go"

class HyperionApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Hyperion - AI Movie Director")
        self.geometry("900x600")
        
        # --- Aergia Theme Assets ---
        # Navigate up from Project Hyperion/hyperion_gui.py to Root, then to Assets
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir) # Aergia_Studio
        bg_path = os.path.join(root_dir, "Aergia_Web", "static", "assets", "wallpapers", "The_Opening_Frame.png")
        
        # Background Image
        from PIL import Image
        if os.path.exists(bg_path):
            self.bg_image = ctk.CTkImage(Image.open(bg_path), size=(900, 600))
            self.bg_label = ctk.CTkLabel(self, text="", image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Set Icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "hyperion.ico")
            self.iconbitmap(icon_path)
        except:
            print("Icon not found, using default.")

        # --- UI Layout ---
        
        # 1. Header (Transparent/Dark)
        self.header_frame = ctk.CTkFrame(self, fg_color="#0b1a20", bg_color="transparent")
        self.header_frame.pack(fill="x", padx=10, pady=5)
        
        # Banner Image (Identity)
        banner_path = os.path.join(root_dir, "Aergia_Web", "static", "assets", "banners", "Hyperion_Banner.png")
        if os.path.exists(banner_path):
            self.banner_img = ctk.CTkImage(Image.open(banner_path), size=(210, 80))
            self.banner_label = ctk.CTkLabel(self.header_frame, text="", image=self.banner_img)
            self.banner_label.pack(side="left", padx=10, pady=5)
        
        self.label_title = ctk.CTkLabel(self.header_frame, text="Project Hyperion", font=("Roboto", 24, "bold"), text_color="#00d2d3")
        self.label_title.pack(side="left", padx=10, pady=10)
        
        # Connection Status Indicator
        self.btn_status = ctk.CTkButton(self.header_frame, text="Checking...", width=100, fg_color="#333333", state="disabled")
        self.btn_status.pack(side="right", padx=10)

        # Open Gallery Button
        self.btn_gallery = ctk.CTkButton(self.header_frame, text="📂 Open Gallery", width=120, fg_color="#440044", hover_color="#660066", command=self.open_gallery)
        self.btn_gallery.pack(side="right", padx=10)

        # Status Bar (Pack First at Bottom)
        self.label_status = ctk.CTkLabel(self, text="Director Mode: Ready", text_color="#00d2d3")
        self.label_status.pack(side="bottom", pady=2)

        # 3. Action Bar (Pack Second at Bottom)
        self.action_frame = ctk.CTkFrame(self, fg_color="#0b1a20")
        self.action_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        self.btn_generate = ctk.CTkButton(self.action_frame, text="🎬 Action! (Generate Movie)", width=200, height=40, font=("Roboto", 16, "bold"), command=self.generate_movie, fg_color="#e0af65", hover_color="#c09f55", text_color="black")
        self.btn_generate.pack(pady=5)

        # 2. Main Content Area (Split View)
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Left: Scene Input (Script / Voice)
        self.left_panel = ctk.CTkFrame(self.content_frame, fg_color="#0b1a20")
        self.left_panel.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        self.lbl_script = ctk.CTkLabel(self.left_panel, text="Scene Script / Prompt", font=("Roboto", 16), text_color="#e0af65")
        self.lbl_script.pack(pady=5)
        
        self.txt_script = ctk.CTkTextbox(self.left_panel, height=200, fg_color="#050e11", text_color="white", border_color="#005f60", border_width=1)
        self.txt_script.pack(fill="x", padx=10, pady=5)
        self.txt_script.insert("0.0", "Describe your movie scene here...")
        
        self.btn_voice = ctk.CTkButton(self.left_panel, text="🎤 Dictate Scene", fg_color="#005f60", hover_color="#00d2d3")
        self.btn_voice.pack(pady=10)
        
        # Right: Storyboard / Preview
        self.right_panel = ctk.CTkFrame(self.content_frame, fg_color="#0b1a20")
        self.right_panel.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        self.lbl_board = ctk.CTkLabel(self.right_panel, text="AI Storyboard Preview", font=("Roboto", 16), text_color="#e0af65")
        self.lbl_board.pack(pady=5)
        
        self.preview_box = ctk.CTkLabel(self.right_panel, text="[Video Preview Area]", width=300, height=200, fg_color="black")
        self.preview_box.pack(pady=20)



        # Start Connection Check
        self.backend_url = "http://localhost:5001"
        self.check_backend()

    def check_backend(self):
        threading.Thread(target=self._ping_backend).start()

    def _ping_backend(self):
        try:
            # Simple health check
            response = requests.get(self.backend_url, timeout=2)
            if response.status_code == 200:
                self.after(0, lambda: self.update_status_indicator(True))
            else:
                self.after(0, lambda: self.update_status_indicator(False))
        except:
            self.after(0, lambda: self.update_status_indicator(False))
        
        # Poll again in 3 seconds
        self.after(3000, self.check_backend)

    def update_status_indicator(self, online):
        if online:
            self.btn_status.configure(text="Connected", fg_color="green")
            self.label_status.configure(text="Director Mode: Connected to Chimera Core", text_color="green")
        else:
            self.btn_status.configure(text="Offline", fg_color="red")
            self.label_status.configure(text="Warning: Chimera Backend (Port 8081) not reachable!", text_color="red")

    def open_gallery(self):
        # Update path to match where worker.py actually saves videos
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(root_dir, "Project Chimera", "project-chimera", "backend-flask", "static", "videos")
        
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except OSError:
                pass # Might be permissions or already exists
        
        # Cross-platform opener
        print(f"Opening Gallery at: {output_dir}")
        if os.name == 'nt': # Windows
            os.startfile(output_dir)
        else: # Mac/Linux
            import subprocess
            subprocess.call(['open', output_dir])

    def generate_movie(self):
        script = self.txt_script.get("0.0", "end").strip()
        if not script:
            self.label_status.configure(text="Error: Script is empty!", text_color="red")
            return

        self.label_status.configure(text=f"Sending Job...", text_color="cyan")
        
        # Run in thread to prevent freezing
        threading.Thread(target=self._send_to_chimera, args=(script,)).start()

    def _send_to_chimera(self, script):
        API_URL = f"{self.backend_url}/api/add_storyboard_job"
        API_KEY = "local-dev-key"
        
        self.action_frame.after(0, lambda: self.label_status.configure(text="AI Director is thinking... (Generating Scenes)", text_color="cyan"))
        
        # 1. AI Director Phase
        try:
            from hyperion_director import HyperionDirector
            director = HyperionDirector()
            scenes = director.direct_movie(script)
            
            if not scenes:
                raise Exception("AI Director returned no scenes. Please try a different prompt.")
                
        except Exception as e:
            error_msg = f"Director Error: {e}"
            print(error_msg)
            self.action_frame.after(0, lambda msg=error_msg: self.label_status.configure(text=msg, text_color="red"))
            return

        # 2. Build Payload
        self.action_frame.after(0, lambda: self.label_status.configure(text=f"Sending {len(scenes)} scenes to Production...", text_color="cyan"))
        
        payload = {}
        preview_text = "🎬 New Production Started:\n"
        
        for scene in scenes:
            key = f"scene_{scene['scene_number']}"
            # Format: Script|Prompt
            # Remember worker uses: Script (Voice) | Prompt (Visual)
            # Director returns: script (Audio), prompt (Visual)
            value = f"{scene['script']}|{scene['prompt']}"
            payload[key] = value
            preview_text += f"\n[Scene {scene['scene_number']}]\n{scene['prompt'][:50]}...\n"

        self.action_frame.after(0, lambda: self.append_preview(preview_text))

        headers = {
            "X-API-KEY": API_KEY
        }
        
        try:
            response = requests.post(API_URL, data=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                job_id = data.get("storyboard_id")
                self.action_frame.after(0, lambda: self.label_status.configure(text=f"Success! Job ID: {job_id}", text_color="green"))
                self.action_frame.after(0, lambda: self.append_preview(f"\n✅ Job {job_id} Queued!"))
            else:
                self.action_frame.after(0, lambda: self.label_status.configure(text=f"Error: {response.text}", text_color="red"))
                
        except Exception as e:
            self.action_frame.after(0, lambda: self.label_status.configure(text=f"Connection Failed (Is Chimera Backend running?)", text_color="orange"))
            print(f"API Error: {e}")

    def append_preview(self, text):
        self.preview_box.configure(text=text)

    def show_history_window(self):
        history_window = ctk.CTkToplevel(self)
        history_window.title("Production History")
        history_window.geometry("600x400")
        
        # Bring to front
        history_window.attributes("-topmost", True)
        
        title_lbl = ctk.CTkLabel(history_window, text="Recent Productions", font=("Roboto", 20, "bold"))
        title_lbl.pack(pady=10)
        
        scroll_frame = ctk.CTkScrollableFrame(history_window, width=550, height=300)
        scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self._populate_history(scroll_frame)
        
        refresh_btn = ctk.CTkButton(history_window, text="Refresh List", command=lambda: self._populate_history(scroll_frame))
        refresh_btn.pack(pady=10)

    def _populate_history(self, scroll_frame):
        # Clear existing
        for widget in scroll_frame.winfo_children():
            widget.destroy()
            
        API_URL = f"{self.backend_url}/api/storyboards"
        API_KEY = "local-dev-key"
        headers = {"X-API-KEY": API_KEY}
        
        try:
            response = requests.get(API_URL, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                jobs = data.get("jobs", [])
                
                if not jobs:
                    ctk.CTkLabel(scroll_frame, text="No history found.").pack(pady=20)
                    return
                    
                for job in jobs:
                    job_id = job['id']
                    status = job['status']
                    video_url = job.get('video_url')
                    
                    row = ctk.CTkFrame(scroll_frame, fg_color="#1a1a1a")
                    row.pack(fill="x", pady=2, padx=5)
                    
                    ctk.CTkLabel(row, text=f"#{job_id}", width=50, font=("Roboto", 12, "bold")).pack(side="left", padx=5)
                    
                    status_color = "green" if status == "complete" else "orange" if status == "pending" else "red"
                    ctk.CTkLabel(row, text=status.upper(), width=100, text_color=status_color).pack(side="left", padx=5)
                    
                    if status == "complete" and video_url:
                        ctk.CTkButton(row, text="▶ Play", width=80, height=24, fg_color="green", 
                                      command=lambda u=video_url: self.play_movie(u)).pack(side="right", padx=10, pady=5)
                    else:
                         ctk.CTkLabel(row, text="...", width=80).pack(side="right", padx=10) # Spacer
                         
            else:
                 ctk.CTkLabel(scroll_frame, text=f"Error: {response.text}").pack(pady=20)
                 
        except Exception as e:
            ctk.CTkLabel(scroll_frame, text=f"Connection Failed").pack(pady=20)
            print(f"History Error: {e}") 

    def play_movie(self, video_url):
        import webbrowser
        
        # If relative URL, prepend backend base
        if video_url.startswith("/"):
             video_url = f"{self.backend_url}{video_url}"
             
        print(f"Opening Video: {video_url}")
        webbrowser.open(video_url) 

if __name__ == "__main__":
    app = HyperionApp()
    app.mainloop()
