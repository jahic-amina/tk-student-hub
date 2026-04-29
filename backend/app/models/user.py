from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime

class UserRole(str, Enum):
    member = "member"
    mentor = "mentor"
    admin = "admin"

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    full_name: str
    password_hash: str
    role: UserRole = Field(default=UserRole.member)
    created_at: Optional[datetime] = Field(default=None)
