"""
Backlog alert job — sends push notifications for overdue/backlog tasks.

Rules:
- P0 tasks in backlog: alert every hour
- All high-priority backlogs: daily summary push
"""
import logging
from datetime import date

from app.database import SessionLocal
from app.models.user import User
from app.models.task import Task, Priority, TaskStatus
from app.services.notification_service import send_push_to_user

logger = logging.getLogger(__name__)


def run_p0_backlog_alert():
    """Hourly job: alert user about P0 tasks still in backlog or overdue."""
    db = SessionLocal()
    try:
        today = date.today()
        users = db.query(User).all()

        for user in users:
            p0_tasks = (
                db.query(Task)
                .filter(
                    Task.user_id == user.id,
                    Task.priority == Priority.P0,
                    Task.status.in_([TaskStatus.OPEN, TaskStatus.IN_PROGRESS]),
                    (Task.scheduled_for < today) | (Task.scheduled_for == None),
                )
                .all()
            )
            if not p0_tasks:
                continue

            count = len(p0_tasks)
            titles = [t.title for t in p0_tasks[:3]]
            title = f"🔴 {count} critical task{'s' if count > 1 else ''} overdue!"
            body = "\n".join(f"• {t}" for t in titles)
            if count > 3:
                body += f"\n...and {count - 3} more"

            send_push_to_user(user, title, body, data={"type": "p0_backlog_alert"})
            logger.info("Sent P0 backlog alert to %s: %d tasks", user.name, count)
    except Exception:
        logger.exception("Error in P0 backlog alert job")
    finally:
        db.close()


def run_daily_backlog_summary():
    """Daily job: summarize full backlog status."""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        today = date.today()

        for user in users:
            backlog_tasks = (
                db.query(Task)
                .filter(
                    Task.user_id == user.id,
                    Task.status.in_([TaskStatus.OPEN, TaskStatus.IN_PROGRESS, TaskStatus.BACKLOG]),
                )
                .all()
            )
            if not backlog_tasks:
                continue

            p0_count = sum(1 for t in backlog_tasks if t.priority == Priority.P0)
            p1_count = sum(1 for t in backlog_tasks if t.priority == Priority.P1)
            p2_count = sum(1 for t in backlog_tasks if t.priority == Priority.P2)
            overdue = [t for t in backlog_tasks if t.scheduled_for and t.scheduled_for < today]

            title = f"📋 Backlog: {len(backlog_tasks)} tasks ({p0_count} critical)"
            lines = []
            if overdue:
                lines.append(f"⚠️ {len(overdue)} overdue")
            lines.append(f"P0: {p0_count} | P1: {p1_count} | P2: {p2_count}")

            # Check threshold
            threshold = (user.prefs or {}).get("backlog_threshold", 15)
            if len(backlog_tasks) > threshold:
                lines.append(f"🚨 Over your {threshold}-task threshold!")

            body = "\n".join(lines)
            send_push_to_user(user, title, body, data={"type": "daily_backlog_summary"})
            logger.info("Sent daily backlog summary to %s: %d tasks", user.name, len(backlog_tasks))
    except Exception:
        logger.exception("Error in daily backlog summary job")
    finally:
        db.close()
