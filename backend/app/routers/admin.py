from fastapi import APIRouter, Depends, HTTPException, Query
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

class ChangeRoleRequest(BaseModel):
    role: UserRole

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

@router.patch("/users/{user_id}/role", response_model=UserAdminResponse)
def change_user_role(
    user_id: int,
    data: ChangeRoleRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    user = db.exec(select(User).where(User.id == user_id)).first()

    if not user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen.")

    if current_admin.id == user_id:
        raise HTTPException(
            status_code=400,
            detail="Administrator ne može sam sebi promijeniti ulogu."
        )

    user.role = data.role

    db.add(user)
    db.commit()
    db.refresh(user)

    return user