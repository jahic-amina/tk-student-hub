from fastapi import APIRouter, Depends
from sqlmodel import Session
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User

class UserUpdate(BaseModel):
    ime: Optional[str] = None
    biografija: Optional[str] = None
    godina_studija: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    ime: Optional[str]
    biografija: Optional[str]
    godina_studija: Optional[int]

    class Config:
        from_attributes = True

router = APIRouter(prefix="/profiles", tags=["profiles"])

# -------------------------------------------------------
# Team 4 — Profiles & Dashboard
# This is your router. All your endpoints go here.
#
# Example protected endpoint:
#
# @router.get("/")
# def get_profile(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return {"message": "your code here"}
#
# -------------------------------------------------------

@router.get("/")
def profiles_placeholder():
    return {"message": "Profiles router is working — Team 4 builds here"}

@router.patch("/me", response_model=UserResponse)
def update_profile_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
   # 1. Izdvajamo samo ona polja koja su poslana u JSON zahtjevu
    update_data = user_update.model_dump(exclude_unset=True)
    
    # 2. Ažuriramo trenutnog korisnika
    for key, value in update_data.items():
        setattr(current_user, key, value)
    
    # 3. Spašavamo u bazu pomoću SQLModel-a
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return current_user