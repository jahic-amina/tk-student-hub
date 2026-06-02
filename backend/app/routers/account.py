from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import BaseModel
from datetime import datetime, timezone

from app.database import get_db
from app.core.security import get_current_user, verify_password
from app.models.user import User

router = APIRouter(prefix="/account", tags=["account"])

# --- Šeme za Zahtjeve ---
class DeactivateRequest(BaseModel):
    password: str

class ReactivateRequest(BaseModel):
    email: str
    password: str


# --- Rute ---

# 1. DEAKTIVACIJA NALOGA
@router.post("/deactivate", status_code=status.HTTP_200_OK)
def deactivate_account(
    data: DeactivateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # a) Verifikacija lozinke
    if not verify_password(data.password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unesena lozinka nije ispravna."
        )

    current_user.is_active = False
    current_user.deactivated_at = datetime.now(timezone.utc)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return {"detail": "Nalog je uspješno deaktiviran. Sve aktivne sesije su prekinute."}


# 2. REAKTIVACIJA NALOGA
@router.post("/reactivate", status_code=status.HTTP_200_OK)
def reactivate_account(
    data: ReactivateRequest,
    db: Session = Depends(get_db)
):
    # Ovdje NE koristimo Depends(get_current_user) jer je nalog neaktivan 
    # i middleware bi ga blokirao. Korisnik se identifikuje preko Email-a i Lozinke.
    
    # a) Pronalaženje korisnika u bazi
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Korisnik sa ovim emailom ne postoji."
        )
    
    # b) Verifikacija lozinke
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unesena lozinka nije ispravna."
        )
    
    if user.is_active:
        return {"detail": "Nalog je već aktivan."}
        
    # c) Vraćanje is_active na True i postavljanje deactivated_at na NULL
    user.is_active = True
    user.deactivated_at = None
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {"detail": "Nalog je uspješno reaktiviran. Sada se možete ponovo prijaviti."}