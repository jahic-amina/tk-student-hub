from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/workshops", tags=["workshops"])

# -------------------------------------------------------
# Team 1 — Workshops
# This is your router. All your endpoints go here.
# 
# Example protected endpoint:
#
# @router.get("/")
# def get_workshops(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return {"message": "your code here"}
#
# -------------------------------------------------------

@router.get("/")
def workshops_placeholder():
    return {"message": "Workshops router is working — Team 1 builds here"}