# 🧹 Aergia Studio: Codebase Cleanup & Consolidation Checklist

> **Purpose:** Transform `Aergia_Studio` from a sprawling multi-agent prototyping workspace into a structured, production-grade, and secure monorepo.
> **Status:** ✅ Completed (October 2026)

---

## 🎯 Executive Summary
The `Aergia_Studio` root directory has been fully overhauled:
* **Root Files Reduced:** From over 100 loose files down to clean, essential components and launchers.
* **Launchers Unified:** Replaced 15+ redundant scripts with `scripts/launch.py`, `launch.bat`, `launch.sh`, and clean root shortcuts (`Launch_Suite.bat`, `Launch_Health_Ops.bat`, `Launch_Orchestrator.bat`).
* **Security Hardened:** Plaintext credentials (`openrouterapi.txt`, `schwab_tokens.json`, `chimera-credentials.json`) quarantined; git tracking purged of secret files and `.gitignore` updated.
* **Tests & Diagnostics Relocated:** 30+ loose scripts categorized into `tests/router/`, `tests/system/`, `tests/assets/`, `scripts/maintenance/`, and `logs/archive/`.
* **Documentation Harmonized:** 17 loose markdown files consolidated into structured `docs/` subdirectories (`architecture/`, `vision/`, `guides/`, `archive/`).
* **Dependencies Layered:** Requirements split into modular packages in `requirements/` (`base.txt`, `ai.txt`, `finance.txt`, `health.txt`).

---

## 🚦 Phase 1: Security & Credential Isolation (Critical Priority)

- [x] **1.1 Quarantine Plaintext Secrets from Root**
  - [x] Verified `openrouterapi.txt` key exists securely in `.env`.
  - [x] Removed tracked `openrouterapi.txt` from git index (`git rm --cached openrouterapi.txt`) and deleted plain file from root.
  - [x] Relocated root `chimera-credentials.json` to `config/credentials/` and added `config/credentials/` to `.gitignore`.
  - [x] Removed duplicate root `schwab_tokens.json` and `paper_account.json` (canonical files exist in `Project Midas/`).
  - [x] Added `*credentials*.json`, `*tokens*.json`, `paper_account.json`, and `openrouterapi.txt` to `.gitignore`.

- [x] **1.2 Verify Git Privacy & History**
  - [x] Confirmed `.env`, `*.db`, `*.json` token files, and `*.key` remain strictly excluded in `.gitignore`.
  - [x] Verified git status shows no secrets in index or working tree.

---

## 📁 Phase 2: Directory Architecture & Monorepo Restructuring

- [x] **2.1 Isolate Health Ops & Knowledge Engines**
  - [x] Configured unified launchers to run Health Ops Server (`health_ops_server.py`) and Desktop Dashboard (`health_ops_dashboard.py`).
  - [x] Preserved peptide knowledge engine (`modules/peptide_engine/`) and agent skills (`skills/health_agent/`).
  - [x] Protected runtime database (`health_ops.db`) from git via `.gitignore`.

- [x] **2.2 Sub-Projects Preserved & Mapped**
  - [x] Preserved and mapped sub-agents: Project Aura, Chimera, Hermes, Hestia, Hyperion, Kairos, Midas, Morai, and Plutus.

- [x] **2.3 Archive Legacy & Transient Directories**
  - [x] Safely deleted obsolete `_backup_before_merge` directory.
  - [x] Moved `_MOBILE_INSTALL_HELPER`, `clone_to_mobile.py`, and `prepare_for_transfer.bat` to `scripts/mobile_install/`.

---

## 🚀 Phase 3: Launchers & Automation Unification

- [x] **3.1 Consolidate to Single Cross-Platform Launch Orchestrator**
  - [x] Created `scripts/launch.py` with interactive ASCII menu and CLI flags:
    - `--suite` / `-s` (Full Aergia Suite: API Server + Desktop GUI + Web Command Center)
    - `--health` / `-H` (Health Ops Server + Tkinter Desktop Dashboard)
    - `--health-server` (Health Ops API only)
    - `--health-gui` (Health Ops GUI only)
    - `--orchestrator` / `-o` (Desktop Orchestrator GUI)
    - `--api` / `-a` (Aergia API Server)
    - `--midas` / `-m` (Project Midas Trading System)
    - `--chimera` / `-c` (Project Chimera Creative Swarm)
    - `--test` / `-t` (Automated Test Suite)
  - [x] Created root entrypoint wrappers:
    - `launch.bat` (Windows)
    - `launch.sh` (macOS / Linux)
    - `Launch_Suite.bat` (Shortcut for Full Suite)
    - `Launch_Health_Ops.bat` (Shortcut for Health Ops)
    - `Launch_Orchestrator.bat` (Shortcut for Orchestrator)
  - [x] Archived 15 redundant legacy launchers to `scripts/legacy_launchers/`.

- [x] **3.2 Organize Mac Remote Scripts**
  - [x] Moved `Connect_Mac_Node.command`, `Fix_Mac_Permissions.command`, `Launch_Exo_Cluster.command`, and `setup_mac.sh` into `scripts/mac_node/`.

---

## 🧪 Phase 4: Test & Diagnostic File Relocation

- [x] **4.1 Move Provider & Router Tests to `tests/router/`**
  - [x] Relocated `test_coinbase.py`, `test_fal_direct.py`, `test_final_router.py`, `test_finance_router.py`, `test_ollama.py`, `test_reasoning.py`, `verify_fal_full.py`, `verify_google_key.py`, `verify_openrouter.py`, `probe_longcat.py`, `demo_finance_agent.py`, `demo_swarm.py`, `debug_router.py`.

- [x] **4.2 Move System & GUI Tests to `tests/system/`**
  - [x] Relocated `check_model_simple.py`, `check_server.py`, `sanity_check.py`, `test_gui_launch.py`, `test_import.py`, `test_orchestrator.py`, `test_verify_E.py`, `test_chimera_job.py`, `debug_dashboard.py`.

- [x] **4.3 Move Shortcut & Maintenance Scripts to `scripts/maintenance/`**
  - [x] Shortcuts: `Create_Desktop_Shortcut.py`, `create_shortcut.py`, `dump_shortcut.py`, `fix_shortcuts.py`, `inspect_shortcut.py`, `reset_shortcuts_powershell.py`, `restore_simple_shortcut.py`, `restore_wallpapers.py` moved to `scripts/maintenance/shortcuts/`.
  - [x] Asset Tools: `audit_assets.py`, `migrate_assets.py`, `build_canon_selector.py`, `generate_canon_gallery.py`, `generate_gallery.py`, `generate_icon.py`, `recreate_personal_scenes.py`, `regenerate_canon.py`, `setup_cinema_assets.py`, `canon_selector.html`, `visual_canon_gallery.html`, `visual_sorter.html` moved to `scripts/maintenance/assets/`.
  - [x] General: `dump_code.py`, `list_models.py`, `scan_paths.py`, `inspect_db_schema.py`, `setup_delta_sync.py` moved to `scripts/maintenance/`.

- [x] **4.4 Archive Transient Output & Log Dumps**
  - [x] Moved to `logs/archive/`: `debug_log.txt`, `debug_output_full.txt`, `diag_output.txt`, `diag_paths_output.txt`, `diag_utf8.txt`, `clear_ro.txt`, `paths.txt`, `models.txt`, `assets.txt`, `recreation_debug.txt`, `router_test_output.txt`, `shortcut_debug_info.txt`, `shortcut_info.json`, `aergia_paths_diag.bat`.
  - [x] Moved test images to `tests/assets/`: `test_capture_1766456234.png`, `test_icon_crop.png`, `test_pollinations.jpg`, `test_image.py`.

---

## 📚 Phase 5: Documentation Harmonization

- [x] **5.1 Consolidate Architecture & Vision into `docs/`**
  - [x] `docs/architecture/`: `Aergia_OS_Blueprint.md`, `Aergia_Full_Codebase.md`, `Project_Aergia_Full_Context.md`, `AERGIA_BIBLE.md`.
  - [x] `docs/vision/`: `Aergia_Project_Vision_2026.md`, `Aergia_NotebookLM_Update.md`.
  - [x] `docs/guides/`: `AERGIA_MAC_FIXES.md`, `DISTRIBUTED_GUIDE.md`, `REMOTE_ACCESS.md`, `GITHUB_WORKFLOW.md`, `DASHBOARD_README.md`.
  - [x] `docs/archive/`: `NEXT_STEPS.md`, `README_NEXT_STEPS.txt`, `ANTIGRAVITY_LAUNCH.md`, `walkthrough.md`, `implementation_plan.md`.

- [x] **5.2 Curate Root Documentation**
  - [x] Re-authored `README.md` with clean UTF-8 formatting, clear quick start instructions, directory map, and Health Ops guide.
  - [x] Retained `aergia-cleanup-checklist.md` as the definitive consolidation audit record.

---

## 📦 Phase 6: Dependency & Environment Harmonization

- [x] **6.1 Unify Python Dependencies**
  - [x] Layered requirements created in `requirements/`:
    - `requirements/base.txt` (core GUI, API, HTTP, environment)
    - `requirements/ai.txt` (Google GenAI, Vertex, automation)
    - `requirements/finance.txt` (yfinance, finvizfinance)
    - `requirements/health.txt` (Flask, health ops libraries)
  - [x] Root `requirements.txt` unified to link modular sub-requirements.

- [x] **6.2 Node.js Clean Status**
  - [x] Verified `node_modules` remains completely ignored and uncommitted in git.

---

## ✅ Final Status Summary

| Stage | Focus Area | Status |
| :--- | :--- | :--- |
| **Phase 1** | Plaintext Secrets & Tokens Quarantine | ✅ Complete |
| **Phase 2** | Directory Restructuring & App Isolation | ✅ Complete |
| **Phase 3** | Launcher Consolidation (`scripts/launch.py`) | ✅ Complete |
| **Phase 4** | Test & Maintenance Scripts Relocation | ✅ Complete |
| **Phase 5** | Documentation Consolidation into `docs/` | ✅ Complete |
| **Phase 6** | Dependencies & Multi-Platform Harmonization | ✅ Complete |
