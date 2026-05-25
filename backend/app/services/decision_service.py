import os

HUMAN_REQUIRED_INTENTS = {
    "refund_exchange",
    "order_problem",
    "complaint",
    "collaboration",
    "event_booking",
    "human_required",
    "negative_feedback",
    "price_negotiation",
}

SAFE_AUTO_REPLY_INTENTS = {
    "greeting",
    "menu_inquiry",
    "price_inquiry",
    "recommendation",
    "opening_hours",
    "location",
    "compliment",
    "general_question"
}

def should_auto_send(
    risk_level,
    sentiment_confidence,
    intent_confidence,
    post_safe,
    status,
    intent_label=None
):
    risk_level = str(risk_level or "").upper()
    status = str(status or "").lower()
    intent_label = str(intent_label or "").lower()

    sentiment_confidence = float(sentiment_confidence or 0)
    intent_confidence = float(intent_confidence or 0)

    auto_send_enabled = os.getenv("AUTO_SEND_LOW_RISK", "true").lower() == "true"

    if not auto_send_enabled:
        return {
            "auto_send": False,
            "reason": "auto_send_disabled"
        }

    if status == "spam":
        return {
            "auto_send": False,
            "reason": "spam_detected"
        }

    if not post_safe:
        return {
            "auto_send": False,
            "reason": "post_safety_failed"
        }

    if intent_label in HUMAN_REQUIRED_INTENTS:
        return {
            "auto_send": False,
            "reason": f"human_required_intent_{intent_label}"
        }

    if risk_level == "LOW" and intent_label in SAFE_AUTO_REPLY_INTENTS:
        return {
            "auto_send": True,
            "reason": f"safe_auto_reply_intent_{intent_label}"
        }

    sentiment_threshold = float(
        os.getenv("SENTIMENT_CONFIDENCE_THRESHOLD", "0.65")
    )
    intent_threshold = float(
        os.getenv("INTENT_CONFIDENCE_THRESHOLD", "0.60")
    )

    if sentiment_confidence < sentiment_threshold:
        return {
            "auto_send": False,
            "reason": "low_sentiment_confidence"
        }

    if intent_confidence < intent_threshold:
        return {
            "auto_send": False,
            "reason": "low_intent_confidence"
        }

    return {
        "auto_send": True,
        "reason": "low_risk_high_confidence_safe"
    }