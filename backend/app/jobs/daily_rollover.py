import logging

from app.database import SessionLocal
from app.models.user import User
from app.services.task_service import rollover_tasks

logger = logging.getLogger(__name__)


def run_daily_rollover():
    """Scheduled job: roll over incomplete past-due tasks to today."""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        for user in users:
            count = rollover_tasks(db, user.id)
            if count > 0:
                logger.info("Rolled over %d task(s) for user %s", count, user.name)
    except Exception:
        logger.exception("Error in daily rollover job")
    finally:
        db.close()
