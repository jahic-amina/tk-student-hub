import os
import mimetypes
import shutil
import uuid
import fitz
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, Query
from fastapi.responses import FileResponse
from sqlmodel import Session, select, func
from app.database import get_db
from app.core.security import get_current_user, decode_access_token
from app.models.user import User, UserRole
from app.models.materials import (
    Material, MaterialsResponse, MaterialDetailResponse, 
    Rating, Comment, Subject, RatingCreate, CommentResponse, CommentCreate, Bookmark, Download, PaginatedMaterialsResponse, 
)
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.models.notification import Notification, NotificationType, NotificationCreate
from app.services.activity_log_service import log_activity
from app.enums.activity import ActivityType
from datetime import datetime

router = APIRouter(prefix="/materials", tags=["materials"])


def get_materials_by_status(
        session: Session,
    status: Optional[str],
        years: Optional[List[int]] = None,
        types: Optional[List[str]] = None,
        subject_id: Optional[int] = None,
    user_id: Optional[int] = None,
        current_user: Optional[User] = None,
):
    query = (
        select(
            Material,
            func.avg(Rating.rating).label("average_rating"),
            func.count(Rating.id).label("rating_count"),
        )
        .outerjoin(Rating, Rating.material_id == Material.id)
    )
    if status is not None:
        query = query.where(Material.status == status)
    if years:
        query = query.join(Subject, Material.subject_id == Subject.id).where(Subject.study_year.in_(years))
    if types:
        query = query.where(Material.file_type.in_(types))
    if subject_id:
        query = query.where(Material.subject_id == subject_id)
    if user_id is not None:
        query = query.where(Material.user_id == user_id).where(Material.status != "deleted")

    query = (
        query.options(
            selectinload(Material.subject),
            selectinload(Material.user),
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
            is_bookmarked=material.id in user_bookmarks,
        )
        materials.append(response)
    return materials


ALLOWED_FORMATS = {".pdf", ".doc", ".docx", ".ppt", ".pptx", ".zip", ".txt"}


def validate_file_format(file: UploadFile):
    extension = "." + file.filename.split(".")[-1].lower()
    if extension not in ALLOWED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Format {extension} nije podržan. Dozvoljeni formati: PDF, DOC, DOCX, PPT, PPTX, ZIP, TXT",
        )
    return extension


def save_file_to_disk(file: UploadFile) -> str:
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{uuid.uuid4()}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path

# Generisanje thumbnail-a prve stranice PDF-a
def generate_thumbnail(file_path: str) -> Optional[str]:
    try:
        thumbnail_dir = "uploads/thumbnails"
        os.makedirs(thumbnail_dir, exist_ok=True)
        thumbnail_path = f"{thumbnail_dir}/{os.path.basename(file_path)}.png"
        
        # Ako je PDF - direktno generiši
        if file_path.lower().endswith('.pdf'):
            doc = fitz.open(file_path)
            page = doc[0]
            pix = page.get_pixmap(matrix=fitz.Matrix(0.5, 0.5))
            pix.save(thumbnail_path)
            doc.close()
            return thumbnail_path
        
        # Za PPTX, DOCX, PPT, DOC - konvertuj u PDF pa generiši
        convertable = ('.pptx', '.ppt', '.docx', '.doc')
        if any(file_path.lower().endswith(ext) for ext in convertable):
            import subprocess
            result = subprocess.run([
                            '/opt/homebrew/bin/soffice', '--headless', '--convert-to', 'pdf',
                '--outdir', '/tmp', file_path
            ], capture_output=True, timeout=30)
            
            pdf_path = f"/tmp/{os.path.basename(file_path).rsplit('.', 1)[0]}.pdf"
            if os.path.exists(pdf_path):
                doc = fitz.open(pdf_path)
                page = doc[0]
                pix = page.get_pixmap(matrix=fitz.Matrix(0.5, 0.5))
                pix.save(thumbnail_path)
                doc.close()
                os.remove(pdf_path)
                return thumbnail_path
        
        return None
    except Exception as e:
        return None

# ---------------------------------------------------------------------------
# NOTE: Static/fixed-path routes MUST come before parameterized routes
# (e.g. /subjects, /pending, /upload) so FastAPI doesn't match them against
# /{id} or /{material_id}.
# ---------------------------------------------------------------------------

@router.get("/subjects", response_model=list[Subject])
def get_subjects(session: Session = Depends(get_db)):
    return session.exec(select(Subject)).all()


@router.get("/pending", response_model=list[MaterialsResponse])
def get_pending_materials(
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Samo admin može pristupiti ovom endpointu.")
    return get_materials_by_status(session, "pending")


@router.post("/upload")
def upload_material(
    title: str = Form(...),
    description: str = Form(""),
    subject_id: int = Form(...),
    file_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    validate_file_format(file)

    existing_title = db.exec(
        select(Material).where(
            func.lower(Material.title) == title.strip().lower(),
            Material.user_id == current_user.id,
        )
    ).first()
    if existing_title:
        raise HTTPException(status_code=409, detail="Već ste dodali materijal sa ovim nazivom.")

    existing_file = db.exec(
        select(Material).where(Material.file_path.contains(file.filename))
    ).first()
    if existing_file:
        raise HTTPException(status_code=409, detail="Ovaj fajl je već uploadovan.")

    file_path = save_file_to_disk(file)
    thumbnail_path = generate_thumbnail(file_path) 
    try:
        new_material = Material(
            title=title,
            description=description,
            file_path=file_path,
            file_type=file_type,
            subject_id=subject_id,
            user_id=current_user.id,
            status="pending",
            thumbnail_path=thumbnail_path,
        )
        db.add(new_material)
        db.commit()
        db.refresh(new_material)

        admini = db.exec(select(User).where(User.role == UserRole.admin)).all()
        for admin in admini:
            tekst = f"Novi materijal '{new_material.title}' čeka odobrenje."
            db.add(Notification(
                user_id=admin.id,
                text=tekst,
                type=NotificationType.MATERIAL_PENDING_APPROVAL
            ))
        db.commit()
        subject = db.get(Subject, subject_id)
        log_activity(
            db,
            current_user.id,
            ActivityType.material_posted,
            new_material.title,
            f"{subject.name if subject else ''} · {file_type.upper()}",
            new_material.id 
        )

        return new_material
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail="Greška pri uploadu.")


@router.get("/", response_model=PaginatedMaterialsResponse)
def get_materials(
    session: Session = Depends(get_db),
    years: Optional[list[int]] = Query(None),
    types: Optional[list[str]] = Query(None),
    subject_id: Optional[int] = Query(None),
    mine_only: bool = Query(False),
    current_user: Optional[User] = Depends(get_current_user),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=50),
):
    user_id = current_user.id if mine_only and current_user else None
    status = "approved" if not mine_only else None

    if mine_only and current_user is None:
        raise HTTPException(status_code=401, detail="Niste prijavljeni.")

    svi = get_materials_by_status(
        session,
        status or "approved",
        years=years,
        types=types,
        subject_id=subject_id,
        user_id=user_id,
        current_user=current_user,
    )
    total = len(svi)
    start = (page - 1) * per_page
    end = start + per_page
    return PaginatedMaterialsResponse(
        items=svi[start:end],
        total=total,
        page=page,
        per_page=per_page,
        total_pages=(total + per_page - 1) // per_page,
    )

@router.get("/{id}/preview")
def preview_material(id: int, db: Session = Depends(get_db)):
    material = db.exec(select(Material).where(Material.id == id)).first()
    if not material:
        raise HTTPException(status_code=404, detail="Materijal sa tim ID-em ne postoji.")
    if not os.path.exists(material.file_path):
        raise HTTPException(status_code=404, detail="Fajl nije pronađen na serveru.")
    
    media_type, _ = mimetypes.guess_type(material.file_path)    
    media_type = media_type or "application/octet-stream"
    
    return FileResponse(
        path=material.file_path,
        media_type=media_type,
        headers={
            "Content-Disposition": "inline"
        })

@router.get("/{id}/download")
def download_material(
    id: int,
    db: Session = Depends(get_db),
    token: Optional[str] = Query(None),
):
    # Provjera da li materijal postoji
    material = db.exec(select(Material).where(Material.id == id)).first()
    if material is None:
        raise HTTPException(status_code=404, detail="Materijal sa tim ID-em ne postoji.")
    
    # Provjera da li je materijal obrisan ili nije odobren
    if material.status == "deleted":
        raise HTTPException(status_code=404, detail="Materijal je uklonjen.")

    is_admin = False
    if token:
        payload = decode_access_token(token)
        if payload:
            user_id_from_token = payload.get("sub")
            if user_id_from_token:
                user = db.get(User, int(user_id_from_token))
                if user and user.role == UserRole.admin:
                    is_admin = True

    if material.status != "approved" and not is_admin:
        raise HTTPException(status_code=403, detail="Materijal nije odobren i ne može se preuzeti.")

    # Provjera da fajl fizički postoji na serveru
    if not os.path.exists(material.file_path):
        raise HTTPException(status_code=404, detail="Fajl nije pronađen na serveru.")

    # Odrediti tip fajla za FileResponse header
    media_type = material.file_type
    if not media_type or "/" not in media_type:
        guessed, _ = mimetypes.guess_type(material.file_path)
        media_type = guessed or "application/octet-stream"

    # Povećaj broj preuzimanja
    material.number_of_downloads += 1
    db.add(material)

   # Bilježi ko je preuzeo koristeći query token
    if token:
        payload = decode_access_token(token)
        if payload:
            user_id = payload.get("sub")
            if user_id:
                already = db.exec(
                    select(Download).where(
                        Download.material_id == id,
                        Download.user_id == int(user_id)
                    )
                ).first()
                if not already:
                    db.add(Download(material_id=id, user_id=int(user_id)))

    db.commit()

    return FileResponse(
        path=material.file_path,
        filename=os.path.basename(material.file_path),
        media_type=media_type,
    )

# Vraća true/false — da li je prijavljeni korisnik preuzeo ovaj materijal
# Koristi se u frontendu da odluči da li prikazati zvjezdice kao aktivne
@router.get("/{id}/has-downloaded")
def has_downloaded(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # mora biti prijavljen
):
    result = db.exec(
        select(Download).where(
            Download.material_id == id,
            Download.user_id == current_user.id
        )
    ).first()
    return {"has_downloaded": result is not None}

@router.patch("/{material_id}/approve")
def approve_material(
    material_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Samo admin može odobriti materijal.")
    material = session.get(Material, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Materijal nije pronađen.")
    material.status = "approved"
    session.add(material)

    tekst = f"Vaš materijal '{material.title}' je odobren i sada je vidljiv ostalim studentima."
    session.add(Notification(
        user_id=material.user_id,
        text=tekst,
        type=NotificationType.STATUS_CHANGE
    ))

    session.commit()
    return {"message": "Materijal odobren."}


@router.patch("/{material_id}/reject")
def reject_material(
    material_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Samo admin može odbiti materijal.")
    material = session.get(Material, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Materijal nije pronađen.")
    material.status = "rejected"
    session.add(material)

    tekst = f"Vaš materijal '{material.title}' je odbijen."
    session.add(Notification(
        user_id=material.user_id,
        text=tekst,
        type=NotificationType.STATUS_CHANGE
    ))

    session.commit()
    return {"message": "Materijal odbijen."}

@router.patch("/{material_id}/update")
def update_material(
    material_id: int,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    subject_id: Optional[int] = Form(None),
    material_type: Optional[str] = Form(None),
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    material = session.get(Material, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Materijal nije pronađen.")
    if material.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nemate dozvolu za ažuriranje ovog materijala.")
    if title:
        material.title = title
    if description:
        material.description = description
    if subject_id:
        material.subject_id = subject_id
    if material_type:
        material.file_type = material_type
    if file:
        validate_file_format(file)
        if os.path.exists(material.file_path):
            os.remove(material.file_path)
        new_file_path = save_file_to_disk(file)
        material.file_path = new_file_path
        material.file_type = file.content_type
        material.status = "pending"  
    session.add(material)
    session.commit()
    session.refresh(material)
    return {"message": "Materijal ažuriran."}

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
    return session.exec(query).all()


@router.post("/{material_id}/comments", response_model=CommentResponse, status_code=201)
def create_comment(
    material_id: int,
    comment_data: CommentCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    material = session.get(Material, material_id)
    if not material or material.status == "deleted":
        raise HTTPException(status_code=404, detail="Materijal nije pronađen.")

    sadrzaj = comment_data.content.strip()
    if not sadrzaj:
        raise HTTPException(status_code=400, detail="Komentar ne može biti prazan.")
    if len(sadrzaj) > 500:
        raise HTTPException(status_code=400, detail="Komentar ne može biti duži od 500 karaktera.")

    novi_komentar = Comment(content=sadrzaj, material_id=material_id, user_id=current_user.id)
    session.add(novi_komentar)
    session.commit()
    session.refresh(novi_komentar)
    novi_komentar.user = current_user
    return novi_komentar


@router.delete("/{material_id}/comments/{comment_id}", status_code=204)
def delete_comment(
    material_id: int,
    comment_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    komentar = session.get(Comment, comment_id)
    if not komentar or komentar.material_id != material_id:
        raise HTTPException(status_code=404, detail="Komentar nije pronađen.")

    if current_user.role != UserRole.admin and komentar.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nemate dozvolu za brisanje ovog komentara.")

    session.delete(komentar)
    session.commit()
    return None

@router.patch("/{material_id}/comments/{comment_id}", response_model=CommentResponse)
def update_comment(
    material_id: int,
    comment_id: int,
    comment_data: CommentCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = session.get(Comment, comment_id)
    if not comment or comment.material_id != material_id:
        raise HTTPException(status_code=404, detail="Komentar nije pronađen.")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nemate dozvolu za uređivanje ovog komentara.")

    content = comment_data.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="Komentar ne može biti prazan.")
    if len(content) > 500:
        raise HTTPException(status_code=400, detail="Komentar ne može biti duži od 500 karaktera.")

    comment.content = content
    comment.updated_at = datetime.utcnow()
    session.add(comment)
    session.commit()
    session.refresh(comment)
    comment.user = current_user
    return comment

@router.post("/{id}/rate", status_code=201)
def rate_material(
    id: int,
    rating_data: RatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Provjera da li materijal postoji
    material = db.exec(select(Material).where(Material.id == id)).first()
    if not material:
        raise HTTPException(status_code=404, detail="Materijal nije pronađen.")
    
    # Provjera da li je korisnik preuzeo materijal prije ocjenjivanja
    download = db.exec(
        select(Download).where(
            Download.material_id == id,
            Download.user_id == current_user.id
        )
    ).first()
    if not download:
        raise HTTPException(status_code=403, detail="Morate preuzeti materijal prije ocjenjivanja.")

    # Provjera da li je korisnik već ocijenio ovaj materijal
    existing = db.exec(
        select(Rating).where(Rating.material_id == id, Rating.user_id == current_user.id)
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Već ste ocijenili ovaj materijal.")

    # Sačuvaj novu ocjenu
    new_rating = Rating(rating=rating_data.rating, material_id=id, user_id=current_user.id)
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    
    if material.user_id != current_user.id:
        text = f"Vaš materijal '{material.title}' je ocijenjen sa {rating_data.rating}/5."
        db.add(Notification(
            user_id=material.user_id,
            text=text,
            type=NotificationType.MATERIAL_GRADED
        ))
        db.commit()
    return new_rating


@router.patch("/{id}/rate", status_code=200)
def update_rating(
    id: int,
    rating_data: RatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Provjera da li je korisnik preuzeo materijal prije izmjene ocjene
    download = db.exec(
        select(Download).where(
            Download.material_id == id,
            Download.user_id == current_user.id
        )
    ).first()
    if not download:
        raise HTTPException(status_code=403, detail="Morate preuzeti materijal prije ocjenjivanja.")

    # Provjera da li korisnik ima postojeću ocjenu koju mijenja
    existing = db.exec(
        select(Rating).where(Rating.material_id == id, Rating.user_id == current_user.id)
    ).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Niste ocijenili ovaj materijal.")
    
    # Ažuriraj ocjenu
    existing.rating = rating_data.rating
    db.add(existing)
    db.commit()
    db.refresh(existing)
    return existing


@router.post("/{material_id}/bookmark")
def toggle_bookmark(
    material_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == UserRole.admin:
        raise HTTPException(status_code=403, detail="Admini ne mogu bookmarkovati materijale.")

    statement = select(Bookmark).where(
        Bookmark.user_id == current_user.id,
        Bookmark.material_id == material_id,
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
        raise HTTPException(status_code=404, detail="Materijal nije pronađen")

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
        rating_count=count,
        thumbnail_path=material.thumbnail_path,
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_material(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    material = db.exec(select(Material).where(Material.id == id)).first()
    if not material:
        raise HTTPException(status_code=404, detail="Materijal ne postoji.")

    if current_user.role != UserRole.admin and material.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nemate dozvolu za brisanje ovog materijala.")

    material.status = "deleted"
    db.add(material)
    db.commit()
    return None
