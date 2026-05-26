from datetime import datetime, timezone

from app.services.cleaning_service import clean_text
from app.services.spam_service import is_spam, duplicate_key
from app.services.safety_service import pre_safety_check, post_safety_check
from app.services.sentiment_service import predict_sentiment
from app.services.intent_service import predict_intent
from app.services.risk_service import score_risk
from app.services.knowledge_service import retrieve_knowledge
from app.services.template_service import select_template
from app.services.brand_service import get_brand_settings
from app.services.llama_service import refine_reply_with_llama
from app.services.decision_service import should_auto_send
from app.services.line_service import push_message, reply_message, get_line_display_name
from app.services.notification_service import notify_admin_for_review
from app.services.feedback_service import save_feedback
from app.services.firebase_service import db_push, db_update
from app.services.logging_service import log_event


def utc_now():
    return datetime.now(timezone.utc).isoformat()


async def process_line_message(event, mock=False):
    comment_id = None

    try:
        text = event.get("message", {}).get("text", "")
        reply_token = event.get("replyToken")
        line_user_id = event.get("source", {}).get("userId", "unknown-line-user")
        line_display_name = line_user_id

        if not text:
            await log_event(
                "validate_input",
                "failed",
                "Empty LINE message",
                fallback_used=True,
                severity="error"
            )
            raise ValueError("Empty LINE message")

        clean = clean_text(text)

        await log_event(
            "text_cleaning",
            "success",
            "Text cleaned"
        )

        spam_result = is_spam(clean)
        status = "spam" if spam_result.get("is_spam") else "processing"

        await log_event(
            "duplicate_spam_check",
            "success",
            str({
                "spam_score": spam_result.get("score"),
                "spam_matched": spam_result.get("matched")
            }),
            f"Status: {status}"
        )

        pre = pre_safety_check(clean)

        await log_event(
            "pre_safety_check",
            "success" if pre.get("safe") else "failed",
            str(pre),
            severity="normal" if pre.get("safe") else "warning"
        )

        sentiment = predict_sentiment(clean)

        await log_event(
            "sentiment_prediction",
            "success",
            str(sentiment),
            fallback_used=bool(sentiment.get("fallback_used")),
            severity="warning" if sentiment.get("fallback_used") else "normal"
        )

        intent = predict_intent(clean)

        await log_event(
            "intent_prediction",
            "success",
            str(intent)
        )

        risk = score_risk(
            clean,
            sentiment.get("label"),
            intent.get("label"),
            pre.get("safe")
        )

        await log_event(
            "risk_scoring",
            "success",
            str(risk)
        )

        knowledge = retrieve_knowledge(
            intent.get("label"),
            clean
        )

        await log_event(
            "knowledge_retrieval",
            "success",
            str({
                "title": knowledge.get("title"),
                "matched": knowledge.get("matched")
            })
        )

        template_result = select_template(
            intent.get("label"),
            knowledge_base=knowledge,
            customer_text=clean,
            sentiment_label=sentiment.get("label"),
            risk_level=risk.get("level")
        )

        template = template_result.get("reply") or knowledge.get("answer") or knowledge.get("content")
        brand = get_brand_settings()

        llm_reason = None
        llm_error = None

        if not pre.get("safe"):
            template = (
                "ขอบคุณที่บอกให้ Pudding Petals ทราบนะคะ "
                "ข้อความนี้อาจต้องให้แอดมินช่วยตรวจสอบเพิ่มเติมก่อน "
                "เพื่อให้ดูแลคุณลูกค้าได้อย่างถูกต้องและสบายใจที่สุดค่ะ 🌷"
            )
            ai_reply = template
            llm_used = False
            llm_status = "skipped_pre_safety_failed"
            llm_reason = "pre_safety_failed"
        else:
            llm_result = refine_reply_with_llama(
                clean,
                template,
                knowledge.get("content", ""),
                brand
            )

            if isinstance(llm_result, dict):
                ai_reply = llm_result.get("reply") or template
                llm_used = llm_result.get("used_llama", False)
                llm_status = llm_result.get("status", "unknown")
                llm_reason = llm_result.get("reason")
                llm_error = llm_result.get("error")
            else:
                ai_reply = llm_result or template
                llm_used = False
                llm_status = "legacy_return"

        await log_event(
            "llm_reply_refinement",
            "success",
            str({
                "message": "LLM used successfully" if llm_used else "LLM fallback used",
                "llm_used": llm_used,
                "llm_status": llm_status,
                "llm_reason": llm_reason,
                "llm_error": llm_error
            }),
            fallback_used=not llm_used,
            severity="normal" if llm_used else "warning"
        )

        post = post_safety_check(ai_reply)

        if not post.get("safe"):
            ai_reply = (
                "ขอบคุณที่บอกให้ Pudding Petals ทราบนะคะ "
                "ข้อความนี้อาจต้องให้แอดมินช่วยตรวจสอบเพิ่มเติมก่อน "
                "เพื่อให้ดูแลคุณลูกค้าได้อย่างถูกต้องและสบายใจที่สุดค่ะ 🌷"
            )

            await log_event(
                "post_safety_check",
                "failed",
                str(post),
                fallback_used=True,
                severity="warning"
            )
        else:
            await log_event(
                "post_safety_check",
                "success",
                str(post)
            )

        decision = should_auto_send(
            risk.get("level"),
            sentiment.get("confidence"),
            intent.get("confidence"),
            post.get("safe"),
            status,
            intent_label=intent.get("label")
        )

        final_status = "auto_sent" if decision.get("auto_send") else "pending_review"

        if not pre.get("safe"):
            final_status = "pending_review"

        if status == "spam":
            final_status = "spam"

        data = {
            "platform": "LINE OA",
            "line_user_id": line_user_id,
            "customer_name": line_display_name,
            "line_display_name": line_display_name,
            "reply_token": reply_token,
            "original_text": text,
            "clean_text": clean,
            "duplicate_key": duplicate_key(clean),

            "pre_safe": pre.get("safe"),

            "sentiment": sentiment.get("label"),
            "sentiment_confidence": sentiment.get("confidence"),
            "sentiment_model": sentiment.get("model"),
            "sentiment_fallback_used": sentiment.get("fallback_used"),
            "sentiment_fallback_reason": sentiment.get("fallback_reason"),

            "intent": intent.get("label"),
            "intent_confidence": intent.get("confidence"),
            "intent_method": intent.get("method"),

            "risk_level": risk.get("level"),
            "risk_score": risk.get("score"),

            "knowledge_title": knowledge.get("title"),
            "knowledge_matched": knowledge.get("matched"),

            "template_reply": template,
            "ai_reply": ai_reply,
            "post_safe": post.get("safe"),

            "reply_source": "llama" if llm_used else "template_fallback",
            "llm_used": llm_used,
            "llm_status": llm_status,
            "llm_reason": llm_reason,
            "llm_error": llm_error,

            "decision_reason": decision.get("reason"),
            "status": final_status,
            "created_at": utc_now()
        }

        ref = db_push("comments", data)
        comment_id = ref.key

        await log_event(
            "save_to_firebase",
            "success",
            f"Saved comment {comment_id}",
            comment_id=comment_id
        )

        if decision.get("auto_send") and final_status == "auto_sent":
            try:
                if mock:
                    sent = {
                        "mock": True,
                        "message": ai_reply
                    }
                else:
                    sent = (
                        reply_message(reply_token, ai_reply)
                        if reply_token
                        else push_message(line_user_id, ai_reply)
                    )

                    if not sent.get("success"):
                        raise RuntimeError(f"LINE send failed: {sent}")

                db_update(
                    f"comments/{comment_id}",
                    {
                        "send_result": sent,
                        "sent_at": utc_now()
                    }
                )

                await save_feedback(
                    comment_id,
                    {
                        "admin_action": "auto_sent",
                        "edited_reply": ai_reply
                    }
                )

                await log_event(
                    "line_auto_reply",
                    "success",
                    "Auto reply sent",
                    comment_id=comment_id
                )

            except Exception as exc:
                db_update(
                    f"comments/{comment_id}",
                    {
                        "status": "pending_review",
                        "send_error": str(exc)
                    }
                )

                await log_event(
                    "line_auto_reply",
                    "failed",
                    str(exc),
                    comment_id=comment_id,
                    fallback_used=True,
                    severity="error"
                )

                await notify_admin_for_review(
                    {
                        **data,
                        "status": "pending_review"
                    },
                    comment_id,
                    "Auto Reply Failed"
                )

        if final_status == "pending_review":
            await notify_admin_for_review(
                data,
                comment_id,
                "High Risk" if risk.get("level") == "HIGH" else "Pending Review"
            )

        return {
            "comment_id": comment_id,
            **data
        }

    except Exception as exc:
        await log_event(
            "pipeline",
            "failed",
            str(exc),
            comment_id=comment_id,
            fallback_used=True,
            severity="error"
        )
        raise