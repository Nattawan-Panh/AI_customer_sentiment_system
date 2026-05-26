# =========================================================
# SELECT TEMPLATE
# ใช้กับ pipeline_service.py
# ให้ priority กับ knowledge_base ก่อน fallback
# =========================================================

def _safe_template_str(value, default=""):
    if value is None:
        return default
    return str(value).strip()


def normalize_template_intent(intent):
    if isinstance(intent, dict):
        intent = (
            intent.get("canonical_intent")
            or intent.get("intent")
            or intent.get("label")
            or intent.get("predicted_intent")
            or "general_question"
        )

    intent = _safe_template_str(intent, "general_question").lower()

    if not intent:
        return "general_question"

    aliases = {
        "general": "general_question",
        "unknown": "general_question",
        "fallback": "general_question",
        "other": "general_question",

        "menu": "menu_inquiry",
        "ask_menu": "menu_inquiry",
        "menu_question": "menu_inquiry",

        "price": "price_inquiry",
        "ask_price": "price_inquiry",

        "drink_recommendation": "recommendation",
        "menu_recommendation": "recommendation",
        "ask_recommendation": "recommendation",
        "best_seller": "recommendation",
        "signature_menu": "recommendation",

        "delivery": "delivery_takeaway",
        "takeaway": "delivery_takeaway",

        "hours": "opening_hours",
        "open_hours": "opening_hours",
        "business_hours": "opening_hours",

        "map": "location",
        "store_location": "location",

        "complaint": "complaint_service",
        "refund": "refund_return",
        "return": "refund_return",
        "cancel_order": "refund_return",
        "human_required": "high_risk_complaint",
    }

    return aliases.get(intent, intent)


def _fallback_template(intent):
    normalized_intent = normalize_template_intent(intent)

    fallback_templates = {
        "greeting": "สวัสดีค่ะ ยินดีต้อนรับสู่ Pudding Petals นะคะ 🌷 วันนี้ให้แอดมินช่วยดูเรื่องไหนดีคะ",

        "thanks": "ยินดีมาก ๆ ค่ะ 🌷 ถ้ามีอะไรให้ Pudding Petals ช่วยดูเพิ่มเติม ทักมาได้เสมอนะคะ",

        "recommendation": "ที่ร้านมีเมนูแนะนำหลายรายการค่ะ 🌷 ถ้าหากลูกค้าชอบเค้กหวานๆ ขอแนะนำเป็น Strawberry Garden Shortcake เลยค่ะ",

        "menu_inquiry": "ที่ร้านมีเค้ก ขนมหวาน เบเกอรี่ และเครื่องดื่มค่ะ 🌷 หากลูกค้าสนใจเมนูไหนเป็นพิเศษ สามารถสอบถามชื่อเมนูหรือราคาได้เลยนะคะ",

        "price_inquiry": "ราคาเมนูจะแตกต่างกันตามประเภทและขนาดค่ะ 🌷 ลูกค้าสามารถแจ้งชื่อเมนูที่สนใจได้เลยนะคะ แอดมินจะช่วยดูราคาให้ค่ะ",

        "opening_hours": "ร้านเปิดทุกวันค่ะ เวลา 10:00 - 20:00 น. ค่ะ 🌷",

        "location": "ร้าน Pudding Petals Cafe ตั้งอยู่โซนราชพฤกษ์ค่ะ 🌷ะ",

        "reservation": "ลูกค้าสามารถ Walk-in ได้ หรือทักแชทเพื่อสอบถามโต๊ะว่างก่อนเข้ามาได้ค่ะ 🌷 ช่วงวันหยุดแนะนำจองล่วงหน้านะคะ",

        "delivery_takeaway": "ลูกค้าสามารถสั่งผ่าน GrabFood และ LineMan ได้ค่ะ 🌷",

        "payment": "ทางร้านรับชำระแบบเงินสด โอน และสแกนจ่ายค่ะ 🌷",

        "complaint_service": "ขออภัยในความไม่สะดวกนะคะ ทางร้านขอรับเรื่องไว้ตรวจสอบและให้แอดมินช่วยดูแลต่อให้นะคะ 🌷",

        "complaint_product": "ขออภัยที่สินค้าไม่เป็นไปตามที่คาดหวังนะคะ รบกวนแจ้งรายละเอียดออเดอร์หรือแนบรูปเพิ่มเติม เพื่อให้แอดมินช่วยตรวจสอบให้นะคะ 🌷",

        "refund_return": "ขออภัยในความไม่สะดวกนะคะ เรื่องคืนเงินหรือเปลี่ยนสินค้า แอดมินจะช่วยตรวจสอบเลขออเดอร์และรายละเอียดให้นะคะ 🌷",

        "allergy": "หากลูกค้ามีอาการแพ้อาหาร ทางร้านขอส่งต่อให้แอดมินช่วยตรวจสอบวัตถุดิบรายเมนูอย่างละเอียดก่อนนะคะ เพื่อความปลอดภัยที่สุดค่ะ 🌷",

        "general_question": "ได้เลยค่ะ แอดมินยินดีช่วยดูให้นะคะ 🌷 ลูกค้าสามารถบอกรายละเอียดเพิ่มเติมได้เลยค่ะ เช่น สนใจเมนู จองโต๊ะ ราคา หรือข้อมูลร้านด้านไหนเป็นพิเศษคะ",
    }

    reply = fallback_templates.get(
        normalized_intent,
        fallback_templates["general_question"]
    )

    return {
        "reply": reply,
        "source": "template_fallback",
        "intent": normalized_intent,
        "used_knowledge": False
    }


def select_template(
    intent,
    knowledge_base=None,
    customer_text=None,
    matched_menu=None,
    sentiment_label=None,
    risk_level=None
):
    """
    เลือกข้อความตั้งต้นสำหรับตอบลูกค้า

    Priority:
    1. ใช้คำตอบจาก knowledge_base ก่อน
    2. ถ้าไม่มี knowledge จริง ๆ ค่อยใช้ fallback template
    """

    normalized_intent = normalize_template_intent(intent)

    if isinstance(knowledge_base, dict):
        knowledge_reply = (
            knowledge_base.get("answer")
            or knowledge_base.get("content")
            or ""
        )

        knowledge_reply = str(knowledge_reply or "").strip()

        if knowledge_base.get("matched") and knowledge_reply:
            return {
                "reply": knowledge_reply,
                "source": knowledge_base.get("source", "knowledge_base_json"),
                "intent": normalized_intent,
                "used_knowledge": True,
                "matched_menu": knowledge_base.get("matched_menu")
            }

    return _fallback_template(normalized_intent)



