# import streamlit as st
# import pytesseract
# from PIL import Image
# from googletrans import Translator
# from datetime import datetime
# import tempfile
# from firebase_admin import firestore
# from utils.firebase_setup import init_firebase, get_user_id
# import base64

# def run(uid):
#     # st.set_page_config(page_title="Image Translator", page_icon="🖼️")

#     # Initialize translator
#     translator = Translator()

#     # st.title("🖼️ Image Translator with OCR")

#     # Check if user is logged in
#     if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
#         st.warning("Please log in first.")
#         return

#     email = st.session_state["email"]
# # Initialize Firebase
# init_firebase()
# db = firestore.client()

# # Function to store translation
# def save_translation(email, extracted_text, translated_text, source_lang, target_lang):
#     user_id = get_user_id(email)
#     doc_ref = db.collection("image_translations").document()
#     doc_ref.set({
#         "user_id": user_id,
#         "email": email,
#         "extracted_text": extracted_text,
#         "translated_text": translated_text,
#         "source_lang": source_lang,
#         "target_lang": target_lang,
#         "timestamp": firestore.SERVER_TIMESTAMP
#     })

# # Function to view translation history with delete/download buttons
# def view_translation_history(email):
#     st.subheader("📜 Translation History")

#     try:
#         docs = db.collection("image_translations") \
#                  .where("email", "==", email) \
#                  .order_by("timestamp", direction=firestore.Query.DESCENDING) \
#                  .stream()

#         docs_list = list(docs)
#         if not docs_list:
#             st.info("No translation history found.")
#             return

#         for doc in docs_list:
#             data = doc.to_dict()
#             ts = data.get("timestamp")
#             timestamp_str = ts.strftime('%Y-%m-%d %H:%M:%S') if isinstance(ts, datetime) else "Pending..."

#             with st.expander(f"🕒 {timestamp_str} | {data['source_lang']} ➜ {data['target_lang']}"):
#                 st.markdown(f"**📝 Extracted:**\n{data['extracted_text']}")
#                 st.markdown(f"**🌍 Translated:**\n{data['translated_text']}")

#                 col1, col2 = st.columns([1, 1])
#                 with col1:
#                     b64 = base64.b64encode(data['translated_text'].encode()).decode()
#                     href = f'<a href="data:file/txt;base64,{b64}" download="translation.txt">📥 Download</a>'
#                     st.markdown(href, unsafe_allow_html=True)

#                 with col2:
#                     if st.button("🗑️ Delete", key=f"delete_{doc.id}"):
#                         db.collection("image_translations").document(doc.id).delete()
#                         st.success("Deleted!")
#                         st.rerun()

#     except Exception as e:
#         st.error(f"⚠️ Failed to load history: {e}")
#         st.info("If the error mentions an index, click the link and create the suggested Firestore index.")

# # --- MAIN UI ---
# if not st.session_state.get("logged_in"):
#     st.warning("Please log in first.")
#     st.stop()

# email = st.session_state["email"]

# st.markdown("<h2 style='text-align:center;'>🖼️ Image Translator (OCR + Translate)</h2>", unsafe_allow_html=True)

# uploaded_image = st.file_uploader("📤 Upload an image", type=["png", "jpg", "jpeg"])

# lang_options = {
#     "auto": "🌐 Auto-Detect",
#     "eng": "🇺🇸 English",
#     "hin": "🇮🇳 Hindi",
#     "fra": "🇫🇷 French",
#     "deu": "🇩🇪 German",
#     "spa": "🇪🇸 Spanish",
#     "jpn": "🇯🇵 Japanese",
#     "chi_sim": "🇨🇳 Chinese (Simplified)"
# }

# col1, col2 = st.columns(2)
# with col1:
#     source_lang = st.selectbox("🔤 OCR Source Language", options=lang_options.keys(), format_func=lambda x: lang_options[x])
# with col2:
#     target_lang = st.selectbox("🌐 Target Translation Language", ["en", "hi", "fr", "es", "de", "zh-cn", "ja"])

# if uploaded_image:
#     image = Image.open(uploaded_image)
#     st.image(image, caption="📷 Uploaded Image", use_column_width=True)

#     with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
#         image.save(tmp_file.name)
#         try:
#             detected_lang = source_lang
#             if source_lang == "auto":
#                 try:
#                     osd = pytesseract.image_to_osd(Image.open(tmp_file.name), output_type=pytesseract.Output.DICT)
#                     script = osd.get("script", "Latin").lower()
#                     lang_map = {
#                         "latin": "eng",
#                         "devanagari": "hin",
#                         "cyrillic": "rus",
#                         "japanese": "jpn",
#                         "chinese": "chi_sim"
#                     }
#                     detected_lang = lang_map.get(script, "eng")
#                     st.info(f"🔎 Detected OCR Language: `{detected_lang}`")
#                 except Exception as e:
#                     detected_lang = "eng"
#                     st.warning(f"⚠️ Language auto-detection failed, defaulting to English. Error: {e}")

#             extracted_text = pytesseract.image_to_string(Image.open(tmp_file.name), lang=detected_lang)

#             st.subheader("📝 Extracted Text")
#             st.code(extracted_text)

#             if st.button("🌍 Translate"):
#                 translator = Translator()
#                 translated_text = translator.translate(extracted_text, src="auto", dest=target_lang).text

#                 st.subheader("✅ Translated Text")
#                 st.success(translated_text)

#                 save_translation(email, extracted_text, translated_text, detected_lang, target_lang)
#                 st.rerun()

#         except Exception as e:
#             st.error(f"❌ OCR or translation failed: {e}")

# view_translation_history(email)

# # Back to Dashboard
# if st.button("⬅ Back to Dashboard"):
#         st.session_state["current_page"] = "dashboard"
#         st.experimental_rerun()




# import streamlit as st
# import pytesseract
# from PIL import Image
# from googletrans import Translator
# from datetime import datetime
# import tempfile
# from firebase_admin import firestore
# from utils.firebase_setup import init_firebase, get_user_id
# import base64
# import os
# import zipfile
# from io import BytesIO

# # Initialize Firebase
# init_firebase()
# db = firestore.client()

# # Save translation to Firestore
# def save_translation(email, extracted_text, translated_text, source_lang, target_lang):
#     user_id = get_user_id(email)
#     doc_ref = db.collection("image_translations").document()
#     doc_ref.set({
#         "user_id": user_id,
#         "email": email,
#         "extracted_text": extracted_text,
#         "translated_text": translated_text,
#         "source_lang": source_lang,
#         "target_lang": target_lang,
#         "timestamp": firestore.SERVER_TIMESTAMP
#     })

# # View translation history with batch download/delete
# def view_translation_history(email):
#     st.subheader("📜 Translation History")
#     try:
#         docs = db.collection("image_translations") \
#                  .where("email", "==", email) \
#                  .order_by("timestamp", direction=firestore.Query.DESCENDING) \
#                  .stream()

#         docs_list = list(docs)
#         if not docs_list:
#             st.info("No translation history found.")
#             return

#         zip_buffer = BytesIO()
#         txt_files = []
#         delete_ids = []

#         for i, doc in enumerate(docs_list):
#             data = doc.to_dict()
#             ts = data.get("timestamp")
#             timestamp_str = ts.strftime('%Y-%m-%d_%H-%M-%S') if isinstance(ts, datetime) else f"entry_{i+1}"
#             filename = f"translation_{timestamp_str}.txt"
#             file_content = f"Extracted Text:\n{data['extracted_text']}\n\nTranslated Text:\n{data['translated_text']}"
#             txt_files.append((filename, file_content))
#             delete_ids.append(doc.id)

#             with st.expander(f"🕒 {timestamp_str} | {data['source_lang']} ➜ {data['target_lang']}"):
#                 st.markdown(f"**📝 Extracted:**\n{data['extracted_text']}")
#                 st.markdown(f"**🌍 Translated:**\n{data['translated_text']}")

#                 col1, col2 = st.columns(2)
#                 with col1:
#                     b64 = base64.b64encode(file_content.encode()).decode()
#                     href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 Download</a>'
#                     st.markdown(href, unsafe_allow_html=True)
#                 with col2:
#                     if st.button("🗑️ Delete", key=f"delete_{doc.id}"):
#                         db.collection("image_translations").document(doc.id).delete()
#                         st.success("Deleted!")
#                         st.rerun()

#         # Batch ZIP download
#         with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zipf:
#             for filename, content in txt_files:
#                 zipf.writestr(filename, content)
#         zip_buffer.seek(0)
#         b64_zip = base64.b64encode(zip_buffer.read()).decode()
#         href_zip = f'<a href="data:application/zip;base64,{b64_zip}" download="translation_history.zip">📦 Download All as ZIP</a>'

#         st.markdown("---")
#         st.markdown("### 🧰 Batch Actions")
#         st.markdown(href_zip, unsafe_allow_html=True)

#         if st.button("🗑️ Delete All History"):
#             for doc_id in delete_ids:
#                 db.collection("image_translations").document(doc_id).delete()
#             st.success("✅ All history deleted.")
#             st.rerun()

#     except Exception as e:
#         st.error(f"⚠️ Failed to load history: {e}")
#         st.info("If the error mentions an index, click the link and create the suggested Firestore index.")

# # --- MAIN UI ---
# def run():
#      if not st.session_state.get("logged_in"):
#         st.warning("Please log in first.")
#         st.stop()

# email = st.session_state["email"]

# st.markdown("<h2 style='text-align:center;'>🖼️ Image Translator (OCR + Translate)</h2>", unsafe_allow_html=True)

# uploaded_images = st.file_uploader("📤 Upload one or more images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

# lang_options = {
#     "auto": "🌐 Auto-Detect",
#     "eng": "🇺🇸 English",
#     "hin": "🇮🇳 Hindi",
#     "fra": "🇫🇷 French",
#     "deu": "🇩🇪 German",
#     "spa": "🇪🇸 Spanish",
#     "jpn": "🇯🇵 Japanese",
#     "chi_sim": "🇨🇳 Chinese (Simplified)"
# }

# col1, col2 = st.columns(2)
# with col1:
#     source_lang = st.selectbox("🔤 OCR Source Language", options=lang_options.keys(), format_func=lambda x: lang_options[x])
# with col2:
#     target_lang = st.selectbox("🌐 Target Translation Language", ["en", "hi", "fr", "es", "de", "zh-cn", "ja"])

# translator = Translator()

# if uploaded_images:
#     for uploaded_image in uploaded_images:
#         image = Image.open(uploaded_image)
#         st.image(image, caption=f"📷 {uploaded_image.name}", use_container_width=True)

#         with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
#             image.save(tmp_file.name)
#             try:
#                 detected_lang = source_lang
#                 if source_lang == "auto":
#                     try:
#                         osd = pytesseract.image_to_osd(Image.open(tmp_file.name), output_type=pytesseract.Output.DICT)
#                         script = osd.get("script", "Latin").lower()
#                         lang_map = {
#                             "latin": "eng",
#                             "devanagari": "hin",
#                             "cyrillic": "rus",
#                             "japanese": "jpn",
#                             "chinese": "chi_sim"
#                         }
#                         detected_lang = lang_map.get(script, "eng")
#                         st.info(f"🔎 Detected OCR Language: `{detected_lang}`")
#                     except Exception as e:
#                         detected_lang = "eng"
#                         st.warning(f"⚠️ Language auto-detection failed. Defaulting to English. Error: {e}")

#                 # Use OCR Engine Mode 1 for handwritten support
#                 custom_config = r'--oem 1'
#                 extracted_text = pytesseract.image_to_string(Image.open(tmp_file.name), lang=detected_lang, config=custom_config)

#                 st.subheader("📝 Extracted Text")
#                 st.code(extracted_text)

#                 if st.button(f"🌍 Translate {uploaded_image.name}", key=uploaded_image.name):
#                     translated_text = translator.translate(extracted_text, src="auto", dest=target_lang).text

#                     st.subheader("✅ Translated Text")
#                     st.success(translated_text)

#                     save_translation(email, extracted_text, translated_text, detected_lang, target_lang)
#                     st.rerun()

#             except Exception as e:
#                 st.error(f"❌ OCR or translation failed for {uploaded_image.name}: {e}")

# view_translation_history(email)

# if st.button("⬅ Back to Dashboard"):
#     st.session_state["current_page"] = "dashboard"
#     st.experimental_rerun()


import streamlit as st
import pytesseract
from PIL import Image
from googletrans import Translator
from datetime import datetime
import tempfile
from firebase_admin import firestore
from utils.firebase_setup import init_firebase, get_user_id
import base64
import os

# Initialize Firebase
init_firebase()
db = firestore.client()

def save_translation(email, extracted_text, translated_text, source_lang, target_lang):
    user_id = get_user_id(email)
    doc_ref = db.collection("image_translations").document()
    doc_ref.set({
        "user_id": user_id,
        "email": email,
        "extracted_text": extracted_text,
        "translated_text": translated_text,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "timestamp": firestore.SERVER_TIMESTAMP
    })

def view_translation_history(email):
    st.subheader("📜 Translation History")
    try:
        docs = db.collection("image_translations") \
                 .where("email", "==", email) \
                 .order_by("timestamp", direction=firestore.Query.DESCENDING) \
                 .stream()

        docs_list = list(docs)
        if not docs_list:
            st.info("No translation history found.")
            return

        for doc in docs_list:
            data = doc.to_dict()
            ts = data.get("timestamp")
            timestamp_str = ts.strftime('%Y-%m-%d %H:%M:%S') if isinstance(ts, datetime) else "Unknown time"
            extracted_text = data.get("extracted_text", "")
            translated_text = data.get("translated_text", "")
            source_lang = data.get("source_lang", "")
            target_lang = data.get("target_lang", "")

            with st.expander(f"🕒 {timestamp_str} | {source_lang} ➜ {target_lang}"):
                st.markdown(f"**📝 Extracted:**\n{extracted_text}")
                st.markdown(f"**🌍 Translated:**\n{translated_text}")

                # Provide download link for this translation as a .txt file
                file_content = f"Extracted Text:\n{extracted_text}\n\nTranslated Text:\n{translated_text}"
                b64 = base64.b64encode(file_content.encode()).decode()
                filename = f"translation_{timestamp_str.replace(':','-').replace(' ','_')}.txt"
                href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 Download</a>'
                st.markdown(href, unsafe_allow_html=True)

                # Delete button
                if st.button("🗑️ Delete", key=f"delete_{doc.id}"):
                    db.collection("image_translations").document(doc.id).delete()
                    st.success("Deleted!")
                    st.experimental_rerun()

    except Exception as e:
        st.error(f"⚠️ Failed to load translation history: {e}")

def run():
    if not st.session_state.get("logged_in"):
        st.warning("Please log in first.")
        st.stop()

    email = st.session_state["email"]

    st.markdown("<h2 style='text-align:center;'>🖼️ Image Translator (OCR + Translate)</h2>", unsafe_allow_html=True)

    uploaded_images = st.file_uploader("📤 Upload one or more images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    uploaded_image_names = [img.name for img in uploaded_images] if uploaded_images else []

    # Clear cached texts for removed images
    if "extracted_texts" in st.session_state:
        for key in list(st.session_state.extracted_texts.keys()):
            if key not in uploaded_image_names:
                st.session_state.extracted_texts.pop(key)
                st.session_state.translated_texts.pop(key, None)

    # OCR Language options (pytesseract codes)
    lang_options = {
        "auto": "🌐 Auto-Detect",
        "eng": "🇺🇸 English",
        "hin": "🇮🇳 Hindi",
        "fra": "🇫🇷 French",
        "deu": "🇩🇪 German",
        "spa": "🇪🇸 Spanish",
        "jpn": "🇯🇵 Japanese",
        "chi_sim": "🇨🇳 Chinese (Simplified)",
        "ara": "🇸🇦 Arabic",
        "rus": "🇷🇺 Russian",
        "kor": "🇰🇷 Korean",
        "ita": "🇮🇹 Italian",
        "por": "🇵🇹 Portuguese",
        "tur": "🇹🇷 Turkish",
        "vie": "🇻🇳 Vietnamese",
        "pol": "🇵🇱 Polish",
        "nld": "🇳🇱 Dutch",
        "tha": "🇹🇭 Thai",
    }

    # Translation Language options (googletrans codes)
    target_lang_options = {
        "en": "🇺🇸 English",
        "hi": "🇮🇳 Hindi",
        "fr": "🇫🇷 French",
        "es": "🇪🇸 Spanish",
        "de": "🇩🇪 German",
        "zh-cn": "🇨🇳 Chinese (Simplified)",
        "zh-tw": "🇹🇼 Chinese (Traditional)",
        "ja": "🇯🇵 Japanese",
        "ar": "🇸🇦 Arabic",
        "ru": "🇷🇺 Russian",
        "ko": "🇰🇷 Korean",
        "it": "🇮🇹 Italian",
        "pt": "🇵🇹 Portuguese",
        "tr": "🇹🇷 Turkish",
        "vi": "🇻🇳 Vietnamese",
        "pl": "🇵🇱 Polish",
        "nl": "🇳🇱 Dutch",
        "th": "🇹🇭 Thai",
    }

    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox(
            "🔤 OCR Source Language",
            options=list(lang_options.keys()),
            format_func=lambda x: lang_options[x]
        )
    with col2:
        target_lang = st.selectbox(
            "🌐 Target Translation Language",
            options=list(target_lang_options.keys()),
            format_func=lambda x: target_lang_options[x]
        )

    translator = Translator()

    # State to keep extracted texts and translations
    if "extracted_texts" not in st.session_state:
        st.session_state.extracted_texts = {}
    if "translated_texts" not in st.session_state:
        st.session_state.translated_texts = {}

    if uploaded_images:
        for uploaded_image in uploaded_images:
            st.image(uploaded_image, caption=f"📷 {uploaded_image.name}", use_container_width=True)

            # If OCR not done yet for this image, do it
            if uploaded_image.name not in st.session_state.extracted_texts:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                    tmp_file.write(uploaded_image.getbuffer())
                    tmp_file.flush()

                    try:
                        detected_lang = source_lang
                        if source_lang == "auto":
                            try:
                                osd = pytesseract.image_to_osd(Image.open(tmp_file.name), output_type=pytesseract.Output.DICT)
                                script = osd.get("script", "Latin").lower()
                                lang_map = {
                                    "latin": "eng",
                                    "devanagari": "hin",
                                    "cyrillic": "rus",
                                    "japanese": "jpn",
                                    "chinese": "chi_sim"
                                }
                                detected_lang = lang_map.get(script, "eng")
                                st.info(f"🔎 Detected OCR Language: `{detected_lang}`")
                            except Exception as e:
                                detected_lang = "eng"
                                st.warning(f"⚠️ Language auto-detection failed. Defaulting to English. Error: {e}")

                        # Use OCR Engine Mode 1 for handwritten support
                        custom_config = r'--oem 1'
                        extracted_text = pytesseract.image_to_string(Image.open(tmp_file.name), lang=detected_lang, config=custom_config)

                        st.session_state.extracted_texts[uploaded_image.name] = (extracted_text, detected_lang)

                    except Exception as e:
                        st.error(f"❌ OCR failed for {uploaded_image.name}: {e}")
                        st.session_state.extracted_texts[uploaded_image.name] = ("", detected_lang)

                    finally:
                        try:
                            os.unlink(tmp_file.name)
                        except Exception:
                            pass

            # Show extracted text if available
            if uploaded_image.name in st.session_state.extracted_texts:
                extracted_text, detected_lang = st.session_state.extracted_texts[uploaded_image.name]
                st.subheader(f"📝 Extracted Text from {uploaded_image.name}")
                st.code(extracted_text)

                # Translate button (allow multiple translations)
                if st.button(f"🌍 Translate {uploaded_image.name}", key=f"translate_{uploaded_image.name}"):
                    with st.spinner(f"Translating {uploaded_image.name}..."):
                        try:
                            translated_text = translator.translate(extracted_text, src="auto", dest=target_lang).text
                            st.session_state.translated_texts[uploaded_image.name] = translated_text

                            save_translation(email, extracted_text, translated_text, detected_lang, target_lang)
                            st.success(f"Translation saved for {uploaded_image.name}")

                        except Exception as e:
                            st.error(f"❌ Translation failed for {uploaded_image.name}: {e}")

                # Show translated text if available
                if uploaded_image.name in st.session_state.translated_texts:
                    st.subheader(f"✅ Translated Text for {uploaded_image.name}")
                    st.success(st.session_state.translated_texts[uploaded_image.name])

    # Show translation history
    view_translation_history(email)

    if st.button("⬅ Back to Dashboard"):
        st.session_state["current_page"] = "dashboard"
        st.rerun()

if __name__ == "__main__":
    run()
