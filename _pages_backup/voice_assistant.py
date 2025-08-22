import streamlit as st
import requests
from googletrans import Translator
from firebase_admin import firestore
from utils.audio_utils import text_to_speech_custom
from utils.firebase_utils import db
from datetime import datetime
import pandas as pd
import tempfile
import os
import whisper
import sounddevice as sd
import soundfile as sf

# Load Whisper model once
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

whisper_model = load_whisper_model()

# Optional tab title
st.markdown("<title>🧠 Voice Assistant</title>", unsafe_allow_html=True)

def run(uid):
    openrouter_key = st.secrets["openrouter"]["api_key"]
    translator = Translator()

    st.markdown("<h1 style='font-family:Times New Roman;'>🗣️ Multilingual Voice Assistant</h1>", unsafe_allow_html=True)

    # Language and gender selection
    language_options = {
        'en': 'English 🇺🇸', 'hi': 'Hindi 🇮🇳', 'fr': 'French 🇫🇷', 'es': 'Spanish 🇪🇸', 'de': 'German 🇩🇪',
        'zh-cn': 'Chinese 🇨🇳', 'ja': 'Japanese 🇯🇵', 'it': 'Italian 🇮🇹', 'ru': 'Russian 🇷🇺', 'ko': 'Korean 🇰🇷',
        'ar': 'Arabic 🇸🇦', 'pt': 'Portuguese 🇧🇷', 'bn': 'Bengali 🇧🇩', 'pl': 'Polish 🇵🇱', 'tr': 'Turkish 🇹🇷',
        'nl': 'Dutch 🇳🇱', 'sv': 'Swedish 🇸🇪', 'uk': 'Ukrainian 🇺🇦', 'th': 'Thai 🇹🇭', 'ro': 'Romanian 🇷🇴',
        'vi': 'Vietnamese 🇻🇳', 'fa': 'Persian 🇮🇷', 'el': 'Greek 🇬🇷', 'no': 'Norwegian 🇳🇴', 'he': 'Hebrew 🇮🇱',
        'id': 'Indonesian 🇮🇩', 'cs': 'Czech 🇨🇿', 'hu': 'Hungarian 🇭🇺', 'fi': 'Finnish 🇫🇮', 'da': 'Danish 🇩🇰'
    }

    col1, col2 = st.columns(2)
    with col1:
        lang = st.selectbox("🌍 Answer Language", list(language_options.keys()), format_func=lambda x: language_options.get(x, x))
    with col2:
        voice_gender = st.selectbox("🎙️ Voice Gender", ["Female", "Male"])

    st.markdown("### 💬 Ask me anything...")
    user_query = st.text_area("Type your query or use voice below", key="user_query")

    st.markdown("### 🎤 Or record your voice")

    if st.button("🎙️ Record Voice"):
        duration = 10  # seconds
        fs = 16000
        st.info("🎧 Recording... Please speak.")

        try:
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
            sd.wait()

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                wav_path = temp_audio.name
                sf.write(wav_path, recording, fs)

            st.audio(wav_path, format="audio/wav")

            result = whisper_model.transcribe(wav_path)
            user_query = result["text"]
            detected_lang = result["language"]
            st.success(f"🗣️ Detected: {user_query} ({detected_lang.upper()})")
            os.remove(wav_path)
        except Exception as e:
            st.error(f"❌ Error processing audio: {e}")
            return

    # Ask OpenRouter AI if query is available
    if user_query.strip():
        def ask_openai(prompt):
            try:
                headers = {
                    "Authorization": f"Bearer {openrouter_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "mistralai/mistral-7b-instruct",
                    "messages": [
                        {"role": "system", "content": "You are a helpful multilingual voice assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 300
                }
                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"].strip()
            except Exception as e:
                return f"Error: {e}"

        with st.spinner("💡 Thinking..."):
            response = ask_openai(user_query)
            translated = translator.translate(response, dest=lang).text

        st.subheader("💬 AI Response")
        st.markdown(f"<div style='padding:10px; background-color:#222; color:white; border-radius:10px;'>{response}</div>", unsafe_allow_html=True)

        st.subheader(f"🌐 Translated ({language_options.get(lang, lang)})")
        st.success(translated)

        st.subheader("🔊 Voice Output")
        audio_path = text_to_speech_custom(translated, voice_gender, lang, "normal")
        st.audio(audio_path, format="audio/wav")

        # Save to Firestore
        db.collection("voice_assistant_history").add({
            "uid": uid,
            "question": user_query,
            "response": response,
            "translated_response": translated,
            "language": lang,
            "gender": voice_gender,
            "timestamp": datetime.utcnow()
        })

    # Show voice assistant history
    st.subheader("📂 History of Voice Outputs")
    docs = db.collection("voice_assistant_history") \
        .where("uid", "==", uid) \
        .order_by("timestamp", direction=firestore.Query.DESCENDING) \
        .stream()

    history_data = []
    for doc in docs:
        d = doc.to_dict()
        history_data.append({
            "Question": d.get("question", ""),
            "Answer": d.get("translated_response", ""),
            "Language": language_options.get(d.get("language", ""), d.get("language", "")),
            "Time": d.get("timestamp").strftime("%Y-%m-%d %H:%M") if d.get("timestamp") else ""
        })

    if history_data:
        df = pd.DataFrame(history_data)
        st.dataframe(df, use_container_width=True)
        st.download_button("⬇️ Download History (.csv)", data=df.to_csv(index=False), file_name="voice_assistant_history.csv")
    else:
        st.info("No history found.")

    # Back to dashboard button
    st.markdown("""
        <style>
        .back-button {
            background-color: #111;
            color: white;
            padding: 0.5em 1.2em;
            border-radius: 8px;
            text-align: center;
            transition: all 0.3s ease-in-out;
            font-family: 'Times New Roman';
            border: none;
        }
        .back-button:hover {
            background-color: #444;
            transform: scale(1.05);
            cursor: pointer;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("⬅ Back to Dashboard"):
        st.session_state["current_page"] = "dashboard"
        st.rerun()
