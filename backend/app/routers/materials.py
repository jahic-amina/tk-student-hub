from fastapi import APIRouter, Depends, HTTPException
from requests import session
from sqlmodel import Session, select, func
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.materials import Material, MaterialsResponse, MaterialDetailResponse, Rating
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
        select(
            Material,
            func.avg(Rating.rating).label("average_rating"),
            func.count(Rating.id).label("rating_count")
        )  
        .outerjoin(Rating, Rating.material_id == Material.id) 
        .options(
            selectinload(Material.subject),
            selectinload(Material.user)
        )
        .where(Material.status == "approved")
        .group_by(Material.id)
        .order_by(Material.created_at.desc())
    )
    results = session.exec(query).all()
    materials = []
    for material, avg, count in results:
        material.rating_count = count
        material.average_rating = round(avg, 1) if avg is not None else None
        materials.append(material)
    return materials

@router.get("/{material_id}", response_model=MaterialDetailResponse)
def get_material(material_id: int, session: Session = Depends(get_db)):
    query = (
        select(Material)
        .where(Material.id == material_id)
        .where(Material.status == "approved")
        .options(
            selectinload(Material.subject),
            selectinload(Material.user),
            selectinload(Material.comments),
            selectinload(Material.ratings)
        )
    )
    material = session.exec(query).first()
    
    if not material:
        raise HTTPException(status_code=404, detail="Materijal nije pronadjen")
    
    return material