# Midas "Squeeze Scout" - Brainstorming & Trading Ideas

*Note: This document contains manual trading logic and epiphanies intended for future automation within Project Midas and Project Aergia.*

## 📈 Active Trade Example: The "Squeeze Scout"
- **Symbol**: SOUN (SoundHound AI Inc)
- **Position**: 1 Contract | July 17, 2026 | $9.00 Call
- **Key Catalyst**: Earnings on May 7, 2026.
- **The Plan**: Monitor for a "Sell the Rumor" exit around May 5-6 to avoid the IV (Implied Volatility) crush. Wait for the stock to hold above `$8.30` as a confirmation signal before considering adding any more contracts.

## 🛠️ Triggers & Technicals for Midas Automation
Future Aergia agents (like the "Scout" agent) should look for the following conditions to flag potential trades:
1. **Short Float**: > 25-30% (The "Fuel")
2. **Days to Cover**: > 4-5 Days 
3. **Sizzle Index**: > 2.0 (High options volume compared to 5-day average - The "Spark")
4. **Vol Index**: Spiking (e.g., > 100%)
5. **Catalyst**: Upcoming earnings or news events within 14-21 days.

## 📊 The "Centurion" Roadmap (100-Trade Goal)
To prove that Midas has a replicable and statistically significant "Edge":
1. **Trades 1-10 (Manual/Augmented)**: Log metrics manually (Delta, Gamma, Sizzle, Short Interest) to refine the thesis.
2. **Trades 11-50 (Shadow Mode)**: Aergia identifies trades; user approves.
3. **Trades 51-100 (Autonomous)**: Aergia trades with small capital; uses Prometheus loop to auto-adjust on losses.

## 💻 Tech Stack & Security Plan (Laptop Build)
- **Central Nervous System**: Self-hosted `n8n` to trigger Schwab API.
- **The Brain**: Gemma 4 (via Google AI Edge/Ollama) running locally for analysis.
- **Security Check**: Enforce `midas_privacy.yaml` rules through NemoClaw to keep API keys encrypted and off plain text.
