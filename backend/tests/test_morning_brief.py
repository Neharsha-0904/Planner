from datetime import date
from app.models.task import Task, Priority, TaskStatus
from app.services.morning_brief import compose_morning_brief


def test_morning_brief_includes_tasks(db, user):
    """Brief should include today's tasks grouped by priority."""
    today = date.today()
    tasks = [
        Task(user_id=user.id, title="Critical thing", priority=Priority.P0, status=TaskStatus.OPEN, scheduled_for=today),
        Task(user_id=user.id, title="Important thing", priority=Priority.P1, status=TaskStatus.OPEN, scheduled_for=today),
        Task(user_id=user.id, title="Normal thing", priority=Priority.P2, status=TaskStatus.OPEN, scheduled_for=today),
    ]
    for t in tasks:
        db.add(t)
    db.commit()

    subject, body = compose_morning_brief(db, user.id, user.name)

    assert "Morning Brief" in subject
    assert "Critical thing" in body
    assert "Important thing" in body
    assert "Normal thing" in body
    assert body.index("Critical thing") < body.index("Important thing")


def test_morning_brief_empty_day(db, user):
    """Brief for a day with no tasks should say so."""
    subject, body = compose_morning_brief(db, user.id, user.name)

    assert "0 task" in body or "No tasks" in body


def test_morning_brief_shows_rollover_info(db, user):
    """Tasks with rollover count should be flagged in the brief."""
    today = date.today()
    task = Task(
        user_id=user.id,
        title="Neglected task",
        priority=Priority.P0,
        status=TaskStatus.OPEN,
        scheduled_for=today,
        rolled_over_count=5,
    )
    db.add(task)
    db.commit()

    _, body = compose_morning_brief(db, user.id, user.name)

    assert "rolled over" in body.lower()
    assert "5" in body
