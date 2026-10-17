import os
import sqlite3
import json
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)
DB_PATH = "health_ops.db"

# HTML/JS Template with premium styling, glassmorphism, and all Hestia features fully integrated
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aergia Health & Peptide Command Center</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.55);
            --border-color: rgba(255, 255, 255, 0.08);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-blue: #3b82f6;
            --accent-green: #10b981;
            --accent-purple: #8b5cf6;
            --accent-red: #ef4444;
            --accent-warning: #f59e0b;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Outfit', sans-serif;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-primary);
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
            padding-bottom: 80px;
        }

        header {
            margin-bottom: 25px;
            text-align: center;
        }

        h1 {
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(to right, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }

        .subtitle {
            font-size: 0.9rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 600;
        }

        /* Tabs Navigation */
        .tabs {
            display: flex;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 6px;
            margin-bottom: 25px;
            backdrop-filter: blur(12px);
            gap: 5px;
            overflow-x: auto;
        }

        .tab-btn {
            flex: 1;
            min-width: 120px;
            background: transparent;
            border: none;
            color: var(--text-secondary);
            padding: 12px 10px;
            font-size: 0.95rem;
            font-weight: 600;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.25s ease;
            white-space: nowrap;
        }

        .tab-btn.active {
            background: var(--accent-blue);
            color: var(--text-primary);
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        }

        /* Layout Grid */
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        .grid-3-1 {
            display: grid;
            grid-template-columns: 2.5fr 1fr;
            gap: 20px;
        }

        @media (max-width: 900px) {
            .grid-2, .grid-3-1 {
                grid-template-columns: 1fr;
            }
        }

        /* Cards */
        .card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 20px;
            backdrop-filter: blur(16px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }

        .card-title {
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 18px;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Forms */
        .form-group {
            margin-bottom: 16px;
        }

        .form-row {
            display: flex;
            gap: 15px;
            margin-bottom: 16px;
        }

        .form-row .form-group {
            flex: 1;
            margin-bottom: 0;
        }

        label {
            display: block;
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-bottom: 6px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        input, select, textarea {
            width: 100%;
            padding: 12px;
            background: #1e293b;
            border: 1px solid var(--border-color);
            border-radius: 10px;
            color: var(--text-primary);
            font-size: 0.95rem;
            outline: none;
            transition: border-color 0.2s;
        }

        input:focus, select:focus, textarea:focus {
            border-color: var(--accent-blue);
        }

        .btn-submit {
            background: var(--accent-blue);
            color: var(--text-primary);
            border: none;
            padding: 14px 20px;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            width: 100%;
            transition: all 0.2s;
            text-align: center;
        }

        .btn-submit:hover {
            opacity: 0.9;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            padding: 10px 15px;
            border-radius: 10px;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
            text-align: center;
        }

        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.1);
        }

        /* Table styles */
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }

        th {
            text-align: left;
            padding: 12px;
            background: rgba(0, 0, 0, 0.2);
            color: var(--text-secondary);
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 2px solid var(--border-color);
        }

        td {
            padding: 12px;
            border-bottom: 1px solid var(--border-color);
            font-size: 0.95rem;
            color: var(--text-primary);
        }

        tr:hover {
            background: rgba(255, 255, 255, 0.02);
        }

        /* Checklist */
        .checklist-group {
            margin-bottom: 20px;
        }

        .checklist-group h3 {
            font-size: 0.95rem;
            color: var(--accent-blue);
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 700;
        }

        .check-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 12px;
            margin-bottom: 8px;
            cursor: pointer;
        }

        .check-item input[type="checkbox"] {
            width: 20px;
            height: 20px;
            accent-color: var(--accent-blue);
            cursor: pointer;
        }

        /* Conflict Grid */
        .conflict-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 12px;
            margin-bottom: 20px;
        }

        .conflict-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 15px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .conflict-card input[type="checkbox"] {
            width: 18px;
            height: 18px;
        }

        .conflict-alert {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid var(--accent-red);
            color: #fca5a5;
            padding: 15px;
            border-radius: 12px;
            margin-top: 15px;
            line-height: 1.5;
        }

        /* RAG / AI Styles */
        .ai-output-box {
            background: rgba(15, 23, 42, 0.4);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            min-height: 150px;
            margin-top: 15px;
            font-size: 0.95rem;
            line-height: 1.6;
            color: #cbd5e1;
        }

        .spinner {
            display: none;
            text-align: center;
            padding: 20px;
        }

        .spinner-circle {
            width: 30px;
            height: 30px;
            border: 3px solid rgba(255,255,255,0.1);
            border-radius: 50%;
            border-top-color: var(--accent-blue);
            animation: spin 1s ease-in-out infinite;
            display: inline-block;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .paper-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255,255,255,0.05);
            padding: 15px;
            border-radius: 12px;
            margin-top: 10px;
        }

        .paper-title {
            font-weight: 600;
            color: var(--accent-green);
        }

        /* Search inputs */
        .search-container {
            margin-bottom: 15px;
        }

        .search-input {
            padding: 10px 15px;
        }

        /* History panel */
        .history-panel {
            background: #111827;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 15px;
            max-height: 250px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 0.85rem;
            color: #e2e8f0;
            line-height: 1.5;
        }
    </style>
</head>
<body>

    <header>
        <div class="subtitle">PROJECT AERGIA // INTERACTIVE SATELLITE</div>
        <h1>Health & Bioregulation Command Center</h1>
    </header>

    <div class="tabs">
        <button class="tab-btn active" onclick="switchTab('dashboard')">🏠 Dashboard</button>
        <button class="tab-btn" onclick="switchTab('log')">✍️ Log Stats</button>
        <button class="tab-btn" onclick="switchTab('reconstitute')">🧪 Reconstitution</button>
        <button class="tab-btn" onclick="switchTab('orders')">🛒 Order Planner</button>
        <button class="tab-btn" onclick="switchTab('analyzer')">🛡️ Conflict Scan</button>
        <button class="tab-btn" onclick="switchTab('baselines')">🩸 Baselines & Labs</button>
        <button class="tab-btn" onclick="switchTab('ai')">🧠 AI Edu RAG</button>
        <button class="tab-btn" onclick="switchTab('poster')">🖼️ V7 Protocol Chart</button>
    </div>

    <!-- TAB: DASHBOARD -->
    <div id="tab-dashboard" class="tab-content">
        <div class="grid-3-1">
            <div>
                <div class="card">
                    <div class="card-title">📋 Today's Supplement & Peptide Routine</div>
                    <div id="checklist-container">
                        <p style="color: var(--text-secondary);">Loading routine schedule...</p>
                    </div>
                </div>
            </div>
            <div>
                <div class="card">
                    <div class="card-title">🔬 Protocol Config</div>
                    <div id="protocol-status-banner" style="font-weight: 700; color: var(--accent-green); margin-bottom: 15px; font-size: 0.95rem;">
                        Loading...
                    </div>
                    <div class="form-group">
                        <label>Day 1 Start Date</label>
                        <input type="date" id="settings-start-date" onchange="saveProtocolSettings()">
                    </div>
                    <div style="border-top: 1px solid var(--border-color); padding-top: 15px; margin-top: 15px;">
                        <div style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 8px; font-weight: 600;">ACTIVE CYCLES</div>
                        <label class="check-item" style="cursor: pointer; text-transform: none; font-weight: 400; font-size: 0.95rem;">
                            <input type="checkbox" id="settings-epithalon" onchange="saveProtocolSettings()">
                            <span style="margin-left: 10px;">Epithalon (10-Day circadian reset)</span>
                        </label>
                        <label class="check-item" style="cursor: pointer; text-transform: none; font-weight: 400; font-size: 0.95rem;">
                            <input type="checkbox" id="settings-ta1" onchange="saveProtocolSettings()">
                            <span style="margin-left: 10px;">Thymosin Alpha-1 (Immune management)</span>
                        </label>
                    </div>
                    <div style="border-top: 1px solid var(--border-color); padding-top: 15px; margin-top: 15px;">
                        <div style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 5px; font-weight: 600;">MOTS-C FLOATER TRACKER</div>
                        <div id="settings-mots-last-date" style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 10px;">Last Injection: --</div>
                        <button class="btn-secondary" style="width: 100%;" onclick="logMotsCInjection()">Log MOTS-c Injection Today</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB: LOG STATS -->
    <div id="tab-log" class="tab-content" style="display: none;">
        <div class="grid-2">
            <div class="card">
                <div class="card-title">💪 Log Daily Workout</div>
                <form id="workout-form" onsubmit="logWorkout(event)">
                    <div class="form-group">
                        <label for="w_type">Workout Type</label>
                        <input type="text" id="w_type" placeholder="e.g. Upper Body Strength, YMCA Swim" required>
                    </div>
                    <div class="form-group">
                        <label for="w_duration">Duration (minutes)</label>
                        <input type="number" id="w_duration" required>
                    </div>
                    <div class="form-group">
                        <label for="w_hr">Average Heart Rate (BPM)</label>
                        <input type="number" id="w_hr" required>
                    </div>
                    <div class="form-group">
                        <label for="w_details">Details / Notes</label>
                        <textarea id="w_details" placeholder="Specific exercises, sets, or reps..."></textarea>
                    </div>
                    <button type="submit" class="btn-submit">Save Workout</button>
                </form>
            </div>
            
            <div class="card">
                <div class="card-title">🛌 Log Recovery & Weight</div>
                <form id="recovery-form" onsubmit="logRecovery(event)">
                    <div class="form-group">
                        <label for="r_pain">Joint Pain Score (1-10)</label>
                        <select id="r_pain">
                            <option value="1">1 - Minimal / None</option>
                            <option value="2" selected>2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5 - Moderate</option>
                            <option value="6">6</option>
                            <option value="7">7</option>
                            <option value="8">8 - High</option>
                            <option value="9">9</option>
                            <option value="10">10 - Severe</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="r_soreness">Muscle Soreness Score (1-10)</label>
                        <select id="r_soreness">
                            <option value="1">1</option>
                            <option value="2" selected>2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                            <option value="6">6</option>
                            <option value="7">7</option>
                            <option value="8">8</option>
                            <option value="9">9</option>
                            <option value="10">10</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="r_sleep">Sleep Quality (1-10)</label>
                        <select id="r_sleep">
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                            <option value="6">6</option>
                            <option value="7">7</option>
                            <option value="8" selected>8</option>
                            <option value="9">9</option>
                            <option value="10">10</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="r_weight">Current Weight (lbs)</label>
                        <input type="number" step="0.1" id="r_weight" required>
                    </div>
                    <div class="form-group">
                        <label for="r_notes">Daily Health Notes</label>
                        <textarea id="r_notes" placeholder="Notes on energy, stress, or symptoms..."></textarea>
                    </div>
                    <button type="submit" class="btn-submit">Save Stats</button>
                </form>
            </div>
        </div>
    </div>

    <!-- TAB: RECONSTITUTION -->
    <div id="tab-reconstitute" class="tab-content" style="display: none;">
        <div class="card">
            <div class="card-title">🧪 Reconstitution Master Guidelines</div>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Lid Color</th>
                            <th>Compound</th>
                            <th>Vial Size</th>
                            <th>BAC Water</th>
                            <th>Target Dose</th>
                            <th>Syringe Draw</th>
                            <th>Shelf-Life</th>
                        </tr>
                    </thead>
                    <tbody id="reconstitute-table-body">
                        <!-- Dynamically generated -->
                    </tbody>
                </table>
            </div>
        </div>

        <div class="grid-2">
            <div class="card">
                <div class="card-title">🧮 Syringe Draw Calculator</div>
                <div class="form-group">
                    <label>Vial Size (mg)</label>
                    <input type="number" id="calc-vial-size" placeholder="e.g., 10" oninput="runCalculator()">
                </div>
                <div class="form-group">
                    <label>BAC Water Added (mL)</label>
                    <input type="number" id="calc-bac-water" placeholder="e.g., 2.0" oninput="runCalculator()">
                </div>
                <div class="form-group">
                    <label>Target Dose (mcg)</label>
                    <input type="number" id="calc-target-dose" placeholder="e.g., 250" oninput="runCalculator()">
                </div>
                <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); border-radius: 12px; padding: 15px; margin-top: 15px; text-align: center;">
                    <div style="font-size: 0.8rem; color: var(--text-secondary); text-transform: uppercase;">Required Syringe Draw</div>
                    <div id="calc-result" style="font-size: 1.8rem; font-weight: 700; color: var(--accent-blue);">-- Units</div>
                </div>
            </div>

            <div class="card">
                <div class="card-title">🚨 Sharing & Blending Safety</div>
                <div class="grid-2" style="gap: 15px;">
                    <div>
                        <div style="font-weight: 700; color: var(--accent-green); font-size: 0.95rem; margin-bottom: 8px;">✅ SAFE TO BLEND</div>
                        <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">
                            • <strong>Night Growth Stack:</strong> Tesamorelin + Ipamorelin (Pituitary Synergism)<br><br>
                            • <strong>Morning Brain Stack:</strong> Semax + Selank + Pinealon (Neuro-Compatible)<br><br>
                            • <strong>Fat-Burning Shot:</strong> Lipo-C + B12 (Deep SubQ/IM - Requires 3mL syringe)
                        </div>
                    </div>
                    <div>
                        <div style="font-weight: 700; color: var(--accent-red); font-size: 0.95rem; margin-bottom: 8px;">🚫 NEVER BLEND</div>
                        <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">
                            • <strong>NAD+:</strong> Highly acidic (pH ~2.5) -> degrades peptides instantly.<br><br>
                            • <strong>Glutathione:</strong> High sulfur blocks amino chains.<br><br>
                            • <strong>MOTS-c:</strong> High stinging/localized reaction risk.<br><br>
                            • <strong>Mounjaro:</strong> Pre-filled single use auto-pen.
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB: ORDERS -->
    <div id="tab-orders" class="tab-content" style="display: none;">
        <div class="grid-3-1">
            <div class="card">
                <div class="card-title">🛒 Vendor Kit Reference Pricing</div>
                <div class="search-container">
                    <input type="text" id="order-search" class="search-input" placeholder="Search compounds..." oninput="filterVendorTable()">
                </div>
                <div style="overflow-y: auto; max-height: 380px;">
                    <table>
                        <thead>
                            <tr>
                                <th>Compound</th>
                                <th>Code</th>
                                <th>Specification</th>
                                <th>Price</th>
                                <th>Lifespan</th>
                                <th>Trigger Month</th>
                            </tr>
                        </thead>
                        <tbody id="vendor-pricing-table">
                            <!-- Filled dynamically -->
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div class="card">
                <div class="card-title">✍️ Log Inventory Order</div>
                <form id="order-form" onsubmit="logNewOrder(event)">
                    <div class="form-group">
                        <label>Compound Name</label>
                        <input type="text" id="o_name" placeholder="e.g. Tesamorelin" required>
                    </div>
                    <div class="form-group">
                        <label>Vials In Kit</label>
                        <input type="number" id="o_vials" placeholder="e.g. 10" required>
                    </div>
                    <div class="form-group">
                        <label>Vial Size (mg)</label>
                        <input type="number" step="0.1" id="o_size" placeholder="e.g. 10.0" required>
                    </div>
                    <div class="form-group">
                        <label>Dosage (Units/Infection)</label>
                        <input type="number" id="o_dose" placeholder="e.g. 25" required>
                    </div>
                    <div class="form-group">
                        <label>Doses Per Week</label>
                        <input type="number" id="o_freq" placeholder="e.g. 5" required>
                    </div>
                    <button type="submit" class="btn-submit">Log Order & Forecast</button>
                </form>
            </div>
        </div>

        <div class="card" style="margin-top: 20px;">
            <div class="card-title">📦 Logged Inventory & Depletion Planner</div>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Compound/Supplement</th>
                            <th>Order Date</th>
                            <th>Vials Qty</th>
                            <th>Dose (U)</th>
                            <th>Freq/Wk</th>
                            <th>Est. Depletion Date</th>
                        </tr>
                    </thead>
                    <tbody id="orders-log-table">
                        <!-- Loaded dynamically -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- TAB: CONFLICT SCAN -->
    <div id="tab-analyzer" class="tab-content" style="display: none;">
        <div class="card">
            <div class="card-title">🛡️ Clinical Redundancy & Safety Scanner</div>
            <p style="color: var(--text-secondary); margin-bottom: 20px;">
                Select the compounds you are currently administering to scan for receptor overlap, competitive pathways, or organ stress indicators.
            </p>
            <div class="conflict-grid" id="analyzer-checkboxes">
                <!-- Dynamically loaded checkboxes -->
            </div>
            <button class="btn-submit" onclick="runConflictAnalysis()">Run Safety Check</button>
            
            <div id="analyzer-result" style="display: none;"></div>
        </div>
    </div>

    <!-- TAB: BASELINES & LABS -->
    <div id="tab-baselines" class="tab-content" style="display: none;">
        <div class="grid-3-1">
            <div class="card">
                <div class="card-title">🩸 Biomarker Lab Baselines</div>
                <div style="overflow-y: auto; max-height: 400px;">
                    <table>
                        <thead>
                            <tr>
                                <th>Marker</th>
                                <th>Baseline</th>
                                <th>Current</th>
                                <th>Unit</th>
                                <th>Variance</th>
                                <th>Notes</th>
                            </tr>
                        </thead>
                        <tbody id="baselines-table-body">
                            <!-- Loaded dynamically -->
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="card">
                <div class="card-title">📈 Record Lab Reading</div>
                <div id="selected-marker-lbl" style="font-weight: 700; color: var(--accent-green); margin-bottom: 12px; font-size: 0.95rem;">
                    Select a marker from the left table
                </div>
                <form id="lab-reading-form" onsubmit="logLabReading(event)">
                    <div class="form-group">
                        <label>Value</label>
                        <input type="number" step="0.01" id="l_value" required>
                    </div>
                    <div class="form-group">
                        <label>Date</label>
                        <input type="date" id="l_date" required>
                    </div>
                    <div class="form-group">
                        <label>Notes / Context</label>
                        <input type="text" id="l_notes" placeholder="e.g. Fasting, Labcorp panel">
                    </div>
                    <button type="submit" class="btn-submit" style="margin-bottom: 10px;">Save Reading</button>
                </form>

                <div style="border-top: 1px solid var(--border-color); padding-top: 15px; margin-top: 15px;">
                    <div style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 8px; font-weight: 600;">ADJUST BASELINE REFERENCE</div>
                    <div class="form-group">
                        <input type="number" step="0.01" id="l_new_baseline" placeholder="New Baseline Target">
                    </div>
                    <button class="btn-secondary" style="width: 100%;" onclick="updateBaselineReference()">Update Reference</button>
                </div>
            </div>
        </div>

        <div class="card" style="margin-top: 20px;">
            <div class="card-title">📊 Selected Biomarker Historical Records</div>
            <div class="history-panel" id="biometrics-history-container">
                Select a marker above to load historical logs.
            </div>
        </div>
    </div>

    
    <!-- TAB: V7 PROTOCOL POSTER -->
    <div id="tab-poster" class="tab-content" style="display: none;">
        <div class="card" style="text-align: center;">
            <div class="card-title">🖼️ Clinical Reference Protocol: Phase 2 V7 (September Update)</div>
            <p style="color: var(--text-secondary); margin-bottom: 15px;">High-resolution master protocol visual reference chart.</p>
            <div style="overflow-x: auto; max-width: 100%;">
                <img src="/static/assets/banners/Hestia_Banner.png" alt="Hestia Master Protocol V7" style="width: 100%; border-radius: 12px; border: 1px solid var(--border-color); box-shadow: 0 8px 25px rgba(0,0,0,0.5);">
            </div>
        </div>
    </div>

    <!-- TAB: AI RAG -->
    <div id="tab-ai" class="tab-content" style="display: none;">
        <div class="card">
            <div class="card-title">🧠 AI Educational Query Assistant</div>
            <p style="color: var(--text-secondary); margin-bottom: 20px;">
                Ask scientific questions about target receptors, cell pathways, and physiological mechanisms for your compounds. 
                Queries retrieve peer-reviewed NCBI PubMed evidence in real-time.
            </p>
            <div class="form-group">
                <input type="text" id="ai-query-input" placeholder="e.g., Explain the GHRH receptor signaling pathway of Tesamorelin" onkeypress="handleQueryKey(event)">
            </div>
            <button class="btn-submit" onclick="submitQuery()">Request RAG Report</button>
            
            <div class="spinner" id="query-spinner">
                <div class="spinner-circle"></div>
                <div style="margin-top: 10px; color: var(--text-secondary);">Querying PubMed & generating report via local model...</div>
            </div>
            
            <div id="ai-result-box" class="ai-output-box" style="display: none;"></div>
            <div id="ai-references-box" style="margin-top: 20px;"></div>
        </div>
    </div>

    <script>
        let currentTab = 'dashboard';
        let selectedMarkerName = '';

        // Reconstitution Guidelines Data
        const reconstitutionData = [
            ["🟣 RED WINE", "NAD+", "500mg", "2.0 mL", "12.5-25 Units (31-62.5mg)", "12.5-25 Units", "~2.5 Weeks"],
            ["🟡 YELLOW", "5-Amino-1MQ", "50mg", "2.5 mL", "20 Units (4mg)", "20 Units", "~30 Days"],
            ["🟡 YELLOW", "SS-31", "10mg", "2.0 mL", "20 Units (1mg)", "20 Units", "~30 Days"],
            ["🩵 TEAL", "Semax", "10mg", "2.0 mL", "5-10 Units (250-500mcg)", "5-10 Units", "~30 Days"],
            ["🩵 TEAL", "Selank", "10mg", "2.0 mL", "5-10 Units (250-500mcg)", "5-10 Units", "~30 Days"],
            ["💜 PURPLE", "Pinealon", "10mg", "2.0 mL", "20 Units (1mg)", "20 Units", "~30 Days"],
            ["🟢 LT GREEN", "Glutathione", "600mg", "3.0 mL", "50 Units (100mg)", "50 Units", "~30 Days"],
            ["🔴 RED", "Tesamorelin", "10mg", "2.0 mL", "25 Units (1.25mg)", "25 Units", "~2.5 Weeks"],
            ["🔴 RED", "Ipamorelin", "10mg", "2.0 mL", "5-10 Units (250-500mcg)", "5-10 Units", "~30 Days"],
            ["🟠 ORANGE", "KLOW Blend", "80mg", "2.0 mL", "10 Units (0.1 mL)", "10 Units", "~30 Days"],
            ["🌌 NAVY", "DSIP", "10mg", "2.0 mL", "10 Units (500mcg)", "10 Units", "~30 Days"],
            ["🩷 PINK", "Kisspeptin-10", "10mg", "2.0 mL", "10 Units (500mcg)", "10 Units", "~30 Days"],
            ["🩵 VIOLET", "GHK-Cu (SubQ)", "50mg", "2.5-5.0 mL", "5-10 Units (1-2mg)", "5-10 Units", "~30 Days"],
            ["CLEAR", "GHK-Cu (Topical)", "50mg", "2.5-5.0 mL", "1% to 2% Solution", "Pat on skin", "* 30d"],
            ["🔵 BLUE", "MOTS-c", "10mg", "2.0 mL", "50 Units (2.5mg)", "50 Units", "~20 Days"],
            ["⚪ WHITE", "Lipo-C (10mL)", "10 mL Liquid", "Pre-Mixed", "100 Units (1.0 mL)", "100 Units", "Exp. Date on Vial"],
            ["♦️ RUBY", "Vitamin B12", "1mg/mL", "Pre-Mixed", "50 Units (0.5 mL)", "50 Units", "Exp. Date on Vial"],
            ["🖊️ AUTO-PEN", "Mounjaro", "2.5mg Pen", "Pre-Mixed", "1 Pen (2.5mg)", "Auto-Pen", "Single Use"]
        ];

        // Vendor Reference Data
        const vendorData = [
            ["Semaglutide", "SM5", "5mg*10vials", "$35.00", "As Needed", "As Needed"],
            ["Semaglutide", "SM10", "10mg*10vials", "$45.00", "As Needed", "As Needed"],
            ["Semaglutide", "SM15", "15mg*10vials", "$60.00", "As Needed", "As Needed"],
            ["Semaglutide", "SM20", "20mg*10vials", "$70.00", "As Needed", "As Needed"],
            ["Semaglutide", "SM30", "30mg*10vials", "$90.00", "As Needed", "As Needed"],
            ["Semaglutide", "SM40", "40mg*10vials", "$110.00", "As Needed", "As Needed"],
            ["Semaglutide", "SM50", "50mg*10vials", "$125.00", "As Needed", "As Needed"],
            ["Tirzepatide", "TR5", "5mg*10vials", "$35.00", "As Needed", "As Needed"],
            ["Tirzepatide", "TR10", "10mg*10vials", "$55.00", "As Needed", "As Needed"],
            ["Tirzepatide", "TR15", "15mg*10vials", "$70.00", "As Needed", "As Needed"],
            ["Tirzepatide", "TR20", "20mg*10vials", "$85.00", "As Needed", "As Needed"],
            ["Tirzepatide", "TR30", "30mg*10vials", "$100.00", "As Needed", "As Needed"],
            ["Tirzepatide", "TR40", "40mg*10vials", "$125.00", "As Needed", "As Needed"],
            ["Tirzepatide", "TR50", "50mg*10vials", "$170.00", "As Needed", "As Needed"],
            ["Tirzepatide", "TR60", "60mg*10vials", "$190.00", "As Needed", "As Needed"],
            ["Tirzepatide", "TR100", "100mg*10vials", "$250.00", "As Needed", "As Needed"],
            ["Tirzepatide", "TR120", "120mg*10vials", "$290.00", "As Needed", "As Needed"],
            ["Retatrutide", "RT5", "5mg*10vials", "$55.00", "As Needed", "As Needed"],
            ["Retatrutide", "RT10", "10mg*10vials", "$80.00", "As Needed", "As Needed"],
            ["Retatrutide", "RT15", "15mg*10vials", "$110.00", "As Needed", "As Needed"],
            ["Retatrutide", "RT20", "20mg*10vials", "$135.00", "As Needed", "As Needed"],
            ["Retatrutide", "RT30", "30mg*10vials", "$170.00", "As Needed", "As Needed"],
            ["Retatrutide", "RT40", "40mg*10vials", "$205.00", "As Needed", "As Needed"],
            ["Retatrutide", "RT50", "50mg*10vials", "$245.00", "As Needed", "As Needed"],
            ["Retatrutide", "RT60", "60mg*10vials", "$270.00", "As Needed", "As Needed"],
            ["Retatrutide", "RT100", "100mg*10vials", "$360.00", "As Needed", "As Needed"],
            ["Tesamorelin", "TSM2", "2mg*10vials", "$55.00", "As Needed", "As Needed"],
            ["Tesamorelin", "TSM5", "5mg*10vials", "$100.00", "As Needed", "As Needed"],
            ["Tesamorelin", "TSM10", "10mg * 10vials", "$180.00", "~26.6 Weeks (6.5 Mo)", "Month 5"],
            ["Tesamorelin", "TSM15", "15mg*10vials", "$250.00", "As Needed", "As Needed"],
            ["Tesamorelin", "TSM20", "20mg*10vials", "$325.00", "As Needed", "As Needed"],
            ["MOTS-c (Human)", "MS5", "5mg*10vials", "$55.00", "As Needed", "As Needed"],
            ["MOTS-c (Human)", "MS10", "10mg * 10vials", "$70.00", "~200 Days (6.5 Mo)", "Month 5"],
            ["MOTS-c (Human)", "MS20", "20mg*10vials", "$115.00", "As Needed", "As Needed"],
            ["MOTS-c (Human)", "MS40", "40mg*10vials", "$180.00", "As Needed", "As Needed"],
            ["GHK-Cu", "Cu50", "50mg*10vials", "$35.00", "As Needed", "As Needed"],
            ["GHK-Cu", "Cu100", "100mg*10vials", "$45.00", "As Needed", "As Needed"],
            ["AHK-CU", "AHK50", "50mg*10vials", "$45.00", "As Needed", "As Needed"],
            ["AHK-CU", "AHK100", "100mg*10vials", "$70.00", "As Needed", "As Needed"],
            ["SS-31", "2S10", "10mg * 10vials", "$90.00", "~33 Weeks (8 Mo)", "Month 6.5"],
            ["SS-31", "2S50", "50mg*10vials", "$290.00", "As Needed", "As Needed"],
            ["GLOW (BPC157+GHK-Cu+TB500)", "GLOW70", "70mg*10vials", "$190.00", "As Needed", "As Needed"],
            ["KLOW Blend", "KLOW80", "80mg * 10vials", "$215.00", "~66 Weeks (15 Mo)", "Month 13"],
            ["IGF-1LR3", "IG01", "0.1mg*10vials", "$45.00", "As Needed", "As Needed"],
            ["IGF-1LR3", "IG1", "1mg*10vials", "$180.00", "As Needed", "As Needed"],
            ["BPC 157", "BC5", "5mg*10vials", "$45.00", "As Needed", "As Needed"],
            ["BPC 157", "BC10", "10mg*10vials", "$65.00", "As Needed", "As Needed"],
            ["BPC 157", "BC20", "20mg*10vials", "$110.00", "As Needed", "As Needed"],
            ["Ipamorelin", "Ipa5", "5mg*10vials", "$45.00", "As Needed", "As Needed"],
            ["Ipamorelin", "Ipa10", "10mg * 10vials", "$70.00", "~66 Weeks (15 Mo)", "Month 13"],
            ["KPV", "KP5", "5mg*10vials", "$45.00", "As Needed", "As Needed"],
            ["KPV", "KP10", "10mg*10vials", "$65.00", "As Needed", "As Needed"],
            ["KPV", "KP30", "30mg*10vials", "$125.00", "As Needed", "As Needed"],
            ["VIP", "VIP5", "5mg*10vials", "$70.00", "As Needed", "As Needed"],
            ["VIP", "VIP10", "10mg*10vials", "$125.00", "As Needed", "As Needed"],
            ["TB500", "TB5", "5mg*10vials", "$80.00", "As Needed", "As Needed"],
            ["TB500", "TB10", "10mg*10vials", "$145.00", "As Needed", "As Needed"],
            ["AOD 9064", "AOD5", "5mg*10vials", "$90.00", "As Needed", "As Needed"],
            ["AOD 9064", "AOD10", "10mg*10vials", "$170.00", "As Needed", "As Needed"],
            ["NAD+", "NJ100", "100mg*10vials", "$25.00", "As Needed", "As Needed"],
            ["NAD+", "NJ500", "500mg * 10vials", "$55.00", "~26.6 Weeks (6.5 Mo)", "Month 5"],
            ["NAD+", "NJ1000", "1000mg*10vials", "$80.00", "As Needed", "As Needed"],
            ["Selank", "sk5", "5mg*10vials", "$35.00", "As Needed", "As Needed"],
            ["Selank", "sk10", "10mg * 10vials", "$55.00", "~66 Weeks (15 Mo)", "Month 13"],
            ["Selank", "sk30", "30mg*10vials", "$145.00", "As Needed", "As Needed"],
            ["Semax", "XA5", "5mg*10vials", "$35.00", "As Needed", "As Needed"],
            ["Semax", "XA10", "10mg * 10vials", "$55.00", "~66 Weeks (15 Mo)", "Month 13"],
            ["Semax", "XA30", "30mg*10vials", "$145.00", "As Needed", "As Needed"],
            ["5-Amino-1MQ", "5AM", "5mg*10vials", "$35.00", "As Needed", "As Needed"],
            ["5-Amino-1MQ", "10AM", "10mg*10vials", "$45.00", "As Needed", "As Needed"],
            ["5-Amino-1MQ", "50AM", "50mg * 10vials", "$90.00", "~40 Weeks (9 Mo)", "Month 7.5"],
            ["Epithalon (Seasonal)", "ET10", "10mg * 10vials", "$55.00", "10 doses/cycle", "As Needed"],
            ["Epithalon", "ET50", "50mg*10vials", "$155.00", "As Needed", "As Needed"],
            ["ARA290 (Cibinetide)", "ARA10", "10mg*10vials", "$70.00", "As Needed", "As Needed"],
            ["Adipotide", "AP5", "5mg*10vials", "$155.00", "As Needed", "As Needed"],
            ["Adipotide", "AP10", "10mg*10vials", "$260.00", "As Needed", "As Needed"],
            ["Aicar", "AR50", "50mg*10vials", "$45.00", "As Needed", "As Needed"],
            ["Aicar", "AR100", "100mg*10vials", "$80.00", "As Needed", "As Needed"],
            ["Vitamin B12", "B12", "1mg/ml", "$55.00", "N/A", "As Needed"],
            ["BPC 5mg + TB 5mg", "BB10", "10mg*10vials", "$100.00", "As Needed", "As Needed"],
            ["BPC 10mg + TB 10mg", "BB20", "20mg*10vials", "$180.00", "As Needed", "As Needed"],
            ["CJC 1295 (No DAC)", "CND2", "2mg*10vials", "$55.00", "As Needed", "As Needed"],
            ["CJC 1295 (No DAC)", "CND5", "5mg*10vials", "$80.00", "As Needed", "As Needed"],
            ["CJC 1295 (No DAC)", "CND10", "10mg*10vials", "$155.00", "As Needed", "As Needed"],
            ["CJC 1295 with DAC", "CD2", "2mg*10vials", "$90.00", "As Needed", "As Needed"],
            ["CJC 1295 with DAC", "CD5", "5mg*10vials", "$160.00", "As Needed", "As Needed"],
            ["CJC 1295 with DAC", "CD10", "10mg*10vials", "$270.00", "As Needed", "As Needed"],
            ["CJC 1295 (No DAC) 5mg+IPA 5mg", "CP10", "10mg*10vials", "$80.00", "As Needed", "As Needed"],
            ["Cagrilintide", "CGL5", "5mg*10vials", "$110.00", "As Needed", "As Needed"],
            ["Cagrilintide", "CGL10", "10mg*10vials", "$180.00", "As Needed", "As Needed"],
            ["Cagrilintide", "CGL20", "20mg*10vials", "$290.00", "As Needed", "As Needed"],
            ["Thymosin Alpha-1 (Seasonal)", "TA10", "10mg * 10vials", "$155.00", "~6 doses/vial", "As Needed"],
            ["Thymosin Alpha-1", "TA5", "5mg*10vials", "$90.00", "As Needed", "As Needed"],
            ["DSIP", "DS5", "5mg*10vials", "$40.00", "As Needed", "As Needed"],
            ["DSIP", "DS10", "10mg * 10vials", "$75.00", "~100 Weeks (23 Mo)", "Month 20"],
            ["DSIP", "DS15", "15mg*10vials", "$115.00", "As Needed", "As Needed"],
            ["FOXO4", "FOX10", "10mg*10vials", "$385.00", "As Needed", "As Needed"],
            ["GHRP-2", "G25", "5mg*10vials", "$40.00", "As Needed", "As Needed"],
            ["GHRP-2", "G210", "10mg*10vials", "$55.00", "As Needed", "As Needed"],
            ["GHRP-6", "G65", "5mg*10vials", "$40.00", "As Needed", "As Needed"],
            ["GHRP-6", "G610", "10mg*10vials", "$55.00", "As Needed", "As Needed"],
            ["LL37", "LL375", "5mg*10vials", "$100.00", "As Needed", "As Needed"],
            ["Melanotan I", "MT1", "10mg*10vials", "$55.00", "As Needed", "As Needed"],
            ["Melanotan II", "ML2", "10mg*10vials", "$55.00", "As Needed", "As Needed"],
            ["Kisspeptin-10", "KS5", "5mg*10vials", "$55.00", "As Needed", "As Needed"],
            ["Kisspeptin-10", "KS10", "10mg*10vials", "$80.00", "As Needed", "As Needed"],
            ["Mazdutide", "MAZ10", "10mg*10vials", "$305.00", "As Needed", "As Needed"],
            ["Oxytocin Acetate", "oxy5", "5mg*10vials", "$55.00", "As Needed", "As Needed"],
            ["Oxytocin Acetate", "oxy10", "10mg*10vials", "$70.00", "As Needed", "As Needed"],
            ["Pinealon", "Pin10", "10mg * 10vials", "$70.00", "~33 Weeks (8 Mo)", "Month 6.5"],
            ["Sermorelin Acetate", "Serm5", "5mg*10vials", "$70.00", "As Needed", "As Needed"],
            ["Sermorelin Acetate", "Serm10", "10mg*10vials", "$125.00", "As Needed", "As Needed"],
            ["Snap8", "Snap10", "10mg*10vials", "$45.00", "As Needed", "As Needed"],
            ["Snap8", "Snap20", "20mg*10vials", "$70.00", "As Needed", "As Needed"],
            ["HGH Fragment 176-191", "FRAG5", "5mg*10vials", "$80.00", "As Needed", "As Needed"],
            ["HGH Fragment 176-191", "FRAG10", "10mg*10vials", "$145.00", "As Needed", "As Needed"],
            ["HGH Fragment 176-191", "FRAG12", "12mg*10vials", "$160.00", "As Needed", "As Needed"],
            ["HGH Fragment 176-191", "FRAG15", "15mg*10vials", "$205.00", "As Needed", "As Needed"],
            ["HMG", "G75", "75iu*10vials", "$60.00", "As Needed", "As Needed"],
            ["Hexarelin Acetate", "HX2", "2mg*10vials", "$45.00", "As Needed", "As Needed"],
            ["Hexarelin Acetate", "HX5", "5mg*10vials", "$100.00", "As Needed", "As Needed"],
            ["Lipo-C", "LC10", "10ml * 10vials", "$55.00", "100 Doses (~1 Year)", "Month 10"],
            ["PEG MGF", "PMF2", "2mg*10vials", "$80.00", "As Needed", "As Needed"],
            ["PT141", "PT10", "10mg*10vials", "$65.00", "As Needed", "As Needed"],
            ["Thymalin/Thymulin", "TY10", "10mg*10vials", "$65.00", "As Needed", "As Needed"],
            ["Glutathione", "GTT600", "600mg * 10vials", "$35.00", "~60 Weeks (14 Mo)", "Month 12"],
            ["Glutathione", "GTT1500", "1500mg*10vials", "$65.00", "As Needed", "As Needed"],
            ["Gonadorelin Acetate", "GND2", "2mg*10vials", "$35.00", "As Needed", "As Needed"],
            ["Gonadorelin Acetate", "GND5", "5mg*10vials", "$55.00", "As Needed", "As Needed"],
            ["Survodutide", "SUR10", "10mg*10vials", "$215.00", "As Needed", "As Needed"],
            ["ACE 031", "AC1", "1mg*10vials", "$35.00", "As Needed", "As Needed"],
            ["Cagrisema (2.5mg+2.5mg)", "CS5", "5mg*10vials", "$70.00", "As Needed", "As Needed"],
            ["Cagrisema (5mg+5mg)", "CS10", "10mg*10vials", "$115.00", "As Needed", "As Needed"],
            ["EPO", "EPO3000", "3000iu *10vials", "$60.00", "As Needed", "As Needed"],
            ["Acetic acid 0.6% water", "AA3", "3ml *10vials", "$10.00", "As Needed", "As Needed"],
            ["Acetic acid 0.6% water", "AA5", "5ml*10vials", "$15.00", "As Needed", "As Needed"],
            ["Acetic acid 0.6% water", "AA10", "10ml*10vials", "$20.00", "As Needed", "As Needed"],
            ["Lemon Bottle", "LB10", "10ml*10vials", "$55.00", "As Needed", "As Needed"],
            ["Bacteriostatic Water", "BAC3", "3ml *10vials", "$10.00", "As Needed", "As Needed"],
            ["Bacteriostatic Water", "BAC10", "10ml * 10vials", "$15.00", "N/A", "As Needed"]
        ];

        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            
            document.getElementById('tab-' + tabId).style.display = 'block';
            event.currentTarget.classList.add('active');
            
            if (tabId === 'reconstitute') {
                loadReconstitutionTable();
            } else if (tabId === 'orders') {
                loadOrdersTable();
            } else if (tabId === 'analyzer') {
                loadConflictAnalyzer();
            } else if (tabId === 'baselines') {
                loadBaselinesTable();
            }
        }

        // --- DASHBOARD & PROTOCOL STATE ---
        function loadDashboardState() {
            fetch('/api/state')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('widget-weight').innerText = data.weight ? data.weight + ' lbs' : '-- lbs';
                    document.getElementById('widget-pain').innerText = data.last_pain ? data.last_pain + '/10' : '--/10';
                    document.getElementById('r_weight').value = data.weight || '';

                    // Load Protocol Config widgets
                    document.getElementById('settings-start-date').value = data.settings.pivot_start_date || '';
                    document.getElementById('settings-epithalon').checked = data.settings.epithalon_active === '1';
                    document.getElementById('settings-ta1').checked = data.settings.ta1_active === '1';
                    document.getElementById('settings-mots-last-date').innerText = "Last Injection: " + (data.settings.last_mots_c_date || '--');

                    // Compute Protocol Banner
                    const start_date = new Date(data.settings.pivot_start_date);
                    const today = new Date();
                    const diffTime = Math.abs(today - start_date);
                    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                    const is_kisspeptin = diffDays > 90;
                    
                    let bannerText = `Day ${diffDays} of Endocrine Protocol &middot; `;
                    if (is_kisspeptin) {
                        bannerText += `<span style="color: var(--accent-purple);">Phase: Day 91+ (Kisspeptin active, Clomid retired)</span>`;
                    } else {
                        bannerText += `<span style="color: var(--accent-green);">Phase: Days 1-90 Pivot (Clomid EOD active)</span>`;
                    }
                    document.getElementById('protocol-status-banner').innerHTML = bannerText;

                    // Load Checklist
                    const schedule = data.schedule || {};
                    const checked = data.checked_logs || [];
                    const container = document.getElementById('checklist-container');
                    container.innerHTML = '';

                    const periods = ['morning', 'midday', 'night'];
                    periods.forEach(period => {
                        const items = schedule[period] || [];
                        if (items.length > 0) {
                            const section = document.createElement('div');
                            section.className = 'checklist-group';
                            section.innerHTML = `<h3>${period}</h3>`;
                            
                            items.forEach(item => {
                                const isChecked = checked.includes(item);
                                const itemDiv = document.createElement('div');
                                itemDiv.className = 'check-item';
                                itemDiv.innerHTML = `
                                    <input type="checkbox" ${isChecked ? 'checked' : ''} onchange="toggleChecklist('${item}', this.checked)">
                                    <span style="font-size: 0.95rem; margin-left: 10px;">${item}</span>
                                `;
                                section.appendChild(itemDiv);
                            });
                            container.appendChild(section);
                        }
                    });
                })
                .catch(err => console.error("Error loading state:", err));
        }

        function toggleChecklist(itemText, isChecked) {
            const payload = {
                events: [{
                    type: 'toggle_checklist',
                    item: itemText,
                    checked: isChecked ? 1 : 0
                }]
            };

            fetch('/api/sync', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(() => loadDashboardState())
            .catch(err => console.error("Error toggling checklist:", err));
        }

        function saveProtocolSettings() {
            const payload = {
                pivot_start_date: document.getElementById('settings-start-date').value,
                epithalon_active: document.getElementById('settings-epithalon').checked ? '1' : '0',
                ta1_active: document.getElementById('settings-ta1').checked ? '1' : '0'
            };

            fetch('/api/settings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(() => loadDashboardState())
            .catch(err => console.error("Error saving settings:", err));
        }

        function logMotsCInjection() {
            const todayStr = new Date().toISOString().split('T')[0];
            fetch('/api/settings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ last_mots_c_date: todayStr })
            })
            .then(res => res.json())
            .then(() => {
                alert("Logged MOTS-c Injection for today!");
                loadDashboardState();
            })
            .catch(err => console.error("Error logging MOTS-c:", err));
        }

        // --- TAB: LOG STATS WORKFLOW ---
        function logWorkout(e) {
            e.preventDefault();
            const payload = {
                events: [{
                    type: 'log_workout',
                    workout_type: document.getElementById('w_type').value,
                    duration: parseInt(document.getElementById('w_duration').value),
                    avg_hr: parseInt(document.getElementById('w_hr').value),
                    details: document.getElementById('w_details').value
                }]
            };

            fetch('/api/sync', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(() => {
                alert("Workout logged successfully!");
                document.getElementById('workout-form').reset();
                switchTab('dashboard');
                loadDashboardState();
            })
            .catch(err => console.error("Error logging workout:", err));
        }

        function logRecovery(e) {
            e.preventDefault();
            const payload = {
                events: [{
                    type: 'log_recovery',
                    joint_pain: parseInt(document.getElementById('r_pain').value),
                    soreness: parseInt(document.getElementById('r_soreness').value),
                    sleep_quality: parseInt(document.getElementById('r_sleep').value),
                    weight_lbs: parseFloat(document.getElementById('r_weight').value),
                    notes: document.getElementById('r_notes').value
                }]
            };

            fetch('/api/sync', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(() => {
                alert("Recovery logs saved!");
                document.getElementById('recovery-form').reset();
                switchTab('dashboard');
                loadDashboardState();
            })
            .catch(err => console.error("Error saving recovery:", err));
        }

        // --- TAB: RECONSTITUTION ---
        function loadReconstitutionTable() {
            const body = document.getElementById('reconstitute-table-body');
            body.innerHTML = '';
            
            reconstitutionData.forEach(row => {
                const tr = document.createElement('tr');
                tr.style.cursor = 'pointer';
                tr.onclick = () => {
                    // Populate calculator
                    const size = parseFloat(row[2]);
                    const bac = parseFloat(row[3]);
                    const target = row[4];
                    
                    document.getElementById('calc-vial-size').value = isNaN(size) ? '' : size;
                    document.getElementById('calc-bac-water').value = isNaN(bac) ? '' : bac;
                    
                    // Regex extract target dose mcg (e.g. 500mcg or 1mg)
                    let target_val = '';
                    if (target.includes('mcg')) {
                        const match = target.match(/(\\d+)\\s*mcg/);
                        if (match) target_val = match[1];
                    } else if (target.includes('mg')) {
                        const match = target.match(/(\\d+)\\s*mg/);
                        if (match) target_val = parseFloat(match[1]) * 1000;
                    }
                    document.getElementById('calc-target-dose').value = target_val;
                    runCalculator();
                };
                
                row.forEach(cell => {
                    const td = document.createElement('td');
                    td.innerText = cell;
                    tr.appendChild(td);
                });
                body.appendChild(tr);
            });
        }

        function runCalculator() {
            const size = parseFloat(document.getElementById('calc-vial-size').value);
            const water = parseFloat(document.getElementById('calc-bac-water').value);
            const dose = parseFloat(document.getElementById('calc-target-dose').value); // in mcg

            const resultDiv = document.getElementById('calc-result');

            if (!size || !water || !dose) {
                resultDiv.innerText = '-- Units';
                return;
            }

            // Calculations:
            // total mcg in vial = size * 1000
            // total units in syringe = water * 100 (for U100 syringe)
            // mcg per unit = total mcg / total units
            // units to draw = dose / mcg per unit
            const totalMcg = size * 1000;
            const totalUnits = water * 100;
            const mcgPerUnit = totalMcg / totalUnits;
            const drawUnits = dose / mcgPerUnit;

            resultDiv.innerText = drawUnits.toFixed(1) + ' Units';
        }

        // --- TAB: ORDERS ---
        function loadOrdersTable() {
            // Fill vendor kit table
            const pricingBody = document.getElementById('vendor-pricing-table');
            pricingBody.innerHTML = '';
            vendorData.forEach(row => {
                const tr = document.createElement('tr');
                tr.style.cursor = 'pointer';
                tr.onclick = () => {
                    document.getElementById('o_name').value = row[0];
                    // Regex extract kit specs
                    const size_match = row[2].match(/(\\d+)\\s*mg/);
                    document.getElementById('o_size').value = size_match ? size_match[1] : '';
                    document.getElementById('o_vials').value = 10; // Kit default
                };

                row.forEach(cell => {
                    const td = document.createElement('td');
                    td.innerText = cell;
                    tr.appendChild(td);
                });
                pricingBody.appendChild(tr);
            });

            // Fetch logged orders from server
            fetch('/api/orders')
                .then(res => res.json())
                .then(orders => {
                    const logBody = document.getElementById('orders-log-table');
                    logBody.innerHTML = '';
                    if (orders.length === 0) {
                        logBody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--text-secondary);">No orders logged yet.</td></tr>';
                        return;
                    }
                    orders.forEach(o => {
                        const tr = document.createElement('tr');
                        tr.innerHTML = `
                            <td>${o.item_name}</td>
                            <td>${o.order_date}</td>
                            <td>${o.quantity_vials} (${o.vial_size_mg}mg)</td>
                            <td>${o.dosage_units} U</td>
                            <td>${o.frequency_per_week}x</td>
                            <td style="color: var(--accent-warning); font-weight: 600;">${o.depletion_date}</td>
                        `;
                        logBody.appendChild(tr);
                    });
                })
                .catch(err => console.error("Error loading orders:", err));
        }

        function filterVendorTable() {
            const query = document.getElementById('order-search').value.toLowerCase();
            const rows = document.getElementById('vendor-pricing-table').querySelectorAll('tr');
            rows.forEach(tr => {
                const text = tr.innerText.toLowerCase();
                tr.style.display = text.includes(query) ? '' : 'none';
            });
        }

        function logNewOrder(e) {
            e.preventDefault();
            const payload = {
                item_name: document.getElementById('o_name').value,
                quantity_vials: parseInt(document.getElementById('o_vials').value),
                vial_size_mg: parseFloat(document.getElementById('o_size').value),
                dosage_units: parseInt(document.getElementById('o_dose').value),
                frequency_per_week: parseInt(document.getElementById('o_freq').value)
            };

            fetch('/api/orders', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(data => {
                alert(`Order Saved! Est. depletion: ${data.depletion_date}`);
                document.getElementById('order-form').reset();
                loadOrdersTable();
            })
            .catch(err => console.error("Error logging order:", err));
        }

        // --- TAB: CONFLICT SCAN ---
        const scanCompounds = [
            "Mounjaro (Tirzepatide)", "Semaglutide (Ozempic/Wegovy)", "Retatrutide",
            "Tesamorelin", "CJC-1295 (No DAC)", "Sermorelin", "Ipamorelin",
            "BPC-157 (Standalone)", "TB-500 (Standalone)", 
            "KLOW Blend (GHK-Cu, BPC-157, TB-500, KPV)", "NAD+ (Injectable)", 
            "5-Amino-1MQ", "SS-31 (Elamipretide)", "MOTS-c", "Jardiance (Empagliflozin)"
        ];

        function loadConflictAnalyzer() {
            const grid = document.getElementById('analyzer-checkboxes');
            grid.innerHTML = '';
            scanCompounds.forEach((c, idx) => {
                const card = document.createElement('label');
                card.className = 'conflict-card';
                card.innerHTML = `
                    <input type="checkbox" id="scan-c-${idx}" value="${c}">
                    <span style="font-size: 0.9rem;">${c}</span>
                `;
                grid.appendChild(card);
            });
        }

        function runConflictAnalysis() {
            const active = [];
            scanCompounds.forEach((c, idx) => {
                const cb = document.getElementById(`scan-c-${idx}`);
                if (cb && cb.checked) {
                    active.push(c);
                }
            });

            const resultBox = document.getElementById('analyzer-result');
            resultBox.innerHTML = '';
            resultBox.style.display = 'block';

            const conflicts = [];

            // GLP-1 Overlap
            const glp1 = ["Mounjaro (Tirzepatide)", "Semaglutide (Ozempic/Wegovy)", "Retatrutide"];
            const glp1_count = active.filter(x => glp1.includes(x)).length;
            if (glp1_count > 1) {
                conflicts.push("⚠️ <strong>GLP-1 Receptor Agonist Overload:</strong> Multiple glycemic weight loss agonists selected. Combining Tirzepatide, Semaglutide, or Retatrutide is highly redundant and increases gastrointestinal/glycemic risks.");
            }

            // GHRH Overlap
            const ghrh = ["Tesamorelin", "CJC-1295 (No DAC)", "Sermorelin"];
            const ghrh_count = active.filter(x => ghrh.includes(x)).length;
            if (ghrh_count > 1) {
                conflicts.push("⚠️ <strong>Pituitary GHRH Receptor Overlap:</strong> Selected multiple GHRH analogs (e.g. CJC-1295, Tesamorelin, Sermorelin). These target the same receptors, causing redundant competition & receptor desensitization.");
            }

            // Tissue Repair
            const healing = active.includes("KLOW Blend (GHK-Cu, BPC-157, TB-500, KPV)") && 
                            (active.includes("BPC-157 (Standalone)") || active.includes("TB-500 (Standalone)"));
            if (healing) {
                conflicts.push("⚠️ <strong>Tissue-Repair Redundancy:</strong> Standalone BPC-157/TB-500 overlaps with KLOW Blend, which already contains both. Avoid double-dosing these regenerative pathways.");
            }

            // Mitochondrial strain
            const mito = ["NAD+ (Injectable)", "5-Amino-1MQ", "SS-31 (Elamipretide)", "MOTS-c"];
            const mito_count = active.filter(x => mito.includes(x)).length;
            if (mito_count > 2) {
                conflicts.push("⚠️ <strong>Mitochondrial Overstimulation:</strong> Stacking NAD+, 5-Amino-1MQ, SS-31, and MOTS-c simultaneously places intense metabolic demands on your cell-clearing pathways. Consider cycling them instead.");
            }

            // Jardiance + Mounjaro
            if (active.includes("Jardiance (Empagliflozin)") && active.includes("Mounjaro (Tirzepatide)")) {
                conflicts.push("ℹ️ <strong>Prescription Co-Administration Sync:</strong> Combining SGLT2 inhibitors (Jardiance) and GLP-1/GIP agonists (Mounjaro) requires careful tracking of HbA1c and hydration levels. Ensure your physician has cleared your kidney filtration values (eGFR).");
            }

            if (conflicts.length === 0) {
                resultBox.innerHTML = `
                    <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid var(--accent-green); color: #34d399; padding: 15px; border-radius: 12px; margin-top: 15px;">
                        ✅ No conflicts or redundancies found! Your selected stack targets distinct, safe physiological pathways.
                    </div>
                `;
            } else {
                conflicts.forEach(c => {
                    const alertDiv = document.createElement('div');
                    alertDiv.className = 'conflict-alert';
                    alertDiv.innerHTML = c;
                    resultBox.appendChild(alertDiv);
                });
            }
        }

        // --- TAB: BASELINES & LABS ---
        function loadBaselinesTable() {
            fetch('/api/baselines')
                .then(res => res.json())
                .then(data => {
                    const body = document.getElementById('baselines-table-body');
                    body.innerHTML = '';
                    
                    data.forEach(r => {
                        const tr = document.createElement('tr');
                        tr.style.cursor = 'pointer';
                        tr.onclick = () => selectMarker(r.marker_name, r.current_value);
                        
                        let varColor = 'var(--text-primary)';
                        if (r.variance.startsWith('+')) varColor = 'var(--accent-red)';
                        if (r.variance.startsWith('-')) varColor = 'var(--accent-green)';
                        if (r.marker_name === 'Weight') varColor = 'var(--accent-green)'; // Loss is good

                        tr.innerHTML = `
                            <td style="font-weight: 600;">${r.marker_name}</td>
                            <td>${r.baseline_value}</td>
                            <td style="color: var(--accent-blue); font-weight: 600;">${r.current_value}</td>
                            <td>${r.unit}</td>
                            <td style="color: ${varColor}; font-weight: 600;">${r.variance || '0.0%'}</td>
                            <td style="font-size: 0.8rem; color: var(--text-secondary);">${r.notes}</td>
                        `;
                        body.appendChild(tr);
                    });
                })
                .catch(err => console.error("Error loading baselines:", err));
        }

        function selectMarker(markerName, currentVal) {
            selectedMarkerName = markerName;
            document.getElementById('selected-marker-lbl').innerText = `Selected Marker: ${markerName}`;
            document.getElementById('l_value').value = currentVal || '';
            document.getElementById('l_new_baseline').value = '';
            document.getElementById('l_date').value = new Date().toISOString().split('T')[0];
            
            // Load History
            loadMarkerHistory(markerName);
        }

        function loadMarkerHistory(marker) {
            const container = document.getElementById('biometrics-history-container');
            container.innerHTML = 'Loading history...';

            fetch(`/api/baselines/history?marker=${encodeURIComponent(marker)}`)
                .then(res => res.json())
                .then(history => {
                    container.innerHTML = '';
                    if (history.length === 0) {
                        container.innerText = `No history logged for: ${marker}`;
                        return;
                    }
                    history.forEach(h => {
                        const div = document.createElement('div');
                        div.style.marginBottom = '6px';
                        div.innerHTML = `<span style="color: var(--accent-blue);">[${h.recorded_date}]</span> <strong style="color: #ffffff;">${h.recorded_value}</strong> | ${h.notes || 'No context'}`;
                        container.appendChild(div);
                    });
                })
                .catch(err => {
                    container.innerText = "Error loading history.";
                    console.error(err);
                });
        }

        function logLabReading(e) {
            e.preventDefault();
            if (!selectedMarkerName) {
                alert("Please select a biomarker first!");
                return;
            }

            const payload = {
                marker_name: selectedMarkerName,
                recorded_value: parseFloat(document.getElementById('l_value').value),
                recorded_date: document.getElementById('l_date').value,
                notes: document.getElementById('l_notes').value
            };

            fetch('/api/baselines', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(() => {
                alert(`Logged reading for ${selectedMarkerName}!`);
                document.getElementById('lab-reading-form').reset();
                loadBaselinesTable();
                loadMarkerHistory(selectedMarkerName);
            })
            .catch(err => console.error("Error logging reading:", err));
        }

        function updateBaselineReference() {
            if (!selectedMarkerName) {
                alert("Please select a biomarker first!");
                return;
            }
            const val = parseFloat(document.getElementById('l_new_baseline').value);
            if (isNaN(val)) {
                alert("Please enter a valid numeric baseline value.");
                return;
            }

            const payload = {
                marker_name: selectedMarkerName,
                baseline_value: val
            };

            fetch('/api/baselines', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(() => {
                alert(`Baseline reference for ${selectedMarkerName} updated!`);
                document.getElementById('l_new_baseline').value = '';
                loadBaselinesTable();
            })
            .catch(err => console.error("Error updating baseline:", err));
        }

        // --- TAB: AI RAG ---
        function handleQueryKey(e) {
            if (e.key === 'Enter') {
                submitQuery();
            }
        }

        function submitQuery() {
            const input = document.getElementById('ai-query-input');
            const queryText = input.value.trim();
            if (!queryText) return;

            const spinner = document.getElementById('query-spinner');
            const resultBox = document.getElementById('ai-result-box');
            const refBox = document.getElementById('ai-references-box');

            spinner.style.display = 'block';
            resultBox.style.display = 'none';
            refBox.innerHTML = '';

            fetch('/api/peptide/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: queryText })
            })
            .then(res => res.json())
            .then(data => {
                spinner.style.display = 'none';
                
                if (data.error) {
                    resultBox.innerText = "Error: " + data.error;
                    resultBox.style.display = 'block';
                    return;
                }

                // Simple parser markdown headers/lists to HTML format
                let htmlResponse = data.response
                    .replace(/### (.*)/g, '<h3 style="color: var(--accent-blue); margin-top: 15px; margin-bottom: 8px;">$1</h3>')
                    .replace(/#### (.*)/g, '<h4 style="color: var(--accent-green); margin-top: 10px; margin-bottom: 5px;">$1</h4>')
                    .replace(/\\*\\*(.*?)\\*\\/g, '<strong>$1</strong>')
                    .replace(/- (.*)/g, '<li style="margin-left: 15px; margin-bottom: 4px;">$1</li>')
                    .replace(/\\n/g, '<br>');

                resultBox.innerHTML = htmlResponse;
                resultBox.style.display = 'block';

                if (data.papers && data.papers.length > 0) {
                    const header = document.createElement('h3');
                    header.style.color = 'var(--text-primary)';
                    header.style.marginTop = '25px';
                    header.innerText = '📚 Referenced Scientific Abstracts';
                    refBox.appendChild(header);

                    data.papers.forEach(paper => {
                        const card = document.createElement('div');
                        card.className = 'paper-card';
                        card.innerHTML = `
                            <div class="paper-title">${paper.title}</div>
                            <div style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 8px;">
                                ${paper.journal} (${paper.year}) &middot; <a style="color: var(--accent-blue); text-decoration: none;" href="${paper.link}" target="_blank">View on PubMed</a>
                            </div>
                            <div style="font-size: 0.85rem; line-height: 1.5; color: #cbd5e1;">${paper.abstract}</div>
                        `;
                        refBox.appendChild(card);
                    });
                }
            })
            .catch(err => {
                spinner.style.display = 'none';
                resultBox.innerText = "Error requesting AI report: " + err;
                resultBox.style.display = 'block';
            });
        }

        // Initial Load
        loadDashboardState();
    </script>
</body>
</html>
"""

# DB Helper to initialize/migrate tables and default baseline markers
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables if not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS checklist_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            item_text TEXT NOT NULL,
            checked INTEGER DEFAULT 0,
            UNIQUE(date, item_text)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            workout_type TEXT NOT NULL,
            duration INTEGER,
            avg_hr INTEGER,
            details TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recovery_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE NOT NULL,
            joint_pain INTEGER,
            soreness INTEGER,
            sleep_quality INTEGER,
            weight_lbs REAL,
            notes TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            order_date TEXT NOT NULL,
            quantity_vials INTEGER NOT NULL,
            vial_size_mg REAL NOT NULL,
            dosage_units INTEGER NOT NULL,
            frequency_per_week INTEGER NOT NULL,
            depletion_date TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS baselines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marker_name TEXT UNIQUE NOT NULL,
            baseline_value REAL,
            current_value REAL,
            unit TEXT NOT NULL,
            notes TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS biometrics_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marker_name TEXT NOT NULL,
            recorded_value REAL NOT NULL,
            recorded_date TEXT NOT NULL,
            notes TEXT
        )
    """)

    # Seed Default Settings
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('pivot_start_date', ?)", (datetime.now().strftime("%Y-%m-%d"),))
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('last_mots_c_date', '2026-08-08')")
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('epithalon_active', '0')")
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('ta1_active', '0')")

    # Seed Baseline markers
    default_markers = [
        ("HbA1c", 5.4, 5.4, "%", "Blood sugar management marker (Jardiance tracking)"),
        ("eGFR", 92.0, 92.0, "mL/min/1.73m2", "Kidney filtration rate (Renal safety tracker)"),
        ("Total Testosterone", 420.0, 420.0, "ng/dL", "Endocrine pivot target (Clomid/Kisspeptin)"),
        ("LDL Cholesterol", 110.0, 110.0, "mg/dL", "Lipid safety baseline (Atorvastatin tracker)"),
        ("HDL Cholesterol", 45.0, 45.0, "mg/dL", "Lipid safety baseline (Atorvastatin tracker)"),
        ("Resting Heart Rate", 68.0, 68.0, "bpm", "Cardiovascular baseline"),
        ("Systolic BP", 120.0, 120.0, "mmHg", "Blood pressure tracking (Lisinopril tracker)"),
        ("Diastolic BP", 80.0, 80.0, "mmHg", "Blood pressure tracking (Lisinopril tracker)"),
        ("Fasting Glucose", 95.0, 95.0, "mg/dL", "Glucose management (Jardiance tracker)"),
        ("Triglycerides", 150.0, 150.0, "mg/dL", "Lipid safety baseline (Atorvastatin tracker)"),
        ("IGF-1", 150.0, 150.0, "ng/mL", "Growth hormone tracking (Tesamorelin/Ipamorelin)"),
        ("LH", 4.0, 4.0, "mIU/mL", "Luteinizing Hormone (Clomid tracking)"),
        ("FSH", 4.0, 4.0, "mIU/mL", "Follicle-Stimulating Hormone (Clomid tracking)"),
        ("ALT", 25.0, 25.0, "U/L", "Liver function enzyme (Hepatic safety rest)"),
        ("AST", 25.0, 25.0, "U/L", "Liver function enzyme (Hepatic safety rest)"),
        ("Creatinine", 0.9, 0.9, "mg/dL", "Kidney function marker (Renal safety rest)"),
        ("Vitamin B12", 500.0, 500.0, "pg/mL", "B12 levels (Vitamin B12 injection tracker)"),
        ("Vitamin D, 25-OH", 40.0, 40.0, "ng/mL", "Vitamin D levels (Supplement tracker)"),
        ("Magnesium", 2.0, 2.0, "mg/dL", "Magnesium levels (Supplement tracker)"),
        ("Weight", 362.3, 310.0, "lbs", "Bodyweight baseline tracker (Down from 362.3 lbs, -52.3 lbs lost)")
    ]
    for marker, val, cur, unit, notes in default_markers:
        cursor.execute("""
            INSERT OR IGNORE INTO baselines (marker_name, baseline_value, current_value, unit, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (marker, val, cur, unit, notes))

    conn.commit()
    conn.close()

# Helper to compute checklist items dynamically based on settings in SQLite
def get_day_schedule():
    now_dt = datetime.now()
    day_name = now_dt.strftime("%A")

    # Load settings from db
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM settings")
    settings = dict(cursor.fetchall())
    conn.close()

    pivot_start_str = settings.get('pivot_start_date', now_dt.strftime("%Y-%m-%d"))
    try:
        pivot_start = datetime.strptime(pivot_start_str, "%Y-%m-%d")
        days_diff = (now_dt - pivot_start).days + 1
    except Exception:
        days_diff = 1

    is_kisspeptin_phase = days_diff > 90
    epithalon_active = settings.get('epithalon_active') == '1'
    ta1_active = settings.get('ta1_active') == '1'

    morning = []
    midday = []
    night = []

    # Daily basic meds
    morning.append("Daily Morning Meds: Jardiance (25mg) | Lisinopril (5mg)")
    night.append("Daily Nighttime Meds: Atorvastatin (40mg) | Cetirizine HCL (10mg)")

    # Clomid logic (EOD Pivot phase days 1-90)
    is_even_day = (days_diff % 2 == 0)
    if (not is_kisspeptin_phase) and is_even_day:
        midday.append("Clomid - EOD Midday Window")

    # Seasonal cycles
    if epithalon_active:
        morning.append("🟢 Epithalon: 20 Units (1mg) daily circadian reset")
    if ta1_active and day_name in ["Tuesday", "Thursday", "Saturday"]:
        morning.append("🟢 Thymosin Alpha-1 (TA-1): 30 Units (1.5mg) immune management")

    # Wash / Peptide day routing
    if day_name in ["Monday", "Thursday"]:
        morning.append("🧘 Active Rest: Perform 5-10 mins of light stretching")
        midday.append("🏃 Workout: Light Mobility & Active Recovery Stretching (15 mins)")
        if day_name == "Monday":
            morning.append("🟢 Glutathione: 50 Units (Weekly Dose)")
            midday.extend([
                "🖊️ Mounjaro (Tirzepatide): 2.5mg (1 Pen)",
                "⚪ Lipo-C: 1.0 mL (100 Units)",
                "♦️ Vitamin B12: 0.5 mL (50 Units)",
                "🏋️ Workout: Lower Body & Joint Prep Gym Workout (Leg Press, Extensions, Treadmill progression)"
            ])
            night.extend([
                "🔴 Tesamorelin: 25 Units",
                "🔴 Ipamorelin: 5 to 10 Units",
                "🟠 KLOW Blend: 10 Units"
            ])
            if not epithalon_active:
                night.append("🌌 DSIP: 10 Units")
            if is_kisspeptin_phase:
                night.append("🩷 Kisspeptin: 5 to 10 Units")

    elif day_name == "Tuesday":
        morning.extend([
            "🟣 NAD+: 12.5 to 25 Units",
            "🟡 5-Amino-1MQ: 20 Units",
            "🟡 SS-31: 20 Units",
            "🩵 Semax: 5 to 10 Units",
            "🩵 Selank: 5 to 10 Units",
            "💜 Pinealon: 20 Units",
            "🟢 Glutathione: 50 Units (Weekly Dose)"
        ])
        midday.extend([
            "🖊️ Mounjaro (Tirzepatide): 2.5mg (1 Pen)",
            "⚪ Lipo-C: 1.0 mL (100 Units)",
            "♦️ Vitamin B12: 0.5 mL (50 Units)",
            "🏋️ Workout: Lower Body & Joint Prep Gym Workout (Leg Press, Extensions, Treadmill progression)"
        ])
        night.extend([
            "🔴 Tesamorelin: 25 Units",
            "🔴 Ipamorelin: 5 to 10 Units",
            "🟠 KLOW Blend: 10 Units"
        ])
        if not epithalon_active:
            night.append("🌌 DSIP: 10 Units")
        if is_kisspeptin_phase:
            night.append("🩷 Kisspeptin: 5 to 10 Units")

    elif day_name == "Friday":
        morning.extend([
            "🟣 NAD+: 12.5 to 25 Units",
            "🟡 5-Amino-1MQ: 20 Units",
            "🟡 SS-31: 20 Units",
            "🩵 Semax: 5 to 10 Units",
            "🩵 Selank: 5 to 10 Units",
            "💜 Pinealon: 20 Units"
        ])
        midday.extend([
            "⚪ Lipo-C: 1.0 mL (100 Units)",
            "♦️ Vitamin B12: 0.5 mL (50 Units)",
            "🏋️ Workout: Lower Body & Joint Prep Gym Workout (Leg Press, Extensions, Treadmill progression)"
        ])
        night.extend([
            "🔴 Tesamorelin: 25 Units",
            "🔴 Ipamorelin: 5 to 10 Units",
            "🟠 KLOW Blend: 10 Units"
        ])
        if not epithalon_active:
            night.append("🌌 DSIP: 10 Units")
        if is_kisspeptin_phase:
            night.append("🩷 Kisspeptin: 5 to 10 Units")

    elif day_name in ["Wednesday", "Saturday"]:
        morning.extend([
            "Base: Molecular Hydrogen Tablet (in water)",
            "TMG (1000mg) - NAD+ Methyl Donor",
            "Hyaluronic Acid (200mg)",
            "🧬 Urolithin A (Mitophagy Support)"
        ])
        midday.extend([
            "Base: Animal Pak Powder (in water)",
            "Pure Krill Oil (1 softgel)",
            "Ubiquinol CoQ-10 (100mg)",
            "Astaxanthin (12mg)",
            "Calcium AKG (1000mg)",
            "🧬 Fisetin (Senolytic Support)",
            "Glutathione Triple Boost (1 serving)",
            "🏊 Workout: Upper Body Strength & YMCA Lap Swim"
        ])
        night.extend([
            "Base: Collagen Peptides (in water)",
            "Magnesium Glycinate (200–400mg)"
        ])

    elif day_name == "Sunday":
        midday.append("🛌 Rest & Recovery: Pure recovery day (YMCA & Gym Closed)")
        if is_kisspeptin_phase:
            night.append("🩷 Kisspeptin: 5 to 10 Units")

    # MOTS-c floater check
    last_mots_str = settings.get('last_mots_c_date', '2026-08-08')
    try:
        last_mots = datetime.strptime(last_mots_str, "%Y-%m-%d")
        diff_mots = (now_dt.date() - last_mots.date()).days
        if diff_mots % 5 == 0:
            morning.append("🔵 MOTS-c (Floater): 50 Units (Isolated SubQ injection)")
    except Exception:
        pass

    return {"morning": morning, "midday": midday, "night": night}

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# GET/POST settings
@app.route('/api/settings', methods=['GET', 'POST'])
def handle_settings():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if request.method == 'POST':
        data = request.get_json() or {}
        for k, v in data.items():
            cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (k, str(v)))
        conn.commit()
    cursor.execute("SELECT key, value FROM settings")
    settings = dict(cursor.fetchall())
    conn.close()
    return jsonify(settings)

@app.route('/api/state')
def get_state():
    init_db()
    today = datetime.now().strftime("%Y-%m-%d")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get today's checkoff status
    cursor.execute("SELECT item_text FROM checklist_logs WHERE date=? AND checked=1", (today,))
    checked_items = [r[0] for r in cursor.fetchall()]
    
    # Get last weight log
    cursor.execute("SELECT current_value FROM baselines WHERE marker_name='Weight'")
    weight_row = cursor.fetchone()
    weight = weight_row[0] if weight_row else 310.0
    
    # Get last logged pain score
    cursor.execute("SELECT joint_pain FROM recovery_logs ORDER BY date DESC LIMIT 1")
    pain_row = cursor.fetchone()
    last_pain = pain_row[0] if pain_row else 2

    # Get settings
    cursor.execute("SELECT key, value FROM settings")
    settings = dict(cursor.fetchall())
    
    conn.close()
    
    return jsonify({
        "schedule": get_day_schedule(),
        "checked_logs": checked_items,
        "weight": weight,
        "last_pain": last_pain,
        "settings": settings
    })

@app.route('/api/sync', methods=['POST'])
def sync_data():
    init_db()
    data = request.get_json()
    events = data.get("events", [])
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    
    for ev in events:
        ev_type = ev.get("type")
        
        if ev_type == "toggle_checklist":
            cursor.execute("""
                INSERT OR REPLACE INTO checklist_logs (date, item_text, checked)
                VALUES (?, ?, ?)
            """, (today, ev.get("item"), ev.get("checked")))
            
        elif ev_type == "log_workout":
            cursor.execute("""
                INSERT INTO workouts (date, workout_type, duration, avg_hr, details)
                VALUES (?, ?, ?, ?, ?)
            """, (today, ev.get("workout_type"), ev.get("duration"), ev.get("avg_hr"), ev.get("details")))
            
        elif ev_type == "log_recovery":
            cursor.execute("""
                INSERT OR REPLACE INTO recovery_logs (date, joint_pain, soreness, sleep_quality, weight_lbs, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (today, ev.get("joint_pain"), ev.get("soreness"), ev.get("sleep_quality"), ev.get("weight_lbs"), ev.get("notes")))
            
            weight = ev.get("weight_lbs")
            if weight:
                # Sync Weight baseline
                cursor.execute("UPDATE baselines SET current_value=? WHERE marker_name='Weight'", (weight,))
                cursor.execute("""
                    INSERT INTO biometrics_history (marker_name, recorded_value, recorded_date, notes)
                    VALUES ('Weight', ?, ?, 'Logged via sync')
                """, (weight, today))
                
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "synced_count": len(events)})

# GET/POST orders
@app.route('/api/orders', methods=['GET', 'POST'])
def handle_orders():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if request.method == 'POST':
        data = request.get_json() or {}
        item = data.get("item_name")
        vials = int(data.get("quantity_vials", 10))
        size = float(data.get("vial_size_mg", 10))
        dose = int(data.get("dosage_units", 25))
        freq = int(data.get("frequency_per_week", 5))
        order_date = datetime.now().strftime("%Y-%m-%d")

        # Standard reconstitution calculation
        total_units_available = vials * 200
        weekly_consumption = dose * freq
        if weekly_consumption > 0:
            weeks_lasting = total_units_available / weekly_consumption
            days_lasting = int(weeks_lasting * 7)
            depletion_dt = datetime.now() + timedelta(days=days_lasting)
            depletion_date_str = depletion_dt.strftime("%Y-%m-%d")
        else:
            depletion_date_str = "N/A"

        cursor.execute("""
            INSERT INTO orders (item_name, order_date, quantity_vials, vial_size_mg, dosage_units, frequency_per_week, depletion_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (item, order_date, vials, size, dose, freq, depletion_date_str))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "depletion_date": depletion_date_str})

    cursor.execute("SELECT item_name, order_date, quantity_vials, vial_size_mg, dosage_units, frequency_per_week, depletion_date FROM orders ORDER BY order_date DESC")
    rows = cursor.fetchall()
    orders_list = []
    for r in rows:
        orders_list.append({
            "item_name": r[0],
            "order_date": r[1],
            "quantity_vials": r[2],
            "vial_size_mg": r[3],
            "dosage_units": r[4],
            "frequency_per_week": r[5],
            "depletion_date": r[6]
        })
    conn.close()
    return jsonify(orders_list)

# GET/POST baselines
@app.route('/api/baselines', methods=['GET', 'POST'])
def handle_baselines():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if request.method == 'POST':
        data = request.get_json() or {}
        marker = data.get("marker_name")
        val = data.get("recorded_value")
        date_str = data.get("recorded_date", datetime.now().strftime("%Y-%m-%d"))
        notes = data.get("notes", "")

        # Optional new baseline value override
        new_base = data.get("baseline_value")

        if new_base is not None:
            cursor.execute("UPDATE baselines SET baseline_value=? WHERE marker_name=?", (new_base, marker))
        
        if val is not None:
            cursor.execute("UPDATE baselines SET current_value=? WHERE marker_name=?", (val, marker))
            cursor.execute("""
                INSERT INTO biometrics_history (marker_name, recorded_value, recorded_date, notes)
                VALUES (?, ?, ?, ?)
            """, (marker, val, date_str, notes))
            
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})

    cursor.execute("SELECT marker_name, baseline_value, current_value, unit, notes FROM baselines")
    rows = cursor.fetchall()
    baselines_list = []
    for r in rows:
        marker, val, cur, unit, notes = r
        variance = ""
        if val is not None and cur is not None:
            if val != 0:
                diff_pct = ((cur - val) / val) * 100
                variance = f"{diff_pct:+.1f}%"
            else:
                variance = f"{cur - val:+.1f}"
        
        baselines_list.append({
            "marker_name": marker,
            "baseline_value": val,
            "current_value": cur,
            "unit": unit,
            "variance": variance,
            "notes": notes
        })
    conn.close()
    return jsonify(baselines_list)

# GET history
@app.route('/api/baselines/history')
def handle_baseline_history():
    marker = request.args.get("marker", "")
    if not marker:
        return jsonify([])
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT recorded_value, recorded_date, notes 
        FROM biometrics_history 
        WHERE marker_name=? 
        ORDER BY recorded_date DESC
    """, (marker,))
    rows = cursor.fetchall()
    conn.close()
    history = [{"recorded_value": r[0], "recorded_date": r[1], "notes": r[2]} for r in rows]
    return jsonify(history)

# GET peptides
@app.route('/api/peptides')
def get_peptides_db():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modules", "peptide_engine", "compound_database.json")
    if os.path.exists(db_path):
        with open(db_path, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify({})

# POST query
@app.route('/api/peptide/query', methods=['POST'])
def query_peptide_edu():
    data = request.get_json() or {}
    user_query = data.get("query", "")
    if not user_query:
        return jsonify({"error": "Missing query parameter"}), 400
        
    try:
        from modules.peptide_engine.educational_rag import PeptideEduEngine
        engine = PeptideEduEngine()
        response, papers = engine.query(user_query)
        return jsonify({
            "response": response,
            "papers": papers
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
