# PROJECT AERGIA: SYSTEM MEMORY & STATUS REPORT
**Date:** January 6, 2026
**Version:** 2.0 (Phase 3 Active)
**Architecture:** Distributed AI Operating System (Python/Flask/React)

---

## 1. THE CORE INFRASTRUCTURE (The OS)
We have built a centralized ecosystem called **"The Aergia Pantheon"**.

### 🖥️ Aergia Dashboard (`aergia_dashboard.py`)
*   **Function:** Master Control Panel.
*   **Recent Upgrade:** Added the **"Brain Bar"**—a command row connecting the three intelligences:
    1.  **Project Athena (ChatLLM):** Strategy & Planning.
    2.  **Project Prometheus (Gemini):** Simulation & Thinking.
    3.  **Project Hephaestus (Antigravity):** Building & Forge.
*   **Tech:** CustomTkinter, Python, Subprocess Launchers.

### 🧠 Intelligence Router (`intelligence_router.py`)
*   **Function:** Central Brain for all apps.
*   **Status:** **UPGRADED (Phase 3).**
    *   Removed legacy Google SDKs.
    *   Converted to Pure REST Architecture.
    *   **Connected To:** **DeepSeek V3** (Creative/Coding) and **DeepSeek R1** (Reasoning) via OpenRouter.
    *   **Capabilities:** Can switch between "Speed," "Reasoning," and "Creative" modes dynamically.

---

## 2. THE APP MODULES (The Gods)

### 💰 PROJECT MIDAS (Financial Engine)
*   **Goal:** Automated Swing Trading & Income Generation.
*   **Status:** **ACTIVE**.
*   **Features Built:**
    *   **Portfolio Dashboard:** Tracks Live (Schwab) vs. Paper ($25k Virtual) accounts.
    *   **Multi-Account Logic:** Separates Personal vs. Business (AXL LLC).
    *   **Auto-Charting:** Generates HTML charts for signals using `plotly`.
    *   **Mobile Briefings:** Synthesizes daily portfolio news into MP3 and texts it to user (Verizon MMS).

### 🎬 PROJECT CHIMERA (Video Engine)
*   **Goal:** Faceless Viral Content Creation (TikTok/YouTube).
*   **Status:** **PRODUCTION READY**.
*   **Architecture:**
    *   **Worker (`worker.py`):** Background service that processes video jobs.
    *   **AI Provider:** **FAL.ai (Minimax-Video)** for high-quality generation.
    *   **Audio:** EdgeTTS for voiceovers.
    *   **Fixes Implemented:**
        *   Resolved "Port 8081" conflict (Standardized to 5001).
        *   Fixed MoviePy 2.0 resizing bugs ("Ken Burns" effect).

### 👁️ PROJECT HYPERION (AI Director)
*   **Goal:** Creative Interface for Chimera.
*   **Status:** **ONLINE**.
*   **Features:**
    *   **Director Mode:** User types a rough idea -> AI writes the Script & Prompts.
    *   **Integration:** Directly submits jobs to Chimera Worker.
    *   **Upgrade:** Now uses **DeepSeek V3** (via Router) for high-creativity scriptwriting.

---

## 3. PLANNED EXPANSION (Phase 3 & 4)

### 🏠 PROJECT HESTIA (The Hearth)
*   **Goal:** Smart Home & Health.
*   **Plan:** Connect iPhone/iPad to PC for local data sync.
*   **Tech:** Apple HomeKit Bridge + Local Calendars (projected).

### ⏳ PROJECT KAIROS (Time)
*   **Goal:** AI Scheduling Agent.
*   **Plan:** Ingest appointments to optimize the user's day.

---

## 4. HARDWARE STRATEGY
### 🛡️ Project MagHub (The "Digital Soul")
*   **Device:** MagHub Go (2TB NVMe SSD).
*   **Security:** Hardware Fingerprint Encryption.
*   **Workflow:**
    *   **Portable Python:** The entire ecosystem runs directly off the drive.
    *   **Security:** Financial Keys (Midas) are physically removed from the PC when the drive is unplugged.
    *   **Multi-Device:** Plug-and-play on any Windows machine.

---

## 5. TECHNICAL CONTEXT FOR AI
*   **Root Directory:** `C:\Users\z143d\Aergia_Studio`
*   **API Management:** Managed via `.env` (DeepSeek, FAL, Schwab, Google, Coinbase).
*   **Database:** SQLite (`chimera.db`) for lightweight local storage.
