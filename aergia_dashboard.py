import os
import sys
import subprocess
import webbrowser
import customtkinter as ctk
from tkinter import messagebox

# ---------- CONFIG ----------
AERGIA_ROOT = os.path.dirname(os.path.abspath(__file__))

# Projects (adjust if your folder names differ)
MIDAS_PATH = os.path.join(AERGIA_ROOT, "Project Midas", "midas_home.py")
CHIMERA_PATH = os.path.join(AERGIA_ROOT, "Project Chimera", "project-chimera", "backend-flask", "app.py")
HYPERION_PATH = os.path.join(AERGIA_ROOT, "Project Hyperion", "hyperion_gui.py")

# External portals
ATHENA_URL = "https://apps.abacus.ai/chatllm"
HEPHAESTUS_URL = "https://antigravity.abacus.ai/"
PROMETHEUS_URL = "https://aistudio.google.com/"     # Gemini / Google AI Studio

# ---------- UI SETUP ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class AergiaDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Project Aergia OS - The Pantheon (Phase 3)")
        self.geometry("1000x650")

        # Top title
        self.header = ctk.CTkLabel(
            self,
            text="PROJECT AERGIA OS — THE PANTHEON",
            font=ctk.CTkFont(size=26, weight="bold"),
        )
        self.header.pack(pady=20)

        # Brain Bar Frame
        self.brain_frame = ctk.CTkFrame(self, corner_radius=12)
        self.brain_frame.pack(fill="x", padx=30, pady=10)

        self.brain_label = ctk.CTkLabel(
            self.brain_frame,
            text="🧠 Brain Bar — Choose Your Intelligence Lane",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        self.brain_label.pack(pady=10)

        self.brain_buttons_frame = ctk.CTkFrame(self.brain_frame, fg_color="transparent")
        self.brain_buttons_frame.pack(pady=10)

        self.athena_btn = ctk.CTkButton(
            self.brain_buttons_frame,
            text="ATHENA (Strategy & Planning)",
            width=260,
            command=self.open_athena
        )
        self.athena_btn.grid(row=0, column=0, padx=10, pady=8)

        self.prometheus_btn = ctk.CTkButton(
            self.brain_buttons_frame,
            text="PROMETHEUS (Simulation & Thinking)",
            width=260,
            command=self.open_prometheus
        )
        self.prometheus_btn.grid(row=0, column=1, padx=10, pady=8)

        self.hephaestus_btn = ctk.CTkButton(
            self.brain_buttons_frame,
            text="HEPHAESTUS (Build & Forge)",
            width=260,
            command=self.open_hephaestus
        )
        self.hephaestus_btn.grid(row=0, column=2, padx=10, pady=8)

        # Active Projects Frame
        self.active_frame = ctk.CTkFrame(self, corner_radius=12)
        self.active_frame.pack(fill="x", padx=30, pady=15)

        self.active_label = ctk.CTkLabel(
            self.active_frame,
            text="⚡ Active Modules",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        self.active_label.pack(pady=10)

        self.active_buttons_frame = ctk.CTkFrame(self.active_frame, fg_color="transparent")
        self.active_buttons_frame.pack(pady=10)

        self.midas_btn = ctk.CTkButton(
            self.active_buttons_frame,
            text="PROJECT MIDAS (Financial Engine)",
            width=300,
            command=self.launch_midas
        )
        self.midas_btn.grid(row=0, column=0, padx=15, pady=10)

        self.chimera_btn = ctk.CTkButton(
            self.active_buttons_frame,
            text="PROJECT CHIMERA (Video Engine)",
            width=300,
            command=self.launch_chimera
        )
        self.chimera_btn.grid(row=0, column=1, padx=15, pady=10)

        self.hyperion_btn = ctk.CTkButton(
            self.active_buttons_frame,
            text="PROJECT HYPERION (AI Director)",
            width=300,
            command=self.launch_hyperion
        )
        self.hyperion_btn.grid(row=0, column=2, padx=15, pady=10)

        # Planned Projects Frame
        self.planned_frame = ctk.CTkFrame(self, corner_radius=12)
        self.planned_frame.pack(fill="x", padx=30, pady=15)

        self.planned_label = ctk.CTkLabel(
            self.planned_frame,
            text="🔥 Planned Expansions",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        self.planned_label.pack(pady=10)

        self.planned_buttons_frame = ctk.CTkFrame(self.planned_frame, fg_color="transparent")
        self.planned_buttons_frame.pack(pady=10)

        self.hestia_btn = ctk.CTkButton(
            self.planned_buttons_frame,
            text="PROJECT HESTIA (The Hearth)",
            width=300,
            command=self.launch_hestia
        )
        self.hestia_btn.grid(row=0, column=0, padx=15, pady=10)

        self.kairos_btn = ctk.CTkButton(
            self.planned_buttons_frame,
            text="PROJECT KAIROS (Time / Scheduler)",
            width=300,
            command=self.kairos_placeholder
        )
        self.kairos_btn.grid(row=0, column=1, padx=15, pady=10)

        # Footer
        self.footer = ctk.CTkLabel(
            self,
            text="Phase 3 Active — The Pantheon Online",
            font=ctk.CTkFont(size=14),
        )
        self.footer.pack(pady=20)

    # ---------- Helpers ----------
    def _launch_python(self, script_path: str):
        if not os.path.exists(script_path):
            messagebox.showerror("Not Found", f"Could not find:\n{script_path}")
            return
        try:
            # Use separate process with a new console window
            subprocess.Popen(
                [sys.executable, script_path],
                cwd=os.path.dirname(script_path),
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        except Exception as e:
            messagebox.showerror("Launch Error", str(e))

    # ---------- Brain Bar Actions ----------
    def open_athena(self):
        webbrowser.open(ATHENA_URL)

    def open_prometheus(self):
        webbrowser.open(PROMETHEUS_URL)

    def open_hephaestus(self):
        webbrowser.open(HEPHAESTUS_URL)

    # ---------- Module Launch Actions ----------
    def launch_midas(self):
        self._launch_python(MIDAS_PATH)

    def launch_chimera(self):
        self._launch_python(CHIMERA_PATH)

    def launch_hyperion(self):
        self._launch_python(HYPERION_PATH)

    def launch_hestia(self):
        webbrowser.open("http://localhost:8501")

    # ---------- Placeholders ----------
    def kairos_placeholder(self):
        messagebox.showinfo("Coming Soon", "Project Kairos (Scheduling) is planned but not yet wired in.")


if __name__ == "__main__":
    app = AergiaDashboard()
    app.mainloop()
