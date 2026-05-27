from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import BaseModel
from datetime import datetime, timezone

from app.database import get_db
from app.core.security import get_current_user, pwd_context
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
    if not pwd_context.verify(data.password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unesena lozinka nije ispravna."
        )
    
    # b) Postavljanje statusa na 'inactive' i bilježenje vremena
    current_user.status = "inactive"
    current_user.deactivated_at = datetime.now(timezone.utc)
    
    db.add(current_user)
    db.commit()
    
    # c) Invalidacija sesije:
    # S obzirom na to da smo u Koraku 1 podesili da 'get_current_user' automatski 
    # odbija sve 'inactive' korisnike, trenutni JWT token ovog korisnika ovog trenutka 
    # postaje nevažeći (invalidiran) za bilo koju drugu akciju u aplikaciji.
    
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
    if not pwd_context.verify(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unesena lozinka nije ispravna."
        )
    
    if user.status == "active":
        return {"detail": "Nalog je već aktivan."}
        
    # c) Vraćanje statusa na 'active' i postavljanje deactivated_at na NULL
    user.status = "active"
    user.deactivated_at = None
    
    db.add(user)
    db.commit()
    
    return {"detail": "Nalog je uspješno reaktiviran. Sada se možete ponovo prijaviti."}