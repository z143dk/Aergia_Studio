# SwitchBot AI Hub & Holographic Avatar Conversation (Hestia Integration)

**Date:** June 7, 2026
**Project:** Hestia (Smart Home, Health & Device Sync)

## 1. Hardware Selection: iPad Pro 11-inch (M2) & Hologram Pyramids

### Compatible 360-Degree Pyramid Kits
Several professional-grade kits designed for tablets in the 11-inch range can support the weight of the SwitchBot camera:
- **Holapex VIVID Hologram Pyramid:** Highly recommended for iPad Pro. Fits 7" to 12" displays. Durable plastic with a matte black "hat" cover.
  - *Durability:* Holds up to 5 lbs (safe for the 6.9 oz SwitchBot indoor 3K camera).
  - *Software:* Holapex Hologram Video Creator app (iPadOS 13.0+) converts standard videos to 4-sided holographic videos.
- **Pixel XL by Holusion:** Premium holographic pyramid for 10" to 13" tablets. Creates a floating 3D illusion directly under the iPad Pro with 360° visibility.
- **Hologram Pyramid HD Acrylic:** Heavy-duty acrylic/plastic panels for 8-13 inch tablets. Rigid, non-folding structure ideal for permanent desk placement.

| Feature / Detail | Holapex VIVID | Pixel XL |
| :--- | :--- | :--- |
| **Tablet Size** | 7" to 12" | 10" to 13" |
| **Weight Capacity** | 5 lbs | High (Professional grade) |
| **Visibility** | 360 Degrees | 360 Degrees |
| **Software Support** | Native App available | Custom/Universal content |

### Engineering Tips for iPad Pro (M2)
1. **Deep Blacks are Key:** Render the avatar against a pitch-black background so the iPad screen blends into the darkness, making the reflection look floating.
2. **Screen Brightness:** Keep the iPad Pro's display at 100% brightness for crisp reflections.
3. **Lining Up the Image:** Place an alignment "cross" in the center of the video file to perfectly center the pyramid point with the tablet's screen.

---

## 2. SwitchBot AI Hub & Software Stack

The SwitchBot AI Hub can act as the local agent for home monitoring, bridged with a laptop for development.

### Stack Breakdown
- **Central Orchestration (Home Assistant):** Can run directly on the SwitchBot AI Hub. Offers a web interface accessible via the Hub's IP address.
- **AI & Logic (OpenClaw + Hermes):**
  - **OpenClaw:** Run via the SwitchBot App (`AI Hub > Settings > OpenClaw Setup`) to enable conversational device control.
  - **Hermes:** A fast execution framework with a "Hermes Desktop" entry point, excellent checkpoint/rollback system, and easier learning path. Useful for multi-agent teams.
- **Video Intelligence (Frigate):** Local object detection for 3K cameras, accessed via `AI Hub > Settings > Frigate Setup`.
- **Custom Development:**
  - **SwitchBot Open API:** Obtained via "Developer Options" in the SwitchBot App (unlocked by tapping App Version 10–15 times under Profile > Preference).
  - **Gemini Integration:** Connect Google AI Pro/Gemini API to Home Assistant/OpenClaw/Hermes to act as the primary brain.

---

## 3. Setup & Integrations

### Apple HomeKit Setup (via Matter)
To resolve the pairing issues:
1. Ensure a Matter controller (HomePod mini, Apple TV, etc.) is connected to your Apple ID.
2. Go to **AI Hub > Settings > Matter Setup** in the SwitchBot app and copy the Matter pairing code.
3. In the Apple Home App, tap **+** > **Add Accessory** > **More options** > **My Accessory Isn't Shown Here** > **Enter code** and paste the code.
4. Manually add sub-devices (cameras) by selecting **Secondary Devices** on the Hub's Matter setup page in the SwitchBot app.

### Suggested Development Workflow

| Task | Best Hardware for the Job |
| :--- | :--- |
| **Presence Detection** | SwitchBot AI Hub + SwitchBot 3K Cameras. |
| **3D Modeling & Animation** | Laptop (Blender, VTuber Maker, etc.). |
| **Conversational "Brain"** | Laptop/Cloud (OpenAI / Gemini API, Hermes SDK). |
| **Smart Home Triggers** | SwitchBot AI Hub (via OpenClaw or Home Assistant). |
