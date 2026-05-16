from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime

class AvatarUploadResponse(SQLModel):
    profilna_slika_url: str

class AvatarDeleteResponse(SQLModel):
    message: str
