"""
Aergia Studio Unified Mission Control Launcher
Cross-platform process launcher and orchestrator for Aergia Ecosystem.
"""

import os
import sys
import time
import argparse
import subprocess
import webbrowser
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
os.chdir(ROOT_DIR)

# Ensure ROOT_DIR is in PYTHONPATH
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
os.environ["PYTHONPATH"] = str(ROOT_DIR) + os.pathsep + os.environ.get("PYTHONPATH", "")

def get_python_exe():
    """Detect appropriate Python executable."""
    # Check current executable
    if sys.executable and os.path.exists(sys.executable):
        return sys.executable
    # Known Windows fallback
    win_py312 = r"C:\Users\z143d\AppData\Local\Programs\Python\Python312\python.exe"
    if os.name == "nt" and os.path.exists(win_py312):
        return win_py312
    return "python"

PYTHON = get_python_exe()

def launch_proc(cmd, title="Aergia Process", background=True, wait=False):
    """Launch a process cross-platform."""
    env = os.environ.copy()
    if os.name == "nt":
        if background:
            return subprocess.Popen(
                ["cmd.exe", "/c", "start", title] + cmd,
                cwd=str(ROOT_DIR),
                shell=False,
                env=env
            )
        else:
            return subprocess.run(cmd, cwd=str(ROOT_DIR), env=env)
    else:
        # Unix / macOS
        if background:
            return subprocess.Popen(cmd, cwd=str(ROOT_DIR), env=env)
        else:
            return subprocess.run(cmd, cwd=str(ROOT_DIR), env=env)

def start_health_server():
    print("[+] Starting Health Ops Flask Server on http://localhost:5000 ...")
    launch_proc([PYTHON, "health_ops_server.py"], title="Health Ops Server", background=True)

def start_health_gui():
    print("[+] Launching Health Ops Desktop Dashboard (Tkinter) ...")
    launch_proc([PYTHON, "health_ops_dashboard.py"], title="Health Ops Dashboard", background=True)

def start_health_ops():
    start_health_server()
    time.sleep(2)
    start_health_gui()

def start_api():
    print("[+] Starting Aergia API Server (The Brain) ...")
    launch_proc([PYTHON, "aergia_api.py"], title="Aergia API Server", background=True)

def start_orchestrator():
    print("[+] Launching Desktop Orchestrator ...")
    launch_proc([PYTHON, "aergia_orchestrator_gui.py"], title="Aergia Orchestrator", background=True)

def start_dashboard():
    print("[+] Launching Aergia Dashboard ...")
    launch_proc([PYTHON, "aergia_dashboard.py"], title="Aergia Dashboard", background=True)

def start_midas():
    print("[+] Launching Project Midas ...")
    midas_script = ROOT_DIR / "Project Midas" / "midas_home.py"
    if not midas_script.exists():
        midas_script = ROOT_DIR / "Project Midas" / "main.py"
    launch_proc([PYTHON, str(midas_script)], title="Project Midas", background=True)

def start_chimera():
    print("[+] Launching Project Chimera ...")
    chimera_dir = ROOT_DIR / "Project Chimera"
    if (chimera_dir / "start_chimera.bat").exists() and os.name == "nt":
        launch_proc([str(chimera_dir / "start_chimera.bat")], title="Chimera", background=True)
    elif (ROOT_DIR / "scripts" / "legacy_launchers" / "start_chimera.bat").exists():
        launch_proc([str(ROOT_DIR / "scripts" / "legacy_launchers" / "start_chimera.bat")], title="Chimera", background=True)
    else:
        print("[!] Chimera start script not located.")

def start_suite():
    print("\n" + "="*56)
    print("      🪐  AERGIA STUDIO: INITIALIZING FULL SUITE  🪐")
    print("="*56 + "\n")
    
    start_api()
    
    # Check Ollama if Windows
    if os.name == "nt":
        try:
            tasks = subprocess.check_output('tasklist /fi "imagename eq ollama.exe"', shell=True, text=True)
            if "ollama.exe" not in tasks.lower():
                print("[*] Starting local Ollama service...")
                subprocess.Popen(["cmd.exe", "/c", "start", "ollama"], shell=False)
            else:
                print("[*] Ollama service is already active.")
        except Exception:
            pass
            
    print("[*] Waiting for API server initialization...")
    time.sleep(3)
    
    start_orchestrator()
    time.sleep(1)
    
    print("[*] Opening Web Command Center at http://127.0.0.1:5050 ...")
    try:
        webbrowser.open("http://127.0.0.1:5050")
    except Exception:
        pass
        
    print("\n" + "="*56)
    print("                 ✨  ALL SYSTEMS ONLINE  ✨")
    print("="*56 + "\n")

def run_tests():
    print("[+] Running test suite in tests/ ...")
    subprocess.run([PYTHON, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"], cwd=str(ROOT_DIR))

def interactive_menu():
    while True:
        print("\n" + "="*60)
        print("    🪐  AERGIA STUDIO: UNIFIED MISSION CONTROL LAUNCHER")
        print("="*60)
        print("  [1] Full Aergia Suite (API Server + Orchestrator + Web UI)")
        print("  [2] Health Ops Platform (Server + Desktop Dashboard)")
        print("  [3] Health Ops Server Only (Port 5000)")
        print("  [4] Health Ops Dashboard Only (Tkinter GUI)")
        print("  [5] Desktop Orchestrator GUI")
        print("  [6] Aergia API Server")
        print("  [7] Project Midas (Trading Intelligence)")
        print("  [8] Project Chimera (Creative Swarm)")
        print("  [9] Run Test Suite")
        print("  [0] Exit")
        print("="*60)
        
        choice = input("\nSelect an option [0-9]: ").strip()
        if choice == "1":
            start_suite()
            break
        elif choice == "2":
            start_health_ops()
            break
        elif choice == "3":
            start_health_server()
            break
        elif choice == "4":
            start_health_gui()
            break
        elif choice == "5":
            start_orchestrator()
            break
        elif choice == "6":
            start_api()
            break
        elif choice == "7":
            start_midas()
            break
        elif choice == "8":
            start_chimera()
            break
        elif choice == "9":
            run_tests()
        elif choice in ("0", "q", "exit"):
            print("Exiting.")
            sys.exit(0)
        else:
            print("[!] Invalid selection. Please choose 0-9.")

def main():
    parser = argparse.ArgumentParser(description="Aergia Studio Unified Mission Control Launcher")
    parser.add_argument("--suite", "-s", action="store_true", help="Launch full Aergia Suite")
    parser.add_argument("--health", "-H", action="store_true", help="Launch Health Ops Suite (Server + Dashboard)")
    parser.add_argument("--health-server", action="store_true", help="Launch Health Ops Server only")
    parser.add_argument("--health-gui", action="store_true", help="Launch Health Ops Dashboard GUI only")
    parser.add_argument("--orchestrator", "-o", action="store_true", help="Launch Desktop Orchestrator GUI")
    parser.add_argument("--api", "-a", action="store_true", help="Launch Aergia API Server")
    parser.add_argument("--dashboard", "-d", action="store_true", help="Launch Aergia Dashboard")
    parser.add_argument("--midas", "-m", action="store_true", help="Launch Project Midas")
    parser.add_argument("--chimera", "-c", action="store_true", help="Launch Project Chimera")
    parser.add_argument("--test", "-t", action="store_true", help="Run test suite")
    
    args = parser.parse_args()
    
    if args.suite:
        start_suite()
    elif args.health:
        start_health_ops()
    elif args.health_server:
        start_health_server()
    elif args.health_gui:
        start_health_gui()
    elif args.orchestrator:
        start_orchestrator()
    elif args.api:
        start_api()
    elif args.dashboard:
        start_dashboard()
    elif args.midas:
        start_midas()
    elif args.chimera:
        start_chimera()
    elif args.test:
        run_tests()
    else:
        interactive_menu()

if __name__ == "__main__":
    main()
