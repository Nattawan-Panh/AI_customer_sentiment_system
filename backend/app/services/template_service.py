TEMPLATES = {
    "greeting": {
        "reply": (
            "สวัสดีค่ะ 🌷 "
            "ยินดีต้อนรับสู่ Pudding Petals Cafe คาเฟ่ขนมหวานบรรยากาศสวนดอกไม้นะคะ"
        ),
        "requires_human": False,
        "category": "general"
    },

    "thanks": {
        "reply": (
            "ยินดีมาก ๆ ค่ะ 🌷 "
            "ขอบคุณที่ติดต่อ Pudding Petals Cafe นะคะ"
        ),
        "requires_human": False,
        "category": "general"
    },

    "menu_inquiry": {
        "reply": (
            "ที่ร้านมีทั้งเค้ก ขนมหวาน เบเกอรี่ "
            "และเครื่องดื่มค่ะ 🍰✨"
        ),
        "requires_human": False,
        "category": "menu"
    },

    "recommendation": {
        "reply": (
            "เมนูแนะนำของร้านมีทั้งเค้ก ขนมหวาน "
            "และเครื่องดื่มที่เข้ากับบรรยากาศสวนดอกไม้ค่ะ 🌷"
        ),
        "requires_human": False,
        "category": "recommendation"
    },

    "promotion": {
        "reply": (
            "ตอนนี้ทางร้านมีโปรโมชันสำหรับเมนูขนมและเครื่องดื่มค่ะ 🌷 "
            "เหมาะสำหรับลูกค้าที่อยากทานขนมหวานคู่กับเครื่องดื่มในบรรยากาศสวนดอกไม้ค่ะ"
        ),
        "requires_human": False,
        "category": "promotion"
    },

    "price_inquiry": {
        "reply": (
            "ราคาของเมนูที่ร้านจะแตกต่างกันตามประเภทและขนาดค่ะ 🌷 "
            "มีทั้งขนาด Mini, Regular, Whole Cake และแบบ Set ในบางเมนูค่ะ"
        ),
        "requires_human": False,
        "category": "menu"
    },

    "size_option": {
        "reply": (
            "เมนูของร้านมีหลายขนาดให้เลือกค่ะ 🌷 "
            "เช่น Mini, Regular, Whole Cake หรือแบบ Set ตามประเภทของเมนูค่ะ"
        ),
        "requires_human": False,
        "category": "menu"
    },

    "availability": {
        "reply": (
            "เมนูขนมและเบเกอรี่บางรายการอาจมีจำนวนจำกัดในแต่ละวันค่ะ 🌷 "
            "ทางร้านจะเตรียมสดใหม่เพื่อคงคุณภาพของเมนูค่ะ"
        ),
        "requires_human": False,
        "category": "menu"
    },

    "opening_hours": {
        "reply": (
            "ร้าน Pudding Petals Cafe เปิดทุกวัน เวลา 10:00 - 20:00 น. ค่ะ 🌷"
        ),
        "requires_human": False,
        "category": "store_info"
    },

    "location": {
        "reply": (
            "ร้าน Pudding Petals Cafe ตั้งอยู่โซนราชพฤกษ์ค่ะ 🌷 "
            "เป็นคาเฟ่ขนมหวานบรรยากาศสวนดอกไม้ มีทั้งโซน indoor และ outdoor ค่ะ"
        ),
        "requires_human": False,
        "category": "store_info"
    },

    "reservation": {
        "reply": (
            "ร้านสามารถ Walk-in ได้ตามปกติค่ะ 🌷 "
            "หากเป็นช่วงวันหยุดหรือมากันหลายคน แนะนำจองล่วงหน้าเล็กน้อยนะคะ"
        ),
        "requires_human": True,
        "category": "reservation"
    },

    "delivery_takeaway": {
        "reply": (
            "ทางร้านมีบริการเดลิเวอรี่ผ่าน GrabFood และ LINE MAN ค่ะ 🌷 "
            "และสามารถสั่งกลับบ้านหรือรับเองได้ตามความสะดวกค่ะ"
        ),
        "requires_human": False,
        "category": "delivery"
    },

    "payment": {
        "reply": (
            "ทางร้านรองรับการชำระเงินตามช่องทางที่ร้านกำหนดค่ะ 🌷 "
            "หากเป็นออเดอร์พิเศษ แอดมินจะแจ้งรายละเอียดการชำระเงินให้ชัดเจนค่ะ"
        ),
        "requires_human": True,
        "category": "payment"
    },

    "order_status": {
        "reply": (
            "สำหรับสถานะออเดอร์เดลิเวอรี่ ลูกค้าสามารถตรวจสอบผ่านแอปที่สั่งซื้อได้ค่ะ 🌷 "
            "หากเป็นปัญหาเกี่ยวกับสินค้า ทางร้านจะช่วยตรวจสอบให้ค่ะ"
        ),
        "requires_human": True,
        "category": "support"
    },

    "custom_cake": {
        "reply": (
            "ทางร้านมีเมนูเค้กที่เหมาะสำหรับวันเกิดและโอกาสพิเศษค่ะ 🎂✨ "
            "เช่น เค้กแบบ Whole Cake สำหรับ 4-6 คนค่ะ"
        ),
        "requires_human": True,
        "category": "custom_order"
    },

    "special_occasion": {
        "reply": (
            "สำหรับโอกาสพิเศษ เช่น วันเกิด วันครบรอบ ของขวัญ หรือของฝาก "
            "ทางร้านมีเมนูขนมหวานและเค้กที่เหมาะกับบรรยากาศละมุน ๆ ค่ะ 🌷"
        ),
        "requires_human": False,
        "category": "special_occasion"
    },

    "packaging": {
        "reply": (
            "ทางร้านแพ็กขนมและเครื่องดื่มอย่างระมัดระวังค่ะ 🌷 "
            "หากต้องการแพ็กเป็นของขวัญหรือรับกลับบ้าน สามารถแจ้งเพิ่มเติมได้ค่ะ"
        ),
        "requires_human": True,
        "category": "packaging"
    },

    "sweetness_adjustment": {
        "reply": (
            "เครื่องดื่มบางเมนูสามารถเลือกระดับความหวานได้ค่ะ 🌷 "
            "ส่วนขนมและเค้กจะมีความหวานตามสูตรของร้านค่ะ"
        ),
        "requires_human": False,
        "category": "menu_safety"
    },

    "allergy": {
        "reply": (
            "หากลูกค้ามีอาการแพ้อาหาร เช่น แพ้นม ไข่ ถั่ว หรือกลูเตน "
            "ทางร้านแนะนำให้ตรวจสอบส่วนผสมก่อนสั่งนะคะ 🌷"
        ),
        "requires_human": True,
        "category": "menu_safety"
    },

    "ingredients": {
        "reply": (
            "เมนูขนมหวานและเบเกอรี่ของร้านมีส่วนผสมแตกต่างกันค่ะ 🌷 "
            "บางเมนูอาจมีนม ไข่ เนย ครีม กลูเตน หรือถั่วค่ะ"
        ),
        "requires_human": True,
        "category": "menu_safety"
    },

    "dietary_option": {
        "reply": (
            "สำหรับตัวเลือกอาหารพิเศษ เช่น vegan, halal, keto, gluten-free หรือ dairy-free "
            "จำเป็นต้องตรวจสอบตามวัตถุดิบของแต่ละเมนูก่อนค่ะ 🌷"
        ),
        "requires_human": True,
        "category": "menu_safety"
    },

    "ambience_photo_spot": {
        "reply": (
            "Pudding Petals Cafe เป็นคาเฟ่บรรยากาศสวนดอกไม้ค่ะ 🌷 "
            "มีทั้งโซน indoor และ outdoor พร้อมมุมถ่ายรูปหลายมุมค่ะ"
        ),
        "requires_human": False,
        "category": "store_info"
    },

    "facility": {
        "reply": (
            "ที่ร้านมี Wi-Fi มีปลั๊กบางจุดในโซน indoor "
            "มีที่จอดรถจำนวนจำกัด และโซน outdoor สามารถพาสัตว์เลี้ยงมาได้ค่ะ 🌷"
        ),
        "requires_human": False,
        "category": "store_info"
    },

    "compliment": {
        "reply": (
            "ขอบคุณมาก ๆ เลยค่ะ 🌷 "
            "ดีใจมากที่ลูกค้าชอบขนม เครื่องดื่ม และบรรยากาศของร้านค่ะ"
        ),
        "requires_human": False,
        "category": "positive"
    },

    "complaint_product": {
        "reply": (
            "ทางร้านขออภัยอย่างมากสำหรับประสบการณ์ที่ไม่ดีค่ะ 🙏 "
            "ทางร้านจะรับเรื่องเกี่ยวกับสินค้าไว้ตรวจสอบและดูแลต่ออย่างเหมาะสมค่ะ"
        ),
        "requires_human": True,
        "category": "support"
    },

    "complaint_service": {
        "reply": (
            "ทางร้านขออภัยอย่างจริงใจสำหรับประสบการณ์ด้านการบริการค่ะ 🙏 "
            "ทางร้านจะรับเรื่องไว้ตรวจสอบกับทีมงานและปรับปรุงการบริการให้ดีขึ้นค่ะ"
        ),
        "requires_human": True,
        "category": "support"
    },

    "complaint_staff": {
        "reply": (
            "ทางร้านขออภัยอย่างจริงใจสำหรับเหตุการณ์ที่เกี่ยวข้องกับพนักงานค่ะ 🙏 "
            "ทางร้านจะรับเรื่องไว้ตรวจสอบและปรับปรุงการสื่อสารให้เหมาะสมมากขึ้นค่ะ"
        ),
        "requires_human": True,
        "category": "support"
    },

    "refund_return": {
        "reply": (
            "กรณีคืนเงิน เปลี่ยนสินค้า เคลม หรือยกเลิกออเดอร์ "
            "ทางร้านจะรับเรื่องไว้ตรวจสอบตามรายละเอียดและเงื่อนไขของร้านค่ะ 🙏"
        ),
        "requires_human": True,
        "category": "support"
    },

    "high_risk_complaint": {
        "reply": (
            "ทางร้านขออภัยอย่างสูงสำหรับเหตุการณ์ที่เกิดขึ้นค่ะ 🙏 "
            "กรณีนี้เป็นเคสเร่งด่วน ทางร้านจะส่งต่อให้แอดมินตรวจสอบทันทีค่ะ"
        ),
        "requires_human": True,
        "category": "risk"
    },

    "empty_message": {
        "reply": (
            "Pudding Petals Cafe ยินดีให้บริการค่ะ 🌷 "
            "ร้านมีเมนูเค้ก ขนมหวาน เบเกอรี่ เครื่องดื่ม และบรรยากาศสวนดอกไม้ค่ะ"
        ),
        "requires_human": False,
        "category": "general"
    },

    "service_question": {
        "reply": (
            "Pudding Petals Cafe ยินดีให้บริการข้อมูลเกี่ยวกับเมนู ราคา โปรโมชัน "
            "การจองโต๊ะ เดลิเวอรี่ และข้อมูลร้านค่ะ 🌷"
        ),
        "requires_human": False,
        "category": "general"
    },

    "general_question": {
        "reply": (
            "ขอบคุณที่ติดต่อเข้ามานะคะ 🌷 "
            "Pudding Petals Cafe เป็นคาเฟ่ขนมหวานบรรยากาศสวนดอกไม้ "
            "มีเค้ก ขนมหวาน เบเกอรี่ และเครื่องดื่มค่ะ"
        ),
        "requires_human": False,
        "category": "general"
    }
}


TEMPLATE_ALIASES = {
    "general": "general_question",
    "unknown": "general_question",
    "fallback": "general_question",
    "other": "general_question",

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


def normalize_template_intent(intent):
    if isinstance(intent, dict):
        intent = (
            intent.get("canonical_intent")
            or intent.get("intent")
            or intent.get("label")
            or intent.get("risk_intent")
            or "general_question"
        )

    intent = str(intent or "general_question").strip()

    if not intent:
        intent = "general_question"

    return TEMPLATE_ALIASES.get(intent, intent)


def select_template(intent):
    normalized_intent = normalize_template_intent(intent)

    result = TEMPLATES.get(
        normalized_intent,
        TEMPLATES["general_question"]
    )

    return {
        "intent": normalized_intent,
        "reply": result.get("reply"),
        "requires_human": result.get("requires_human", False),
        "category": result.get("category", "general")
    }