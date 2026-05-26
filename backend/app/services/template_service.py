import os
import json
from pathlib import Path
from functools import lru_cache
from typing import Any, Dict, List, Optional


# =========================================================
# PATH CONFIG
# คงชื่อตัวแปรเดิม เพื่อให้ไฟล์อื่นที่ import อยู่ไม่พัง
# =========================================================

APP_DIR = Path(__file__).resolve().parents[1]
BASE_DIR = Path(__file__).resolve().parents[2]
KNOWLEDGE_PATH = BASE_DIR / "data" / "sample_knowledge.json"


# =========================================================
# DEFAULT KNOWLEDGE
# ใช้เป็น fallback กรณีไม่พบไฟล์ JSON / ไม่พบ intent
# =========================================================

DEFAULT_KNOWLEDGE = {
    "title": "General Question",
    "answer": (
        "Pudding Petals Cafe เป็นคาเฟ่ขนมหวานบรรยากาศสวนดอกไม้ "
        "มีเค้ก ขนมหวาน เบเกอรี่ เครื่องดื่ม และพื้นที่นั่งทั้งโซน indoor และ outdoor ค่ะ 🌷"
    ),
    "keywords": [],
    "examples": [],
    "requires_human": False,
    "handoff_note": None,
    "category": "general"
}


# =========================================================
# INTENT ALIASES
# รองรับชื่อ intent เก่า / ชื่อจากโมเดล / ชื่อจาก rule base
# =========================================================

KNOWLEDGE_ALIASES = {
    # general / fallback
    "general": "general_question",
    "unknown": "general_question",
    "fallback": "general_question",
    "other": "general_question",
    "none": "general_question",
    "null": "general_question",

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
    "negative_feedback": "complaint_service",

    # menu aliases
    "menu": "menu_inquiry",
    "ask_menu": "menu_inquiry",
    "menu_question": "menu_inquiry",
    "product_question": "menu_inquiry",
    "menu_detail": "menu_inquiry",
    "product_detail": "menu_inquiry",
    "taste": "menu_inquiry",
    "flavor": "menu_inquiry",

    "price": "price_inquiry",
    "ask_price": "price_inquiry",

    "size": "size_option",
    "sizes": "size_option",

    "ingredient": "ingredients",
    "allergens": "allergy",

    # recommendation aliases
    "drink_recommendation": "recommendation",
    "menu_recommendation": "recommendation",
    "ask_recommendation": "recommendation",
    "recommended_menu": "recommendation",
    "best_seller": "recommendation",
    "signature_menu": "recommendation",
    "recommend": "recommendation",

    # store aliases
    "hours": "opening_hours",
    "open_hours": "opening_hours",
    "business_hours": "opening_hours",
    "store_location": "location",
    "map": "location",
    "ambience": "ambience_photo_spot",
    "photo": "ambience_photo_spot",
    "facilities": "facility",

    # order / service aliases
    "delivery": "delivery_takeaway",
    "takeaway": "delivery_takeaway",
    "payment_method": "payment",
    "pay": "payment",

    # booking / occasion
    "booking": "reservation",
    "table_booking": "reservation",
    "custom_order": "custom_cake",
    "birthday_cake": "custom_cake",

    # support / risk
    "refund": "refund_return",
    "return": "refund_return",
    "cancel_order": "refund_return",
    "urgent": "high_risk_complaint",
    "legal_threat": "high_risk_complaint",
    "food_poisoning": "high_risk_complaint",

    # optional / extra intents
    "collab": "collaboration",
    "influencer": "collaboration",
    "event": "event_booking",
    "private_event": "event_booking",
    "social": "social_media",
    "queue": "queue_waiting",
    "waiting": "queue_waiting",
    "parking": "facility",
    "work": "work_study",
    "study": "work_study"
}


# =========================================================
# SUPPORTED INTENTS
# อ้างอิง intent หลักของระบบ
# =========================================================

SUPPORTED_INTENTS = {
    # 1. general
    "greeting",
    "thanks",
    "general_question",
    "empty_message",
    "service_question",

    # 2. menu / price / promotion
    "promotion",
    "recommendation",
    "menu_inquiry",
    "price_inquiry",
    "size_option",
    "availability",

    # 3. store info
    "opening_hours",
    "location",
    "reservation",
    "ambience_photo_spot",
    "facility",

    # 4. ordering / service
    "delivery_takeaway",
    "payment",
    "order_status",

    # 5. special occasion
    "custom_cake",
    "special_occasion",
    "packaging",

    # 6. sweetness / ingredient / dietary
    "sweetness_adjustment",
    "allergy",
    "ingredients",
    "dietary_option",

    # 7. customer emotion / review
    "compliment",

    "complaint_product",
    "complaint_service",
    "complaint_staff",
    "refund_return",
    "high_risk_complaint",

    # extra intents
    "collaboration",
    "event_booking",
    "social_media",
    "queue_waiting",
    "weather_outdoor",
    "work_study"
}


# =========================================================
# FILE LOADER
# รองรับหลาย path เพื่อกันปัญหาตอนรัน local / deploy
# =========================================================

def _candidate_knowledge_paths() -> List[Path]:
    env_path = os.getenv("KNOWLEDGE_BASE_PATH", "").strip()

    paths: List[Path] = []

    if env_path:
        paths.append(Path(env_path))

    paths.extend([
        # path หลักของโปรเจกต์
        KNOWLEDGE_PATH,
        BASE_DIR / "data" / "sample_knowledge.json",
        APP_DIR / "data" / "sample_knowledge.json",

        # เผื่อตอนรันจาก root project / backend
        Path.cwd() / "data" / "sample_knowledge.json",
        Path.cwd() / "backend" / "data" / "sample_knowledge.json",
        Path.cwd() / "backend" / "app" / "data" / "sample_knowledge.json",
        Path.cwd() / "app" / "data" / "sample_knowledge.json",

        # เผื่อใช้โฟลเดอร์ knowledge
        BASE_DIR / "knowledge" / "sample_knowledge.json",
        APP_DIR / "knowledge" / "sample_knowledge.json",
        Path.cwd() / "knowledge" / "sample_knowledge.json",
        Path.cwd() / "backend" / "knowledge" / "sample_knowledge.json",
    ])

    # ลบ path ซ้ำ แต่ยังคงลำดับเดิม
    unique_paths = []
    seen = set()

    for path in paths:
        key = str(path)
        if key not in seen:
            unique_paths.append(path)
            seen.add(key)

    return unique_paths


@lru_cache(maxsize=1)
def load_knowledge_base() -> dict:
    """
    โหลดไฟล์ knowledge base จาก JSON

    รองรับ:
    - sample_knowledge.json
    - path จาก env: KNOWLEDGE_BASE_PATH
    """
    for path in _candidate_knowledge_paths():
        try:
            if path.exists() and path.is_file():
                with open(path, "r", encoding="utf-8") as file:
                    data = json.load(file)

                if isinstance(data, dict):
                    return data
        except FileNotFoundError:
            continue
        except json.JSONDecodeError:
            continue
        except Exception:
            continue

    return {}


def reload_knowledge_base():
    """
    ใช้ reload knowledge base หลังแก้ไฟล์ JSON
    """
    load_knowledge_base.cache_clear()
    return load_knowledge_base()


def clear_knowledge_cache():
    """
    alias เพิ่มเติม เผื่อไฟล์อื่นเรียกใช้
    """
    load_knowledge_base.cache_clear()


def get_knowledge_debug_status() -> dict:
    """
    ใช้ debug ว่าระบบโหลด sample_knowledge.json ได้จริงหรือไม่
    """
    paths = _candidate_knowledge_paths()
    found_paths = []

    for path in paths:
        try:
            if path.exists() and path.is_file():
                found_paths.append(str(path))
        except Exception:
            pass

    kb = load_knowledge_base()
    menu_catalog = kb.get("menu_catalog", {}) if isinstance(kb, dict) else {}
    items = menu_catalog.get("items", []) if isinstance(menu_catalog, dict) else []

    return {
        "loaded": bool(kb),
        "found_paths": found_paths,
        "top_level_keys": list(kb.keys()) if isinstance(kb, dict) else [],
        "has_intents": isinstance(kb.get("intents"), dict) if isinstance(kb, dict) else False,
        "has_extra_intents": isinstance(kb.get("extra_intents"), dict) if isinstance(kb, dict) else False,
        "has_menu_catalog": isinstance(menu_catalog, dict),
        "menu_count": len(items) if isinstance(items, list) else 0,
    }


# =========================================================
# BASIC HELPERS
# =========================================================

def _safe_str(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value).strip()


def _first_existing(data: Dict[str, Any], keys: List[str], default=None):
    if not isinstance(data, dict):
        return default

    for key in keys:
        if key in data:
            return data.get(key)

    return default


def _as_list(value: Any) -> List[str]:
    if value is None:
        return []

    if isinstance(value, list):
        return [
            str(item).strip()
            for item in value
            if str(item or "").strip()
        ]

    if isinstance(value, str):
        value = value.strip()
        return [value] if value else []

    return []


def _list_to_text(value: Any, separator: str = ", ") -> str:
    items = _as_list(value)
    return separator.join(items)


def _is_true(value: Any) -> bool:
    return value is True or str(value).strip().lower() in {"true", "1", "yes", "y"}


def _is_knowledge_item(value: Any) -> bool:
    return isinstance(value, dict) and (
        "answer" in value
        or "reply" in value
        or "response" in value
        or "template" in value
        or "message" in value
        or "content" in value
        or "default_response" in value
        or "response_templates" in value
    )


def _format_bool_available(value: Any) -> str:
    return "มีให้บริการ" if _is_true(value) else "ไม่มีให้บริการ"


def _shorten(text: str, max_len: int = 1200) -> str:
    text = _safe_str(text)
    if len(text) <= max_len:
        return text
    return text[: max_len - 20].rstrip() + "...เพิ่มเติมค่ะ"


# =========================================================
# SAMPLE KNOWLEDGE STRUCTURE ACCESSORS
# =========================================================

def get_metadata() -> dict:
    kb = load_knowledge_base()
    metadata = kb.get("metadata", {})
    return metadata if isinstance(metadata, dict) else {}


def get_brand_profile() -> dict:
    kb = load_knowledge_base()
    brand_profile = kb.get("brand_profile", {})
    return brand_profile if isinstance(brand_profile, dict) else {}


def get_store_info() -> dict:
    kb = load_knowledge_base()

    store_info = _first_existing(
        kb,
        ["STORE_INFO", "store_info", "store", "STORE"],
        {}
    )

    return store_info if isinstance(store_info, dict) else {}


def get_delivery_info() -> dict:
    kb = load_knowledge_base()

    delivery_info = _first_existing(
        kb,
        ["DELIVERY_INFO", "delivery_info", "delivery", "DELIVERY"],
        {}
    )

    return delivery_info if isinstance(delivery_info, dict) else {}


def get_menu_catalog() -> dict:
    kb = load_knowledge_base()
    menu_catalog = kb.get("menu_catalog", {})
    return menu_catalog if isinstance(menu_catalog, dict) else {}


def get_menu_items() -> list:
    kb = load_knowledge_base()

    # schema จริงของ sample_knowledge.json
    menu_catalog = kb.get("menu_catalog")
    if isinstance(menu_catalog, dict):
        items = menu_catalog.get("items")
        if isinstance(items, list):
            return items

    # fallback เผื่อใช้ schema เก่า
    menu_items = _first_existing(
        kb,
        ["MENU_ITEMS", "menu_items", "menus", "MENU", "menu"],
        []
    )

    return menu_items if isinstance(menu_items, list) else []


def get_recommendation_rules() -> dict:
    kb = load_knowledge_base()
    rules = kb.get("recommendation_rules", {})
    return rules if isinstance(rules, dict) else {}


def get_packaging_options() -> dict:
    kb = load_knowledge_base()
    options = kb.get("packaging_options", {})
    return options if isinstance(options, dict) else {}


def get_policies() -> dict:
    kb = load_knowledge_base()

    policies = _first_existing(
        kb,
        ["POLICIES", "policies", "policy", "POLICY"],
        {}
    )

    return policies if isinstance(policies, dict) else {}


def get_slot_schema() -> dict:
    kb = load_knowledge_base()
    slots = kb.get("slot_schema", {})
    return slots if isinstance(slots, dict) else {}


def get_response_generation_rules() -> dict:
    kb = load_knowledge_base()
    rules = kb.get("response_generation_rules", {})
    return rules if isinstance(rules, dict) else {}


def get_risk_scoring_rules() -> dict:
    kb = load_knowledge_base()
    rules = kb.get("risk_scoring_rules", {})
    return rules if isinstance(rules, dict) else {}


def get_response_templates() -> dict:
    kb = load_knowledge_base()

    templates = _first_existing(
        kb,
        [
            "RESPONSE_TEMPLATES",
            "response_templates",
            "templates",
            "TEMPLATES"
        ],
        {}
    )

    return templates if isinstance(templates, dict) else {}


def get_intent_priority_list() -> list:
    kb = load_knowledge_base()

    priority = _first_existing(
        kb,
        ["INTENT_PRIORITY", "intent_priority", "priority"],
        []
    )

    return priority if isinstance(priority, list) else []


# =========================================================
# INTENT / FAQ HELPERS
# =========================================================

def extract_intent_answer(intent_data: dict) -> str:
    """
    ดึงคำตอบจาก intent ใน sample_knowledge.json
    รองรับ:
    - default_response
    - response_templates
    - answer/content/reply/response/template/message
    """

    if not isinstance(intent_data, dict):
        return ""

    for key in [
        "answer",
        "content",
        "default_response",
        "reply",
        "response",
        "template",
        "message"
    ]:
        value = intent_data.get(key)

        if isinstance(value, str) and value.strip():
            return value.strip()

        if isinstance(value, list) and value:
            first = value[0]
            if isinstance(first, str) and first.strip():
                return first.strip()

    templates = intent_data.get("response_templates")
    if isinstance(templates, list) and templates:
        first_template = templates[0]
        if isinstance(first_template, str) and first_template.strip():
            return first_template.strip()

    return ""


def _extract_answer(data: Dict[str, Any]) -> str:
    return extract_intent_answer(data)


def _extract_requires_human(data: Dict[str, Any]) -> bool:
    if not isinstance(data, dict):
        return False

    if "requires_human" in data:
        return bool(data.get("requires_human"))

    if "requires_human_default" in data:
        return bool(data.get("requires_human_default"))

    if "human_required" in data:
        return bool(data.get("human_required"))

    handoff = data.get("handoff")
    if isinstance(handoff, dict):
        return bool(handoff.get("required", False))

    return False


def _extract_handoff_note(data: Dict[str, Any]) -> Optional[str]:
    if not isinstance(data, dict):
        return None

    handoff = data.get("handoff")
    if isinstance(handoff, dict):
        message = _safe_str(handoff.get("handoff_message"))
        if message:
            return message

    note = (
        data.get("handoff_note")
        or data.get("admin_note")
        or data.get("escalation_note")
    )

    note = _safe_str(note)

    return note or None


def _extract_handoff_when(data: Dict[str, Any]) -> List[str]:
    if not isinstance(data, dict):
        return []

    handoff = data.get("handoff")
    if isinstance(handoff, dict):
        return _as_list(handoff.get("when"))

    return []


def _extract_category(data: Dict[str, Any], default: str = "general") -> str:
    if not isinstance(data, dict):
        return default

    category = (
        data.get("category")
        or data.get("group")
        or default
    )

    category = _safe_str(category, default)

    return category or default


def _extract_keywords(data: Dict[str, Any]) -> List[str]:
    if not isinstance(data, dict):
        return []

    keywords = (
        data.get("keywords")
        or data.get("keyword")
        or []
    )

    return _as_list(keywords)


def _extract_examples(data: Dict[str, Any]) -> List[str]:
    if not isinstance(data, dict):
        return []

    examples = (
        data.get("examples")
        or data.get("sample_questions")
        or data.get("customer_examples")
        or data.get("utterances")
        or []
    )

    return _as_list(examples)


def _extract_follow_up_prompts(data: Dict[str, Any]) -> List[str]:
    if not isinstance(data, dict):
        return []
    return _as_list(data.get("follow_up_prompts"))


def _extract_related_kb(data: Dict[str, Any]) -> List[str]:
    if not isinstance(data, dict):
        return []
    return _as_list(data.get("related_kb"))


def _normalize_knowledge_item(intent: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    แปลงข้อมูล intent จาก JSON ให้เป็นรูปแบบกลางของระบบ
    """
    if not isinstance(data, dict):
        data = {}

    title = (
        data.get("title")
        or data.get("display_name")
        or data.get("name")
        or intent
    )

    answer = _extract_answer(data)

    return {
        "title": title,
        "answer": answer,
        "content": answer,
        "keywords": _extract_keywords(data),
        "examples": _extract_examples(data),
        "requires_human": _extract_requires_human(data),
        "handoff_note": _extract_handoff_note(data),
        "handoff_when": _extract_handoff_when(data),
        "category": _extract_category(data),
        "intent": intent,
        "label": intent,
        "canonical_intent": intent,
        "follow_up_prompts": _extract_follow_up_prompts(data),
        "related_kb": _extract_related_kb(data),
        "risk_level": data.get("risk_level"),
        "auto_reply_allowed": data.get("auto_reply_allowed"),
        "required_slots": _as_list(data.get("required_slots")),
    }


def _faq_from_list(items: list) -> dict:
    faq = {}

    for item in items:
        if not isinstance(item, dict):
            continue

        intent = (
            item.get("intent")
            or item.get("canonical_intent")
            or item.get("label")
            or item.get("name")
        )

        intent = normalize_intent_label(intent)

        if intent:
            faq[intent] = item

    return faq


def get_faq() -> dict:
    """
    รองรับหลายรูปแบบ JSON:

    1) แบบเก่า:
       {"FAQ": {"greeting": {"answer": "..."}}}

    2) แบบใหม่:
       {"INTENTS": {"greeting": {"answer": "..."}}}

    3) แบบ sample_knowledge.json:
       {"intents": {...}, "extra_intents": {...}}

    4) แบบ list:
       {"intents": [{"intent": "greeting", "answer": "..."}]}

    5) แบบ top-level:
       {"greeting": {"answer": "..."}}
    """
    kb = load_knowledge_base()

    faq: Dict[str, Any] = {}

    # schema หลักของ sample_knowledge.json
    intents = kb.get("intents")
    if isinstance(intents, dict):
        faq.update(intents)
    elif isinstance(intents, list):
        faq.update(_faq_from_list(intents))

    extra_intents = kb.get("extra_intents")
    if isinstance(extra_intents, dict):
        faq.update(extra_intents)
    elif isinstance(extra_intents, list):
        faq.update(_faq_from_list(extra_intents))

    if faq:
        return faq

    possible_keys = [
        "FAQ",
        "faq",
        "INTENTS",
        "INTENTS_KB",
        "INTENT_KB",
        "intent_kb",
        "INTENT_KNOWLEDGE",
        "intent_knowledge"
    ]

    for key in possible_keys:
        value = kb.get(key)

        if isinstance(value, dict):
            return value

        if isinstance(value, list):
            return _faq_from_list(value)

    return {
        key: value
        for key, value in kb.items()
        if _is_knowledge_item(value)
    }


def _get_aliases_from_kb() -> Dict[str, str]:
    kb = load_knowledge_base()
    aliases = kb.get("intent_aliases", {})
    if not isinstance(aliases, dict):
        return {}

    return {
        _safe_str(key).lower(): _safe_str(value).lower()
        for key, value in aliases.items()
        if _safe_str(key) and _safe_str(value)
    }


def _intent_exists_in_faq(intent: str) -> bool:
    faq = get_faq()
    return intent in faq


def normalize_intent_label(intent_label: Any, text: str = "") -> str:
    """
    รับ intent ได้ทั้ง str หรือ dict จาก intent_service.py

    ตัวอย่าง:
    - "promotion"
    - {"label": "promotion"}
    - {"intent": "promotion"}
    - {"canonical_intent": "complaint_service"}
    - {"risk_intent": "high_risk_complaint"}
    """
    if isinstance(intent_label, dict):
        raw_label = (
            intent_label.get("canonical_intent")
            or intent_label.get("intent")
            or intent_label.get("label")
            or intent_label.get("risk_intent")
            or intent_label.get("predicted_intent")
            or "general_question"
        )
    else:
        raw_label = intent_label

    label = _safe_str(raw_label, "general_question").lower()

    if not label:
        label = "general_question"

    # กรณี intent เก่า sweetness_allergy ให้แยกจากข้อความ
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
            "dairy",
            "nut",
            "peanut",
            "กินนมไม่ได้",
            "กินไข่ไม่ได้",
            "กินถั่วไม่ได้",
            "แพ้กลูเตน"
        ]

        if any(word in text_lower for word in allergy_words):
            return "allergy"

        return "sweetness_adjustment"

    # aliases จากไฟล์ JSON มาก่อน แล้วค่อยตามด้วย aliases ในโค้ด
    kb_aliases = _get_aliases_from_kb()
    label = kb_aliases.get(label, KNOWLEDGE_ALIASES.get(label, label))

    if label in SUPPORTED_INTENTS:
        return label

    try:
        if _intent_exists_in_faq(label):
            return label
    except Exception:
        pass

    return "general_question"


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

    return _normalize_knowledge_item(normalized_intent, data)


# =========================================================
# MENU FUNCTIONS
# =========================================================

def get_menu_name(item: dict) -> str:
    if not isinstance(item, dict):
        return "เมนู"

    return (
        item.get("name_th")
        or item.get("name_en")
        or item.get("name")
        or item.get("id")
        or "เมนู"
    )


def get_menu_names(item: dict) -> List[str]:
    if not isinstance(item, dict):
        return []

    names = [
        item.get("id", ""),
        item.get("name", ""),
        item.get("name_th", ""),
        item.get("name_en", ""),
    ]

    aliases = item.get("aliases", [])
    if isinstance(aliases, list):
        names.extend(aliases)

    return [
        _safe_str(name)
        for name in names
        if _safe_str(name)
    ]


def get_available_menu_items(category: str = None) -> list:
    menu_items = get_menu_items()

    results = []

    for item in menu_items:
        if not isinstance(item, dict):
            continue

        # sample_knowledge.json ใช้ available_default
        available = item.get("available", item.get("available_default", True))

        if available is True:
            results.append(item)

    if category:
        category = _safe_str(category).lower()

        results = [
            item for item in results
            if _safe_str(item.get("category")).lower() == category
        ]

    return results


def _normalize_for_match(value: str) -> str:
    return (
        _safe_str(value)
        .lower()
        .replace(" ", "")
        .replace("-", "")
        .replace("_", "")
        .replace("'", "")
        .replace('"', "")
    )


def find_menu_by_keyword(keyword: str) -> list:
    keyword = _safe_str(keyword).lower()

    if not keyword:
        return []

    normalized_keyword = _normalize_for_match(keyword)
    results = []

    for item in get_available_menu_items():
        searchable_parts = [
            item.get("id", ""),
            item.get("name", ""),
            item.get("name_th", ""),
            item.get("name_en", ""),
            item.get("category", ""),
            item.get("description", ""),
            item.get("sweetness", ""),
            item.get("sweetness_level", ""),
        ]

        for field_name in ["tags", "recommended_for", "allergens", "aliases", "pairing"]:
            value = item.get(field_name, [])
            if isinstance(value, list):
                searchable_parts.extend(value)

        searchable_text = " ".join(
            str(part or "") for part in searchable_parts
        ).lower()

        normalized_searchable_text = _normalize_for_match(searchable_text)

        if keyword in searchable_text or normalized_keyword in normalized_searchable_text:
            results.append(item)

    return results


def find_menu_in_text(text: str) -> Optional[dict]:
    """
    ค้นหาเมนูจากข้อความลูกค้า
    เช่น ลูกค้าถามว่า Strawberry Garden Shortcake ราคาเท่าไหร่
    """
    text_lower = _safe_str(text).lower()
    normalized_text = _normalize_for_match(text_lower)

    if not text_lower:
        return None

    best_item = None
    best_score = 0

    for item in get_available_menu_items():
        if not isinstance(item, dict):
            continue

        score = 0

        for name in get_menu_names(item):
            name_lower = _safe_str(name).lower()
            normalized_name = _normalize_for_match(name_lower)

            if name_lower and name_lower in text_lower:
                score += 20 + len(name_lower)

            if normalized_name and normalized_name in normalized_text:
                score += 20 + len(normalized_name)

            # จับคำบางส่วนจากชื่อภาษาอังกฤษ เช่น flower milk pudding
            name_parts = [
                part.strip()
                for part in name_lower.replace("-", " ").replace("_", " ").split()
                if len(part.strip()) >= 4
            ]

            score += sum(3 for part in name_parts if part in text_lower)

        if score > best_score:
            best_score = score
            best_item = item

    return best_item if best_score >= 8 else None


def format_price_from_sizes(sizes) -> str:
    if not isinstance(sizes, list):
        return ""

    prices = []

    for size in sizes:
        if not isinstance(size, dict):
            continue

        size_name = str(size.get("size") or size.get("name") or "").strip()
        price = size.get("price")

        if size_name and price is not None:
            prices.append(f"{size_name} {price} บาท")
        elif price is not None:
            prices.append(f"{price} บาท")

    return ", ".join(prices)


def format_menu_price(item: dict) -> str:
    if not isinstance(item, dict):
        return ""

    name = get_menu_name(item)
    sizes = item.get("sizes", [])

    if not isinstance(sizes, list) or not sizes:
        price = item.get("price")
        if price is not None:
            return f"{name} ราคา {price} บาทค่ะ"
        return f"{name} สามารถสอบถามราคาเพิ่มเติมกับแอดมินได้ค่ะ"

    price_parts = []

    for size in sizes:
        if not isinstance(size, dict):
            continue

        size_name = size.get("size") or size.get("name") or "ขนาด"
        price = size.get("price")
        serving = _safe_str(size.get("serving"))
        preorder = _safe_str(size.get("preorder"))

        if price is not None:
            text = f"{size_name} {price} บาท"
        else:
            text = str(size_name)

        details = []
        if serving:
            details.append(serving)
        if preorder:
            details.append(f"สั่งล่วงหน้า {preorder}")

        if details:
            text += f" ({', '.join(details)})"

        price_parts.append(text)

    if not price_parts:
        return f"{name} สามารถสอบถามราคาเพิ่มเติมกับแอดมินได้ค่ะ"

    return f"{name} มีราคา {', '.join(price_parts)} ค่ะ 🌷"


def format_menu_item(item: dict, include_price: bool = True) -> str:
    name = get_menu_name(item)
    description = _safe_str(item.get("description"))
    price_text = format_price_from_sizes(item.get("sizes"))

    line = f"{name}"

    if description:
        line += f" - {description}"

    if include_price and price_text:
        line += f" ({price_text})"

    return line


def format_menu_detail(item: dict) -> str:
    if not isinstance(item, dict):
        return ""

    name = get_menu_name(item)
    description = _safe_str(item.get("description"))
    sweetness = _safe_str(item.get("sweetness") or item.get("sweetness_level"))
    sweetness_adjustable = item.get("sweetness_adjustable")
    allergens = item.get("allergens", [])
    caffeine = item.get("contains_caffeine")
    availability_note = _safe_str(item.get("availability_note"))
    pairing = item.get("pairing", [])
    recommended_for = item.get("recommended_for", [])
    price_text = format_menu_price(item)

    lines = [price_text]

    if description:
        lines.append(description)

    if sweetness:
        adjust_text = ""
        if sweetness_adjustable is True:
            adjust_text = " และสามารถปรับระดับความหวานได้"
        elif sweetness_adjustable is False:
            adjust_text = " และเป็นสูตรความหวานของร้าน"
        lines.append(f"ระดับความหวาน: {sweetness}{adjust_text}")

    if caffeine is True:
        lines.append("คาเฟอีน: มีคาเฟอีน")
    elif caffeine is False:
        lines.append("คาเฟอีน: ไม่มีคาเฟอีน")
    elif caffeine:
        lines.append(f"คาเฟอีน: {caffeine}")

    if isinstance(allergens, list) and allergens:
        lines.append(
            "ส่วนผสมที่อาจก่อให้เกิดอาการแพ้: "
            + ", ".join(str(a) for a in allergens)
        )

    if isinstance(recommended_for, list) and recommended_for:
        lines.append("เหมาะสำหรับ: " + ", ".join(str(item) for item in recommended_for))

    if isinstance(pairing, list) and pairing:
        lines.append("ทานคู่กับ: " + ", ".join(str(item) for item in pairing[:3]))

    if availability_note:
        lines.append(availability_note)

    return "\n".join(line for line in lines if _safe_str(line))


def detect_menu_category(text: str) -> str:
    text = str(text or "").lower()

    if any(word in text for word in ["เครื่องดื่ม", "น้ำ", "ชา", "กาแฟ", "ลาเต้", "โซดา", "drink"]):
        return "drink"

    if any(word in text for word in ["เค้ก", "cake"]):
        return "cake"

    if any(word in text for word in ["ขนม", "ของหวาน", "dessert", "พุดดิ้ง", "ทาร์ต"]):
        return "dessert"

    if any(word in text for word in ["เบเกอรี่", "ครัวซองต์", "bakery"]):
        return "bakery"

    return ""


def detect_recommendation_rule(text: str) -> str:
    text_lower = _safe_str(text).lower()

    rule_keywords = [
        ("first_time_customer", ["ครั้งแรก", "มือใหม่", "เริ่ม", "กินอะไรดี", "แนะนำ"]),
        ("not_too_sweet", ["หวานน้อย", "ไม่หวาน", "ไม่ชอบหวาน", "หวานไม่มาก"]),
        ("photo_lover", ["ถ่ายรูป", "รูปสวย", "คาเฟ่ฮอป", "สวย", "ถ่ายภาพ"]),
        ("birthday", ["วันเกิด", "birthday", "เค้กวันเกิด"]),
        ("gift", ["ของฝาก", "ของขวัญ", "ฝาก", "gift"]),
        ("kids_friendly", ["เด็ก", "kid", "kids", "น้อง"]),
        ("coffee_pairing", ["กาแฟ", "coffee", "americano", "latte"]),
        ("lavender_theme", ["ลาเวนเดอร์", "lavender", "ม่วง"]),
    ]

    for rule, keywords in rule_keywords:
        if any(keyword in text_lower for keyword in keywords):
            return rule

    return ""


def _menu_items_by_ids(ids: List[str]) -> List[dict]:
    id_set = set(_safe_str(item_id) for item_id in ids)
    results = []

    for item in get_available_menu_items():
        if _safe_str(item.get("id")) in id_set:
            results.append(item)

    return results


def build_recommendation_answer(kb: dict, text: str) -> str:
    menu_catalog = kb.get("menu_catalog", {})
    items = menu_catalog.get("items", [])

    if not isinstance(items, list):
        return ""

    category = detect_menu_category(text)
    rule_name = detect_recommendation_rule(text)
    recommendation_rules = get_recommendation_rules()

    filtered_items = []

    # ใช้ recommendation_rules ก่อน ถ้าข้อความสื่อความต้องการเฉพาะ
    if rule_name and isinstance(recommendation_rules.get(rule_name), list):
        filtered_items = _menu_items_by_ids(recommendation_rules.get(rule_name))

        if category:
            filtered_items = [
                item for item in filtered_items
                if item.get("category") == category
            ]

    # ถ้าไม่มี rule หรือ rule ไม่ตรง ให้คัดจาก menu_catalog
    if not filtered_items:
        for item in items:
            if not isinstance(item, dict):
                continue

            if category and item.get("category") != category:
                continue

            tags = item.get("tags", [])
            recommended_for = item.get("recommended_for", [])

            tag_text = " ".join(str(tag).lower() for tag in tags) if isinstance(tags, list) else ""
            recommended_text = (
                " ".join(str(value).lower() for value in recommended_for)
                if isinstance(recommended_for, list)
                else ""
            )

            is_recommended = (
                "signature" in tag_text
                or "signature_drink" in tag_text
                or "best_seller" in tag_text
                or "photo_friendly" in tag_text
                or "not_too_sweet" in tag_text
                or bool(recommended_text)
            )

            if is_recommended:
                filtered_items.append(item)

    if not filtered_items:
        filtered_items = [
            item for item in items
            if isinstance(item, dict)
            and (not category or item.get("category") == category)
        ]

    selected_items = filtered_items[:3]

    if not selected_items:
        return ""

    if category == "drink":
        intro = "เครื่องดื่มแนะนำของร้านมีหลายเมนูที่เข้ากับบรรยากาศสวนดอกไม้มาก ๆ ค่ะ 🌷"
    elif category == "cake":
        intro = "เค้กแนะนำของร้านมีหลายเมนูน่าลองค่ะ 🌷"
    elif category == "dessert":
        intro = "ขนมหวานแนะนำของร้านมีเมนูนุ่มละมุนหลายรายการค่ะ 🌷"
    elif category == "bakery":
        intro = "เบเกอรี่แนะนำของร้านมีเมนูหอมละมุนที่ทานคู่เครื่องดื่มได้ดีค่ะ 🌷"
    else:
        intro = "เมนูแนะนำของร้านมีหลายเมนูที่ลูกค้าชอบค่ะ 🌷"

    lines = [intro]

    for item in selected_items:
        lines.append(f"- {format_menu_item(item)}")

    lines.append("ลูกค้าชอบแนวหวานน้อย ชา กาแฟ นม หรือโซดาสดชื่นเป็นพิเศษไหมคะ")

    return "\n".join(lines)


def build_menu_summary(category: str = "") -> str:
    menu_items = get_available_menu_items(category if category else None)

    if not menu_items:
        return ""

    categories: Dict[str, List[str]] = {}

    for item in menu_items:
        item_category = _safe_str(item.get("category"), "other")
        name = get_menu_name(item)

        if not name:
            continue

        categories.setdefault(item_category, []).append(name)

    if not categories:
        return ""

    menu_catalog = get_menu_catalog()
    category_labels = menu_catalog.get("categories", {}) if isinstance(menu_catalog, dict) else {}

    default_labels = {
        "cake": "เค้ก",
        "dessert": "ขนมหวาน",
        "bakery": "เบเกอรี่",
        "drink": "เครื่องดื่ม",
        "coffee": "กาแฟ",
        "tea": "ชา",
        "soda": "โซดา",
        "other": "เมนูอื่น ๆ"
    }

    lines = []

    for category_key, names in categories.items():
        label = category_labels.get(category_key) or default_labels.get(category_key, category_key)
        preview = ", ".join(names[:8])
        lines.append(f"- {label}: {preview}")

    return (
        "ที่ร้านมีเมนูเค้ก ขนมหวาน เบเกอรี่ และเครื่องดื่มค่ะ 🍰✨\n"
        + "\n".join(lines)
        + "\n\nหากสนใจเมนูไหนเป็นพิเศษ สามารถถามราคา ขนาด รสชาติ หรือส่วนผสมของเมนูนั้นได้เลยนะคะ 🌷"
    )


def build_price_summary(limit: int = 10, category: str = "") -> str:
    menu_items = get_available_menu_items(category if category else None)

    if not menu_items:
        return ""

    lines = []

    for item in menu_items[:limit]:
        price_line = format_menu_price(item)
        if price_line:
            lines.append(f"- {price_line}")

    if not lines:
        return ""

    return (
        "ราคาเมนูของร้านจะแตกต่างกันตามประเภทและขนาดค่ะ 🌷\n"
        + "\n".join(lines)
        + "\n\nหากลูกค้าต้องการดูราคาเมนูเฉพาะ สามารถแจ้งชื่อเมนูมาได้เลยนะคะ"
    )


def build_recommendation_summary() -> str:
    kb = load_knowledge_base()
    return build_recommendation_answer(kb, "")


def build_size_option_answer(text: str = "") -> str:
    matched_menu = find_menu_in_text(text) if text else None

    if matched_menu:
        return format_menu_price(matched_menu)

    return (
        "ขนาดของเมนูจะแตกต่างกันตามประเภทค่ะ 🌷 "
        "เค้กบางเมนูมี Mini, Regular หรือ Whole Cake ส่วนเครื่องดื่มส่วนใหญ่มี Regular และ Large "
        "ลูกค้าสนใจเมนูไหนเป็นพิเศษไหมคะ"
    )


def build_availability_answer(text: str = "") -> str:
    matched_menu = find_menu_in_text(text) if text else None

    if matched_menu:
        name = get_menu_name(matched_menu)
        note = _safe_str(matched_menu.get("availability_note"))
        if note:
            return f"{name}: {note}"
        return f"{name} โดยปกติเป็นเมนูที่มีจำหน่ายค่ะ แต่จำนวนอาจเปลี่ยนตามรอบอบและช่วงเวลา แนะนำให้แอดมินเช็กให้อีกครั้งนะคะ 🌷"

    return (
        "เมนูของร้านส่วนใหญ่มีจำหน่ายตามรอบอบและช่วงเวลาค่ะ 🌷 "
        "บางเมนูอาจมีจำนวนจำกัดต่อวัน หากลูกค้าสนใจเมนูไหนเป็นพิเศษ แจ้งชื่อเมนูมาได้เลยนะคะ"
    )


# =========================================================
# POLICY / STORE / DELIVERY ANSWERS
# =========================================================

def _build_store_info_answer(intent: str) -> str:
    store_info = get_store_info()

    if not store_info:
        return ""

    if intent == "opening_hours":
        opening_hours = store_info.get("opening_hours")

        if isinstance(opening_hours, dict):
            days = _safe_str(opening_hours.get("days"))
            time = _safe_str(opening_hours.get("time"))
            holiday_note = _safe_str(opening_hours.get("holiday_note"))

            if days or time:
                answer = f"ร้าน Pudding Petals {days} เวลา {time} ค่ะ 🌷".strip()

                if holiday_note:
                    answer += f" {holiday_note}"

                return answer

        opening_hours_text = _safe_str(opening_hours)
        if opening_hours_text:
            return f"ร้าน Pudding Petals Cafe {opening_hours_text} ค่ะ 🌷"

    if intent == "location":
        location = _safe_str(store_info.get("location"))
        if location:
            return (
                f"ร้าน Pudding Petals Cafe ตั้งอยู่แถว{location}ค่ะ 🌷 "
                "เป็นคาเฟ่ขนมหวานบรรยากาศสวนดอกไม้ มีทั้งโซน indoor และ outdoor ค่ะ"
            )

    if intent == "reservation":
        reservation_policy = _safe_str(store_info.get("reservation_policy"))
        if reservation_policy:
            return reservation_policy

    if intent == "facility":
        facilities = store_info.get("facilities", {})
        if isinstance(facilities, dict):
            lines = ["สิ่งอำนวยความสะดวกของร้านมีดังนี้ค่ะ 🌷"]

            label_map = {
                "wifi": "Wi-Fi",
                "power_plug": "ปลั๊กไฟ",
                "parking": "ที่จอดรถ",
                "pet_friendly": "สัตว์เลี้ยง",
                "restroom": "ห้องน้ำ",
                "air_conditioning": "แอร์"
            }

            for key, value in facilities.items():
                if isinstance(value, dict):
                    label = label_map.get(key, key)
                    desc = _safe_str(value.get("description"))
                    available = value.get("available")
                    if desc:
                        lines.append(f"- {label}: {desc}")
                    else:
                        lines.append(f"- {label}: {_format_bool_available(available)}")

            return "\n".join(lines)

    if intent == "ambience_photo_spot":
        zones = store_info.get("cafe_zones", {})
        if isinstance(zones, dict):
            photo_spots = zones.get("photo_spots", [])
            indoor = zones.get("indoor", {})
            outdoor = zones.get("outdoor", {})

            lines = ["ร้านตกแต่งในบรรยากาศสวนดอกไม้ โทนอ่อนหวาน ถ่ายรูปได้หลายมุมค่ะ 🌷"]

            if isinstance(indoor, dict) and indoor.get("description"):
                lines.append(f"- Indoor: {indoor.get('description')}")

            if isinstance(outdoor, dict) and outdoor.get("description"):
                lines.append(f"- Outdoor: {outdoor.get('description')}")

            if isinstance(photo_spots, list) and photo_spots:
                lines.append("มุมถ่ายรูปแนะนำ: " + ", ".join(str(spot) for spot in photo_spots))

            return "\n".join(lines)

    return ""


def _build_delivery_answer() -> str:
    info = get_delivery_info()

    if not info:
        return ""

    platforms = _list_to_text(info.get("platforms"))
    description = _safe_str(info.get("description"))
    takeaway = info.get("takeaway_available")
    pickup = info.get("pickup_available")

    lines = []

    if description:
        lines.append(description)
    elif platforms:
        lines.append(f"สามารถสั่งผ่าน {platforms} ได้ค่ะ 🌷")

    if takeaway is True or pickup is True:
        options = []
        if takeaway is True:
            options.append("สั่งกลับบ้าน")
        if pickup is True:
            options.append("รับเองที่ร้าน")
        lines.append("รองรับ: " + ", ".join(options))

    tracking_policy = _safe_str(info.get("tracking_policy"))
    if tracking_policy:
        lines.append(tracking_policy)

    return "\n".join(lines)


def _build_payment_answer() -> str:
    policies = get_policies()
    return _safe_str(policies.get("payment_policy"))


def _build_packaging_answer() -> str:
    options = get_packaging_options()
    if not options:
        return ""

    lines = ["ทางร้านมีตัวเลือกการแพ็กสินค้าหลายแบบค่ะ 🌷"]

    for key, value in options.items():
        if not isinstance(value, dict):
            continue

        description = _safe_str(value.get("description"))
        extra_fee = value.get("extra_fee")

        if description:
            line = f"- {description}"
            if extra_fee not in [None, ""]:
                line += f" (ค่าใช้จ่ายเพิ่มเติม: {extra_fee})"
            lines.append(line)

    return "\n".join(lines)


def _build_policy_answer(intent: str) -> str:
    policies = get_policies()

    policy_map = {
        "promotion": "promotion_policy",
        "payment": "payment_policy",
        "reservation": "reservation_policy",
        "custom_cake": "whole_cake_policy",
        "special_occasion": "whole_cake_policy",
        "delivery_takeaway": "takeaway_policy",
        "allergy": "allergy_policy",
        "ingredients": "allergy_policy",
        "dietary_option": "dietary_policy",
        "sweetness_adjustment": "sweetness_policy",
        "order_status": "order_status_policy",
        "refund_return": "refund_return_policy",
        "complaint_product": "service_recovery_policy",
        "complaint_service": "service_recovery_policy",
        "complaint_staff": "service_recovery_policy",
        "high_risk_complaint": "high_risk_escalation_policy",
        "ambience_photo_spot": "photography_policy",
        "facility": "pet_policy",
        "packaging": "takeaway_policy",
    }

    key = policy_map.get(intent)
    if key:
        return _safe_str(policies.get(key))

    return ""


def _build_brand_answer() -> str:
    brand = get_brand_profile()
    if not brand:
        return ""

    store_name = _safe_str(brand.get("store_name"))
    concept = _safe_str(brand.get("brand_concept"))

    if store_name and concept:
        return f"{store_name} เป็น {concept} ค่ะ 🌷"

    return concept


def _build_complaint_answer(intent: str, faq_data: dict) -> str:
    answer = _safe_str(faq_data.get("answer"))
    if answer:
        return answer

    policy = _build_policy_answer(intent)
    if policy:
        return (
            "ขออภัยอย่างจริงใจนะคะ แอดมินรับเรื่องไว้ตรวจสอบให้ค่ะ 🌷 "
            + policy
        )

    return (
        "ขออภัยอย่างจริงใจนะคะ แอดมินรับเรื่องไว้ตรวจสอบให้ค่ะ 🌷 "
        "รบกวนแจ้งรายละเอียดเพิ่มเติม เช่น เลขออเดอร์ วันเวลา ช่องทางที่สั่ง และรูปสินค้า เพื่อให้ตรวจสอบได้ถูกต้องนะคะ"
    )


# =========================================================
# HUMAN / HANDOFF FUNCTIONS
# =========================================================

def get_human_required_intents() -> set:
    faq = get_faq()

    human_required = set()

    for intent, data in faq.items():
        if _extract_requires_human(data) is True:
            human_required.add(normalize_intent_label(intent))

    return human_required


def is_human_required(intent_label: str, text: str = "") -> bool:
    faq_data = get_faq_answer(intent_label, text)
    return faq_data.get("requires_human") is True


def get_handoff_note(intent_label: str, text: str = ""):
    faq_data = get_faq_answer(intent_label, text)
    return faq_data.get("handoff_note")


# =========================================================
# KEYWORD SEARCH
# =========================================================

def search_faq_by_keyword(text: str) -> dict:
    text = _safe_str(text).lower()
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
        normalized_intent = normalize_intent_label(intent)

        keywords = _extract_keywords(data)
        examples = _extract_examples(data)

        score = 0

        for keyword in keywords:
            keyword = _safe_str(keyword).lower()

            if keyword and keyword in text:
                score += 3 + len(keyword)

        for example in examples:
            example = _safe_str(example).lower()

            if example and example in text:
                score += 2 + len(example)

        if score > best_score:
            best_score = score
            best_match = {
                "intent": normalized_intent,
                **_normalize_knowledge_item(normalized_intent, data)
            }

    if best_match and best_score > 0:
        return best_match

    faq_data = get_faq_answer("general_question")

    return {
        "intent": "general_question",
        **faq_data
    }


# =========================================================
# RETRIEVE KNOWLEDGE
# ใช้กับ pipeline_service.py / reply_service.py
# =========================================================

def _build_return(
    *,
    title: str,
    answer: str,
    matched: bool,
    intent: str,
    source: str,
    faq_data: dict,
    category: str = "general",
    requires_human: Optional[bool] = None,
    handoff_note: Optional[str] = None,
    matched_menu: Optional[dict] = None,
    extra: Optional[dict] = None
) -> dict:
    answer = _safe_str(answer)

    data = {
        "title": title,
        "content": answer,
        "answer": answer,
        "matched": bool(matched and answer),
        "intent": intent,
        "label": intent,
        "canonical_intent": intent,
        "requires_human": (
            bool(requires_human)
            if requires_human is not None
            else bool(faq_data.get("requires_human", False))
        ),
        "handoff_note": handoff_note if handoff_note is not None else faq_data.get("handoff_note"),
        "handoff_when": faq_data.get("handoff_when", []),
        "keywords": faq_data.get("keywords", []),
        "examples": faq_data.get("examples", []),
        "follow_up_prompts": faq_data.get("follow_up_prompts", []),
        "related_kb": faq_data.get("related_kb", []),
        "category": category or faq_data.get("category", "general"),
        "source": source,
    }

    if matched_menu:
        data["matched_menu"] = matched_menu

    if extra:
        data.update(extra)

    return data


def _text_asks_menu_detail(text: str) -> bool:
    text_lower = _safe_str(text).lower()

    detail_words = [
        "รสชาติ",
        "เป็นยังไง",
        "เป็นอย่างไร",
        "อร่อยไหม",
        "อร่อยมั้ย",
        "หวานไหม",
        "หวานมั้ย",
        "มีอะไร",
        "ส่วนผสม",
        "แพ้",
        "คาเฟอีน",
        "ราคา",
        "ขนาด",
        "แนะนำไหม",
        "ดีไหม",
        "รายละเอียด"
    ]

    return any(word in text_lower for word in detail_words)


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
    text = _safe_str(text)
    normalized_intent = normalize_intent_label(intent_label, text)

    faq_data = get_faq_answer(normalized_intent, text)

    # ถ้าเป็น general_question แต่มีข้อความ ให้ลองหา intent จาก keyword
    if normalized_intent == "general_question" and text:
        keyword_match = search_faq_by_keyword(text)

        if keyword_match.get("intent") != "general_question":
            normalized_intent = keyword_match.get("intent")
            faq_data = keyword_match

    category = detect_menu_category(text)

    # หาเมนูเฉพาะตั้งแต่ต้น เพื่อให้คำถาม "Flower Milk Pudding รสชาติเป็นยังไง"
    # ไม่ไหลไป fallback หรือ menu summary
    matched_menu = find_menu_in_text(text) if text else None

    if matched_menu:
        if normalized_intent == "price_inquiry" or "ราคา" in text:
            answer = format_menu_price(matched_menu)
            return _build_return(
                title="Price Inquiry",
                answer=answer,
                matched=True,
                intent=normalized_intent,
                source="menu_catalog_json",
                faq_data=faq_data,
                category="menu_price",
                matched_menu=matched_menu
            )

        if (
            normalized_intent in {
                "menu_inquiry",
                "general_question",
                "service_question",
                "recommendation",
                "size_option",
                "availability",
                "ingredients",
                "sweetness_adjustment",
                "allergy",
                "dietary_option",
            }
            or _text_asks_menu_detail(text)
        ):
            answer = format_menu_detail(matched_menu)

            requires_human = normalized_intent in {"ingredients", "allergy", "dietary_option"}
            handoff_note = (
                "ส่งต่อแอดมินเพื่อตรวจสอบส่วนผสมหรือข้อมูลการแพ้อาหาร"
                if requires_human
                else None
            )

            return _build_return(
                title="Menu Detail",
                answer=answer,
                matched=True,
                intent=normalized_intent,
                source="menu_catalog_json",
                faq_data=faq_data,
                category="menu_detail",
                requires_human=requires_human,
                handoff_note=handoff_note,
                matched_menu=matched_menu
            )

    # ถามเมนูรวม
    if normalized_intent == "menu_inquiry":
        menu_summary = build_menu_summary(category)
        if menu_summary:
            return _build_return(
                title="Menu Inquiry",
                answer=menu_summary,
                matched=True,
                intent=normalized_intent,
                source="menu_catalog_json",
                faq_data=faq_data,
                category="menu"
            )

    # ถามราคาเมนูเฉพาะ / ราคาทั่วไป
    if normalized_intent == "price_inquiry":
        price_summary = build_price_summary(category=category)
        if price_summary:
            return _build_return(
                title="Price Inquiry",
                answer=price_summary,
                matched=True,
                intent=normalized_intent,
                source="menu_catalog_json",
                faq_data=faq_data,
                category="menu_price"
            )

    # ขอเมนูแนะนำ
    if normalized_intent == "recommendation":
        kb = load_knowledge_base()

        recommendation_answer = build_recommendation_answer(kb, text)

        if not recommendation_answer:
            recommendation_answer = build_recommendation_summary()

        if recommendation_answer:
            return _build_return(
                title="Recommendation",
                answer=recommendation_answer,
                matched=True,
                intent=normalized_intent,
                source="menu_catalog_json",
                faq_data=faq_data,
                category="menu"
            )

    # ขนาด
    if normalized_intent == "size_option":
        answer = build_size_option_answer(text)
        if answer:
            return _build_return(
                title="Size Option",
                answer=answer,
                matched=True,
                intent=normalized_intent,
                source="menu_catalog_json",
                faq_data=faq_data,
                category="menu_size"
            )

    # สถานะ/ความพร้อมของเมนู
    if normalized_intent == "availability":
        answer = build_availability_answer(text)
        if answer:
            return _build_return(
                title="Availability",
                answer=answer,
                matched=True,
                intent=normalized_intent,
                source="menu_catalog_json",
                faq_data=faq_data,
                category="menu_availability"
            )

    # ข้อมูลร้าน
    store_answer = _build_store_info_answer(normalized_intent)
    if store_answer:
        return _build_return(
            title=faq_data.get("title", normalized_intent),
            answer=store_answer,
            matched=True,
            intent=normalized_intent,
            source="store_info_json",
            faq_data=faq_data,
            category=faq_data.get("category", "store_info")
        )

    # เดลิเวอรี่ / สั่งกลับบ้าน
    if normalized_intent == "delivery_takeaway":
        delivery_answer = _build_delivery_answer()
        if delivery_answer:
            return _build_return(
                title="Delivery / Takeaway",
                answer=delivery_answer,
                matched=True,
                intent=normalized_intent,
                source="delivery_info_json",
                faq_data=faq_data,
                category="delivery"
            )

    # การชำระเงิน
    if normalized_intent == "payment":
        payment_answer = _build_payment_answer()
        if payment_answer:
            return _build_return(
                title="Payment",
                answer=payment_answer,
                matched=True,
                intent=normalized_intent,
                source="policies_json",
                faq_data=faq_data,
                category="payment"
            )

    # แพ็กเกจ / ของขวัญ
    if normalized_intent == "packaging":
        packaging_answer = _build_packaging_answer()
        if packaging_answer:
            return _build_return(
                title="Packaging",
                answer=packaging_answer,
                matched=True,
                intent=normalized_intent,
                source="packaging_options_json",
                faq_data=faq_data,
                category="packaging"
            )

    # นโยบายและเคสต้องระวัง
    if normalized_intent in {
        "promotion",
        "custom_cake",
        "special_occasion",
        "sweetness_adjustment",
        "allergy",
        "ingredients",
        "dietary_option",
        "order_status",
        "refund_return",
    }:
        policy_answer = _build_policy_answer(normalized_intent)
        faq_answer = _safe_str(faq_data.get("answer"))
        answer = faq_answer or policy_answer

        if answer:
            return _build_return(
                title=faq_data.get("title", normalized_intent),
                answer=answer,
                matched=True,
                intent=normalized_intent,
                source="knowledge_base_json",
                faq_data=faq_data,
                category=faq_data.get("category", "policy"),
                requires_human=faq_data.get("requires_human", normalized_intent in {"allergy", "refund_return"})
            )

    # ร้องเรียน / ความเสี่ยง
    if normalized_intent in {
        "complaint_product",
        "complaint_service",
        "complaint_staff",
        "high_risk_complaint",
    }:
        answer = _build_complaint_answer(normalized_intent, faq_data)

        return _build_return(
            title=faq_data.get("title", normalized_intent),
            answer=answer,
            matched=True,
            intent=normalized_intent,
            source="knowledge_base_json",
            faq_data=faq_data,
            category="complaint",
            requires_human=True
        )

    # brand / general
    if normalized_intent == "general_question" and any(word in text.lower() for word in ["ร้านเป็นยังไง", "คาเฟ่", "pudding petals", "เกี่ยวกับร้าน"]):
        brand_answer = _build_brand_answer()
        if brand_answer:
            return _build_return(
                title="Brand Profile",
                answer=brand_answer,
                matched=True,
                intent=normalized_intent,
                source="brand_profile_json",
                faq_data=faq_data,
                category="brand"
            )

    # ใช้ default_response / response_templates ของ intent
    content = faq_data.get("answer", "")

    # ใช้ fallback_response จาก response_generation_rules ถ้า general ไม่มีคำตอบ
    if not content and normalized_intent == "general_question":
        response_rules = get_response_generation_rules()
        content = _safe_str(response_rules.get("fallback_response"))

    return _build_return(
        title=faq_data.get("title", normalized_intent),
        answer=content,
        matched=True if content else False,
        intent=normalized_intent,
        source="knowledge_base_json",
        faq_data=faq_data,
        category=faq_data.get("category", "general")
    )
