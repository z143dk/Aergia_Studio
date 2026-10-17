import customtkinter as ctk
import os
import sys
import threading
import time
from PIL import Image

# Ensure Root is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Ensure Project Midas is in path (for Schwab API)
midas_dir = os.path.join(parent_dir, "Project Midas")
if midas_dir not in sys.path:
    sys.path.append(midas_dir)

# Import Router for Credits
from intelligence_router import router
from router.registry import ProviderIDs

# Import Schwab (Reusing Midas Logic if available)
try:
    from schwab_api.client import SchwabClient
    HAS_SCHWAB = True
except ImportError:
    HAS_SCHWAB = False

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green") 

class PlutusTreasury(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Plutus - Treasury & Resources")
        self.geometry("900x600")

        # --- Aergia Theme Assets ---
        bg_path = os.path.join(parent_dir, "Aergia_Web", "static", "assets", "wallpapers", "The_Opening_Frame.png")
        if os.path.exists(bg_path):
            self.bg_image = ctk.CTkImage(Image.open(bg_path), size=(900, 600))
            self.bg_label = ctk.CTkLabel(self, text="", image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="#0b1a20", bg_color="transparent")
        self.header_frame.pack(fill="x", padx=10, pady=5)
        
        banner_path = os.path.join(parent_dir, "Aergia_Web", "static", "assets", "banners", "Plutus_Banner.png")
        if os.path.exists(banner_path):
             self.banner_img = ctk.CTkImage(Image.open(banner_path), size=(210, 80))
             self.banner_label = ctk.CTkLabel(self.header_frame, text="", image=self.banner_img)
             self.banner_label.pack(side="left", padx=10, pady=5)
        
        ctk.CTkLabel(self.header_frame, text="Bank of Aergia", font=("Roboto", 24, "bold"), text_color="#f1c40f").pack(side="left", padx=10)

        self.btn_refresh = ctk.CTkButton(self.header_frame, text="🔄 Refresh Balances", command=self.refresh_all, fg_color="#f39c12", hover_color="#d35400", text_color="black")
        self.btn_refresh.pack(side="right", padx=10)

        # Content Area
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)

        # --- LEFT: API Resources ---
        self.frame_api = ctk.CTkFrame(self.content_frame, fg_color="#1a1a1a")
        self.frame_api.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(self.frame_api, text="⚡ API CREDITS (The Fuel)", font=("Roboto", 18, "bold"), text_color="#3498db").pack(pady=15)

        # OpenRouter
        self.lbl_or = ctk.CTkLabel(self.frame_api, text="OpenRouter (Intelligence)", font=("Roboto", 14, "bold"))
        self.lbl_or.pack(pady=(10, 0))
        self.val_or = ctk.CTkLabel(self.frame_api, text="Fetching...", font=("Consolas", 16, "bold"), text_color="#ecc19c")
        self.val_or.pack(pady=(0, 10))

        # FAL
        self.lbl_fal = ctk.CTkLabel(self.frame_api, text="FAL.ai (Video Generation)", font=("Roboto", 14, "bold"))
        self.lbl_fal.pack(pady=(10, 0))
        self.val_fal = ctk.CTkLabel(self.frame_api, text="Fetching...", font=("Consolas", 16, "bold"), text_color="#ecc19c")
        self.val_fal.pack(pady=(0, 10))

        # Google
        self.lbl_goog = ctk.CTkLabel(self.frame_api, text="Google Gemini (Midas Brain)", font=("Roboto", 14, "bold"))
        self.lbl_goog.pack(pady=(10, 0))
        self.val_goog = ctk.CTkLabel(self.frame_api, text="Paid via Card (Post-Pay)", font=("Consolas", 16), text_color="gray")
        self.val_goog.pack(pady=(0, 10))


        # --- RIGHT: Financial Assets ---
        self.frame_fin = ctk.CTkFrame(self.content_frame, fg_color="#1a1a1a")
        self.frame_fin.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(self.frame_fin, text="🏛️ TREASURY (The Vault)", font=("Roboto", 18, "bold"), text_color="#2ecc71").pack(pady=15)

        if HAS_SCHWAB:
            self.lbl_schwab = ctk.CTkLabel(self.frame_fin, text="Schwab Accounts (Total)", font=("Roboto", 14, "bold"))
            self.lbl_schwab.pack(pady=(10, 0))
            self.val_schwab = ctk.CTkLabel(self.frame_fin, text="Fetching...", font=("Consolas", 24, "bold"), text_color="#27ae60")
            self.val_schwab.pack(pady=(0, 10))
            
            self.schwab_details = ctk.CTkTextbox(self.frame_fin, height=200, fg_color="#000", text_color="#2ecc71")
            self.schwab_details.pack(fill="x", padx=15, pady=10)
        else:
            ctk.CTkLabel(self.frame_fin, text="Schwab Client Not Found").pack(pady=20)

        # Status Footer
        self.status = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.status.pack(side="bottom", pady=5)

        # Auto-Load
        self.after(1000, self.refresh_all)

    def refresh_all(self):
        self.btn_refresh.configure(state="disabled", text="Loading...")
        threading.Thread(target=self._run_audit).start()

    def _run_audit(self):
        # 1. OpenRouter
        try:
            # We need to access the provider instance directly
            # This is a bit of a hack into the registry
            if router.registry.has(ProviderIDs.OPENROUTER_DEEPSEEK_V3):
                prov = router.registry.get(ProviderIDs.OPENROUTER_DEEPSEEK_V3)
                if hasattr(prov, 'check_credits'):
                    data = prov.check_credits()
                    # Parse logic
                    usage = data.get('usage', 0)
                    limit = data.get('limit')
                    
                    if limit is None:
                        display = foo = f"Usage: ${usage:.2f} (No Limit)"
                    else:
                        remaining = float(limit) - float(usage)
                        display = f"Rem: ${remaining:.2f} (Used: ${usage:.2f})"
                        
                    self.update_label(self.val_or, display)
                else:
                    self.update_label(self.val_or, "Not Supported")
            else:
                 self.update_label(self.val_or, "Not Configured")
        except Exception as e:
            self.update_label(self.val_or, "Error")
            print(e)

        # 2. FAL
        try:
            if router.registry.has(ProviderIDs.FAL_FLUX_SCHNELL):
                prov = router.registry.get(ProviderIDs.FAL_FLUX_SCHNELL)
                if hasattr(prov, 'check_balance'):
                    data = prov.check_balance()
                    note = data.get('note', 'Unknown')
                    self.update_label(self.val_fal, note)
        except:
             self.update_label(self.val_fal, "Error")

        # 3. Schwab
        if HAS_SCHWAB:
            try:
                client = SchwabClient()
                accts = client.get_account_numbers()
                total_liq = 0
                details = ""
                
                for acct in accts:
                    h = acct.get('hashValue')
                    num = acct.get('accountNumber', 'xxxx')[-4:]
                    bal = client.get_account_balance(h)
                    liq = bal.get('securitiesAccount', {}).get('currentBalances', {}).get('liquidationValue', 0)
                    total_liq += liq
                    details += f"Acct ..{num}: ${liq:,.2f}\n"
                
                self.update_label(self.val_schwab, f"${total_liq:,.2f}")
                
                def _upd_text():
                    self.schwab_details.delete("0.0", "end")
                    self.schwab_details.insert("0.0", details)
                self.after(0, _upd_text)
                
            except Exception as e:
                self.update_label(self.val_schwab, "Auth Error")
                print(e)

        # Reset Init
        self.after(0, lambda: self.btn_refresh.configure(state="normal", text="🔄 Refresh Balances"))
        self.after(0, lambda: self.status.configure(text=f"Last Updated: {time.strftime('%H:%M:%S')}"))

    def update_label(self, label, text):
        self.after(0, lambda: label.configure(text=text))

if __name__ == "__main__":
    app = PlutusTreasury()
    app.mainloop()
