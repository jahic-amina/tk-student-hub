from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
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
    status: str

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
    # 1. Pronađi korisnika u bazi preko ID-ja
    user = db.exec(select(User).where(User.id == id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")
    
    # 2. Postavi status na False (deaktiviran)
    user.is_active = False
    user.status = "inactive"
    
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
    # 1. Pronađi korisnika u bazi preko ID-ja
    user = db.exec(select(User).where(User.id == id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")
    
    # 2. Postavi status na True (aktiviran)
    user.is_active = True
    user.status = "active"
    
    # 3. Spasi izmjene u bazu
    db.add(user)
    db.commit()
    db.refresh(user)

    print(f"\n[ADMIN AKCIJA] Korisnik {user.email} je upravo aktiviran. Baza sada kaže -> is_active: {user.is_active}, status: {user.status}\n")

    
    return {"message": f"Korisnik {user.full_name} je uspješno aktiviran."}