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