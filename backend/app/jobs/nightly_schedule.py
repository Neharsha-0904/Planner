"""
Nightly schedule job — sends tomorrow's classes at 9 PM via email + WhatsApp.
"""
import logging
from datetime import date, timedelta

from app.database import SessionLocal
from app.models.user import User
from app.models.class_slot import ClassSlot
from app.services.email_service import get_email_service
from app.integrations.whatsapp import send_whatsapp_message
from app.config import settings

logger = logging.getLogger(__name__)

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def run_nightly_schedule():
    """9 PM job: send tomorrow's class schedule via email + WhatsApp."""
    db = SessionLocal()
    try:
        tomorrow = date.today() + timedelta(days=1)
        dow = tomorrow.weekday()

        users = db.query(User).all()
        for user in users:
            slots = (
                db.query(ClassSlot)
                .filter(
                    ClassSlot.user_id == user.id,
                    ClassSlot.day_of_week == dow,
                    ClassSlot.active == True,
                )
                .order_by(ClassSlot.start_time)
                .all()
            )

            if not slots:
                continue

            # Build message
            lines = [
                f"TOMORROW'S CLASSES - {DAY_NAMES[dow]}, {tomorrow.strftime('%B %d')}",
                f"{len(slots)} class(es):",
                "",
            ]
            for s in slots:
                lines.append(f"  {s.start_time.strftime('%H:%M')}-{s.end_time.strftime('%H:%M')}  {s.name}")
                lines.append(f"      Room: {s.location or 'TBD'}")
                lines.append("")

            body = "\n".join(lines)
            subject = f"[Planner] Tomorrow's Classes - {DAY_NAMES[dow]}, {tomorrow.strftime('%b %d')}"

            # Email
            email_service = get_email_service()
            recipients = [user.email]
            if user.notification_emails:
                recipients.extend(user.notification_emails)
            email_service.send(to=list(set(recipients)), subject=subject, body=body)

            # WhatsApp
            if settings.WA_MY_PHONE:
                wa_msg = f"*{subject}*\n\n{body}"
                send_whatsapp_message(settings.WA_MY_PHONE, wa_msg)

            logger.info("Sent tomorrow's schedule to %s: %d classes", user.name, len(slots))
    except Exception:
        logger.exception("Error in nightly schedule job")
    finally:
        db.close()
