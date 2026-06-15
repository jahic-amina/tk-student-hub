from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/prakse-i-edukacije", tags=["prakse"])

# -------------------------------------------------------
# Team 1 — Prakse i edukacije
# This is your router. All your endpoints go here.
#
# Example protected endpoint:
#
# @router.get("/")
# def get_prakse(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return {"message": "your code here"}
#
# -------------------------------------------------------

@router.get("/")
def prakse_placeholder():
    return {"message": "Prakse i edukacije router radi — Team 1 ovdje gradi"}
