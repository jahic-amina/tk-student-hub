import re
from pydantic import field_validator
from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from enum import Enum
from datetime import datetime, timezone
from typing import Optional
from app.models.user import User
from app.models.ad import Ad


class ApplicationStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class Application(SQLModel, table=True):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("user_id", "ad_id", name="uq_user_ad"),
        {"extend_existing": True},
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    ad_id: int = Field(foreign_key="ads.id", index=True)

    cv_path: str
    motivational_letter_path: str
    linkedin_url: Optional[str] = Field(default=None)
    github_url: Optional[str] = Field(default=None)
    phone: str

    status: ApplicationStatus = Field(default=ApplicationStatus.pending)
    admin_feedback: Optional[str] = Field(default=None)
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    is_archived: bool = Field(default=False)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: "User" = Relationship()
    ad: "Ad" = Relationship()


class ApplicationCreate(SQLModel):
    ad_id: int
    cv_path: str
    motivational_letter_path: str
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    phone: str

    @field_validator("linkedin_url")
    @classmethod
    def validate_linkedin_url(cls, v):
        return _validate_linkedin_url(v)

    @field_validator("github_url")
    @classmethod
    def validate_github_url(cls, v):
        return _validate_github_url(v)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        return _validate_phone(v)


class ApplicationRead(SQLModel):
    id: int
    user_id: int
    ad_id: int
    cv_path: str
    motivational_letter_path: str
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    phone: str
    status: ApplicationStatus
    admin_feedback: Optional[str] = None
    rating: Optional[int] = None
    is_archived: bool
    created_at: datetime
    updated_at: datetime


class ApplicationUpdate(SQLModel):
    status: Optional[ApplicationStatus] = None
    admin_feedback: Optional[str] = None
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    is_archived: Optional[bool] = None


# --- Validation helpers ---

def _validate_linkedin_url(v: Optional[str]) -> Optional[str]:
    if v is not None:
        pattern = r'^https://(www\.)?linkedin\.com/in/[a-zA-Z0-9_%-]+/?$'
        if not re.match(pattern, v.strip()):
            raise ValueError("LinkedIn URL must be in format https://linkedin.com/in/username.")
    return v


def _validate_github_url(v: Optional[str]) -> Optional[str]:
    if v is not None:
        pattern = r'^https://(www\.)?github\.com/[a-zA-Z0-9_%-]+/?$'
        if not re.match(pattern, v.strip()):
            raise ValueError("GitHub URL must be in format https://github.com/username.")
    return v


def _validate_phone(v: str) -> str:
    pattern = r'^\+?[0-9\s\-\(\)]{7,20}$'
    if not re.match(pattern, v.strip()):
        raise ValueError("Phone number is not in a valid format.")
    return v