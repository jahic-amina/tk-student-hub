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
    profile_picture_url: Optional[str]
    biography: Optional[str] = None

class AvatarUploadResponse(SQLModel):
    profile_picture_url: str

class AvatarDeleteResponse(SQLModel):
    message: str
