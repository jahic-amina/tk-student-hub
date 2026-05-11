from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
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
