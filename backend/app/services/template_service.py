TEMPLATES = {
    "greeting": {
        "reply": (
            "สวัสดีค่ะ 🌷 "
            "ยินดีต้อนรับสู่ Pudding Petals นะคะ "
            "วันนี้ให้แอดมินช่วยดูเรื่องไหนดีคะ"
        ),
        "requires_human": False,
        "category": "general"
    },

    "menu_inquiry": {
        "reply": (
            "ที่ร้านมีทั้งเค้ก ขนมหวาน เบเกอรี่ "
            "และเครื่องดื่มเลยค่ะ 🍰✨ "
            "หากลูกค้าสนใจแนวไหนเป็นพิเศษ "
            "แอดมินช่วยแนะนำเพิ่มเติมได้เลยนะคะ"
        ),
        "requires_human": False,
        "category": "menu"
    },

    "price_inquiry": {
        "reply": (
            "ขอบคุณที่สนใจเมนูของร้านนะคะ 🌷 "
            "ราคาของแต่ละเมนูจะขึ้นอยู่กับขนาดและประเภทค่ะ "
            "ลูกค้าสามารถแจ้งเมนูที่สนใจเพิ่มเติมได้เลยนะคะ"
        ),
        "requires_human": False,
        "category": "menu"
    },

    "recommendation": {
        "reply": (
            "ถ้ายังเลือกไม่ถูก "
            "แอดมินแนะนำ Strawberry Garden Shortcake "
            "กับ Flower Milk Pudding เลยค่ะ 🍓✨ "
            "เป็นเมนูยอดนิยมและถ่ายรูปสวยมาก ๆ ค่ะ"
        ),
        "requires_human": False,
        "category": "recommendation"
    },

    "delivery_issue": {
        "reply": (
            "ขออภัยสำหรับความไม่สะดวกที่เกิดขึ้นนะคะ 🙏 "
            "รบกวนส่งรายละเอียดออเดอร์เพิ่มเติมให้แอดมินตรวจสอบได้เลยค่ะ"
        ),
        "requires_human": True,
        "category": "support"
    },

    "order_problem": {
        "reply": (
            "ต้องขออภัยจริง ๆ นะคะ "
            "หากสินค้าไม่ครบหรือได้รับผิดเมนู "
            "รบกวนส่งรูปสินค้าและเลขออเดอร์เพิ่มเติมให้แอดมินได้เลยค่ะ 🙏"
        ),
        "requires_human": True,
        "category": "support"
    },

    "refund_exchange": {
        "reply": (
            "ทางร้านต้องขออภัยสำหรับปัญหาที่เกิดขึ้นด้วยนะคะ "
            "รบกวนส่งเลขออเดอร์และรายละเอียดเพิ่มเติม "
            "เพื่อให้แอดมินช่วยตรวจสอบให้ค่ะ 🙏"
        ),
        "requires_human": True,
        "category": "support"
    },

    "complaint": {
        "reply": (
            "ต้องขออภัยจริง ๆ สำหรับประสบการณ์ที่เกิดขึ้นนะคะ "
            "แอดมินจะรีบรับเรื่องและช่วยตรวจสอบให้อย่างดีที่สุดค่ะ 🙏"
        ),
        "requires_human": True,
        "category": "risk"
    },

    "compliment": {
        "reply": (
            "ขอบคุณมาก ๆ เลยนะคะ 🌷 "
            "ดีใจมากที่ลูกค้าชอบขนมและบรรยากาศของร้านค่ะ "
            "คำชมของลูกค้าเป็นกำลังใจให้ทีมงานมากเลยค่ะ"
        ),
        "requires_human": False,
        "category": "positive"
    },

    "reservation": {
        "reply": (
            "สามารถจองโต๊ะได้ค่ะ 🌷 "
            "รบกวนแจ้งวัน เวลา และจำนวนคน "
            "ให้แอดมินช่วยตรวจสอบโต๊ะว่างให้นะคะ"
        ),
        "requires_human": True,
        "category": "reservation"
    },

    "custom_cake": {
        "reply": (
            "ทางร้านมีบริการเค้กวันเกิดและเค้กสั่งทำค่ะ 🎂✨ "
            "ลูกค้าสามารถแจ้งธีม สี หรือข้อความหน้าเค้กเพิ่มเติมได้เลยนะคะ"
        ),
        "requires_human": True,
        "category": "custom_order"
    },

    "human_required": {
        "reply": (
            "ได้เลยค่ะ 🌷 "
            "แอดมินจะรับเรื่องไว้และช่วยดูแลต่อให้นะคะ "
            "รบกวนฝากรายละเอียดเพิ่มเติมไว้ได้เลยค่ะ"
        ),
        "requires_human": True,
        "category": "risk"
    },

    "general_question": {
        "reply": (
            "ขอบคุณที่ติดต่อเข้ามานะคะ 🌷 "
            "ทางร้านยินดีช่วยดูแลค่ะ "
            "ลูกค้าสามารถแจ้งรายละเอียดเพิ่มเติมได้เลยนะคะ"
        ),
        "requires_human": False,
        "category": "general"
    }
}


def select_template(intent):
    intent = str(intent or "").strip()

    result = TEMPLATES.get(
        intent,
        TEMPLATES["general_question"]
    )

    return {
        "intent": intent,
        "reply": result.get("reply"),
        "requires_human": result.get("requires_human", False),
        "category": result.get("category", "general")
    }