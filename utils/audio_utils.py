from edge_tts import Communicate
import uuid
import asyncio

# Language + gender voice map
LANGUAGE_VOICE_MAP = {
    "English": {
        "female": "en-US-AriaNeural",
        "male": "en-US-GuyNeural"
    },
    "Hindi": {
        "female": "hi-IN-SwaraNeural",
        "male": "hi-IN-MadhurNeural"
    },
    "Arabic": {
        "female": "ar-EG-SalmaNeural",
        "male": "ar-EG-ShakirNeural"
    },
    "Spanish": {
        "female": "es-ES-ElviraNeural",
        "male": "es-ES-AlvaroNeural"
    },
    "French": {
        "female": "fr-FR-DeniseNeural",
        "male": "fr-FR-HenriNeural"
    },
    "German": {
        "female": "de-DE-KatjaNeural",
        "male": "de-DE-ConradNeural"
    },
    "Chinese": {
        "female": "zh-CN-XiaoxiaoNeural",
        "male": "zh-CN-YunxiNeural"
    },
    "Japanese": {
        "female": "ja-JP-NanamiNeural",
        "male": "ja-JP-KeitaNeural"
    },
    "Russian": {
        "female": "ru-RU-SvetlanaNeural",
        "male": "ru-RU-DmitryNeural"
    },
    "Italian": {
        "female": "it-IT-ElsaNeural",
        "male": "it-IT-DiegoNeural"
    }
}

def get_valid_voice(language: str, gender: str) -> str:
    language = language.capitalize()
    gender = gender.lower()
    return LANGUAGE_VOICE_MAP.get(language, LANGUAGE_VOICE_MAP["English"]).get(gender, "en-US-GuyNeural")

def text_to_speech_custom(text, gender="female", speed="normal", language="English"):
    rate_map = {"slow": "-30%", "normal": "+0%", "fast": "+30%"}
    rate = rate_map.get(speed, "+0%")

    file_path = f"temp_audio_{uuid.uuid4().hex}.mp3"
    voice = get_valid_voice(language, gender)

    async def generate():
        communicate = Communicate(text=text, voice=voice, rate=rate)
        await communicate.save(file_path)

    asyncio.run(generate())
    return file_path

def extract_language_code(language_string: str) -> str:
    """
    Extracts the ISO language code from a label like 'English 🇺🇸'
    For example: 'English 🇺🇸' -> 'en'
    """
    language = language_string.split(" ")[0].lower()

    language_map = {
        "english": "en",
        "hindi": "hi",
        "arabic": "ar",
        "spanish": "es",
        "french": "fr",
        "german": "de",
        "chinese": "zh",
        "japanese": "ja",
        "russian": "ru",
        "italian": "it"
    }

    return language_map.get(language, "en")  # Default to English

