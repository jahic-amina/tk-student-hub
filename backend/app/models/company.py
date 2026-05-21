from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime, timezone
import re
import secrets
from pydantic import field_validator

def _validate_company_name(v: Optional[str]) -> Optional[str]:
    if v is not None and len(v.strip()) < 2:
        raise ValueError('Company name must be at least 2 characters long.')
    return v


def _validate_description(v: Optional[str]) -> Optional[str]:
    if v is not None and len(v.strip()) < 10:
        raise ValueError('Description must be at least 10 characters long.')
    return v


def _validate_website_url(v: Optional[str]) -> Optional[str]:
    if v is not None:
        pattern = r'^https://[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+(/.*)?$'
        if not re.match(pattern, v.strip()):
            raise ValueError('Website URL must be in format https://something.something.')
    return v


def _validate_logo_url(v: Optional[str]) -> Optional[str]:
    if v is not None:
        pattern = r'^https://.+\.(png|jpg|jpeg|webp)(\?.*)?$'
        if not re.match(pattern, v.strip(), flags=re.IGNORECASE):
            raise ValueError('Logo URL must point to a .png, .jpg, .jpeg or .webp image.')
    return v


def _validate_email(v: Optional[str]) -> Optional[str]:
    if v is not None:
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if not re.match(pattern, v.strip()):
            raise ValueError('Email is not in a valid format.')
    return v


def _validate_jib(v: Optional[str]) -> Optional[str]:
    if v is not None:
        v_stripped = v.strip()
        
        if not v_stripped.isdigit():
            raise ValueError('JIB must contain only digits.')
        
        if len(v_stripped) != 13:
            raise ValueError('JIB must be exactly 13 digits long.')
    return v


def _validate_address(v: Optional[str]) -> Optional[str]:
    if v is not None and len(v.strip()) <= 2:
        raise ValueError('Address must be longer than 2 characters.')
    return v


class CompanyStatus(str, Enum):
    approved = "approved"
    denied = "denied"
    pending = "pending"


class Company(SQLModel, table=True):
    __tablename__ = "companies"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    company_name: str = Field(index=True)
    description: str
    website_url: str
    logo_url: str
    email: str = Field(index=True)
    phone_number: str = Field(index=True)
    jib: str = Field(index=True)
    hashed_password: str  
    api_key: str = Field(default_factory=lambda: secrets.token_urlsafe(32), index=True)
    status: CompanyStatus = Field(default=CompanyStatus.pending)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_deleted: bool = Field(default=False)
    address: str


class CompanyCreate(SQLModel):
    company_name: str
    description: str
    website_url: str
    logo_url: str
    email: str
    phone_number: str
    jib: str
    address: str
    password: str

    @field_validator('company_name')
    @classmethod
    def validate_company_name(cls, v):
        return _validate_company_name(v)

    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        return _validate_description(v)

    @field_validator('website_url')
    @classmethod
    def validate_website_url(cls, v):
        return _validate_website_url(v)

    @field_validator('logo_url')
    @classmethod
    def validate_logo_url(cls, v):
        return _validate_logo_url(v)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        return _validate_email(v)

    @field_validator('jib')
    @classmethod
    def validate_jib(cls, v):
        return _validate_jib(v)

    @field_validator('address')
    @classmethod
    def validate_address(cls, v):
        return _validate_address(v)


class CompanyUpdate(SQLModel):
    company_name: Optional[str] = None
    description: Optional[str] = None
    website_url: Optional[str] = None
    logo_url: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    jib: Optional[str] = None
    address: Optional[str] = None
    status: Optional[CompanyStatus] = None

    @field_validator('company_name')
    @classmethod
    def validate_company_name(cls, v):
        return _validate_company_name(v)

    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        return _validate_description(v)

    @field_validator('website_url')
    @classmethod
    def validate_website_url(cls, v):
        return _validate_website_url(v)

    @field_validator('logo_url')
    @classmethod
    def validate_logo_url(cls, v):
        return _validate_logo_url(v)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        return _validate_email(v)

    @field_validator('jib')
    @classmethod
    def validate_jib(cls, v):
        return _validate_jib(v)

    @field_validator('address')
    @classmethod
    def validate_address(cls, v):
        return _validate_address(v)


class CompanyRead(SQLModel):
    id: int
    company_name: str
    description: str
    website_url: str
    logo_url: str
    email: str
    phone_number: str
    jib: str
    status: CompanyStatus
    created_at: datetime
    address: str