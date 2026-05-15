from fastapi import APIRouter, Depends, HTTPException, UploadFile, File,Form
from sqlmodel import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User

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

# -------------------------------------------------------
#SCRUM-31

ALLOWED_FORMATS = {
    ".pdf",
    ".doc", ".docx",
    ".ppt", ".pptx",
    ".zip",
    ".txt",
}
# -------------------------------------------------------
def validate_file_format(file: UploadFile):
    extension = "." + file.filename.split(".")[-1].lower()
    if extension not in ALLOWED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Format {extension} nije podržan. Dozvoljeni formati: PDF, DOC, DOCX, PPT, PPTX, ZIP, TXT"
        )
    return extension

@router.get("/")
def mentoring_placeholder():
    return {"message": "Mentoring router is working — Team 2 builds here"}