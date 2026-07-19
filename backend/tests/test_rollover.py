from datetime import date, timedelta
from app.models.task import Task, Priority, TaskStatus
from app.services.task_service import rollover_tasks


def test_rollover_moves_past_tasks_to_today(db, user):
    """Tasks with scheduled_for in the past get moved to today."""
    yesterday = date.today() - timedelta(days=1)
    task = Task(
        user_id=user.id,
        title="Overdue task",
        priority=Priority.P1,
        status=TaskStatus.OPEN,
        scheduled_for=yesterday,
        rolled_over_count=0,
    )
    db.add(task)
    db.commit()

    count = rollover_tasks(db, user.id)

    db.refresh(task)
    assert count == 1
    assert task.scheduled_for == date.today()
    assert task.rolled_over_count == 1


def test_rollover_increments_count(db, user):
    """Rollover count accumulates across multiple rollovers."""
    two_days_ago = date.today() - timedelta(days=2)
    task = Task(
        user_id=user.id,
        title="Multi-rollover task",
        priority=Priority.P0,
        status=TaskStatus.IN_PROGRESS,
        scheduled_for=two_days_ago,
        rolled_over_count=3,  # Already rolled over 3 times before
    )
    db.add(task)
    db.commit()

    rollover_tasks(db, user.id)

    db.refresh(task)
    assert task.rolled_over_count == 4
    assert task.scheduled_for == date.today()


def test_rollover_skips_done_tasks(db, user):
    """Completed tasks should NOT be rolled over."""
    yesterday = date.today() - timedelta(days=1)
    task = Task(
        user_id=user.id,
        title="Done task",
        priority=Priority.P1,
        status=TaskStatus.DONE,
        scheduled_for=yesterday,
        rolled_over_count=0,
    )
    db.add(task)
    db.commit()

    count = rollover_tasks(db, user.id)

    db.refresh(task)
    assert count == 0
    assert task.scheduled_for == yesterday  # Unchanged


def test_rollover_skips_future_tasks(db, user):
    """Tasks scheduled for today or future should not be touched."""
    tomorrow = date.today() + timedelta(days=1)
    task = Task(
        user_id=user.id,
        title="Future task",
        priority=Priority.P1,
        status=TaskStatus.OPEN,
        scheduled_for=tomorrow,
        rolled_over_count=0,
    )
    db.add(task)
    db.commit()

    count = rollover_tasks(db, user.id)

    db.refresh(task)
    assert count == 0
    assert task.scheduled_for == tomorrow
