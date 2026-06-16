from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.application import Application, ApplicationRead, ApplicationStatus

router = APIRouter(prefix="/applications/me", tags=["My Applications"])

@router.get("/all", response_model=List[ApplicationRead])
def get_my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = select(Application).where(
        Application.user_id == current_user.id,
        Application.is_archived == False,
        Application.status.in_([ApplicationStatus.pending, ApplicationStatus.accepted])
    )
    return db.exec(statement).all()