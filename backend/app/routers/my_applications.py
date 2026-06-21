from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.application import Application, ApplicationRead, ApplicationStatus
from app.models.ad import Ad
from pydantic import BaseModel
router = APIRouter(prefix="/applications/me", tags=["My Applications"])

from pydantic import BaseModel

class StudentProfilApplicationResponse(BaseModel):
    id: int
    naziv: str
    kompanija: str
    status: ApplicationStatus

@router.get("/all", response_model=List[StudentProfilApplicationResponse])
def get_my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = select(Application).where(
        Application.user_id == current_user.id,
        Application.is_archived == False,
        Application.status.in_([ApplicationStatus.pending, ApplicationStatus.accepted])
    )
    applications = db.exec(statement).all()

    result = []
    for app in applications:
        ad = db.get(Ad, app.ad_id)
        result.append({
            "id": app.id,
            "naziv": ad.title if ad else "Nepoznata praksa",
            "kompanija": ad.company.company_name if ad and ad.company else "",
            "status": app.status
        })

    return result