"""
Startup catch-up — runs when the app starts.

Solves the LOCAL app problem: if the laptop was off during scheduled job times,
this ensures nothing is missed when you finally open it.

On every startup:
1. Run daily rollover if not done today
2. Send morning brief if not sent today
3. Check for classes in the next 60 min and send reminders
"""
import logging
from datetime import date, datetime, timedelta

import pytz

from app.config import settings
from app.database import SessionLocal
from app.models.user import User
from app.models.task import Task, TaskStatus
from app.models.class_slot import ClassSlot
from app.models.notification import EmailLog, NotificationType
from app.services.task_service import rollover_tasks
from app.services.morning_brief import compose_morning_brief
from app.services.email_service import get_email_service
from app.services.notification_service import send_push_to_user

logger = logging.getLogger(__name__)


def run_startup_catchup():
    """Run all missed jobs on app startup."""
    db = SessionLocal()
    try:
        tz = pytz.timezone(settings.USER_TIMEZONE)
        now = datetime.now(tz)
        today = now.date()

        users = db.query(User).all()
        if not users:
            logger.info("No users in DB — skipping startup catch-up")
            return

        for user in users:
            # 1. Rollover if not done today
            overdue_tasks = (
                db.query(Task)
                .filter(
                    Task.user_id == user.id,
                    Task.scheduled_for < today,
                    Task.status.in_([TaskStatus.OPEN, TaskStatus.IN_PROGRESS]),
                )
                .count()
            )
            if overdue_tasks > 0:
                count = rollover_tasks(db, user.id)
                logger.info("Startup rollover: moved %d tasks to today for %s", count, user.name)

            # 2. Morning brief if not sent today
            brief_sent_today = (
                db.query(EmailLog)
                .filter(
                    EmailLog.user_id == user.id,
                    EmailLog.type == NotificationType.MORNING_BRIEF,
                    EmailLog.sent_at >= datetime.combine(today, datetime.min.time()).replace(tzinfo=tz),
                )
                .first()
            )
            if not brief_sent_today:
                subject, body = compose_morning_brief(db, user.id, user.name)
                email_service = get_email_service()
                recipients = [user.email]
                if user.notification_emails:
                    recipients.extend(user.notification_emails)
                recipients = list(set(recipients))
                email_service.send(to=recipients, subject=subject, body=body)
                send_push_to_user(user, subject, body[:200])

                from app.models.notification import EmailStatus
                log_entry = EmailLog(
                    user_id=user.id,
                    type=NotificationType.MORNING_BRIEF,
                    subject=subject,
                    body=body,
                    status=EmailStatus.SENT,
                )
                db.add(log_entry)
                db.commit()
                logger.info("Startup: sent missed morning brief to %s", user.name)

            # 3. Class reminders for the next 60 minutes
            current_day = now.weekday()
            window_end = (now + timedelta(minutes=60)).time()
            upcoming_slots = (
                db.query(ClassSlot)
                .filter(
                    ClassSlot.user_id == user.id,
                    ClassSlot.day_of_week == current_day,
                    ClassSlot.active == True,
                    ClassSlot.start_time >= now.time(),
                    ClassSlot.start_time <= window_end,
                )
                .all()
            )
            for slot in upcoming_slots:
                minutes_until = (
                    datetime.combine(today, slot.start_time).replace(tzinfo=tz) - now
                ).total_seconds() / 60
                title = f"📚 Class in {int(minutes_until)} min: {slot.name}"
                body = f"{slot.start_time.strftime('%H:%M')} — {slot.location or 'TBD'}"
                send_push_to_user(user, title, body)
                logger.info("Startup: class reminder for %s in %d min", slot.name, int(minutes_until))

        logger.info("Startup catch-up complete for %d user(s)", len(users))
    except Exception:
        logger.exception("Error in startup catch-up")
    finally:
        db.close()
