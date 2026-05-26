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

    "price": "price_inquiry",
    "ask_price": "price_inquiry",

    "size": "size_option",
    "sizes": "size_option",

    "ingredient": "ingredients",
    "allergens": "allergy",

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
    - pudding_petals_intent_knowledge_base.json
    - sample_knowledge.json เดิม
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


def _is_knowledge_item(value: Any) -> bool:
    return isinstance(value, dict) and (
        "answer" in value
        or "reply" in value
        or "response" in value
        or "template" in value
        or "message" in value
        or "content" in value
    )

def extract_intent_answer(intent_data: dict) -> str:
    """
    ดึงคำตอบจาก intent ใน sample_knowledge.json
    รองรับ schema เดิมของไฟล์:
    - default_response
    - response_templates
    - answer/content เผื่ออนาคต
    """

    if not isinstance(intent_data, dict):
        return ""

    for key in ["answer", "content", "default_response"]:
        value = intent_data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    templates = intent_data.get("response_templates")
    if isinstance(templates, list) and templates:
        first_template = templates[0]
        if isinstance(first_template, str) and first_template.strip():
            return first_template.strip()

    return ""

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

def format_price_from_sizes(sizes) -> str:
    if not isinstance(sizes, list):
        return ""

    prices = []

    for size in sizes:
        if not isinstance(size, dict):
            continue

        size_name = str(size.get("size") or "").strip()
        price = size.get("price")

        if size_name and price:
            prices.append(f"{size_name} {price} บาท")
        elif price:
            prices.append(f"{price} บาท")

    return ", ".join(prices)


def format_menu_item(item: dict) -> str:
    name = get_menu_name(item)
    description = item.get("description") or ""
    price_text = format_price_from_sizes(item.get("sizes"))

    line = f"{name}"

    if description:
        line += f" - {description}"

    if price_text:
        line += f" ({price_text})"

    return line

def build_recommendation_answer(kb: dict, text: str) -> str:
    menu_catalog = kb.get("menu_catalog", {})
    items = menu_catalog.get("items", [])

    if not isinstance(items, list):
        return ""

    category = detect_menu_category(text)

    filtered_items = []

    for item in items:
        if not isinstance(item, dict):
            continue

        if category and item.get("category") != category:
            continue

        tags = item.get("tags", [])
        recommended_for = item.get("recommended_for", [])

        is_recommended = (
            "signature" in tags
            or "signature_drink" in tags
            or "best_seller" in tags
            or "photo_friendly" in tags
            or len(recommended_for) > 0
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
    else:
        intro = "เมนูแนะนำของร้านมีหลายเมนูที่ลูกค้าชอบค่ะ 🌷"

    lines = [intro]

    for item in selected_items:
        lines.append(f"- {format_menu_item(item)}")

    lines.append("ลูกค้าชอบแนวหวานน้อย ชา กาแฟ นม หรือโซดาสดชื่นเป็นพิเศษไหมคะ")

    return "\n".join(lines)

def _extract_answer(data: Dict[str, Any]) -> str:
    if not isinstance(data, dict):
        return ""

    # รองรับ schema เดิม + schema ใหม่ของ sample_knowledge.json
    for key in [
        "answer",
        "content",
        "default_response",
        "reply",
        "response",
        "template",
        "message"
    ]:
        value = data.get(key)

        if isinstance(value, str) and value.strip():
            return value.strip()

        if isinstance(value, list) and value:
            first = value[0]
            if isinstance(first, str) and first.strip():
                return first.strip()

    # sample_knowledge.json ใช้ response_templates เป็น list
    templates = data.get("response_templates")
    if isinstance(templates, list) and templates:
        first_template = templates[0]
        if isinstance(first_template, str) and first_template.strip():
            return first_template.strip()

    return ""

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


def _normalize_knowledge_item(intent: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    แปลงข้อมูล intent จาก JSON ให้เป็นรูปแบบกลางของระบบ
    """
    if not isinstance(data, dict):
        data = {}

    title = (
        data.get("title")
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
        "category": _extract_category(data),
        "intent": intent,
        "label": intent,
        "canonical_intent": intent,
    }


# =========================================================
# FAQ / INTENT KNOWLEDGE
# =========================================================

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

    3) แบบ list:
       {"intents": [{"intent": "greeting", "answer": "..."}]}

    4) แบบ top-level:
       {"greeting": {"answer": "..."}, "promotion": {"answer": "..."}}
    """
    kb = load_knowledge_base()

    possible_keys = [
        "FAQ",
        "faq",
        "INTENTS",
        "intents",
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

    label = KNOWLEDGE_ALIASES.get(label, label)

    if label in SUPPORTED_INTENTS:
        return label

    # เผื่อ JSON มี intent เพิ่มเติมที่ยังไม่ได้ใส่ SUPPORTED_INTENTS
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
# DATA ACCESSORS
# คงชื่อฟังก์ชันเดิมไว้ เพื่อให้ไฟล์อื่นใช้งานต่อได้
# =========================================================

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

def get_policies() -> dict:
    kb = load_knowledge_base()

    policies = _first_existing(
        kb,
        ["POLICIES", "policies", "policy", "POLICY"],
        {}
    )

    return policies if isinstance(policies, dict) else {}


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

def find_menu_by_keyword(keyword: str) -> list:
    keyword = _safe_str(keyword).lower()

    if not keyword:
        return []

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

        if keyword in searchable_text:
            results.append(item)

    return results

def find_menu_in_text(text: str) -> Optional[dict]:
    """
    ค้นหาเมนูจากข้อความลูกค้า
    เช่น ลูกค้าถามว่า Strawberry Garden Shortcake ราคาเท่าไหร่
    """
    text_lower = _safe_str(text).lower()

    if not text_lower:
        return None

    for item in get_available_menu_items():
        if not isinstance(item, dict):
            continue

        searchable_names = [
            item.get("id", ""),
            item.get("name", ""),
            item.get("name_th", ""),
            item.get("name_en", "")
        ]

        aliases = item.get("aliases", [])
        if isinstance(aliases, list):
            searchable_names.extend(aliases)

        for name in searchable_names:
            name_lower = _safe_str(name).lower()

            if name_lower and name_lower in text_lower:
                return item

        item_name = _safe_str(get_menu_name(item)).lower()

        name_parts = [
            part.strip()
            for part in item_name.replace("-", " ").split()
            if len(part.strip()) >= 4
        ]

        if any(part in text_lower for part in name_parts):
            return item

    return None

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

        if price is not None:
            price_parts.append(f"{size_name} {price} บาท")
        else:
            price_parts.append(str(size_name))

    if not price_parts:
        return f"{name} สามารถสอบถามราคาเพิ่มเติมกับแอดมินได้ค่ะ"

    return f"{name} มีราคา {', '.join(price_parts)} ค่ะ 🌷"

def format_menu_detail(item: dict) -> str:
    if not isinstance(item, dict):
        return ""

    name = item.get("name") or item.get("id") or "เมนู"
    description = _safe_str(item.get("description"))
    sweetness = _safe_str(item.get("sweetness") or item.get("sweetness_level"))
    allergens = item.get("allergens", [])
    price_text = format_menu_price(item)

    lines = [price_text]

    if description:
        lines.append(description)

    if sweetness:
        lines.append(f"ระดับความหวาน: {sweetness}")

    if isinstance(allergens, list) and allergens:
        lines.append(
            "ส่วนผสมที่อาจก่อให้เกิดอาการแพ้: "
            + ", ".join(str(a) for a in allergens)
        )

    return "\n".join(lines)


def build_menu_summary() -> str:
    menu_items = get_available_menu_items()

    if not menu_items:
        return ""

    categories: Dict[str, List[str]] = {}

    for item in menu_items:
        category = _safe_str(item.get("category"), "other")
        name = get_menu_name(item)

        if not name:
            continue

        categories.setdefault(category, []).append(name)

    if not categories:
        return ""

    category_labels = {
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

    for category, names in categories.items():
        label = category_labels.get(category, category)
        preview = ", ".join(names[:6])
        lines.append(f"- {label}: {preview}")

    return (
        "ที่ร้านมีเมนูเค้ก ขนมหวาน เบเกอรี่ และเครื่องดื่มค่ะ 🍰✨\n"
        + "\n".join(lines)
        + "\n\nหากสนใจเมนูไหนเป็นพิเศษ สามารถถามราคา ขนาด หรือส่วนผสมของเมนูนั้นได้เลยนะคะ 🌷"
    )

def build_price_summary(limit: int = 10) -> str:
    menu_items = get_available_menu_items()

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
    menu_items = get_available_menu_items()

    if not menu_items:
        return ""

    recommended = []

    for item in menu_items:
        tags = item.get("tags", [])
        recommended_for = item.get("recommended_for", [])

        tag_text = " ".join(str(t).lower() for t in tags) if isinstance(tags, list) else ""
        rec_text = " ".join(str(t).lower() for t in recommended_for) if isinstance(recommended_for, list) else ""

        if (
            "signature" in tag_text
            or "signature_drink" in tag_text
            or "best_seller" in tag_text
            or "ยอดนิยม" in tag_text
            or "ขายดี" in tag_text
            or "ถ่ายรูปสวย" in tag_text
            or "ลูกค้าใหม่" in rec_text
            or "first_time_customer" in rec_text
            or rec_text
        ):
            recommended.append(item)

    if not recommended:
        recommended = menu_items[:3]

    lines = []

    for item in recommended[:5]:
        name = get_menu_name(item)
        description = _safe_str(item.get("description"))
        price = format_menu_price(item)

        if description:
            lines.append(f"- {name}: {description}\n  {price}")
        else:
            lines.append(f"- {price}")

    return (
        "ถ้าเพิ่งมาครั้งแรก แอดมินแนะนำเมนูที่เข้ากับบรรยากาศสวนดอกไม้ของร้านค่ะ 🌷\n"
        + "\n".join(lines)
        + "\n\nถ้าลูกค้าชอบหวานน้อย ชอบถ่ายรูป หรืออยากได้เมนูสำหรับวันเกิด บอกแอดมินได้เลยนะคะ"
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
                score += 2

        for example in examples:
            example = _safe_str(example).lower()

            if example and example in text:
                score += 1

        if score > best_score:
            best_score = score
            best_match = {
                "intent": normalized_intent,
                **_normalize_knowledge_item(normalized_intent, data)
            }

    if best_match:
        return best_match

    faq_data = get_faq_answer("general_question")

    return {
        "intent": "general_question",
        **faq_data
    }


# =========================================================
# STORE INFO RESPONSE HELPERS
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
                f"ร้าน Pudding Petals Cafe ตั้งอยู่โซน{location}ค่ะ 🌷 "
                "เป็นคาเฟ่ขนมหวานบรรยากาศสวนดอกไม้ มีทั้งโซน indoor และ outdoor ค่ะ"
            )

    if intent == "reservation":
        reservation_policy = _safe_str(store_info.get("reservation_policy"))
        if reservation_policy:
            return reservation_policy

    return ""

# =========================================================
# RETRIEVE KNOWLEDGE
# ใช้กับ pipeline_service.py / reply_service.py
# =========================================================

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

    # ถามราคาเมนูเฉพาะ
    if normalized_intent == "price_inquiry" and text:
        matched_menu = find_menu_in_text(text)

        if matched_menu:
            answer = format_menu_price(matched_menu)
            return {
                "title": "Price Inquiry",
                "content": answer,
                "answer": answer,
                "matched": True,
                "intent": normalized_intent,
                "label": normalized_intent,
                "canonical_intent": normalized_intent,
                "requires_human": False,
                "handoff_note": None,
                "keywords": faq_data.get("keywords", []),
                "examples": faq_data.get("examples", []),
                "category": "menu",
                "source": "menu_items_json",
                "matched_menu": matched_menu
            }

    # ถามรายละเอียดเมนูเฉพาะ
    if normalized_intent in {"menu_inquiry", "ingredients", "sweetness_adjustment", "allergy"} and text:
        matched_menu = find_menu_in_text(text)

        if matched_menu and normalized_intent != "menu_inquiry":
            answer = format_menu_detail(matched_menu)
            return {
                "title": "Menu Detail",
                "content": answer,
                "answer": answer,
                "matched": True,
                "intent": normalized_intent,
                "label": normalized_intent,
                "canonical_intent": normalized_intent,
                "requires_human": normalized_intent in {"ingredients", "allergy"},
                "handoff_note": (
                    "ส่งต่อแอดมินเพื่อตรวจสอบส่วนผสมหรือข้อมูลการแพ้อาหาร"
                    if normalized_intent in {"ingredients", "allergy"}
                    else None
                ),
                "keywords": faq_data.get("keywords", []),
                "examples": faq_data.get("examples", []),
                "category": "menu_safety",
                "source": "menu_items_json",
                "matched_menu": matched_menu
            }

    # ถามเมนูรวม
    if normalized_intent == "menu_inquiry":
        menu_summary = build_menu_summary()
        if menu_summary:
            return {
                "title": "Menu Inquiry",
                "content": menu_summary,
                "answer": menu_summary,
                "matched": True,
                "intent": normalized_intent,
                "label": normalized_intent,
                "canonical_intent": normalized_intent,
                "requires_human": False,
                "handoff_note": None,
                "keywords": faq_data.get("keywords", []),
                "examples": faq_data.get("examples", []),
                "category": "menu",
                "source": "menu_items_json"
            }

    # ถามราคาทั่วไป
    if normalized_intent == "price_inquiry":
        price_summary = build_price_summary()
        if price_summary:
            return {
                "title": "Price Inquiry",
                "content": price_summary,
                "answer": price_summary,
                "matched": True,
                "intent": normalized_intent,
                "label": normalized_intent,
                "canonical_intent": normalized_intent,
                "requires_human": False,
                "handoff_note": None,
                "keywords": faq_data.get("keywords", []),
                "examples": faq_data.get("examples", []),
                "category": "menu",
                "source": "menu_items_json"
            }

    # ขอเมนูแนะนำ
    if normalized_intent == "recommendation":
        kb = load_knowledge_base()

        # ใช้คำถามลูกค้าเพื่อแยก category เช่น เครื่องดื่ม / เค้ก / ขนม
        recommendation_answer = build_recommendation_answer(kb, text)

        # fallback เผื่อ build_recommendation_answer ไม่ได้ผล
        if not recommendation_answer:
            recommendation_answer = build_recommendation_summary()

        if recommendation_answer:
            return {
                "title": "Recommendation",
                "content": recommendation_answer,
                "answer": recommendation_answer,
                "matched": True,
                "intent": normalized_intent,
                "label": normalized_intent,
                "canonical_intent": normalized_intent,
                "requires_human": False,
                "handoff_note": None,
                "keywords": faq_data.get("keywords", []),
                "examples": faq_data.get("examples", []),
                "category": "menu",
                "source": "menu_catalog_json"
            }

    # ข้อมูลร้านที่ดึงจาก STORE_INFO ได้โดยตรง
    store_answer = _build_store_info_answer(normalized_intent)
    if store_answer:
        return {
            "title": faq_data.get("title", normalized_intent),
            "content": store_answer,
            "answer": store_answer,
            "matched": True,
            "intent": normalized_intent,
            "label": normalized_intent,
            "canonical_intent": normalized_intent,
            "requires_human": faq_data.get("requires_human", False),
            "handoff_note": faq_data.get("handoff_note"),
            "keywords": faq_data.get("keywords", []),
            "examples": faq_data.get("examples", []),
            "category": faq_data.get("category", "store_info"),
            "source": "store_info_json"
        }

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
        "examples": faq_data.get("examples", []),
        "category": faq_data.get("category", "general"),
        "source": "knowledge_base_json"
    }


