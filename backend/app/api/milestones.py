import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.milestone import Milestone

router = APIRouter(prefix="/milestones", tags=["milestones"])


class MilestoneRead(BaseModel):
    id: uuid.UUID
    title: str
    category: str
    status: str
    target_date: str | None
    exam_date: str | None
    progress_pct: int

    model_config = {"from_attributes": True}


@router.get("", response_model=list[MilestoneRead])
def list_milestones(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    milestones = db.query(Milestone).filter(Milestone.user_id == current_user.id).all()
    result = []
    for m in milestones:
        result.append(MilestoneRead(
            id=m.id,
            title=m.title,
            category=m.category.value,
            status=m.status.value,
            target_date=m.target_date.isoformat() if m.target_date else None,
            exam_date=m.exam_date.isoformat() if m.exam_date else None,
            progress_pct=m.progress_pct,
        ))
    return result
