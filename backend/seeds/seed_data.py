"""
Seed script — populates the database with:
- 1 user (Neharsha Vishnu)
- 22 class slots from real M.Tech AI Sem 1 timetable (Aug-Sept 2026)
- Milestones: courses + certs (MS AI Engineer DONE, rest planned) + projects
- 40+ tasks planned through September with realistic scheduling

Run: python -m seeds.seed_data
"""

import sys
from datetime import date, time, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.task import Task, Priority, TaskStatus
from app.models.class_slot import ClassSlot
from app.models.milestone import Milestone, MilestoneCategory, MilestoneStatus

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed():
    db: Session = SessionLocal()

    # Check if already seeded
    existing = db.query(User).filter(User.email == "neharsha@planner.local").first()
    if existing:
        print("Database already seeded. Skipping. (Drop DB and re-run to reseed)")
        db.close()
        return

    # --- User ---
    user = User(
        name="Neharsha Vishnu",
        email="neharsha@planner.local",
        hashed_password=pwd_context.hash("planner123"),
        timezone="Asia/Kolkata",
        prefs={"quiet_hours": "22:00-07:00", "backlog_threshold": 15, "email_frequency": "daily"},
    )
    db.add(user)
    db.flush()

    # --- Class Slots (Sem 1 M.Tech AI, Aug-Nov 2026) ---
    slots = [
        # Monday (day_of_week=0)
        ("Advanced Algorithm Design", "24AI632", 0, time(8, 50), time(9, 40), "ABIII - Seminar Hall"),
        ("Foundations of Artificial Intelligence", "24AI601", 0, time(9, 40), time(10, 30), "ABIII - C203"),
        ("Mathematical Foundations of Computing", "24MA603", 0, time(10, 45), time(11, 35), "ABIII - F303"),
        ("Machine Learning - Lab", "24AI602", 0, time(11, 35), time(13, 15), "ABIII - F303/Anugraha Hall"),
        # Tuesday (day_of_week=1)
        ("Foundations of Artificial Intelligence", "24AI601", 1, time(8, 50), time(9, 40), "ABIII - C203"),
        ("Advanced Algorithm Design - Lab", "24AI632", 1, time(10, 45), time(12, 25), "ABIII - GF F103 Seminar Hall"),
        ("Mastery Over Mind (MAOM)", "22AVP103", 1, time(12, 25), time(13, 15), "Seminar Hall"),
        ("Mathematical Foundations of Computing", "24MA603", 1, time(14, 5), time(14, 55), "ABIII - A103"),
        # Wednesday (day_of_week=2)
        ("Machine Learning", "24AI602", 2, time(8, 50), time(9, 40), "ABIII - F303"),
        ("Foundations of Artificial Intelligence", "24AI601", 2, time(9, 40), time(10, 30), "ABIII - TF Achala"),
        ("Career Competency I (SS)", "23HU601", 2, time(10, 45), time(11, 35), "ABIII - D407"),
        ("Career Competency I (APT)", "23HU601", 2, time(11, 35), time(12, 25), "ABIII - D407"),
        ("Career Competency I (VER)", "23HU601", 2, time(12, 25), time(13, 15), "ABIII - D407"),
        ("Mathematical Foundations of Computing", "24MA603", 2, time(14, 5), time(14, 55), "ABIII - F301"),
        ("Foundations of AI - Lab", "24AI601", 2, time(15, 45), time(16, 35), "ABIII - F301"),
        # Thursday (day_of_week=3)
        ("Mastery Over Mind / Mentoring", "22AVP103", 3, time(8, 0), time(9, 40), "ABIII - Anugraha Hall"),
        ("Advanced Algorithm Design", "24AI632", 3, time(9, 40), time(10, 30), "ABIII - Anugraha Hall"),
        ("Machine Learning", "24AI602", 3, time(10, 45), time(11, 35), "ABIII - C203"),
        ("Mathematical Foundations of Computing", "24MA603", 3, time(12, 25), time(13, 15), "ABIII - F303"),
        ("Research Methodology", "24RM605", 3, time(15, 45), time(16, 35), "D406"),
        # Friday (day_of_week=4)
        ("Advanced Algorithm Design", "24AI632", 4, time(9, 40), time(10, 30), "ABIII - Anugraha Hall"),
        ("Machine Learning", "24AI602", 4, time(10, 45), time(11, 35), "ABIII - C302"),
    ]

    for name, code, day, start, end, location in slots:
        db.add(ClassSlot(
            user_id=user.id, name=name, course_code=code,
            day_of_week=day, start_time=start, end_time=end,
            location=location, semester="Sem 1", active=True,
        ))

    # --- Milestones ---
    milestones_data = [
        # Courses (Sem 1, Aug-Dec 2026)
        ("Mathematical Foundations of Computing", MilestoneCategory.COURSE, date(2026, 12, 15), None, MilestoneStatus.NOT_STARTED, 0),
        ("Foundations of Artificial Intelligence", MilestoneCategory.COURSE, date(2026, 12, 15), None, MilestoneStatus.NOT_STARTED, 0),
        ("Machine Learning", MilestoneCategory.COURSE, date(2026, 12, 15), None, MilestoneStatus.NOT_STARTED, 0),
        ("Advanced Algorithm Design", MilestoneCategory.COURSE, date(2026, 12, 15), None, MilestoneStatus.NOT_STARTED, 0),
        ("Research Methodology", MilestoneCategory.COURSE, date(2026, 12, 15), None, MilestoneStatus.NOT_STARTED, 0),
        # Certifications
        ("Microsoft AI Engineer (AI-102)", MilestoneCategory.CERTIFICATION, date(2026, 7, 1), date(2026, 6, 15), MilestoneStatus.DONE, 100),
        ("Anthropic Claude Developer", MilestoneCategory.CERTIFICATION, date(2026, 7, 10), None, MilestoneStatus.DONE, 100),
        ("AWS Solutions Architect Associate", MilestoneCategory.CERTIFICATION, date(2026, 11, 30), date(2026, 11, 15), MilestoneStatus.NOT_STARTED, 0),
        # Learning paths (self-paced)
        ("Andrew Ng ML Specialization (Coursera)", MilestoneCategory.COURSE, date(2026, 9, 30), None, MilestoneStatus.NOT_STARTED, 0),
        ("Andrej Karpathy Neural Networks Zero-to-Hero", MilestoneCategory.COURSE, date(2026, 10, 31), None, MilestoneStatus.NOT_STARTED, 0),
        ("3Blue1Brown — Essence of Linear Algebra + Calculus", MilestoneCategory.COURSE, date(2026, 8, 31), None, MilestoneStatus.NOT_STARTED, 0),
        # Projects
        ("Multi-Agent RAG System", MilestoneCategory.PROJECT, date(2027, 3, 31), None, MilestoneStatus.NOT_STARTED, 0),
        ("ML Pipeline End-to-End", MilestoneCategory.PROJECT, date(2027, 2, 28), None, MilestoneStatus.NOT_STARTED, 0),
        # DSA
        ("LeetCode 300 (NeetCode 150 + Blind 75 + extras)", MilestoneCategory.PROJECT, date(2027, 3, 31), None, MilestoneStatus.NOT_STARTED, 0),
    ]

    milestone_objs = {}
    for title, category, target, exam, status, pct in milestones_data:
        m = Milestone(
            user_id=user.id, title=title, category=category,
            target_date=target, exam_date=exam, status=status, progress_pct=pct,
        )
        db.add(m)
        db.flush()
        milestone_objs[title] = m

    # --- Tasks (planned through September 2026) ---
    today = date.today()  # 2026-07-20

    def d(offset_days):
        """Helper: date relative to today."""
        return today + timedelta(days=offset_days)

    # Week 1 (Jul 20 - Jul 26): Foundation week
    # Week 2 (Jul 27 - Aug 2): Continue foundations
    # Week 3+ (Aug onwards): Semester starts, balance coursework + self-study

    tasks_data = [
        # === 3Blue1Brown (finish by end of August) ===
        {"title": "3B1B: Essence of Linear Algebra — Ep 1-4 (Vectors, Span, Transformations)", "priority": Priority.P1, "scheduled_for": d(0), "due_date": d(2), "tags": ["learning", "math", "3b1b"], "milestone": "3Blue1Brown — Essence of Linear Algebra + Calculus", "estimated_minutes": 60},
        {"title": "3B1B: Essence of Linear Algebra — Ep 5-8 (Determinants, Inverse, Nonsquare)", "priority": Priority.P1, "scheduled_for": d(2), "due_date": d(4), "tags": ["learning", "math", "3b1b"], "milestone": "3Blue1Brown — Essence of Linear Algebra + Calculus", "estimated_minutes": 60},
        {"title": "3B1B: Essence of Linear Algebra — Ep 9-13 (Eigenvectors, Abstract)", "priority": Priority.P1, "scheduled_for": d(4), "due_date": d(6), "tags": ["learning", "math", "3b1b"], "milestone": "3Blue1Brown — Essence of Linear Algebra + Calculus", "estimated_minutes": 60},
        {"title": "3B1B: Essence of Calculus — Ep 1-5 (Derivatives, Chain rule)", "priority": Priority.P2, "scheduled_for": d(7), "due_date": d(10), "tags": ["learning", "math", "3b1b"], "milestone": "3Blue1Brown — Essence of Linear Algebra + Calculus", "estimated_minutes": 75},
        {"title": "3B1B: Essence of Calculus — Ep 6-10 (Integration, Taylor)", "priority": Priority.P2, "scheduled_for": d(10), "due_date": d(14), "tags": ["learning", "math", "3b1b"], "milestone": "3Blue1Brown — Essence of Linear Algebra + Calculus", "estimated_minutes": 75},
        {"title": "3B1B: Neural Networks series (4 episodes)", "priority": Priority.P1, "scheduled_for": d(14), "due_date": d(17), "tags": ["learning", "ml", "3b1b"], "milestone": "3Blue1Brown — Essence of Linear Algebra + Calculus", "estimated_minutes": 90},

        # === Andrew Ng ML Specialization (start Aug, target Sept 30) ===
        {"title": "Andrew Ng: Course 1 Week 1 — Intro to ML, Supervised Learning", "priority": Priority.P1, "scheduled_for": d(14), "due_date": d(20), "tags": ["learning", "ml", "andrew-ng"], "milestone": "Andrew Ng ML Specialization (Coursera)", "estimated_minutes": 180},
        {"title": "Andrew Ng: Course 1 Week 2 — Linear Regression, Gradient Descent", "priority": Priority.P1, "scheduled_for": d(21), "due_date": d(27), "tags": ["learning", "ml", "andrew-ng"], "milestone": "Andrew Ng ML Specialization (Coursera)", "estimated_minutes": 240},
        {"title": "Andrew Ng: Course 1 Week 3 — Logistic Regression, Regularization", "priority": Priority.P1, "scheduled_for": d(28), "due_date": d(34), "tags": ["learning", "ml", "andrew-ng"], "milestone": "Andrew Ng ML Specialization (Coursera)", "estimated_minutes": 240},
        {"title": "Andrew Ng: Course 2 Week 1 — Neural Networks, Forward Prop", "priority": Priority.P1, "scheduled_for": d(35), "due_date": d(41), "tags": ["learning", "ml", "andrew-ng"], "milestone": "Andrew Ng ML Specialization (Coursera)", "estimated_minutes": 240},
        {"title": "Andrew Ng: Course 2 Week 2 — Training NNs, Backprop", "priority": Priority.P1, "scheduled_for": d(42), "due_date": d(48), "tags": ["learning", "ml", "andrew-ng"], "milestone": "Andrew Ng ML Specialization (Coursera)", "estimated_minutes": 240},
        {"title": "Andrew Ng: Course 2 Week 3 — Decision Trees, Ensembles", "priority": Priority.P1, "scheduled_for": d(49), "due_date": d(55), "tags": ["learning", "ml", "andrew-ng"], "milestone": "Andrew Ng ML Specialization (Coursera)", "estimated_minutes": 240},
        {"title": "Andrew Ng: Course 3 — Unsupervised Learning, Recommenders", "priority": Priority.P1, "scheduled_for": d(56), "due_date": d(68), "tags": ["learning", "ml", "andrew-ng"], "milestone": "Andrew Ng ML Specialization (Coursera)", "estimated_minutes": 360},

        # === Karpathy Neural Networks (start after 3B1B neural nets, ~Aug) ===
        {"title": "Karpathy: makemore Part 1 — Bigrams, Torch basics", "priority": Priority.P2, "scheduled_for": d(18), "due_date": d(21), "tags": ["learning", "ml", "karpathy"], "milestone": "Andrej Karpathy Neural Networks Zero-to-Hero", "estimated_minutes": 120},
        {"title": "Karpathy: makemore Part 2 — MLP", "priority": Priority.P2, "scheduled_for": d(22), "due_date": d(25), "tags": ["learning", "ml", "karpathy"], "milestone": "Andrej Karpathy Neural Networks Zero-to-Hero", "estimated_minutes": 120},
        {"title": "Karpathy: makemore Part 3 — BatchNorm, Activations", "priority": Priority.P2, "scheduled_for": d(26), "due_date": d(30), "tags": ["learning", "ml", "karpathy"], "milestone": "Andrej Karpathy Neural Networks Zero-to-Hero", "estimated_minutes": 120},
        {"title": "Karpathy: Building GPT from scratch", "priority": Priority.P2, "scheduled_for": d(35), "due_date": d(42), "tags": ["learning", "ml", "karpathy"], "milestone": "Andrej Karpathy Neural Networks Zero-to-Hero", "estimated_minutes": 180},
        {"title": "Karpathy: Tokenizers (BPE)", "priority": Priority.P2, "scheduled_for": d(43), "due_date": d(49), "tags": ["learning", "ml", "karpathy"], "milestone": "Andrej Karpathy Neural Networks Zero-to-Hero", "estimated_minutes": 120},

        # === LeetCode (daily habit, start now) ===
        {"title": "LeetCode: Complete NeetCode Arrays & Hashing (9 problems)", "priority": Priority.P1, "scheduled_for": d(0), "due_date": d(3), "tags": ["leetcode", "dsa"], "milestone": "LeetCode 300 (NeetCode 150 + Blind 75 + extras)", "estimated_minutes": 135},
        {"title": "LeetCode: NeetCode Two Pointers (5 problems)", "priority": Priority.P1, "scheduled_for": d(4), "due_date": d(6), "tags": ["leetcode", "dsa"], "milestone": "LeetCode 300 (NeetCode 150 + Blind 75 + extras)", "estimated_minutes": 90},
        {"title": "LeetCode: NeetCode Sliding Window (6 problems)", "priority": Priority.P1, "scheduled_for": d(7), "due_date": d(10), "tags": ["leetcode", "dsa"], "milestone": "LeetCode 300 (NeetCode 150 + Blind 75 + extras)", "estimated_minutes": 120},
        {"title": "LeetCode: NeetCode Stack (7 problems)", "priority": Priority.P1, "scheduled_for": d(11), "due_date": d(14), "tags": ["leetcode", "dsa"], "milestone": "LeetCode 300 (NeetCode 150 + Blind 75 + extras)", "estimated_minutes": 120},
        {"title": "LeetCode: NeetCode Binary Search (7 problems)", "priority": Priority.P1, "scheduled_for": d(15), "due_date": d(19), "tags": ["leetcode", "dsa"], "milestone": "LeetCode 300 (NeetCode 150 + Blind 75 + extras)", "estimated_minutes": 120},
        {"title": "LeetCode: NeetCode Linked List (11 problems)", "priority": Priority.P1, "scheduled_for": d(20), "due_date": d(26), "tags": ["leetcode", "dsa"], "milestone": "LeetCode 300 (NeetCode 150 + Blind 75 + extras)", "estimated_minutes": 180},
        {"title": "LeetCode: NeetCode Trees (15 problems)", "priority": Priority.P1, "scheduled_for": d(27), "due_date": d(37), "tags": ["leetcode", "dsa"], "milestone": "LeetCode 300 (NeetCode 150 + Blind 75 + extras)", "estimated_minutes": 270},
        {"title": "LeetCode: NeetCode Graphs (13 problems)", "priority": Priority.P1, "scheduled_for": d(38), "due_date": d(50), "tags": ["leetcode", "dsa"], "milestone": "LeetCode 300 (NeetCode 150 + Blind 75 + extras)", "estimated_minutes": 270},
        {"title": "LeetCode: NeetCode Dynamic Programming (12 problems)", "priority": Priority.P1, "scheduled_for": d(51), "due_date": d(65), "tags": ["leetcode", "dsa"], "milestone": "LeetCode 300 (NeetCode 150 + Blind 75 + extras)", "estimated_minutes": 300},

        # === AWS SAA Prep (start Sept, slow build) ===
        {"title": "AWS SAA: Ch 1 — Cloud Concepts & AWS Overview", "priority": Priority.P2, "scheduled_for": d(45), "due_date": d(49), "tags": ["cert-prep", "aws"], "milestone": "AWS Solutions Architect Associate", "estimated_minutes": 60},
        {"title": "AWS SAA: Ch 2 — IAM & AWS CLI", "priority": Priority.P2, "scheduled_for": d(50), "due_date": d(54), "tags": ["cert-prep", "aws"], "milestone": "AWS Solutions Architect Associate", "estimated_minutes": 90},
        {"title": "AWS SAA: Ch 3 — EC2 Fundamentals", "priority": Priority.P2, "scheduled_for": d(55), "due_date": d(60), "tags": ["cert-prep", "aws"], "milestone": "AWS Solutions Architect Associate", "estimated_minutes": 90},
        {"title": "AWS SAA: Ch 4 — EC2 Storage (EBS, EFS)", "priority": Priority.P2, "scheduled_for": d(61), "due_date": d(65), "tags": ["cert-prep", "aws"], "milestone": "AWS Solutions Architect Associate", "estimated_minutes": 90},
        {"title": "AWS SAA: Ch 5 — S3", "priority": Priority.P2, "scheduled_for": d(66), "due_date": d(70), "tags": ["cert-prep", "aws"], "milestone": "AWS Solutions Architect Associate", "estimated_minutes": 90},

        # === Projects (start late Aug with small setup tasks) ===
        {"title": "RAG Project: Research LangChain vs LlamaIndex, pick stack", "priority": Priority.P2, "scheduled_for": d(30), "due_date": d(35), "tags": ["project", "rag"], "milestone": "Multi-Agent RAG System", "estimated_minutes": 60},
        {"title": "RAG Project: Set up repo + basic retrieval pipeline", "priority": Priority.P2, "scheduled_for": d(40), "due_date": d(47), "tags": ["project", "rag"], "milestone": "Multi-Agent RAG System", "estimated_minutes": 120},
        {"title": "ML Pipeline: Set up Python env (conda + GPU check)", "priority": Priority.P2, "scheduled_for": d(21), "due_date": d(23), "tags": ["project", "ml"], "milestone": "ML Pipeline End-to-End", "estimated_minutes": 30},
        {"title": "ML Pipeline: EDA on a Kaggle dataset (tabular)", "priority": Priority.P2, "scheduled_for": d(35), "due_date": d(42), "tags": ["project", "ml"], "milestone": "ML Pipeline End-to-End", "estimated_minutes": 120},

        # === Immediate / Career ===
        {"title": "Update LinkedIn — M.Tech AI + MS AI Engineer cert", "priority": Priority.P2, "scheduled_for": d(0), "due_date": d(1), "tags": ["career", "networking"], "estimated_minutes": 15},
        {"title": "Set up Planner daily routine — use every morning", "priority": Priority.P0, "scheduled_for": d(0), "due_date": d(0), "tags": ["personal", "planning"], "estimated_minutes": 10},
        {"title": "Plan weekly review ritual (Sunday 6pm)", "priority": Priority.P2, "scheduled_for": d(1), "due_date": d(3), "tags": ["personal", "planning"], "estimated_minutes": 20},

        # === Python Fundamentals (since user is transitioning from Java) ===
        {"title": "Python: Complete 'Python for Data Science' crash course (NumPy, Pandas basics)", "priority": Priority.P1, "scheduled_for": d(1), "due_date": d(5), "tags": ["learning", "python"], "estimated_minutes": 180},
        {"title": "Python: Practice — solve 10 HackerRank Python challenges", "priority": Priority.P2, "scheduled_for": d(5), "due_date": d(8), "tags": ["learning", "python"], "estimated_minutes": 90},
    ]

    for td in tasks_data:
        milestone_title = td.pop("milestone", None)
        milestone_id = milestone_objs[milestone_title].id if milestone_title else None
        task = Task(user_id=user.id, milestone_id=milestone_id, status=TaskStatus.OPEN, **td)
        db.add(task)

    db.commit()
    db.close()
    print(f"✅ Seeded: 1 user, {len(slots)} class slots, {len(milestones_data)} milestones, {len(tasks_data)} tasks")
    print(f"   Tasks planned from {today} through {today + timedelta(days=70)} (~10 weeks)")
    print(f"   Milestones DONE: Microsoft AI Engineer, Anthropic Claude Developer")
    print(f"   Milestones PLANNED: AWS SAA, Andrew Ng, Karpathy, 3B1B, NeetCode, RAG project, ML pipeline")


if __name__ == "__main__":
    seed()
