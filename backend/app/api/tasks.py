import uuid
from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.task import Task, Priority, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate, TaskRead
from app.services.task_service import get_tasks_for_view

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskRead])
def list_tasks(
    view: str = Query("today", pattern="^(today|backlog|done|all)$"),
    priority: Priority | None = None,
    tags: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tag_list = [t.strip() for t in tags.split(",")] if tags else None
    tasks = get_tasks_for_view(db, current_user.id, view, priority=priority, tags=tag_list)
    return tasks


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    body: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = Task(
        user_id=current_user.id,
        title=body.title,
        description=body.description,
        priority=body.priority,
        status=body.status,
        due_date=body.due_date,
        scheduled_for=body.scheduled_for,
        estimated_minutes=body.estimated_minutes,
        parent_task_id=body.parent_task_id,
        milestone_id=body.milestone_id,
        tags=body.tags,
        recurrence_rule=body.recurrence_rule,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(Task).filter(
        Task.id == task_id, Task.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: uuid.UUID,
    body: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(Task).filter(
        Task.id == task_id, Task.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(Task).filter(
        Task.id == task_id, Task.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db.delete(task)
    db.commit()


@router.post("/{task_id}/complete", response_model=TaskRead)
def complete_task(
    task_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(Task).filter(
        Task.id == task_id, Task.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    task.status = TaskStatus.DONE
    task.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(task)
    return task
