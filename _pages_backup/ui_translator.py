import streamlit as st
from googletrans import Translator
from streamlit_extras.switch_page_button import switch_page
from gtts import gTTS
import tempfile
import os
import pyperclip
from utils.firebase_ui_logs import (
    store_ui_submission, fetch_ui_history, delete_ui_entry, update_ui_entry
)
from functools import lru_cache
from io import BytesIO
import base64

def run():
    st.markdown("<h1 style='text-align: center;'>🌍 Multilingual UI Translator</h1>", unsafe_allow_html=True)

    # ✅ Define uid INSIDE the run() function
    uid = st.session_state.get("uid", "anonymous")

    # ... rest of the logic using uid ...
    translator = Translator()

    supported_languages = {
        "English 🇬🇧": "en", "Hindi 🇮🇳": "hi", "French 🇫🇷": "fr",
        "Spanish 🇪🇸": "es", "German 🇩🇪": "de", "Chinese 🇨🇳": "zh-cn",
        "Japanese 🇯🇵": "ja", "Arabic 🇸🇦": "ar", "Hebrew 🇮🇱": "he",
        "Urdu 🇵🇰": "ur", "Russian 🇷🇺": "ru", "Portuguese 🇵🇹": "pt",
        "Korean 🇰🇷": "ko", "Italian 🇮🇹": "it", "Turkish 🇹🇷": "tr"
    }

    rtl_languages = {"ar", "he", "ur"}
    selected_lang = st.selectbox("🌐 Choose UI Language", list(supported_languages.keys()))
    lang_code = supported_languages[selected_lang]
    is_rtl = lang_code in rtl_languages

    if is_rtl:
        st.markdown("""
            <style>
                .rtl * { direction: rtl; text-align: right; }
            </style>
        """, unsafe_allow_html=True)
        rtl_class = "rtl"
    else:
        rtl_class = ""

    @lru_cache(maxsize=256)
    def cached_translate(text, dest):
        try:
            return translator.translate(text, dest=dest).text
        except Exception:
            return text

    def t(text):
        return cached_translate(text, lang_code)

    st.markdown(f"<div class='{rtl_class}'>{t('Welcome to the multilingual translation system!')}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='{rtl_class}'>{t('Translate UI content into your preferred language.')}</div>", unsafe_allow_html=True)

    name = st.text_input(t("Enter your name:"), key="ui_name")
    message = st.text_area(t("Write a message:"), key="ui_msg")

    if st.button(t("Submit")) and name.strip() and message.strip():
        store_ui_submission(uid, name.strip(), message.strip(), lang_code)
        st.success(t("Submission saved successfully!"))
        st.rerun()

    st.markdown("---")
    st.subheader(t("📜 Your History"))

    entries = fetch_ui_history(uid)  # ✅ Used inside run() after uid is defined
    if not entries:
        st.info(t("No previous submissions found."))
    else:
        for entry in entries:
            with st.expander(f"📝 {entry['name']} - {entry['timestamp']}"):
                st.markdown(f"<div class='{rtl_class}'>{entry['message']}</div>", unsafe_allow_html=True)

                if st.button(f"🔊 {t('Listen')}", key=f"tts_{entry['id']}"):
                    tts = gTTS(text=entry['message'], lang=lang_code)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                        tts.save(tmp.name)
                        # audio_bytes = open(tmp.name, "rb").read()
                        # st.audio(audio_bytes, format="audio/mp3")
                        with open(tmp.name, "rb") as audio_file:
                          st.audio(audio_file.read(), format="audio/mp3")

                    try:
                        os.remove(tmp.name)
                    except PermissionError:
                        st.warning("Please close the audio before submitting again.")

                st.download_button("📄 " + t("Export"), data=entry['message'], file_name="message.txt", key=f"export_{entry['id']}")
                share_link = f"data:text/plain;base64,{base64.b64encode(entry['message'].encode()).decode()}"
                st.code(share_link, language="")

                new_msg = st.text_area("✏️ " + t("Edit message"), value=entry['message'], key=f"edit_{entry['id']}")
                if st.button("💾 " + t("Update"), key=f"update_{entry['id']}"):
                    update_ui_entry(uid, entry['id'], new_msg)
                    st.success(t("Message updated!"))
                    st.rerun()

                if st.button("❌ " + t("Delete"), key=f"delete_{entry['id']}"):
                    delete_ui_entry(uid, entry['id'])
                    st.warning(t("Message deleted!"))
                    st.rerun()

    st.markdown("---")
    if st.button("🏠 " + t("Back to Dashboard")):
        st.session_state.current_page = "dashboard"
    st.rerun()


# Inject external CSS
def inject_custom_css(file_path="assets/styles/ui_translator_style.css"):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

inject_custom_css()
