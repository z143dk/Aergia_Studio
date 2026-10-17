import customtkinter as ctk
import yfinance as yf
import threading

class SqueezeTrackerWindow(ctk.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("🎯 Midas Squeeze Tracker")
        self.geometry("600x700")
        self.attributes("-topmost", True)  # Floating window effect
        
        # Color palette (Aergia theme)
        self.bg_color = "#081116"
        self.panel_color = "#0B1D25"
        self.accent_gold = "#E0AF65"
        self.accent_teal = "#00D2D3"
        self.text_main = "#FFFFFF"
        self.text_sub = "#A0B0B5"

        self.configure(fg_color=self.bg_color)
        
        # --- Top Search Bar ---
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        self.symbol_entry = ctk.CTkEntry(
            self.top_frame,
            placeholder_text="Enter Ticker (e.g. SOUN, GME)",
            font=ctk.CTkFont(size=20, weight="bold"),
            width=250,
            height=40,
            fg_color=self.panel_color,
            text_color=self.accent_gold,
            border_color="#183645"
        )
        self.symbol_entry.pack(side="left", padx=(0, 10))
        
        self.track_btn = ctk.CTkButton(
            self.top_frame,
            text="TRACK",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#005F60",
            hover_color=self.accent_teal,
            width=100,
            height=40,
            command=self.fetch_data
        )
        self.track_btn.pack(side="left")

        # --- Status / Price Bar ---
        self.status_frame = ctk.CTkFrame(self, fg_color=self.panel_color, corner_radius=10)
        self.status_frame.pack(fill="x", padx=20, pady=10)
        
        self.name_label = ctk.CTkLabel(self.status_frame, text="Awaiting Ticker...", font=ctk.CTkFont(size=18), text_color=self.text_main)
        self.name_label.pack(side="left", padx=15, pady=15)

        self.price_label = ctk.CTkLabel(self.status_frame, text="$0.00", font=ctk.CTkFont(size=24, weight="bold"), text_color=self.text_main)
        self.price_label.pack(side="right", padx=15, pady=15)

        # --- Squeeze Core Metrics Board ---
        self.metrics_container = ctk.CTkFrame(self, fg_color="transparent")
        self.metrics_container.pack(fill="x", padx=20, pady=10)
        
        self.metrics_container.grid_columnconfigure(0, weight=1)
        self.metrics_container.grid_columnconfigure(1, weight=1)
        self.metrics_container.grid_columnconfigure(2, weight=1)

        # Short Interest Box
        self.box_si = self._create_metric_box(self.metrics_container, "Short Interest", "--%", 0)
        # Volume Box
        self.box_vol = self._create_metric_box(self.metrics_container, "Rel Volume", "--x", 1)
        # DTC Box
        self.box_dtc = self._create_metric_box(self.metrics_container, "Days To Cover", "--", 2)

        # --- Rule Checklist (Epiphany Guardrails) ---
        self.rules_frame = ctk.CTkFrame(self, fg_color=self.panel_color, corner_radius=10)
        self.rules_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        ctk.CTkLabel(self.rules_frame, text="🛡️ Midas Squeeze Protocol", font=ctk.CTkFont(size=18, weight="bold"), text_color=self.accent_gold).pack(pady=(15, 5))
        
        # 1D:1m
        self.cb_1m = ctk.CTkCheckBox(self.rules_frame, text="1D:1m | Watch the first 15 mins for Panic Covering vs Short Attack", font=ctk.CTkFont(size=14))
        self.cb_1m.pack(anchor="w", padx=20, pady=10)
        
        # 10D:30m
        self.cb_30m = ctk.CTkCheckBox(self.rules_frame, text="10D:30m | The 'Sweet Spot'. Filter noise but catch momentum shifts.", font=ctk.CTkFont(size=14))
        self.cb_30m.pack(anchor="w", padx=20, pady=10)
        
        # 20D:1h
        self.cb_1h = ctk.CTkCheckBox(self.rules_frame, text="20D:1h | Strategic View. Ensure 'Bull Flag' and $ levels hold intact.", font=ctk.CTkFont(size=14))
        self.cb_1h.pack(anchor="w", padx=20, pady=10)
        
        # Option Volume
        self.cb_opt = ctk.CTkCheckBox(self.rules_frame, text="Options | Check volume & open interest anomalies ('The Spark').", font=ctk.CTkFont(size=14))
        self.cb_opt.pack(anchor="w", padx=20, pady=10)

    def _create_metric_box(self, parent, title, initial_val, col):
        frame = ctk.CTkFrame(parent, fg_color=self.panel_color, corner_radius=8)
        frame.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
        
        lbl_title = ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=12), text_color=self.text_sub)
        lbl_title.pack(pady=(10, 0))
        
        lbl_val = ctk.CTkLabel(frame, text=initial_val, font=ctk.CTkFont(size=22, weight="bold"), text_color=self.accent_teal)
        lbl_val.pack(pady=(0, 10))
        
        return lbl_val  # Return label to update later

    def fetch_data(self):
        symbol = self.symbol_entry.get().strip().upper()
        if not symbol: return
        
        self.name_label.configure(text=f"Scanning {symbol}...")
        self.track_btn.configure(state="disabled")
        
        def _fetch():
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                
                # Extract specifics
                name = info.get('shortName', symbol)
                price = info.get('currentPrice', info.get('regularMarketPrice', 0))
                short_ratio = info.get('shortPercentFloat', 0)
                dtc = info.get('shortRatio', 0)  # Days to cover
                
                vol = info.get('volume', 0)
                avg_vol = info.get('averageVolume10days', 1)
                if not avg_vol: avg_vol = 1
                rel_vol = vol / avg_vol
                
                # Safely format UI updates back on main thread
                # Midas rule -> Short Float above 30% is gold. Let's color code it.
                si_pct = (short_ratio or 0) * 100
                si_text = f"{si_pct:.1f}%"
                si_color = "#2ECC71" if si_pct > 25 else self.accent_teal
                
                dtc_text = f"{dtc:.1f}" if dtc else "--"
                dtc_color = "#2ECC71" if dtc and dtc > 5 else self.accent_teal
                
                rv_text = f"{rel_vol:.1f}x"
                rv_color = "#2ECC71" if rel_vol > 1.5 else self.accent_teal
                
                self.name_label.configure(text=f"{symbol} - {name}")
                self.price_label.configure(text=f"${price:,.2f}")
                
                self.box_si.configure(text=si_text, text_color=si_color)
                self.box_dtc.configure(text=dtc_text, text_color=dtc_color)
                self.box_vol.configure(text=rv_text, text_color=rv_color)
                
            except Exception as e:
                self.name_label.configure(text=f"Error fetching {symbol}")
                print(f"[Tracker] Error: {e}")
            finally:
                self.track_btn.configure(state="normal")
                
        threading.Thread(target=_fetch, daemon=True).start()

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("100x100")
    app.withdraw() # Hide root
    tracker = SqueezeTrackerWindow(app)
    tracker.mainloop()
