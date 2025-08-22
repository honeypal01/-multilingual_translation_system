import streamlit as st
from googletrans import Translator
import firebase_admin
from firebase_admin import db
from utils.firebase_setup import init_firebase, get_user_id

# ✅ Initialize Firebase
init_firebase()

# ❌ DO NOT call this here if main.py already calls set_page_config
# st.set_page_config(page_title="Multilingual Chat", layout="wide")

# 🌐 Page title
st.title("🌐 Multilingual Real-Time Chat")

# 🗣️ Supported languages
languages = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh-cn",
    "Arabic": "ar",
    "Japanese": "ja",
    "Russian": "ru",
    "Portuguese": "pt"
}

# 👤 Get user info from session
email = st.session_state.get("email")
if email:
    try:
        user_id = get_user_id(email)
    except Exception as e:
        st.error(f"❌ Could not fetch user ID: {e}")
        st.stop()
else:
    st.error("❌ User not logged in or email missing. Please log in again.")
    st.stop()

username = st.text_input("Enter your display name:", key="username")

# 🌐 Language selection
selected_lang = st.selectbox("Select your language", list(languages.keys()))
lang_code = languages[selected_lang]

# 🔗 Firebase Realtime Database reference
chat_ref = db.reference("chat")

# 🔄 Translator instance
translator = Translator()

# ✉️ Send message form
with st.form("chat_form", clear_on_submit=True):
    user_msg = st.text_input("Your message")
    submitted = st.form_submit_button("Send")

    if submitted and user_msg.strip():
        try:
            translated_text = translator.translate(user_msg, dest="en").text
        except Exception as e:
            st.error(f"❌ Translation failed: {e}")
            translated_text = user_msg

        message_obj = {
            "user_id": user_id,
            "username": username if username else "Guest",
            "message": user_msg,
            "translated": translated_text,
            "lang": lang_code
        }
        chat_ref.push(message_obj)

# 💬 Display chat messages
st.subheader("💬 Chat Messages")
messages = chat_ref.order_by_key().limit_to_last(20).get()

if messages:
    for key, msg in messages.items():
        original = msg.get("message", "")
        sender = msg.get("username", "Unknown")
        try:
            translated = translator.translate(msg.get("translated", ""), dest=lang_code).text
        except Exception:
            translated = msg.get("translated", "")

        st.markdown(f"**{sender}:** {translated}  _(original: {original})_")
else:
    st.info("No messages yet. Start chatting!")
