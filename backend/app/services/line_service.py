import os
import requests


LINE_PUSH_URL = os.getenv(
    "LINE_PUSH_URL",
    "https://api.line.me/v2/bot/message/push"
)

LINE_REPLY_URL = os.getenv(
    "LINE_REPLY_URL",
    "https://api.line.me/v2/bot/message/reply"
)

LINE_TEXT_LIMIT = 5000


def _headers():
    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "").strip()

    if not token:
        raise RuntimeError("LINE_CHANNEL_ACCESS_TOKEN is missing")

    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }


def _normalize_text(text: str) -> str:
    text = str(text or "").strip()

    if not text:
        text = "ขออภัยค่ะ ระบบไม่พบข้อความสำหรับตอบกลับ"

    if len(text) > LINE_TEXT_LIMIT:
        text = text[:LINE_TEXT_LIMIT - 20] + "...ข้อความถูกตัด"

    return text


def _send_line_request(url: str, payload: dict) -> dict:
    try:
        response = requests.post(
            url,
            headers=_headers(),
            json=payload,
            timeout=15
        )

        response.raise_for_status()

        return {
            "success": True,
            "status": "sent",
            "status_code": response.status_code,
            "response": response.text
        }

    except requests.exceptions.HTTPError as e:
        return {
            "success": False,
            "status": "failed",
            "error_type": "http_error",
            "status_code": getattr(e.response, "status_code", None),
            "response": getattr(e.response, "text", str(e))
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "status": "failed",
            "error_type": "timeout",
            "error": "LINE API request timeout"
        }

    except Exception as e:
        return {
            "success": False,
            "status": "failed",
            "error_type": "unknown_error",
            "error": str(e)
        }


def push_message(line_user_id: str, text: str) -> dict:
    line_user_id = str(line_user_id or "").strip()
    text = _normalize_text(text)

    if not line_user_id:
        return {
            "success": False,
            "status": "failed",
            "error": "line_user_id is required"
        }

    payload = {
        "to": line_user_id,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }

    return _send_line_request(LINE_PUSH_URL, payload)


def reply_message(reply_token: str, text: str) -> dict:
    reply_token = str(reply_token or "").strip()
    text = _normalize_text(text)

    if not reply_token:
        return {
            "success": False,
            "status": "failed",
            "error": "reply_token is required"
        }

    payload = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }

    return _send_line_request(LINE_REPLY_URL, payload)
