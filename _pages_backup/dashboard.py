
# import streamlit as st
# import datetime
# import plotly.express as px
# from utils.firestore_utils import (
#     get_user_data, get_recent_activity, get_daily_usage,
#     get_daily_voice_usage, get_language_usage, update_user_profile
# )

# # === Inject External Styles ===
# def inject_css():
#     with open("assets/styles/dashboard_styles.css") as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# # === Admin View ===
# def show_admin_view():
#     st.subheader("🛠️ Admin Panel: All Users")
#     from utils.firestore_utils import db
#     users = db.collection("users").stream()
#     for user in users:
#         d = user.to_dict()
#         st.markdown(f"- 👤 **{d.get('name')}** ({d.get('email')})")

# # === Dashboard UI ===
# def show_dashboard(uid):
#     inject_css()

#     user = get_user_data(uid)
#     if not user:
#         st.error("⚠️ User not found.")
#         return

#     name = user.get("name", "User")
#     photo_url = user.get("photo_url", "https://cdn-icons-png.flaticon.com/512/3135/3135715.png")
#     is_admin = user.get("is_admin", False)

#     # Sidebar
#     # with st.sidebar:
#     #     st.image(photo_url, width=120)
#     #     st.subheader(name)

#         # if st.button("✏️ Edit Profile"):
#             # with st.form("edit_profile"):
#                 # new_name = st.text_input("Display Name", value=name)
#                 # new_photo = st.text_input("Photo URL", value=photo_url)
#                 # if st.form_submit_button("Update"):
#                 #     update_user_profile(uid, new_name, new_photo)
#                 #     st.experimental_rerun()

#         # if is_admin and st.button("🔧 Admin View"):
#         #     st.session_state.current_page = "admin"
#         #     st.rerun()

#         # if st.button("🔓 Logout"):
#         #     st.session_state.logged_in = False
#         #     st.session_state.pop("uid", None)
#         #     st.session_state.current_page = "dashboard"
#         #     st.rerun()

#     st.markdown(
#         f"""<div class="welcome-section">
#              <img src='{photo_url}' class='profile-pic'/>
#              <h2>👋 Welcome, <span>{name}</span>!</h2>
#              <p>Your personalized translation dashboard ✨</p>
#            </div>""",
#         unsafe_allow_html=True
#     )

#     # Metrics
#     c1, c2, c3 = st.columns(3)
#     c1.metric("📝 Text Translations", user.get("text_translations", 0))
#     c2.metric("🎙️ Voice Translations", user.get("voice_translations", 0))
#     c3.metric("🖼️ Image Translations", user.get("image_translations", 0))

#     # Daily usage
#     st.subheader("📊 Daily Translation Usage (Last 7 Days)")
#     daily = get_daily_usage(uid)
#     if daily:
#         dates, counts = zip(*daily)
#         fig = px.bar(x=dates, y=counts, labels={"x": "Date", "y": "Count"}, height=300)
#         st.plotly_chart(fig, use_container_width=True)
#     else:
#         st.info("No usage data for the last 7 days.")

#     # Voice usage
#     st.subheader("🎙️ Daily Voice Usage")
#     voice = get_daily_voice_usage(uid)
#     if voice:
#         v_dates, v_counts = zip(*voice)
#         fig_v = px.line(x=v_dates, y=v_counts, labels={"x": "Date", "y": "Voice Translations"}, height=300)
#         st.plotly_chart(fig_v, use_container_width=True)
#     else:
#         st.info("No voice data.")

#     # Language pairs
#     st.subheader("🌍 Top Language Pairs")
#     langs = get_language_usage(uid)
#     if langs:
#         pie = px.pie(names=list(langs.keys()), values=list(langs.values()), title="Languages Translated")
#         st.plotly_chart(pie, use_container_width=True)
#     else:
#         st.info("No language usage yet.")

#     # Recent activity
#     st.subheader("🕘 Recent Activity")
#     logs = get_recent_activity(uid)
#     if logs:
#         for log in logs:
#             ts = log.get("timestamp", datetime.datetime.utcnow())
#             st.markdown(f"""
#                 <div class='activity-card'>
#                   <b>🔹 {log.get('type','Activity')}</b> at <i>{ts.strftime('%b %d, %Y %H:%M')}</i><br/>
#                   <span>{log.get('description','')}</span>
#                 </div>
#             """, unsafe_allow_html=True)
#     else:
#         st.info("No recent activity.")

#     # Feature Access
#     st.subheader("🚀 Feature Navigation")
#     feature_names = [
#         ("📝 Text Translator", "text_translator"),
#         ("🎙️ Voice Translator", "voice_translator"),
#         ("🖼️ Image Translator", "image_translator"),
#         ("📄 Document Translator", "document_translator"),
#         ("🎤 Speech-to-Speech", "speech_to_speech"),
#         ("🧠 AI Doc Summarizer", "ai_doc_summarizer"),
#         ("💬 Chat Translator", "chat_translator"),
#         ("🤖 Voice Assistant", "voice_assistant"),
#         ("🌐 UI Translator", "ui_translator"),
#         ("📊 Admin Analytics", "admin_analytics"),
#         ("🎞️ Video Subtitles", "video_subtitles"),
#     ]

#     for label, page in feature_names:
#         if st.button(label):
#             st.session_state.current_page = page
#             st.rerun()

#     st.markdown("<center><sub>🔒 All translations are private & secure</sub></center>", unsafe_allow_html=True)

# # === Dispatcher ===
# def run(uid):
#     if "uid" not in st.session_state:
#         st.session_state.uid = uid
#     if "current_page" not in st.session_state:
#         st.session_state.current_page = "dashboard"

#     if st.session_state.current_page == "dashboard":
#         show_dashboard(uid)
#     elif st.session_state.current_page == "admin":
#         show_admin_view()

#     elif st.session_state.current_page == "text_translator":
#         from _pages_backup.text_translator import run_text_translator
#         run_text_translator()

#     elif st.session_state.current_page == "voice_translator":
#         from _pages_backup.voice_translator import run as run_voice_translator
#         run_voice_translator()

#     elif st.session_state.current_page == "image_translator":
#         from _pages_backup.image_translator import run as run_image_translator
#         run_image_translator()

#     elif st.session_state.current_page == "document_translator":
#         from _pages_backup.document_translator import run as run_document_translator
#         run_document_translator()

#     elif st.session_state.current_page == "speech_to_speech":
#         from _pages_backup.speech_to_speech import run as run_speech_to_speech
#         run_speech_to_speech()

#     elif st.session_state.current_page == "chat_translator":
#         from _pages_backup.chat_translator import run as run_chat_translator
#         run_chat_translator()

#     elif st.session_state.current_page == "ai_doc_summarizer":
#         from _pages_backup.ai_doc_summarizer import run as run_ai_doc_summarizer
#         run_ai_doc_summarizer()

#     elif st.session_state.current_page == "voice_assistant":
#         from _pages_backup.voice_assistant import run as run_voice_assistant
#         run_voice_assistant()

#     elif st.session_state.current_page == "ui_translator":
#         from _pages_backup.ui_translator import run as run_ui_translator
#         run_ui_translator()

#     elif st.session_state.current_page == "admin_analytics":
#         from _pages_backup.admin_analytics import run as run_admin_analytics
#         run_admin_analytics()

#     elif st.session_state.current_page == "video_subtitles":
#         from _pages_backup.video_subtitles import run as run_video_subtitles
#         run_video_subtitles()


import streamlit as st
import datetime
import plotly.express as px
from utils.firestore_utils import (
    get_user_data, get_recent_activity, get_daily_usage,
    get_daily_voice_usage, get_language_usage, update_user_profile
)

# === Inject External Styles ===
def inject_css():
    with open("assets/styles/dashboard_styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# === Admin View ===
def show_admin_view():
    st.subheader("🛠️ Admin Panel: All Users")
    from utils.firestore_utils import db
    users = db.collection("users").stream()
    for user in users:
        d = user.to_dict()
        st.markdown(f"- 👤 **{d.get('name')}** ({d.get('email')})")

# === Dashboard UI ===
def show_dashboard(uid):
    inject_css()

    user = get_user_data(uid)
    if not user:
        st.error("⚠️ User not found.")
        return

    name = user.get("name", "User")
    photo_url = user.get("photo_url", "https://cdn-icons-png.flaticon.com/512/3135/3135715.png")
    is_admin = user.get("is_admin", False)


    st.markdown(
        f"""<div class="welcome-section">
             <img src='{photo_url}' class='profile-pic'/>
             <h2>👋 Welcome, <span>{name}</span>!</h2>
             <p>Your personalized translation dashboard ✨</p>
           </div>""",
        unsafe_allow_html=True
    )

    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("📝 Text Translations", user.get("text_translations", 0))
    c2.metric("🎙️ Voice Translations", user.get("voice_translations", 0))
    c3.metric("🖼️ Image Translations", user.get("image_translations", 0))

    # Daily usage
    st.subheader("📊 Daily Translation Usage (Last 7 Days)")
    daily = get_daily_usage(uid)
    if daily:
        dates, counts = zip(*daily)
        fig = px.bar(x=dates, y=counts, labels={"x": "Date", "y": "Count"}, height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No usage data for the last 7 days.")

    # Voice usage
    st.subheader("🎙️ Daily Voice Usage")
    voice = get_daily_voice_usage(uid)
    if voice:
        v_dates, v_counts = zip(*voice)
        fig_v = px.line(x=v_dates, y=v_counts, labels={"x": "Date", "y": "Voice Translations"}, height=300)
        st.plotly_chart(fig_v, use_container_width=True)
    else:
        st.info("No voice data.")

    # Language pairs
    st.subheader("🌍 Top Language Pairs")
    langs = get_language_usage(uid)
    if langs:
        pie = px.pie(names=list(langs.keys()), values=list(langs.values()), title="Languages Translated")
        st.plotly_chart(pie, use_container_width=True)
    else:
        st.info("No language usage yet.")

    # Recent activity
    st.subheader("🕘 Recent Activity")
    logs = get_recent_activity(uid)
    if logs:
        for log in logs:
            ts = log.get("timestamp", datetime.datetime.utcnow())
            st.markdown(f"""
                <div class='activity-card'>
                  <b>🔹 {log.get('type','Activity')}</b> at <i>{ts.strftime('%b %d, %Y %H:%M')}</i><br/>
                  <span>{log.get('description','')}</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent activity.")

    st.markdown("---")
    st.subheader("🚀 Feature Navigation")

    feature_names = [
        ("📝 Text Translator", "text_translator"),
        ("🎙️ Voice Translator", "voice_translator"),
        ("🖼️ Image Translator", "image_translator"),
        ("📄 Document Translator", "document_translator"),
        ("🎤 Speech-to-Speech", "speech_to_speech"),
        ("🧠 AI Doc Summarizer", "ai_doc_summarizer"),
        ("💬 Chat Translator", "chat_translator"),
        ("🤖 Voice Assistant", "voice_assistant"),
        ("🌐 UI Translator", "ui_translator"),
        ("📊 Admin Analytics", "admin_analytics"),
        ("🎞️ Video Subtitles", "video_subtitles"),
    ]

    for i in range(0, len(feature_names), 3):
        cols = st.columns(3)
        for idx, (label, page) in enumerate(feature_names[i:i+3]):
            with cols[idx]:
                if st.button(label, key=f"feature_{page}"):
                    st.session_state.current_page = page
                    st.rerun()

    st.markdown(
        """
        <div style='text-align: center; padding-top: 20px; font-size: 0.9rem; color: gray;'>
            🔒 All translations are private & secure
        </div>
        """,
        unsafe_allow_html=True
    )


# === Dispatcher ===
def run(uid):
    if "uid" not in st.session_state:
        st.session_state.uid = uid
    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"

    if st.session_state.current_page == "dashboard":
        show_dashboard(uid)
    elif st.session_state.current_page == "admin":
        show_admin_view()

    elif st.session_state.current_page == "text_translator":
        from _pages_backup.text_translator import run_text_translator
        run_text_translator()

    elif st.session_state.current_page == "voice_translator":
        from _pages_backup.voice_translator import run as run_voice_translator
        run_voice_translator(uid)

    elif st.session_state.current_page == "image_translator":
        from _pages_backup.image_translator import run as run_image_translator
        run_image_translator()

    elif st.session_state.current_page == "document_translator":
        from _pages_backup.document_translator import run as run_document_translator
        run_document_translator(uid)

    elif st.session_state.current_page == "speech_to_speech":
        from _pages_backup.speech_to_speech import run as run_speech_to_speech
        run_speech_to_speech(uid)

    elif st.session_state.current_page == "chat_translator":
        from _pages_backup.chat_translator import run_chat_translator
        run_chat_translator()

    elif st.session_state.current_page == "ai_doc_summarizer":
        from _pages_backup.ai_doc_summarizer import run as run_ai_doc_summarizer
        run_ai_doc_summarizer(uid)

    elif st.session_state.current_page == "voice_assistant":
        from _pages_backup.voice_assistant import run as run_voice_assistant
        run_voice_assistant(uid)

    elif st.session_state.current_page == "ui_translator":
        from _pages_backup.ui_translator import run as run_ui_translator
        run_ui_translator()

    elif st.session_state.current_page == "admin_analytics":
        from _pages_backup.admin_analytics import run as run_admin_analytics
        run_admin_analytics(uid)

    elif st.session_state.current_page == "video_subtitles":
        from _pages_backup.video_subtitles import run as run_video_subtitles
        run_video_subtitles(uid)