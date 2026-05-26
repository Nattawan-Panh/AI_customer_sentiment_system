from typing import Any, Dict, Optional

from app.services.knowledge_service import (
    normalize_intent_label,
    retrieve_knowledge,
    is_human_required as knowledge_is_human_required,
)


# =========================================================
# DEFAULT CONFIG
# คงชื่อตัวแปรเดิม เพื่อให้ไฟล์อื่นที่ import อยู่ไม่พัง
# =========================================================

DEFAULT_INTENT = "general_question"


# =========================================================
# FALLBACK TEMPLATES
# ใช้เฉพาะกรณี knowledge_service หาไม่เจอ / JSON โหลดไม่ได้
# ไม่ควรใส่ข้อมูลราคา เมนู หรือข้อมูลร้านจริงเยอะเกินไปที่นี่
# =========================================================

TEMPLATES = {
    "greeting": {
        "reply": (
            "สวัสดีค่ะ 🌷 ยินดีต้อนรับสู่ Pudding Petals Cafe "
            "คาเฟ่ขนมหวานท่ามกลางสวนดอกไม้นะคะ "
            "วันนี้ให้แอดมินช่วยดูเรื่องไหนดีคะ"
        ),
        "requires_human": False,
        "category": "general",
        "handoff_note": None
    },

    "thanks": {
        "reply": (
            "ยินดีมาก ๆ ค่ะ 🌷 "
            "ขอบคุณที่ติดต่อ Pudding Petals Cafe นะคะ"
        ),
        "requires_human": False,
        "category": "general",
        "handoff_note": None
    },

    "general_question": {
        "reply": (
            "ได้เลยค่ะ 🌷 แอดมินยินดีช่วยดูให้นะคะ "
            "ลูกค้าสามารถบอกรายละเอียดเพิ่มเติมได้เลยค่ะ"
        ),
        "requires_human": False,
        "category": "general",
        "handoff_note": None
    },

    "empty_message": {
        "reply": (
            "Pudding Petals Cafe ยินดีให้บริการค่ะ 🌷 "
            "หากต้องการสอบถามเมนู ราคา โปรโมชัน การจองโต๊ะ หรือเดลิเวอรี่ "
            "สามารถพิมพ์ข้อความมาได้เลยนะคะ"
        ),
        "requires_human": False,
        "category": "general",
        "handoff_note": None
    },

    "service_question": {
        "reply": (
            "Pudding Petals Cafe ยินดีให้บริการข้อมูลเกี่ยวกับเมนู ราคา โปรโมชัน "
            "การจองโต๊ะ เดลิเวอรี่ และข้อมูลร้านค่ะ 🌷"
        ),
        "requires_human": False,
        "category": "general",
        "handoff_note": None
    },

    "promotion": {
        "reply": (
            "โปรโมชันของร้านอาจเปลี่ยนตามช่วงเวลาค่ะ 🌷 "
            "ลูกค้าสามารถสอบถามโปรล่าสุดกับแอดมินได้เลยนะคะ"
        ),
        "requires_human": False,
        "category": "menu",
        "handoff_note": None
    },

    "recommendation": {
        "reply": (
            "ถ้าเพิ่งมาครั้งแรก แอดมินแนะนำเมนู signature หรือเมนูขายดีของร้านค่ะ 🌷 "
            "ลูกค้าบอกได้เลยนะคะว่าชอบหวานน้อย ชอบถ่ายรูป หรืออยากได้เมนูสำหรับโอกาสพิเศษ"
        ),
        "requires_human": False,
        "category": "menu",
        "handoff_note": None
    },

    "menu_inquiry": {
        "reply": (
            "ที่ร้านมีทั้งเค้ก ขนมหวาน เบเกอรี่ และเครื่องดื่มค่ะ 🍰✨ "
            "หากสนใจเมนูไหนเป็นพิเศษ สามารถถามราคา ขนาด หรือส่วนผสมได้เลยนะคะ"
        ),
        "requires_human": False,
        "category": "menu",
        "handoff_note": None
    },

    "price_inquiry": {
        "reply": (
            "ราคาของเมนูจะแตกต่างกันตามประเภทและขนาดค่ะ 🌷 "
            "ลูกค้าสามารถแจ้งชื่อเมนูที่สนใจได้เลยนะคะ เดี๋ยวแอดมินช่วยดูราคาให้ค่ะ"
        ),
        "requires_human": False,
        "category": "menu",
        "handoff_note": None
    },

    "size_option": {
        "reply": (
            "เมนูของร้านมีหลายขนาดให้เลือกค่ะ 🌷 "
            "เช่น Mini, Regular, Set หรือ Whole Cake ตามประเภทของเมนูค่ะ"
        ),
        "requires_human": False,
        "category": "menu",
        "handoff_note": None
    },

    "availability": {
        "reply": (
            "เมนูบางรายการอาจมีจำนวนจำกัดในแต่ละวันค่ะ 🌷 "
            "หากสนใจเมนูไหนเป็นพิเศษ แอดมินช่วยเช็กให้ได้ค่ะ"
        ),
        "requires_human": True,
        "category": "menu",
        "handoff_note": "ให้แอดมินตรวจสอบสต็อกหรือจำนวนสินค้าที่พร้อมขาย"
    },

    "opening_hours": {
        "reply": (
            "ร้าน Pudding Petals Cafe เปิดทุกวันค่ะ 🌷 "
            "สามารถสอบถามเวลาเปิด-ปิดล่าสุดกับแอดมินได้เลยนะคะ"
        ),
        "requires_human": False,
        "category": "store_info",
        "handoff_note": None
    },

    "location": {
        "reply": (
            "ร้าน Pudding Petals Cafe อยู่ราชพฤกษ์ค่ะ 🌷 "
        ),
        "requires_human": False,
        "category": "store_info",
        "handoff_note": None
    },

    "reservation": {
        "reply": (
            "สามารถสอบถามโต๊ะว่างหรือจองโต๊ะกับแอดมินได้เลยค่ะ 🌷 "
            "รบกวนแจ้งวันที่ เวลา และจำนวนคนที่ต้องการเข้ามานะคะ"
        ),
        "requires_human": True,
        "category": "reservation",
        "handoff_note": "ส่งต่อแอดมินเพื่อเช็กโต๊ะว่าง วันที่ เวลา จำนวนคน และโซนที่ต้องการ"
    },

    "ambience_photo_spot": {
        "reply": (
            "Pudding Petals Cafe เป็นคาเฟ่ขนมหวานท่ามกลางสวนดอกไม้ค่ะ 🌷 "
            "มีมุมถ่ายรูปหลายมุมทั้งโซน indoor และ outdoor ค่ะ"
        ),
        "requires_human": False,
        "category": "store_info",
        "handoff_note": None
    },

    "facility": {
        "reply": (
            "ที่ร้านมีสิ่งอำนวยความสะดวกสำหรับลูกค้าค่ะ 🌷 "
            "เช่น Wi-Fi ที่นั่ง indoor/outdoor และรายละเอียดอื่น ๆ สามารถสอบถามเพิ่มเติมได้เลยนะคะ"
        ),
        "requires_human": False,
        "category": "store_info",
        "handoff_note": None
    },

    "delivery_takeaway": {
        "reply": (
            "ทางร้านมีบริการเดลิเวอรี่และสั่งกลับบ้านค่ะ 🌷 "
            "ลูกค้าสามารถสอบถามช่องทางสั่งซื้อที่สะดวกได้เลยนะคะ"
        ),
        "requires_human": False,
        "category": "delivery",
        "handoff_note": None
    },

    "payment": {
        "reply": (
            "ทางร้านรับชำระเงินเป็นแบบสแกนจ่าย โอน และเงินสดค่ะ 🌷 "
        ),
        "requires_human": False,
        "category": "payment",
        "handoff_note": None
    },

    "order_status": {
        "reply": (
            "สำหรับสถานะออเดอร์ รบกวนลูกค้าส่งเลขออเดอร์หรือรายละเอียดการสั่งซื้อให้แอดมินตรวจสอบได้เลยค่ะ 🌷"
        ),
        "requires_human": True,
        "category": "support",
        "handoff_note": "ส่งต่อแอดมินเพื่อตรวจสอบสถานะออเดอร์"
    },

    "custom_cake": {
        "reply": (
            "ทางร้านมีเค้กสำหรับวันเกิดและโอกาสพิเศษค่ะ 🎂✨ "
            "รบกวนแจ้งแบบ ขนาด วันที่รับ และข้อความหน้าเค้กให้แอดมินช่วยดูรายละเอียดต่อนะคะ"
        ),
        "requires_human": True,
        "category": "custom_order",
        "handoff_note": "ส่งต่อแอดมินเพื่อสอบถามแบบเค้ก ขนาด วันรับสินค้า และข้อความหน้าเค้ก"
    },

    "special_occasion": {
        "reply": (
            "สำหรับโอกาสพิเศษ เช่น วันเกิด วันครบรอบ ของขวัญ หรือของฝาก "
            "แอดมินช่วยแนะนำเมนูที่เหมาะให้ได้ค่ะ 🌷"
        ),
        "requires_human": False,
        "category": "special_occasion",
        "handoff_note": None
    },

    "packaging": {
        "reply": (
            "ทางร้านสามารถช่วยดูเรื่องแพ็กขนม กล่อง ถุง หรือแพ็กของขวัญได้ค่ะ 🌷 "
            "รบกวนแจ้งรูปแบบที่ต้องการเพิ่มเติมนะคะ"
        ),
        "requires_human": True,
        "category": "packaging",
        "handoff_note": "ส่งต่อแอดมินหากลูกค้าต้องการแพ็กของขวัญหรือรายละเอียดแพ็กเกจพิเศษ"
    },

    "sweetness_adjustment": {
        "reply": (
            "เครื่องดื่มบางเมนูสามารถเลือกระดับความหวานได้ค่ะ 🌷 "
            "ส่วนขนมและเค้กจะมีความหวานตามสูตรของร้านค่ะ"
        ),
        "requires_human": False,
        "category": "menu_safety",
        "handoff_note": None
    },

    "allergy": {
        "reply": (
            "หากลูกค้ามีอาการแพ้อาหาร เช่น แพ้นม ไข่ ถั่ว หรือกลูเตน "
            "รบกวนแจ้งแอดมินก่อนสั่งทุกครั้งนะคะ 🌷 "
            "ทางร้านจะช่วยตรวจสอบส่วนผสมให้ละเอียดก่อนค่ะ"
        ),
        "requires_human": True,
        "category": "menu_safety",
        "handoff_note": "ส่งต่อแอดมินทันทีหากลูกค้ามีอาการแพ้อาหารหรือข้อจำกัดด้านวัตถุดิบ"
    },

    "ingredients": {
        "reply": (
            "ส่วนผสมของแต่ละเมนูจะแตกต่างกันค่ะ 🌷 "
            "หากลูกค้าต้องการตรวจสอบเมนูใดเป็นพิเศษ แจ้งชื่อเมนูให้แอดมินได้เลยค่ะ"
        ),
        "requires_human": True,
        "category": "menu_safety",
        "handoff_note": "ส่งต่อแอดมินเพื่อเช็กส่วนผสมเฉพาะเมนู"
    },

    "dietary_option": {
        "reply": (
            "สำหรับตัวเลือกอาหารพิเศษ เช่น vegan, vegetarian, halal, keto, low sugar, "
            "gluten-free หรือ lactose-free จำเป็นต้องตรวจสอบตามวัตถุดิบของแต่ละเมนูก่อนค่ะ 🌷"
        ),
        "requires_human": True,
        "category": "menu_safety",
        "handoff_note": "ส่งต่อแอดมินเพื่อตรวจสอบตัวเลือกอาหารพิเศษตามวัตถุดิบจริง"
    },

    "compliment": {
        "reply": (
            "ขอบคุณมาก ๆ เลยค่ะ 🌷 "
            "ดีใจมากที่ลูกค้าชอบขนม เครื่องดื่ม และบรรยากาศของร้านนะคะ"
        ),
        "requires_human": False,
        "category": "positive",
        "handoff_note": None
    },

    "complaint_product": {
        "reply": (
            "ทางร้านต้องขออภัยอย่างมากสำหรับประสบการณ์ที่ไม่ดีเกี่ยวกับสินค้านะคะ 🙏 "
            "รบกวนลูกค้าส่งเลขออเดอร์ รูปสินค้า และรายละเอียดปัญหาเพิ่มเติมได้เลยค่ะ"
        ),
        "requires_human": True,
        "category": "support",
        "handoff_note": "ส่งต่อแอดมินเพื่อตรวจสอบเลขออเดอร์ รูปสินค้า และรายละเอียดปัญหา"
    },

    "complaint_service": {
        "reply": (
            "ทางร้านต้องขออภัยอย่างจริงใจสำหรับประสบการณ์ด้านการบริการนะคะ 🙏 "
            "แอดมินจะรับเรื่องไว้ตรวจสอบและนำไปปรับปรุงให้ดีขึ้นค่ะ"
        ),
        "requires_human": True,
        "category": "support",
        "handoff_note": "ส่งต่อแอดมินเพื่อตรวจสอบเหตุการณ์ด้านการบริการ"
    },

    "complaint_staff": {
        "reply": (
            "ทางร้านต้องขออภัยอย่างจริงใจสำหรับเหตุการณ์ที่เกี่ยวข้องกับพนักงานนะคะ 🙏 "
            "แอดมินจะรับเรื่องไว้ตรวจสอบอย่างเหมาะสมค่ะ"
        ),
        "requires_human": True,
        "category": "support",
        "handoff_note": "ส่งต่อแอดมินเพื่อตรวจสอบเหตุการณ์ที่เกี่ยวข้องกับพนักงาน"
    },

    "refund_return": {
        "reply": (
            "กรณีคืนเงิน เปลี่ยนสินค้า เคลม หรือยกเลิกออเดอร์ "
            "ทางร้านขอรับรายละเอียดไว้ตรวจสอบก่อนนะคะ 🙏"
        ),
        "requires_human": True,
        "category": "support",
        "handoff_note": "ส่งต่อแอดมินเพื่อตรวจสอบเงื่อนไขการคืนเงิน เปลี่ยนสินค้า หรือเคลมสินค้า"
    },

    "high_risk_complaint": {
        "reply": (
            "ทางร้านต้องขออภัยอย่างสูงสำหรับเหตุการณ์ที่เกิดขึ้นนะคะ 🙏 "
            "กรณีนี้เป็นเคสเร่งด่วน แอดมินจะส่งต่อให้ผู้เกี่ยวข้องตรวจสอบทันทีค่ะ"
        ),
        "requires_human": True,
        "category": "risk",
        "handoff_note": "เคสเสี่ยงสูง ต้องส่งต่อแอดมินหรือผู้ดูแลทันที"
    }
}


# =========================================================
# INTENT ALIASES
# คงตัวแปรเดิมไว้ และ map ให้ตรงกับ knowledge_service
# =========================================================

TEMPLATE_ALIASES = {
    "general": "general_question",
    "unknown": "general_question",
    "fallback": "general_question",
    "other": "general_question",
    "none": "general_question",
    "null": "general_question",


    "sweetness_allergy": "sweetness_adjustment",


    "cafe_facilities": "facility",
    "photo_spot": "ambience_photo_spot",
    "delivery_platform": "delivery_takeaway",
    "delivery_issue": "order_status",
    "order_problem": "complaint_product",
    "refund_exchange": "refund_return",
    "complaint": "complaint_service",
    "human_required": "high_risk_complaint",


    "staff_complaint": "complaint_staff",
    "service_complaint": "complaint_service",
    "product_complaint": "complaint_product",
    "negative_feedback": "complaint_service",


    "menu": "menu_inquiry",
    "ask_menu": "menu_inquiry",
    "menu_question": "menu_inquiry",


    "price": "price_inquiry",
    "ask_price": "price_inquiry",

    "size": "size_option",
    "sizes": "size_option",


    "hours": "opening_hours",
    "open_hours": "opening_hours",
    "business_hours": "opening_hours",

    "store_location": "location",
    "map": "location",

    "delivery": "delivery_takeaway",
    "takeaway": "delivery_takeaway",

    "ingredient": "ingredients",
    "allergens": "allergy",

    "ambience": "ambience_photo_spot",
    "photo": "ambience_photo_spot",
    "facilities": "facility",

    "booking": "reservation",
    "table_booking": "reservation",

    "payment_method": "payment",
    "pay": "payment",


    "custom_order": "custom_cake",
    "birthday_cake": "custom_cake",


    "refund": "refund_return",
    "return": "refund_return",
    "cancel_order": "refund_return",

    "urgent": "high_risk_complaint",
    "legal_threat": "high_risk_complaint",
    "food_poisoning": "high_risk_complaint",


    "collab": "collaboration",
    "influencer": "collaboration",
    "event": "event_booking",
    "private_event": "event_booking",
    "social": "social_media",
    "queue": "queue_waiting",
    "waiting": "queue_waiting"
}


# =========================================================
# NORMALIZE INTENT
# =========================================================

def normalize_template_intent(intent):
    """
    คงชื่อฟังก์ชันเดิมไว้
    ใช้ normalize_intent_label จาก knowledge_service เป็นหลัก
    """
    if isinstance(intent, dict):
        raw_intent = (
            intent.get("canonical_intent")
            or intent.get("intent")
            or intent.get("label")
            or intent.get("risk_intent")
            or intent.get("predicted_intent")
            or DEFAULT_INTENT
        )
    else:
        raw_intent = intent

    raw_intent = str(raw_intent or DEFAULT_INTENT).strip().lower()

    if not raw_intent:
        raw_intent = DEFAULT_INTENT

    raw_intent = TEMPLATE_ALIASES.get(raw_intent, raw_intent)

    return normalize_intent_label(raw_intent)


# =========================================================
# INTERNAL HELPERS
# =========================================================

def _fallback_template(intent: str) -> Dict[str, Any]:
    normalized_intent = normalize_template_intent(intent)

    item = TEMPLATES.get(normalized_intent)

    if not item:
        item = TEMPLATES[DEFAULT_INTENT]
        normalized_intent = DEFAULT_INTENT

    return {
        "intent": normalized_intent,
        "reply": item.get("reply"),
        "requires_human": item.get("requires_human", False),
        "category": item.get("category", "general"),
        "handoff_note": item.get("handoff_note")
    }


def _knowledge_to_template_result(knowledge: Dict[str, Any], fallback: Dict[str, Any]) -> Dict[str, Any]:
    answer = (
        knowledge.get("answer")
        or knowledge.get("content")
        or fallback.get("reply")
    )

    return {
        "intent": knowledge.get("canonical_intent") or knowledge.get("intent") or fallback.get("intent"),
        "reply": answer,
        "requires_human": bool(
            knowledge.get("requires_human")
            if "requires_human" in knowledge
            else fallback.get("requires_human", False)
        ),
        "category": knowledge.get("category") or fallback.get("category", "general"),
        "handoff_note": knowledge.get("handoff_note") or fallback.get("handoff_note"),
        "source": knowledge.get("source", "knowledge_service")
    }


# =========================================================
# MAIN SELECT TEMPLATE
# ใช้แทนของเดิมได้เลย
# =========================================================

def select_template(
    intent,
    knowledge_base=None,
    customer_text=None,
    matched_menu=None,
    sentiment_label=None,
    risk_level=None
):
    
    normalized_intent = normalize_template_intent(intent)

    if isinstance(knowledge_base, dict):
        knowledge_reply = (
            knowledge_base.get("answer")
            or knowledge_base.get("content")
            or ""
        ).strip()

        if knowledge_base.get("matched") and knowledge_reply:
            return {
                "reply": knowledge_reply,
                "source": knowledge_base.get("source", "sample_knowledge_json"),
                "intent": normalized_intent,
                "used_knowledge": True
            }

    return _fallback_template(normalized_intent)


# =========================================================
# OPTIONAL UTILS
# เผื่อไฟล์อื่นเรียกใช้
# =========================================================

def is_human_required(intent, customer_text: str = "") -> bool:
    try:
        return knowledge_is_human_required(
            normalize_template_intent(intent),
            customer_text
        )
    except Exception:
        template = select_template(intent, customer_text=customer_text)
        return bool(template.get("requires_human", False))


def get_template_reply(intent, customer_text: str = "") -> str:
    template = select_template(intent, customer_text=customer_text)
    return template.get("reply") or ""


def get_template_category(intent, customer_text: str = "") -> str:
    template = select_template(intent, customer_text=customer_text)
    return template.get("category") or "general"
