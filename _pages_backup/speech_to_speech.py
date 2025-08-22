
# import base64
# import os
# import tempfile
# from datetime import datetime
# from io import BytesIO
# import speech_recognition as sr
# from googletrans import Translator
# from gtts import gTTS
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# import streamlit as st

# from utils.firebase_config import firestore_db as db
# from firebase_admin import firestore

# # === Optional Whisper Support ===
# import whisper

# # === Futuristic UI Styles ===
# st.markdown("""
#     <style>
#     .block-container {
#         background-color: #0f1117;
#         color: #ffffff;
#     }
#     .stButton>button {
#         background-color: #2e8b57;
#         color: white;
#     }
#     </style>
# """, unsafe_allow_html=True)

# translator = Translator()
# model = whisper.load_model("base")

# supported_languages = {
#     "af": "Afrikaans", "sq": "Albanian", "am": "Amharic", "ar": "Arabic", "hy": "Armenian",
#     "az": "Azerbaijani", "eu": "Basque", "be": "Belarusian", "bn": "Bengali", "bs": "Bosnian",
#     "bg": "Bulgarian", "ca": "Catalan", "ceb": "Cebuano", "ny": "Chichewa", "zh-cn": "Chinese (Simplified)",
#     "zh-tw": "Chinese (Traditional)", "co": "Corsican", "hr": "Croatian", "cs": "Czech", "da": "Danish",
#     "nl": "Dutch", "en": "English", "eo": "Esperanto", "et": "Estonian", "tl": "Filipino",
#     "fi": "Finnish", "fr": "French", "fy": "Frisian", "gl": "Galician", "ka": "Georgian",
#     "de": "German", "el": "Greek", "gu": "Gujarati", "ht": "Haitian Creole", "ha": "Hausa",
#     "haw": "Hawaiian", "iw": "Hebrew", "hi": "Hindi", "hmn": "Hmong", "hu": "Hungarian",
#     "is": "Icelandic", "ig": "Igbo", "id": "Indonesian", "ga": "Irish", "it": "Italian",
#     "ja": "Japanese", "jw": "Javanese", "kn": "Kannada", "kk": "Kazakh", "km": "Khmer",
#     "ko": "Korean", "ku": "Kurdish (Kurmanji)", "ky": "Kyrgyz", "lo": "Lao", "la": "Latin",
#     "lv": "Latvian", "lt": "Lithuanian", "lb": "Luxembourgish", "mk": "Macedonian", "mg": "Malagasy",
#     "ms": "Malay", "ml": "Malayalam", "mt": "Maltese", "mi": "Maori", "mr": "Marathi",
#     "mn": "Mongolian", "my": "Myanmar (Burmese)", "ne": "Nepali", "no": "Norwegian", "ps": "Pashto",
#     "fa": "Persian", "pl": "Polish", "pt": "Portuguese", "pa": "Punjabi", "ro": "Romanian",
#     "ru": "Russian", "sm": "Samoan", "gd": "Scots Gaelic", "sr": "Serbian", "st": "Sesotho",
#     "sn": "Shona", "sd": "Sindhi", "si": "Sinhala", "sk": "Slovak", "sl": "Slovenian",
#     "so": "Somali", "es": "Spanish", "su": "Sundanese", "sw": "Swahili", "sv": "Swedish",
#     "tg": "Tajik", "ta": "Tamil", "te": "Telugu", "th": "Thai", "tr": "Turkish",
#     "uk": "Ukrainian", "ur": "Urdu", "uz": "Uzbek", "vi": "Vietnamese", "cy": "Welsh",
#     "xh": "Xhosa", "yi": "Yiddish", "yo": "Yoruba", "zu": "Zulu"
# }


# def recognize_speech_from_mic():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.info("🎙️ Listening... Please speak now.")
#         audio = r.listen(source)
#     try:
#         st.success("✅ Speech captured.")
#         return r.recognize_google(audio)
#     except sr.UnknownValueError:
#         st.warning("⚠️ Could not understand the audio.")
#     except sr.RequestError:
#         st.error("❌ API unavailable.")
#     return None

# def whisper_transcribe_audio(file_path):
#     result = model.transcribe(file_path)
#     return result['text']

# def translate_text(text, dest_lang):
#     try:
#         result = translator.translate(text, dest=dest_lang)
#         return result.text
#     except:
#         return ""

# def text_to_speech(text, lang):
#     try:
#         tts = gTTS(text=text, lang=lang)
#         tmp_path = tempfile.mktemp(suffix=".mp3")
#         tts.save(tmp_path)
#         return tmp_path
#     except:
#         return ""

# def save_to_firestore(uid, original, translated, lang):
#     db.collection("speech_to_speech_history").add({
#         "uid": uid,
#         "original_text": original,
#         "translated_text": translated,
#         "language": lang,
#         "timestamp": datetime.utcnow()
#     })

# def view_history(uid):
#     st.subheader("📜 Translation History")

#     keyword = st.text_input("🔍 Search keyword (original or translated text)")
#     lang_filter = st.selectbox("🌐 Filter by Language", ["All"] + list(supported_languages.values()))
#     date_range = st.date_input("📅 Filter by Date Range", [])

#     query = db.collection("speech_to_speech_history").where("uid", "==", uid)
#     docs = query.order_by("timestamp", direction=firestore.Query.DESCENDING).stream()

#     export_entries = []

#     for doc in docs:
#         data = doc.to_dict()
#         match_keyword = (
#             keyword.lower() in data["original_text"].lower() or
#             keyword.lower() in data["translated_text"].lower()
#         ) if keyword else True

#         match_lang = (lang_filter == "All" or data["language"] == lang_filter)

#         match_date = True
#         if len(date_range) == 2:
#             start, end = date_range
#             match_date = start <= data["timestamp"].date() <= end

#         if match_keyword and match_lang and match_date:
#             export_entries.append(data)

#             st.markdown(f"**🕒 {data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}**")
#             st.markdown(f"- 🗣️ Original: `{data['original_text']}`")
#             st.markdown(f"- 🌐 Translated: `{data['translated_text']}`")
#             st.markdown(f"- 🏳️ Language: `{data['language']}`")

#             if st.button(f"🗑️ Delete", key=doc.id):
#                 db.collection("speech_to_speech_history").document(doc.id).delete()
#                 st.success("🗑️ Deleted.")
#                 st.rerun()

#             st.markdown("---")

#     if export_entries:
#         export_format = st.radio("📤 Export Format", ["TXT", "PDF"], horizontal=True)
#         if st.button("📁 Export History"):
#             if export_format == "TXT":
#                 txt_content = ""
#                 for e in export_entries:
#                     txt_content += f"{e['timestamp']} | {e['language']}\nOriginal: {e['original_text']}\nTranslated: {e['translated_text']}\n\n"
#                 st.download_button("⬇️ Download TXT", txt_content, file_name="speech_translation_history.txt")

#             elif export_format == "PDF":
#                 buffer = BytesIO()
#                 p = canvas.Canvas(buffer, pagesize=letter)
#                 width, height = letter
#                 y = height - 40
#                 for e in export_entries:
#                     p.drawString(40, y, f"{e['timestamp']} | {e['language']}")
#                     y -= 20
#                     p.drawString(60, y, f"Original: {e['original_text']}")
#                     y -= 20
#                     p.drawString(60, y, f"Translated: {e['translated_text']}")
#                     y -= 30
#                     if y < 100:
#                         p.showPage()
#                         y = height - 40
#                 p.save()
#                 buffer.seek(0)
#                 st.download_button("⬇️ Download PDF", buffer, file_name="speech_translation_history.pdf")
#     else:
#         st.info("No matching entries found.")

# def speech_to_speech(uid):
#     st.header("🗣️ Real-Time Speech Translator")

#     mode = st.radio("Choose Mode", ["🎙️ Single Translation", "👥 Turn-Based Conversation", "📜 View History", "🔙 Back to Dashboard"])
#     auto_detect = st.toggle("🌍 Auto-Detect Spoken Language", value=False)
#     target_lang = st.selectbox("🔁 Select Target Translation Language", 
#                                 list(supported_languages.keys()),
#                                 format_func=lambda x: supported_languages[x])


# def handle_translation(audio_path, speaker_label):
#     with st.spinner("🔊 Processing..."):
#         try:
#             # Step 1: Transcribe the audio
#             if auto_detect:
#                 text = whisper_transcribe_audio(audio_path)
#             else:
#                 recognizer = sr.Recognizer()
#                 with sr.AudioFile(audio_path) as source:
#                     audio_data = recognizer.record(source)
#                     text = recognizer.recognize_google(audio_data)

#             # Display original text
#             st.markdown(
#                 f"<div style='padding:10px;border-radius:10px;background:#333;color:white;margin:5px 0;'>"
#                 f"<b>{speaker_label}:</b> {text}</div>", unsafe_allow_html=True
#             )

#             # Step 2: Translate text
#             translated = translate_text(text, target_lang)
#             if translated:
#                 save_to_firestore(uid, text, translated, target_lang)

#                 # Display translated text
#                 st.markdown(
#                     f"<div style='padding:10px;border-radius:10px;background:#4caf50;color:#fff;'>"
#                     f"<b>Translated:</b> {translated}</div>", unsafe_allow_html=True
#                 )

#                 # Step 3: Convert translation to speech
#                 audio_output_path = text_to_speech(translated, target_lang)
#                 if audio_output_path:
#                     with open(audio_output_path, "rb") as audio_file:
#                         audio_bytes = audio_file.read()
#                         b64_audio = base64.b64encode(audio_bytes).decode()

#                     audio_html = f"""
#                     <audio autoplay controls>
#                         <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
#                         Your browser does not support the audio element.
#                     </audio>
#                     """
#                     st.markdown(audio_html, unsafe_allow_html=True)

#                     # Offer download button
#                     st.download_button("⬇️ Download Audio", audio_bytes, file_name="translated_audio.mp3")

#         except Exception as e:
#             st.error(f"⚠️ Could not process the audio: {e}")
#     if mode == "🎙️ Single Translation":
#         input_mode = st.radio("Input Method", ["🎤 Speak Now", "📁 Upload Audio File"])
#         if input_mode == "🎤 Speak Now" and st.button("🎧 Start Recording"):
#             recognized_text = recognize_speech_from_mic()
#             if recognized_text:
#                 st.write(f"🗣️ You said: `{recognized_text}`")
#                 translated = translate_text(recognized_text, target_lang)
#                 if translated:
#                     st.success(f"🌐 Translation: `{translated}`")
#                     save_to_firestore(uid, recognized_text, translated, target_lang)
#                     audio_path = text_to_speech(translated, target_lang)
#                     if audio_path:
#                         st.audio(audio_path)
#                         with open(audio_path, "rb") as audio_file:
#                             st.download_button("⬇️ Download Audio", audio_file, file_name="translated_audio.mp3")

#         elif input_mode == "📁 Upload Audio File":
#             uploaded = st.file_uploader("Upload audio (MP3/WAV)", type=["mp3", "wav"])
#             if uploaded:
#                 with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
#                     f.write(uploaded.read())
#                     temp_path = f.name
#                 handle_translation(temp_path, "User")

#     elif mode == "👥 Turn-Based Conversation":
#         speaker = st.radio("🎙️ Select Speaker", ["👤 Speaker 1", "👥 Speaker 2"])
#         input_mode = st.radio("Input Method", ["🎤 Speak", "📁 Upload"], key="turn_input")

#         if input_mode == "🎤 Speak" and st.button("🎧 Record"):
#             recognized_text = recognize_speech_from_mic()
#             if recognized_text:
#                 st.write(f"🗣️ {speaker}: `{recognized_text}`")
#                 translated = translate_text(recognized_text, target_lang)
#                 if translated:
#                     st.success(f"🌐 Translation: `{translated}`")
#                     save_to_firestore(uid, recognized_text, translated, target_lang)
#                     audio_path = text_to_speech(translated, target_lang)
#                     if audio_path:
#                         st.audio(audio_path)
#                         with open(audio_path, "rb") as audio_file:
#                             st.download_button("⬇️ Download Audio", audio_file, file_name="translated_audio.mp3")

#         elif input_mode == "📁 Upload":
#             uploaded = st.file_uploader("Upload audio (MP3/WAV)", type=["mp3", "wav"], key="turn_upload")
#             if uploaded:
#                 with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
#                     f.write(uploaded.read())
#                     temp_path = f.name
#                 handle_translation(temp_path, speaker)

#     elif mode == "📜 View History":
#         view_history(uid)

#     elif mode == "🔙 Back to Dashboard":
#         st.session_state["current_page"] = "dashboard"
#         st.rerun()

# # ✅ Fix: Define run(uid) to be used in imports
# def run(uid):
#     speech_to_speech(uid) #check 




# speech_to_speech.py

import base64
import os
import tempfile
from datetime import datetime
from io import BytesIO
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import streamlit as st

from utils.firebase_config import firestore_db as db
from firebase_admin import firestore
import whisper

# === Styling ===
st.markdown("""
    <style>
    .block-container {
        background-color: #0f1117;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #2e8b57;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

translator = Translator()
model = whisper.load_model("base")

supported_languages = {
    "en": "English", "hi": "Hindi", "es": "Spanish", "fr": "French", "de": "German",
    "zh-cn": "Chinese (Simplified)", "ja": "Japanese", "ko": "Korean", "ru": "Russian",
    "ar": "Arabic", "pt": "Portuguese", "bn": "Bengali", "it": "Italian", "ta": "Tamil",
    "te": "Telugu", "ur": "Urdu"
}

def recognize_speech_from_mic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening... Please speak now.")
        audio = r.listen(source)
    try:
        st.success("✅ Speech captured.")
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        st.warning("⚠️ Could not understand the audio.")
    except sr.RequestError:
        st.error("❌ API unavailable.")
    return None

def whisper_transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result['text']

def translate_text(text, dest_lang):
    try:
        result = translator.translate(text, dest=dest_lang)
        return result.text
    except:
        return ""

def text_to_speech(text, lang):
    try:
        tts = gTTS(text=text, lang=lang)
        tmp_path = tempfile.mktemp(suffix=".mp3")
        tts.save(tmp_path)
        return tmp_path
    except:
        return ""

def save_to_firestore(uid, original, translated, lang):
    db.collection("speech_to_speech_history").add({
        "uid": uid,
        "original_text": original,
        "translated_text": translated,
        "language": lang,
        "timestamp": datetime.utcnow()
    })

def view_history(uid):
    st.subheader("📜 Translation History")

    keyword = st.text_input("🔍 Search keyword (original or translated text)")
    lang_filter = st.selectbox("🌐 Filter by Language", ["All"] + list(supported_languages.values()))
    date_range = st.date_input("📅 Filter by Date Range", [])

    query = db.collection("speech_to_speech_history").where("uid", "==", uid)
    docs = query.order_by("timestamp", direction=firestore.Query.DESCENDING).stream()

    export_entries = []

    for doc in docs:
        data = doc.to_dict()
        match_keyword = (
            keyword.lower() in data["original_text"].lower() or
            keyword.lower() in data["translated_text"].lower()
        ) if keyword else True

        match_lang = (lang_filter == "All" or data["language"] == lang_filter)

        match_date = True
        if len(date_range) == 2:
            start, end = date_range
            match_date = start <= data["timestamp"].date() <= end

        if match_keyword and match_lang and match_date:
            export_entries.append(data)

            st.markdown(f"**🕒 {data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}**")
            st.markdown(f"- 🗣️ Original: `{data['original_text']}`")
            st.markdown(f"- 🌐 Translated: `{data['translated_text']}`")
            st.markdown(f"- 🏳️ Language: `{data['language']}`")

            if st.button(f"🗑️ Delete", key=doc.id):
                db.collection("speech_to_speech_history").document(doc.id).delete()
                st.success("🗑️ Deleted.")
                st.rerun()

            st.markdown("---")

    if export_entries:
        export_format = st.radio("📤 Export Format", ["TXT", "PDF"], horizontal=True)
        if st.button("📁 Export History"):
            if export_format == "TXT":
                txt_content = ""
                for e in export_entries:
                    txt_content += f"{e['timestamp']} | {e['language']}\nOriginal: {e['original_text']}\nTranslated: {e['translated_text']}\n\n"
                st.download_button("⬇️ Download TXT", txt_content, file_name="speech_translation_history.txt")

            elif export_format == "PDF":
                buffer = BytesIO()
                p = canvas.Canvas(buffer, pagesize=letter)
                width, height = letter
                y = height - 40
                for e in export_entries:
                    p.drawString(40, y, f"{e['timestamp']} | {e['language']}")
                    y -= 20
                    p.drawString(60, y, f"Original: {e['original_text']}")
                    y -= 20
                    p.drawString(60, y, f"Translated: {e['translated_text']}")
                    y -= 30
                    if y < 100:
                        p.showPage()
                        y = height - 40
                p.save()
                buffer.seek(0)
                st.download_button("⬇️ Download PDF", buffer, file_name="speech_translation_history.pdf")
    else:
        st.info("No matching entries found.")

def handle_translation(audio_path, speaker_label, uid, target_lang, auto_detect):
    with st.spinner("🔊 Processing..."):
        try:
            text = whisper_transcribe_audio(audio_path) if auto_detect else recognize_speech_from_file(audio_path)
            st.markdown(f"**{speaker_label}**: {text}")
            translated = translate_text(text, target_lang)

            if translated:
                st.success(f"🌐 Translation: `{translated}`")
                save_to_firestore(uid, text, translated, target_lang)

                audio_path = text_to_speech(translated, target_lang)
                if audio_path:
                    with open(audio_path, "rb") as audio_file:
                        audio_bytes = audio_file.read()
                        st.audio(audio_path)
                        st.download_button("⬇️ Download Audio", audio_bytes, file_name="translated_audio.mp3")
        except Exception as e:
            st.error(f"❌ Error: {e}")

def recognize_speech_from_file(path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = recognizer.record(source)
        return recognizer.recognize_google(audio)

def speech_to_speech(uid):
    st.header("🗣️ Real-Time Speech Translator")
    mode = st.radio("Choose Mode", ["🎙️ Single Translation", "👥 Turn-Based Conversation", "📜 View History", "🔙 Back to Dashboard"])
    auto_detect = st.toggle("🌍 Auto-Detect Language", value=False)
    target_lang = st.selectbox("🌐 Target Language", list(supported_languages.keys()), format_func=lambda x: supported_languages[x])

    if mode == "🎙️ Single Translation":
        input_mode = st.radio("Input", ["🎤 Speak", "📁 Upload Audio"])
        if input_mode == "🎤 Speak" and st.button("🎧 Record"):
            text = recognize_speech_from_mic()
            if text:
                translated = translate_text(text, target_lang)
                st.success(f"🌐 Translated: {translated}")
                save_to_firestore(uid, text, translated, target_lang)
                path = text_to_speech(translated, target_lang)
                if path:
                    st.audio(path)
                    with open(path, "rb") as f:
                        st.download_button("⬇️ Download Audio", f, file_name="translated.mp3")

        elif input_mode == "📁 Upload Audio":
            uploaded = st.file_uploader("Upload audio file (mp3/wav)", type=["mp3", "wav"])
            if uploaded:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    f.write(uploaded.read())
                    handle_translation(f.name, "User", uid, target_lang, auto_detect)

    elif mode == "👥 Turn-Based Conversation":
        speaker = st.radio("Speaker", ["👤 Speaker 1", "👥 Speaker 2"])
        input_mode = st.radio("Input", ["🎤 Speak", "📁 Upload"])
        if input_mode == "🎤 Speak" and st.button("🎧 Record"):
            text = recognize_speech_from_mic()
            if text:
                translated = translate_text(text, target_lang)
                st.success(f"🌐 Translated: {translated}")
                save_to_firestore(uid, text, translated, target_lang)
                path = text_to_speech(translated, target_lang)
                if path:
                    st.audio(path)
                    with open(path, "rb") as f:
                        st.download_button("⬇️ Download Audio", f, file_name="translated.mp3")
        elif input_mode == "📁 Upload":
            uploaded = st.file_uploader("Upload audio", type=["mp3", "wav"])
            if uploaded:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    f.write(uploaded.read())
                    handle_translation(f.name, speaker, uid, target_lang, auto_detect)

    elif mode == "📜 View History":
        view_history(uid)

    elif mode == "🔙 Back to Dashboard":
        st.session_state["current_page"] = "dashboard"
        st.rerun()

# Main function to be called in your app
def run(uid):
    speech_to_speech(uid)
