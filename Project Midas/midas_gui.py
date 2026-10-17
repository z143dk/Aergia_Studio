import customtkinter as ctk
import threading
import os
import time
from midas_agent import init_midas, capture_screen, analyze_market, list_available_models

# --- Configuration ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MidasApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Midas - Visual Trading Mentor")
        self.geometry("400x600")
        self.attributes('-topmost', True) # Always on top
        self.resizable(True, True)
        
        # Set Icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "midas.ico")
            self.iconbitmap(icon_path)
        except:
            print("Icon not found, using default.")

        # Initialize Midas Agent
        try:
            init_midas()
            self.agent_ready = True
        except Exception as e:
            print(f"Midas Init Error: {e}")
            self.agent_ready = False
            self.init_error = str(e)

        # Get Available Models (Dynamic)
        valid_models = []
        if self.agent_ready:
            valid_models = list_available_models()
        
        # Fallback if API fails or returns nothing
        if not valid_models:
             valid_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"]

        # --- UI Layout ---
        
        # 1. Header
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(fill="x", padx=10, pady=5)
        
        self.label_title = ctk.CTkLabel(self.header_frame, text="Midas Agent", font=("Roboto", 20, "bold"))
        self.label_title.pack(side="left", padx=10)

        # Model Selector
        # Default to the first one (usually newest due to sort)
        self.model_var = ctk.StringVar(value=valid_models[0])
        self.combo_model = ctk.CTkComboBox(self.header_frame, 
                                         values=valid_models,
                                         width=160,
                                         variable=self.model_var)
        self.combo_model.pack(side="right", padx=5)
        
        # 2. Chat Area (Scrollable)
        self.chat_display = ctk.CTkTextbox(self, width=380, height=400, state="disabled")
        self.chat_display.pack(padx=10, pady=5, fill="both", expand=True)
        
        if self.agent_ready:
            self.append_message("Midas", "I am ready. Point me at your ThinkOrSwim screen and ask a question!")
        else:
            self.append_message("System", f"Initialization Failed: {self.init_error}\nPlease check your .env file for GOOGLE_API_KEY.")

        # 3. Input Area
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(fill="x", padx=10, pady=5)
        
        self.entry_query = ctk.CTkEntry(self.input_frame, placeholder_text="Ask Midas...", width=250)
        self.entry_query.pack(side="left", padx=5, fill="x", expand=True)
        self.entry_query.bind("<Return>", lambda event: self.run_analysis())
        
        self.btn_analyze = ctk.CTkButton(self.input_frame, text="👁️ Capture & Analyze", width=100, command=self.run_analysis)
        self.btn_analyze.pack(side="right", padx=5)
        
        # Log Trade Button
        self.btn_log = ctk.CTkButton(self.input_frame, text="💾 Save Log", width=80, fg_color="green", command=self.save_to_journal)
        self.btn_log.pack(side="right", padx=5)
        
        # Auto-Scan Button (New)
        self.btn_scan = ctk.CTkButton(self.input_frame, text="🔍 Auto-Scan", width=80, fg_color="#D35400", command=self.run_autoscan)
        self.btn_scan.pack(side="right", padx=5)
        
        # Privacy Toggle
        self.privacy_var = ctk.BooleanVar(value=True) # Default to Secure
        self.chk_privacy = ctk.CTkCheckBox(self.input_frame, text="Privacy Mode", variable=self.privacy_var)
        self.chk_privacy.pack(side="right", padx=5)

        # Status Bar
        status_text = "Ready" if self.agent_ready else "Error"
        status_color = "gray" if self.agent_ready else "red"
        self.label_status = ctk.CTkLabel(self, text=status_text, text_color=status_color)
        self.label_status.pack(side="bottom", pady=2)

    def append_message(self, sender, text):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"\n[{sender}]: {text}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def save_to_journal(self):
        """Saves the current chat history to a text file."""
        try:
            content = self.chat_display.get("0.0", "end")
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            filename = "midas_trade_journal.txt"
            
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"\n{'='*30}\n")
                f.write(f"LOG DATE: {timestamp}\n")
                f.write(f"{'='*30}\n")
                f.write(content.strip())
                f.write(f"\n\n")
            
            self.label_status.configure(text=f"Saved to {filename}", text_color="green")
            # Clear status after 3 seconds
            self.after(3000, lambda: self.label_status.configure(text="Ready", text_color="gray"))
            
        except Exception as e:
            self.label_status.configure(text=f"Save Error: {e}", text_color="red")
            print(f"Log Error: {e}")

    def run_autoscan(self):
        """Preset query for Option Hacker analysis."""
        prompt = (
            "Analyze this Option Hacker screen. "
            "Identify the highest probability defined risk swing trade (Vertical/Condor). "
            "Analyze the Greeks (Delta/Theta) and check for Day Trade risks."
        )
        self.entry_query.delete(0, "end")
        self.entry_query.insert(0, prompt)
        self.run_analysis()

    def run_analysis(self):
        if not self.agent_ready:
            self.append_message("System", "Agent is not initialized. Cannot run analysis.")
            return

        query = self.entry_query.get()
        if not query:
            query = "Analyze this screen. What do you see?"
        
        self.append_message("You", query)
        self.entry_query.delete(0, "end")
        
        # Get Privacy State on GUI Thread
        secure_mode = self.privacy_var.get()
        selected_model = self.model_var.get()
        
        self.label_status.configure(text=f"Thinking with {selected_model}...", text_color="yellow")
        
        # Run in thread to not freeze GUI
        threading.Thread(target=self._process_analysis, args=(query, secure_mode, selected_model)).start()

    def _process_analysis(self, query, secure_mode, model_name):
        try:
            img_path = capture_screen(mask_privacy=secure_mode)
            response = analyze_market(img_path, query, model_name=model_name)
            
            # Clean up
            if os.path.exists(img_path):
                os.remove(img_path)
                
            self.append_message("Midas", response)
            self.label_status.configure(text="Ready", text_color="gray")
            
        except Exception as e:
            self.append_message("System", f"Error: {e}")
            self.label_status.configure(text="Error", text_color="red")

if __name__ == "__main__":
    app = MidasApp()
    app.mainloop()
