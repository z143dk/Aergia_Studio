# 🌍 Project Aergia: Universal Remote Access Guide

Use this guide to access your Aergia Dashboard from your iPhone/iPad/MacBook.

---

## 🏠 Option A: SAME HOUSE (WiFi Only)
**Use this URL ONLY when your device is connected to the SAME WiFi network as this computer.**
(e.g., You are sitting on your couch at home).

👉 **http://[YOUR-MAC-IP]:5050**

*Note: The app runs on your Mac. Your iPad/iPhone acts as a remote control. You do NOT need to install files on the iPad.*

---

## ✈️ Option B: WORK / OVERSEAS (Tailscale VPN)
**Use this method when you are at the OFFICE, Hotel, or using Data (4G/5G).**

### 1. Setup (One-time)
*   **On THIS PC**: Install **Tailscale** (tailscale.com) and log in.
*   **On your iPhone/Work Laptop**: Install the **Tailscale App** and log in with the *same account*.

### 2. The "Magic" URL
Once both are connected to Tailscale:
1.  Tailscale will give you a computer name (e.g., `z143d-pc`).
2.  Your global access URL is:
    👉 **http://[YOUR-TAILSCALE-MACHINE-NAME]:3000**
    *(Or copy the "Tailscale IP" starting with 100.x.y.z from the app)*

This link works from ANYWHERE in the world, securely.

---

## 🍎 Apple HomeKit (Project Hestia)
*   **Status**: Library installed.
*   **Aura**: Edge nodes active.
*   **Hestia**: Ready to pair with HomeKit devices on your *Home Network*.

---

## ⚠️ Troubleshooting: "Site Can't Be Reached"
If you cannot connect from your phone, Windows Firewall is blocking it.

**The Fix (Must be done on this PC):**
1.  Click **Start**, type `PowerShell`.
2.  Right-click **Windows PowerShell** -> **Run as Administrator**.
3.  Paste this exact command and hit Enter:
    ```powershell
    netsh advfirewall firewall add rule name="Aergia Ecosystem" dir=in action=allow protocol=TCP localport=5050,5001,8081
    ```
4.  Try the link again on your phone.
