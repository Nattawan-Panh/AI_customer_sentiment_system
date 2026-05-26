def score_risk(text="", sentiment_label=None, intent_label=None, pre_safe=True):
    text = str(text or "").lower()
    sentiment_label = str(sentiment_label or "").lower()
    intent_label = str(intent_label or "").lower()

    score = 0
    reasons = []

    # -----------------------------
    # 1) Pre-safety check
    # -----------------------------
    if pre_safe is False:
        score += 40
        reasons.append("pre_safety_failed")

    # -----------------------------
    # 2) Sentiment score
    # -----------------------------
    if sentiment_label in ["negative", "neg"]:
        score += 25
        reasons.append("negative_sentiment")
    elif sentiment_label in ["neutral"]:
        score += 10
        reasons.append("neutral_sentiment")
    elif sentiment_label in ["positive", "pos"]:
        score += 0
        reasons.append("positive_sentiment")

    # -----------------------------
    # 3) Intent risk groups
    # -----------------------------
    high_risk_intents = [
        "high_risk_complaint",
        "human_required",
        "urgent",
        "legal_complaint",
        "safety_issue"
    ]

    medium_risk_intents = [
        "complaint",
        "complaint_product",
        "complaint_service",
        "refund_request",
        "refund_return",
        "cancel_order",
        "negative_feedback",
        "allergy"
    ]

    low_safe_intents = [
        "greeting",
        "thanks",
        "menu_inquiry",
        "recommendation",
        "promotion",
        "price_inquiry",
        "size_option",
        "availability",
        "opening_hours",
        "location",
        "reservation",
        "delivery_takeaway",
        "payment",
        "custom_cake",
        "special_occasion",
        "packaging",
        "sweetness_adjustment",
        "ingredients",
        "dietary_option",
        "ambience_photo_spot",
        "facility",
        "service_question",
        "compliment",
        "general_question"
    ]

    if intent_label in high_risk_intents:
        score += 40
        reasons.append(f"high_risk_intent:{intent_label}")

    elif intent_label in medium_risk_intents:
        score += 25
        reasons.append(f"medium_risk_intent:{intent_label}")

    elif intent_label in low_safe_intents:
        score += 0
        reasons.append(f"safe_intent:{intent_label}")

    else:
        score += 5
        reasons.append(f"unknown_intent:{intent_label}")

    # -----------------------------
    # 4) Keyword risk
    # -----------------------------
    high_risk_keywords = [
        "ฟ้อง",
        "แจ้งความ",
        "ร้องเรียน",
        "ไม่ปลอดภัย",
        "อาหารเสีย",
        "ของเสีย",
        "แพ้",
        "เข้าโรงพยาบาล",
        "ป่วย",
        "ท้องเสีย",
        "เป็นพิษ",
        "ขู่",
        "ประจาน",
        "รีวิวเสียหาย"
    ]

    medium_risk_keywords = [
        "คืนเงิน",
        "ขอเงินคืน",
        "ยกเลิก",
        "ไม่พอใจ",
        "แย่มาก",
        "โมโห",
        "เสียใจ",
        "รอนาน",
        "ไม่ได้รับของ",
        "พนักงานพูดจาไม่ดี",
        "พนักงานไม่สุภาพ",
        "บริการไม่ดี",
        "ของไม่ครบ",
        "ส่งผิด",
        "รสชาติไม่ดี",
        "ไม่อร่อย"
    ]

    matched_high_keywords = [kw for kw in high_risk_keywords if kw in text]
    matched_medium_keywords = [kw for kw in medium_risk_keywords if kw in text]

    if matched_high_keywords:
        score += min(len(matched_high_keywords) * 20, 40)
        reasons.append({
            "matched_high_keywords": matched_high_keywords
        })

    if matched_medium_keywords:
        score += min(len(matched_medium_keywords) * 10, 30)
        reasons.append({
            "matched_medium_keywords": matched_medium_keywords
        })

    # -----------------------------
    # 5) Extra rule: negative + complaint/refund/cancel
    # -----------------------------
    if (
        sentiment_label in ["negative", "neg"]
        and intent_label in medium_risk_intents
    ):
        score += 10
        reasons.append("negative_sentiment_with_risky_intent")

    # -----------------------------
    # 6) Limit max score
    # -----------------------------
    score = min(score, 100)

    # -----------------------------
    # 7) Risk level
    # -----------------------------
    if score >= 70:
        level = "HIGH"
    elif score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "score": score,
        "level": level,
        "reasons": reasons
    }