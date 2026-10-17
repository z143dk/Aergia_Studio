"""
AERGIA ORCHESTRATOR CONTROL CENTER
Desktop GUI for monitoring and controlling the Aergia OS Pantheon
"""

import customtkinter as ctk
from datetime import datetime
import threading
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

try:
    from intelligence_router import IntelligenceRouter
    from router.schemas import TaskRequest
except ImportError as e:
    print(f"Import Error: {e}")
    print("Make sure intelligence_router.py and router/ folder exist")
    sys.exit(1)


class AergiaOrchestratorGUI:
    def __init__(self):
        # Initialize router
        self.router = IntelligenceRouter()
        
        # Setup window
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.window = ctk.CTk()
        self.window.title("🏛️ AERGIA ORCHESTRATOR CONTROL CENTER v2.0")
        self.window.geometry("1400x900")
        
        # State
        self.is_executing = False
        
        # Build UI
        self._build_ui()
        
        # Start status updater
        self._update_status()
        
    def _build_ui(self):
        """Build the complete UI"""
        
        # ============ HEADER ============
        header_frame = ctk.CTkFrame(self.window, fg_color=("#1a1a2e", "#16213e"))
        header_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🏛️ AERGIA OS v2.0 - ORCHESTRATOR CONTROL CENTER",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        self.system_status_label = ctk.CTkLabel(
            header_frame,
            text="● ONLINE",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#00ff00"
        )
        self.system_status_label.pack(side="right", padx=20, pady=15)
        
        # ============ MAIN CONTAINER ============
        main_container = ctk.CTkFrame(self.window, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left Panel (Status)
        left_panel = ctk.CTkFrame(main_container, width=400)
        left_panel.pack(side="left", fill="both", padx=(0, 5))
        left_panel.pack_propagate(False)
        
        # Right Panel (Mission Control + Logs)
        right_panel = ctk.CTkFrame(main_container)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # ============ LEFT PANEL: PANTHEON STATUS ============
        status_title = ctk.CTkLabel(
            left_panel,
            text="📊 PANTHEON STATUS",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        status_title.pack(pady=(10, 20))
        
        # Scrollable frame for gods
        self.status_scroll = ctk.CTkScrollableFrame(left_panel, fg_color="transparent")
        self.status_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # God status cards
        self.god_cards = {}
        gods = [
            ("Athena", "🦉", "Strategy", "OpenRouter", "#3498db"),
            ("Prometheus", "🔥", "Reasoning", "Google Gemini", "#e74c3c"),
            ("Hephaestus", "⚒️", "Code Forge", "Antigravity", "#95a5a6"),
            ("Chimera", "🎬", "Video Engine", "FAL.ai", "#9b59b6"),
            ("Midas", "💰", "Financial", "Schwab+Coinbase", "#f39c12"),
            ("Hyperion", "☀️", "AI Director", "Mission Control", "#e67e22"),
        ]
        
        for name, icon, role, provider, color in gods:
            self._create_god_card(name, icon, role, provider, color)
        
        # ============ RIGHT PANEL: MISSION CONTROL ============
        mission_title = ctk.CTkLabel(
            right_panel,
            text="🎯 MISSION CONTROL",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        mission_title.pack(pady=(10, 10))
        
        # Mission input
        mission_label = ctk.CTkLabel(
            right_panel,
            text="Enter your mission:",
            font=ctk.CTkFont(size=14)
        )
        mission_label.pack(pady=(5, 5))
        
        self.mission_input = ctk.CTkTextbox(
            right_panel,
            height=100,
            font=ctk.CTkFont(size=14)
        )
        self.mission_input.pack(fill="x", padx=20, pady=5)
        self.mission_input.insert("1.0", "Check my BTC balance and analyze the trend")
        
        # Button row
        button_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        button_frame.pack(pady=10)
        
        self.orchestrate_btn = ctk.CTkButton(
            button_frame,
            text="🚀 ORCHESTRATE",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40,
            width=200,
            command=self._execute_orchestrate,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.orchestrate_btn.pack(side="left", padx=5)
        
        self.quick_task_btn = ctk.CTkButton(
            button_frame,
            text="⚡ QUICK TASK",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40,
            width=200,
            command=self._execute_quick_task,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        self.quick_task_btn.pack(side="left", padx=5)
        
        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="🔄 CLEAR",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40,
            width=150,
            command=self._clear_log,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        self.clear_btn.pack(side="left", padx=5)
        
        # ============ EXECUTION LOG ============
        log_title = ctk.CTkLabel(
            right_panel,
            text="📋 EXECUTION LOG",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        log_title.pack(pady=(20, 10))
        
        self.log_display = ctk.CTkTextbox(
            right_panel,
            font=ctk.CTkFont(size=12, family="Consolas"),
            wrap="word"
        )
        self.log_display.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Initial log message
        self._log("System initialized. Pantheon online. Ready for missions.")
        
        # ============ FOOTER ============
        footer_frame = ctk.CTkFrame(self.window, fg_color=("#1a1a2e", "#16213e"), height=40)
        footer_frame.pack(fill="x", padx=10, pady=10)
        footer_frame.pack_propagate(False)
        
        footer_label = ctk.CTkLabel(
            footer_frame,
            text="🌴 Built with Love in Hampton, VA | Powered by Recovery, Resilience, and Python",
            font=ctk.CTkFont(size=12)
        )
        footer_label.pack(pady=10)
        
    def _create_god_card(self, name, icon, role, provider, color):
        """Create a status card for a god"""
        card = ctk.CTkFrame(self.status_scroll, fg_color=color, corner_radius=10)
        card.pack(fill="x", pady=5)
        
        # Header
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=5)
        
        icon_label = ctk.CTkLabel(
            header_frame,
            text=icon,
            font=ctk.CTkFont(size=24)
        )
        icon_label.pack(side="left")
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=name,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        name_label.pack(side="left", padx=10)
        
        status_indicator = ctk.CTkLabel(
            header_frame,
            text="● ONLINE",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#00ff00"
        )
        status_indicator.pack(side="right")
        
        # Details
        role_label = ctk.CTkLabel(
            card,
            text=role,
            font=ctk.CTkFont(size=12),
            text_color="#ecf0f1"
        )
        role_label.pack(anchor="w", padx=10)
        
        provider_label = ctk.CTkLabel(
            card,
            text=provider,
            font=ctk.CTkFont(size=10),
            text_color="#bdc3c7"
        )
        provider_label.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Store references
        self.god_cards[name] = {
            'card': card,
            'status': status_indicator,
            'color': color
        }
        
    def _update_status(self):
        """Update god status (placeholder for now)"""
        # In a real implementation, this would ping each provider
        # For now, we'll just keep them all online
        self.window.after(5000, self._update_status)
        
    def _log(self, message, level="INFO"):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Color coding
        if level == "ERROR":
            prefix = "❌"
        elif level == "SUCCESS":
            prefix = "✓"
        elif level == "STEP":
            prefix = "→"
        else:
            prefix = "ℹ️"
        
        log_message = f"[{timestamp}] {prefix} {message}\n"
        self.log_display.insert("end", log_message)
        self.log_display.see("end")
        
    def _clear_log(self):
        """Clear the log display"""
        self.log_display.delete("1.0", "end")
        self._log("Log cleared. Ready for new missions.")
        
    def _execute_orchestrate(self):
        """Execute full orchestration with planning"""
        if self.is_executing:
            self._log("Mission already in progress. Please wait.", "ERROR")
            return
        
        mission = self.mission_input.get("1.0", "end").strip()
        if not mission:
            self._log("Please enter a mission.", "ERROR")
            return
        
        # Run in thread to avoid blocking UI
        thread = threading.Thread(target=self._run_orchestrate, args=(mission,))
        thread.daemon = True
        thread.start()
        
    def _run_orchestrate(self, mission):
        """Run orchestration in background thread"""
        self.is_executing = True
        self.orchestrate_btn.configure(state="disabled", text="🔄 EXECUTING...")
        
        try:
            self._log(f"Mission received: {mission}")
            self._log("Planning mission with Planner...", "STEP")
            
            # Call planner
            result = self.router.plan_and_execute(mission)
            
            self._log("Mission complete!", "SUCCESS")
            self._log(f"Result: {result[:500]}...")  # Truncate long results
            
        except Exception as e:
            self._log(f"Mission failed: {str(e)}", "ERROR")
            
        finally:
            self.is_executing = False
            self.orchestrate_btn.configure(state="normal", text="🚀 ORCHESTRATE")
            
    def _execute_quick_task(self):
        """Execute single task without planning"""
        if self.is_executing:
            self._log("Task already in progress. Please wait.", "ERROR")
            return
        
        task = self.mission_input.get("1.0", "end").strip()
        if not task:
            self._log("Please enter a task.", "ERROR")
            return
        
        # Run in thread
        thread = threading.Thread(target=self._run_quick_task, args=(task,))
        thread.daemon = True
        thread.start()
        
    def _run_quick_task(self, task):
        """Run quick task in background thread"""
        self.is_executing = True
        self.quick_task_btn.configure(state="disabled", text="⚡ RUNNING...")
        
        try:
            self._log(f"Quick task: {task}")
            
            # Create request
            req = TaskRequest(
                prompt=task,
                task_type="creative"  # Default to creative
            )
            
            # Execute
            result = self.router.execute(req)
            
            self._log("Task complete!", "SUCCESS")
            self._log(f"Result: {result.content[:500]}...")
            
        except Exception as e:
            self._log(f"Task failed: {str(e)}", "ERROR")
            
        finally:
            self.is_executing = False
            self.quick_task_btn.configure(state="normal", text="⚡ QUICK TASK")
            
    def run(self):
        """Start the GUI"""
        self.window.mainloop()


def main():
    """Entry point"""
    try:
        app = AergiaOrchestratorGUI()
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
