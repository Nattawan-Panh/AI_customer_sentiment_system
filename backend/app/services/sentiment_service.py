import os
import re

try:
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
except Exception:
    torch = None
    AutoTokenizer = None
    AutoModelForSequenceClassification = None


POSITIVE_WORDS = [
    "ดี",
    "ชอบ",
    "น่ารัก",
    "ประทับใจ",
    "เยี่ยม",
    "ส่งไว",
    "ถูกใจ",
    "อร่อย",
    "ละมุน",
    "บริการดี",
]

NEGATIVE_WORDS = [
    "แย่",
    "ช้า",
    "เสีย",
    "พัง",
    "ผิดหวัง",
    "โกง",
    "คืนเงิน",
    "ไม่โอเค",
    "ร้องเรียน",
    "บริการแย่",
]

STRONG_NEGATIVE_WORDS = [
    "โกง",
    "ฟ้อง",
    "ประจาน",
    "หลอก",
    "สคบ",
]

POSITIVE_EMOJIS = [
    "😍",
    "🥰",
    "❤️",
    "💖",
    "😊",
    "😋",
]

NEGATIVE_EMOJIS = [
    "😡",
    "😭",
    "😠",
    "💢",
    "👎",
]

NEGATION_WORDS = [
    "ไม่",
    "ไม่ได้",
    "ไม่ค่อย",
]

SENTIMENT_MODEL_NAME = os.getenv("SENTIMENT_MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

_sentiment_tokenizer = None
_sentiment_model = None
_sentiment_id2label = None


def load_sentiment_model():
    global _sentiment_tokenizer, _sentiment_model, _sentiment_id2label

    if not SENTIMENT_MODEL_NAME:
        return None, None

    if torch is None or AutoTokenizer is None or AutoModelForSequenceClassification is None:
        return None, None

    if _sentiment_tokenizer is not None and _sentiment_model is not None:
        return _sentiment_tokenizer, _sentiment_model

    try:
        _sentiment_tokenizer = AutoTokenizer.from_pretrained(
            SENTIMENT_MODEL_NAME,
            token=HF_TOKEN
        )

        _sentiment_model = AutoModelForSequenceClassification.from_pretrained(
            SENTIMENT_MODEL_NAME,
            token=HF_TOKEN
        )

        _sentiment_model.eval()
        _sentiment_id2label = _sentiment_model.config.id2label

        return _sentiment_tokenizer, _sentiment_model

    except Exception:
        _sentiment_tokenizer = None
        _sentiment_model = None
        _sentiment_id2label = None
        return None, None


def predict_sentiment_with_model(text: str):
    tokenizer, model = load_sentiment_model()

    if tokenizer is None or model is None:
        return None

    try:
        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        )

        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.softmax(outputs.logits, dim=-1)[0]
            pred_id = int(torch.argmax(probs).item())
            confidence = float(probs[pred_id].item())

        raw_label = str(_sentiment_id2label.get(pred_id, pred_id)).lower()

        label_map = {
            "label_0": "negative",
            "label_1": "neutral",
            "label_2": "positive",
            "0": "negative",
            "1": "neutral",
            "2": "positive",
            "neg": "negative",
            "negative": "negative",
            "neu": "neutral",
            "neutral": "neutral",
            "pos": "positive",
            "positive": "positive",
        }

        label = label_map.get(raw_label, raw_label)

        if label not in ["positive", "neutral", "negative"]:
            label = "neutral"

        return {
            "label": label,
            "confidence": round(confidence, 2),
            "score": 0,
            "positive_matches": [],
            "negative_matches": [],
            "model": SENTIMENT_MODEL_NAME
        }

    except Exception:
        return None


def normalize_text(text: str) -> str:
    text = str(text or "").lower()

    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    return text


def contains_negation(text: str, word: str) -> bool:
    return any(
        f"{neg}{word}" in text or f"{neg} {word}" in text
        for neg in NEGATION_WORDS
    )


def predict_sentiment(text):
    text = normalize_text(text)

    model_result = predict_sentiment_with_model(text)
    if model_result is not None:
        return model_result

    positive_matches = []
    negative_matches = []

    score = 0

    for word in POSITIVE_WORDS:
        if word in text:
            if contains_negation(text, word):
                negative_matches.append(f"not_{word}")
                score -= 1
            else:
                positive_matches.append(word)
                score += 1

    for word in NEGATIVE_WORDS:
        if word in text:
            negative_matches.append(word)
            score -= 1

    for word in STRONG_NEGATIVE_WORDS:
        if word in text:
            negative_matches.append(f"strong_{word}")
            score -= 2

    for emoji in POSITIVE_EMOJIS:
        if emoji in text:
            positive_matches.append(emoji)
            score += 1

    for emoji in NEGATIVE_EMOJIS:
        if emoji in text:
            negative_matches.append(emoji)
            score -= 1

    if score > 0:
        label = "positive"

        confidence = min(
            0.95,
            0.60 + (abs(score) * 0.08)
        )

    elif score < 0:
        label = "negative"

        confidence = min(
            0.97,
            0.62 + (abs(score) * 0.08)
        )

    else:
        label = "neutral"
        confidence = 0.70

    return {
        "label": label,
        "confidence": round(confidence, 2),
        "score": score,
        "positive_matches": positive_matches,
        "negative_matches": negative_matches,
        "model": "rule_fallback_wangchanberta_ready"
    }