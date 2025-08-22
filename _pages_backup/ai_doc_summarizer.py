# import streamlit as st
# from googletrans import LANGUAGES, Translator
# from firebase_admin import firestore
# from utils.firebase_setup import init_firebase, get_user_id
# from api.summarizer_api import summarize_text
# from datetime import datetime
# import PyPDF2, docx, base64, os
# import textwrap
# from fpdf import FPDF
# from io import BytesIO


# def ai_doc_summarizer_ui(uid):
#     # --- STYLING ---
#     st.markdown("""
#     <style>
#     body, * {
#         font-family: 'Times New Roman', Times, serif;
#     }
#     .summary-card {
#         background-color: #1e1e1e;
#         color: #f1f1f1;
#         padding: 20px;
#         border-radius: 12px;
#         margin-bottom: 15px;
#     }
#     .button-row {
#         display: flex;
#         justify-content: space-between;
#         gap: 10px;
#         margin-top: 10px;
#     }
#     .stButton > button {
#         font-family: 'Times New Roman', Times, serif;
#     }
#     .back-btn {
#         background-color: #333333;
#         color: white;
#         padding: 10px 18px;
#         border: none;
#         border-radius: 10px;
#         cursor: pointer;
#         transition: background-color 0.3s ease, transform 0.2s ease;
#         font-size: 16px;
#         margin-top: 30px;
#     }
#     .back-btn:hover {
#         background-color: #555555;
#         transform: scale(1.05);
#     }
#     .download-buttons {
#         display: flex;
#         align-items: center;
#         gap: 12px;
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     # --- INIT ---
#     st.title("🧠 AI Document Summarizer + 🌍 Translator")
#     init_firebase()
#     translator = Translator()

#     if not st.session_state.get("logged_in") or not st.session_state.get("email"):
#         st.warning("🔐 Please log in first.")
#         st.stop()

#     db = firestore.client()
#     user_email = st.session_state["email"]
#     user_id = get_user_id(user_email)
#     summary_ref = db.collection("summaries").document(user_id).collection("items")

#     # --- UTILS ---
#     def extract_text(file):
#         if file.type == "application/pdf":
#             reader = PyPDF2.PdfReader(file)
#             return " ".join(page.extract_text() or "" for page in reader.pages)
#         elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#             doc = docx.Document(file)
#             return " ".join(paragraph.text for paragraph in doc.paragraphs)
#         elif file.type == "text/plain":
#             return file.read().decode()
#         return ""

#     def store_summary(original_text, summary, translated, lang_code):
#         summary_ref.add({
#             "original": original_text,
#             "summary": summary,
#             "translated": translated,
#             "language": lang_code,
#             "timestamp": datetime.utcnow()
#         })

#     def get_txt_download_link(content, filename):
#         b64 = base64.b64encode(content.encode()).decode()
#         return f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 TXT</a>'

#     def get_pdf_download_link(content, filename):
#         pdf = FPDF()
#         pdf.add_page()
#         pdf.add_font('DejaVu', '', os.path.join("assets", "fonts", "DejaVuSans.ttf"), uni=True)
#         pdf.set_font("DejaVu", size=12)
#         pdf.set_auto_page_break(auto=True, margin=15)

#         for line in textwrap.wrap(content, width=90):
#             pdf.cell(0, 10, txt=line, ln=True)

#         pdf_bytes = BytesIO()
#         pdf.output(pdf_bytes)
#         b64 = base64.b64encode(pdf_bytes.getvalue()).decode()
#         return f'<a href="data:application/pdf;base64,{b64}" download="{filename}">📄 PDF</a>'

#     def split_text_into_chunks(text, max_words=1000):
#         words = text.split()
#         return [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

#     # --- INPUT ---
#     uploaded_file = st.file_uploader("📂 Upload Document", type=["pdf", "docx", "txt"])

#     lang_names = {code: name.title() for code, name in LANGUAGES.items()}
#     lang_code_to_name = {v: k for k, v in lang_names.items()}
#     sorted_langs = sorted(lang_names.items(), key=lambda x: x[1])

#     col1, col2 = st.columns(2)
#     selected_lang_name = col1.selectbox("🌍 Translate Summary To:", [name for _, name in sorted_langs])
#     lang_code = lang_code_to_name[selected_lang_name]
#     auto_summarize = col2.checkbox("⚡ Auto Summarize")

#     if uploaded_file:
#         full_text = extract_text(uploaded_file)
#         if not full_text.strip():
#             st.warning("❌ No text found in document.")
#         else:
#             st.subheader("📄 Extracted Document Text")
#             st.text_area("Full content", full_text[:3000] + "...", height=200)

#             word_count = len(full_text.split())
#             max_len = 512 if word_count > 2000 else 400 if word_count > 1000 else 200

#             if auto_summarize or st.button("🧠 Summarize & Translate"):
#                 with st.spinner("Generating summary..."):
#                     chunks = split_text_into_chunks(full_text, 1000)
#                     summaries = [summarize_text(chunk, max_length=max_len) for chunk in chunks]
#                     combined_summary = "\n".join(summaries)
#                     translated = translator.translate(combined_summary, dest=lang_code).text
#                     store_summary(full_text, combined_summary, translated, lang_code)
#                     st.success("✅ Summary Saved!")
#                     st.rerun()

#     # --- SEARCH / FILTER ---
#     st.subheader("🔎 Filter Summaries")
#     filter_lang = st.selectbox("🌐 Filter by Language", ["All"] + [name for _, name in sorted_langs])
#     filter_date = st.date_input("📅 Filter by Date", value=None)

#     # --- VIEW HISTORY ---
#     st.subheader("🕓 Your Past Summaries")
#     summaries = summary_ref.order_by("timestamp", direction=firestore.Query.DESCENDING).stream()

#     for doc in summaries:
#         data = doc.to_dict()
#         timestamp = data.get("timestamp", "").strftime("%Y-%m-%d %H:%M") if "timestamp" in data else "N/A"
#         doc_id = doc.id

#         lang_name = lang_names.get(data.get("language", ""), data.get("language", "Unknown")).title()
#         date_match = (not filter_date or (data.get("timestamp") and data["timestamp"].date() == filter_date))
#         lang_match = (filter_lang == "All" or lang_name == filter_lang)

#         if date_match and lang_match:
#             st.markdown(f"""
#             <div class="summary-card">
#                 <strong>🗓️ {timestamp}</strong><br><br>
#                 <b>📝 Summary:</b><br>{data.get("summary", "")[:1000]}...<br><br>
#                 <b>🌐 Translated ({lang_name}):</b><br>{data.get("translated", "")[:1000]}...
#                 <div class="button-row">
#                     <div class="download-buttons">
#                         {get_txt_download_link(data.get("translated", ""), "summary.txt")}
#                         {get_pdf_download_link(data.get("translated", ""), "summary.pdf")}
#                     </div>
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)

#             if st.button(f"🗑️ Confirm Delete {timestamp}", key=doc_id):
#                 summary_ref.document(doc_id).delete()
#                 st.success("🗑️ Summary deleted.")
#                 st.rerun()

#     # --- BACK BUTTON ---
#     if st.button("⬅ Back to Dashboard"):
#         st.session_state["current_page"] = "dashboard"
#         st.rerun()

# # --- EXPORTABLE ENTRY POINT ---
# def run(uid):
#     ai_doc_summarizer_ui(uid)




# import streamlit as st
# from googletrans import LANGUAGES, Translator
# from firebase_admin import firestore
# from utils.firebase_setup import init_firebase, get_user_id
# from api.summarizer_api import summarize_text
# from datetime import datetime
# import PyPDF2, docx, base64, os
# import textwrap
# from fpdf import FPDF
# from io import BytesIO
# import os
# import textwrap


# def ai_doc_summarizer_ui(uid=None):
#     # --- STYLING ---
#     st.markdown("""
#     <style>
#     body, * {
#         font-family: 'Times New Roman', Times, serif;
#     }
#     .summary-card {
#         background-color: #1e1e1e;
#         color: #f1f1f1;
#         padding: 20px;
#         border-radius: 12px;
#         margin-bottom: 15px;
#     }
#     .button-row {
#         display: flex;
#         justify-content: space-between;
#         gap: 10px;
#         margin-top: 10px;
#     }
#     .stButton > button {
#         font-family: 'Times New Roman', Times, serif;
#     }
#     .back-btn {
#         background-color: #333333;
#         color: white;
#         padding: 10px 18px;
#         border: none;
#         border-radius: 10px;
#         cursor: pointer;
#         transition: background-color 0.3s ease, transform 0.2s ease;
#         font-size: 16px;
#         margin-top: 30px;
#     }
#     .back-btn:hover {
#         background-color: #555555;
#         transform: scale(1.05);
#     }
#     .download-buttons {
#         display: flex;
#         align-items: center;
#         gap: 12px;
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     # --- INIT ---
#     st.title("🧠 AI Document Summarizer + 🌍 Translator")
#     init_firebase()
#     translator = Translator()

#     db = firestore.client()

#     # If uid not provided, fallback to generic user or guest id
#     if not uid:
#         user_email = "guest@example.com"  # or some default email/id
#         user_id = get_user_id(user_email)
#     else:
#         user_id = uid

#     summary_ref = db.collection("summaries").document(user_id).collection("items")

#     # --- UTILS ---
#     def extract_text(file):
#         if file.type == "application/pdf":
#             reader = PyPDF2.PdfReader(file)
#             return " ".join(page.extract_text() or "" for page in reader.pages)
#         elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#             doc = docx.Document(file)
#             return " ".join(paragraph.text for paragraph in doc.paragraphs)
#         elif file.type == "text/plain":
#             return file.read().decode()
#         return ""

#     def store_summary(original_text, summary, translated, lang_code):
#         summary_ref.add({
#             "original": original_text,
#             "summary": summary,
#             "translated": translated,
#             "language": lang_code,
#             "timestamp": datetime.utcnow()
#         })

#     def get_txt_download_link(content, filename):
#         b64 = base64.b64encode(content.encode()).decode()
#         return f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 TXT</a>'

#     def get_pdf_download_link(content, filename):
#         pdf = FPDF()
#         pdf.add_page()
#         pdf.add_font('DejaVu', '', os.path.join("assets", "fonts", "DejaVuSans.ttf"), uni=True)
#         pdf.set_font("DejaVu", size=12)
#         pdf.set_auto_page_break(auto=True, margin=15)

#     for line in textwrap.wrap(content, width=90):
#         pdf.cell(0, 10, txt=line, ln=True)

#     pdf_bytes = pdf.output(dest='S').encode('latin1')
#     b64 = base64.b64encode(pdf_bytes).decode()
#     return f'<a href="data:application/pdf;base64,{b64}" download="{filename}">📄 PDF</a>'

#     def split_text_into_chunks(text, max_words=1000):
#         words = text.split()
#         return [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

#     # --- INPUT ---
#     uploaded_file = st.file_uploader("📂 Upload Document", type=["pdf", "docx", "txt"])

#     lang_names = {code: name.title() for code, name in LANGUAGES.items()}
#     lang_code_to_name = {v: k for k, v in lang_names.items()}
#     sorted_langs = sorted(lang_names.items(), key=lambda x: x[1])

#     col1, col2 = st.columns(2)
#     selected_lang_name = col1.selectbox("🌍 Translate Summary To:", [name for _, name in sorted_langs])
#     lang_code = lang_code_to_name[selected_lang_name]
#     auto_summarize = col2.checkbox("⚡ Auto Summarize")

#     if uploaded_file:
#         full_text = extract_text(uploaded_file)
#         if not full_text.strip():
#             st.warning("❌ No text found in document.")
#         else:
#             st.subheader("📄 Extracted Document Text")
#             st.text_area("Full content", full_text[:3000] + "...", height=200)

#             word_count = len(full_text.split())
#             max_len = 512 if word_count > 2000 else 400 if word_count > 1000 else 200

#             if auto_summarize or st.button("🧠 Summarize & Translate"):
#                 with st.spinner("Generating summary..."):
#                     chunks = split_text_into_chunks(full_text, 1000)
#                     summaries = [summarize_text(chunk, max_length=max_len) for chunk in chunks]
#                     combined_summary = "\n".join(summaries)
#                     translated = translator.translate(combined_summary, dest=lang_code).text
#                     store_summary(full_text, combined_summary, translated, lang_code)
#                     st.success("✅ Summary Saved!")
#                     st.experimental_rerun()

#     # --- SEARCH / FILTER ---
#     st.subheader("🔎 Filter Summaries")
#     filter_lang = st.selectbox("🌐 Filter by Language", ["All"] + [name for _, name in sorted_langs])
#     filter_date = st.date_input("📅 Filter by Date", value=None)

#     # --- VIEW HISTORY ---
#     st.subheader("🕓 Your Past Summaries")
#     summaries = summary_ref.order_by("timestamp", direction=firestore.Query.DESCENDING).stream()

#     for doc in summaries:
#         data = doc.to_dict()
#         timestamp = data.get("timestamp", "").strftime("%Y-%m-%d %H:%M") if "timestamp" in data else "N/A"
#         doc_id = doc.id

#         lang_name = lang_names.get(data.get("language", ""), data.get("language", "Unknown")).title()
#         date_match = (not filter_date or (data.get("timestamp") and data["timestamp"].date() == filter_date))
#         lang_match = (filter_lang == "All" or lang_name == filter_lang)

#         if date_match and lang_match:
#             st.markdown(f"""
#             <div class="summary-card">
#                 <strong>🗓️ {timestamp}</strong><br><br>
#                 <b>📝 Summary:</b><br>{data.get("summary", "")[:1000]}...<br><br>
#                 <b>🌐 Translated ({lang_name}):</b><br>{data.get("translated", "")[:1000]}...
#                 <div class="button-row">
#                     <div class="download-buttons">
#                         {get_txt_download_link(data.get("translated", ""), "summary.txt")}
#                         {get_pdf_download_link(data.get("translated", ""), "summary.pdf")}
#                     </div>
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)

#             if st.button(f"🗑️ Confirm Delete {timestamp}", key=doc_id):
#                 summary_ref.document(doc_id).delete()
#                 st.success("🗑️ Summary deleted.")
#                 st.experimental_rerun()

#     # --- BACK BUTTON ---
#     if st.button("⬅ Back to Dashboard"):
#         st.session_state["current_page"] = "dashboard"
#         st.experimental_rerun()

# # --- EXPORTABLE ENTRY POINT ---
# def run(uid=None):
#     ai_doc_summarizer_ui(uid)



import streamlit as st
from googletrans import LANGUAGES, Translator
from firebase_admin import firestore
from utils.firebase_setup import init_firebase, get_user_id
from api.summarizer_api import summarize_text
from datetime import datetime
import PyPDF2, docx, base64, os
from fpdf import FPDF
import textwrap

def ai_doc_summarizer_ui(uid=None):
    # --- STYLING ---
    st.markdown("""
    <style>
    body, * {
        font-family: 'Times New Roman', Times, serif;
    }
    .summary-card {
        background-color: #1e1e1e;
        color: #f1f1f1;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
    }
    .button-row {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin-top: 10px;
    }
    .stButton > button {
        font-family: 'Times New Roman', Times, serif;
    }
    .back-btn {
        background-color: #333333;
        color: white;
        padding: 10px 18px;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.2s ease;
        font-size: 16px;
        margin-top: 30px;
    }
    .back-btn:hover {
        background-color: #555555;
        transform: scale(1.05);
    }
    .download-buttons {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- INIT ---
    st.title("🧠 AI Document Summarizer + 🌍 Translator")
    init_firebase()
    translator = Translator()
    db = firestore.client()
    user_id = uid if uid else get_user_id("guest@example.com")
    summary_ref = db.collection("summaries").document(user_id).collection("items")

    # --- UTILS ---
    def extract_text(file):
        if file.type == "application/pdf":
            reader = PyPDF2.PdfReader(file)
            return " ".join(page.extract_text() or "" for page in reader.pages)
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(file)
            return " ".join(paragraph.text for paragraph in doc.paragraphs)
        elif file.type == "text/plain":
            return file.read().decode()
        return ""

    def store_summary(original_text, summary, translated, lang_code):
        summary_ref.add({
            "original": original_text,
            "summary": summary,
            "translated": translated,
            "language": lang_code,
            "timestamp": datetime.utcnow()
        })

    def get_txt_download_link(content, filename):
        b64 = base64.b64encode(content.encode()).decode()
        return f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 TXT</a>'

    def get_pdf_download_link(content, filename):
        pdf = FPDF()
        pdf.add_page()
        font_path = os.path.join("assets", "fonts", "DejaVuSans.ttf")
        if os.path.exists(font_path):
            pdf.add_font('DejaVu', '', font_path, uni=True)
            pdf.set_font("DejaVu", size=12)
        else:
            pdf.set_font("Arial", size=12)
        pdf.set_auto_page_break(auto=True, margin=15)
        for line in textwrap.wrap(content, width=90):
            pdf.cell(0, 10, txt=line, ln=True)
        pdf_bytes = pdf.output(dest='S').encode('latin1')
        b64 = base64.b64encode(pdf_bytes).decode()
        return f'<a href="data:application/pdf;base64,{b64}" download="{filename}">📄 PDF</a>'

    def split_text_into_chunks(text, max_words=1000):
        words = text.split()
        return [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

    # --- INPUT ---
    uploaded_file = st.file_uploader("📂 Upload Document", type=["pdf", "docx", "txt"])
    lang_names = {code: name.title() for code, name in LANGUAGES.items()}
    lang_code_to_name = {v: k for k, v in lang_names.items()}
    sorted_langs = sorted(lang_names.items(), key=lambda x: x[1])
    col1, col2 = st.columns(2)
    selected_lang_name = col1.selectbox("🌍 Translate Summary To:", [name for _, name in sorted_langs])
    lang_code = lang_code_to_name[selected_lang_name]
    auto_summarize = col2.checkbox("⚡ Auto Summarize")

    if uploaded_file:
        full_text = extract_text(uploaded_file)
        if not full_text.strip():
            st.warning("❌ No text found in document.")
        else:
            st.subheader("📄 Extracted Document Text")
            st.text_area("Full content", full_text[:3000] + "...", height=200)
            word_count = len(full_text.split())
            max_len = 512 if word_count > 2000 else 400 if word_count > 1000 else 200

            if auto_summarize or st.button("🧠 Summarize & Translate"):
                with st.spinner("Generating summary..."):
                    chunks = split_text_into_chunks(full_text, 1000)
                    summaries = [summarize_text(chunk, max_length=max_len) for chunk in chunks]
                    combined_summary = "\n".join(summaries)
                    translated = translator.translate(combined_summary, dest=lang_code).text
                    store_summary(full_text, combined_summary, translated, lang_code)
                    st.success("✅ Summary Saved!")
                    st.rerun()

    # --- SEARCH / FILTER ---
    st.subheader("🔎 Filter Summaries")
    filter_lang = st.selectbox("🌐 Filter by Language", ["All"] + [name for _, name in sorted_langs])
    filter_date = st.date_input("📅 Filter by Date", value=None)

    # --- VIEW HISTORY ---
    st.subheader("🕓 Your Past Summaries")
    summaries = summary_ref.order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
    for doc in summaries:
        data = doc.to_dict()
        timestamp = data.get("timestamp", "").strftime("%Y-%m-%d %H:%M") if "timestamp" in data else "N/A"
        doc_id = doc.id
        lang_name = lang_names.get(data.get("language", ""), data.get("language", "Unknown")).title()
        date_match = (not filter_date or (data.get("timestamp") and data["timestamp"].date() == filter_date))
        lang_match = (filter_lang == "All" or lang_name == filter_lang)

        if date_match and lang_match:
            st.markdown(f"""
            <div class="summary-card">
                <strong>🗓️ {timestamp}</strong><br><br>
                <b>📝 Summary:</b><br>{data.get("summary", "")[:1000]}...<br><br>
                <b>🌐 Translated ({lang_name}):</b><br>{data.get("translated", "")[:1000]}...
                <div class="button-row">
                    <div class="download-buttons">
                        {get_txt_download_link(data.get("translated", ""), "summary.txt")}
                        {get_pdf_download_link(data.get("translated", ""), "summary.pdf")}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"🗑️ Confirm Delete {timestamp}", key=doc_id):
                summary_ref.document(doc_id).delete()
                st.success("🗑️ Summary deleted.")
                st.rerun()

    # --- BACK BUTTON ---
    if st.button("⬅ Back to Dashboard"):
        st.session_state["current_page"] = "dashboard"
        st.rerun()

# --- EXPORTABLE ENTRY POINT ---
def run(uid=None):
    ai_doc_summarizer_ui(uid)
