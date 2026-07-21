"""
Replace Andrew Ng + Karpathy tasks with the 14-day ML Foundations curriculum.
Starts from today (2026-07-22).
"""
import sys
from datetime import date, timedelta

sys.path.insert(0, ".")

from sqlalchemy import cast, text
from app.database import SessionLocal, engine
from app.models.task import Task, Priority, TaskStatus
from app.models.milestone import Milestone, MilestoneCategory, MilestoneStatus

db = SessionLocal()
today = date(2026, 7, 22)

# ── 1. Remove Andrew Ng + Karpathy tasks ────────────────────────────────────
all_tasks = db.query(Task).filter(Task.tags != None).all()
deleted_count = 0
for t in all_tasks:
    if t.tags and any(tag in t.tags for tag in ["andrew-ng", "karpathy", "3b1b"]):
        db.delete(t)
        deleted_count += 1
db.flush()
print(f"Deleted {deleted_count} Andrew Ng / Karpathy / 3B1B tasks...")

# ── 2. Create/find the 14-day plan milestone ─────────────────────────────────
user = db.query(Milestone).first()
user_id = user.user_id if user else None

plan_ms = db.query(Milestone).filter(Milestone.title.like("%14-Day%")).first()
if not plan_ms:
    plan_ms = Milestone(
        user_id=user_id,
        title="14-Day ML Foundations Sprint",
        category=MilestoneCategory.COURSE,
        target_date=today + timedelta(days=13),
        status=MilestoneStatus.IN_PROGRESS,
        progress_pct=0,
    )
    db.add(plan_ms)
    db.flush()
    print("Created milestone: 14-Day ML Foundations Sprint")

# ── 3. Curriculum ─────────────────────────────────────────────────────────────
curriculum = [
    {
        "day": 1, "topic": "Python & NumPy Foundations",
        "video": "NumPy Crash Course", "deliverable": "day01_numpy_basics.ipynb",
        "focus": "Arrays, dtype, shape, ndim, indexing",
        "hw": "25 NumPy exercises — build array utilities without shortcuts",
        "interview": "Why NumPy over Python lists?",
        "mins_video": 60, "mins_hw": 90,
    },
    {
        "day": 2, "topic": "Advanced NumPy",
        "video": "NumPy Crash Course (Advanced)", "deliverable": "day02_numpy_advanced.ipynb",
        "focus": "Slicing, views vs copies, reshaping, broadcasting",
        "hw": "Reimplement broadcasting examples + matrix manipulation tasks",
        "interview": "Explain broadcasting to an interviewer",
        "mins_video": 60, "mins_hw": 90,
    },
    {
        "day": 3, "topic": "Pandas for ML",
        "video": "Pandas Official Tutorials", "deliverable": "day03_pandas.ipynb",
        "focus": "Series, DataFrame, indexing, filtering",
        "hw": "Titanic dataset — clean + explore",
        "interview": "Why Pandas before ML?",
        "mins_video": 60, "mins_hw": 90,
    },
    {
        "day": 4, "topic": "Data Visualization",
        "video": "Matplotlib + Seaborn Intro", "deliverable": "day04_visualization.ipynb",
        "focus": "Scatter, histogram, boxplot, heatmap",
        "hw": "Plot Titanic insights + visual EDA report",
        "interview": "Which plot would you choose?",
        "mins_video": 60, "mins_hw": 90,
    },
    {
        "day": 5, "topic": "Linear Algebra I — Vectors",
        "video": "3Blue1Brown Essence of Linear Algebra #1-2", "deliverable": "day05_vectors.ipynb",
        "focus": "Vectors, basis, coordinate systems, dot product",
        "hw": "Implement vector operations from scratch",
        "interview": "Why is dot product important?",
        "mins_video": 45, "mins_hw": 90,
    },
    {
        "day": 6, "topic": "Linear Algebra II — Matrices",
        "video": "3Blue1Brown #3-4", "deliverable": "day06_matrices.ipynb",
        "focus": "Matrix multiplication, transformations",
        "hw": "Matrix multiplication from scratch + transformation problems",
        "interview": "Matrix vs vector interview questions",
        "mins_video": 45, "mins_hw": 90,
    },
    {
        "day": 7, "topic": "Statistics I",
        "video": "StatQuest Statistics Playlist", "deliverable": "day07_statistics.ipynb",
        "focus": "Mean, median, mode, variance, standard deviation",
        "hw": "Implement statistics library from scratch",
        "interview": "Why standard deviation? Bias vs variance.",
        "mins_video": 60, "mins_hw": 90,
    },
    {
        "day": 8, "topic": "Probability & Bayes",
        "video": "StatQuest Probability Playlist", "deliverable": "day08_probability.ipynb",
        "focus": "Conditional probability, Bayes theorem",
        "hw": "Bayesian probability calculator",
        "interview": "Real-world probability + Bayes questions",
        "mins_video": 60, "mins_hw": 90,
    },
    {
        "day": 9, "topic": "Calculus for ML",
        "video": "Calculus Essentials", "deliverable": "day09_calculus.ipynb",
        "focus": "Derivatives, slopes, gradients, chain rule",
        "hw": "Numerical differentiation implementation",
        "interview": "Why derivatives in ML?",
        "mins_video": 60, "mins_hw": 90,
    },
    {
        "day": 10, "topic": "Optimization & Gradient Descent",
        "video": "Gradient Descent Intuition", "deliverable": "day10_optimization.ipynb",
        "focus": "Cost surfaces, minima, learning rate",
        "hw": "Visualize optimization + learning-rate experiments",
        "interview": "Local minima, why optimization?",
        "mins_video": 60, "mins_hw": 90,
    },
    {
        "day": 11, "topic": "ML Introduction",
        "video": "Stanford CS229 Lecture 1", "deliverable": "day11_intro_ml.ipynb",
        "focus": "Supervised vs Unsupervised, ML workflow",
        "hw": "First ML pipeline + read about datasets",
        "interview": "Types of ML, ML basics",
        "mins_video": 75, "mins_hw": 60,
    },
    {
        "day": 12, "topic": "Linear Regression Intuition",
        "video": "Stanford CS229 Lecture 1 (continued)", "deliverable": "day12_regression_intro.ipynb",
        "focus": "Hypothesis function, training examples",
        "hw": "Predict house prices manually + small regression worksheet",
        "interview": "Why linear regression? Regression intuition.",
        "mins_video": 60, "mins_hw": 90,
    },
    {
        "day": 13, "topic": "Cost Function (MSE)",
        "video": "Stanford CS229 Lecture 1", "deliverable": "day13_cost_function.ipynb",
        "focus": "Mean Squared Error, error surface intuition",
        "hw": "Implement MSE without numpy.mean()",
        "interview": "Why MSE instead of MAE?",
        "mins_video": 45, "mins_hw": 90,
    },
    {
        "day": 14, "topic": "Gradient Descent from Scratch",
        "video": "Stanford CS229 Lecture 1", "deliverable": "day14_gradient_descent.ipynb",
        "focus": "Gradient Descent algorithm, convergence",
        "hw": "Implement Gradient Descent from scratch on California Housing",
        "interview": "20-question viva + whiteboard explanation",
        "mins_video": 60, "mins_hw": 120,
    },
]

inserted = 0
for c in curriculum:
    d = today + timedelta(days=c["day"] - 1)

    # Main study task (video + notes)
    db.add(Task(
        user_id=user_id,
        milestone_id=plan_ms.id,
        title=f"Day {c['day']}: {c['topic']} — Watch + Notes",
        description=f"Video: {c['video']}\nFocus: {c['focus']}\nInterview prep: {c['interview']}",
        priority=Priority.P0,
        status=TaskStatus.OPEN,
        scheduled_for=d,
        due_date=d,
        tags=["14-day-plan", "ml-foundations", f"day{c['day']:02d}"],
        estimated_minutes=c["mins_video"],
    ))

    # Homework/lab task
    db.add(Task(
        user_id=user_id,
        milestone_id=plan_ms.id,
        title=f"Day {c['day']}: Build {c['deliverable']}",
        description=f"Lab: {c['hw']}",
        priority=Priority.P0,
        status=TaskStatus.OPEN,
        scheduled_for=d,
        due_date=d,
        tags=["14-day-plan", "ml-foundations", "lab", f"day{c['day']:02d}"],
        estimated_minutes=c["mins_hw"],
    ))
    inserted += 2

db.commit()
db.close()
print(f"Done! Inserted {inserted} tasks for Days 1-14 (Jul 22 - Aug 4)")
print(f"Today (Day 1): Python & NumPy Foundations")
