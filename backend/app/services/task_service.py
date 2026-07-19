import uuid
from datetime import date

from sqlalchemy import and_, case
from sqlalchemy.orm import Session

from app.models.task import Task, Priority, TaskStatus


def get_tasks_for_view(
    db: Session,
    user_id: uuid.UUID,
    view: str,
    priority: Priority | None = None,
    tags: list[str] | None = None,
) -> list[Task]:
    """Query tasks for a given view with optional filters."""
    today = date.today()
    query = db.query(Task).filter(Task.user_id == user_id)

    if view == "today":
        query = query.filter(
            and_(
                Task.status != TaskStatus.DONE,
                Task.scheduled_for == today,
            )
        )
        # Sort: P0 first, then P1, P2; within same priority, higher rollover count first
        priority_order = case(
            (Task.priority == Priority.P0, 0),
            (Task.priority == Priority.P1, 1),
            (Task.priority == Priority.P2, 2),
        )
        query = query.order_by(priority_order, Task.rolled_over_count.desc())

    elif view == "backlog":
        query = query.filter(
            and_(
                Task.status.in_([TaskStatus.OPEN, TaskStatus.IN_PROGRESS, TaskStatus.BACKLOG]),
                # Only past-due or unscheduled tasks — NOT future-planned ones
                (Task.scheduled_for < today) | (Task.scheduled_for.is_(None)),
            )
        )
        priority_order = case(
            (Task.priority == Priority.P0, 0),
            (Task.priority == Priority.P1, 1),
            (Task.priority == Priority.P2, 2),
        )
        query = query.order_by(
            Task.rolled_over_count.desc(), priority_order, Task.created_at.asc()
        )

    elif view == "done":
        query = query.filter(Task.status == TaskStatus.DONE)
        query = query.order_by(Task.completed_at.desc())

    elif view == "all":
        # All non-done tasks (for calendar view)
        query = query.filter(Task.status != TaskStatus.DONE)
        query = query.order_by(Task.scheduled_for.asc())

    # Apply optional filters
    if priority is not None:
        query = query.filter(Task.priority == priority)
    if tags:
        query = query.filter(Task.tags.overlap(tags))

    return query.all()


def rollover_tasks(db: Session, user_id: uuid.UUID) -> int:
    """Move past-due tasks to today. Returns count of rolled-over tasks."""
    today = date.today()
    tasks = db.query(Task).filter(
        and_(
            Task.user_id == user_id,
            Task.scheduled_for < today,
            Task.status.in_([TaskStatus.OPEN, TaskStatus.IN_PROGRESS]),
        )
    ).all()

    for task in tasks:
        task.scheduled_for = today
        task.rolled_over_count += 1

    db.commit()
    return len(tasks)
