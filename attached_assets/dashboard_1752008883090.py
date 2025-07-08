import streamlit as st
import pandas as pd
import numpy as np
import random
import time

st.set_page_config(page_title="📊 Market Risk Monitor", layout="wide")

st.title("🚨 Strategic Market Risk Monitoring System")
st.markdown("### Real-Time Risk Gauge & History")

# Simulated risk score
score = random.randint(0, 100)
risk_level = "LOW"
if score >= 80:
    risk_level = "RED"
elif score >= 60:
    risk_level = "ORANGE"
elif score >= 40:
    risk_level = "YELLOW"

st.metric(label="Risk Score", value=score)
st.markdown(f"**Current Risk Level: {risk_level}**")

# Simulate historical data
def generate_history():
    np.random.seed(42)
    base = random.randint(30, 70)
    noise = np.random.normal(0, 5, 50)
    series = np.clip(base + np.cumsum(noise), 0, 100)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=50)
    return pd.DataFrame({'Date': dates, 'Risk Score': series})

history_df = generate_history()

st.line_chart(history_df.set_index("Date"))

# Optional auto-refresh
refresh = st.checkbox("🔄 Auto-refresh chart every 30s", value=False)
if refresh:
    time.sleep(30)
    st.experimental_rerun()