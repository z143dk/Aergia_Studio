# SwitchBot AI Hub & Holographic Avatar Conversation (Hermes Reference)

**Date:** June 7, 2026

## 1. Hardware Selection: iPad Pro 11-inch (M2) & Hologram Pyramids

### Compatible 360-Degree Pyramid Kits
- **Holapex VIVID Hologram Pyramid:** Fits 7" to 12" displays. Fully assembled pyramid holds up to 5 lbs (safe for the 6.9 oz SwitchBot indoor 3K camera).
- **Pixel XL by Holusion:** Premium holographic pyramid for 10" to 13" tablets. Creates floating 3D illusion directly under iPad Pro.
- **Hologram Pyramid HD Acrylic:** Heavy-duty acrylic/plastic panels for 8-13 inch tablets. Rigid, non-folding structure.

### Engineering Tips for iPad Pro (M2)
1. **Deep Blacks are Key:** Render the avatar against a pitch-black background.
2. **Screen Brightness:** Keep the iPad Pro's display at 100% brightness.
3. **Lining Up the Image:** Place a "cross" in the center of the video file to perfectly center the pyramid.

---

## 2. SwitchBot AI Hub & Software Stack

- **Central Orchestration (Home Assistant):** Can run directly on the SwitchBot AI Hub.
- **AI & Logic (OpenClaw + Hermes):**
  - **OpenClaw:** Run via the SwitchBot App (`AI Hub > Settings > OpenClaw Setup`).
  - **Hermes:** Low-latency execution framework; can run side-by-side with OpenClaw.
- **Video Intelligence (Frigate):** Local object detection for 3K cameras.
- **Custom Development:**
  - **SwitchBot Open API:** Secret Key and Token from App "Developer Options".
  - **Gemini Integration:** Connect Google AI Pro/Gemini to Home Assistant/OpenClaw/Hermes.

---

## 3. Setup & Integrations

### Apple HomeKit Setup (via Matter)
1. Ensure Matter controller (HomePod mini, Apple TV, etc.) is connected.
2. Navigate to **AI Hub > Settings > Matter Setup** in the SwitchBot app, copy Matter pairing code.
3. In the Apple Home App, tap **+** > **Add Accessory** > **More options** > **My Accessory Isn't Shown Here** > **Enter code** and paste.
4. Add secondary camera devices manually on the Hub's Matter setup page in the SwitchBot app.
