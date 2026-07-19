import uuid
import enum
from datetime import datetime

from sqlalchemy import String, Text, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class NotificationType(str, enum.Enum):
    MORNING_BRIEF = "morning_brief"
    TASK_DUE = "task_due"
    TASK_MISSED = "task_missed"
    BACKLOG_ALERT = "backlog_alert"
    WEEKLY_SUMMARY = "weekly_summary"
    WATCHER_NOTIFY = "watcher_notify"


class EmailStatus(str, enum.Enum):
    SENT = "sent"
    FAILED = "failed"
    SKIPPED = "skipped"


class EmailLog(Base):
    __tablename__ = "email_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType, name="notification_type_enum", create_constraint=True),
        nullable=False,
    )
    subject: Mapped[str] = mapped_column(String(500), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    related_task_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=True
    )
    sent_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    status: Mapped[EmailStatus] = mapped_column(
        Enum(EmailStatus, name="email_status_enum", create_constraint=True),
        default=EmailStatus.SENT,
        nullable=False,
    )
