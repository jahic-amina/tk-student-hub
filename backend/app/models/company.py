from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime, timezone

class CompanyStatus(str, Enum):
	approved = "approved"
	denied = "denied"
	pending = "pending"

class Company(SQLModel, table=True):
	__tablename__ = "companies"

	id: Optional[int] = Field(default=None, primary_key=True)
	company_name: str = Field(index=True)
	description: str
	website_url: str
	logo_url: str
	email: str = Field(index=True)
	phone_number: str = Field(index=True)
	jib: str = Field(index=True)
	hashed_password: str  
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
