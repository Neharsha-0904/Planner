import logging

from app.database import SessionLocal
from app.models.user import User
from app.models.notification import EmailLog, NotificationType, EmailStatus
from app.services.morning_brief import compose_morning_brief
from app.services.email_service import get_email_service
from app.services.notification_service import send_push_to_user
from app.integrations.telegram import send_telegram
from app.integrations.whatsapp import send_whatsapp_message
from app.config import settings

logger = logging.getLogger(__name__)


def run_morning_brief():
    """Scheduled job: send morning brief via email + Telegram + WhatsApp."""
    db = SessionLocal()
    try:
        email_service = get_email_service()
        users = db.query(User).all()

        for user in users:
            subject, body = compose_morning_brief(db, user.id, user.name)

            # Email
            recipients = list(set([user.email] + (user.notification_emails or [])))
            success = email_service.send(to=recipients, subject=subject, body=body)

            # Push
            send_push_to_user(user, subject, body[:200])

            # Telegram (preferred — free, permanent)
            send_telegram(f"<b>{subject}</b>\n\n{body[:800]}")

            # WhatsApp (if configured)
            if settings.WA_MY_PHONE:
                send_whatsapp_message(settings.WA_MY_PHONE, f"{subject}\n\n{body[:500]}")

            log_entry = EmailLog(
                user_id=user.id,
                type=NotificationType.MORNING_BRIEF,
                subject=subject,
                body=body,
                status=EmailStatus.SENT if success else EmailStatus.FAILED,
            )
            db.add(log_entry)
            db.commit()
    except Exception:
        logger.exception("Error in morning brief job")
    finally:
        db.close()
