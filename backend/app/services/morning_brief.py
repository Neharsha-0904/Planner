from datetime import date

from sqlalchemy.orm import Session

from app.models.task import Task, TaskStatus, Priority


def compose_morning_brief(db: Session, user_id, user_name: str) -> tuple[str, str]:
    """Compose the morning brief email. Returns (subject, body)."""
    today = date.today()

    tasks = (
        db.query(Task)
        .filter(Task.user_id == user_id, Task.scheduled_for == today, Task.status != TaskStatus.DONE)
        .all()
    )

    p0_tasks = [t for t in tasks if t.priority == Priority.P0]
    p1_tasks = [t for t in tasks if t.priority == Priority.P1]
    p2_tasks = [t for t in tasks if t.priority == Priority.P2]

    subject = f"☀️ Morning Brief — {today.strftime('%A, %B %d')}"

    lines = [
        f"Good morning, {user_name}!",
        f"You have {len(tasks)} task(s) scheduled for today.",
        "",
    ]

    if p0_tasks:
        lines.append("🔴 P0 — Critical:")
        for t in p0_tasks:
            rolled = f" (rolled over {t.rolled_over_count}x)" if t.rolled_over_count else ""
            lines.append(f"  • {t.title}{rolled}")
        lines.append("")

    if p1_tasks:
        lines.append("🟡 P1 — Important:")
        for t in p1_tasks:
            rolled = f" (rolled over {t.rolled_over_count}x)" if t.rolled_over_count else ""
            lines.append(f"  • {t.title}{rolled}")
        lines.append("")

    if p2_tasks:
        lines.append("🔵 P2 — Normal:")
        for t in p2_tasks:
            lines.append(f"  • {t.title}")
        lines.append("")

    if not tasks:
        lines.append("No tasks scheduled for today. Enjoy the free day or pull something from your backlog!")

    body = "\n".join(lines)
    return subject, body
