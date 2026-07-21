from app.database import SessionLocal
from app.models.task import Task, TaskStatus
from app.integrations.telegram import send_telegram
from datetime import date

db = SessionLocal()
today = date.today()

# Today's tasks
today_tasks = db.query(Task).filter(
    Task.scheduled_for == today,
    Task.status != TaskStatus.DONE
).order_by(Task.priority).all()

# Backlog = tasks scheduled BEFORE today that are still open (missed/overdue)
backlog_tasks = db.query(Task).filter(
    Task.scheduled_for < today,
    Task.status.in_(["open", "in_progress"])
).order_by(Task.scheduled_for, Task.priority).all()

# Group backlog by the day they were originally scheduled
from collections import defaultdict
backlog_by_day = defaultdict(list)
for t in backlog_tasks:
    backlog_by_day[t.scheduled_for].append(t)

day_str = today.strftime("%A %d %b")
lines = [f"<b>TODAY — {day_str}</b>", f"{len(today_tasks)} task(s) scheduled", ""]

for t in today_tasks:
    pri = t.priority.value.upper()
    mins = f" ({t.estimated_minutes}min)" if t.estimated_minutes else ""
    lines.append(f"[{pri}] {t.title}{mins}")

if backlog_by_day:
    lines.append("")
    lines.append(f"<b>BACKLOG — {len(backlog_tasks)} missed task(s) from previous days</b>")
    lines.append("<i>(These were not completed on their scheduled day)</i>")
    for day_date in sorted(backlog_by_day.keys()):
        tasks_on_day = backlog_by_day[day_date]
        lines.append(f"\n<b>{day_date.strftime('%b %d')}:</b>")
        for t in tasks_on_day:
            pri = t.priority.value.upper()
            rolled = f" (rolled {t.rolled_over_count}x)" if t.rolled_over_count else ""
            lines.append(f"  [{pri}] {t.title}{rolled}")
else:
    lines.append("")
    lines.append("No backlog. Clean slate!")

send_telegram("\n".join(lines))
db.close()
print("Sent!")

