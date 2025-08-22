# multilingual_chat.py

import streamlit as st
import uuid
from googletrans import Translator
from firebase_admin import db
from utils.firebase_setup import get_user_id, init_firebase

# Initialize Firebase
init_firebase()

translator = Translator()
chat_ref = db.reference("/chat_messages")

def translate_message(message, target_lang):
    try:
        translated = translator.translate(message, dest=target_lang)
        return translated.text
    except:
        return message

def send_message(user_id, username, message, language):
    if message.strip() == "":
        return
    chat_ref.push({
        "user_id": user_id,
        "username": username,
        "message": message,
        "language": language
    })

def get_all_messages():
    return chat_ref.get() or {}

def multilingual_chat():
    st.title("🌐 Multilingual Real-Time Chat")

    if 'username' not in st.session_state:
        st.warning("🚫 You must be logged in to access the chat.")
        return

    user_id = get_user_id()
    username = st.session_state['username']
    target_lang = st.selectbox("🌍 Choose your preferred language:", ["en", "hi", "fr", "es", "de", "zh-cn", "ja"])

    with st.chat_message("user"):
        st.write(f"🧑 Logged in as **{username}** | Chat language: **{target_lang.upper()}**")

    messages = get_all_messages()
    for key in sorted(messages.keys()):
        msg = messages[key]
        translated_text = translate_message(msg['message'], target_lang)
        with st.chat_message("assistant" if msg['user_id'] != user_id else "user"):
            st.markdown(f"**{msg['username']}**: {translated_text}")

    with st.form("chat_form", clear_on_submit=True):
        message = st.text_input("💬 Type your message:")
        submitted = st.form_submit_button("Send")
        if submitted:
            send_message(user_id, username, message, target_lang)
            st.experimental_rerun()