import uuid
import enum
from datetime import datetime, date

from sqlalchemy import (
    String, Text, Integer, ForeignKey, DateTime, Date, JSON, Enum, func, ARRAY
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Priority(str, enum.Enum):
    P0 = "p0"
    P1 = "p1"
    P2 = "p2"


class TaskStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BACKLOG = "backlog"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    priority: Mapped[Priority] = mapped_column(
        Enum(Priority, name="priority_enum", create_constraint=True),
        default=Priority.P2,
        nullable=False,
    )
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status_enum", create_constraint=True),
        default=TaskStatus.OPEN,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    scheduled_for: Mapped[date | None] = mapped_column(Date, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    estimated_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    actual_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)

    parent_task_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=True
    )
    milestone_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("milestones.id"), nullable=True
    )

    tags: Mapped[list[str] | None] = mapped_column(
        ARRAY(String), nullable=True
    )
    recurrence_rule: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    rolled_over_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    user = relationship("User", back_populates="tasks")
    milestone = relationship("Milestone", back_populates="tasks")
    parent_task = relationship("Task", remote_side="Task.id", backref="subtasks")
