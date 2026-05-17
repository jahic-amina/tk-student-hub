import os
import mimetypes
import shutil
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.responses import FileResponse
from sqlmodel import Session, select, func
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.materials import Material, MaterialsResponse, MaterialDetailResponse, Rating, Comment
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

""" 

DONWLOAD MATERIAL ENDPOINT

"""
@router.get("/{id}/download")
def download_material(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Pronaci materijal u bazi po ID-u
    material = db.query(Material).filter(Material.id == id).first()
    if material is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Materijal sa tim ID-em ne postoji.",
        )

    # Provjera statusa 
    if material.status != "approved":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Materijal nije odobren i ne moze se preuzeti.",
        )

    # Provjera da fajl fizicki postoji na disku
    if not os.path.exists(material.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fajl nije pronadjen na serveru.",
        )

    # Odrediti MIME tip — tip iz baze
    media_type = material.file_type
    if not media_type or "/" not in media_type:
        guessed, _ = mimetypes.guess_type(material.file_path)
        media_type = guessed or "application/octet-stream"

    #  Vratiti fajl korisniku bez ovaranja u novom prozoru
    return FileResponse(
        path=material.file_path,
        filename=os.path.basename(material.file_path),
        media_type=media_type,
    )

#SCRUM-31

ALLOWED_FORMATS = {
    ".pdf",
    ".doc", ".docx",
    ".ppt", ".pptx",
    ".zip",
    ".txt",
}
# -------------------------------------------------------
#SCRUM-32, SCRUM-33, SCRUM-34
def validate_file_format(file: UploadFile):
    extension = "." + file.filename.split(".")[-1].lower()
    if extension not in ALLOWED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Format {extension} nije podržan. Dozvoljeni formati: PDF, DOC, DOCX, PPT, PPTX, ZIP, TXT"
        )
    return extension

def save_file_to_disk(file: UploadFile) -> str:
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{uuid.uuid4()}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path

@router.post("/upload")
def upload_material(
    title: str = Form(...),
    description: str = Form(""),
    subject_id: int = Form(...),
    file_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    extension = validate_file_format(file)
#-------------------------------------------------------------------
   # SCRUM-28 — provjera duplikata
    existing_title = db.exec(
        select(Material).where(
            func.lower(Material.title) == title.strip().lower(),
            Material.user_id == current_user.id
        )
    ).first()

    if existing_title:
        raise HTTPException(
            status_code=409,
            detail="Već ste dodali materijal sa ovim nazivom."
        )

    existing_file = db.exec(
        select(Material).where(
            Material.file_path.contains(file.filename)
        )
    ).first()

    if existing_file:
        raise HTTPException(
            status_code=409,
            detail="Ovaj fajl je već uploadovan."
        )
    # -------------------------------------------------------------

    file_path = save_file_to_disk(file)

    try:

        new_material = Material(
            title=title,
            description=description,
            file_path=file_path,
            file_type=file_type,
            subject_id=subject_id,
            user_id=current_user.id,
            status="pending"
        )
        db.add(new_material)
        db.commit()
        db.refresh(new_material)
        return new_material

    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail="Greška pri uploadu.")
# -------------------------------------------------------

@router.get("/", response_model=list[MaterialsResponse])
def get_materials(session: Session = Depends(get_db)):
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
        response = MaterialsResponse(
            **material.model_dump(),
            subject=material.subject,
            user=material.user,
            average_rating=round(avg, 1) if avg is not None else None,
            rating_count=count
        )
        materials.append(response)
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
            selectinload(Material.comments).selectinload(Comment.user),
            selectinload(Material.ratings),
        )
    )
    material = session.exec(query).first()
    
    if not material:
        raise HTTPException(status_code=404, detail="Materijal nije pronadjen")
    
    material.comments.sort(key=lambda c: c.created_at, reverse=True) 
    return material


#amer
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_material(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Vraćena autentifikacija
):
    material = db.query(Material).filter(Material.id == id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Materijal ne postoji.")

    # Provjera: Admin ili autor materijala
    is_admin = getattr(current_user, "role", "") == "admin"
    is_author = material.user_id == current_user.id

    if not is_admin and not is_author:
        raise HTTPException(
            status_code=403, 
            detail="Nemate dozvolu za brisanje ovog materijala."
        )

    # Soft delete
    material.status = "deleted"
    db.add(material)
    db.commit()
    return None