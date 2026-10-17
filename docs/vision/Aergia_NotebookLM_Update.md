# Project Aergia - System Context & State Update
**Compiled on:** June 16, 2026

This document contains the latest architectural changes, configurations, and state updates for the Aergia Intelligence Ecosystem, designed to keep your NotebookLM sources completely up to date.

---

## 🚀 Recent Architecture Update: OpenClaw CLI & Edge Integration
We have hardened the local developer workspace and unified our edge models stack.

### 1. OpenClaw CLI & Gateway Scaffolding
* **Core Version:** OpenClaw CLI `2026.5.12 (f066dd2)` configured natively on host `dansasusvivo`.
* **Background Persistence:** Registered as a native Windows startup script at:
  `C:\Users\z143d\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\OpenClaw Gateway.cmd`
* **Local Hardening & Privacy:** Strictly set to `gateway.mode local`. Operator control interface is hard-locked to the loopback interface array via escaped string validation: `"[\"loopback:127.0.0.1\"]"`.
* **Ecosystem Handshake:** Authorized the laptop as the primary operator station under the identifier `"Daniel Workstation"`. Background task scripts generated at `~\.openclaw\node.cmd`.

### 2. Local Ollama (Edge AI) Integration
* **Ollama Provider:** Target model `gemma2:2b` runs offline on `http://localhost:11434` for rapid command parsing and zero-token speed routing.

---

## 🏛️ Central State & Project Status

### Hermes Mission Control (Travel, Network & Comms)
* **Location:** `Project Hermes/`
* **Current Net Placement:** Operating remotely on subnet address `192.168.0.52`.
* **Tailscale Mesh State:** Network tunnel is online and active at IP `100.111.220.42`.
* **Sync Delay:** The home-based tower (`shitboxver2`) is offline to the Tailscale mesh (last seen 120d ago). Local routing (`192.168.1.212`) for RTSP camera stream pipelines is temporarily held.

### Project Midas (Options Trading Engine)
* **Status:** Parallel trading system active. Goal is to grow capital via Short Interest triggers to sponsor CR-1/K-1 milestones.
* **Integrations:** Charles Schwab API and Coinbase CDP client keys mapped.

### Project Ares (Cybersecurity & Incident Response)
* **Status:** Protocol SIFT MCP server in standby. Talos Sentry logging active.

### Project Hestia (Smart Home, Health & DB Sync)
* **Location:** `Project Hestia/`
* **Relational DB Recovery:** Audited legacy container purge and recovered PostgreSQL 15-alpine physical binary data at `C:\Users\z143d\Aergia_Studio\Project Hestia\data`.
* **Isolated Composition:** Created an independent, loopback-isolated (`127.0.0.1`) Docker Compose setup to bind directly to the recovered `data` paths on port `5432` (db) and `5050` (pgAdmin) to protect historical health schemas.

---

## 🔄 How to Keep NotebookLM Sync Current
Upload this single document directly into your **Project Aergia Mission Control** notebook sources in NotebookLM. It overrides or supplements old file records to ensure the AI stays fully aligned with the active state of your local code.
