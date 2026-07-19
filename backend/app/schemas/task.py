import uuid
from pydantic import BaseModel
from datetime import date, datetime
from app.models.task import Priority, TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    priority: Priority = Priority.P2
    status: TaskStatus = TaskStatus.OPEN
    due_date: date | None = None
    scheduled_for: date | None = None
    estimated_minutes: int | None = None
    parent_task_id: uuid.UUID | None = None
    milestone_id: uuid.UUID | None = None
    tags: list[str] | None = None
    recurrence_rule: dict | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: Priority | None = None
    status: TaskStatus | None = None
    due_date: date | None = None
    scheduled_for: date | None = None
    estimated_minutes: int | None = None
    actual_minutes: int | None = None
    parent_task_id: uuid.UUID | None = None
    milestone_id: uuid.UUID | None = None
    tags: list[str] | None = None
    recurrence_rule: dict | None = None


class TaskRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    description: str | None = None
    priority: Priority
    status: TaskStatus
    created_at: datetime
    due_date: date | None = None
    scheduled_for: date | None = None
    completed_at: datetime | None = None
    estimated_minutes: int | None = None
    actual_minutes: int | None = None
    parent_task_id: uuid.UUID | None = None
    milestone_id: uuid.UUID | None = None
    tags: list[str] | None = None
    recurrence_rule: dict | None = None
    rolled_over_count: int = 0

    model_config = {"from_attributes": True}
