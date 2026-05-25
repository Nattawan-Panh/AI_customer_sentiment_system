import os
from fastapi import APIRouter, HTTPException, Request, Header
from app.services.firebase_service import db_get, db_update
from app.services.line_service import push_message
from app.services.feedback_service import save_feedback
from app.services.logging_service import log_event
from app.services.security_service import limiter

router = APIRouter()

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")


@router.post('/send-line-reply')
@limiter.limit('60/minute')
async def send_line_reply(
    request: Request,
    payload: dict,
    x_admin_key: str = Header(default="", alias="X-Admin-Key")
):
    if not ADMIN_API_KEY or x_admin_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    cid = payload.get('comment_id')
    msg = payload.get('message')

    if not cid or not msg:
        raise HTTPException(
            status_code=400,
            detail='comment_id and message are required'
        )

    c = db_get(f'comments/{cid}')

    if not c:
        raise HTTPException(status_code=404, detail='comment not found')

    uid = c.get('line_user_id')

    if not uid:
        raise HTTPException(status_code=400, detail='line_user_id missing')

    try:
        sent = push_message(uid, msg)

        if not sent.get("success"):
            raise HTTPException(status_code=502, detail=sent)

        db_update(f'comments/{cid}', {
            'status': 'sent',
            'final_reply': msg,
            'send_result': sent
        })

        await save_feedback(
            cid,
            {
                'admin_action': 'sent',
                'edited_reply': msg
            }
        )

        await log_event(
            'send_line_reply',
            'success',
            f'Sent LINE reply for {cid}',
            comment_id=cid
        )

        return {
            'ok': True,
            'sent': sent
        }

    except HTTPException:
        raise

    except Exception as exc:
        await log_event(
            'send_line_reply',
            'error',
            str(exc),
            comment_id=cid,
            fallback_used=True,
            severity='high'
        )

        raise HTTPException(status_code=500, detail=str(exc))