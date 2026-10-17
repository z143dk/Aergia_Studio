# Aergia Studio: Project Vision & Architecture (2026)

## 1. The Concept: "The Lazy Genius"
**Aergia Studio** began as a personalized digital heirloom and dashboard but has fundamentally evolved into an **Agentic AI Operating System**. It is designed around the core philosophy of "High-output, low-friction, local-first AI orchestration."

We have moved away from standalone scripts and manual API usage into an **Agentic Loop** architecture. Aergia acts as a central coordinator ("The Pantheon") where specialized AI agents (the "Gods") handle distinct verticals of the user's life—from automated financial trading to viral video production. 

---

## 2. History & Pivots: How We Got Here

### Phase 1: The Monolith
- **Initial Setup:** We started with simple scripts, basic visual dashboards (`aergia_dashboard.py`), and direct SDK integrations.
- **Hardware Foundation:** Originally relied on physical devices (like "Project MagHub"), but after hardware failures and security compromises (desktop breach requiring new credit cards), the architecture had to shift.

### Phase 2: Distributed Processing
- **Networking & Compute:** Migrated fully off the compromised desktop and broken external drives. The ecosystem now runs securely and exclusively across two devices: the **MacBook Pro** and the **Ryzen Windows Laptop**.
- **Network Sync (Paused):** We began setting up Tailscale to synchronize the Mac and Windows laptops, but implementation is currently paused due to travel. (Note: Attempts to use Exo Labs for local clustering were unsuccessful and abandoned).

### Phase 3: The Agentic Pivot (Current State)
- **API Restructuring:** We pivoted away from heavy, localized, or manual SDKs in favor of a **Pure REST Architecture**.
- **The "Brain Bar":** Rebuilt the central dashboard to route natural language commands to specialized LLMs.
- **Model Upgrades:** Swapped legacy models for the ultimate cost/performance stack: **DeepSeek V3** (Creativity), **DeepSeek R1** (Reasoning/Finance), and **FAL.ai/Minimax** for high-end video generation.

---

## 3. Current Architecture & Structure

Aergia Studio is divided into specialized modules, coordinated by the OS "Brain."

### 🧠 The Core OS (Project Aergia)
- **Master UI:** `aergia_dashboard.py` serves as the visual command center.
- **The Intelligence Router:** `intelligence_router.py` acts as the system's neural network. It takes user commands (via text) and routes them to the cheapest/smartest model available via **OpenRouter**, determining whether a query requires "Speed," "Reasoning," or "Creative" execution.

### 💰 Project Midas (The Financial Engine)
- **Goal:** Automated Swing Trading & Portfolio Management.
- **Tech & APIs:** Python, Charles Schwab API (Equity Options), Coinbase API (Crypto).
- **Features:**
  - Parallel Live ($) vs. Paper ($25k virtual) portfolios.
  - Multi-account separation (Personal vs. Business / AXL LLC).
  - Daily mobile intelligence briefings sent via MMS (Verizon integration + EdgeTTS audio).

### 🎬 Project Chimera & Hyperion (The Media Factory)
- **Goal:** Faceless Viral Content Production (TikTok / YouTube) at ~$1.00/video.
- **Project Hyperion (The Director):** The frontend UI where the user types a rough idea. It uses DeepSeek V3/R1 to expand the idea into a full script and precise video prompts.
- **Project Chimera (The Worker):** The backend execution engine (`worker.py` / Flask API).
  - **Visuals:** Calls **FAL.ai (Minimax-Video)** for high-FPS, professional-grade generation.
  - **Audio:** Uses **EdgeTTS** for automated, natural-sounding voiceovers.

---

## 4. The Agentic Workflow
When you request a task through Aergia, the system follows a defined path:
1. **The Strategy (ChatLLM):** Understands the request, brainstorms logic, and creates a plan.
2. **The Simulation (Brain/Router):** Verifies the plan. (e.g., *Does the Schwab API accept this order?*)
3. **The Execution (Antigravity):** Agent writes code, updates scripts, executes the terminal, and deploys it across the Tailscale cluster.

---

## 5. Future Vision & Next Steps

Our living ecosystem is designed to be easily extensible. The priority is to solidify existing pipelines before expanding into physical automation.

- **Stabilize the Router:** Ensure `intelligence_router.py` reliably brokers all requests without manual intervention.
- **Full Automation in Midas:** Upgrade Midas from an alert/dashboard system into a fully execution-authorized "Smart Hedging" agent tracking live volatility.
- **Automate Chimera Publishing:** Connect the Chimera output folder to an auto-scheduler (Project Kairos) to push content directly to YouTube/TikTok.
- **Phase 4 Expansion (Hestia / Hermes Mission Control):** Bridge Aergia to the physical world via Apple HomeKit and local iOS sync for smart home and health integration.

This document serves as our "North Star." As we write new features, they must align with this decoupled, agent-driven, and local-first architecture.
