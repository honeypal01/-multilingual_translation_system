# # translator_utils.py

# from langdetect import detect
# from googletrans import Translator
# from gtts import gTTS
# import io

# # Initialize the Google Translator
# translator = Translator()

# # Mapping of language names to ISO codes
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

# def detect_language(text):
#     """Detect the language code of a given text."""
#     return detect(text)

# def get_language_code(lang_name):
#     """Return ISO language code for a given language name."""
#     return LANGUAGE_CODES.get(lang_name, "en")

# def translate_text(text, src_lang, target_lang):
#     """Translate text from source to target language."""
#     try:
#         result = translator.translate(text, src=src_lang, dest=target_lang)
#         return result.text
#     except Exception as e:
#         return f"[Translation Error] {e}"

# def text_to_speech(text, lang="en"):
#     """Convert text to speech and return audio BytesIO."""
#     try:
#         tts = gTTS(text=text, lang=lang)
#         audio_fp = io.BytesIO()
#         tts.write_to_fp(audio_fp)
#         audio_fp.seek(0)
#         return audio_fp
#     except Exception as e:
#         return None

# def get_supported_languages():
#     """Return a sorted list of supported language names."""
#     return sorted(LANGUAGE_CODES.keys())


# translator.py

from langdetect import detect, LangDetectException
from googletrans import Translator
from gtts import gTTS
import io

translator = Translator()

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

def detect_language(text):
    """Detect the language code of a given text using langdetect."""
    try:
        lang_code = detect(text)
        return lang_code
    except LangDetectException:
        return "en"  # default to English if detection fails

def get_language_code(lang_name):
    """Return ISO language code for a given language name (case insensitive)."""
    for key in LANGUAGE_CODES:
        if key.lower() == lang_name.lower():
            return LANGUAGE_CODES[key]
    return "en"  # default fallback

def translate_text(text, src, dest):
    """Translate text from source to target language using googletrans."""
    try:
        result = translator.translate(text, src=src, dest=dest)
        return result.text
    except Exception as e:
        return f"[Translation Error] {e}"

def text_to_speech(text, lang="en"):
    """Convert text to speech and return audio as BytesIO object."""
    try:
        tts = gTTS(text=text, lang=lang)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    except Exception:
        return None

def get_supported_languages():
    """Return a sorted list of supported language names."""
    return sorted(LANGUAGE_CODES.keys())
