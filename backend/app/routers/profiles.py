from fastapi import APIRouter, Depends
from sqlmodel import Session
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    biografija: Optional[str] = None
    godina_studija: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    full_name: Optional[str]
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
    
    # Unutar funkcije update_profile_me u profiles.py, na samom kraju zamijenite return sa ovim:
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "ime": current_user.full_name.split(" ")[0] if current_user.full_name else "",
        "biografija": "Biografija",
        "godina_studija": 3
    }

@router.get("/me")
def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    Vraća podatke trenutno ulogovanog korisnika.
    """
    # Pošto u auth.py vidimo da model User koristi 'full_name' i 'email':
    return {
        "full_name": current_user.full_name,
        "email": current_user.email,
        "godina_studija": getattr(current_user, "godina_studija", 3),  # ako postoji u bazi
        "biografija": getattr(current_user, "biografija", "")         # ako postoji u bazi
    }