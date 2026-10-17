import streamlit as st
import pandas as pd
import json
import time
import os
import plotly.express as px

st.set_page_config(page_title="Midas 2.0 Live", layout="wide", page_icon="🏦")

# Iron Man Theme
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #00FFCC;
    }
    .metric-card {
        background-color: #1E1E1E;
        border: 1px solid #00FFCC;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    .status-active {
        color: #00FF00;
        font-weight: bold;
    }
    .status-sleep {
        color: #FFFF00;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏦 MIDAS 2.0 // LIVE OPERATIONS CENTER")
st.caption("MONITORING INFINITE LOOP DAEMON")

# Path to log file
LOG_FILE = r"c:\Users\z143d\OneDrive\Desktop\Project Aergia\Project Midas\trade_history.json"

def load_data():
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, 'r') as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except:
        return []

# Auto-Refresh Logic
if st.button("REFRESH NOW"):
    st.rerun()

# 1. System Heartbeat
col1, col2, col3 = st.columns(3)

data = load_data()
df = pd.DataFrame(data)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("TOTAL SCANS", len(df) if not df.empty else 0)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    last_active = df.iloc[-1]['timestamp'] if not df.empty else "WAITING..."
    st.metric("LAST HEARTBEAT", last_active)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    # Count "APPROVED" trades or similar
    trades = df[df['risk_data'].astype(str).str.contains("APPROVED", na=False)] if not df.empty else pd.DataFrame()
    st.metric("STRATEGY SIGNALS", len(trades))
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# 2. Live Feed (Data Table)
st.subheader("📡 LIVE DATA FEED")

if not df.empty:
    # Sort by time desc
    df = df.sort_index(ascending=False)
    
    # Selecting relevant columns for display
    display_cols = ['timestamp', 'ticker', 'signal_data', 'risk_data', 'researcher_data']
    
    # We might need to flatten signal_data if it's a dict/string
    st.dataframe(
        df,
        column_config={
            "timestamp": "Time",
            "ticker": "Symbol",
            "signal_data": st.column_config.TextColumn("Analyst Signal", width="medium"),
            "risk_data": st.column_config.TextColumn("Risk Guard", width="medium"),
            "researcher_data": st.column_config.TextColumn("Coach/Researcher", width="large"),
        },
        use_container_width=True,
        hide_index=True
    )
    
    # 3. Visuals (ML Probability Distribution if available)
    # Extract prob from researcher data or add it to new logs
    
else:
    st.info("WAITING FOR DATA INGESTION... (System is sleeping or initializing)")

# Auto-rerun script every 5 seconds
time.sleep(5)
st.rerun()
