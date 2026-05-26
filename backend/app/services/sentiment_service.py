import os
import re

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # On production, env vars usually come from Railway/Render directly.
    # If python-dotenv is not installed yet, do not crash the service.
    pass

try:
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
except Exception as import_error:
    torch = None
    AutoTokenizer = None
    AutoModelForSequenceClassification = None
    TRANSFORMERS_IMPORT_ERROR = str(import_error)
else:
    TRANSFORMERS_IMPORT_ERROR = None


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
    "สวย",
    "น่ากิน",
    "น่าทาน",
    "โอเค",
    "ดีมาก",
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
    "ไม่ดี",
    "รอนาน",
    "ไม่สุภาพ",
    "ไม่อร่อย",
    "ผิดเมนู",
]

STRONG_NEGATIVE_WORDS = [
    "โกง",
    "ฟ้อง",
    "ประจาน",
    "หลอก",
    "สคบ",
    "แจ้งความ",
    "อาหารเป็นพิษ",
    "เข้าโรงพยาบาล",
    "แพ้รุนแรง",
]

POSITIVE_EMOJIS = [
    "😍",
    "🥰",
    "❤️",
    "💖",
    "😊",
    "😋",
    "✨",
    "🌷",
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


# Keep the original variable names so other files that reference them will not break.
SENTIMENT_MODEL_NAME = os.getenv("SENTIMENT_MODEL_NAME", "").strip()
HF_TOKEN = os.getenv("HF_TOKEN", "").strip()
USE_MODEL = os.getenv("USE_MODEL", "true").strip().lower() in [
    "true",
    "1",
    "yes",
    "y",
    "on",
]

_sentiment_tokenizer = None
_sentiment_model = None
_sentiment_id2label = None
_sentiment_model_error = None
_sentiment_loaded_model_name = None


def _refresh_env_settings():
    """
    Read env vars at runtime, not only at import time.
    This fixes the case where .env is loaded after this service is imported.
    """
    global SENTIMENT_MODEL_NAME
    global HF_TOKEN
    global USE_MODEL

    SENTIMENT_MODEL_NAME = os.getenv("SENTIMENT_MODEL_NAME", "").strip()
    HF_TOKEN = os.getenv("HF_TOKEN", "").strip()
    USE_MODEL = os.getenv("USE_MODEL", "true").strip().lower() in [
        "true",
        "1",
        "yes",
        "y",
        "on",
    ]

    return SENTIMENT_MODEL_NAME, HF_TOKEN, USE_MODEL


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


def _get_hf_kwargs() -> dict:
    _, hf_token, _ = _refresh_env_settings()

    if hf_token:
        return {"token": hf_token}

    return {}


def _get_legacy_hf_kwargs() -> dict:
    _, hf_token, _ = _refresh_env_settings()

    if hf_token:
        return {"use_auth_token": hf_token}

    return {}


def _reset_model_cache(error_message=None):
    global _sentiment_tokenizer
    global _sentiment_model
    global _sentiment_id2label
    global _sentiment_model_error
    global _sentiment_loaded_model_name

    _sentiment_tokenizer = None
    _sentiment_model = None
    _sentiment_id2label = None
    _sentiment_loaded_model_name = None
    _sentiment_model_error = error_message


def load_sentiment_model():
    global _sentiment_tokenizer
    global _sentiment_model
    global _sentiment_id2label
    global _sentiment_model_error
    global _sentiment_loaded_model_name

    model_name, _, use_model = _refresh_env_settings()

    if not use_model:
        _sentiment_model_error = "USE_MODEL is false"
        return None, None

    if not model_name:
        _sentiment_model_error = "SENTIMENT_MODEL_NAME is missing"
        return None, None

    if torch is None or AutoTokenizer is None or AutoModelForSequenceClassification is None:
        _sentiment_model_error = (
            TRANSFORMERS_IMPORT_ERROR
            or "torch or transformers is not installed"
        )
        return None, None

    # Reuse model if it has already loaded successfully.
    # Reload only when SENTIMENT_MODEL_NAME has changed.
    if (
        _sentiment_tokenizer is not None
        and _sentiment_model is not None
        and _sentiment_loaded_model_name == model_name
    ):
        return _sentiment_tokenizer, _sentiment_model

    try:
        hf_kwargs = _get_hf_kwargs()

        _sentiment_tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            use_fast=False,
            **hf_kwargs
        )

        _sentiment_model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            **hf_kwargs
        )

        _sentiment_model.eval()
        _sentiment_id2label = _sentiment_model.config.id2label or {}
        _sentiment_loaded_model_name = model_name
        _sentiment_model_error = None

        print(f"[SENTIMENT MODEL] Loaded: {model_name}")
        return _sentiment_tokenizer, _sentiment_model

    except TypeError:
        # Compatibility for older transformers versions that use use_auth_token.
        try:
            auth_kwargs = _get_legacy_hf_kwargs()

            _sentiment_tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                use_fast=False,
                **auth_kwargs
            )

            _sentiment_model = AutoModelForSequenceClassification.from_pretrained(
                model_name,
                **auth_kwargs
            )

            _sentiment_model.eval()
            _sentiment_id2label = _sentiment_model.config.id2label or {}
            _sentiment_loaded_model_name = model_name
            _sentiment_model_error = None

            print(f"[SENTIMENT MODEL] Loaded: {model_name}")
            return _sentiment_tokenizer, _sentiment_model

        except Exception as exc:
            error_message = str(exc)
            _reset_model_cache(error_message)
            print(f"[SENTIMENT MODEL ERROR] {error_message}")
            return None, None

    except Exception as exc:
        error_message = str(exc)
        _reset_model_cache(error_message)
        print(f"[SENTIMENT MODEL ERROR] {error_message}")
        return None, None


def _map_sentiment_label(raw_label):
    raw_label = str(raw_label).strip().lower()

    label_map = {
        "label_0": "negative",
        "label_1": "neutral",
        "label_2": "positive",
        "0": "negative",
        "1": "neutral",
        "2": "positive",
        "neg": "negative",
        "negative": "negative",
        "negative_label": "negative",
        "neu": "neutral",
        "neutral": "neutral",
        "neutral_label": "neutral",
        "pos": "positive",
        "positive": "positive",
        "positive_label": "positive",
    }

    label = label_map.get(raw_label, raw_label)

    if label not in ["positive", "neutral", "negative"]:
        label = "neutral"

    return label


def predict_sentiment_with_model(text: str):
    global _sentiment_model_error

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

        raw_label = _sentiment_id2label.get(pred_id, pred_id)
        label = _map_sentiment_label(raw_label)
        model_name, _, _ = _refresh_env_settings()

        return {
            "label": label,
            "confidence": round(confidence, 2),
            "score": 0,
            "positive_matches": [],
            "negative_matches": [],
            "model": model_name,
            "fallback_used": False,
            "fallback_reason": None
        }

    except Exception as exc:
        _sentiment_model_error = str(exc)
        print(f"[SENTIMENT PREDICT ERROR] {_sentiment_model_error}")
        return None


def predict_sentiment_by_rules(text: str) -> dict:
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

    fallback_reason = _sentiment_model_error or "model_result_is_none"

    return {
        "label": label,
        "confidence": round(confidence, 2),
        "score": score,
        "positive_matches": positive_matches,
        "negative_matches": negative_matches,
        "model": "rule_based_fallback",
        "fallback_used": True,
        "fallback_reason": fallback_reason
    }


def predict_sentiment(text):
    text = normalize_text(text)

    model_result = predict_sentiment_with_model(text)

    if model_result is not None:
        return model_result

    return predict_sentiment_by_rules(text)


def analyze_sentiment(text):
    return predict_sentiment(text)


def get_sentiment(text):
    return predict_sentiment(text)


def get_sentiment_model_status():
    """
    Optional helper for debug/admin route.
    It does not force model loading; it only reports current cached state.
    """
    model_name, _, use_model = _refresh_env_settings()

    return {
        "use_model": use_model,
        "sentiment_model_name": model_name,
        "model_loaded": _sentiment_model is not None,
        "loaded_model_name": _sentiment_loaded_model_name,
        "fallback_reason": _sentiment_model_error,
        "transformers_import_error": TRANSFORMERS_IMPORT_ERROR,
    }
