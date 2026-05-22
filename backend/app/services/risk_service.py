HIGH_KEYWORDS = [
    "ฟ้อง",
    "สคบ",
    "โกง",
    "ประจาน",
    "คืนเงิน",
    "หลอก",
    "ร้องเรียน",
    "แจ้งความ",
    "เสียหายมาก",
    "บริการแย่มาก",
    "รับผิดชอบ",
]

MEDIUM_KEYWORDS = [
    "แย่",
    "ช้า",
    "เสีย",
    "พัง",
    "ผิดหวัง",
    "ไม่โอเค",
    "ไม่พอใจ",
    "ของไม่ครบ",
    "ได้ของผิด",
    "เค้กเละ",
    "ขนมหก",
    "ส่งช้า",
]

HIGH_RISK_INTENTS = {
    "refund_exchange",
    "complaint",
    "human_required",
}

MEDIUM_RISK_INTENTS = {
    "order_problem",
    "delivery_issue",
    "event_booking",
    "collaboration",
    "sweetness_allergy",
    "custom_cake",
    "reservation",
}


def score_risk(text, sentiment, intent, pre_safe):
    text = str(text or "").lower()
    sentiment = str(sentiment or "").lower()
    intent = str(intent or "").lower()

    score = 0
    reasons = []

    matched_high_keywords = [
        word for word in HIGH_KEYWORDS
        if word.lower() in text
    ]

    if matched_high_keywords:
        added_score = len(matched_high_keywords) * 3
        score += added_score
        reasons.append({
            "type": "high_keywords",
            "matched": matched_high_keywords,
            "score": added_score
        })

    matched_medium_keywords = [
        word for word in MEDIUM_KEYWORDS
        if word.lower() in text
    ]

    if matched_medium_keywords:
        added_score = len(matched_medium_keywords) * 1
        score += added_score
        reasons.append({
            "type": "medium_keywords",
            "matched": matched_medium_keywords,
            "score": added_score
        })

    if sentiment == "negative":
        score += 2
        reasons.append({
            "type": "negative_sentiment",
            "score": 2
        })

    if intent in HIGH_RISK_INTENTS:
        score += 3
        reasons.append({
            "type": "high_risk_intent",
            "intent": intent,
            "score": 3
        })

    elif intent in MEDIUM_RISK_INTENTS:
        score += 2
        reasons.append({
            "type": "medium_risk_intent",
            "intent": intent,
            "score": 2
        })

    if pre_safe is False:
        score += 4
        reasons.append({
            "type": "pre_safety_failed",
            "score": 4
        })

    if score >= 5:
        level = "HIGH"
    elif score >= 2:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "level": level,
        "score": score,
        "reasons": reasons
    }