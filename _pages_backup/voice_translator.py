# import streamlit as st
# from utils.audio_utils import text_to_speech_custom, extract_language_code
# from langdetect import detect
# from firebase_admin import firestore
# from utils.firebase_utils import get_firestore_client
# from datetime import datetime


# # Set page config
# st.set_page_config(page_title="Voice Translator", page_icon="🔊")

# st.title("🌐 Online Voice Translator (Microsoft Edge TTS)")



# # Initialize session state
# if "uid" not in st.session_state:
#     st.error("You're not logged in!")
#     st.stop()

# uid = st.session_state.uid
# db = get_firestore_client()

# # Input Section
# st.subheader("✍️ Enter Text")
# text_input = st.text_area("Enter the text to speak:")

# # Auto detect language
# detected_lang = ""
# auto_voice = None
# if text_input.strip():
#     try:
#         detected_lang = detect(text_input)
#         for label, name in voice_options.items():
#             if detected_lang in name:
#                 auto_voice = label
#                 break
#     except Exception:
#         detected_lang = "unknown"

# # Voice and Speed selection
# st.subheader("🔊 Voice & Speed Settings")
# voice_display = st.selectbox("🗣️ Choose Voice:", list(voice_options.keys()), index=list(voice_options.keys()).index(auto_voice) if auto_voice else 0)
# voice_name = voice_options[voice_display]
# speed = st.selectbox("⚡ Choose Speed:", ["slow", "normal", "fast"], index=1)

# # Generate and Play
# if st.button("🎧 Generate Speech"):
#     if text_input.strip():
#         audio_path = text_to_speech_custom(text_input, voice_name, speed)
#         st.audio(audio_path)
#         st.download_button("⬇️ Download Audio", open(audio_path, "rb"), file_name="voice.mp3", mime="audio/mpeg")

#         # Save history to Firestore
#         db.collection("voice_history").add({
#             "uid": uid,
#             "text": text_input,
#             "voice": voice_name,
#             "language": extract_language_code(voice_name),
#             "timestamp": datetime.utcnow()
#         })
#     else:
#         st.warning("Please enter some text.")

# # Back to Dashboard
# if st.button("⬅️ Back to Dashboard"):
#     st.switch_page("dashboard.py")


import streamlit as st
from utils.audio_utils import text_to_speech_custom, extract_language_code
from langdetect import detect
from firebase_admin import firestore
from utils.firebase_utils import db
from datetime import datetime

voice_options = {
    # English (US)
    "English (US) - Aria (Female)": "en-US-AriaNeural",
    "English (US) - Guy (Male)": "en-US-GuyNeural",
    "English (US) - Jenny (Female)": "en-US-JennyNeural",

    # English (UK)
    "English (UK) - Sonia (Female)": "en-GB-SoniaNeural",
    "English (UK) - Ryan (Male)": "en-GB-RyanNeural",

    # Hindi
    "Hindi - Swara (Female)": "hi-IN-SwaraNeural",
    "Hindi - Madhur (Male)": "hi-IN-MadhurNeural",

    # Spanish (Spain & Mexico)
    "Spanish (ES) - Elvira (Female)": "es-ES-ElviraNeural",
    "Spanish (ES) - Alvaro (Male)": "es-ES-AlvaroNeural",
    "Spanish (MX) - Dalia (Female)": "es-MX-DaliaNeural",
    "Spanish (MX) - Jorge (Male)": "es-MX-JorgeNeural",

    # French
    "French - Denise (Female)": "fr-FR-DeniseNeural",
    "French - Henri (Male)": "fr-FR-HenriNeural",

    # German
    "German - Conrad (Male)": "de-DE-ConradNeural",
    "German - Katja (Female)": "de-DE-KatjaNeural",

    # Arabic
    "Arabic - Hamed (Male)": "ar-EG-HamedNeural",
    "Arabic - Salma (Female)": "ar-EG-SalmaNeural",

    # Chinese
    "Chinese - Xiaoxiao (Female)": "zh-CN-XiaoxiaoNeural",
    "Chinese - Yunyang (Male)": "zh-CN-YunyangNeural",

    # Japanese
    "Japanese - Nanami (Female)": "ja-JP-NanamiNeural",
    "Japanese - Keita (Male)": "ja-JP-KeitaNeural",

    # Korean
    "Korean - SunHi (Female)": "ko-KR-SunHiNeural",
    "Korean - InJoon (Male)": "ko-KR-InJoonNeural",

    # Russian
    "Russian - Svetlana (Female)": "ru-RU-SvetlanaNeural",
    "Russian - Dmitry (Male)": "ru-RU-DmitryNeural",

    # Italian
    "Italian - Isabella (Female)": "it-IT-IsabellaNeural",
    "Italian - Diego (Male)": "it-IT-DiegoNeural",

    # Portuguese (Brazil)
    "Portuguese (BR) - Francisca (Female)": "pt-BR-FranciscaNeural",
    "Portuguese (BR) - Antonio (Male)": "pt-BR-AntonioNeural",
}

def run(uid):
    st.session_state.uid = uid
    # all your Streamlit logic goes here

    st.set_page_config(page_title="Voice Translator", page_icon="🔊")
    st.title("🌐 Online Voice Translator (Microsoft Edge TTS)")

    if not uid:
        st.error("You're not logged in!")
        return

    # db = get_firestore_client()

    # Input Section
    st.subheader("✍️ Enter Text")
    text_input = st.text_area("Enter the text to speak:")

    # Auto detect language
    detected_lang = ""
    auto_voice = None
    if text_input.strip():
        try:
            detected_lang = detect(text_input)
            for label, name in voice_options.items():
                if detected_lang in name:
                    auto_voice = label
                    break
        except Exception:
            detected_lang = "unknown"

    # Voice and Speed selection
    st.subheader("🔊 Voice & Speed Settings")
    voice_display = st.selectbox("🗣️ Choose Voice:", list(voice_options.keys()), index=list(voice_options.keys()).index(auto_voice) if auto_voice else 0)
    voice_name = voice_options[voice_display]
    speed = st.selectbox("⚡ Choose Speed:", ["slow", "normal", "fast"], index=1)

    # Generate and Play
    if st.button("🎧 Generate Speech"):
        if text_input.strip():
            audio_path = text_to_speech_custom(text_input, voice_name, speed)
            st.audio(audio_path)
            st.download_button("⬇️ Download Audio", open(audio_path, "rb"), file_name="voice.mp3", mime="audio/mpeg")

            # ✅ Save history to Firestore
            db.collection("voice_history").add({
                "uid": uid,
                "text": text_input,
                "voice": voice_name,
                "language": extract_language_code(voice_name),
                "timestamp": datetime.utcnow()
            })
        else:
            st.warning("Please enter some text.")

    # Back to Dashboard
    if st.button("⬅️ Back to Dashboard"):
        st.switch_page("dashboard.py")
