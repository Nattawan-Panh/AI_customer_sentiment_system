INTENT_KEYWORDS = {
    "greeting": [
        "สวัสดี", "ดีค่ะ", "ดีคับ", "hello", "hi", "ทักค่ะ"
    ],

    "menu_inquiry": [
        "มีเมนูอะไร", "เมนู", "ขายอะไร", "ขนมอะไร", "เค้กอะไร",
        "เครื่องดื่ม", "เบเกอรี่", "ของหวาน"
    ],

    "price_inquiry": [
        "ราคา", "กี่บาท", "เท่าไหร่", "แพงไหม", "งบ", "ไม่เกิน",
        "เริ่มต้น", "ราคาเริ่ม"
    ],

    "recommendation": [
        "แนะนำ", "เมนูไหนดี", "กินอะไรดี", "อันไหนดี",
        "ขายดี", "signature", "ซิกเนเจอร์", "ยอดนิยม"
    ],

    "size_option": [
        "ขนาด", "ไซส์", "ชิ้นเล็ก", "ชิ้นใหญ่", "mini", "regular",
        "whole cake", "ปอนด์", "กี่คนทาน"
    ],

    "sweetness_allergy": [
        "หวานน้อย", "หวานมากไหม", "แพ้", "นม", "ถั่ว", "ไข่",
        "กลูเตน", "คาเฟอีน", "เจ"
    ],

    "custom_cake": [
        "เค้กวันเกิด", "สั่งทำ", "custom", "เขียนหน้าเค้ก",
        "ปักเทียน", "จัดเซ็ต", "ของขวัญ"
    ],

    "opening_hours": [
        "เปิดกี่โมง", "ปิดกี่โมง", "เปิดไหม", "วันหยุด",
        "เวลาเปิด", "เวลาปิด"
    ],

    "location": [
        "ร้านอยู่ไหน", "พิกัด", "โลเคชั่น", "ไปยังไง", "แผนที่",
        "สาขา", "อยู่แถวไหน"
    ],

    "reservation": [
        "จองโต๊ะ", "จองได้ไหม", "walk in", "วอล์คอิน",
        "คนเยอะไหม", "โต๊ะว่างไหม"
    ],

    "cafe_facilities": [
        "wifi", "ไวไฟ", "ปลั๊ก", "นั่งทำงาน", "ทำงานได้ไหม",
        "แอร์", "ห้องน้ำ", "ที่จอดรถ", "pet friendly", "พาสัตว์เลี้ยง"
    ],

    "photo_spot": [
        "ถ่ายรูป", "มุมถ่ายรูป", "สวนดอกไม้", "วิว", "สวยไหม",
        "แต่งร้าน", "outdoor", "indoor"
    ],

    "delivery_platform": [
        "เดลิเวอรี่", "delivery", "grab", "grabfood",
        "lineman", "ไลน์แมน", "สั่งออนไลน์", "สั่งผ่านแอป"
    ],

    "delivery_issue": [
        "ไรเดอร์", "ของยังไม่มา", "ส่งช้า", "ตามออเดอร์",
        "สถานะ", "ขนส่ง", "แอปมีปัญหา"
    ],

    "order_problem": [
        "ได้ของผิด", "ของไม่ครบ", "ขนมหก", "เค้กเละ",
        "เครื่องดื่มหก", "เสียหาย", "ไม่ตรงปก"
    ],

    "refund_exchange": [
        "คืนเงิน", "เปลี่ยนสินค้า", "เคลม", "refund",
        "ยกเลิกออเดอร์", "คืนได้ไหม"
    ],

    "complaint": [
        "แย่", "ไม่พอใจ", "ผิดหวัง", "ช้ามาก", "เสียความรู้สึก",
        "บริการไม่ดี", "ร้องเรียน"
    ],

    "compliment": [
        "อร่อย", "น่ารัก", "ชอบมาก", "ประทับใจ", "ร้านสวย",
        "ดีมาก", "ขอบคุณ"
    ],

    "collaboration": [
        "รีวิว", "collab", "influencer", "ถ่ายงาน", "ติดต่อโปรโมท",
        "สปอนเซอร์", "ร่วมงาน"
    ],

    "event_booking": [
        "จัดงาน", "วันเกิด", "ปาร์ตี้", "private event",
        "เหมาร้าน", "จัดเลี้ยง"
    ],

    "human_required": [
        "ผู้จัดการ", "คุยกับแอดมิน", "ติดต่อเจ้าของร้าน",
        "เรื่องด่วน", "ฟ้อง", "แจ้งความ", "เสียหายมาก"
    ]
}


INTENT_PRIORITY = {
    "human_required": 100,
    "refund_exchange": 95,
    "order_problem": 90,
    "complaint": 85,
    "delivery_issue": 80,
    "event_booking": 75,
    "collaboration": 70,
    "sweetness_allergy": 65,
    "custom_cake": 60,
    "reservation": 55,
    "delivery_platform": 50,
    "price_inquiry": 45,
    "menu_inquiry": 40,
    "recommendation": 38,
    "size_option": 35,
    "opening_hours": 30,
    "location": 30,
    "cafe_facilities": 25,
    "photo_spot": 20,
    "compliment": 15,
    "greeting": 10,
}


def predict_intent(text: str):
    text = str(text or "").lower().strip()

    if not text:
        return {
            "label": "general_question",
            "confidence": 0.50,
            "method": "rule-based",
            "matched_keywords": []
        }

    matched_results = []

    for intent, keywords in INTENT_KEYWORDS.items():
        matched_keywords = [
            keyword for keyword in keywords
            if keyword.lower() in text
        ]

        if matched_keywords:
            matched_results.append({
                "label": intent,
                "matched_keywords": matched_keywords,
                "match_count": len(matched_keywords),
                "priority": INTENT_PRIORITY.get(intent, 0)
            })

    if not matched_results:
        return {
            "label": "general_question",
            "confidence": 0.60,
            "method": "rule-based",
            "matched_keywords": []
        }

    best_match = sorted(
        matched_results,
        key=lambda item: (
            item["priority"],
            item["match_count"]
        ),
        reverse=True
    )[0]

    confidence = min(
        0.95,
        0.70 + (best_match["match_count"] * 0.05)
    )

    return {
        "label": best_match["label"],
        "confidence": confidence,
        "method": "rule-based",
        "matched_keywords": best_match["matched_keywords"],
        "all_matches": matched_results
    }


def detect_intent(text: str) -> str:
    return predict_intent(text)["label"]