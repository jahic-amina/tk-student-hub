import os
import mimetypes
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlmodel import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
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

    # Provjera statusa — samo aktivni materijali mogu se preuzeti
    if material.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Materijal nije aktivan i ne moze se preuzeti.",
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

@router.get("/")
def mentoring_placeholder():
    return {"message": "Mentoring router is working — Team 2 builds here"}