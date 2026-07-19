import logging

from app.database import SessionLocal
from app.models.user import User
from app.models.notification import EmailLog, NotificationType, EmailStatus
from app.services.morning_brief import compose_morning_brief
from app.services.email_service import get_email_service
from app.services.notification_service import send_push_to_user

logger = logging.getLogger(__name__)


def run_morning_brief():
    """Scheduled job: compose and send the morning brief to all users via email + push."""
    db = SessionLocal()
    try:
        email_service = get_email_service()
        users = db.query(User).all()

        for user in users:
            subject, body = compose_morning_brief(db, user.id, user.name)

            # Collect all email addresses for this user
            recipients = [user.email]
            if user.notification_emails:
                recipients.extend(user.notification_emails)
            # Deduplicate
            recipients = list(set(recipients))

            success = email_service.send(to=recipients, subject=subject, body=body)

            # Also send as push notification (short version)
            send_push_to_user(user, subject, body[:200])

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
