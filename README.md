# 🪐 Aergia Studio: Local-First, Multi-Agent AI Mission Control & Orchestration
> **Portfolio Submission: Anthropic Claude Corps Fellows Program (AI Security Track)**
> *Focusing on catastrophic risk reduction, air-gapped infrastructure resilience, agent steerability, and robust system integrity.*

Aergia Studio is a local-first, multi-agent AI mission control ecosystem designed to run complex orchestrations (financial intelligence, health operations & clinical RAG, creative swarm generation, local sensory processing) with a zero-trust, high-resilience security posture. This project serves as an empirical engineering showcase demonstrating how to safely deploy, monitor, and steer autonomous agent swarms while mitigating the containment risks associated with advanced AI execution.

---

## 🏛️ AI Security & Infrastructure Posture

The architecture of Aergia Studio directly aligns with the core pillars of the **Anthropic AI Security Track**, addressing both infrastructure security and alignment verification.

### 1. Zero-Trust Local-First Security & "Digital Soul" Air-Gapping
To mitigate risks from external access and credential leakage:
* **Project MagHub Go:** Aergia runs entirely off a portable 2TB NVMe SSD. Financial credentials, API keys, and sensitive database connections reside on this physical drive.
* **Hardware Fingerprint Encryption:** Unplugging the drive instantly air-gaps all cryptographic materials from the host system, leaving zero persistent secrets on the host computer.
* **Local Sandboxing:** LLM operations, memory indexes, and code execution environments are contained locally, preventing sensitive user profiles from being exfiltrated to the public cloud.

### 2. Multi-Agent Steerability & Policy-Enforcement Gating
Rather than allowing agents unconstrained action spaces, Aergia enforces behavioral control at the infrastructure layer:
* **The Policy Engine:** Enforces system-level constraints before a request reaches any LLM provider.
* **Task Boundary Isolation:** Separation of concerns between **Project Athena** (Strategy & Planning), **Project Prometheus** (Reasoning/Thinking), and **Project Hephaestus** (Local Forge/Execution). Agents cannot cross boundaries without explicit permission.
* **Structured Output Enforcers:** Prevents code execution pipelines from receiving raw, unvalidated strings, minimizing prompt injection and remote code execution (RCE) vulnerabilities.

### 3. Graceful Resilience & Hybrid Network Bridging
Running distributed agents across Windows, WSL, and Docker containers introduces frequent network drops and bridging failures.
* Aergia employs a resilient connection manager for its persistent tracking database (`hestia_tracking`), implementing **exponential backoff with random jitter** and **SQLite-backed local caching** to prevent data loss or state corruption during connection drops.

---

## 🚀 Quick Start & Launchers

Aergia Studio includes a unified, cross-platform launcher in `scripts/launch.py` with convenient root scripts:

### Windows:
```cmd
:: Launch interactive control center
launch.bat

:: Launch specific modules directly:
Launch_Suite.bat          :: Full Suite (API + Orchestrator GUI + Web Console)
Launch_Health_Ops.bat      :: Health Ops Server + Desktop Dashboard
Launch_Orchestrator.bat    :: Native Orchestrator GUI
```

### macOS / Linux:
```bash
./launch.sh               # Interactive menu
./launch.sh --suite       # Full suite
./launch.sh --health      # Health Ops
```

### Direct Python Launcher:
```bash
python scripts/launch.py --suite
python scripts/launch.py --health
python scripts/launch.py --midas
python scripts/launch.py --test
```

---

## 📂 Repository Structure

```text
Aergia_Studio/
├── apps/                         # Core running applications
│   ├── aergia_api.py             # Flask API server & brain
│   ├── aergia_orchestrator_gui.py# Native desktop orchestrator
│   ├── aergia_dashboard.py       # Pantheon status dashboard
│   ├── health_ops_server.py      # Health Ops API & clinical tracking server
│   └── health_ops_dashboard.py   # Health Ops Tkinter Desktop GUI
├── core/
│   ├── router/                   # Multi-provider hive mind (DeepSeek, Gemini, Ollama, FAL)
│   └── modules/                  # Peptide knowledge engine & PubMed RAG
├── projects/                     # Autonomous agent sub-projects
│   ├── Project Aura/             # Sensory & environment interface
│   ├── Project Chimera/          # Video/audio creative production swarm
│   ├── Project Hermes/           # Core identity, memory, soul, and user context
│   ├── Project Hestia/           # State persistence, DB failover, cache engine
│   ├── Project Hyperion/         # Real-time pipeline & vision intelligence
│   ├── Project Kairos/           # Scheduling & timeline orchestration
│   ├── Project Midas/            # Quantitative market analysis & broker integrations
│   ├── Project Morai/            # Simulation & game engine
│   └── Project Plutus/           # Treasury & automated trade execution
├── skills/                       # Modular agent capability packages (e.g. Health Agent)
├── scripts/
│   ├── launch.py                 # Cross-platform master orchestrator
│   ├── maintenance/              # Shortcut repairs, asset generators, sync tools
│   ├── mac_node/                 # Mac node connectivity & permissions
│   ├── mobile_install/           # Mobile PWA installation helpers
│   └── legacy_launchers/         # Archived original launcher scripts
├── tests/                        # Comprehensive unit and integration test suites
│   ├── router/                   # Provider, policy, and routing verification
│   ├── system/                   # Server, GUI, and import checks
│   └── assets/                   # Visual and media tests
├── docs/                         # Consolidated documentation
│   ├── architecture/             # OS blueprints, full context, Bible
│   ├── vision/                   # 2026 project vision & updates
│   ├── guides/                   # Mac setup, distributed cluster, workflow
│   └── archive/                  # Historical planning docs & walkthroughs
└── requirements/                 # Layered dependency specifications
```

---

## 🩺 Health Ops & Peptide Engine

Aergia Studio includes a local-first clinical health operations platform:
* **Server:** `health_ops_server.py` (Local Flask server running on port `5000`)
* **Dashboard:** `health_ops_dashboard.py` (Tkinter UI with reconstitution calculators, inventory planning, laboratory baselines, and workout tracking)
* **Knowledge Engine:** `modules/peptide_engine/` (PubMed integration, educational RAG, compound database)
* **Agent Skills:** `skills/health_agent/` (Automated paper alerts and health protocols)
* **Launch:** Simply double-click `Launch_Health_Ops.bat` or run `python scripts/launch.py --health`.

---

## 🔒 Security & Privacy Notice
* All private keys, sessions, and SQLite databases (`health_ops.db`, `*.tokens.json`, `*.db`) are strictly excluded from git tracking.
* Never commit `.env` or credentials files to remote repositories.

---
*Developed with a commitment to alignment, robust software engineering, and system-level security.*
