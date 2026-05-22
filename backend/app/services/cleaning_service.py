import re

EMOJI_MAP = {
    # positive
    "😊": " positive_emoji ",
    "😄": " positive_emoji ",
    "😁": " positive_emoji ",
    "😍": " love_emoji ",
    "🥰": " love_emoji ",
    "❤️": " love_emoji ",
    "💕": " love_emoji ",
    "👍": " positive_emoji ",

    # negative
    "😡": " angry_emoji ",
    "🤬": " angry_emoji ",
    "😠": " angry_emoji ",
    "😭": " sad_emoji ",
    "😢": " sad_emoji ",
    "😞": " sad_emoji ",
    "👎": " negative_emoji ",

    # neutral / question
    "😐": " neutral_emoji ",
    "🤔": " question_emoji ",
    "❓": " question_emoji ",
    "❗": " alert_emoji ",
}

def replace_emoji(text: str) -> str:
    for emoji, meaning in EMOJI_MAP.items():
        text = text.replace(emoji, meaning)
        
    return text

def clean_text(text: str) -> str:
    text = str(text or "").strip()
    text = replace_emoji(text)
    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"[@#]", "", text)
    text = re.sub(r"(.)\1{3,}", r"\1\1", text)
    text = re.sub(r"[^\w\sก-๙.,!?_]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()