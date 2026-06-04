import os
import time
import pandas as pd
import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv

# Page Configuration
st.set_page_config(page_title="Residuum_Modulus SOC", layout="wide", page_icon="⚡")
st.title("⚡ Residuum_Modulus: CPS Security Radar")
st.markdown("Live Telemetry Stream: **Microgrid3 (Industrial)**")

# Database Connection
load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI")

@st.cache_resource
def init_connection():
    return MongoClient(MONGO_URI)

client = init_connection()
db = client["microgrid_network"]
collection = db["historical_telemetry"]

# 🛠️ THE FIX: Define a fragment that updates natively every 2 seconds without full-page blinking
@st.fragment(run_every=2)
def render_live_telemetry_radar():
    # Fetch the last 30 readings for Microgrid3, sort by newest first
    cursor = collection.find({"microgrid_id": "Microgrid3"}).sort("_id", -1).limit(30)
    data = list(cursor)
    
    if data:
        # Reverse to chronological order for graphing (left to right)
        df = pd.DataFrame(data)[::-1] 
        
        # Plot the Load vs PV data
        chart_data = df.set_index("timestamp")[["load_kw", "pv_kw"]]
        st.line_chart(chart_data, color=["#FF4B4B", "#00D4FF"])
        
        # Visual Alert Logic
        latest_load = df.iloc[-1]["load_kw"]
        latest_pv = df.iloc[-1]["pv_kw"]
        
        if latest_load > 1500 and latest_pv < 900:
            st.error(f"🚨 MANIFOLD VIOLATION DETECTED! Load: {latest_load}kW | PV: {latest_pv}kW. Autonomous Mitigation Engaged.")
        else:
            st.success(f"✅ Grid Stable. Load: {latest_load}kW | PV: {latest_pv}kW")

# Invoke the localized telemetry loop
render_live_telemetry_radar()