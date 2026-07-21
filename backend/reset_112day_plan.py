"""
Reset the database with the full 112-day ML Engineer curriculum.
Clears all existing learning tasks and seeds the complete plan.
"""
import sys
from datetime import date
sys.path.insert(0, ".")

from app.database import SessionLocal
from app.models.user import User
from app.models.task import Task, Priority, TaskStatus
from app.models.milestone import Milestone, MilestoneCategory, MilestoneStatus
from seeds.private_roadmap_v2 import get_curriculum, START_DATE

db = SessionLocal()

# ── 1. Remove all previous learning tasks ────────────────────────────────────
all_tasks = db.query(Task).filter(Task.tags != None).all()
removed = 0
for t in all_tasks:
    if t.tags and any(tag in t.tags for tag in [
        "14-day-plan", "ml-foundations", "andrew-ng", "karpathy",
        "3b1b", "learning", "ml", "leetcode", "dsa", "cert-prep"
    ]):
        db.delete(t)
        removed += 1
db.flush()
print(f"Removed {removed} old learning tasks")

# Also remove the old 14-day milestone
old_ms = db.query(Milestone).filter(Milestone.title.like("%14-Day%")).first()
if old_ms:
    db.delete(old_ms)
    db.flush()
    print("Removed old 14-day milestone")

# ── 2. Create module milestones ───────────────────────────────────────────────
user = db.query(User).first()
user_id = user.user_id if not hasattr(user, 'id') else user.id

milestones = {
    "Foundations": Milestone(
        user_id=user_id, title="Module 1: Foundations (Days 1-15)",
        category=MilestoneCategory.COURSE, status=MilestoneStatus.IN_PROGRESS,
        target_date=START_DATE, progress_pct=0,
    ),
    "Classical ML": Milestone(
        user_id=user_id, title="Module 2: Classical ML (Days 16-39)",
        category=MilestoneCategory.COURSE, status=MilestoneStatus.NOT_STARTED,
        target_date=START_DATE, progress_pct=0,
    ),
    "Deep Learning": Milestone(
        user_id=user_id, title="Module 3: Deep Learning (Days 40-57)",
        category=MilestoneCategory.COURSE, status=MilestoneStatus.NOT_STARTED,
        target_date=START_DATE, progress_pct=0,
    ),
    "MLOps": Milestone(
        user_id=user_id, title="Module 4: MLOps (Days 58-64)",
        category=MilestoneCategory.COURSE, status=MilestoneStatus.NOT_STARTED,
        target_date=START_DATE, progress_pct=0,
    ),
    "LLM": Milestone(
        user_id=user_id, title="Module 5: LLM & Agents (Days 65-75)",
        category=MilestoneCategory.COURSE, status=MilestoneStatus.NOT_STARTED,
        target_date=START_DATE, progress_pct=0,
    ),
    "Capstone": Milestone(
        user_id=user_id, title="Module 6: Capstone & Portfolio (Days 76-112)",
        category=MilestoneCategory.PROJECT, status=MilestoneStatus.NOT_STARTED,
        target_date=START_DATE, progress_pct=0,
    ),
}

for ms in milestones.values():
    db.add(ms)
db.flush()
print(f"Created {len(milestones)} module milestones")

# ── 3. Create tasks for all 112 days ─────────────────────────────────────────
curriculum = get_curriculum()
inserted = 0

for c in curriculum:
    day_date = START_DATE + __import__('datetime').timedelta(days=c["day"] - 1)
    ms = milestones.get(c["module"])
    is_project = c.get("is_project_day", False)
    is_revision = c.get("is_revision_day", False)

    if is_project:
        # Project day: single P0 task
        db.add(Task(
            user_id=user_id,
            milestone_id=ms.id if ms else None,
            title=f"Day {c['day']}: {c['topic']}",
            description=f"Lab: {c['lab']}\nViva: {c['viva']}\nInterview focus: {c['interview']}",
            priority=Priority.P0,
            status=TaskStatus.OPEN,
            scheduled_for=day_date,
            due_date=day_date,
            tags=["112-day-plan", c["module"].lower().replace(" ", "-"), "project", f"day{c['day']:03d}"],
            estimated_minutes=c["mins_lab"],
        ))
        inserted += 1

    elif is_revision:
        # Revision day: single P1 task
        db.add(Task(
            user_id=user_id,
            milestone_id=ms.id if ms else None,
            title=f"Day {c['day']}: {c['topic']}",
            description=f"Focus: {c['focus']}\nLab: {c['lab']}",
            priority=Priority.P1,
            status=TaskStatus.OPEN,
            scheduled_for=day_date,
            due_date=day_date,
            tags=["112-day-plan", c["module"].lower().replace(" ", "-"), "revision", f"day{c['day']:03d}"],
            estimated_minutes=c["mins_lab"],
        ))
        inserted += 1

    else:
        # Normal learning day: 2 tasks
        # Task 1: Watch + notes
        db.add(Task(
            user_id=user_id,
            milestone_id=ms.id if ms else None,
            title=f"Day {c['day']}: [{c['module']}] {c['topic']} — Watch + Notes",
            description=(
                f"Video: {c['video']}\n"
                f"Focus: {c['focus']}\n"
                f"Lecture: {c['lecture']}\n"
                f"Math: {c['math']}\n"
                f"Interview: {c['interview']}"
            ),
            priority=Priority.P0,
            status=TaskStatus.OPEN,
            scheduled_for=day_date,
            due_date=day_date,
            tags=["112-day-plan", c["module"].lower().replace(" ", "-"), "lecture", f"day{c['day']:03d}"],
            estimated_minutes=max(c["mins_video"], 30),
        ))

        # Task 2: Lab + HW
        db.add(Task(
            user_id=user_id,
            milestone_id=ms.id if ms else None,
            title=f"Day {c['day']}: Build {c['deliverable']}",
            description=(
                f"Lab: {c['lab']}\n"
                f"HW: {c['hw']}\n"
                f"Viva: {c['viva']}\n"
                f"Revision: {c['revision']}"
            ),
            priority=Priority.P0,
            status=TaskStatus.OPEN,
            scheduled_for=day_date,
            due_date=day_date,
            tags=["112-day-plan", c["module"].lower().replace(" ", "-"), "lab", f"day{c['day']:03d}"],
            estimated_minutes=c["mins_lab"],
        ))
        inserted += 2

db.commit()
print(f"Inserted {inserted} tasks across {len(curriculum)} days")
print(f"Plan runs: {START_DATE} → {START_DATE + __import__('datetime').timedelta(days=111)}")
print(f"\nToday is Day 1: {curriculum[0]['topic']}")
db.close()
