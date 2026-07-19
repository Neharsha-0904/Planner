from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.class_slot import ClassSlot

router = APIRouter(prefix="/class-slots", tags=["timetable"])


class ClassSlotRead(BaseModel):
    id: uuid.UUID
    name: str
    course_code: str | None
    day_of_week: int
    start_time: str
    end_time: str
    location: str | None
    semester: str | None
    active: bool

    model_config = {"from_attributes": True}


@router.get("", response_model=list[ClassSlotRead])
def list_class_slots(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    slots = db.query(ClassSlot).filter(
        ClassSlot.user_id == current_user.id,
        ClassSlot.active == True,
    ).all()
    # Convert time objects to strings for serialization
    result = []
    for s in slots:
        result.append(ClassSlotRead(
            id=s.id,
            name=s.name,
            course_code=s.course_code,
            day_of_week=s.day_of_week,
            start_time=s.start_time.strftime("%H:%M"),
            end_time=s.end_time.strftime("%H:%M"),
            location=s.location,
            semester=s.semester,
            active=s.active,
        ))
    return result
