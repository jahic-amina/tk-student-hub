from typing import Optional
from datetime import datetime, date
from enum import Enum
from sqlmodel import SQLModel, Field


class OglasStatus(str, Enum):
    active = "active"
    expired = "expired"
    pending = "pending"
    rejected = "rejected"
    changes_requested = "changes_requested"


class OglasTip(str, Enum):
    praksa = "praksa"
    edukacija = "edukacija"
    stipendija = "stipendija"


class Oglas(SQLModel, table=True):
    __tablename__ = "oglasi"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign keys
    kompanija_id: int = Field(foreign_key="kompanije.id")
    approved_by: Optional[int] = Field(
        default=None, foreign_key="users.id"
    )

    # Basic info
    naziv: str = Field(max_length=100)
    tip: OglasTip
    oblast: str = Field(max_length=100)
    lokacija: str = Field(max_length=100)
    opis: str

    # Details
    rok: date
    trajanje: Optional[str] = Field(default=None, max_length=50)
    naknada: Optional[str] = Field(default=None, max_length=50)
    broj_mjesta: int = Field(default=1)
    placeno: bool = Field(default=False)

    # New fields
    requirements: Optional[str] = None
    benefits: Optional[str] = None
    admin_comment: Optional[str] = None
    changes_requested_at: Optional[datetime] = None

    # Status & soft delete
    status: OglasStatus = Field(default=OglasStatus.pending)
    is_deleted: bool = Field(default=False)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None