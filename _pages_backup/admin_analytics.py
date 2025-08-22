import streamlit as st
import plotly.express as px
import pandas as pd
from utils.firebase_utils import fetch_usage_logs  # You must define this function in firebase_utils

# Only allow admin
if st.session_state.get("role") != "admin":
    st.error("🚫 Access Denied: Admins only.")
    st.stop()

st.set_page_config(page_title="📊 Admin Analytics")
st.title("📊 Admin Analytics Dashboard")

# Fetch real usage logs or fallback to sample
try:
    logs = fetch_usage_logs()
except Exception as e:
    st.warning(f"⚠️ Failed to fetch logs from Firebase: {e}")
    logs = []

# Show sample data if empty
if not logs:
    st.info("No usage data found. Showing sample data.")
    logs = [
        {"module": "Text Translator", "user": "User1"},
        {"module": "Voice Translator", "user": "User2"},
        {"module": "Chat Translator", "user": "User3"},
        {"module": "Text Translator", "user": "User1"},
        {"module": "Image Translator", "user": "User2"},
    ]

df = pd.DataFrame(logs)

# Visualize module usage
if not df.empty:
    module_counts = df['module'].value_counts().reset_index()
    module_counts.columns = ['Module', 'Usage Count']
    fig = px.bar(module_counts, x='Module', y='Usage Count',
                 title="📈 Module Usage Statistics", color='Module')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No analytics to display.")

# Navigation
if st.button("⬅ Back to Dashboard"):
    st.session_state["current_page"] = "dashboard"
    st.rerun()
