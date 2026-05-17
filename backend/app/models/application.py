from pydantic import ConfigDict
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from enum import Enum
from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint

class ApplicationStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

class Application(SQLModel, table=True):
    __tablename__ = "applications"
    __table_args__ = (UniqueConstraint("user_id", "ad_id", name="uq_user_ad"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    ad_id: int = Field(foreign_key="ads.id", index=True)

    cv_path: str
    motivational_letter_path: str
    linkedin: Optional[str] = Field(default=None)
    phone: str

    status: ApplicationStatus = Field(default=ApplicationStatus.pending, index=True)
    admin_feedback: Optional[str] = Field(default=None)
    is_archived: bool = Field(default=False, index=True)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: "User" = Relationship(back_populates="applications")
    ad: "Ad" = Relationship(back_populates="applications")

class ApplicationCreate(SQLModel):
    ad_id: int
    cv_path: str
    motivational_letter_path: str
    linkedin: Optional[str] = None
    phone: str

class ApplicationRead(SQLModel):
    id: int
    user_id: int
    ad_id: int
    cv_path: str
    motivational_letter_path: str
    linkedin: Optional[str]
    phone: str
    status: ApplicationStatus
    admin_feedback: Optional[str]
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    model_config=ConfigDict(from_attributes=True)
    

class ApplicationUpdate(SQLModel):
    status: Optional[ApplicationStatus] = None
    admin_feedback: Optional[str] = None
    is_archived: Optional[bool] = None


Application.model_rebuild()
