#!/usr/bin/env python3
"""
Aergia Studio - Delta Sync Setup Automator

This script sets up the necessary prerequisites to allow lightning-fast
Differential Syncing (Rsync) between the Mac and the Windows Ryzen node over Tailscale.

Run this script once on the Mac to establish trust and configure the dashboard.
"""

import os
import sys
import subprocess
import json

WINDOWS_IP = "100.111.220.42"
WINDOWS_USER = "z143dk"

def print_banner():
    print("="*60)
    print(" 🧿 Aergia Delta Sync (Rsync) Setup")
    print("="*60)

def check_rsync():
    print("[*] Checking for local Rsync installation...")
    try:
        subprocess.run(["rsync", "--version"], capture_output=True, check=True)
        print("  ✅ Rsync is installed natively on this Mac.")
        return True
    except Exception:
        print("  ❌ Rsync not found. Please install it (e.g., `brew install rsync`).")
        return False

def check_tailscale_ssh():
    print(f"\n[*] Checking Tailscale SSH connection to Windows Node ({WINDOWS_IP})...")
    print("  (This may hang if the Windows node is offline or SSH is not enabled)")
    
    # We attempt a dummy SSH command via Tailscale to check connectivity
    cmd = ["tailscale", "ssh", f"{WINDOWS_USER}@{WINDOWS_IP}", "echo", "SSH_SUCCESS"]
    
    # Try using the explicit Mac path if 'tailscale' command isn't globally accessible
    if not os.path.exists("/Applications/Tailscale.app/Contents/MacOS/Tailscale"):
         cmd = ["tailscale", "ssh", f"{WINDOWS_USER}@{WINDOWS_IP}", "echo", "SSH_SUCCESS"]
    else:
         cmd = ["/Applications/Tailscale.app/Contents/MacOS/Tailscale", "ssh", f"{WINDOWS_USER}@{WINDOWS_IP}", "echo", "SSH_SUCCESS"]

    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if "SSH_SUCCESS" in result.stdout:
        print("  ✅ Tailscale SSH is fully configured and trusted!")
        return True
    else:
        print("  ❌ Tailscale SSH connection failed.")
        print("     Error details:", result.stderr.strip())
        print("\n--- ACTION REQUIRED ON WINDOWS LAPTOP ---")
        print("1. Open Tailscale settings on your Windows Ryzen laptop.")
        print("2. Go to 'Preferences' or 'Settings'.")
        print("3. Check the box that says 'Run Tailscale SSH'.")
        print("4. (Optional but recommended) Ensure Windows OpenSSH Server is installed.")
        print("-----------------------------------------")
        return False

def configure_paths():
    print("\n[*] Configuring Absolute Sync Paths...")
    mac_path = os.path.dirname(os.path.abspath(__file__))
    
    # Prompt the user for the exact Windows path
    print(f"  Mac Aergia Directory: {mac_path}")
    win_path = input("\nEnter the EXACT absolute path to Aergia_Studio on your Windows laptop\n(e.g., C:/Users/z143dk/Desktop/Aergia_Studio): ").strip()
    
    if not win_path:
        print("  ❌ Path cannot be empty. Aborting.")
        return False
        
    # Ensure Windows path uses forward slashes for Rsync compatibility
    win_path = win_path.replace("\\", "/")
    
    # Save the configuration to a file for the Dashboard API to use
    config = {
        "mac_path": mac_path,
        "windows_target": f"{WINDOWS_USER}@{WINDOWS_IP}:{win_path}"
    }
    
    config_file = os.path.join(mac_path, "sync_config.json")
    with open(config_file, "w") as f:
        json.dump(config, f, indent=4)
        
    print(f"  ✅ Configuration saved to {config_file}")
    return True

def main():
    print_banner()
    
    # 1. Verify local requirements
    if not check_rsync():
        sys.exit(1)
        
    # 2. Verify Tailscale SSH
    if not check_tailscale_ssh():
        print("\nFix the Windows Tailscale SSH settings, then run this script again.")
        sys.exit(1)
        
    # 3. Configure Paths
    if not configure_paths():
        sys.exit(1)
        
    print("\n" + "="*60)
    print(" 🎉 Setup Complete! Delta Sync is ready to use.")
    print(" You can now safely use the 'Deep Sync' button on the Web Dashboard.")
    print("="*60)

if __name__ == "__main__":
    main()
