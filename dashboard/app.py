import streamlit as st
import pandas as pd
import requests
import json
import os

st.set_page_config(page_title="Neuro-Wall SOC Panel", layout="wide")
st.title("🛡️ Neuro-Wall Fusion: Real-Time Cyber Threat Panel")

backend_url = st.sidebar.text_input("Backend API Link", value="http://127.0.0.1:8000")

st.subheader("📊 System Logs Datasets")

if os.path.exists("data/cyber_telemetry.json") and os.path.exists("data/transactions.json"):
    with open("data/cyber_telemetry.json") as f:
        tel_data = json.load(f)
    with open("data/transactions.json") as f:
        tx_data = json.load(f)
        
    col1, col2 = st.columns(2)
    with col1:
        st.write("🛰️ Telemetry Logs Pipeline", pd.DataFrame(tel_data))
    with col2:
        st.write("💳 Transaction Records Stream", pd.DataFrame(tx_data))
        
    if st.sidebar.button("Trigger Live Attack Simulation"):
        st.sidebar.info("Injecting structural threat matrix...")
        
        # Target the explicit attack vector entry we generated
        payload = {"time_delta": 120.0, "amount": 95000.0, "is_vpn": True}
        
        try:
            res = requests.post(f"{backend_url}/api/v1/ingest", json=payload).json()
            if res.get("action") == "BLOCK":
                st.error(f"🚨 Cyber Threat Intercepted! Risk Assessment: {res.get('risk_score')}% - Session Blocked.")
            else:
                st.success("✅ Transaction cleared successfully.")
        except Exception as e:
            st.warning("Could not reach backend. Verify API server status.")
else:
    st.info("Missing dataset matrices. Run data/generate_mock_data.py to configure paths.")
