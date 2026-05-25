import base64, hashlib, hmac, os
from fastapi import APIRouter, Request, HTTPException
from app.services.pipeline_service import process_line_message
from app.services.logging_service import log_event
from app.services.security_service import limiter


router=APIRouter()


def validate_line_signature(body: bytes, signature: str | None) -> bool:
    secret = os.getenv('LINE_CHANNEL_SECRET', '').strip()
    signature = (signature or '').strip()

    if not secret or not signature:
        return False

    digest = hmac.new(
        secret.encode('utf-8'),
        body,
        hashlib.sha256
    ).digest()

    expected = base64.b64encode(digest).decode('utf-8')
    return hmac.compare_digest(expected, signature)


@router.post('/webhook')
@limiter.limit('120/minute')
async def line_webhook(request: Request):
    body = await request.body()
    sig = request.headers.get('x-line-signature') or request.headers.get('X-Line-Signature')

    if not validate_line_signature(body, sig):
        await log_event(
            'line_signature',
            'failed',
            'Invalid LINE signature',
            fallback_used=True,
            severity='critical'
        )
        raise HTTPException(status_code=403, detail='Invalid LINE signature')

    payload = await request.json()
    results = []

    for e in payload.get('events', []):
        try:
            if e.get('type') == 'message' and e.get('message', {}).get('type') == 'text':
                results.append(await process_line_message(e))

            elif e.get("type") == "follow":
                from app.services.line_service import reply_message

                reply_token = e.get("replyToken")
                if reply_token:
                    sent = reply_message(
                        reply_token,
                        "สวัสดีค่ะ 🌷 ยินดีต้อนรับสู่ Pudding Petals นะคะ วันนี้ให้แอดมินช่วยดูเรื่องไหนดีคะ"
                    )
                    results.append({
                        "type": "follow",
                        "status": "welcome_sent",
                        "send_result": sent
                    })

        except Exception as exc:
            await log_event(
                "line_event_processing",
                "failed",
                str(exc),
                fallback_used=True,
                severity="error",
                extra={"event_type": e.get("type")}
            )
            results.append({
                "type": e.get("type"),
                "status": "failed",
                "error": str(exc)
            })

    return {
        'ok': True,
        'processed': len(results),
        'results': results
    }


@router.post('/mock')
@limiter.limit('30/minute')
async def line_mock(request:Request):
    p=await request.json()
    e={'replyToken':p.get('replyToken','mock-reply-token'),'source':{'type':'user','userId':p.get('line_user_id','mock-user')},'message':{'type':'text','text':p.get('text','')}}
    return {'ok':True,'result':await process_line_message(e,mock=True)}
