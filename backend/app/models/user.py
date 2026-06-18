from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import enum
from datetime import datetime
from sqlalchemy import Column, Enum, DateTime

class UserRole(str, enum.Enum):
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
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    profile_picture_url: Optional[str] = Field(default=None)
    biography: Optional[str] = Field(default=None)
    year_of_study: Optional[int] = Field(default=None)
    activity_logs: list["ActivityLog"] = Relationship(back_populates="user")
    deactivated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime, nullable=True)
    )
