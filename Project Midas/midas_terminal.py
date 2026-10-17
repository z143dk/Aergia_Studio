import customtkinter as ctk
import os
import sys
import threading
import time
from datetime import datetime
from PIL import Image

# Ensure Root is in path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import Backend Modules (Robust)
# Import Backend Modules (Robust)
# Import Backend Modules (Robust)
try:
    # Core Dependencies
    import midas_quant # [NEW] Technical Analysis Engine
    from midas_strategist import MidasStrategist # [NEW] The BRAIN (Gemini)
    # [NEW] Swarm Orchestration
    from router.hive_mind import HiveMind
    from router.registry import ProviderRegistry
    
    # Charting & Data
    import mplfinance as mpf
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import pandas as pd
    import yfinance as yf
    
    # Schwab (Might fail if not configured)
    from schwab_api.client import SchwabClient
    from schwab_api import auth # [NEW] For manual re-auth
    from midas_agent import analyze_market, capture_screen
    from squeeze_scanner import get_squeeze_candidates
    import subprocess # [NEW] To open auth url

except ImportError as e:
    print(f"CRITICAL Import Error: {e}")
    # We ideally want to crash or define dummies if critical deps differ
    # But for now, let's just print it. 
    # If MidasStrategist failed, it will be undefined.
    # Let's define None for criticals if they fail to avoid NameError
    if 'MidasStrategist' not in locals(): MidasStrategist = None
    if 'HiveMind' not in locals(): HiveMind = None
    if 'ProviderRegistry' not in locals(): ProviderRegistry = None
    if 'SchwabClient' not in locals(): SchwabClient = None

# --- CONFIGURATION ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# Theme Colors (ThinkOrSwim-ish)
COLOR_BG = "#121212" # Main Background
COLOR_PANEL = "#1a1a1a" # Panels
COLOR_BORDER = "#333333"
COLOR_ACCENT = "#00d2d3" # Cyan (Midas Identity)
COLOR_TEXT = "#e0e0e0"
COLOR_GREEN = "#2ecc71"
COLOR_RED = "#e74c3c"
COLOR_GOLD = "#f1c40f"

class MidasTerminal(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Midas Pro Terminal [MICRO-ACCOUNT MODE]")
        self.geometry("1400x900")
        self.configure(fg_color=COLOR_BG)
        
        # Set Icon
        try:
            icon_path = os.path.join(current_dir, "midas.ico")
            self.iconbitmap(icon_path)
        except: pass

        # --- DATA STATE ---
        self.account_balance = 100.00 # Starting Hard Constraint
        self.active_tickers = ["SPY", "QQQ", "IWM", "BTC"]
        
        # [NEW] Paper Trading State
        self.paper_file = os.path.join(current_dir, "midas_paper_data.json")
        self.is_paper_mode = True # Default to Paper for safety
        self.paper_balance = 100000.00
        self.paper_positions = {} # Symbol -> Qty
        self.load_paper_state()
        
        # --- UI LAYOUT ---
        # Grid: 3 Columns (Left, Center, Right)
        self.grid_columnconfigure(0, weight=0, minsize=250) # Left (Scanner)
        self.grid_columnconfigure(1, weight=1)              # Center (Charts)
        self.grid_columnconfigure(2, weight=0, minsize=300) # Right (Tools)
        
        self.grid_rowconfigure(0, weight=0, minsize=40)     # Top (Ticker)
        self.grid_rowconfigure(1, weight=1)                 # Main Content
        self.grid_rowconfigure(2, weight=0, minsize=150)    # Bottom (Console)

        # 1. TOP TICKER TAPE
        self.build_top_bar()

        # 2. LEFT PANEL (Scanner)
        self.build_left_panel()

        # 3. CENTER PANEL (Charts/Visual)
        self.build_center_panel()

        # 4. RIGHT PANEL (Portfolio/Coach/Hive)
        self.build_right_panel()

        # 5. BOTTOM CONSOLE
        self.build_bottom_console()
        
        # Start Clock
        self.update_clock()
        self.log_system("Midas Pro Terminal Initialized.")
        self.log_system("Micro-Account Strategy Loaded: Limit < $100, Expiry > 30 Days.")
        
        # Initialize Brain
        try:
            self.strategist = MidasStrategist()
            # [NEW] Swarm
            self.registry = ProviderRegistry()
            self.hive_mind = HiveMind(self.registry)
            self.log_system("Hive Mind (Gemini 2.0 + DeepSeek + Kimi) Connected.")
        except Exception as e:
            self.log_system(f"Hive Mind Error: {e}")
            self.strategist = None
            self.hive_mind = None

    def build_top_bar(self):
        self.top_bar = ctk.CTkFrame(self, height=40, corner_radius=0, fg_color="#000000", border_width=0)
        self.top_bar.grid(row=0, column=0, columnspan=3, sticky="ew")
        
        self.lbl_clock = ctk.CTkLabel(self.top_bar, text="00:00:00", font=("Consolas", 12, "bold"), text_color=COLOR_ACCENT)
        self.lbl_clock.pack(side="right", padx=10)
        
        # Ticker Scroller (Live)
        self.lbl_ticker = ctk.CTkLabel(self.top_bar, text="Connecting to Data Feed...", font=("Consolas", 12), text_color=COLOR_GREEN)
        self.lbl_ticker.pack(side="left", padx=10)
        
        # Start Data Loop
        self.after(2000, self.update_market_data)

    def update_market_data(self):
        def _fetch():
            try:
                # Mock Data for now if Schwab is offline, or use Schwab if available
                # In a real scenario, we'd use self.schwab_client.quote(["SPY", "QQQ"])
                # For safety/reliability in this env, we simulate live ticker
                import random
                spy = 500.00 + random.uniform(-1, 1)
                qqq = 420.00 + random.uniform(-1, 1)
                btc = 95000 + random.randint(-100, 100)
                
                text = f"SPY ${spy:.2f} | QQQ ${qqq:.2f} | BTC ${btc:,.0f} | IWM $205.50"
                self.lbl_ticker.configure(text=text)
            except: pass
            
        threading.Thread(target=_fetch, daemon=True).start()
        self.after(5000, self.update_market_data)

    def build_left_panel(self):
        self.left_panel = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=COLOR_PANEL, border_width=1, border_color=COLOR_BORDER)
        self.left_panel.grid(row=1, column=0, sticky="nsew", padx=(0,1), pady=1)
        
        # Header
        ctk.CTkLabel(self.left_panel, text="MARKET SCANNERS", font=("Roboto", 12, "bold")).pack(pady=5)
        
        # Watchlist
        self.watchlist_frame = ctk.CTkScrollableFrame(self.left_panel, label_text="WATCHLIST", height=300, fg_color="transparent")
        self.watchlist_frame.pack(fill="x", padx=5, pady=5)
        
        # Add some dummy items for visual verify
        for ticker in self.active_tickers:
            row = ctk.CTkFrame(self.watchlist_frame, fg_color="#222")
            row.pack(fill="x", pady=1)
            
            lbl_tick = ctk.CTkLabel(row, text=ticker, width=50, anchor="w", font=("Consolas", 12, "bold"), text_color=COLOR_ACCENT)
            lbl_tick.pack(side="left", padx=5)
            lbl_tick.bind("<Button-1>", lambda e, s=ticker: self.update_chart(s))
            
            ctk.CTkLabel(row, text="---", width=50, text_color="gray").pack(side="right", padx=5)

        # Squeeze Radar
        ctk.CTkLabel(self.left_panel, text="SQUEEZE RADAR", font=("Roboto", 12, "bold"), text_color=COLOR_GOLD).pack(pady=(20,5))
        self.radar_frame = ctk.CTkFrame(self.left_panel, fg_color="#222")
        self.radar_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.btn_scan = ctk.CTkButton(self.left_panel, text="Run Scan", command=self.run_scanner, fg_color=COLOR_ACCENT, text_color="black")
        self.btn_scan.pack(pady=10, padx=5)

    def build_center_panel(self):
        self.center_panel = ctk.CTkFrame(self, corner_radius=0, fg_color="#000000") # Start Black for Chart
        self.center_panel.grid(row=1, column=1, sticky="nsew", padx=1, pady=1)
        
        # Theme Background
        try:
            bg_path = os.path.join(parent_dir, "assets", "banners", "Midas_Banner.png")
            if os.path.exists(bg_path):
                # Load
                img = Image.open(bg_path).convert("RGBA")
                
                # [NEW] Make Translucent (Watermark Style)
                # Reduce Alpha channel to 40% intensity as requested
                alpha = img.split()[3]
                alpha = alpha.point(lambda p: p * 0.40)
                img.putalpha(alpha)

                # Resize to fit nicely
                self.bg_image = ctk.CTkImage(light_image=img, dark_image=img, size=(1000, 600))
                
                self.lbl_bg = ctk.CTkLabel(self.center_panel, text="", image=self.bg_image)
                self.lbl_bg.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            print(f"Theme Load Error: {e}")

        # Placeholder Text (Overlay)
        self.lbl_chart_status = ctk.CTkLabel(self.center_panel, text="[NO CHART FEED]", font=("Arial", 20, "bold"), text_color="#333")
        self.lbl_chart_status.place(relx=0.5, rely=0.5, anchor="center")
        
        # Visual Scan Overlay
        self.btn_visual_scan = ctk.CTkButton(self.center_panel, text="👁️ ANALYZE SCREEN", command=self.run_visual_scan, 
                                           bg_color="transparent", fg_color="#0A2F30", 
                                           border_width=1, border_color=COLOR_ACCENT, hover_color=COLOR_ACCENT)
        self.btn_visual_scan.place(relx=0.95, rely=0.05, anchor="ne")

    def build_right_panel(self):
        self.right_panel = ctk.CTkFrame(self, width=300, corner_radius=0, fg_color=COLOR_PANEL, border_width=1, border_color=COLOR_BORDER)
        self.right_panel.grid(row=1, column=2, sticky="nsew", padx=(1,0), pady=1)
        
        self.tabs = ctk.CTkTabview(self.right_panel, fg_color="transparent")
        self.tabs.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.tab_tos = self.tabs.add("TOS")
        self.tab_crypto = self.tabs.add("CRYPTO")
        self.tab_coach = self.tabs.add("COACH")
        self.tab_hive = self.tabs.add("HIVE")

        # -- TAB 4: HIVE CONTROLS --
        # Chat History
        self.hive_chat_frame = ctk.CTkScrollableFrame(self.tab_hive, height=400, fg_color="transparent")
        self.hive_chat_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Input Area
        input_frame = ctk.CTkFrame(self.tab_hive, fg_color="transparent")
        input_frame.pack(fill="x", padx=2, pady=5)
        
        self.hive_input = ctk.CTkEntry(input_frame, placeholder_text="Ask the Board...", font=("Roboto", 12))
        self.hive_input.pack(side="left", fill="x", expand=True, padx=(0,5))
        self.hive_input.bind("<Return>", lambda e: self.send_to_hive())
        
        self.btn_ask_hive = ctk.CTkButton(input_frame, text="SEND", width=60, command=self.send_to_hive, fg_color=COLOR_GOLD, text_color="black")
        self.btn_ask_hive.pack(side="right")
        
        # Initial Message
        self.add_hive_message("Board", "We are assembled. Midas, what is the directive?")

        # -- TAB 1: TOS (ThinkOrSwim / Schwab) --
        self.mode_switch = ctk.CTkSwitch(self.tab_tos, text="PAPER TRADING", command=self.toggle_mode, onvalue=True, offvalue=False)
        self.mode_switch.pack(pady=10)
        self.mode_switch.select() # Default ON

        self.lbl_balance = ctk.CTkLabel(self.tab_tos, text=f"${self.paper_balance:,.2f}", font=("Consolas", 24, "bold"), text_color=COLOR_GOLD)
        self.lbl_balance.pack(pady=5)
        self.lbl_mode = ctk.CTkLabel(self.tab_tos, text="SIMULATION MODE", font=("Arial", 10, "bold"), text_color=COLOR_GOLD)
        self.lbl_mode.pack(pady=0)
        
        self.btn_refresh_port = ctk.CTkButton(self.tab_tos, text="Refresh TOS", command=self.refresh_portfolio, fg_color="#333")
        self.btn_refresh_port.pack(pady=10)
        
        # [NEW] Auth Button
        self.btn_auth = ctk.CTkButton(self.tab_tos, text="Re-Authenticate API", command=self.start_auth_flow, fg_color="#555", width=120, font=("Arial", 10))
        self.btn_auth.pack(pady=5)
        
        self.lbl_positions = ctk.CTkLabel(self.tab_tos, text="Positions: None", justify="left")
        self.lbl_positions.pack(pady=10, fill="x")

        # -- TAB 2: CRYPTO (Coinbase) --
        self.lbl_crypto_header = ctk.CTkLabel(self.tab_crypto, text="COINBASE PORTFOLIO", font=("Roboto", 12, "bold"), text_color=COLOR_ACCENT)
        self.lbl_crypto_header.pack(pady=(10, 5))
        
        self.lbl_crypto_balance = ctk.CTkLabel(self.tab_crypto, text="$0.00", font=("Consolas", 24, "bold"), text_color="#ffffff")
        self.lbl_crypto_balance.pack(pady=5)
        
        self.btn_refresh_crypto = ctk.CTkButton(self.tab_crypto, text="Refresh Crypto", command=self.refresh_crypto_portfolio, fg_color="#333", hover_color="#444")
        self.btn_refresh_crypto.pack(pady=10)
        
        self.lbl_crypto_positions = ctk.CTkLabel(self.tab_crypto, text="Positions: --", justify="left", font=("Consolas", 11))
        self.lbl_crypto_positions.pack(pady=10, fill="x", padx=10)

    def refresh_portfolio(self):
        self.log_system("Fetching Account Data...")
        self.btn_refresh_port.configure(state="disabled", text="Fetching...")
        
        def _worker():
            try:
                client = SchwabClient()
                # 1. Get Accounts
                accts = client.get_account_numbers()
                if not accts:
                    self.log_system("No linked accounts found.")
                    return

                total_liq = 0.0
                pos_text = ""
                
                for acct in accts:
                    # Account Info
                    h = acct.get('hashValue')
                    acct_num = acct.get('accountNumber', 'xxxx')
                    
                    bal = client.get_account_balance(h)
                    val = bal.get('securitiesAccount', {}).get('currentBalances', {}).get('liquidationValue', 0)
                    total_liq += val
                    
                    # Header for this account
                    pos_text += f"\n[ACCT ...{str(acct_num)[-4:]}] ${val:,.2f}\n"
                    
                    # Get Positions
                    positions = bal.get('securitiesAccount', {}).get('positions', [])
                    if not positions:
                        pos_text += "  - (Empty)\n"
                    else:
                        for p in positions:
                            sym = p.get('instrument', {}).get('symbol')
                            qty = p.get('longQuantity', 0)
                            pos_text += f"  - {sym}: {qty}\n"

                self.account_balance = total_liq
                self.after(0, lambda: self.lbl_balance.configure(text=f"${total_liq:,.2f}"))
                self.after(0, lambda: self.lbl_positions.configure(text=pos_text))
                self.log_system(f"Portfolio Updated. Net Liq: ${total_liq:,.2f}")
                
            except Exception as e:
                self.log_system(f"Portfolio Error: {e}")
            finally:
                self.after(0, lambda: self.btn_refresh_port.configure(state="normal", text="Refresh TOS"))
                
        threading.Thread(target=_worker, daemon=True).start()

    def refresh_crypto_portfolio(self):
        self.log_system("Fetching Coinbase Data...")
        self.btn_refresh_crypto.configure(state="disabled", text="Fetching...")
        
        def _worker():
            try:
                if not self.registry or not self.registry.has("coinbase"):
                    self.log_system("Coinbase Provider not configured.")
                    return

                provider = self.registry.get("coinbase")
                client = provider.client
                if not client:
                    self.log_system("Coinbase Client is None.")
                    return

                accounts = client.get_accounts()
                
                # Handle Object vs Dict return from SDK
                acct_list = []
                if hasattr(accounts, "accounts"):
                    acct_list = accounts.accounts
                elif isinstance(accounts, dict):
                    acct_list = accounts.get("accounts", [])
                
                total_usd = 0.0
                pos_text = "Holdings:\n"
                
                for acct in acct_list:
                    val = 0.0
                    curr = "UNKNOWN"
                    
                    if hasattr(acct, "available_balance"):
                         bal_obj = acct.available_balance
                         if hasattr(bal_obj, "value"):
                             val = float(bal_obj.value)
                         elif isinstance(bal_obj, dict):
                             val = float(bal_obj.get("value", 0))
                    elif isinstance(acct, dict):
                         val = float(acct.get("available_balance", {}).get("value", 0))
                    
                    if hasattr(acct, "currency"):
                        curr = acct.currency
                    elif isinstance(acct, dict):
                        curr = acct.get("currency")
                        
                    if val > 0:
                        # Calculate USD Value
                        usd_val = 0.0
                        price_str = "1.00"
                        
                        if curr == "USD":
                            usd_val = val
                        else:
                            try:
                                # Fetch Price
                                product_id = f"{curr}-USD"
                                # Note: This might be slow if many assets. 
                                # Ideally we'd batch or cache, but for <5 assets it's fine.
                                p_data = client.get_product(product_id=product_id)
                                
                                price_val = 0.0
                                if hasattr(p_data, "price"):
                                    price_val = float(p_data.price)
                                elif isinstance(p_data, dict):
                                    price_val = float(p_data.get("price", 0))
                                
                                usd_val = val * price_val
                                price_str = f"{price_val:,.2f}"
                            except Exception as ex:
                                self.log_system(f"Price Error ({curr}): {ex}")
                                # specific handling for USDC or fallback
                                if curr == "USDC": 
                                    usd_val = val # Assume $1 peg if fetch fails or just safe default
                                
                        total_usd += usd_val
                        
                        # Format: "BTC: 0.5234 ($32,000.00)"
                        # Using 4 decimal places for qty since crypto can be small
                        pos_text += f"{curr}: {val:.4f} (${usd_val:,.2f})\n"
                
                self.after(0, lambda: self.lbl_crypto_positions.configure(text=pos_text))
                # Update both balance and header to be sure
                self.after(0, lambda: self.lbl_crypto_balance.configure(text=f"Total: ${total_usd:,.2f}"))
                self.log_system("Coinbase Data Updated.")

            except Exception as e:
                self.log_system(f"Coinbase Error: {e}")
            finally:
                self.after(0, lambda: self.btn_refresh_crypto.configure(state="normal", text="Refresh Crypto"))
        
        threading.Thread(target=_worker, daemon=True).start()

    def build_bottom_console(self):
        self.console_panel = ctk.CTkFrame(self, height=150, corner_radius=0, fg_color="#000000", border_width=1, border_color=COLOR_BORDER)
        self.console_panel.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(1,0))
        
        ctk.CTkLabel(self.console_panel, text="SYSTEM LOG", font=("Consolas", 10, "bold"), text_color="gray").pack(anchor="w", padx=5)
        
        self.console_text = ctk.CTkTextbox(self.console_panel, font=("Consolas", 11), fg_color="transparent", text_color=COLOR_ACCENT)
        self.console_text.pack(fill="both", expand=True, padx=5, pady=2)

    # --- LOGIC ---

    def log_system(self, message):
        ts = datetime.now().strftime("%H:%M:%S")
        self.console_text.insert("end", f"[{ts}] {message}\n")
        self.console_text.see("end")

    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.lbl_clock.configure(text=now)
        self.after(1000, self.update_clock)

    def run_scanner(self):
        self.log_system("Scanning Market (Micro-Account Mode: <$100)...")
        self.btn_scan.configure(state="disabled", text="Scanning...")
        
        def _scan_thread():
            try:
                # 1. Run Standard Squeeze Scan
                candidates = get_squeeze_candidates()
                
                # 2. Filter for Micro-Account
                # Logic: We need options < $1.00 (since $1.00 * 100 shares = $100)
                # For now, we simulate this filter or check price if available
                micro_candidates = []
                for c in candidates:
                    # Mock price check if not in candidate data, or assume candidates are tickers
                    # If candidate has 'price', check it.
                    price = c.get('price', 1000) # Default high to be safe
                    if price < 50: # If stock price is < $50, options might be cheap
                        micro_candidates.append(c)
                
                # Update UI
                self.after(0, lambda: self._update_scanner_ui(candidates)) # Show all for now, highlight affordables
                self.log_system(f"Scan Complete. Found {len(candidates)} potential squeezes.")
                
            except Exception as e:
                self.log_system(f"Scan Error: {e}")
            finally:
                self.after(0, lambda: self.btn_scan.configure(state="normal", text="Run Scan"))
        
        threading.Thread(target=_scan_thread, daemon=True).start()

    def _update_scanner_ui(self, candidates):
        # Clear existing
        for widget in self.radar_frame.winfo_children():
            widget.destroy()

        if not candidates:
            ctk.CTkLabel(self.radar_frame, text="No Squeezes Found", text_color="gray").pack(pady=10)
            return

        # Headers
        header = ctk.CTkFrame(self.radar_frame, fg_color="#333", height=25)
        header.pack(fill="x", pady=1)
        ctk.CTkLabel(header, text="SYM", width=50, font=("Arial",10,"bold")).pack(side="left")
        ctk.CTkLabel(header, text="SQZ", width=40, font=("Arial",10,"bold")).pack(side="left")

        for c in candidates:
            # Color code
            in_squeeze = c.get('in_squeeze', False)
            color = COLOR_RED if in_squeeze else COLOR_GREEN
            
            row = ctk.CTkFrame(self.radar_frame, fg_color="transparent")
            row.pack(fill="x", pady=1)
            
            # Make Symbol Clickable for Chart
            sym_lbl = ctk.CTkLabel(row, text=c['symbol'], width=50, anchor="w", font=("Consolas", 11, "bold"), text_color=COLOR_ACCENT)
            sym_lbl.pack(side="left", padx=2)
            sym_lbl.bind("<Button-1>", lambda e, s=c['symbol']: self.update_chart(s))
            sym_lbl.bind("<Enter>", lambda e: row.configure(fg_color="#333")) # Hover effect
            sym_lbl.bind("<Leave>", lambda e: row.configure(fg_color="transparent"))

            sqz_text = "ON" if in_squeeze else "OFF"
            ctk.CTkLabel(row, text=sqz_text, width=40, text_color=color, font=("Consolas",10)).pack(side="left")
            
            # Action Buttons
            # Analyze (Hive)
            btn_analyze = ctk.CTkButton(row, text="🧠", width=30, height=20, fg_color="#444", 
                        command=lambda s=c['symbol']: self.ask_hive_about(s))
            btn_analyze.pack(side="right", padx=1)
            
            # Paper Buy
            ctk.CTkButton(row, text="BUY", width=40, height=20, fg_color=COLOR_GOLD, text_color="black",
                        command=lambda s=c['symbol'], p=c.get('price', 0): self.execute_paper_trade(s, "BUY", 1, p)).pack(side="right", padx=1)

    def run_visual_scan(self):
        self.log_system("Initiating Visual Analysis...")
        # Logic to be hooked up
        self.log_system("Visual Scan feature coming soon.")

    def send_to_hive(self):
        prompt = self.hive_input.get()
        if not prompt: return
        
        self.add_hive_message("You", prompt)
        self.hive_input.delete(0, "end")
        
        # [NEW] Advanced Intent Parsing
        clean_prompt = prompt.strip().upper()
        
        # [NEW] Clear Command
        if clean_prompt == "CLEAR" or clean_prompt == "/CLEAR":
            self.clear_hive_messages()
            return
        
        # 1. Ticker Extraction (Regex-like or simple scan)
        # Look for the first "Word" that matches a known ticker or is 2-5 chars in uppercase inside the sentence
        potential_ticker = None
        words = clean_prompt.split()
        for w in words:
            # Strip punctuation
            w_clean = ''.join(c for c in w if c.isalnum())
            if w_clean in self.active_tickers or (len(w_clean) >= 2 and len(w_clean) <= 5 and w_clean.isalpha()):
                # Heuristic: If user explicitly typed a short uppercase word, usually a ticker
                # In strict mode, we'd check a dictionary. For now, assume validity if it looks like one.
                # However, common words like "AND", "THE", "FOR" are false positives. 
                # Let's filter common stops if checking arbitrary words.
                if w_clean not in ["AND", "THE", "FOR", "SEE", "HAVE", "BUY", "SELL", "WHAT", "WHY", "HOW", "LOOK"]:
                    potential_ticker = w_clean
                    break
        
        # 2. Command Analysis with Ticker
        if potential_ticker:
             # If "Chart" or "Show" is explicitly requested
             if "CHART" in clean_prompt or "SHOW" in clean_prompt:
                 self.log_system(f"Command: Chart {potential_ticker}")
                 self.update_chart(potential_ticker)
                 self.add_hive_message("Board", f"Charting {potential_ticker}...")
                 return
             
             # If "Analyze", "Quant", "Why" -> Quant Engine
             if any(k in clean_prompt for k in ["ANALYZE", "ANAYLZE", "QUANT", "WHY", "HOW", "STRATEGY"]):
                 self.log_system(f"Command: Quant Analysis {potential_ticker}")
                 self.update_chart(potential_ticker) # Show chart too
                 self.add_hive_message("Board", f"Running Quant Logic on {potential_ticker}...")
                 
                 def _run_quant():
                     try:
                         data = midas_quant.get_technical_summary(potential_ticker)
                         if "error" in data:
                             self.after(0, lambda: self.add_hive_message("Quant", f"Error: {data['error']}"))
                         else:
                             msg = midas_quant.format_quant_response(data)
                             self.after(0, lambda: self.add_hive_message("Quant", msg))
                             self.log_system(f"Quant Analysis for {potential_ticker} complete.")
                     except Exception as e:
                         self.log_system(f"Quant Error: {e}")
                 
                 threading.Thread(target=_run_quant, daemon=True).start()
                 return

        # 3. General Chat (Gemini / Strategist / Swarm)
        # If no specific command matched, or if it's a general question like "Do we have anything for next week?"
        self.log_system(f"Asking Hive (LLM): {prompt}")
        
        def _thread():
            try:
                # Determine if this needs a SWARM (Deep Research) or just Chat
                # Heuristic: Keywords implying depth, future planning, or multiple angles
                needs_swarm = any(k in clean_prompt for k in ["WEEKEND", "NEXT WEEK", "PLAN", "DEEP", "RESEARCH", "FIND ME", "SCAN", "OPTIONS"])
                
                if needs_swarm and self.hive_mind:
                    self.after(0, lambda: self.add_hive_message("Board", "Activating Swarm Mode (DeepSeek + Kimi + Gemini)..."))
                    self.log_system("Swarm Activated.")
                    
                    # Run the async swarm in a sync wrapper
                    import asyncio
                    try:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        response = loop.run_until_complete(self.hive_mind.swarm(prompt))
                        loop.close()
                    except Exception as exe:
                        response = f"Swarm Failed: {exe}"
                        
                    self.after(0, lambda: self.add_hive_message("Hive", response))
                    self.log_system("Swarm Mission Complete.")

                elif any(k in clean_prompt for k in ["COINBASE", "CRYPTO", "BTC", "ETH", "BITCOIN", "ETHEREUM"]):
                    self.log_system("Routing to Coinbase Provider...")
                    self.add_hive_message("Board", "Checking Coinbase...")
                    print("DEBUG: Coinbase Command Triggered")

                    def _run_coinbase():
                        try:
                            print("DEBUG: Inside _run_coinbase thread")
                            # Use registry from self.hive_mind if available, or create new one?
                            # self.registry is set in __init__ now
                            if self.registry and self.registry.has("coinbase"):
                                print("DEBUG: Registry has coinbase")
                                provider = self.registry.get("coinbase")
                                # Use generate() as a simple command interface
                                print(f"DEBUG: Calling provider.generate({prompt})")
                                res = provider.generate(prompt)
                                print(f"DEBUG: Provider returned: {res}")
                                
                                # Extract content from dict or object
                                msg = res.get("content", "No data returned.") if isinstance(res, dict) else res.content
                                print(f"DEBUG: Extracted Msg: {msg}")
                                
                                self.after(0, lambda: self.add_hive_message("Coinbase", msg))
                            else:
                                print("DEBUG: Registry MISSING coinbase")
                                self.after(0, lambda: self.add_hive_message("System", "Coinbase Provider not configured (Check .env)."))
                        except Exception as e:
                             print(f"DEBUG: Coinbase Exception: {e}")
                             import traceback
                             traceback.print_exc()
                             self.after(0, lambda: self.add_hive_message("System", f"Coinbase Error: {e}"))
                    
                    threading.Thread(target=_run_coinbase, daemon=True).start()

                elif self.strategist:
                    # Context for the AI
                    context = f"User Balance: ${self.account_balance:.2f}. Paper Balance: ${self.paper_balance:.2f}. "
                    if self.is_paper_mode: context += "(Simulation Mode). "
                    full_prompt = context + prompt
                    
                    response = self.strategist.ask(full_prompt, mode="explain") # Use 'explain' mode for chat
                    self.after(0, lambda: self.add_hive_message("Board", response))
                    self.log_system("Hive Responded (AI).")
                else:
                    self.after(0, lambda: self.add_hive_message("Board", "Hive Mind Offline. Check API Key."))
            except Exception as e:
                self.log_system(f"Hive Error: {e}")
                import traceback
                traceback.print_exc()
                
        threading.Thread(target=_thread, daemon=True).start()

    def add_hive_message(self, sender, text):
        msg_frame = ctk.CTkFrame(self.hive_chat_frame, fg_color="#222" if sender == "Board" else "#333")
        msg_frame.pack(fill="x", pady=2, padx=2)
        
        color = COLOR_GOLD if sender == "Board" else COLOR_ACCENT
        ctk.CTkLabel(msg_frame, text=f"{sender}:", text_color=color, font=("Arial", 10, "bold"), width=40, anchor="n").pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(msg_frame, text=text, text_color="#eee", font=("Arial", 11), wraplength=200, justify="left").pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # Scroll to bottom
        # self.hive_chat_frame._parent_canvas.yview_moveto(1.0) # ctk hack if needed

    def clear_hive_messages(self):
        for widget in self.hive_chat_frame.winfo_children():
            widget.destroy()
        self.log_system("Hive Chat Cleared.")

    def ask_hive_about(self, ticker):
        msg = f"Analyze {ticker} for a Micro-Account Swing Trade."
        self.log_system(f"Sending to Hive: {msg}")
        # TODO: Link to Hive Dispatcher
        self.tabs.set("HIVE") # Switch tab
        # self.hive_input.insert(msg)...

    def start_auth_flow(self):
        self.log_system("Initiating Manual Re-Auth...")
        try:
            url = auth.generate_auth_url()
            self.log_system(f"Opening Browser: {url[:30]}...")
            try:
                subprocess.Popen(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--profile-directory=Default", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except FileNotFoundError:
                import webbrowser
                webbrowser.open(url)
            
            # Show Input Dialog
            dialog = ctk.CTkInputDialog(text="Paste the full Redirect URL or 'code=' here:", title="Schwab Authentication")
            code_input = dialog.get_input()
            
            if code_input:
                self.finalize_auth(code_input)
            else:
                self.log_system("Auth Cancelled.")
                
        except Exception as e:
            self.log_system(f"Auth Error: {e}")

    def finalize_auth(self, raw_input):
        # Extract code if full URL is pasted
        code = None
        raw_input = raw_input.strip()
        
        # 1. Try robust URL parsing first
        if "code=" in raw_input:
            try:
                import urllib.parse
                parsed = urllib.parse.urlparse(raw_input)
                qs = urllib.parse.parse_qs(parsed.query)
                if 'code' in qs:
                    code = qs['code'][0] # This is DECODED
            except Exception as e: 
                self.log_system(f"URL Parse Error: {e}")
            
            # 2. Fallback: string split (only if parse failed)
            if not code:
                 try:
                     raw_code = raw_input.split("code=")[1].split("&")[0]
                     # Must decode if grabbing raw string, as requests will encode it again
                     import urllib.parse
                     code = urllib.parse.unquote(raw_code)
                 except: pass
        else:
            # Assume user pasted just the code
            # Check if it looks encoded (has %)
            if "%" in raw_input:
                import urllib.parse
                code = urllib.parse.unquote(raw_input)
            else:
                code = raw_input

        if not code:
            self.log_system("Error: Could not extract Auth Code.")
            return

        self.log_system("Exchanging Code for Tokens...")
        # self.log_system(f"Debug Code: {code[:10]}...") # Careful not to log full secrets
        
        def _exchange():
            try:
                tokens = auth.exchange_code_for_token(code)
                auth.save_tokens(tokens) # [CRITICAL FIX] Save to disk!
                self.log_system("Authentication SUCCESS! Tokens refreshed.")
                self.after(0, self.refresh_portfolio) 
            except Exception as e:
                self.log_system(f"Exchange Failed: {e}")
                
        threading.Thread(target=_exchange, daemon=True).start()

    def toggle_mode(self):
        self.is_paper_mode = self.mode_switch.get()
        if self.is_paper_mode:
            self.lbl_balance.configure(text=f"${self.paper_balance:,.2f}", text_color=COLOR_GOLD)
            self.lbl_mode.configure(text="SIMULATION MODE", text_color=COLOR_GOLD)
            self.lbl_positions.configure(text=self._format_paper_positions())
            self.btn_auth.configure(state="disabled")
        else:
            self.lbl_balance.configure(text=f"${self.account_balance:,.2f}", text_color=COLOR_GREEN)
            self.lbl_mode.configure(text="LIVE ACCOUNT (RISK)", text_color=COLOR_RED)
            self.btn_auth.configure(state="normal")
            self.refresh_portfolio() # Fetch real data

    def _format_paper_positions(self):
        if not self.paper_positions:
            return "Positions: None"
        txt = "Positions:\n"
        for sym, qty in self.paper_positions.items():
            txt += f"{sym}: {qty}\n"
        return txt

    def execute_paper_trade(self, symbol, action, qty, price):
        if not self.is_paper_mode:
            self.log_system("Error: Switch to SIMULATION MODE to use Paper Buy.")
            return
            
        if price == 0: price = 100.00 # Mock price if missing
        
        cost = qty * price
        
        if action == "BUY":
            if cost > self.paper_balance:
                self.log_system(f"Paper Trade REJECTED: Insufficient Funds (${cost:,.2f} > ${self.paper_balance:,.2f})")
                return
            
            self.paper_balance -= cost
            self.paper_positions[symbol] = self.paper_positions.get(symbol, 0) + qty
            
            self.log_system(f"PAPER TRADE: BOUGHT {qty} {symbol} @ ${price:.2f} (Total: ${cost:.2f})")
            self.lbl_balance.configure(text=f"${self.paper_balance:,.2f}")
            self.lbl_positions.configure(text=self._format_paper_positions())
            self.save_paper_state()

    def save_paper_state(self):
        import json
        data = {
            "balance": self.paper_balance,
            "positions": self.paper_positions
        }
        try:
            with open(self.paper_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving paper data: {e}")

    def load_paper_state(self):
        import json
        if not os.path.exists(self.paper_file): return
        
        try:
            with open(self.paper_file, 'r') as f:
                data = json.load(f)
                self.paper_balance = data.get("balance", 100000.00)
                self.paper_positions = data.get("positions", {})
        except Exception as e:
            print(f"Error loading paper data: {e}")

    def update_chart(self, ticker):
        self.log_system(f"Loading Chart for {ticker}...")
        
        # 1. Clear Previous
        for widget in self.center_panel.winfo_children():
            widget.destroy()

        # 2. Re-Apply Background (Watermark)
        try:
            if hasattr(self, 'bg_image'):
                self.lbl_bg = ctk.CTkLabel(self.center_panel, text="", image=self.bg_image)
                self.lbl_bg.place(relx=0.5, rely=0.5, anchor="center")
        except: pass

        # 3. Create Chart Frame (Transparent-ish?)
        # Matplotlib integration in Tkinter is a bit heavy, we'll place it on top
        chart_frame = ctk.CTkFrame(self.center_panel, fg_color="transparent")
        chart_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        def _fetch_and_plot():
            try:
                # Fetch Data (Daily for Swing Trading)
                df = yf.download(ticker, period="6mo", interval="1d", progress=False)
                if df.empty:
                    self.log_system(f"No Data for {ticker}")
                    return
                
                # Style
                mc = mpf.make_marketcolors(up=COLOR_GREEN, down=COLOR_RED, edge='inherit', wick='inherit', volume='in', hlines=[100])
                s  = mpf.make_mpf_style(marketcolors=mc, gridstyle=':', y_on_right=True, facecolor=COLOR_BG, edgecolor=COLOR_BORDER, figcolor=COLOR_BG)
                
                # Plot to Figure
                fig, axlist = mpf.plot(df, type='candle', style=s, volume=True, mav=(9, 21), returnfig=True, figsize=(8, 5))
                
                # Embed in Tkinter
                def _draw_on_main():
                    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
                    canvas.draw()
                    canvas.get_tk_widget().pack(fill="both", expand=True)
                    
                    # Add simple "Close Chart" button or Overlay
                    title = ctk.CTkLabel(chart_frame, text=f"{ticker} [DAILY]", font=("Consolas", 14, "bold"), text_color=COLOR_ACCENT, bg_color="#121212")
                    title.place(relx=0.02, rely=0.02, anchor="nw")
                    
                    self.log_system(f"Chart Rendered: {ticker}")

                self.after(0, _draw_on_main)

            except Exception as e:
                self.log_system(f"Chart Error: {e}")
                import traceback
                traceback.print_exc()

        threading.Thread(target=_fetch_and_plot, daemon=True).start()

if __name__ == "__main__":
    app = MidasTerminal()
    app.mainloop()
