import sys
import os
import traceback
import datetime

log_file = "startup_error.log"

def log(msg):
    with open(log_file, "a") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")
    print(msg)

log("--- Starting Debug Midas ---")
log(f"CWD: {os.getcwd()}")
log(f"sys.path: {sys.path}")

try:
    log("Attempting imports...")
    import customtkinter as ctk
    from PIL import Image
    log("Basic imports success.")
    
    # Try importing functional modules
    log("Importing midas_home...")
    import midas_home
    
    log("Midas Home imported. initializing...")
    # We won't run the full app unless we want to test the GUI loop
    # But just importing it should trigger module-level errors
    
except Exception as e:
    log(f"CRITICAL ERROR: {e}")
    log(traceback.format_exc())

log("--- Debug Complete ---")
