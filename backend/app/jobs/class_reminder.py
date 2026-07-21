"""
Class reminder job — sends a push notification 10 minutes before each class.
Runs every minute, checks for classes starting in the next 10 minutes.
"""
import logging
from datetime import datetime, time, timedelta

import pytz

from app.config import settings
from app.database import SessionLocal
from app.models.user import User
from app.models.class_slot import ClassSlot
from app.services.notification_service import send_push_to_user
from app.integrations.telegram import send_telegram
from app.integrations.whatsapp import send_whatsapp_message
from app.config import settings

logger = logging.getLogger(__name__)

# Map day_of_week (0=Mon) to Python weekday()
DAY_MAP = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6}


def run_class_reminder():
    """Check for classes starting in ~10 minutes and send a push."""
    db = SessionLocal()
    try:
        tz = pytz.timezone(settings.USER_TIMEZONE)
        now = datetime.now(tz)
        current_day = now.weekday()  # 0=Mon
        target_time = (now + timedelta(minutes=10)).time()
        # Window: classes starting between now+9min and now+11min
        window_start = (now + timedelta(minutes=9)).time()
        window_end = (now + timedelta(minutes=11)).time()

        users = db.query(User).all()
        for user in users:
            slots = (
                db.query(ClassSlot)
                .filter(
                    ClassSlot.user_id == user.id,
                    ClassSlot.day_of_week == current_day,
                    ClassSlot.active == True,
                    ClassSlot.start_time >= window_start,
                    ClassSlot.start_time <= window_end,
                )
                .all()
            )
            for slot in slots:
                title = f"Class in {int(minutes_until)} min: {slot.name}"
                body_text = f"{slot.start_time.strftime('%H:%M')} — {slot.location or 'TBD'}"
                send_push_to_user(user, title, body_text)
                # Telegram
                send_telegram(f"<b>Class in {int(minutes_until)} min</b>\n{slot.name}\n{slot.start_time.strftime('%H:%M')} — {slot.location or 'TBD'}")
                # WhatsApp
                if settings.WA_MY_PHONE:
                    send_whatsapp_message(settings.WA_MY_PHONE, f"Class in {int(minutes_until)} min: {slot.name} | {slot.start_time.strftime('%H:%M')} | {slot.location or 'TBD'}")
    except Exception:
        logger.exception("Error in class reminder job")
    finally:
        db.close()
