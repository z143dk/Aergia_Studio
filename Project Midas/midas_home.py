import customtkinter as ctk
from PIL import Image, ImageSequence
import threading
import sys
import os

# Ensure Root is in path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import webbrowser
import subprocess
import glob

# Import Midas Modules
from midas_voice import speak
from midas_strategist import MidasStrategist
from squeeze_scanner import get_squeeze_candidates
from midas_notifier import send_alert # Alerts
from midas_notifier import send_alert # Alerts
import midas_agent # For visual scan
from midas_swing import MidasSwingTrader # Swing Logic
from agents.coach import TradingCoach # Trading Coach Logic
from agents.strategy_coordinator import StrategyCoordinator # Auto-Pilot Logic
from virtual_broker import VirtualBroker # Broker logic
from schwab_api.client import SchwabClient # Live Account
from midas_squeeze_tracker import SqueezeTrackerWindow # Tracker UI

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.overrideredirect(True) # No title bar
        
        # Fixed size for splash
        w, h = 600, 400
        self.geometry(f"{w}x{h}")
        
        # Center on screen
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        try:
            self.gif_path = "assets/startup.gif"
            if not os.path.exists(self.gif_path):
                 raise FileNotFoundError("No gif found")
                 
            self.gif_image = Image.open(self.gif_path)
            self.frames = [frame.copy() for frame in ImageSequence.Iterator(self.gif_image)]
            self.frame_index = 0
            
            self.label = ctk.CTkLabel(self, text="")
            self.label.pack(expand=True, fill="both")
            
            self.animate()
            
            # Close after 3 seconds
            self.after(3000, self.finish)
        except Exception as e:
            print(f"Splash Error: {e}")
            self.finish()

    def animate(self):
        try:
            if not self.winfo_exists(): return
            
            frame = self.frames[self.frame_index]
            # Resize frame to fit window if needed, or keep original aspect
            # For simplicity, force fit
            ctk_img = ctk.CTkImage(light_image=frame, dark_image=frame, size=(600, 400))
            self.label.configure(image=ctk_img)
            
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.after(66, self.animate) # ~15fps
        except Exception:
            pass
            
    def finish(self):
        self.destroy()
        self.master.deiconify()

class MidasHome(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Project Midas - AI Trading Workspace")
        self.geometry("1100x700")

        # --- Aergia Theme Assets ---
        bg_path = os.path.join(parent_dir, "Aergia_Web", "static", "assets", "wallpapers", "The_Opening_Frame.png")
        
        # Background Image (Covering entire window)
        if os.path.exists(bg_path):
            self.bg_image = ctk.CTkImage(Image.open(bg_path), size=(1100, 700))
            self.bg_label = ctk.CTkLabel(self, text="", image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Layout Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0) # Portfolio Panel (Fixed/Auto)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar (Avatar & Controls) ---
        # Transparent/Dark for cinematic feel
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#0b1a20", bg_color="transparent") 
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1) # Push bottom spacer

        # Banner Image (Project Identity)
        self.banner_label = ctk.CTkLabel(self.sidebar_frame, text="")
        self.banner_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Load Banner from Assets
        banner_path = os.path.join(parent_dir, "assets", "banners", "Midas_Banner.png")
        if os.path.exists(banner_path):
             # Banner aspect ratio adjustment. Assuming banner is wide.
             # Sidebar is ~250px. Let's make it 210px wide.
             self.banner_img = ctk.CTkImage(Image.open(banner_path), size=(210, 80))
             self.banner_label.configure(image=self.banner_img)
        else:
             self.banner_label.configure(text="[No Banner]")

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="MIDAS AI", font=ctk.CTkFont(size=20, weight="bold"), text_color="#e0af65")
        self.logo_label.grid(row=1, column=0, padx=20, pady=(10, 20))

        # Buttons (Aergia Teal/Gold Accents)
        btn_fg = "#005f60"
        btn_hover = "#00d2d3"
        
        self.btn_briefing = ctk.CTkButton(self.sidebar_frame, text="🌞 Morning Briefing", command=self.start_briefing_thread, fg_color=btn_fg, hover_color=btn_hover)
        self.btn_briefing.grid(row=2, column=0, padx=20, pady=10)

        self.btn_scanner = ctk.CTkButton(self.sidebar_frame, text="🚀 Squeeze Scanner", command=self.run_scanner_thread, fg_color=btn_fg, hover_color=btn_hover)
        self.btn_scanner.grid(row=3, column=0, padx=20, pady=10)

        self.btn_tracker = ctk.CTkButton(self.sidebar_frame, text="🎯 Squeeze Tracker", command=self.open_tracker_window, fg_color="#005f60", hover_color="#00d2d3")
        self.btn_tracker.grid(row=4, column=0, padx=20, pady=10)

        self.btn_visual = ctk.CTkButton(self.sidebar_frame, text="👁️ Visual Scan (Screen)", command=self.run_visual_thread, fg_color="#552222", hover_color="#773333")
        self.btn_visual.grid(row=5, column=0, padx=20, pady=10)

        self.btn_swing = ctk.CTkButton(self.sidebar_frame, text="📈 Quant Swing Trader", command=self.run_swing_thread, fg_color="#225522", hover_color="#337733")
        self.btn_swing.grid(row=6, column=0, padx=20, pady=10)

        # New Tools
        self.btn_chart = ctk.CTkButton(self.sidebar_frame, text="📊 Open Latest Chart", command=self.open_latest_chart, fg_color="#333333", hover_color="#555555")
        self.btn_chart.grid(row=7, column=0, padx=20, pady=10)

        self.btn_launch = ctk.CTkButton(self.sidebar_frame, text="🚀 Launch Workspace", command=self.launch_workspace_thread, fg_color="#440044", hover_color="#660066")
        self.btn_launch.grid(row=8, column=0, padx=20, pady=10)

        self.btn_coach = ctk.CTkButton(self.sidebar_frame, text="🧠 Run Trading Coach", command=self.run_coach_thread, fg_color="#004444", hover_color="#006666")
        self.btn_coach.grid(row=9, column=0, padx=20, pady=10)

        # System Tools
        self.lbl_sys = ctk.CTkLabel(self.sidebar_frame, text="SYSTEM COMMANDS", font=("Arial", 10, "bold"), text_color="#777777")
        self.lbl_sys.grid(row=10, column=0, pady=(20, 5))

        self.btn_auth = ctk.CTkButton(self.sidebar_frame, text="🔑 Weekly Auth Fix", command=self.run_auth_fix, fg_color="#665500", hover_color="#887700")
        self.btn_auth.grid(row=11, column=0, padx=20, pady=5)

        self.btn_guide = ctk.CTkButton(self.sidebar_frame, text="📚 Distributed Guide", command=self.open_guide, fg_color="#444466", hover_color="#666688")
        self.btn_guide.grid(row=12, column=0, padx=20, pady=5)

        self.btn_autopilot = ctk.CTkButton(self.sidebar_frame, text="♾️ Activate Auto-Pilot", command=self.toggle_autopilot, fg_color="#550000", hover_color="#770000")
        self.btn_autopilot.grid(row=13, column=0, padx=20, pady=(20, 20))

        # --- Main Content Area ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Output Log (Briefing/Scan Results)
        # Transparent-ish textbox
        self.textbox = ctk.CTkTextbox(self.main_frame, width=500, height=400, font=("Consolas", 14), fg_color="#0b1a20", text_color="#00d2d3", border_color="#005f60", border_width=1)
        self.textbox.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.textbox.insert("0.0", "Welcome back, Daniel.\nSystem Ready.\n")

        # --- Portfolio Panel (Right Side) ---
        self.portfolio_frame = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#0b1a20")
        self.portfolio_frame.grid(row=0, column=2, sticky="nsew")
        
        self.pf_label = ctk.CTkLabel(self.portfolio_frame, text="PORTFOLIO MONITOR", font=ctk.CTkFont(size=16, weight="bold"))
        self.pf_label.pack(pady=20)

        self.pf_tabview = ctk.CTkTabview(self.portfolio_frame, width=220)
        self.pf_tabview.pack(pady=10, padx=10, expand=True, fill="both")
        
        self.tab_paper = self.pf_tabview.add("Paper")
        self.tab_live = self.pf_tabview.add("Live")
        
        # Paper Widgets
        self.lbl_paper_eq = ctk.CTkLabel(self.tab_paper, text="Net Liq: $---", font=("Consolas", 16))
        self.lbl_paper_eq.pack(pady=10)
        self.lbl_paper_cash = ctk.CTkLabel(self.tab_paper, text="Cash: $---", font=("Consolas", 12))
        self.lbl_paper_cash.pack(pady=5)
        self.lbl_paper_pos = ctk.CTkLabel(self.tab_paper, text="Positions:\nNone", justify="left")
        self.lbl_paper_pos.pack(pady=20, anchor="w")
        self.btn_refresh_paper = ctk.CTkButton(self.tab_paper, text="Refresh Paper", command=self.update_paper_portfolio, height=30)
        self.btn_refresh_paper.pack(pady=10)

        # Live Widgets
        self.lbl_live_eq = ctk.CTkLabel(self.tab_live, text="Net Liq: $---", font=("Consolas", 16))
        self.lbl_live_eq.pack(pady=10)
        self.lbl_live_cash = ctk.CTkLabel(self.tab_live, text="Cash: $---", font=("Consolas", 12))
        self.lbl_live_cash.pack(pady=5)
        self.lbl_live_pos = ctk.CTkLabel(self.tab_live, text="Positions:\n(Hidden)", justify="left")
        self.lbl_live_pos.pack(pady=20, anchor="w")
        self.btn_refresh_live = ctk.CTkButton(self.tab_live, text="Fetch Live Data", command=self.update_live_portfolio, fg_color="#aa0000", hover_color="#cc0000")
        self.btn_refresh_live.pack(pady=10)

        # --- Income / Medicaid Monitor (Bottom of Portfolio Panel) ---
        self.monitor_frame = ctk.CTkFrame(self.portfolio_frame, fg_color="#333333")
        self.monitor_frame.pack(side="bottom", fill="x", padx=10, pady=20)
        
        ctk.CTkLabel(self.monitor_frame, text="MEDICAID SAFETY MONITOR", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Default Values
        self.wages = 10400.00 # $200 * 52
        self.medicaid_limit = 20000.00 # Safe Est.
        
        self.lbl_income_proj = ctk.CTkLabel(self.monitor_frame, text=f"Proj. Income: ${self.wages:,.2f}", font=("Consolas", 12))
        self.lbl_income_proj.pack(pady=2)
        
        self.lbl_income_status = ctk.CTkLabel(self.monitor_frame, text="STATUS: SAFE (Tier 1)", text_color="green", font=("Arial", 10, "bold"))
        self.lbl_income_status.pack(pady=(0, 10))
        
        self.progress_income = ctk.CTkProgressBar(self.monitor_frame, height=10)
        self.progress_income.set(self.wages / self.medicaid_limit)
        self.progress_income.pack(padx=10, pady=(0, 10))

        # Chat Input
        self.entry = ctk.CTkEntry(self.main_frame, placeholder_text="Ask Midas Strategy Brain...")
        self.entry.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.entry.bind("<Return>", self.chat_with_midas)

        self.strategist = MidasStrategist()
        # Initialize Agent SDK just in case
        midas_agent.init_midas()

        # Auto-Refresh Paper on load
        self.update_paper_portfolio()
        
    def load_avatar(self):
        try:
            # Load 'assets/avatar.jpg' or fallback
            path = "assets/avatar.jpg"
            if not os.path.exists(path):
                # Placeholder logic if no file
                return 
            
            my_image = ctk.CTkImage(light_image=Image.open(path),
                                  dark_image=Image.open(path),
                                  size=(150, 150))
            self.avatar_label.configure(image=my_image)
        except Exception as e:
            print(f"Avatar load error: {e}")

    # --- Actions ---
    
    def update_paper_portfolio(self):
        def _update():
            try:
                broker = VirtualBroker()
                summary = broker.get_account_summary()
                
                # Update Labels safely
                self.lbl_paper_eq.configure(text=f"Net Liq: ${summary['liquidation_value']:.2f}")
                self.lbl_paper_cash.configure(text=f"Cash: ${summary['cash']:.2f}")
                
                pos_text = "Positions:\n"
                if not summary['positions']:
                    pos_text += "None"
                else:
                    for sym, data in summary['positions'].items():
                        pos_text += f"{sym}: {data['qty']} @ ${data['avg_price']:.2f}\n"
                
                self.lbl_paper_pos.configure(text=pos_text)
            except Exception as e:
                print(f"Paper Update Error: {e}")
                
        threading.Thread(target=_update, daemon=True).start()

    def update_live_portfolio(self):
        def _update():
            try:
                self.btn_refresh_live.configure(text="Fetching...", state="disabled")
                client = SchwabClient()
                
                # 1. Get Accounts
                accounts = client.get_account_numbers() 
                if not accounts: 
                    self.lbl_live_eq.configure(text="No Accounts Found")
                    return
                
                # Prepare display text
                display_text_eq = ""
                display_text_cash = ""
                display_text_pos = ""
                
                total_liq_val = 0.0
                
                for idx, acct in enumerate(accounts):
                    acct_hash = acct.get('hashValue')
                    acct_num = acct.get('accountNumber', 'xxxx')[-4:] # Last 4 digits
                    
                    # 2. Get Balance for each
                    balance_data = client.get_account_balance(acct_hash)
                    
                    sec_acct = balance_data.get('securitiesAccount', {})
                    curr_bal = sec_acct.get('currentBalances', {})
                    liq_val = curr_bal.get('liquidationValue', 0.0)
                    cash_bal = curr_bal.get('cashBalance', 0.0)
                    
                    total_liq_val += liq_val
                    
                    positions = sec_acct.get('positions', [])
                    
                    # Format Output
                    # Add separator if not first account
                    if idx > 0:
                        display_text_eq += "\n"
                        display_text_cash += "\n"
                        display_text_pos += "\n" + "-"*30 + "\n"

                    display_text_eq += f"#{idx+1} (..{acct_num}): ${liq_val:,.2f}"
                    display_text_cash += f"#{idx+1}: ${cash_bal:,.2f}"
                    
                    display_text_pos += f"--- Account #{idx+1} (..{acct_num}) ---\n"
                    if not positions:
                        display_text_pos += "None\n"
                    else:
                        for p in positions: 
                            sym = p.get('instrument', {}).get('symbol', 'UNK')
                            qty = p.get('longQuantity', 0)
                            display_text_pos += f"{sym}: {qty}\n"

                self.lbl_live_eq.configure(text=display_text_eq.strip())
                self.lbl_live_cash.configure(text=display_text_cash.strip())
                self.lbl_live_pos.configure(text=display_text_pos)
                
                # --- Update Income Monitor ---
                # Use TOTAL Likidation Value for safety calculation
                
                est_gains = 0.0
                # Conservative estimate: Gains = Total Net Liq - (25k * num_accounts)? 
                # Or just assume Total Net Liq - 25000 base. 
                # Let's stick to the previous simple logic but on the Total.
                if total_liq_val > 25000:
                    est_gains = total_liq_val - 25000
                
                total_income = self.wages + est_gains
                fill_ratio = total_income / self.medicaid_limit
                if fill_ratio > 1.0: fill_ratio = 1.0
                
                self.lbl_income_proj.configure(text=f"Proj. Income: ${total_income:,.2f}")
                self.progress_income.set(fill_ratio)
                
                if total_income > self.medicaid_limit:
                    self.lbl_income_status.configure(text="STATUS: DANGER (Limit Exceeded)", text_color="red")
                    self.progress_income.configure(progress_color="red")
                elif total_income > (self.medicaid_limit * 0.9):
                    self.lbl_income_status.configure(text="STATUS: WARNING (Approaching)", text_color="orange")
                    self.progress_income.configure(progress_color="orange")
                else:
                    self.lbl_income_status.configure(text="STATUS: SAFE (Tier 1)", text_color="green")
                    self.progress_income.configure(progress_color="green")
                
            except Exception as e:
                self.lbl_live_eq.configure(text="Error Fetching")
                print(f"Live Update Error: {e}")
            finally:
                self.btn_refresh_live.configure(text="Fetch Live Data", state="normal")
                
        threading.Thread(target=_update, daemon=True).start()

    def log(self, text):
        self.after(0, lambda: self.textbox.insert("end", text + "\n"))
        self.after(0, lambda: self.textbox.see("end"))

    def start_briefing_thread(self):
        self.log("\n--- STARTING MORNING BRIEFING ---")
        threading.Thread(target=self.run_briefing_process, daemon=True).start()

    def run_briefing_process(self):
        # 1. Run Logic & Get Text
        full_text = run_briefing(output_callback=lambda x: None) # Suppress print, we use full text
        self.log(full_text)
        
        # 2. Voice (Multi-Talk)
        intro = "Good morning. Here is your daily briefing."
        clean_text = full_text.replace("*", "").replace("#", "")
        speak(intro)
        speak(clean_text)
        
        # 3. Mobile Alert (Voice & Text)
        self.log("\n📱 Sending Mobile Voice Alert...")
        
        # Generate Audio File for MMS
        audio_file = "briefing_audio.mp3"
        from midas_voice import save_to_file
        save_to_file(clean_text[:1000], audio_file) # Limit length for MMS size limits
        
        success = send_alert("Midas Morning Brief", full_text, attachment_path=audio_file)
        
        if success:
            self.log(">> Voice Briefing sent to Phone & Email.")
        else:
            self.log(">> Alert Failed. **Check EMAIL_SENDER in .env**")
            
        # Cleanup
        if os.path.exists(audio_file):
            try:
                os.remove(audio_file)
            except:
                pass

    def run_scanner_thread(self):
        self.log("\n--- RUNNING SQUEEZE SCANNER ---")
        threading.Thread(target=self.run_scanner_process, daemon=True).start()

    def run_scanner_process(self):
        candidates = get_squeeze_candidates()
        if not candidates:
            self.log("No hits found.")
            speak("I did not find any squeeze candidates for you today.")
        else:
            for c in candidates:
                self.log(f"🚨 {c['symbol']} | SI: {c['short_float']}%")
            speak(f"I found {len(candidates)} potential plays. Check the dashboard.")

    def run_visual_thread(self):
        self.log("\n--- VISUAL SCAN INITIATED ---")
        self.log("Hide this window if it blocks your chart. Capturing in 3 seconds...")
        threading.Thread(target=self.run_visual_process, daemon=True).start()

    def run_visual_process(self):
        import time
        time.sleep(3) # Time to switch windows
        speak("Capturing screen.")
        try:
            path = midas_agent.capture_screen(mask_privacy=True)
            self.log(f"Snapshot taken: {path}")
            
            response = midas_agent.analyze_market(path, "Analyze this chart/chain and suggest a trade.")
            self.log(f"\nMIDAS VISION:\n{response}")
            speak("Analysis complete. Check the log.")
            
            # Privacy cleanup
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            self.log(f"Visual Error: {e}")

    def run_swing_thread(self):
        self.log("\n--- STARTING QUANT SWING TRADER ---")
        threading.Thread(target=self.run_swing_process, daemon=True).start()

    def run_swing_process(self):
        try:
            speak("Initializing Swing Trader Protocol.")
            trader = MidasSwingTrader()
            broker = VirtualBroker()
            
            watchlist = ['SPY', 'QQQ', 'IWM', 'DIA', 'AAPL', 'NVDA', 'AMD', 'TSLA']
            self.log(f"Scanning Watchlist: {watchlist}")
            self.log(f"Paper Balance: ${broker.account['cash']:.2f}")

            hits = 0
            for symbol in watchlist:
                try:
                    analysis = trader.analyze_ticker(symbol)
                    if not analysis or analysis.get('signal') == 'ERROR':
                        continue
                        
                    signal = analysis['signal']
                    # Log result
                    self.log(f"{symbol}: {signal} | Last: {analysis['price']:.2f}")
                    
                    if "BUY" in signal:
                        hits += 1
                        self.log(f"   >>> ACTION REQUIRED: {signal}")
                        self.log(f"   >>> Reason: {analysis['reason']}")
                        if 'chart' in analysis:
                            chart_abs = os.path.abspath(analysis['chart'])
                            self.log(f"   >>> Chart Generated: {chart_abs}")
                            # Could auto-open: os.startfile(chart_abs) if desired

                except Exception as e:
                    self.log(f"Error {symbol}: {e}")
            
            if hits > 0:
                speak(f"Scan complete. I found {hits} trade opportunities.")
            else:
                speak("Scan complete. No significant signals found right now.")
                
        except Exception as e:
            self.log(f"Swing Trader Error: {e}")
            speak("Error running swing trader.")

    def run_coach_thread(self):
        self.log("\n--- STARTING TRADING COACH ---")
        threading.Thread(target=self.run_coach_process, daemon=True).start()

    def run_coach_process(self):
        try:
            speak("Reviewing your performance.")
            coach = TradingCoach()
            # Redirect stdout to capture coach output (simple hack) or just trust logs
            # For now, just run it, coach.py prints to stdout which goes to console, not GUI textbox unless redirected.
            # I will modify coach to return string or just read the 'lessons_learned.md' tail?
            # Let's just run it and read the last lesson.
            
            coach.run_analysis()
            
            # Read last lesson from file
            if os.path.exists(coach.lessons_path):
                with open(coach.lessons_path, 'r') as f:
                    lines = f.readlines()
                    # simplistic tail
                    last_lesson = "".join(lines[-10:]) 
                self.log(f"\n[COACH FEEDBACK]\n{last_lesson}")
                speak("I have updated your lessons learned file.")
            else:
                self.log("Coach finished (No history found).")
                speak("No new trade history to review.")
                
        except Exception as e:
            self.log(f"Coach Error: {e}")
            speak("The Coach encountered an error.")

    def toggle_autopilot(self):
        if hasattr(self, 'autopilot_running') and self.autopilot_running:
            self.autopilot_running = False
            self.btn_autopilot.configure(text="♾️ Activate Auto-Pilot", fg_color="#550000")
            self.log("Auto-Pilot Stopping...")
            speak("Auto Pilot Deactivated.")
        else:
            self.autopilot_running = True
            self.btn_autopilot.configure(text="🛑 Stop Auto-Pilot", fg_color="#005500")
            self.log("Auto-Pilot Activated. Running cycles every 60s.")
            speak("Auto Pilot Engaged. Monitoring markets.")
            threading.Thread(target=self.run_autopilot_loop, daemon=True).start()

    def run_autopilot_loop(self):
        coord = StrategyCoordinator()
        
        while getattr(self, 'autopilot_running', False):
             try:
                 self.log("\n[AUTO-PILOT] Starting Market Cycle...")
                 # We invoke the cycle. Currently it prints to stdout.
                 # Ideally we capture it, but for MVP we log start/finish.
                 coord.run_daily_cycle()
                 self.log("[AUTO-PILOT] Cycle Complete. Sleeping 60s.")
             except Exception as e:
                 self.log(f"[AUTO-PILOT] Error: {e}")
            
             # Sleep in chunks to allow faster stop
             for _ in range(60): 
                 if not getattr(self, 'autopilot_running', False): break
                 threading.Event().wait(1)

    def chat_with_midas(self, event=None):
        prompt = self.entry.get()
        if not prompt: return
        
        self.log(f"\nYOU: {prompt}")
        self.entry.delete(0, "end")
        
        def run_chat():
            response = self.strategist.ask(prompt)
            self.log(f"MIDAS: {response}")
            
        threading.Thread(target=run_chat, daemon=True).start()

    def launch_workspace_thread(self):
        threading.Thread(target=self.launch_workspace, daemon=True).start()

    def launch_workspace(self):
        self.log("\n--- LAUNCHING WORKSPACE ---")
        tos_path = r"C:\Users\z143d\AppData\Local\thinkorswim\thinkorswim.exe"
        coinbase_url = "https://www.coinbase.com/home"
        
        # 1. Launch TOS
        if os.path.exists(tos_path):
            self.log("Launching ThinkOrSwim...")
            try:
                subprocess.Popen(tos_path)
                speak("Launching Think-Or-Swim.")
            except Exception as e:
                self.log(f"Error launching TOS: {e}")
        else:
            self.log(f"TOS not found at: {tos_path}")
            
        # 2. Launch Coinbase
        self.log("Opening Coinbase...")
        webbrowser.open(coinbase_url)
        speak("Opening Coinbase.")

    def open_latest_chart(self):
        self.log("\nSearching for latest chart...")
        try:
            # Find all html files in charts folder
            chart_dir = os.path.join(os.path.dirname(__file__), "charts")
            list_of_files = glob.glob(os.path.join(chart_dir, "*.html"))
            
            if not list_of_files:
                self.log("No charts found.")
                speak("I don't see any generated charts yet.")
                return

            latest_file = max(list_of_files, key=os.path.getctime)
            self.log(f"Opening: {os.path.basename(latest_file)}")
            webbrowser.open(f"file://{os.path.abspath(latest_file)}")
            speak("Opening chart.")
        except Exception as e:
            self.log(f"Error opening chart: {e}")

    def run_auth_fix(self):
        self.log("\n--- RUNNING WEEKLY AUTH FIX ---")
        script_path = os.path.join(current_dir, "weekly_schwab_setup.py")
        if os.path.exists(script_path):
             self.log("Launching auth script... Check the new window.")
             try:
                if sys.platform == "win32":
                    subprocess.Popen(["python", script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
                else:
                    subprocess.Popen(["python3", script_path])
             except Exception as e:
                 self.log(f"Error running script: {e}")
        else:
            self.log(f"Script not found: {script_path}")

    def open_guide(self):
        self.log("\n--- OPENING DISTRIBUTED GUIDE ---")
        guide_path = os.path.join(parent_dir, "DISTRIBUTED_GUIDE.md")
        if os.path.exists(guide_path):
            try:
                if sys.platform == "win32":
                    os.startfile(guide_path)
                else:
                    subprocess.run(["open", guide_path])
                speak("Opening the distributed guide.")
            except Exception as e:
                self.log(f"Error opening guide: {e}")
        else:
            self.log(f"Guide not found at: {guide_path}")

    def open_tracker_window(self):
        self.log("\n--- OPENING SQUEEZE TRACKER ---")
        tracker_window = SqueezeTrackerWindow(self)
        tracker_window.focus()

if __name__ == "__main__":
    # 1. Init App but hide it
    app = MidasHome()
    app.withdraw() # Hide until splash is done
    
    # 2. Show Splash
    splash = SplashScreen(app)
    
    # 3. Process events until splash destroys itself
    # app.mainloop.mainloop() handles the splash because it is a Toplevel of app
    app.mainloop()
