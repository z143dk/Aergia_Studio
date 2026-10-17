---
name: health_agent
description: Connects to the Aergia Health Ops local server to manage checklists, workouts, recovery logging, and search peptide research.
version: 1.0.0
---

# Health Agent Skill

This skill allows the OpenClaw agent to query and update the local Hestia Health Database via the Flask API and fetch scientific research on peptides.

## Instructions

1. **Check Status / Checklist**:
   - If the user asks about their daily checklist, weight, pain score, or overall health schedule, run:
     ```bash
     python scripts/manage_health.py status
     ```

2. **Toggle Daily Checklist Item**:
   - If the user asks to check off, mark complete, or toggle a specific item (e.g. "collagen peptides", "take vitamins"), run:
     ```bash
     python scripts/manage_health.py toggle "<item_text>" <true|false>
     ```

3. **Log a Workout**:
   - If the user logs a workout (e.g. "I ran for 30 minutes at 145 average HR"), run:
     ```bash
     python scripts/manage_health.py log-workout "<workout_type>" <duration_mins> <avg_hr> "[details]"
     ```

4. **Log Recovery & Biometrics**:
   - If the user wants to log daily recovery metrics (soreness, pain, sleep quality, weight), run:
     ```bash
     python scripts/manage_health.py log-recovery <joint_pain_1_10> <soreness_1_10> <sleep_quality_1_10> <weight_lbs> "[notes]"
     ```

5. **Search Peptide News & Publications**:
   - If the user asks for the latest news, scientific research, or publications on a peptide (e.g. "BPC-157", "TB-500", "Collagen"), run:
     ```bash
     python scripts/fetch_peptide_news.py "<peptide_name>"
     ```
