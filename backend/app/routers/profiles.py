import os
from uuid import uuid4
from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlmodel import Session, SQLModel, Field, select
from pydantic import BaseModel

from app.database import get_db
from app.core.security import get_current_user, pwd_context
from app.models.user import User

# Pretpostavka da su ovi modeli definisani u app.models.profile
from app.models.profile import UserProfileResponse, AvatarUploadResponse, AvatarDeleteResponse

# --- Pydantic i SQLModel Šeme ---

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    biografija: Optional[str] = None
    godina_studija: Optional[int] = None  # stored as str in User model

class UserResponse(BaseModel):
    id: int
    full_name: Optional[str]
    biografija: Optional[str]
    godina_studija: Optional[str]

    class Config:
        from_attributes = True

class PasswordChangeRequest(SQLModel):
    current_password: str
    new_password: str = Field(min_length=8, description="Nova lozinka mora imati najmanje 8 karaktera")


# --- Konfiguracija Routera i Konstante ---

router = APIRouter(prefix="/profiles", tags=["profiles"])

UPLOAD_DIR = "uploads/"
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
MAX_FILE_SIZE_MB = 5


# --- Rute (Endpoints) ---

@router.get("/")
def profiles_placeholder():
    return {"message": "Profiles router is working — Team 4 builds here"}

# 1. Čitanje profila (Spojene obje GET /me rute u jednu)
@router.get("/me")
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Vraća sve podatke o korisniku potrebne za frontend profil (slika, podaci, biografija).
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "created_at": current_user.created_at,
        "profilna_slika_url": current_user.profilna_slika_url,
        "godina_studija": getattr(current_user, "godina_studija", 1),
        "biografija": getattr(current_user, "biografija", "")
    }

# 2. Ažuriranje profila (tekstualni podaci)
@router.patch("/me", response_model=UserResponse)
def update_profile_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Izdvajamo samo ona polja koja su poslana u JSON zahtjevu
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Ažuriramo trenutnog korisnika
    for key, value in update_data.items():
        setattr(current_user, key, value)
    
    # Spašavamo u bazu
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    # Vraćamo ažurirane, a ne hardkodirane vrijednosti
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "biografija": getattr(current_user, "biografija", ""),
        "godina_studija": getattr(current_user, "godina_studija", None)
    }

# 3. Promjena lozinke
@router.patch("/me/password", status_code=status.HTTP_200_OK)
def change_password(
    data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Provjera trenutne lozinke preko pwd_context-a
    if not pwd_context.verify(data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Trenutna lozinka nije ispravna."
        )
    
    # Provjera da nova lozinka nije ista kao trenutna
    if data.current_password == data.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nova lozinka ne može biti ista kao trenutna."
        )
    
    # Hesiranje nove lozinke i upis u bazu
    current_user.password_hash = pwd_context.hash(data.new_password)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return {"detail": "Lozinka je uspješno izmijenjena."}

# 4. Upload profilne slike
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
    
    with open(os.path.join(UPLOAD_DIR, filename), "wb") as f:
        f.write(contents)
    
    current_user.profilna_slika_url = f"/uploads/{filename}"
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return {"profilna_slika_url": current_user.profilna_slika_url}

# 5. Brisanje profilne slike
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

class PublicProfileResponse(BaseModel):
    id: int
    full_name: str
    biografija: Optional[str] = None
    godina_studija: Optional[str] = None
    profilna_slika_url: Optional[str] = None

    class Config:
        from_attributes = True


@router.get("/public", response_model=list[PublicProfileResponse])
def get_public_profiles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    users = db.exec(
        select(User).where(User.is_active == True)
    ).all()

    return users


@router.get("/{user_id}/public", response_model=PublicProfileResponse)
def get_public_profile_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.exec(
        select(User).where(User.id == user_id, User.is_active == True)
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="Javni profil nije pronađen.")

    return user
