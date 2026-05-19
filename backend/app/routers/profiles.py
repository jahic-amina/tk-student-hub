from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, SQLModel, Field
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.core.security import get_current_user, pwd_context
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

class PasswordChangeRequest(SQLModel):
    current_password: str
    new_password: str = Field(min_length=8, description="Nova lozinka mora imati najmanje 8 karaktera")

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

    return {
        "full_name": current_user.full_name,
        "email": current_user.email,
        "godina_studija": getattr(current_user, "godina_studija", 3),  # ako postoji u bazi
        "biografija": getattr(current_user, "biografija", "")         # ako postoji u bazi
    }

@router.patch("/me/password", status_code=status.HTTP_200_OK)
def change_password(
    data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Provjera trenutne lozinke preko pwd_context-a
    if not pwd_context.verify(data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Trenutna lozinka nije ispravna."
        )
    
    # 2. Provjera da nova lozinka nije ista kao trenutna
    if data.current_password == data.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nova lozinka ne može biti ista kao trenutna."
        )
    
    # 3. Hesiranje nove lozinke i upis u bazu
    current_user.password_hash = pwd_context.hash(data.new_password)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return {"detail": "Lozinka je uspješno izmijenjena."}