# 🏛️ Project Aergia 2.0: The Agentic OS
**Version:** 2.0.0 (Phase 3: The Pantheon Reborn)
**Core Philosophy:** "Lazy Genius" — High-output, low-friction, local-first AI orchestration.
**Legacy:** Built as a digital heirloom and creative engine.

## 🛰️ System Architecture
*   **Root:** `C:\Users\z143d\Aergia_Studio`
*   **Tech Stack:** Python 3.12, Flask, React, SQLite (chimera.db)
*   **Launcher:** `Launch_Aergia.bat` (Pinned to Python 3.12.4)

## 🧿 The Pantheon (The 12 Gods)
Aergia is a modular system where each "God" represents a specific intelligence capability:

*   **Athena (Wisdom):** General reasoning and chat interface.
*   **Prometheus (Reasoning):** Deep research and long-form planning (Gemini).
*   **Hephaestus (Antigravity):** The Builder. Code generation and system maintenance.
*   **Aergia (Rest):** The Core Identity. Dashboard, UI, and system pacing.
*   **Hermes Mission Control (Travel):** API connectivity and external data routing. Distinct from the third-party Hermes Desktop framework.
*   **Aura (Energy):** UI/UX motion, transitions, and visual "breath."
*   **Hestia (Home):** Local environment stability and file persistence.
*   **Hyperion (Director):** The Conductor. Oversees multi-agent movie/story production.
*   **Midas (Gold):** The Financial Engine. Monetization, budgeting, and income tracking.
*   **Chimera (Creation):** The Media Engine. Video (Veo), Worlds (Genie), and Avatars (MultiTalk).
*   **Kairos (Time):** Scheduling, triggers, and automated posting.
*   **Plutus (Legacy):** Final archival, packaging, and YouTube/TikTok exports.

## ⚙️ Active Modules & Paths
The system uses a Subsystem Registry to locate nested modules:

| Module | Role | Path |
| :--- | :--- | :--- |
| **Dashboard** | Main UI | `aergia_dashboard.py` |
| **Midas** | Finance | `Project Midas\midas_home.py` |
| **Hyperion** | Director | `Project Hyperion\hyperion_gui.py` |
| **Chimera API** | Media Backend | `Project Chimera\...\backend-flask\app.py` |
| **MultiTalk** | Character Engine | `Project Chimera\...\backend-flask\worker.py` |

## 🛠️ Troubleshooting & Maintenance
*   **Python Path:** Always use the full path to `Python312\python.exe` to bypass Windows Store aliases.
*   **Port Collisions:** If Midas and Hyperion cannot run simultaneously, check for shared port usage (defaulting to 5000/8080).
*   **Chimera Worker:** Requires `import sys` at the top of `worker.py` for path resolution.

## 🚀 Roadmap (The Order)
1.  **Foundation:** Restore connectivity and launcher (DONE).
2.  **Documentation:** Establish the System Bible (DONE).
3.  **Orchestration:** Test the Router/Planner (NEXT).
4.  **Visuals:** Audit and display all 27 visual assets.
5.  **Atmosphere:** Generate the Rok Nardin-style theme.
6.  **Expansion:** Implement MultiTalk character branding for TikTok/YouTube.

✅ README Generated.
**Next Command in Order:** TEST ROUTER
