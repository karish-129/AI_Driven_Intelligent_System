import streamlit as st
import pandas as pd
import requests
import random
import time
import json

st.set_page_config(
    page_title="AI_Driven_Intelligent_System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session states
if "telemetry_logs" not in st.session_state:
    st.session_state.telemetry_logs = []
    # Seed initial mock data lines
    for i in range(8):
        st.session_state.telemetry_logs.append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - i*60)),
            "customer_id": f"CUST_{random.randint(1000, 9999)}",
            "amount": round(random.uniform(500.0, 75000.0), 2),
            "time_delta": round(random.uniform(10.0, 3000.0), 2),
            "is_vpn": random.choice([True, False])
        })

if "risk_score" not in st.session_state:
    st.session_state.risk_score = 0.0
if "console_logs" not in st.session_state:
    st.session_state.console_logs = ["[SYSTEM INITIALIZED]: AI_Driven_Intelligent_System Active."]

st.sidebar.header("🛡️ Network Target Control")
backend_url = st.sidebar.text_input("Backend API Link Target", value="http://127.0.0.1:8080")

st.title("🛡️ AI_Driven_Intelligent_System: Real-Time Cyber Threat Panel")
st.write("---")

# Layout the grids
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📡 Live Inbound Telemetry Stream")
    df = pd.DataFrame(st.session_state.telemetry_logs)
    st.dataframe(df[['timestamp', 'customer_id', 'amount', 'time_delta', 'is_vpn']], use_container_width=True)

with col2:
    st.subheader("🚨 Security Inference Core Status")
    score = st.session_state.risk_score
    if score > 75.0:
        st.error(f"⚠️ HIGH THREAT CRITICAL BOUNDARY ACCESSED\n\nInference Risk Score: {score}%")
    elif score > 30.0:
        st.warning(f"⚡ SUSPICIOUS ACTIVITY VECTOR INFERRED\n\nRisk Score: {score}%")
    else:
        st.success(f"✅ System Operational Baseline Secure\n\nLast Vector Evaluation: {score}%")

st.write("---")
st.subheader("🧪 Manual Security Vectors & Attack Simulation Core")

with st.form("simulation_handler"):
    c1, c2, c3 = st.columns(3)
    with c1:
        sim_amount = st.number_input("Transaction Volume ($)", min_value=1.0, max_value=500000.0, value=85000.0)
    with c2:
        sim_delta = st.number_input("Velocity Delta Check (Seconds)", min_value=0.1, max_value=86400.0, value=5.0)
    with c3:
        sim_vpn = st.selectbox("Proxy Network Route Flag (VPN)", options=[True, False], index=0)
        
    submit = st.form_submit_button("🚀 Dispatch Simulation Vector to Ingestion Core")

if submit:
    payload = {"amount": sim_amount, "time_delta": sim_delta, "is_vpn": sim_vpn}
    
    new_vector = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "customer_id": f"SIM_CUST_{random.randint(10, 99)}",
        "amount": sim_amount,
        "time_delta": sim_delta,
        "is_vpn": sim_vpn
    }
    st.session_state.telemetry_logs.insert(0, new_vector)
    if len(st.session_state.telemetry_logs) > 10:
        st.session_state.telemetry_logs.pop()
        
    try:
        response = requests.post(f"{backend_url}/api/v1/ingest", json=payload, timeout=4)
        if response.status_code == 200:
            result_data = response.json()
            st.session_state.risk_score = result_data.get("risk_score", 0.0)
            
            ts = time.strftime("%H:%M:%S")
            st.session_state.console_logs.insert(0, f"[{ts} INGEST]: Inbound payload evaluation requested.")
            st.session_state.console_logs.insert(0, f"[{ts} RESPONSE]: Received from core -> {json.dumps(result_data)}")
            if st.session_state.risk_score > 75.0:
                st.session_state.console_logs.insert(0, f"[{ts} SYSTEM ALERT]: 🚨 Automated firewall dropped packet. Risk is {st.session_state.risk_score}%")
            
            st.success("🤖 Analysis validation returned successfully!")
            st.rerun()
        else:
            st.error(f"❌ Core Error Response Code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error(f"🔌 Failed to communicate with backend target at {backend_url}.")

# --- 📟 HIGH-VISIBILITY UI TERMINAL LOG COMPONENT ---
st.write("---")
st.subheader("📟 System Threat Core Log Matrix")
log_box_content = "\n".join(st.session_state.console_logs)
st.text_area("Live Output Telemetry", value=log_box_content, height=180, disabled=True)
