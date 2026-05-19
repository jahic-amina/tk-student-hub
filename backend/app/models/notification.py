from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from enum import Enum
import sqlalchemy as sa

class NotificationType(str, Enum):
    NOVA_PRILIKA = "nova_prilika"
    PROMJENA_STATUSA = "promjena_statusa"
    ROK_ISTICE = "rok_istice"

class Notification(SQLModel, table=True):
    __tablename__ = "notifications" 

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    tekst: str
    tip: NotificationType
    procitano: bool = Field(default=False)
    
    kreirano: datetime = Field(
        sa_column_kwargs={"server_default": sa.text("CURRENT_TIMESTAMP")}
    )

class NotificationCreate(SQLModel):
    user_id: int
    tekst: str
    tip: NotificationType
    procitano: bool = False

class NotificationUpdate(SQLModel):
    tekst: Optional[str] = None
    tip: Optional[NotificationType] = None
    procitano: Optional[bool] = None