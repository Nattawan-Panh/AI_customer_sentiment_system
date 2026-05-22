import os
import smtplib
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.services.firebase_service import db_push


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def send_admin_email(
    subject,
    body,
    comment_id=None,
    notification_type="review_required"
):
    host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    admin_email = os.getenv("ADMIN_EMAIL")
    from_name = os.getenv(
        "EMAIL_FROM_NAME",
        "AI Customer Sentiment System"
    )

    subject = str(subject or "AI Review Required").strip()
    body = str(body or "").strip()

    if not user or not password or not admin_email:
        error_message = "SMTP_USER, SMTP_PASSWORD, or ADMIN_EMAIL is missing"

        ref = db_push("notifications", {
            "type": notification_type,
            "channel": "email",
            "status": "failed",
            "subject": subject,
            "body": body,
            "comment_id": comment_id,
            "error": error_message,
            "created_at": utc_now()
        })

        return {
            "notification_id": ref.key,
            "status": "failed",
            "error": error_message
        }

    msg = MIMEMultipart()
    msg["From"] = f"{from_name} <{user}>"
    msg["To"] = admin_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP(host, port, timeout=15) as server:
            server.starttls()
            server.login(user, password)
            server.send_message(msg)

        ref = db_push("notifications", {
            "type": notification_type,
            "channel": "email",
            "status": "sent",
            "subject": subject,
            "body": body,
            "comment_id": comment_id,
            "created_at": utc_now()
        })

        return {
            "notification_id": ref.key,
            "status": "sent"
        }

    except Exception as e:
        ref = db_push("notifications", {
            "type": notification_type,
            "channel": "email",
            "status": "failed",
            "subject": subject,
            "body": body,
            "comment_id": comment_id,
            "error": str(e),
            "created_at": utc_now()
        })

        return {
            "notification_id": ref.key,
            "status": "failed",
            "error": str(e)
        }