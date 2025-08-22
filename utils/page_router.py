# utils/page_router.py

import importlib

def load_page(module_name, function_name="run"):
    try:
        module = importlib.import_module(module_name)
        getattr(module, function_name)()
    except Exception as e:
        import streamlit as st
        st.error(f"Failed to load {module_name}: {e}")
