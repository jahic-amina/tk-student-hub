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