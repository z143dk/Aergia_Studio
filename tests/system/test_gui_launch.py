
import sys
import os
from aergia_orchestrator_gui import AergiaOrchestratorGUI
import customtkinter as ctk

def test_gui():
    print("Initializing GUI...")
    try:
        app = AergiaOrchestratorGUI()
        print("GUI Initialized Successfully.")
        
        # Schedule destruction after 2 seconds
        print("scheduling destruction...")
        app.window.after(2000, lambda: destroy_and_exit(app))
        
        print("Running mainloop...")
        app.run()
    except Exception as e:
        print(f"GUI Test Failed: {e}")
        sys.exit(1)

def destroy_and_exit(app):
    print("Destroying window...")
    app.window.destroy()
    print("GUI Test Passed")
    sys.exit(0)

if __name__ == "__main__":
    test_gui()
