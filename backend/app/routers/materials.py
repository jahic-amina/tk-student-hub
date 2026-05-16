from fastapi import APIRouter, Depends, HTTPException
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
        .options(selectinload(Material.subject), 
                 selectinload(Material.user))
        .order_by(Material.created_at.desc())
    )
    materials = session.exec(query).all()
    return materials

@router.get("/{material_id}", response_model=MaterialsResponse)
def get_material(material_id: int, session: Session = Depends(get_db)):
    query = (
        select(Material)
        .where(Material.id == material_id)
        .where(Material.status == "approved")
        .options(
            selectinload(Material.subject),
            selectinload(Material.user)
        )
    )
    material = session.exec(query).first()
    
    if not material:
        raise HTTPException(status_code=404, detail="Materijal nije pronadjen")
    
    return material@router.get("/{material_id}", response_model=MaterialsResponse)