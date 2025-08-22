from transformers import pipeline
from langdetect import detect
from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor
import nltk

# Ensure punkt tokenizer is downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

from nltk.tokenize import sent_tokenize

summarizer = pipeline("summarization", model="t5-small")

# Mapping of langdetect codes to deep_translator supported codes
LANG_MAP = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'as': 'assamese',
    'ay': 'aymara',
    'az': 'azerbaijani',
    'bm': 'bambara',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bho': 'bhojpuri',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',   # <--- add lowercase form
    'zh-CN': 'chinese (simplified)',   # <--- add uppercase form
    'zh-tw': 'chinese (traditional)',
    'zh-TW': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'dv': 'dhivehi',
    'doi': 'dogri',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'ee': 'ewe',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gn': 'guarani',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurmanji',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar',
    'ne': 'nepali',
    'no': 'norwegian',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'tt': 'tatar',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'tk': 'turkmen',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu'
}

def chunk_text(text, max_tokens=400):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""
    current_length = 0
    for sentence in sentences:
        sentence_length = len(sentence.split())
        if current_length + sentence_length <= max_tokens:
            current_chunk += " " + sentence
            current_length += sentence_length
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
            current_length = sentence_length
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def summarize_chunk(chunk, max_length, min_length):
    summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

def summarize_text(text, max_length=130, min_length=30):
    if not text.strip():
        return "⚠️ Empty input provided. Please paste some text to summarize."
    try:
        detected_lang = detect(text)
        original_lang = detected_lang

        # Map detected language to supported code or fallback to English
        source_lang = LANG_MAP.get(detected_lang.lower(), None)
        if source_lang is None:
            return f"❌ Unsupported language detected: {detected_lang}"

        if source_lang != 'english':
            text = GoogleTranslator(source=source_lang, target='english').translate(text)

        chunks = chunk_text(text, max_tokens=400)
        with ThreadPoolExecutor() as executor:
            summaries = list(executor.map(lambda c: summarize_chunk(c, max_length, min_length), chunks))

        summary_text = "\n".join(summaries)

        if source_lang != 'english':
            summary_text = GoogleTranslator(source='english', target=source_lang).translate(summary_text)
            return f"🌐 Auto-translated from {source_lang.upper()} → EN → {source_lang.upper()}:\n\n" + summary_text

        return summary_text

    except Exception as e:
        return f"❌ Error during summarization: {str(e)}"
