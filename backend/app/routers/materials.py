from fastapi import APIRouter, Depends
from requests import session
from sqlmodel import Session, select
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.materials import Material, MaterialsResponse
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/materials", tags=["materials"])

# -------------------------------------------------------
# Team 2 — Mentoring
# This is your router. All your endpoints go here.
#
# Example protected endpoint:
#
# @router.get("/")
# def get_mentors(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return {"message": "your code here"}
#
# -------------------------------------------------------

@router.get("/", response_model=list[MaterialsResponse])
def get_materials(session : Session = Depends(get_db)):
    query = (
        select(Material)
        .where(Material.status == "approved")
        .options(selectinload(Material.subject))
        .order_by(Material.created_at.desc())
    )
    materials = session.exec(query).all()
    return materials