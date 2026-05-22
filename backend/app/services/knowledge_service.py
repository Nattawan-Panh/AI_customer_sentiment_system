import json
from pathlib import Path
from functools import lru_cache


BASE_DIR = Path(__file__).resolve().parents[2]
KNOWLEDGE_PATH = BASE_DIR / "data" / "sample_knowledge.json"


@lru_cache(maxsize=1)
def load_knowledge_base() -> dict:
    with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def get_store_info() -> dict:
    kb = load_knowledge_base()
    return kb.get("STORE_INFO", {})


def get_delivery_info() -> dict:
    kb = load_knowledge_base()
    return kb.get("DELIVERY_INFO", {})


def get_menu_items() -> list:
    kb = load_knowledge_base()
    return kb.get("MENU_ITEMS", [])


def get_faq() -> dict:
    kb = load_knowledge_base()
    return kb.get("FAQ", {})


def get_faq_answer(intent_label: str) -> dict:
    faq = get_faq()
    intent_label = str(intent_label or "general").strip()

    return faq.get(
        intent_label,
        faq.get("general", {
            "answer": "ได้เลยค่ะ แอดมินยินดีช่วยดูให้นะคะ ลูกค้าสามารถบอกรายละเอียดเพิ่มเติมได้เลยค่ะ",
            "requires_human": False,
            "handoff_note": None,
            "keywords": []
        })
    )


def get_available_menu_items(category: str = None) -> list:
    menu_items = get_menu_items()

    results = [
        item for item in menu_items
        if item.get("available") is True
    ]

    if category:
        category = category.lower().strip()
        results = [
            item for item in results
            if item.get("category", "").lower() == category
        ]

    return results


def find_menu_by_keyword(keyword: str) -> list:
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

    return {
        intent
        for intent, data in faq.items()
        if data.get("requires_human") is True
    }


def is_human_required(intent_label: str) -> bool:
    faq_data = get_faq_answer(intent_label)
    return faq_data.get("requires_human") is True


def get_handoff_note(intent_label: str):
    faq_data = get_faq_answer(intent_label)
    return faq_data.get("handoff_note")


def search_faq_by_keyword(text: str) -> dict:
    text = str(text or "").lower().strip()
    faq = get_faq()

    if not text:
        return get_faq_answer("general")

    for intent, data in faq.items():
        keywords = data.get("keywords", [])

        if any(keyword.lower() in text for keyword in keywords):
            return {
                "intent": intent,
                **data
            }

    return {
        "intent": "general",
        **get_faq_answer("general")
    }


def retrieve_knowledge(intent_label: str = "general", text: str = "") -> dict:
    """
    Retrieve knowledge for pipeline_service.py
    Returns: title, content, matched
    """
    intent_label = str(intent_label or "general").strip()
    text = str(text or "").strip()

    faq_data = get_faq_answer(intent_label)

    if intent_label == "general" and text:
        faq_data = search_faq_by_keyword(text)

    content = faq_data.get("answer", "")

    return {
        "title": intent_label,
        "content": content,
        "matched": True if content else False,
        "requires_human": faq_data.get("requires_human", False),
        "handoff_note": faq_data.get("handoff_note"),
        "keywords": faq_data.get("keywords", [])
    }

def reload_knowledge_base():
    load_knowledge_base.cache_clear()
    return load_knowledge_base()