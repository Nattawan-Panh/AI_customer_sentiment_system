import json
from pathlib import Path
from functools import lru_cache
from typing import Any, Dict, List, Optional


BASE_DIR = Path(__file__).resolve().parents[2]
KNOWLEDGE_PATH = BASE_DIR / "data" / "sample_knowledge.json"


DEFAULT_KNOWLEDGE = {
    "title": "General Question",
    "answer": (
        "Pudding Petals Cafe เป็นคาเฟ่ขนมหวานบรรยากาศสวนดอกไม้ "
        "มีเค้ก ขนมหวาน เบเกอรี่ เครื่องดื่ม และพื้นที่นั่งทั้งโซน indoor และ outdoor ค่ะ"
    ),
    "keywords": [],
    "requires_human": False,
    "handoff_note": None
}


# ---------------------------------------------------------
# Intent aliases
# ใช้สำหรับรองรับชื่อ intent เก่าหรือชื่อที่ไฟล์อื่นอาจส่งมา
# โดยให้ map ไปยัง intent ที่มีอยู่จริงใน sample_knowledge.json
# ---------------------------------------------------------

KNOWLEDGE_ALIASES = {
    # general / fallback
    "general": "general_question",
    "unknown": "general_question",
    "fallback": "general_question",
    "other": "general_question",

    # old combined intent
    "sweetness_allergy": "sweetness_adjustment",

    # old knowledge names
    "cafe_facilities": "facility",
    "photo_spot": "ambience_photo_spot",
    "delivery_platform": "delivery_takeaway",
    "delivery_issue": "order_status",
    "order_problem": "complaint_product",
    "refund_exchange": "refund_return",
    "complaint": "complaint_service",
    "human_required": "high_risk_complaint",

    # complaint aliases
    "complaint_staff": "complaint_staff",
    "staff_complaint": "complaint_staff",
    "service_complaint": "complaint_service",
    "product_complaint": "complaint_product",

    # common wording variants
    "menu": "menu_inquiry",
    "price": "price_inquiry",
    "size": "size_option",
    "hours": "opening_hours",
    "open_hours": "opening_hours",
    "store_location": "location",
    "delivery": "delivery_takeaway",
    "takeaway": "delivery_takeaway",
    "ingredient": "ingredients",
    "ambience": "ambience_photo_spot",
    "photo": "ambience_photo_spot",
    "facilities": "facility",
}


# ---------------------------------------------------------
# Intent list aligned with intent_service.py
# ---------------------------------------------------------

SUPPORTED_INTENTS = {
    "greeting",
    "thanks",
    "general_question",
    "empty_message",
    "service_question",

    "promotion",
    "recommendation",
    "menu_inquiry",
    "price_inquiry",
    "size_option",
    "availability",

    "opening_hours",
    "location",
    "reservation",
    "delivery_takeaway",
    "payment",
    "order_status",

    "custom_cake",
    "special_occasion",
    "packaging",

    "sweetness_adjustment",
    "allergy",
    "ingredients",
    "dietary_option",

    "ambience_photo_spot",
    "facility",
    "compliment",

    "complaint_product",
    "complaint_service",
    "complaint_staff",
    "refund_return",
    "high_risk_complaint",
}


@lru_cache(maxsize=1)
def load_knowledge_base() -> dict:
    try:
        with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}
    except Exception:
        return {}


def normalize_intent_label(intent_label: Any, text: str = "") -> str:
    """
    รับ intent ได้ทั้ง str หรือ dict จาก intent_service.py
    เช่น:
    - "promotion"
    - {"label": "promotion"}
    - {"intent": "promotion"}
    - {"canonical_intent": "complaint_service"}
    - {"risk_intent": "complaint_service"}
    """
    if isinstance(intent_label, dict):
        raw_label = (
            intent_label.get("canonical_intent")
            or intent_label.get("intent")
            or intent_label.get("label")
            or intent_label.get("risk_intent")
            or "general_question"
        )
    else:
        raw_label = intent_label

    label = str(raw_label or "general_question").strip()

    if not label:
        label = "general_question"

    # กรณี intent เก่า sweetness_allergy ให้แยกตามข้อความ
    if label == "sweetness_allergy":
        text_lower = str(text or "").lower()
        allergy_words = [
            "แพ้",
            "แพ้อาหาร",
            "แพ้นม",
            "แพ้ไข่",
            "แพ้ถั่ว",
            "allergy",
            "allergic",
            "gluten",
            "lactose",
            "กินนมไม่ได้",
            "กินไข่ไม่ได้",
            "กินถั่วไม่ได้"
        ]

        if any(word in text_lower for word in allergy_words):
            return "allergy"

        return "sweetness_adjustment"

    label = KNOWLEDGE_ALIASES.get(label, label)

    if label not in SUPPORTED_INTENTS:
        return "general_question"

    return label


def _is_knowledge_item(value: Any) -> bool:
    return isinstance(value, dict) and "answer" in value


def get_store_info() -> dict:
    """
    รองรับไฟล์ JSON เก่า ถ้ายังมี STORE_INFO
    ถ้าใช้ JSON ใหม่แบบ top-level intent จะ return {}
    """
    kb = load_knowledge_base()
    return kb.get("STORE_INFO", {})


def get_delivery_info() -> dict:
    """
    รองรับไฟล์ JSON เก่า ถ้ายังมี DELIVERY_INFO
    ถ้าใช้ JSON ใหม่แบบ top-level intent จะ return {}
    """
    kb = load_knowledge_base()
    return kb.get("DELIVERY_INFO", {})


def get_menu_items() -> list:
    """
    รองรับไฟล์ JSON เก่า ถ้ายังมี MENU_ITEMS
    ถ้าใช้ JSON ใหม่แบบ top-level intent จะ return []
    """
    kb = load_knowledge_base()
    return kb.get("MENU_ITEMS", [])


def get_faq() -> dict:
    """
    รองรับ 2 รูปแบบ:
    1) JSON เก่า:
       {
         "FAQ": {
           "greeting": {"answer": "..."}
         }
       }

    2) JSON ใหม่:
       {
         "greeting": {"answer": "..."},
         "promotion": {"answer": "..."}
       }
    """
    kb = load_knowledge_base()

    if isinstance(kb.get("FAQ"), dict):
        return kb.get("FAQ", {})

    return {
        key: value
        for key, value in kb.items()
        if _is_knowledge_item(value)
    }


def get_faq_answer(intent_label: str, text: str = "") -> dict:
    faq = get_faq()
    normalized_intent = normalize_intent_label(intent_label, text)

    data = faq.get(normalized_intent)

    if not data:
        data = faq.get("general_question")

    if not data:
        data = faq.get("general")

    if not data:
        data = DEFAULT_KNOWLEDGE

    return {
        "title": data.get("title", normalized_intent),
        "answer": data.get("answer", ""),
        "keywords": data.get("keywords", []),
        "requires_human": data.get("requires_human", False),
        "handoff_note": data.get("handoff_note"),
        "intent": normalized_intent
    }


def get_available_menu_items(category: str = None) -> list:
    """
    ใช้ได้กับ JSON เก่าที่มี MENU_ITEMS
    ถ้าใช้ JSON ใหม่แบบ top-level intent จะ return []
    """
    menu_items = get_menu_items()

    results = [
        item for item in menu_items
        if item.get("available") is True
    ]

    if category:
        category = str(category or "").lower().strip()
        results = [
            item for item in results
            if item.get("category", "").lower() == category
        ]

    return results


def find_menu_by_keyword(keyword: str) -> list:
    """
    ใช้ค้นหาเมนูใน MENU_ITEMS ถ้าใช้โครงสร้าง JSON เก่า
    ถ้า JSON ใหม่ไม่มี MENU_ITEMS จะ return []
    """
    keyword = str(keyword or "").lower().strip()

    if not keyword:
        return []

    results = []

    for item in get_available_menu_items():
        searchable_text = " ".join([
            item.get("id", ""),
            item.get("name", ""),
            item.get("category", ""),
            item.get("description", ""),
            item.get("sweetness", ""),
            " ".join(item.get("tags", [])),
            " ".join(item.get("recommended_for", [])),
            " ".join(item.get("allergens", []))
        ]).lower()

        if keyword in searchable_text:
            results.append(item)

    return results


def get_human_required_intents() -> set:
    faq = get_faq()

    human_required = set()

    for intent, data in faq.items():
        if data.get("requires_human") is True:
            human_required.add(intent)

    return human_required


def is_human_required(intent_label: str, text: str = "") -> bool:
    faq_data = get_faq_answer(intent_label, text)
    return faq_data.get("requires_human") is True


def get_handoff_note(intent_label: str, text: str = ""):
    faq_data = get_faq_answer(intent_label, text)
    return faq_data.get("handoff_note")


def search_faq_by_keyword(text: str) -> dict:
    text = str(text or "").lower().strip()
    faq = get_faq()

    if not text:
        faq_data = get_faq_answer("general_question")
        return {
            "intent": "general_question",
            **faq_data
        }

    best_match = None
    best_score = 0

    for intent, data in faq.items():
        keywords = data.get("keywords", [])
        score = 0

        for keyword in keywords:
            keyword = str(keyword or "").lower().strip()

            if keyword and keyword in text:
                score += 1

        if score > best_score:
            best_score = score
            best_match = {
                "intent": normalize_intent_label(intent),
                "title": data.get("title", intent),
                "answer": data.get("answer", ""),
                "keywords": data.get("keywords", []),
                "requires_human": data.get("requires_human", False),
                "handoff_note": data.get("handoff_note")
            }

    if best_match:
        return best_match

    faq_data = get_faq_answer("general_question")

    return {
        "intent": "general_question",
        **faq_data
    }


def retrieve_knowledge(intent_label: str = "general_question", text: str = "") -> dict:
    """
    Retrieve knowledge for pipeline_service.py

    Returns:
    {
        "title": "...",
        "content": "...",
        "answer": "...",
        "matched": True,
        "intent": "...",
        "requires_human": False,
        "handoff_note": None,
        "keywords": []
    }
    """
    text = str(text or "").strip()
    normalized_intent = normalize_intent_label(intent_label, text)

    faq_data = get_faq_answer(normalized_intent, text)

    # ถ้าเป็น general_question แต่มีข้อความ ให้ลองหา intent จาก keyword ใน knowledge
    if normalized_intent == "general_question" and text:
        keyword_match = search_faq_by_keyword(text)

        if keyword_match.get("intent") != "general_question":
            normalized_intent = keyword_match.get("intent")
            faq_data = keyword_match

    content = faq_data.get("answer", "")

    return {
        "title": faq_data.get("title", normalized_intent),
        "content": content,
        "answer": content,
        "matched": True if content else False,
        "intent": normalized_intent,
        "label": normalized_intent,
        "canonical_intent": normalized_intent,
        "requires_human": faq_data.get("requires_human", False),
        "handoff_note": faq_data.get("handoff_note"),
        "keywords": faq_data.get("keywords", []),
        "source": "sample_knowledge_json"
    }


def reload_knowledge_base():
    load_knowledge_base.cache_clear()
    return load_knowledge_base()