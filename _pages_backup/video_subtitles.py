import streamlit as st
import tempfile
import os
import whisper
import srt
import subprocess
from datetime import timedelta, datetime
from googletrans import Translator
from moviepy.editor import VideoFileClip
from utils.firebase_utils import upload_file_to_storage, log_file_metadata_to_realtime_db

LANG_OPTIONS = {
    "en": "English", "hi": "Hindi", "fr": "French", "de": "German",
    "es": "Spanish", "zh": "Chinese", "ja": "Japanese"
}

def format_srt(segments):
    srt_list = []
    for i, seg in enumerate(segments):
        start = timedelta(seconds=seg["start"])
        end = timedelta(seconds=seg["end"])
        srt_item = srt.Subtitle(index=i+1, start=start, end=end, content=seg["text"])
        srt_list.append(srt_item)
    return srt.compose(srt_list)

def mux_video_with_subtitles(video_path, subtitle_paths, output_path, languages):
    cmd = ['ffmpeg', '-y', '-i', video_path]

    for i, (sub_path, lang_code) in enumerate(zip(subtitle_paths, languages)):
        cmd += ['-i', sub_path]

    # Map streams and assign language metadata
    map_cmds = ['-map', '0']
    for i in range(len(subtitle_paths)):
        map_cmds += ['-map', str(i + 1)]

    metadata_cmds = []
    for i, lang_code in enumerate(languages):
        metadata_cmds += [
            f"-metadata:s:s:{i}", f"language={lang_code}"
        ]

    cmd += map_cmds + metadata_cmds + ['-c', 'copy', output_path]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run(uid):
    st.title("🎬 Multilingual Video Subtitle Generator")

    video_file = st.file_uploader("📂 Upload a video file", type=["mp4"])

    col1, col2 = st.columns(2)
    with col1:
        src_lang = st.selectbox("🗣️ Transcription Language", list(LANG_OPTIONS.keys()), index=0)
    with col2:
        target_langs = st.multiselect("🌍 Translate Subtitles To", list(LANG_OPTIONS.keys()), default=["hi", "fr"])

    if st.button("⬅ Back to Dashboard"):
        st.session_state["current_page"] = "dashboard"
        st.rerun()

    if video_file:
        st.video(video_file)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_vid:
            tmp_vid.write(video_file.read())
            video_path = tmp_vid.name

        st.info("⏳ Extracting audio and generating subtitles...")

        try:
            audio_path = video_path.replace(".mp4", ".wav")
            clip = VideoFileClip(video_path)
            clip.audio.write_audiofile(audio_path, verbose=False, logger=None)

            model = whisper.load_model("base")
            result = model.transcribe(audio_path, language=src_lang)
            segments = result["segments"]

            st.subheader("📝 Original Subtitles")
            srt_original = format_srt(segments)
            st.code(srt_original[:1000])

            original_srt_path = os.path.join(tempfile.gettempdir(), f"original_{datetime.now().timestamp()}.srt")
            with open(original_srt_path, "w", encoding="utf-8") as f:
                f.write(srt_original)

            translated_srt_paths = []
            lang_codes = []

            translator = Translator()
            for lang in target_langs:
                translated_segments = []
                for seg in segments:
                    translated_text = translator.translate(seg["text"], src=src_lang, dest=lang).text
                    translated_segments.append({
                        "start": seg["start"],
                        "end": seg["end"],
                        "text": translated_text
                    })

                srt_translated = format_srt(translated_segments)
                st.subheader(f"🌐 Translated Subtitles ({LANG_OPTIONS[lang]})")
                st.code(srt_translated[:1000])

                trans_path = os.path.join(tempfile.gettempdir(), f"{lang}_{datetime.now().timestamp()}.srt")
                with open(trans_path, "w", encoding="utf-8") as f:
                    f.write(srt_translated)

                translated_srt_paths.append(trans_path)
                lang_codes.append(lang)

            # Mux all subtitles with video
            st.info("🔄 Adding multiple subtitles to video...")
            final_video_path = video_path.replace(".mp4", "_multi_subtitled.mp4")
            mux_video_with_subtitles(video_path, translated_srt_paths, final_video_path, lang_codes)

            st.success("✅ Subtitled video ready!")

            with open(final_video_path, "rb") as f:
                st.download_button("🎬 Download Subtitled Video", f, file_name="video_with_subtitles.mp4", mime="video/mp4")

            # Firebase Upload
            for lang, srt_path in zip(lang_codes, translated_srt_paths):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{lang}_subtitles_{timestamp}.srt"
                upload_file_to_storage(uid, srt_path, f"Video_Translator/{filename}")
                log_file_metadata_to_realtime_db(uid, {
                    "filename": filename,
                    "feature": "Video Translator",
                    "type": "subtitle",
                    "timestamp": timestamp,
                })

            # Cleanup
            os.remove(audio_path)
            os.remove(video_path)
            os.remove(original_srt_path)
            for path in translated_srt_paths:
                os.remove(path)
            os.remove(final_video_path)

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
