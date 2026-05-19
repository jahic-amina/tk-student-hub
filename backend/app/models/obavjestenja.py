from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from enum import Enum
import sqlalchemy as sa


class NotificationType(str, Enum):
    NOVA_PRILIKA = "nova_prilika"
    PROMJENA_STATUSA = "promjena_statusa"
    ROK_ISTICE = "rok_istice"

class NotificationBase(SQLModel):
    tekst: str
    tip: NotificationType = Field(sa_type=sa.Enum(NotificationType, name="notification_type"))
    procitano: bool = Field(default=False)
    user_id: int = Field(foreign_key="users.id") #

class Notification(NotificationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    kreirano: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": sa.text("CURRENT_TIMESTAMP")}
    )

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(SQLModel):
    tekst: Optional[str] = None
    tip: Optional[NotificationType] = None
    procitano: Optional[bool] = None
    user_id: Optional[int] = None