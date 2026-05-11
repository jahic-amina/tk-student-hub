from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlmodel import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User, AvatarUploadResponse, AvatarDeleteResponse
from uuid import uuid4
import os

router = APIRouter(prefix="/profiles", tags=["profiles"])

UPLOAD_DIR = "uploads/"
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
MAX_FILE_SIZE_MB = 5

@router.get("/")
def profiles_placeholder():
    return {"message": "Profiles router is working — Team 4 builds here"}

@router.get("/me")
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "created_at": current_user.created_at,
        "profilna_slika_url": current_user.profilna_slika_url
    }

@router.get("/me")
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "created_at": current_user.created_at,
        "profilna_slika_url": current_user.profilna_slika_url
    }

@router.post("/me/avatar", response_model=AvatarUploadResponse)
async def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Neispravan format slike. Dozvoljeni formati su JPEG i PNG.")
    
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"Slika je prevelika. Maksimalna veličina je {MAX_FILE_SIZE_MB} MB.")
    
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid4()}{ext}"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(f"{UPLOAD_DIR}{filename}", "wb") as f:
            f.write(contents)
    
    current_user.profilna_slika_url = f"/uploads/{filename}"
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return {"profilna_slika_url": current_user.profilna_slika_url}

@router.delete("/me/avatar", response_model=AvatarDeleteResponse)
def delete_avatar(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.profilna_slika_url:
        raise HTTPException(status_code=400, detail="Nema postavljenu profilnu sliku.")
    
    file_path = current_user.profilna_slika_url.lstrip("/")
    if os.path.exists(file_path):
        os.remove(file_path)
    
    current_user.profilna_slika_url = None
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return {"message": "Profilna slika obrisana."}
