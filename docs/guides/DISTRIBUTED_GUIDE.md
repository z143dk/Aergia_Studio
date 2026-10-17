# Aergia & Midas: Distributed System Guide

This guide explains how to use the new features installed by Antigravity to connect your devices (Mac, Windows Desktop, Windows Laptop, iPad).

## 1. Midas: Weekly Schwab API Fix
We have created a new automated script to make the weekly re-authentication much easier (no more copy-pasting URLs).

**How to use:**
1. Open Terminal (or Command Prompt).
2. Navigate to your project folder:
   ```bash
   cd ~/Desktop/Aergia_Studio/Project\ Midas
   ```
3. Run the weekly setup script:
   ```bash
   python weekly_schwab_setup.py
   ```
4. A browser window will open. Log in to Schwab.
5. **That's it!** The script will automatically catch the redirect and save your new tokens.

---

## 2. iPad Pro Access (Aergia Dashboard)
You can access the full Aergia Studio dashboard from your iPad without installing anything.

1. **On your Mac** (or whichever computer runs Aergia):
   * Make sure `Launch_Web_Dashboard.bat` (Windows) or `python aergia_api.py` (Mac) is running.
   * Find your Mac's IP address. Open Terminal and type:
     ```bash
     ipconfig getifaddr en0
     ```
     (It will be something like `192.168.1.50`)

2. **On your iPad**:
   * Open Safari.
   * Go to: `http://192.168.1.50:5050` (Replace `192.168.1.50` with your actual IP).
   * **Pro Tip**: Tap the "Share" button in Safari -> "Add to Home Screen". This creates an "App" icon for Aergia.

---

## 3. Distributed Compute (Windows Delegator)
You can now use your 16-core Windows Desktop to "crunch numbers" for Midas running on your Mac.

**Setup:**
1. Ensure `Launch_Web_Dashboard.bat` is running on the **Windows Desktop**.
2. Note the Windows Desktop's IP address (e.g., `192.168.1.100`).

**How to send a job from Mac to Windows:**
You can use the new worker API. Here is a Python snippet to use in your Midas scripts:

```python
import requests

# The IP of your Windows Desktop
WINDOWS_WORKER_IP = "http://192.168.1.100:5050" 

task_payload = {
    "script": "crunch_data.py",  # The script inside Project Midas you want to run
    "args": ["--mode", "heavy_compute"],
    "cwd": "C:\\Users\\Desktop\\Aergia_Studio\\Project Midas" # Optional: ensure paths match Windows structure
}

try:
    response = requests.post(f"{WINDOWS_WORKER_IP}/api/worker/execute", json=task_payload)
    print("Job sent:", response.json())
except Exception as e:
    print("Failed to send job:", e)
```

---

## 4. Remote Access (Away from Home)
To access your system from your Ryzen Laptop while away:

1. **Do NOT open ports on your router** (unsafe).
2. **Install Tailscale** (free) on all your devices (Mac, Windows, iPad).
3. Tailscale assigns a "MagicDNS" name (e.g., `macbook-pro.tailscale.net`).
4. You can then access `http://macbook-pro:5050` from anywhere in the world securely.

---

## 5. Working on One Machine (Code Sync)

**Important**: Tailscale connects the *network*, but it does **NOT** automatically sync your files.

### To "Work on One and Update All":
You have two main options:

#### Option A: Git (Recommended)
1.  **Code** on your Mac.
2.  **Push** to GitHub (`git push`).
3.  **Pull** on your Windows Machine (`git pull`).
4.  *Use this if you want a backup and version history.*

#### Option B: VS Code Remote (Tailscale)
1.  Install **VS Code** on your Mac.
2.  Install the **Remote - SSH** extension.
3.  Connect to your Windows machine using its Tailscale IP (e.g., `ssh user@100.x.y.z`).
4.  *Use this if you want to edit files on the Windows machine without moving them.*

### For Exo / Aergia Cluster
Tailscale **IS** the magic link.
-   When running `exo` on your Mac, it broadcasts to the Tailscale network.
-   Your Windows machine (on the same Tailscale net) will "see" the Mac and join the cluster automatically if you use the `Join_Cluster.bat` script.
