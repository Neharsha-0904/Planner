import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from app.config import settings

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler(timezone=settings.USER_TIMEZONE)


def start_scheduler():
    """Register jobs and start the APScheduler."""
    from app.jobs.daily_rollover import run_daily_rollover
    from app.jobs.morning_brief import run_morning_brief
    from app.jobs.class_reminder import run_class_reminder
    from app.jobs.backlog_alert import run_p0_backlog_alert, run_daily_backlog_summary

    # Daily rollover at midnight
    scheduler.add_job(
        run_daily_rollover,
        trigger=CronTrigger(hour=0, minute=1),
        id="daily_rollover",
        replace_existing=True,
    )

    # Morning brief email
    scheduler.add_job(
        run_morning_brief,
        trigger=CronTrigger(hour=settings.MORNING_BRIEF_HOUR, minute=0),
        id="morning_brief",
        replace_existing=True,
    )

    # Class reminder — runs every minute, checks for classes in 10 min
    scheduler.add_job(
        run_class_reminder,
        trigger=IntervalTrigger(minutes=1),
        id="class_reminder",
        replace_existing=True,
    )

    # P0 backlog alert — every hour during waking hours (7am-10pm)
    scheduler.add_job(
        run_p0_backlog_alert,
        trigger=CronTrigger(hour="7-22", minute=0),
        id="p0_backlog_alert",
        replace_existing=True,
    )

    # Daily backlog summary — once at 8am
    scheduler.add_job(
        run_daily_backlog_summary,
        trigger=CronTrigger(hour=8, minute=30),
        id="daily_backlog_summary",
        replace_existing=True,
    )

    scheduler.start()
    logger.info(
        "APScheduler started with jobs: daily_rollover (00:01), morning_brief (%02d:00), "
        "class_reminder (every 1min), p0_backlog_alert (hourly 7-22), daily_backlog_summary (08:30)",
        settings.MORNING_BRIEF_HOUR,
    )


def stop_scheduler():
    """Gracefully shut down the scheduler."""
    scheduler.shutdown(wait=False)
    logger.info("APScheduler shut down.")
