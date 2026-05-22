import re


PRE_UNSAFE_RULES = [
    {
        "pattern": r"ฆ่า|ระเบิด|ทำร้าย",
        "category": "violence",
        "severity": "high"
    },
    {
        "pattern": r"เลขบัตรประชาชน|บัตรประชาชน",
        "category": "privacy",
        "severity": "high"
    },
    {
        "pattern": r"ข้อมูลบัตร|บัตรเครดิต|cvv|otp",
        "category": "financial",
        "severity": "critical"
    },
]


POST_UNSAFE_RULES = [
    {
        "pattern": r"รับประกันคืนเงินทันที",
        "category": "overpromise",
        "severity": "high"
    },
    {
        "pattern": r"จะชนะคดีแน่นอน",
        "category": "legal_claim",
        "severity": "critical"
    },
    {
        "pattern": r"ส่งข้อมูลบัตร|เลขบัตรเครดิต|cvv|otp",
        "category": "financial_request",
        "severity": "critical"
    },
    {
        "pattern": r"แจ้งรหัสผ่าน|ส่งรหัสผ่าน",
        "category": "credential_request",
        "severity": "critical"
    },
]


THAI_ID_CARD_REGEX = r"\b\d{13}\b"
CREDIT_CARD_REGEX = r"\b(?:\d[ -]*?){13,16}\b"


def normalize_text(text: str) -> str:
    text = str(text or "").lower()

    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    return text


def _run_safety_rules(text: str, rules: list):
    text = normalize_text(text)

    matches = []

    for rule in rules:
        pattern = rule.get("pattern", "")

        if re.search(pattern, text, re.IGNORECASE):
            matches.append({
                "pattern": pattern,
                "category": rule.get("category"),
                "severity": rule.get("severity")
            })

    return matches


def pre_safety_check(text: str):
    text = normalize_text(text)

    matches = _run_safety_rules(
        text,
        PRE_UNSAFE_RULES
    )

    if re.search(THAI_ID_CARD_REGEX, text):
        matches.append({
            "pattern": "thai_id_card",
            "category": "privacy",
            "severity": "critical"
        })

    if re.search(CREDIT_CARD_REGEX, text):
        matches.append({
            "pattern": "credit_card",
            "category": "financial",
            "severity": "critical"
        })

    return {
        "safe": len(matches) == 0,
        "matches": matches
    }


def post_safety_check(reply: str):
    reply = normalize_text(reply)

    matches = _run_safety_rules(
        reply,
        POST_UNSAFE_RULES
    )

    return {
        "safe": len(matches) == 0,
        "matches": matches
    }