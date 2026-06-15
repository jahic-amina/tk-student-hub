import os
import mimetypes
import shutil
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, Query
from fastapi.responses import FileResponse
from sqlmodel import Session, select, func
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.materials import Material, MaterialsResponse, MaterialDetailResponse, Rating, Comment, Subject, RatingCreate, CommentResponse, CommentCreate
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.models.materials import Bookmark

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


def get_materials_by_status(
        session: Session, 
        status: str,
        years: Optional[List[int]] = None,
        types: Optional[List[str]] = None,
        subject_id: Optional[int] = None,
        current_user: Optional[User] = None
):

    query = (
        select(
            Material,
            func.avg(Rating.rating).label("average_rating"),
            func.count(Rating.id).label("rating_count")
        )
        .outerjoin(Rating, Rating.material_id == Material.id)
        .where(Material.status == status)
    )
    if years:
        # Moramo uraditi join sa Subject tabelom jer je tamo study_year
        query = query.join(Subject, Material.subject_id == Subject.id).where(Subject.study_year.in_(years))
    
    if types:
        query = query.where(Material.file_type.in_(types))
        
    if subject_id:
        query = query.where(Material.subject_id == subject_id)
    # --------------------

    query = (
        query.options(
            selectinload(Material.subject),
            selectinload(Material.user)
        )
        .group_by(Material.id)
        .order_by(Material.created_at.desc())
    )
    results = session.exec(query).all()

    user_bookmarks = []
    if current_user:
        user_bookmarks = session.exec(
            select(Bookmark.material_id).where(Bookmark.user_id == current_user.id)
        ).all()

    materials = []
    for material, avg, count in results:
        response = MaterialsResponse(
            **material.model_dump(),
            subject=material.subject,
            user=material.user,
            average_rating=round(avg, 1) if avg is not None else None,
            rating_count=count,
            is_bookmarked=material.id in user_bookmarks
        )
        materials.append(response)
    return materials


""" 

DONWLOAD MATERIAL ENDPOINT

"""
@router.get("/{id}/download")
def download_material(
    id: int,
    db: Session = Depends(get_db),
):
    # Pronaci materijal u bazi po ID-u
    material = db.query(Material).filter(Material.id == id).first()
    if material is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Materijal sa tim ID-em ne postoji.",
        )

    if material.status == "deleted":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Materijal je uklonjen.",
        )

    # Provjera statusa 
    if material.status != "approved":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Materijal nije odobren i ne može se preuzeti.",
        )

    # Provjera da fajl fizicki postoji na disku
    if not os.path.exists(material.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fajl nije pronađen na serveru.",
        )

    # Odrediti MIME tip — tip iz baze
    media_type = material.file_type
    if not media_type or "/" not in media_type:
        guessed, _ = mimetypes.guess_type(material.file_path)
        media_type = guessed or "application/octet-stream"

    # Povecaj broj preuzimanja
    material.number_of_downloads += 1
    db.add(material)
    db.commit()

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
def get_materials(
    session: Session = Depends(get_db),
    years: Optional[list[int]] = Query(None), # Prima ?years=1&years=2
    types: Optional[list[str]] = Query(None), # Prima ?types=skripta
    subject_id: Optional[int] = Query(None),
    current_user: Optional[User] = Depends(get_current_user),
):
    # Prosleđujemo filtere u pomoćnu funkciju
    return get_materials_by_status(
        session, 
        "approved", 
        years=years, 
        types=types, 
        subject_id=subject_id,
        current_user=current_user
    )

@router.get("/pending", response_model=list[MaterialsResponse])
def get_pending_materials(session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Samo admin može pristupiti ovom endpointu.")
    return get_materials_by_status(session, "pending")

@router.patch("/{material_id}/approve")
def approve_material(material_id: int, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Samo admin može odobriti materijal.")
    material = session.get(Material, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Materijal nije pronađen.")
    material.status = "approved"
    session.add(material)
    session.commit()
    return {"message": "Materijal odobren."}

@router.patch("/{material_id}/reject")
def reject_material(material_id: int, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Samo admin može odbiti materijal.")
    material = session.get(Material, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Materijal nije pronađen.")
    material.status = "rejected"
    session.add(material)
    session.commit()
    return {"message": "Materijal odbijen."}

@router.get("/subjects", response_model=list[Subject])
def get_subjects(session: Session = Depends(get_db)):
    subjects = session.exec(select(Subject)).all()
    return subjects

@router.get("/{material_id}", response_model=MaterialDetailResponse)
def get_material(material_id: int, session: Session = Depends(get_db)):
    query = (
        select(Material)
        .where(Material.id == material_id)
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
    avg = sum(r.rating for r in material.ratings) / len(material.ratings) if material.ratings else None
    count = len(material.ratings)
    
    return MaterialDetailResponse(
        id=material.id,
        title=material.title,
        description=material.description,
        file_type=material.file_type,
        status=material.status,
        created_at=material.created_at,
        number_of_downloads=material.number_of_downloads,
        subject=material.subject,
        user=material.user,
        comments=material.comments,
        ratings=material.ratings,
        average_rating=round(avg, 1) if avg else None,
        rating_count=count
    )


#amer
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_material(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    material = db.query(Material).filter(Material.id == id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Materijal ne postoji.")

    is_admin = getattr(current_user, "role", "") == "admin"
    is_author = material.user_id == current_user.id

    if not is_admin and not is_author:
        raise HTTPException(
            status_code=403, 
            detail="Nemate dozvolu za brisanje ovog materijala."
        )

    material.status = "deleted"
    db.add(material)
    db.commit()
    return None

"""RATING MATERIAL ENDPOINT"""
@router.post("/{id}/rate", status_code=201)
def rate_material(
    id: int,
    rating_data: RatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    material = db.exec(select(Material).where(Material.id == id)).first()
    if not material:
        raise HTTPException(status_code=404, detail="Materijal nije pronađen.")

    existing = db.exec(
        select(Rating).where(
            Rating.material_id == id,
            Rating.user_id == current_user.id
        )
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Već ste ocijenili ovaj materijal.")

    new_rating = Rating(
        rating=rating_data.rating,
        material_id=id,
        user_id=current_user.id
    )
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating

"""Promijeni ocijenu materijala endpoint"""

@router.patch("/{id}/rate", status_code=200)
def update_rating(
    id: int,
    rating_data: RatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.exec(
        select(Rating).where(
            Rating.material_id == id,
            Rating.user_id == current_user.id
        )
    ).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Niste ocijenili ovaj materijal.")
    
    existing.rating = rating_data.rating
    db.add(existing)
    db.commit()
    db.refresh(existing)
    return existing
# endpoint za dohvatanje komentara materijala
@router.get("/{material_id}/comments", response_model=list[CommentResponse])
def get_comments(material_id: int, session: Session = Depends(get_db)):
    material = session.get(Material, material_id)
    if not material or material.status == "deleted":
        raise HTTPException(status_code=404, detail="Materijal nije pronađen.")
    
    query = (
        select(Comment)
        .where(Comment.material_id == material_id)
        .options(selectinload(Comment.user))
        .order_by(Comment.created_at.desc())
    )
    comments = session.exec(query).all()
    return comments

# Zaštićeni endpoint za dodavanje komentara
@router.post("/{material_id}/comments", response_model=CommentResponse, status_code=201)
def create_comment(
    material_id: int,
    comment_data: CommentCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    material = session.get(Material, material_id)
    if not material or material.status == "deleted":
        raise HTTPException(status_code=404, detail="Materijal nije pronađen.")

    sadrzaj = comment_data.content.strip()
    if not sadrzaj:
        raise HTTPException(status_code=400, detail="Komentar ne može biti prazan.")
    if len(sadrzaj) > 500:
        raise HTTPException(status_code=400, detail="Komentar ne može biti duži od 500 karaktera.")

    novi_komentar = Comment(
        content=sadrzaj,
        material_id=material_id,
        user_id=current_user.id
    )
    session.add(novi_komentar)
    session.commit()
    session.refresh(novi_komentar)


    session.refresh(novi_komentar)
    novi_komentar.user = current_user

    return novi_komentar


# Zaštićeni endpoint za brisanje komentara
@router.delete("/{material_id}/comments/{comment_id}", status_code=204)
def delete_comment(
    material_id: int,
    comment_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    komentar = session.get(Comment, comment_id)
    if not komentar or komentar.material_id != material_id:
        raise HTTPException(status_code=404, detail="Komentar nije pronađen.")

    is_admin = getattr(current_user, "role", "") == "admin"
    is_autor = komentar.user_id == current_user.id

    if not is_admin and not is_autor:
        raise HTTPException(status_code=403, detail="Nemate dozvolu za brisanje ovog komentara.")

    session.delete(komentar)
    session.commit()
    return None
<<<<<<< HEAD




#toggle bookmarka
@router.post("/{material_id}/bookmark")
def toggle_bookmark(
    material_id: int, 
    session: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "admin":
        raise HTTPException(status_code=403, detail="Admini ne mogu bookmarkovati materijale.")

    statement = select(Bookmark).where(
        Bookmark.user_id == current_user.id, 
        Bookmark.material_id == material_id
    )
    bookmark = session.exec(statement).first()

    if bookmark:
        session.delete(bookmark)
        session.commit()
        return {"is_bookmarked": False}
    else:
        new_bookmark = Bookmark(user_id=current_user.id, material_id=material_id)
        session.add(new_bookmark)
        session.commit()
        return {"is_bookmarked": True}
=======
>>>>>>> origin/tim2/dev
