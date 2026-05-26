import re
from typing import Dict, List, Tuple


# =========================================================
# Intent Service for Pudding Petals Cafe
# Brand: Flower Garden Dessert Cafe
# Tone: polite, warm, soft, friendly, feminine, pastel floral mood
# =========================================================


def normalize_text(text: str) -> str:
    """
    Normalize customer text for rule-based intent detection.
    - lower case
    - remove extra spaces
    - normalize Thai polite particles lightly
    """
    text = str(text or "").strip().lower()
    text = re.sub(r"\s+", " ", text)

    replacements = {
        "โปรโมชัน": "โปรโมชั่น",
        "โปรโมชั่น": "โปรโมชั่น",
        "โปรฯ": "โปรโมชั่น",
        "เค๊ก": "เค้ก",
        "คาเฟ": "คาเฟ่",
        "เมนูู": "เมนู",
        "มั้ย": "ไหม",
        "มะ": "ไหม",
        "ป่ะ": "ไหม",
        "ป่าว": "ไหม",
        "รึ": "หรือ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def contains_any(text: str, keywords: List[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def count_matches(text: str, keywords: List[str]) -> int:
    return sum(1 for keyword in keywords if keyword in text)


# ---------------------------------------------------------
# High priority intents
# These should be checked first to prevent wrong matching.
# Example:
# "ช่วงนี้มีโปรโมชั่นไหมคะ" must be promotion, not allergy.
# ---------------------------------------------------------

INTENT_RULES: List[Dict] = [
    {
        "label": "promotion",
        "priority": 100,
        "confidence": 0.95,
        "keywords": [
            "โปรโมชั่น",
            "โปร",
            "ส่วนลด",
            "ลดราคา",
            "มีโปรไหม",
            "มีโปรอะไร",
            "โปรวันนี้",
            "โปรช่วงนี้",
            "จัดโปร",
            "ราคาพิเศษ",
            "ซื้อคู่",
            "ซื้อคู่กับเครื่องดื่ม",
            "แถม",
            "คูปอง",
            "voucher",
            "discount",
            "sale",
            "deal",
            "แพ็กคู่",
            "เซตโปรโมชั่น",
            "เซ็ตโปรโมชั่น",
            "โปร 149",
            "149",
        ],
        "examples": [
            "ช่วงนี้มีโปรโมชั่นไหมคะ",
            "มีโปรอะไรบ้าง",
            "วันนี้มีส่วนลดไหม",
        ],
    },
    {
        "label": "opening_hours",
        "priority": 98,
        "confidence": 0.94,
        "keywords": [
            "เปิดกี่โมง",
            "ปิดกี่โมง",
            "ร้านเปิด",
            "ร้านปิด",
            "เวลาเปิด",
            "เวลาปิด",
            "เปิดถึงกี่โมง",
            "เปิดวันไหน",
            "ปิดวันไหน",
            "หยุดวันไหน",
            "วันนี้เปิดไหม",
            "พรุ่งนี้เปิดไหม",
            "เปิดทุกวันไหม",
            "เวลาให้บริการ",
            "เปิดบริการ",
            "close",
            "open",
            "opening hour",
            "business hour",
        ],
        "examples": [
            "ร้านเปิดกี่โมงคะ",
            "วันนี้ร้านเปิดไหม",
            "ปิดกี่โมงคะ",
        ],
    },
    {
        "label": "location",
        "priority": 96,
        "confidence": 0.93,
        "keywords": [
            "ร้านอยู่ที่ไหน",
            "อยู่ที่ไหน",
            "พิกัด",
            "โลเคชั่น",
            "location",
            "map",
            "แผนที่",
            "ไปยังไง",
            "เดินทางยังไง",
            "ทางไปร้าน",
            "สาขา",
            "อยู่แถวไหน",
            "ใกล้อะไร",
            "มีสาขาไหม",
            "ที่อยู่ร้าน",
        ],
        "examples": [
            "ร้านอยู่ที่ไหนคะ",
            "ขอพิกัดร้านหน่อยค่ะ",
            "เดินทางไปยังไง",
        ],
    },
    {
        "label": "menu_inquiry",
        "priority": 94,
        "confidence": 0.90,
        "keywords": [
            "มีเมนูอะไร",
            "เมนูมีอะไร",
            "ขายอะไรบ้าง",
            "มีอะไรขายบ้าง",
            "ขอเมนู",
            "ดูเมนู",
            "รายการเมนู",
            "เมนูทั้งหมด",
            "เมนูขนม",
            "เมนูเครื่องดื่ม",
            "มีเค้กอะไร",
            "มีขนมอะไร",
            "มีเครื่องดื่มอะไร",
            "มีเบเกอรี่อะไร",
            "มีเบเกอรี่ไหม",
            "มีเค้กไหม",
            "มีขนมไหม",
            "มีเครื่องดื่มไหม",
            "menu",
        ],
        "examples": [
            "เมนูมีอะไรบ้างคะ",
            "ขอเมนูหน่อยค่ะ",
            "มีเครื่องดื่มอะไรบ้าง",
        ],
    },
    {
        "label": "recommendation",
        "priority": 92,
        "confidence": 0.90,
        "keywords": [
            "เมนูแนะนำ",
            "แนะนำเมนู",
            "แนะนำหน่อย",
            "มีอะไรแนะนำ",
            "อะไรอร่อย",
            "ตัวไหนดี",
            "เมนูขายดี",
            "เมนูยอดนิยม",
            "เมนูเด็ด",
            "เค้กแนะนำ",
            "ขนมแนะนำ",
            "เครื่องดื่มแนะนำ",
            "ไม่รู้จะสั่งอะไร",
            "เลือกไม่ถูก",
            "best seller",
            "recommended",
            "signature",
        ],
        "examples": [
            "ทางร้านมีเมนูแนะนำไหมคะ",
            "เครื่องดื่มแนะนำมีอะไรบ้าง",
            "อะไรขายดีคะ",
        ],
    },
    {
        "label": "price_inquiry",
        "priority": 90,
        "confidence": 0.88,
        "keywords": [
            "ราคา",
            "กี่บาท",
            "เท่าไหร่",
            "เท่าไร",
            "แพงไหม",
            "เริ่มต้น",
            "ราคาประมาณ",
            "ราคาเค้ก",
            "ราคาขนม",
            "ราคาเครื่องดื่ม",
            "price",
            "cost",
        ],
        "examples": [
            "เค้กราคาเท่าไหร่คะ",
            "เครื่องดื่มกี่บาท",
            "ราคาเริ่มต้นเท่าไหร่",
        ],
    },
    {
        "label": "size_option",
        "priority": 88,
        "confidence": 0.88,
        "keywords": [
            "ขนาด",
            "ไซซ์",
            "size",
            "mini",
            "regular",
            "set",
            "แบบเซต",
            "แบบ set",
            "ไซซ์อะไร",
            "มีขนาดอะไร",
            "มีไซซ์อะไร",
            "เล็ก",
            "กลาง",
            "ใหญ่",
            "มินิ",
            "เรกูลาร์",
        ],
        "examples": [
            "Mini มีอะไรบ้างคะ",
            "มีขนาดอะไรบ้าง",
            "มีแบบเซตไหมคะ",
        ],
    },
    {
        "label": "availability",
        "priority": 86,
        "confidence": 0.86,
        "keywords": [
            "วันนี้มีไหม",
            "ยังมีไหม",
            "หมดหรือยัง",
            "หมดไหม",
            "มีของไหม",
            "ของหมดไหม",
            "พร้อมขายไหม",
            "มีหน้าร้านไหม",
            "มีพร้อมส่งไหม",
            "ยังเหลือไหม",
            "จองไว้ได้ไหม",
            "สต็อก",
            "stock",
            "available",
        ],
        "examples": [
            "วันนี้มีเค้กไหมคะ",
            "เมนูนี้หมดหรือยัง",
            "ยังมีหน้าร้านไหม",
        ],
    },
    {
        "label": "reservation",
        "priority": 84,
        "confidence": 0.86,
        "keywords": [
            "จองโต๊ะ",
            "จองที่นั่ง",
            "สำรองที่นั่ง",
            "จองร้าน",
            "จองได้ไหม",
            "walk in",
            "วอล์คอิน",
            "ต้องจองไหม",
            "ไปหน้าร้านได้ไหม",
            "มีโต๊ะว่างไหม",
            "โต๊ะว่าง",
            "reservation",
            "booking",
        ],
        "examples": [
            "ต้องจองโต๊ะก่อนไหมคะ",
            "วันนี้มีโต๊ะว่างไหม",
            "walk in ได้ไหม",
        ],
    },
    {
        "label": "delivery_takeaway",
        "priority": 82,
        "confidence": 0.86,
        "keywords": [
            "เดลิเวอรี่",
            "delivery",
            "ส่งไหม",
            "ส่งได้ไหม",
            "จัดส่ง",
            "ส่งถึงบ้าน",
            "สั่งกลับบ้าน",
            "กลับบ้าน",
            "take away",
            "takeaway",
            "รับเอง",
            "pickup",
            "ไปรับเอง",
            "สั่งล่วงหน้า",
        ],
        "examples": [
            "มีเดลิเวอรี่ไหมคะ",
            "สั่งกลับบ้านได้ไหม",
            "ไปรับเองได้ไหม",
        ],
    },
    {
        "label": "payment",
        "priority": 80,
        "confidence": 0.85,
        "keywords": [
            "จ่ายเงิน",
            "ชำระเงิน",
            "โอน",
            "โอนเงิน",
            "เงินสด",
            "qr",
            "คิวอาร์",
            "พร้อมเพย์",
            "บัตรเครดิต",
            "บัตรเดบิต",
            "สแกนจ่าย",
            "payment",
            "pay",
        ],
        "examples": [
            "จ่ายเงินแบบไหนได้บ้างคะ",
            "โอนได้ไหม",
            "รับบัตรไหมคะ",
        ],
    },
    {
        "label": "order_status",
        "priority": 78,
        "confidence": 0.84,
        "keywords": [
            "ออเดอร์",
            "คำสั่งซื้อ",
            "สถานะออเดอร์",
            "ของถึงไหน",
            "ทำเสร็จหรือยัง",
            "เสร็จยัง",
            "ส่งหรือยัง",
            "ได้ของเมื่อไหร่",
            "รอนานไหม",
            "order status",
            "tracking",
        ],
        "examples": [
            "ออเดอร์ถึงไหนแล้วคะ",
            "ทำเสร็จหรือยัง",
            "ส่งหรือยังคะ",
        ],
    },
    {
        "label": "custom_cake",
        "priority": 76,
        "confidence": 0.86,
        "keywords": [
            "เค้กวันเกิด",
            "วันเกิด",
            "เค้กสั่งทำ",
            "สั่งทำเค้ก",
            "custom cake",
            "เขียนหน้าเค้ก",
            "ป้ายวันเกิด",
            "เทียน",
            "เค้กพิเศษ",
            "เค้กตามแบบ",
            "ทำตามรูป",
            "ออกแบบเค้ก",
            "เค้กงานวันเกิด",
            "เค้กครบรอบ",
            "anniversary",
            "birthday",
        ],
        "examples": [
            "สั่งเค้กวันเกิดได้ไหมคะ",
            "เขียนหน้าเค้กได้ไหม",
            "ทำเค้กตามแบบได้ไหม",
        ],
    },
    {
        "label": "special_occasion",
        "priority": 74,
        "confidence": 0.84,
        "keywords": [
            "จัดงาน",
            "งานวันเกิด",
            "งานครบรอบ",
            "งานเลี้ยง",
            "จัดเซต",
            "จัดเบรก",
            "ของขวัญ",
            "ของฝาก",
            "เซอร์ไพรส์",
            "โอกาสพิเศษ",
            "party",
            "event",
            "gift",
        ],
        "examples": [
            "มีเซตของขวัญไหมคะ",
            "จัดเค้กสำหรับวันเกิดได้ไหม",
            "มีเซตสำหรับงานเลี้ยงไหม",
        ],
    },
    {
        "label": "packaging",
        "priority": 72,
        "confidence": 0.82,
        "keywords": [
            "แพ็กเกจ",
            "แพคเกจ",
            "กล่อง",
            "ถุง",
            "ห่อของขวัญ",
            "ใส่กล่อง",
            "แพ็กกลับบ้าน",
            "แพ็กสวยไหม",
            "packaging",
            "gift box",
        ],
        "examples": [
            "มีกล่องของขวัญไหมคะ",
            "แพ็กกลับบ้านได้ไหม",
            "ห่อของขวัญได้ไหม",
        ],
    },
    {
        "label": "sweetness_adjustment",
        "priority": 70,
        "confidence": 0.84,
        "keywords": [
            "หวานน้อย",
            "ลดหวาน",
            "ไม่หวาน",
            "เพิ่มหวาน",
            "หวานมาก",
            "ระดับความหวาน",
            "เลือกความหวาน",
            "ปรับหวาน",
            "หวาน 0",
            "หวาน 25",
            "หวาน 50",
            "หวาน 75",
            "หวาน 100",
            "less sweet",
            "sugar level",
        ],
        "examples": [
            "หวานน้อยได้ไหมคะ",
            "เลือกความหวานได้ไหม",
            "เครื่องดื่มลดหวานได้ไหม",
        ],
    },
    {
        "label": "allergy",
        "priority": 68,
        "confidence": 0.90,
        "keywords": [
            "แพ้",
            "แพ้อาหาร",
            "แพ้นม",
            "แพ้ไข่",
            "แพ้ถั่ว",
            "แพ้แป้ง",
            "แพ้กลูเตน",
            "กินนมไม่ได้",
            "กินไข่ไม่ได้",
            "กินถั่วไม่ได้",
            "allergy",
            "allergic",
            "gluten",
            "lactose",
            "dairy free",
        ],
        "examples": [
            "แพ้นมกินเมนูไหนได้บ้าง",
            "มีเมนูไม่มีไข่ไหม",
            "แพ้ถั่วทานได้ไหม",
        ],
    },
    {
        "label": "ingredients",
        "priority": 66,
        "confidence": 0.82,
        "keywords": [
            "วัตถุดิบ",
            "ส่วนผสม",
            "ทำจากอะไร",
            "ใส่อะไร",
            "มีนมไหม",
            "มีไข่ไหม",
            "มีถั่วไหม",
            "มีแอลกอฮอล์ไหม",
            "ครีม",
            "เนย",
            "นม",
            "ไข่",
            "ถั่ว",
            "ingredient",
        ],
        "examples": [
            "เค้กมีส่วนผสมอะไรบ้าง",
            "เมนูนี้มีนมไหม",
            "ใช้วัตถุดิบอะไรคะ",
        ],
    },
    {
        "label": "dietary_option",
        "priority": 64,
        "confidence": 0.80,
        "keywords": [
            "มังสวิรัติ",
            "วีแกน",
            "vegan",
            "vegetarian",
            "ฮาลาล",
            "halal",
            "เจ",
            "คีโต",
            "keto",
            "น้ำตาลน้อย",
            "แคลน้อย",
            "แคลอรี่",
            "สุขภาพ",
        ],
        "examples": [
            "มีเมนูวีแกนไหมคะ",
            "มีเมนูแคลน้อยไหม",
            "มีฮาลาลไหม",
        ],
    },
    {
        "label": "ambience_photo_spot",
        "priority": 62,
        "confidence": 0.82,
        "keywords": [
            "บรรยากาศ",
            "ถ่ายรูป",
            "มุมถ่ายรูป",
            "สวนดอกไม้",
            "ดอกไม้",
            "ร้านสวยไหม",
            "คาเฟ่สวยไหม",
            "ที่นั่ง",
            "มุมสวย",
            "ถ่ายคอนเทนต์",
            "photo spot",
            "garden",
            "flower",
        ],
        "examples": [
            "ร้านมีมุมถ่ายรูปไหมคะ",
            "บรรยากาศร้านเป็นยังไง",
            "มีสวนดอกไม้ไหม",
        ],
    },
    {
        "label": "facility",
        "priority": 60,
        "confidence": 0.78,
        "keywords": [
            "ที่จอดรถ",
            "จอดรถ",
            "parking",
            "wifi",
            "ไวไฟ",
            "ปลั๊ก",
            "นั่งทำงาน",
            "สัตว์เลี้ยง",
            "pet friendly",
            "เด็กเข้าได้ไหม",
            "ครอบครัว",
            "ห้องน้ำ",
            "แอร์",
        ],
        "examples": [
            "มีที่จอดรถไหมคะ",
            "มี wifi ไหม",
            "พาสัตว์เลี้ยงเข้าได้ไหม",
        ],
    },
    {
        "label": "service_question",
        "priority": 58,
        "confidence": 0.78,
        "keywords": [
            "สอบถาม",
            "ถามหน่อย",
            "ขอถาม",
            "แอดมิน",
            "ติดต่อ",
            "รายละเอียด",
            "ข้อมูลเพิ่มเติม",
            "ช่วยแนะนำ",
            "ช่วยดูให้หน่อย",
        ],
        "examples": [
            "ขอสอบถามหน่อยค่ะ",
            "แอดมินช่วยดูให้หน่อย",
            "ขอรายละเอียดเพิ่มเติมค่ะ",
        ],
    },
    {
        "label": "compliment",
        "priority": 56,
        "confidence": 0.86,
        "keywords": [
            "อร่อย",
            "อร่อยมาก",
            "น่ารัก",
            "ร้านน่ารัก",
            "สวยมาก",
            "บริการดี",
            "ชอบมาก",
            "ประทับใจ",
            "ดีมาก",
            "น่ากิน",
            "น่าทาน",
            "cute",
            "delicious",
            "good",
            "love",
        ],
        "examples": [
            "ร้านน่ารักมากค่ะ",
            "เค้กอร่อยมาก",
            "บริการดีมากค่ะ",
        ],
    },
    {
        "label": "complaint_product",
        "priority": 54,
        "confidence": 0.90,
        "keywords": [
            "ไม่อร่อย",
            "รสชาติแย่",
            "หวานเกินไป",
            "จืด",
            "เปรี้ยวเกิน",
            "เค้กแข็ง",
            "ขนมเสีย",
            "ของเสีย",
            "กลิ่นแปลก",
            "ไม่สด",
            "ผิดหวัง",
            "ไม่ตรงปก",
            "ได้ของผิด",
            "เมนูผิด",
        ],
        "examples": [
            "เค้กแข็งมากค่ะ",
            "ได้เมนูผิด",
            "รสชาติไม่ตรงปก",
        ],
    },
    {
        "label": "complaint_service",
        "priority": 52,
        "confidence": 0.90,
        "keywords": [
            "บริการไม่ดี",
            "พนักงานพูดจาไม่ดี",
            "พนักงานพูดจาไม่น่ารัก",
            "พนักงานไม่สุภาพ",
            "พูดจาไม่ดี",
            "พูดไม่ดี",
            "รอนาน",
            "ช้ามาก",
            "ตอบช้า",
            "ไม่สนใจลูกค้า",
            "พนักงานแย่",
            "เสียความรู้สึก",
        ],
        "examples": [
            "วันนี้เจอพนักงานพูดจาไม่น่ารักเลยค่ะ",
            "รอนานมาก",
            "บริการไม่ดีเลย",
        ],
    },
    {
        "label": "refund_return",
        "priority": 50,
        "confidence": 0.90,
        "keywords": [
            "คืนเงิน",
            "ขอเงินคืน",
            "refund",
            "เปลี่ยนสินค้า",
            "คืนสินค้า",
            "เคลม",
            "ยกเลิกออเดอร์",
            "ยกเลิกคำสั่งซื้อ",
            "cancel order",
        ],
        "examples": [
            "ขอคืนเงินได้ไหม",
            "อยากยกเลิกออเดอร์",
            "ขอเคลมสินค้าได้ไหม",
        ],
    },
    {
        "label": "high_risk_complaint",
        "priority": 48,
        "confidence": 0.95,
        "keywords": [
            "อาหารเป็นพิษ",
            "ท้องเสีย",
            "เข้าโรงพยาบาล",
            "แพ้รุนแรง",
            "หายใจไม่ออก",
            "อันตราย",
            "ฟ้อง",
            "แจ้งความ",
            "ประจาน",
            "โกง",
            "หลอกลวง",
            "ร้องเรียน",
        ],
        "examples": [
            "กินแล้วท้องเสีย",
            "จะแจ้งความ",
            "แพ้รุนแรงมาก",
        ],
    },
    {
        "label": "greeting",
        "priority": 46,
        "confidence": 0.90,
        "keywords": [
            "สวัสดี",
            "หวัดดี",
            "hello",
            "hi",
            "ทักค่ะ",
            "ทักครับ",
        ],
        "examples": [
            "สวัสดีค่ะ",
            "hello",
            "ทักค่ะ",
        ],
    },
    {
        "label": "thanks",
        "priority": 44,
        "confidence": 0.88,
        "keywords": [
            "ขอบคุณ",
            "ขอบใจ",
            "thank",
            "thanks",
            "โอเคค่ะ",
            "โอเคครับ",
            "รับทราบ",
        ],
        "examples": [
            "ขอบคุณค่ะ",
            "โอเคค่ะ",
            "รับทราบค่ะ",
        ],
    },
]


# ---------------------------------------------------------
# Intent aliases
# Keep original labels, but provide canonical/risk labels
# for other services such as risk_service.py and knowledge_service.py.
# ---------------------------------------------------------

INTENT_ALIASES = {
    "complaint_staff": "complaint_service",
}


def get_canonical_intent(label: str) -> str:
    label = str(label or "").strip()
    return INTENT_ALIASES.get(label, label)


# ---------------------------------------------------------
# Conflict rules
# Used when many intents match at the same time.
# ---------------------------------------------------------

def adjust_conflict(text: str, candidates: List[Tuple[Dict, int]]) -> List[Tuple[Dict, int]]:
    """
    Fix common conflicts:
    - Promotion must beat general question / ingredient / allergy unless allergy words are explicit.
    - Recommendation must beat menu_inquiry if customer asks "แนะนำ".
    - Allergy must only win when explicit allergy words exist.
    """
    explicit_allergy_words = [
        "แพ้",
        "แพ้อาหาร",
        "แพ้นม",
        "แพ้ไข่",
        "แพ้ถั่ว",
        "allergy",
        "allergic",
        "กินนมไม่ได้",
        "กินไข่ไม่ได้",
        "กินถั่วไม่ได้",
    ]

    promotion_words = [
        "โปรโมชั่น",
        "โปร",
        "ส่วนลด",
        "ลดราคา",
        "ซื้อคู่",
        "149",
        "แถม",
    ]

    recommendation_words = [
        "แนะนำ",
        "ขายดี",
        "ยอดนิยม",
        "เมนูเด็ด",
        "signature",
        "recommended",
    ]

    adjusted = []

    for rule, score in candidates:
        label = rule["label"]

        # Prevent false allergy match.
        if label == "allergy" and not contains_any(text, explicit_allergy_words):
            score -= 5

        # Promotion should win promotion questions.
        if label == "promotion" and contains_any(text, promotion_words):
            score += 5

        # Recommendation should win "recommend" questions.
        if label == "recommendation" and contains_any(text, recommendation_words):
            score += 4

        # Menu inquiry should not beat recommendation when "แนะนำ" exists.
        if label == "menu_inquiry" and contains_any(text, recommendation_words):
            score -= 2

        adjusted.append((rule, score))

    return adjusted


def classify_intent(text: str) -> Dict:
    """
    Main intent classifier.
    Return format:
    {
        "label": "promotion",
        "intent": "promotion",
        "canonical_intent": "promotion",
        "risk_intent": "promotion",
        "confidence": 0.95,
        "method": "rule_based",
        "matched_keywords": ["โปรโมชั่น"],
        "description": "...",
    }
    """
    original_text = str(text or "")
    text = normalize_text(original_text)

    if not text:
        return {
            "label": "empty_message",
            "intent": "empty_message",
            "canonical_intent": "empty_message",
            "risk_intent": "empty_message",
            "confidence": 0.50,
            "method": "rule_based",
            "matched_keywords": [],
            "description": "Empty or invalid message"
        }

    candidates: List[Tuple[Dict, int]] = []

    for rule in INTENT_RULES:
        matched_keywords = [
            keyword for keyword in rule["keywords"]
            if keyword in text
        ]

        if matched_keywords:
            # Score = priority + number of matched words
            score = rule["priority"] + len(matched_keywords)
            candidates.append((rule, score))

    if not candidates:
        return {
            "label": "general_question",
            "intent": "general_question",
            "canonical_intent": "general_question",
            "risk_intent": "general_question",
            "confidence": 0.60,
            "method": "fallback",
            "matched_keywords": [],
            "description": "General customer question"
        }

    candidates = adjust_conflict(text, candidates)
    candidates.sort(key=lambda item: item[1], reverse=True)

    best_rule, best_score = candidates[0]

    label = best_rule["label"]
    canonical_intent = get_canonical_intent(label)

    matched_keywords = [
        keyword for keyword in best_rule["keywords"]
        if keyword in text
    ]

    confidence = best_rule["confidence"]

    # Slightly increase confidence if many keywords match.
    if len(matched_keywords) >= 2:
        confidence = min(confidence + 0.03, 0.98)

    return {
        "label": label,
        "intent": label,
        "canonical_intent": canonical_intent,
        "risk_intent": canonical_intent,
        "confidence": confidence,
        "method": "rule_based",
        "matched_keywords": matched_keywords,
        "description": f"Matched intent: {label}",
        "candidates": [
            {
                "label": rule["label"],
                "intent": rule["label"],
                "canonical_intent": get_canonical_intent(rule["label"]),
                "risk_intent": get_canonical_intent(rule["label"]),
                "score": score,
                "matched_keywords": [
                    keyword for keyword in rule["keywords"]
                    if keyword in text
                ]
            }
            for rule, score in candidates[:5]
        ]
    }


# ---------------------------------------------------------
# Compatibility wrappers
# Use these names to avoid breaking existing pipeline code.
# ---------------------------------------------------------

def detect_intent(text: str) -> Dict:
    return classify_intent(text)


def detect_intent_rule(text: str) -> Dict:
    return classify_intent(text)


def analyze_intent(text: str) -> Dict:
    return classify_intent(text)


def predict_intent(text: str) -> Dict:
    return classify_intent(text)


def get_intent(text: str) -> Dict:
    return classify_intent(text)


# ---------------------------------------------------------
# Optional quick test
# Run: python backend/app/services/intent_service.py
# ---------------------------------------------------------

if __name__ == "__main__":
    test_messages = [
        "สวัสดีค่ะ",
        "ทางร้านมีเมนูแนะนำมั้ยคะ",
        "ช่วงนี้มีโปรโมชั่นมั้ยคะ",
        "มีเครื่องดื่มแนะนำมั้ยคะ",
        "ร้านเปิดกี่โมงคะ",
        "ร้านอยู่ที่ไหนคะ",
        "Mini มีอะไรบ้างคะ",
        "หวานน้อยได้ไหมคะ",
        "แพ้นมกินเมนูไหนได้บ้าง",
        "มีส่วนผสมอะไรบ้างคะ",
        "มีเดลิเวอรี่ไหม",
        "จ่ายเงินแบบไหนได้บ้าง",
        "วันนี้เจอพนักงานพูดจาไม่น่ารักเลยค่ะ",
        "กินแล้วท้องเสีย ขอคืนเงิน",
        "ร้านมีมุมถ่ายรูปไหมคะ",
    ]

    for msg in test_messages:
        result = classify_intent(msg)
        print("=" * 60)
        print("Text:", msg)
        print("Intent:", result["label"])
        print("Canonical:", result["canonical_intent"])
        print("Risk Intent:", result["risk_intent"])
        print("Confidence:", result["confidence"])
        print("Matched:", result["matched_keywords"])