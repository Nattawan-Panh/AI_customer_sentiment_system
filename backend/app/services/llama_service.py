import os
import requests


GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "llama-3.1-8b-instant"
MAX_INPUT_CHARS = 3000
MAX_REPLY_CHARS = 900


def _safe_text(value, default=""):
    return str(value or default).strip()


def _truncate(text: str, limit: int) -> str:
    text = _safe_text(text)

    if len(text) <= limit:
        return text

    return text[:limit] + "...[ตัดข้อความบางส่วน]"


def refine_reply_with_llama(comment, template, knowledge, brand):
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    model = os.getenv("GROQ_MODEL", DEFAULT_MODEL).strip()

    template = _safe_text(template)
    comment = _truncate(comment, MAX_INPUT_CHARS)
    knowledge = _truncate(knowledge, MAX_INPUT_CHARS)

    brand = brand or {}

    brand_name = _safe_text(
        brand.get("brand_name"),
        "Pudding Petals"
    )
    persona = _safe_text(
        brand.get("persona"),
        "อบอุ่น อ่อนโยน เป็นกันเอง ใส่ใจ และพูดเหมือนเพื่อนผู้หญิงที่ช่วยดูแลลูกค้า"
    )
    tone = _safe_text(
        brand.get("tone"),
        "สุภาพ ละมุน กระชับ และให้ความรู้สึกเหมือนคาเฟ่ขนมหวานในสวนดอกไม้"
    )

    if not template:
        return {
            "reply": "",
            "used_llama": False,
            "status": "failed",
            "reason": "empty_template"
        }

    if not api_key:
        return {
            "reply": template,
            "used_llama": False,
            "status": "fallback",
            "reason": "missing_groq_api_key"
        }

    prompt = f"""
คุณคือแอดมินของแบรนด์ {brand_name}

บุคลิกแบรนด์:
{persona}

โทนภาษา:
{tone}

ข้อความลูกค้า:
{comment}

ข้อมูลอ้างอิงจาก Knowledge Base:
{knowledge}

คำตอบตั้งต้น:
{template}

งานของคุณ:
ปรับคำตอบตั้งต้นให้เป็นคำตอบสำหรับส่งให้ลูกค้าใน LINE OA

กฎสำคัญ:
1. ตอบเป็นภาษาไทยเท่านั้น
2. ใช้น้ำเสียงสุภาพ อ่อนโยน ละมุน และเป็นกันเอง
3. ห้ามแต่งข้อมูลใหม่ที่ไม่มีใน Knowledge Base
4. ห้ามรับปากเกินจริง เช่น ยืนยันคืนเงินทันที ยืนยันโต๊ะว่าง หรือยืนยันสินค้าแทนแอดมิน
5. ถ้าเป็นเรื่องคืนเงิน เคลม ร้องเรียน ออเดอร์มีปัญหา หรือจองงาน ให้ใช้ถ้อยคำรับเรื่องและขอรายละเอียดเพิ่ม
6. คำตอบต้องกระชับ เหมาะกับการส่งใน LINE
7. ห้ามใส่หัวข้อ คำอธิบาย หรือ reasoning เพิ่ม
8. ส่งออกเฉพาะข้อความตอบลูกค้าเท่านั้น
"""

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a careful Thai customer support assistant. "
                    "You must not overpromise beyond the provided knowledge base."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.25,
        "max_tokens": 350
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            GROQ_CHAT_URL,
            headers=headers,
            json=payload,
            timeout=25
        )

        response.raise_for_status()

        data = response.json()
        refined_reply = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            .strip()
        )

        if not refined_reply:
            return {
                "reply": template,
                "used_llama": False,
                "status": "fallback",
                "reason": "empty_llama_response"
            }

        refined_reply = _truncate(refined_reply, MAX_REPLY_CHARS)

        return {
            "reply": refined_reply,
            "used_llama": True,
            "status": "success",
            "model": model
        }

    except requests.exceptions.Timeout:
        return {
            "reply": template,
            "used_llama": False,
            "status": "fallback",
            "reason": "groq_timeout"
        }

    except requests.exceptions.HTTPError as e:
        return {
            "reply": template,
            "used_llama": False,
            "status": "fallback",
            "reason": "groq_http_error",
            "error": getattr(e.response, "text", str(e))
        }

    except Exception as e:
        return {
            "reply": template,
            "used_llama": False,
            "status": "fallback",
            "reason": "unknown_error",
            "error": str(e)
        }