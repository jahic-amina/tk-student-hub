from fastapi import APIRouter, Depends, HTTPException, UploadFile, File,Form
from sqlmodel import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
import shutil, os
from app.models.materials import Material

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
    file_path = f"uploads/{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return file_path

@router.post("/upload")
def upload_material(
    title: str = Form(...),
    description: str = Form(""),
    subject_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    extension = validate_file_format(file)
    file_path = save_file_to_disk(file)
    
    try:
    
        new_material = Material(
            title=title,
            description=description,
            file_path=file_path,
            file_type=extension,
            subject_id=subject_id,
            user_id=current_user.id
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

@router.get("/")
def mentoring_placeholder():
    return {"message": "Mentoring router is working — Team 2 builds here"}