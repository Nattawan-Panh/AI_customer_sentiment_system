import re
import hashlib


SPAM_KEYWORDS = [
    "ฝากร้าน",
    "กดลิงก์",
    "รับเครดิตฟรี",
    "สมัครเว็บ",
    "ทักไลน์",
    "โปรสล็อต",
    "บาคาร่า",
    "พนัน",
    "คาสิโน",
]

SPAM_URL_PATTERNS = [
    r"http[s]?://",
    r"www\.",
    r"bit\.ly",
    r"lin\.ee",
    r"tinyurl",
]

SPAM_EMOJIS = [
    "💸",
    "🎰",
    "🔥",
]


def normalize_text(text: str) -> str:
    text = str(text or "").lower()

    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    return text


def is_spam(text):
    text = normalize_text(text)

    spam_score = 0
    matched = []

    for keyword in SPAM_KEYWORDS:
        if keyword in text:
            spam_score += 2
            matched.append(keyword)

    for pattern in SPAM_URL_PATTERNS:
        if re.search(pattern, text):
            spam_score += 3
            matched.append(pattern)

    repeated_chars = re.findall(r"(.)\1{4,}", text)

    if repeated_chars:
        spam_score += 1
        matched.extend(repeated_chars)

    for emoji in SPAM_EMOJIS:
        if emoji in text:
            spam_score += 1
            matched.append(emoji)

    is_spam_result = spam_score >= 3

    return {
        "is_spam": is_spam_result,
        "score": spam_score,
        "matched": matched
    }


def duplicate_key(text):
    normalized = normalize_text(text)

    return hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()