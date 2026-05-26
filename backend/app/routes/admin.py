import os
from fastapi import APIRouter, HTTPException, Request

from app.services.firebase_service import db_get, db_update
from app.services.line_service import push_message
from app.services.feedback_service import save_feedback
from app.services.logging_service import log_event
from app.services.security_service import limiter


router = APIRouter()


@router.post("/send-line-reply")
@limiter.limit("60/minute")
async def send_line_reply(
    request: Request,
    payload: dict
):
    cid = (
        payload.get("comment_id")
        or payload.get("id")
        or payload.get("commentId")
    )

    msg = (
        payload.get("message")
        or payload.get("reply")
        or payload.get("final_reply")
        or payload.get("finalReply")
    )

    if not cid:
        raise HTTPException(
            status_code=400,
            detail="comment_id is required"
        )

    if not msg:
        raise HTTPException(
            status_code=400,
            detail="message is required"
        )

    comment = db_get(f"comments/{cid}")

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    uid = (
        comment.get("line_user_id")
        or comment.get("lineUserId")
        or comment.get("user_id")
        or comment.get("userId")
    )

    if not uid:
        raise HTTPException(
            status_code=400,
            detail="LINE user id not found in comment"
        )

    sent = push_message(uid, msg)

    if not sent.get("success"):
        await log_event(
            step="admin_send_line_reply",
            status="failed",
            message="LINE push message failed",
            comment_id=cid,
            fallback_used=True,
            severity="error",
            extra=sent
        )

        raise HTTPException(
            status_code=502,
            detail=sent
        )

    db_update(
        f"comments/{cid}",
        {
            "status": "sent",
            "final_reply": msg,
            "send_result": sent
        }
    )

    await save_feedback(
        cid,
        {
            "admin_action": "sent",
            "edited_reply": msg
        }
    )

    await log_event(
        step="admin_send_line_reply",
        status="success",
        message="Admin approved and sent LINE reply",
        comment_id=cid,
        fallback_used=False,
        severity="normal",
        extra=sent
    )

    return {
        "ok": True,
        "status": "sent",
        "comment_id": cid,
        "line_user_id": uid,
        "send_result": sent
    }