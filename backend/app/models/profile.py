from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime

class UserProfileResponse(SQLModel):
    id: int
    email: str
    full_name: str
    role: str
    created_at: Optional[datetime]
    profilna_slika_url: Optional[str]

class AvatarUploadResponse(SQLModel):
    profilna_slika_url: str

class AvatarDeleteResponse(SQLModel):
    message: str
