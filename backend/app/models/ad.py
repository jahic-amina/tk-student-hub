from typing import Optional
from datetime import datetime, date, timezone
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, field_validator, model_validator, ConfigDict
from app.models.company import Company
from app.models.user import User


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
    company_id: int = Field(foreign_key="companies.id")
    approved_by: Optional[int] = Field(default=None, foreign_key="users.id")

    title: str = Field(max_length=100)
    type: AdType
    field: str = Field(max_length=100)
    location: str = Field(max_length=100)
    description: str
    deadline: date
    duration_months: Optional[int] = None
    compensation: Optional[float] = None
    currency: Optional[str] = Field(default="BAM", max_length=10)
    spots: int = Field(default=1)
    requirements: Optional[str] = None
    benefits: Optional[str] = None
    admin_comment: Optional[str] = None
    changes_requested_at: Optional[datetime] = None

    status: AdStatus = Field(default=AdStatus.pending)
    is_deleted: bool = Field(default=False)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    # Relationships
    company: Optional[Company] = Relationship()
    approver: Optional[User] = Relationship()


class AdCreate(BaseModel):
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

    @field_validator("title", "field", "location", "description", mode="before")
    @classmethod
    def strip_strings(cls, v):
        return _strip_string(v)

    @field_validator("deadline")
    @classmethod
    def deadline_must_be_in_the_future(cls, v):
        return _validate_deadline(v)

    @field_validator("duration_months")
    @classmethod
    def duration_must_be_positive(cls, v):
        return _validate_duration(v)

    @field_validator("compensation")
    @classmethod
    def compensation_must_be_non_negative(cls, v):
        return _validate_compensation(v)

    @field_validator("spots")
    @classmethod
    def spots_must_be_positive(cls, v):
        return _validate_spots(v)

    @model_validator(mode="after")
    def currency_required_if_compensation_set(self):
        if self.compensation is not None and not self.currency:
            raise ValueError("Currency is required when compensation is set.")
        return self


class AdUpdate(BaseModel):
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

    @field_validator("title", "field", "location", "description", mode="before")
    @classmethod
    def strip_strings(cls, v):
        return _strip_string(v)

    @field_validator("deadline")
    @classmethod
    def deadline_must_be_in_the_future(cls, v):
        return _validate_deadline(v)

    @field_validator("duration_months")
    @classmethod
    def duration_must_be_positive(cls, v):
        return _validate_duration(v)

    @field_validator("compensation")
    @classmethod
    def compensation_must_be_non_negative(cls, v):
        return _validate_compensation(v)

    @field_validator("spots")
    @classmethod
    def spots_must_be_positive(cls, v):
        return _validate_spots(v)

    @model_validator(mode="after")
    def currency_required_if_compensation_set(self):
        if self.compensation is not None and not self.currency:
            raise ValueError("Currency is required when compensation is set.")
        return self


class AdPatch(BaseModel):
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

    @field_validator("title", "field", "location", "description", mode="before")
    @classmethod
    def strip_strings(cls, v):
        if v is None:
            return v
        return _strip_string(v)

    @field_validator("deadline")
    @classmethod
    def deadline_must_be_in_the_future(cls, v):
        if v is None:
            return v
        return _validate_deadline(v)

    @field_validator("duration_months")
    @classmethod
    def duration_must_be_positive(cls, v):
        if v is None:
            return v
        return _validate_duration(v)

    @field_validator("compensation")
    @classmethod
    def compensation_must_be_non_negative(cls, v):
        if v is None:
            return v
        return _validate_compensation(v)

    @field_validator("spots")
    @classmethod
    def spots_must_be_positive(cls, v):
        if v is None:
            return v
        return _validate_spots(v)


class StatusUpdate(BaseModel):
    status: AdStatus
    admin_comment: Optional[str] = None
    approved_by: Optional[int] = None


class AdRead(BaseModel):
    id: int
    company_id: int
    company_name: Optional[str] = None
    approved_by: Optional[int] = None
    approver_name: Optional[str] = None
    
    title: str
    type: AdType
    field: str
    location: str
    description: str
    deadline: date
    duration_months: Optional[int] = None
    compensation: Optional[float] = None
    currency: Optional[str] = None
    spots: int
    requirements: Optional[str] = None
    benefits: Optional[str] = None
    admin_comment: Optional[str] = None
    changes_requested_at: Optional[datetime] = None
    
    status: AdStatus
    is_deleted: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    applicants_count: int = 0
    # Modernizovano za Pydantic V2
    model_config = ConfigDict(from_attributes=True)


# --- Validation helpers ---

def _strip_string(v: str) -> str:
    v = v.strip()
    if not v:
        raise ValueError("Field cannot be blank.")
    return v


def _validate_deadline(v: date) -> date:
    if v <= date.today():
        raise ValueError("Deadline must be a future date.")
    return v


def _validate_duration(v: Optional[int]) -> Optional[int]:
    if v is not None and v < 1:
        raise ValueError("Duration must be at least 1 month.")
    return v


def _validate_compensation(v: Optional[float]) -> Optional[float]:
    if v is not None and v < 0:
        raise ValueError("Compensation cannot be negative.")
    return v


def _validate_spots(v: int) -> int:
    if v < 1:
        raise ValueError("Number of spots must be at least 1.")
    return v