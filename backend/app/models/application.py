from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime, timezone


class ApplicationStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    


class Application(SQLModel, table=True):
    __tablename__ = "applications"

    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    ad_id: int = Field(index=True)
    motivational_letter_path: str = Field(default=None)
    cv_path: Optional[str] = Field(default=None)
    linkedin: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    status: ApplicationStatus = Field(default=ApplicationStatus.pending, index=True)
    admin_feedback: Optional[str] = Field(default=None)
    is_archived: bool = Field(default=False, index=True)
    datum: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

class ApplicationCreate(SQLModel):
    motivational_letter_path: str
    cv_path: str = None
    linkedin: Optional[str] = None
    phone: str = None

class ApplicationUpdate(SQLModel):
    status: Optional[ApplicationStatus] = None
    admin_feedback: Optional[str] = None
    is_archived: Optional[bool] = None


