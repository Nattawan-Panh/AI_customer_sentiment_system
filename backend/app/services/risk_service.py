def calculate_risk(text: str, sentiment_label: str, intent_label: str) -> dict:
    text = str(text or "").lower()

    high_keywords = [
        "high_risk_complaint"
    ]

    medium_keywords = [
        "allergy",
        "complaint_product",
        "complaint_service",
        "refund_return",
    ]

    low_safe_intents = {
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
        "general_question",
    }

    if any(k in text for k in high_keywords):
        return {
            "level": "HIGH",
            "score": 90,
            "reason": "high_risk_keyword"
        }

    if any(k in text for k in medium_keywords):
        return {
            "level": "MEDIUM",
            "score": 60,
            "reason": "medium_risk_keyword"
        }

    if intent_label in low_safe_intents:
        return {
            "level": "LOW",
            "score": 10,
            "reason": "safe_intent"
        }

    if sentiment_label == "negative":
        return {
            "level": "MEDIUM",
            "score": 50,
            "reason": "negative_sentiment"
        }

    return {
        "level": "LOW",
        "score": 10,
        "reason": "default_low"
    }