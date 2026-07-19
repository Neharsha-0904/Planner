import uuid
import enum
from datetime import date

from sqlalchemy import String, Integer, Date, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class MilestoneCategory(str, enum.Enum):
    COURSE = "course"
    CERTIFICATION = "certification"
    PROJECT = "project"


class MilestoneStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Milestone(Base):
    __tablename__ = "milestones"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    category: Mapped[MilestoneCategory] = mapped_column(
        Enum(MilestoneCategory, name="milestone_category_enum", create_constraint=True),
        nullable=False,
    )
    target_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    exam_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[MilestoneStatus] = mapped_column(
        Enum(MilestoneStatus, name="milestone_status_enum", create_constraint=True),
        default=MilestoneStatus.NOT_STARTED,
        nullable=False,
    )
    progress_pct: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    user = relationship("User", back_populates="milestones")
    tasks = relationship("Task", back_populates="milestone")
