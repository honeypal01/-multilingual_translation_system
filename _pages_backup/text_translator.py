# import streamlit as st
# from utils.styles_utils import load_custom_css

# # Call the function with the file path
# # load_custom_css("assets/styles/styles.css")
 
# from utils.translator_utils import (
#     detect_language,
#     get_language_code,
#     translate_text,
#     text_to_speech,
#     get_supported_languages,
# )


# # Reverse lookup: language code to language name for displaying detected language nicely
# LANGUAGE_CODES = {
#     "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar", "Armenian": "hy",
#     "Azerbaijani": "az", "Basque": "eu", "Bengali": "bn", "Bosnian": "bs", "Bulgarian": "bg",
#     "Catalan": "ca", "Chinese (Simplified)": "zh-cn", "Chinese (Traditional)": "zh-tw",
#     "Croatian": "hr", "Czech": "cs", "Danish": "da", "Dutch": "nl", "English": "en",
#     "Esperanto": "eo", "Estonian": "et", "Filipino": "tl", "Finnish": "fi", "French": "fr",
#     "Galician": "gl", "Georgian": "ka", "German": "de", "Greek": "el", "Gujarati": "gu",
#     "Haitian Creole": "ht", "Hausa": "ha", "Hebrew": "iw", "Hindi": "hi", "Hungarian": "hu",
#     "Icelandic": "is", "Igbo": "ig", "Indonesian": "id", "Irish": "ga", "Italian": "it",
#     "Japanese": "ja", "Javanese": "jw", "Kannada": "kn", "Kazakh": "kk", "Khmer": "km",
#     "Korean": "ko", "Kurdish": "ku", "Kyrgyz": "ky", "Lao": "lo", "Latin": "la",
#     "Latvian": "lv", "Lithuanian": "lt", "Macedonian": "mk", "Malagasy": "mg", "Malay": "ms",
#     "Malayalam": "ml", "Maltese": "mt", "Marathi": "mr", "Mongolian": "mn", "Myanmar (Burmese)": "my",
#     "Nepali": "ne", "Norwegian": "no", "Pashto": "ps", "Persian": "fa", "Polish": "pl",
#     "Portuguese": "pt", "Punjabi": "pa", "Romanian": "ro", "Russian": "ru", "Serbian": "sr",
#     "Sesotho": "st", "Sinhala": "si", "Slovak": "sk", "Slovenian": "sl", "Somali": "so",
#     "Spanish": "es", "Sundanese": "su", "Swahili": "sw", "Swedish": "sv", "Tamil": "ta",
#     "Telugu": "te", "Thai": "th", "Turkish": "tr", "Ukrainian": "uk", "Urdu": "ur",
#     "Uzbek": "uz", "Vietnamese": "vi", "Welsh": "cy", "Xhosa": "xh", "Yoruba": "yo", "Zulu": "zu"
# }
# CODE_TO_LANG = {v: k for k, v in LANGUAGE_CODES.items()}

# def run_text_translator():
#     st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>🌐 INTERACTIVE TEXT TRANSLATOR</h1>", unsafe_allow_html=True)
#     st.markdown("<p style='text-align: center; font-size:18px; color:gray;'>Type or paste your text below. Language detection and translation happen seamlessly!</p>", unsafe_allow_html=True)
#     st.write("---")

#     input_text = st.text_area("📝 Enter Text To Translate", height=180, max_chars=2000)

#     lang_options = get_supported_languages()
#     target_lang = st.selectbox(
#         "🌍 Translate To",
#         sorted(lang_options),
#         index=sorted(lang_options).index("English") if "English" in lang_options else 0
#     )
# def run_text_translator():
#     # Load external CSS styles
#     load_custom_css("assets/styles/styles.css")  # Path to your external CSS file

#     # Styled heading and subheading
#     st.markdown("<h1 class='main-heading'>🌐 SEAMLESS TEXT TRANSLATOR</h1>", unsafe_allow_html=True)
#     st.markdown("<p class='sub-heading'>Type or paste your text below. Language detection and translation happen seamlessly!</p>", unsafe_allow_html=True)
#     st.write("---")

#     # Input area
#     input_text = st.text_area("📝 Enter Text To Translate", height=180, max_chars=2000)

#     # Language selection
#     lang_options = get_supported_languages()
#     target_lang = st.selectbox(
#         "🌍 Translate To",
#         sorted(lang_options),
#         index=sorted(lang_options).index("English") if "English" in lang_options else 0
#     )
#     target_lang_code = get_language_code(target_lang)

#     col1, col2 = st.columns([1,1])
#     with col1:
#         translate_btn = st.button("🔁 Translate", use_container_width=True)
#     with col2:
#         clear_btn = st.button("🧹 Clear Text", use_container_width=True)

#     if clear_btn:
#         st.rerun()

#     if translate_btn:
#         if not input_text.strip():
#             st.warning("⚠️ Please enter some text to translate.")
#             return

#         with st.spinner("Detecting language and translating..."):
#             detected_lang_code = detect_language(input_text)
#             detected_lang_name = CODE_TO_LANG.get(detected_lang_code, detected_lang_code)

#             if detected_lang_code == target_lang_code:
#                 st.info("ℹ️ Source and target languages are the same; no translation needed.")
#                 translated_text = input_text
#             else:
#                 translated_text = translate_text(input_text, detected_lang_code, target_lang_code)

#         st.success("✅ Translation Complete!")

#         # Display detected language with audio button to hear original text pronunciation
#         st.markdown(f"### Detected Language: **{detected_lang_name}**")

#         audio_orig = text_to_speech(input_text, lang=detected_lang_code)
#         if audio_orig:
#             st.audio(audio_orig, format="audio/mp3", start_time=0)

#         st.markdown("### Translated Text:")
#         st.write(translated_text)

#         # Audio for translated text
#         audio_translated = text_to_speech(translated_text, lang=target_lang_code)
#         if audio_translated:
#             st.audio(audio_translated, format="audio/mp3", start_time=0)

#         st.download_button("⬇️ Download Translation", translated_text, file_name="translated_text.txt", mime="text/plain")

# def run():
#     run_text_translator()



# import streamlit as st
# from utils.styles_utils import load_custom_css
# from utils.translator_utils import (
#     detect_language,
#     get_language_code,
#     translate_text,
#     text_to_speech,
#     get_supported_languages,
# )

# LANGUAGE_CODES = {
#     "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar", "Armenian": "hy",
#     "Azerbaijani": "az", "Basque": "eu", "Bengali": "bn", "Bosnian": "bs", "Bulgarian": "bg",
#     "Catalan": "ca", "Chinese (Simplified)": "zh-cn", "Chinese (Traditional)": "zh-tw",
#     "Croatian": "hr", "Czech": "cs", "Danish": "da", "Dutch": "nl", "English": "en",
#     "Esperanto": "eo", "Estonian": "et", "Filipino": "tl", "Finnish": "fi", "French": "fr",
#     "Galician": "gl", "Georgian": "ka", "German": "de", "Greek": "el", "Gujarati": "gu",
#     "Haitian Creole": "ht", "Hausa": "ha", "Hebrew": "iw", "Hindi": "hi", "Hungarian": "hu",
#     "Icelandic": "is", "Igbo": "ig", "Indonesian": "id", "Irish": "ga", "Italian": "it",
#     "Japanese": "ja", "Javanese": "jw", "Kannada": "kn", "Kazakh": "kk", "Khmer": "km",
#     "Korean": "ko", "Kurdish": "ku", "Kyrgyz": "ky", "Lao": "lo", "Latin": "la",
#     "Latvian": "lv", "Lithuanian": "lt", "Macedonian": "mk", "Malagasy": "mg", "Malay": "ms",
#     "Malayalam": "ml", "Maltese": "mt", "Marathi": "mr", "Mongolian": "mn", "Myanmar (Burmese)": "my",
#     "Nepali": "ne", "Norwegian": "no", "Pashto": "ps", "Persian": "fa", "Polish": "pl",
#     "Portuguese": "pt", "Punjabi": "pa", "Romanian": "ro", "Russian": "ru", "Serbian": "sr",
#     "Sesotho": "st", "Sinhala": "si", "Slovak": "sk", "Slovenian": "sl", "Somali": "so",
#     "Spanish": "es", "Sundanese": "su", "Swahili": "sw", "Swedish": "sv", "Tamil": "ta",
#     "Telugu": "te", "Thai": "th", "Turkish": "tr", "Ukrainian": "uk", "Urdu": "ur",
#     "Uzbek": "uz", "Vietnamese": "vi", "Welsh": "cy", "Xhosa": "xh", "Yoruba": "yo", "Zulu": "zu"
# }
# CODE_TO_LANG = {v: k for k, v in LANGUAGE_CODES.items()}


# def run_text_translator():
#     # if st.button("⬅️ Back to Dashboard"):
#     #     st.session_state.page = "dashboard"
#     #     st.rerun()
#     def run_text_translator():
#         st.title("🌐 Text Translator")

#     if st.button("⬅️ Back to Dashboard"):
#         st.session_state.page = "dashboard"
#         st.rerun()

#     st.write("This is the text translator feature.")

#     load_custom_css("assets/styles/styles.css")

#     st.markdown("<h1 class='main-heading'>🌐 SEAMLESS TEXT TRANSLATOR</h1>", unsafe_allow_html=True)
#     st.markdown("<p class='sub-heading'>Type or paste your text below. Language detection and translation happen seamlessly!</p>", unsafe_allow_html=True)
#     st.write("---")

#     input_text = st.text_area("📝 Enter Text To Translate", height=180, max_chars=2000)

#     lang_options = get_supported_languages()
#     target_lang = st.selectbox(
#         "🌍 Translate To",
#         sorted(lang_options),
#         index=sorted(lang_options).index("English") if "English" in lang_options else 0
#     )
#     target_lang_code = get_language_code(target_lang)

#     col1, col2 = st.columns([1, 1])
#     with col1:
#         translate_btn = st.button("🔁 Translate", use_container_width=True)
#     with col2:
#         clear_btn = st.button("🧹 Clear Text", use_container_width=True)

#     if clear_btn:
#         st.rerun()

#     if translate_btn:
#         if not input_text.strip():
#             st.warning("⚠️ Please enter some text to translate.")
#             return

#         with st.spinner("Detecting language and translating..."):
#             detected_lang_code = detect_language(input_text)
#             detected_lang_name = CODE_TO_LANG.get(detected_lang_code, detected_lang_code)

#             if detected_lang_code == target_lang_code:
#                 st.info("ℹ️ Source and target languages are the same; no translation needed.")
#                 translated_text = input_text
#             else:
#                 translated_text = translate_text(input_text, detected_lang_code, target_lang_code)

#         st.success("✅ Translation Complete!")
#         st.markdown(f"### Detected Language: **{detected_lang_name}**")

#         audio_orig = text_to_speech(input_text, lang=detected_lang_code)
#         if audio_orig:
#             st.audio(audio_orig, format="audio/mp3", start_time=0)

#         st.markdown("### Translated Text:")
#         st.write(translated_text)

#         audio_translated = text_to_speech(translated_text, lang=target_lang_code)
#         if audio_translated:
#             st.audio(audio_translated, format="audio/mp3", start_time=0)

#         st.download_button("⬇️ Download Translation", translated_text, file_name="translated_text.txt", mime="text/plain")



# import streamlit as st
# from utils.styles_utils import load_custom_css
# from utils.translator_utils import (
#     detect_language,
#     get_language_code,
#     translate_text,
#     text_to_speech,
#     get_supported_languages,
# )
# from utils.firebase_utils import log_file_download, fetch_user_usage_logs
# from datetime import datetime

# # Language Maps
# LANGUAGE_CODES = {
#     "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar", "Armenian": "hy",
#     "Azerbaijani": "az", "Basque": "eu", "Bengali": "bn", "Bosnian": "bs", "Bulgarian": "bg",
#     "Catalan": "ca", "Chinese (Simplified)": "zh-cn", "Chinese (Traditional)": "zh-tw",
#     "Croatian": "hr", "Czech": "cs", "Danish": "da", "Dutch": "nl", "English": "en",
#     "Esperanto": "eo", "Estonian": "et", "Filipino": "tl", "Finnish": "fi", "French": "fr",
#     "Galician": "gl", "Georgian": "ka", "German": "de", "Greek": "el", "Gujarati": "gu",
#     "Haitian Creole": "ht", "Hausa": "ha", "Hebrew": "iw", "Hindi": "hi", "Hungarian": "hu",
#     "Icelandic": "is", "Igbo": "ig", "Indonesian": "id", "Irish": "ga", "Italian": "it",
#     "Japanese": "ja", "Javanese": "jw", "Kannada": "kn", "Kazakh": "kk", "Khmer": "km",
#     "Korean": "ko", "Kurdish": "ku", "Kyrgyz": "ky", "Lao": "lo", "Latin": "la",
#     "Latvian": "lv", "Lithuanian": "lt", "Macedonian": "mk", "Malagasy": "mg", "Malay": "ms",
#     "Malayalam": "ml", "Maltese": "mt", "Marathi": "mr", "Mongolian": "mn", "Myanmar (Burmese)": "my",
#     "Nepali": "ne", "Norwegian": "no", "Pashto": "ps", "Persian": "fa", "Polish": "pl",
#     "Portuguese": "pt", "Punjabi": "pa", "Romanian": "ro", "Russian": "ru", "Serbian": "sr",
#     "Sesotho": "st", "Sinhala": "si", "Slovak": "sk", "Slovenian": "sl", "Somali": "so",
#     "Spanish": "es", "Sundanese": "su", "Swahili": "sw", "Swedish": "sv", "Tamil": "ta",
#     "Telugu": "te", "Thai": "th", "Turkish": "tr", "Ukrainian": "uk", "Urdu": "ur",
#     "Uzbek": "uz", "Vietnamese": "vi", "Welsh": "cy", "Xhosa": "xh", "Yoruba": "yo", "Zulu": "zu"
# }
# CODE_TO_LANG = {v: k for k, v in LANGUAGE_CODES.items()}

# def run_text_translator():
#     load_custom_css("assets/styles/styles.css")
#     load_custom_css("assets/styles/text_sidebar_tools.css") 

#     with st.sidebar:
#         st.markdown("""
#             <div class="sidebar-nav">
#                 <h3>🔧 Tools</h3>
#                 <a href="/dashboard" target="_self">🏠 Dashboard</a>
#                 <a href="/video_subtitles" target="_self">🎞️ Video Subtitles</a>
#                 <a href="/document_translator" target="_self">📄 Document Translator</a>
#                 <a href="/speech_to_speech" target="_self">🗣️ Speech-to-Speech</a>
#                 <a href="/chat_translator" target="_self">💬 Chat Translator</a>
#                 <a href="/ai_doc_summarizer" target="_self">📑 AI Summarizer</a>
#                 <a href="/voice_assistant" target="_self">🎤 Voice Assistant</a>
#                 <a href="/ui_translator" target="_self">🧭 UI Translator</a>
#                 <a href="/admin_analytics" target="_self">📊 Admin Analytics</a>
#             </div>
#         """, unsafe_allow_html=True)

#     st.markdown("<h1 class='main-heading'>🌐 SEAMLESS TEXT TRANSLATOR</h1>", unsafe_allow_html=True)
#     st.markdown("<p class='sub-heading'>Type or paste your text below. Language detection and translation happen seamlessly!</p>", unsafe_allow_html=True)
#     st.write("---")

#     input_text = st.text_area("📝 Enter Text To Translate", height=180, max_chars=2000)
#     lang_options = get_supported_languages()
#     target_lang = st.selectbox(
#         "🌍 Translate To",
#         sorted(lang_options),
#         index=sorted(lang_options).index("English") if "English" in lang_options else 0
#     )
#     target_lang_code = get_language_code(target_lang)

#     col1, col2 = st.columns([1, 1])
#     with col1:
#         translate_btn = st.button("🔁 Translate", use_container_width=True)
#     with col2:
#         clear_btn = st.button("🧹 Clear Text", use_container_width=True)

#     if clear_btn:
#         st.rerun()

#     if translate_btn:
#         if not input_text.strip():
#             st.warning("⚠️ Please enter some text to translate.")
#             return

#         with st.spinner("Detecting language and translating..."):
#             detected_lang_code = detect_language(input_text)
#             detected_lang_name = CODE_TO_LANG.get(detected_lang_code, detected_lang_code)

#             if detected_lang_code == target_lang_code:
#                 st.info("ℹ️ Source and target languages are the same; no translation needed.")
#                 translated_text = input_text
#             else:
#                 translated_text = translate_text(input_text, detected_lang_code, target_lang_code)

#         st.success("✅ Translation Complete!")
#         st.markdown(f"### Detected Language: **{detected_lang_name}**")

#         audio_orig = text_to_speech(input_text, lang=detected_lang_code)
#         if audio_orig:
#             st.markdown("#### 🎧 Original Text Audio:")
#             st.audio(audio_orig, format="audio/mp3")
#             st.download_button("⬇️ Download Original Audio", audio_orig, file_name="original_audio.mp3", mime="audio/mp3")

#         st.markdown("### Translated Text:")
#         st.write(translated_text)

#         audio_translated = text_to_speech(translated_text, lang=target_lang_code)
#         if audio_translated:
#             st.markdown("#### 🔊 Translated Audio:")
#             st.audio(audio_translated, format="audio/mp3")
#             st.download_button("⬇️ Download Translated Audio", audio_translated, file_name="translated_audio.mp3", mime="audio/mp3")

#         st.download_button("⬇️ Download Translation as Text", translated_text, file_name="translated_text.txt", mime="text/plain")

#         try:
#             log_file_download(
#                 uid=st.session_state.get("uid", "anonymous"),
#                 feature="Text Translator",
#                 details={
#                     "from_lang": detected_lang_code,
#                     "to_lang": target_lang_code,
#                     "text_length": len(input_text),
#                     "timestamp": datetime.now().isoformat()
#                 }
#             )
#         except Exception as e:
#             st.warning(f"⚠️ Could not log usage to Firebase. Reason: {str(e)}")

# if st.button("⬅️ Back to Dashboard"):
#     st.session_state["redirect_to"] = "dashboard.py"
#     st.rerun()
    
#     log_file_download(st.session_state["uid"], "translated_doc.pdf") 
#     st.write("---")
#     with st.expander("📌 View Recent Translation Usage"):
#         try:
#             uid = st.session_state.get("uid", "anonymous")
#             logs = fetch_user_usage_logs(uid, feature="Text Translator")
#             if logs:
#                 for log in logs:
#                     st.markdown(f"- **{log['timestamp']}**: {log['details']['from_lang']} → {log['details']['to_lang']} (Length: {log['details']['text_length']})")
#             else:
#                 st.info("No recent usage logs found.")
#         except Exception as e:
#             st.error(f"Unable to fetch logs: {e}")







# import streamlit as st
# import os
# from datetime import datetime
# from utils.styles_utils import load_custom_css
# from utils.translator_utils import (
#     detect_language,
#     get_language_code,
#     translate_text,
#     text_to_speech,
#     get_supported_languages,
# )
# from utils.firebase_utils import (
#     log_file_download,
#     fetch_user_usage_logs,
#     upload_file_to_storage,
#     log_file_metadata_to_realtime_db,
# )

# # Language Maps
# LANGUAGE_CODES = {
#     "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar", "Armenian": "hy",
#     "Azerbaijani": "az", "Basque": "eu", "Bengali": "bn", "Bosnian": "bs", "Bulgarian": "bg",
#     "Catalan": "ca", "Chinese (Simplified)": "zh-cn", "Chinese (Traditional)": "zh-tw",
#     "Croatian": "hr", "Czech": "cs", "Danish": "da", "Dutch": "nl", "English": "en",
#     "Esperanto": "eo", "Estonian": "et", "Filipino": "tl", "Finnish": "fi", "French": "fr",
#     "Galician": "gl", "Georgian": "ka", "German": "de", "Greek": "el", "Gujarati": "gu",
#     "Haitian Creole": "ht", "Hausa": "ha", "Hebrew": "iw", "Hindi": "hi", "Hungarian": "hu",
#     "Icelandic": "is", "Igbo": "ig", "Indonesian": "id", "Irish": "ga", "Italian": "it",
#     "Japanese": "ja", "Javanese": "jw", "Kannada": "kn", "Kazakh": "kk", "Khmer": "km",
#     "Korean": "ko", "Kurdish": "ku", "Kyrgyz": "ky", "Lao": "lo", "Latin": "la",
#     "Latvian": "lv", "Lithuanian": "lt", "Macedonian": "mk", "Malagasy": "mg", "Malay": "ms",
#     "Malayalam": "ml", "Maltese": "mt", "Marathi": "mr", "Mongolian": "mn", "Myanmar (Burmese)": "my",
#     "Nepali": "ne", "Norwegian": "no", "Pashto": "ps", "Persian": "fa", "Polish": "pl",
#     "Portuguese": "pt", "Punjabi": "pa", "Romanian": "ro", "Russian": "ru", "Serbian": "sr",
#     "Sesotho": "st", "Sinhala": "si", "Slovak": "sk", "Slovenian": "sl", "Somali": "so",
#     "Spanish": "es", "Sundanese": "su", "Swahili": "sw", "Swedish": "sv", "Tamil": "ta",
#     "Telugu": "te", "Thai": "th", "Turkish": "tr", "Ukrainian": "uk", "Urdu": "ur",
#     "Uzbek": "uz", "Vietnamese": "vi", "Welsh": "cy", "Xhosa": "xh", "Yoruba": "yo", "Zulu": "zu"
# }
# CODE_TO_LANG = {v: k for k, v in LANGUAGE_CODES.items()}


# def run_text_translator():
#     load_custom_css("assets/styles/styles.css")
#     load_custom_css("assets/styles/text_sidebar_tools.css")

#     with st.sidebar:
#         st.markdown("""
#             <div class="sidebar-nav">
#                 <h3>🔧 Tools</h3>
#                 <a href="/_pages_backup/dashboard" target="_self">🏠 Dashboard</a>
#                 <a href="/_pages_backup/video_subtitles" target="_self">🎞️ Video Subtitles</a>
#                 <a href="/_pages_backup/document_translator" target="_self">📄 Document Translator</a>
#                 <a href="/_pages_backup/speech_to_speech" target="_self">🗣️ Speech-to-Speech</a>
#                 <a href="/_pages_backup/chat_translator" target="_self">💬 Chat Translator</a>
#                 <a href="/_pages_backup/ai_doc_summarizer" target="_self">📑 AI Summarizer</a>
#                 <a href="/_pages_backup/voice_assistant" target="_self">🎤 Voice Assistant</a>
#                 <a href="/_pages_backup/ui_translator" target="_self">🧭 UI Translator</a>
#                 <a href="/_pages_backup/admin_analytics" target="_self">📊 Admin Analytics</a>
#             </div>
#         """, unsafe_allow_html=True)

#     st.markdown("<h1 class='main-heading'>🌐 SEAMLESS TEXT TRANSLATOR</h1>", unsafe_allow_html=True)
#     st.markdown("<p class='sub-heading'>Type or paste your text below. Language detection and translation happen seamlessly!</p>", unsafe_allow_html=True)
#     st.write("---")

#     input_text = st.text_area("📝 Enter Text To Translate", height=180, max_chars=2000)
#     lang_options = get_supported_languages()
#     target_lang = st.selectbox("🌍 Translate To", sorted(lang_options), index=sorted(lang_options).index("English"))
#     target_lang_code = get_language_code(target_lang)

#     col1, col2 = st.columns([1, 1])
#     with col1:
#         translate_btn = st.button("🔁 Translate", use_container_width=True)
#     with col2:
#         clear_btn = st.button("🧹 Clear Text", use_container_width=True)

#     if clear_btn:
#         st.rerun()

#     if translate_btn:
#         if not input_text.strip():
#             st.warning("⚠️ Please enter some text to translate.")
#             return

#         with st.spinner("Detecting language and translating..."):
#             detected_lang_code = detect_language(input_text)
#             detected_lang_name = CODE_TO_LANG.get(detected_lang_code, detected_lang_code)

#             if detected_lang_code == target_lang_code:
#                 st.info("ℹ️ Source and target languages are the same; no translation needed.")
#                 translated_text = input_text
#             else:
#                 translated_text = translate_text(input_text, detected_lang_code, target_lang_code)

#         st.success("✅ Translation Complete!")
#         st.markdown(f"### Detected Language: **{detected_lang_name}**")

#         # AUDIO 1: ORIGINAL
#         audio_orig = text_to_speech(input_text, lang=detected_lang_code)
#         if audio_orig:
#             st.markdown("#### 🎧 Original Text Audio:")
#             st.audio(audio_orig, format="audio/mp3")
#             st.download_button("⬇️ Download Original Audio", audio_orig, file_name="original_audio.mp3", mime="audio/mp3")

#         # TEXT RESULT
#         st.markdown("### Translated Text:")
#         st.write(translated_text)

#         # AUDIO 2: TRANSLATED
#         audio_translated = text_to_speech(translated_text, lang=target_lang_code)
#         if audio_translated:
#             st.markdown("#### 🔊 Translated Audio:")
#             st.audio(audio_translated, format="audio/mp3")
#             st.download_button("⬇️ Download Translated Audio", audio_translated, file_name="translated_audio.mp3", mime="audio/mp3")

#         # TEXT DOWNLOAD
#         st.download_button("⬇️ Download Translation as Text", translated_text, file_name="translated_text.txt", mime="text/plain")

#         # 🔥 SAVE TO FIREBASE STORAGE
#         uid = st.session_state.get("uid", "anonymous")
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         preview = input_text.strip().replace("\n", " ")[:30].replace(" ", "_")

#         # Save .txt
#         text_path = f"/tmp/{timestamp}_{preview}.txt"
#         with open(text_path, "w", encoding="utf-8") as f:
#             f.write(translated_text)
#         upload_file_to_storage(uid, text_path, f"Text_Translator/{timestamp}_{preview}.txt")
#         log_file_metadata_to_realtime_db(uid, {
#             "filename": f"{timestamp}_{preview}.txt",
#             "feature": "Text Translator",
#             "type": "text",
#             "timestamp": timestamp,
#         })

#         # Save translated audio
#         if audio_translated:
#             audio_path = f"/tmp/{timestamp}_{preview}_translated.mp3"
#             with open(audio_path, "wb") as f:
#                 f.write(audio_translated.getbuffer())
#             upload_file_to_storage(uid, audio_path, f"Text_Translator/{timestamp}_{preview}_translated.mp3")
#             log_file_metadata_to_realtime_db(uid, {
#                 "filename": f"{timestamp}_{preview}_translated.mp3",
#                 "feature": "Text Translator",
#                 "type": "audio",
#                 "timestamp": timestamp,
#             })

#         # ✅ Log Usage
#         log_file_download(uid, "Text Translator", {
#             "from_lang": detected_lang_code,
#             "to_lang": target_lang_code,
#             "text_length": len(input_text),
#             "timestamp": datetime.now().isoformat()
#         })

#     st.write("---")
#     with st.expander("📌 View Recent Translation Usage"):
#         try:
#             uid = st.session_state.get("uid", "anonymous")
#             logs = fetch_user_usage_logs(uid, feature="Text Translator")
#             if logs:
#                 for log in logs:
#                     st.markdown(f"- **{log['timestamp']}**: {log['details']['from_lang']} → {log['details']['to_lang']} (Length: {log['details']['text_length']})")
#             else:
#                 st.info("No recent usage logs found.")
#         except Exception as e:
#             st.error(f"Unable to fetch logs: {e}")





import streamlit as st
import os
from datetime import datetime
from utils.styles_utils import load_custom_css
from tempfile import NamedTemporaryFile
from utils.translator_utils import (
    detect_language,
    get_language_code,
    translate_text,
    text_to_speech,
    get_supported_languages,
)
from utils.firebase_utils import (
    log_file_download,
    fetch_user_usage_logs,
    upload_file_to_storage,
    log_file_metadata_to_realtime_db,
)

LANGUAGE_CODES = {
    "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar", "Armenian": "hy",
    "Azerbaijani": "az", "Basque": "eu", "Bengali": "bn", "Bosnian": "bs", "Bulgarian": "bg",
    "Catalan": "ca", "Chinese (Simplified)": "zh-cn", "Chinese (Traditional)": "zh-tw",
    "Croatian": "hr", "Czech": "cs", "Danish": "da", "Dutch": "nl", "English": "en",
    "Esperanto": "eo", "Estonian": "et", "Filipino": "tl", "Finnish": "fi", "French": "fr",
    "Galician": "gl", "Georgian": "ka", "German": "de", "Greek": "el", "Gujarati": "gu",
    "Haitian Creole": "ht", "Hausa": "ha", "Hebrew": "iw", "Hindi": "hi", "Hungarian": "hu",
    "Icelandic": "is", "Igbo": "ig", "Indonesian": "id", "Irish": "ga", "Italian": "it",
    "Japanese": "ja", "Javanese": "jw", "Kannada": "kn", "Kazakh": "kk", "Khmer": "km",
    "Korean": "ko", "Kurdish": "ku", "Kyrgyz": "ky", "Lao": "lo", "Latin": "la",
    "Latvian": "lv", "Lithuanian": "lt", "Macedonian": "mk", "Malagasy": "mg", "Malay": "ms",
    "Malayalam": "ml", "Maltese": "mt", "Marathi": "mr", "Mongolian": "mn", "Myanmar (Burmese)": "my",
    "Nepali": "ne", "Norwegian": "no", "Pashto": "ps", "Persian": "fa", "Polish": "pl",
    "Portuguese": "pt", "Punjabi": "pa", "Romanian": "ro", "Russian": "ru", "Serbian": "sr",
    "Sesotho": "st", "Sinhala": "si", "Slovak": "sk", "Slovenian": "sl", "Somali": "so",
    "Spanish": "es", "Sundanese": "su", "Swahili": "sw", "Swedish": "sv", "Tamil": "ta",
    "Telugu": "te", "Thai": "th", "Turkish": "tr", "Ukrainian": "uk", "Urdu": "ur",
    "Uzbek": "uz", "Vietnamese": "vi", "Welsh": "cy", "Xhosa": "xh", "Yoruba": "yo", "Zulu": "zu"
}
CODE_TO_LANG = {v: k for k, v in LANGUAGE_CODES.items()}

def run_text_translator():
    from streamlit_extras.switch_page_button import switch_page

    load_custom_css("assets/styles/styles.css")
    load_custom_css("assets/styles/text_sidebar_tools.css")


    st.markdown("<h1 class='main-heading'>🌐 SEAMLESS TEXT TRANSLATOR</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-heading'>Type or paste your text below. Language detection and translation happen seamlessly!</p>", unsafe_allow_html=True)
    st.write("---")

    input_text = st.text_area("📝 Enter Text To Translate", height=180, max_chars=2000)
    lang_options = get_supported_languages()
    target_lang = st.selectbox("🌍 Translate To", sorted(lang_options), index=sorted(lang_options).index("English"))
    target_lang_code = get_language_code(target_lang)

    col1, col2 = st.columns([1, 1])
    with col1:
        translate_btn = st.button("🔁 Translate", use_container_width=True)
    with col2:
        clear_btn = st.button("🧹 Clear Text", use_container_width=True)

    if clear_btn:
        st.rerun()
        return

    if translate_btn:
        if not input_text.strip():
            st.warning("⚠️ Please enter some text to translate.")
            return

        with st.spinner("Detecting language and translating..."):
            detected_lang_code = detect_language(input_text)
            detected_lang_name = CODE_TO_LANG.get(detected_lang_code, detected_lang_code)

            if detected_lang_code == target_lang_code:
                st.info("ℹ️ Source and target languages are the same; no translation needed.")
                translated_text = input_text
            else:
                translated_text = translate_text(input_text, detected_lang_code, target_lang_code)

        st.success("✅ Translation Complete!")
        st.markdown(f"### Detected Language: **{detected_lang_name}**")

        audio_orig = text_to_speech(input_text, lang=detected_lang_code)
        if audio_orig:
            st.markdown("#### 🎙️ Original Text Audio:")
            st.audio(audio_orig, format="audio/mp3")
            st.download_button("⬇️ Download Original Audio", audio_orig, file_name="original_audio.mp3", mime="audio/mp3")

        st.markdown("### Translated Text:")
        st.write(translated_text)

        audio_translated = text_to_speech(translated_text, lang=target_lang_code)
        if audio_translated:
            st.markdown("#### 🔊 Translated Audio:")
            st.audio(audio_translated, format="audio/mp3")
            st.download_button("⬇️ Download Translated Audio", audio_translated, file_name="translated_audio.mp3", mime="audio/mp3")

        st.download_button("⬇️ Download Translation as Text", translated_text, file_name="translated_text.txt", mime="text/plain")

        try:
            uid = st.session_state.get("uid", "anonymous")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            preview = input_text.strip().replace("\n", " ")[:30].replace(" ", "_")

            with NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as temp_txt:
                temp_txt.write(translated_text)
                txt_path = temp_txt.name

            upload_file_to_storage(uid, txt_path, f"Text_Translator/{timestamp}_{preview}.txt")
            log_file_metadata_to_realtime_db(uid, {
                "filename": f"{timestamp}_{preview}.txt",
                "feature": "Text Translator",
                "type": "text",
                "timestamp": timestamp,
            })

            if audio_translated:
                with NamedTemporaryFile(delete=False, suffix=".mp3", mode="wb") as temp_audio:
                    temp_audio.write(audio_translated.getbuffer())
                    audio_path = temp_audio.name

                upload_file_to_storage(uid, audio_path, f"Text_Translator/{timestamp}_{preview}_translated.mp3")
                log_file_metadata_to_realtime_db(uid, {
                    "filename": f"{timestamp}_{preview}_translated.mp3",
                    "feature": "Text Translator",
                    "type": "audio",
                    "timestamp": timestamp,
                })

            log_file_download(uid, "Text Translator", {
                "from_lang": detected_lang_code,
                "to_lang": target_lang_code,
                "text_length": len(input_text),
                "timestamp": datetime.now().isoformat()
            })

        except Exception as e:
            st.error(f"🔥 Error saving or uploading files: {e}")
            
    if st.button("⬅️ Back to Dashboard"):
        st.session_state["current_page"] = "dashboard"
        st.rerun()


    st.write("---")
    with st.expander("📌 View Recent Translation Usage"):
        try:
            uid = st.session_state.get("uid", "anonymous")
            logs = fetch_user_usage_logs(uid, feature="Text Translator")
            if logs:
                logs_sorted = sorted(logs, key=lambda x: x['timestamp'], reverse=True)[:10]
                for log in logs_sorted:
                    st.markdown(f"- **{log['timestamp']}**: {log['details']['from_lang']} → {log['details']['to_lang']} (Length: {log['details']['text_length']})")
            else:
                st.info("No recent usage logs found.")
        except Exception as e:
            st.error(f"Unable to fetch logs: {e}")

      