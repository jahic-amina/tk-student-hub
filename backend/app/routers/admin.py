from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from typing import Optional
from pydantic import BaseModel
from app.database import get_db
from app.models.user import User, UserRole
from app.core.security import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])

class UserAdminResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: UserRole
    is_active: bool
    

    class Config:
        from_attributes = True


class UsersListResponse(BaseModel):
    users: list[UserAdminResponse]
    total: int
    prikazano: int

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=403,
            detail="Pristup dozvoljen samo administratorima"
        )
    return current_user

@router.get("/users", response_model=UsersListResponse)
def get_all_users(
    search: Optional[str] = Query(None, description="Pretraga po imenu ili emailu"),
    role: Optional[UserRole] = Query(None, description="Filter po ulozi"),
    is_active: Optional[bool] = Query(None, description="Filter po statusu"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin) 
):
    query = select(User)

    if search:
        query = query.where(
            (User.full_name.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%"))
        )

    if role:
        query = query.where(User.role == role)

    if is_active is not None:
        query = query.where(User.is_active == is_active)

    users = db.exec(query).all()

    return {
        "users": users,
        "total": len(users),
        "prikazano": len(users)
    }


@router.post("/users/{id}/deactivate")
def deactivate_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    
    # Sigurnosna provjera: Spriječi admina da deaktivira sam sebe
    if current_user.id == id:
        raise HTTPException(
            status_code=400,
            detail="Ne možete mijenjati status vlastitog administratorskog računa."
        )
    # 1. Pronađi korisnika u bazi preko ID-ja
    user = db.exec(select(User).where(User.id == id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")
    
    # 2. Postavi status na False (deaktiviran)
    user.is_active = False
    
    # 3. Spasi izmjene u bazu
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {"message": f"Korisnik {user.full_name} je uspješno deaktiviran."}


@router.post("/users/{id}/activate")
def activate_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    # Sigurnosna provjera: Spriječi admina da deaktivira sam sebe
    if current_user.id == id:
        raise HTTPException(
            status_code=400,
            detail="Ne možete mijenjati status vlastitog administratorskog računa."
        )

    # 1. Pronađi korisnika u bazi preko ID-ja
    user = db.exec(select(User).where(User.id == id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")
    
    # 2. Postavi status na True (aktiviran)
    user.is_active = True
    
    # 3. Spasi izmjene u bazu
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {"message": f"Korisnik {user.full_name} je uspješno aktiviran."}

@router.delete("/users/{user_id}", status_code=200)
async def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin) 
):
    # 1. Pronađi korisnika u bazi
    user = db.exec(select(User).where(User.id == user_id)).first()
    
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="Korisnik nije pronađen."
        )
    
    # 2. Sigurnosna provjera: Spriječi admina da obriše sam sebe
    if current_admin.id == user_id:
        raise HTTPException(
            status_code=400, 
            detail="Ne možete obrisati vlastiti administratorski račun."
        )
        
    try:
        # 3. Trajno brisanje iz baze podataka
        db.delete(user)
        db.commit()
        
        return {"message": "Korisnik je uspješno trajno obrisan."}
        
    except Exception as e:
        db.rollback()
        print(f"Greška pri brisanju: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Došlo je do greške na serveru prilikom brisanja korisnika."
        )