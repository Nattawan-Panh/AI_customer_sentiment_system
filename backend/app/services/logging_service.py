from datetime import datetime, timezone

from app.services.firebase_service import db_push


VALID_STATUSES = {
    "success",
    "failed",
    "fallback",
    "skipped",
    "pending"
}

VALID_SEVERITIES = {
    "debug",
    "normal",
    "warning",
    "error",
    "critical"
}


def utc_now():
    return datetime.now(timezone.utc).isoformat()


async def log_event(
    step,
    status,
    message,
    comment_id=None,
    fallback_used=False,
    severity="normal",
    extra=None
):
    step = str(step or "unknown_step").strip()
    status = str(status or "pending").strip().lower()
    message = str(message or "").strip()
    severity = str(severity or "normal").strip().lower()

    if status not in VALID_STATUSES:
        status = "pending"

    if severity not in VALID_SEVERITIES:
        severity = "normal"

    log_data = {
        "step": step,
        "status": status,
        "message": message,
        "comment_id": comment_id,
        "fallback_used": bool(fallback_used),
        "severity": severity,
        "timestamp": utc_now()
    }

    if isinstance(extra, dict):
        log_data["extra"] = extra

    try:
        ref = db_push("logs", log_data)

        return {
            "status": "success",
            "log_id": ref.key,
            "data": log_data
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "data": log_data
        }