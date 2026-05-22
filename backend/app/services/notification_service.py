from app.services.email_service import send_admin_email
from app.services.logging_service import log_event


def _safe_get(data, key, default="-"):
    if not isinstance(data, dict):
        return default

    value = data.get(key)

    if value is None or value == "":
        return default

    return value


def _build_review_email_body(comment: dict, comment_id, reason: str) -> str:
    comment = comment or {}

    return f"""
มีข้อความจาก LINE OA ที่ต้องรอแอดมินตรวจสอบ

==============================
ข้อมูลการตรวจสอบ
==============================
Reason: {reason}
Comment ID: {comment_id}
Platform: {_safe_get(comment, "platform", "LINE OA")}
LINE User ID: {_safe_get(comment, "line_user_id")}
Customer Name: {_safe_get(comment, "customer_name")}

==============================
ข้อความลูกค้า
==============================
{_safe_get(comment, "original_text")}

==============================
ผลการวิเคราะห์ของระบบ
==============================
Sentiment: {_safe_get(comment, "sentiment")}
Sentiment Confidence: {_safe_get(comment, "sentiment_confidence")}
Intent: {_safe_get(comment, "intent")}
Intent Confidence: {_safe_get(comment, "intent_confidence")}
Risk Level: {_safe_get(comment, "risk_level")}
Risk Score: {_safe_get(comment, "risk_score")}

==============================
AI Draft Reply
==============================
{_safe_get(comment, "ai_reply")}

==============================
สิ่งที่แอดมินต้องทำ
==============================
กรุณาเข้า Dashboard เพื่อ Approve / Edit / Reject คำตอบก่อนส่งให้ลูกค้า
""".strip()


async def notify_admin_for_review(comment, comment_id, reason):
    reason = str(reason or "review_required").strip()
    subject = f"[AI Review Required] {reason} - LINE OA Message"
    body = _build_review_email_body(comment, comment_id, reason)

    try:
        result = send_admin_email(
            subject=subject,
            body=body,
            comment_id=comment_id,
            notification_type="review_required"
        )

        await log_event(
            step="email_notification",
            status="success",
            message=f"Admin review email sent: {reason}",
            comment_id=comment_id,
            fallback_used=False,
            severity="normal",
            extra={
                "reason": reason,
                "notification_status": result.get("status")
            }
        )

        return {
            "status": "success",
            "channel": "email",
            "reason": reason,
            "result": result
        }

    except Exception as exc:
        await log_event(
            step="email_notification",
            status="failed",
            message=f"Admin review email failed: {str(exc)}",
            comment_id=comment_id,
            fallback_used=True,
            severity="error",
            extra={
                "reason": reason
            }
        )

        return {
            "status": "failed",
            "channel": "email",
            "reason": reason,
            "error": str(exc)
        }