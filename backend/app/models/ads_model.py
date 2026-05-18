from typing import Optional
from datetime import datetime, date
from enum import Enum
from sqlmodel import SQLModel, Field
from pydantic import BaseModel, field_validator


class AdStatus(str, Enum):
    active = "active"
    expired = "expired"
    pending = "pending"
    rejected = "rejected"
    changes_requested = "changes_requested"


class AdType(str, Enum):
    internship = "internship"
    education = "education"
    scholarship = "scholarship"


class Ad(SQLModel, table=True):
    __tablename__ = "ads"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign keys
    company_id: int = Field(foreign_key="companies.id")
    approved_by: Optional[int] = Field(
        default=None, foreign_key="users.id"
    )

    # Basic info
    title: str = Field(max_length=100)
    type: AdType
    field: str = Field(max_length=100)
    location: str = Field(max_length=100)
    description: str

    # Details
    deadline: date
    duration_months: Optional[int] = None
    compensation: Optional[float] = None
    currency: Optional[str] = Field(default="BAM", max_length=10)
    spots: int = Field(default=1)

    # Additional info
    requirements: Optional[str] = None
    benefits: Optional[str] = None
    admin_comment: Optional[str] = None
    changes_requested_at: Optional[datetime] = None

    # Status & soft delete
    status: AdStatus = Field(default=AdStatus.pending)
    is_deleted: bool = Field(default=False)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


class AdCreate(BaseModel):
    company_id: int
    title: str
    type: AdType
    field: str
    location: str
    description: str
    deadline: date
    duration_months: Optional[int] = None
    compensation: Optional[float] = None
    currency: Optional[str] = "BAM"
    spots: int = 1
    requirements: Optional[str] = None
    benefits: Optional[str] = None

    @field_validator("deadline")
    @classmethod
    def deadline_must_be_future(cls, v):
        if v <= date.today():
            raise ValueError("Deadline must be a future date.")
        return v

    @field_validator("spots")
    @classmethod
    def spots_must_be_positive(cls, v):
        if v < 1:
            raise ValueError("Number of spots must be at least 1.")
        return v


class AdUpdate(BaseModel):
    """Full update – PUT (all fields required except those with defaults)."""
    title: str
    type: AdType
    field: str
    location: str
    description: str
    deadline: date
    duration_months: Optional[int] = None
    compensation: Optional[float] = None
    currency: Optional[str] = "BAM"
    spots: int = 1
    requirements: Optional[str] = None
    benefits: Optional[str] = None

    @field_validator("deadline")
    @classmethod
    def deadline_must_be_future(cls, v):
        if v <= date.today():
            raise ValueError("Deadline must be a future date.")
        return v

    @field_validator("spots")
    @classmethod
    def spots_must_be_positive(cls, v):
        if v < 1:
            raise ValueError("Number of spots must be at least 1.")
        return v


class AdPatch(BaseModel):
    """Partial update – PATCH (all fields optional)."""
    title: Optional[str] = None
    type: Optional[AdType] = None
    field: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[date] = None
    duration_months: Optional[int] = None
    compensation: Optional[float] = None
    currency: Optional[str] = None
    spots: Optional[int] = None
    requirements: Optional[str] = None
    benefits: Optional[str] = None
    status: Optional[AdStatus] = None
    admin_comment: Optional[str] = None


class StatusUpdate(BaseModel):
    status: AdStatus
    admin_comment: Optional[str] = None
    approved_by: Optional[int] = None