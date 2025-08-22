# utils/styles_utils.py
import streamlit as st

def load_custom_css(file_path):
    """Load external CSS styles into Streamlit app."""
    try:
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"⚠️ Could not find the CSS file at: {file_path}")

