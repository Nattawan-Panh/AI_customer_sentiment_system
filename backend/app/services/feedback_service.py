from datetime import datetime, timezone
from app.services.firebase_service import db_push


def utc_now():
    return datetime.now(timezone.utc).isoformat()


async def save_feedback(comment_id, payload):
    try:
        if not isinstance(payload, dict):
            payload = {}

        feedback_data = {
            "comment_id": str(comment_id or "").strip(),
            "feedback_type": payload.get(
                "feedback_type",
                "general_feedback"
            ),
            "created_at": utc_now(),

            # merge payload
            **payload
        }

        ref = db_push("feedback", feedback_data)

        return {
            "status": "success",
            "feedback_id": ref.key
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }