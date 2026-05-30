from sqlmodel import SQLModel, Field
from pydantic import field_validator
from typing import Optional
from datetime import datetime, timezone
from enum import Enum


class NotificationType(str, Enum):
    NEW_OPPORTUNITY = "new_opportunity"
    STATUS_CHANGE = "status_change"
    DEADLINE_EXPIRING = "deadline_expiring"


class Notification(SQLModel, table=True):
    __tablename__ = "notifications"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    text: str
    type: NotificationType
    is_read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class NotificationCreate(SQLModel):
    text: str
    type: NotificationType
    is_read: bool = False

    @field_validator("text")
    @classmethod
    def validate_text(cls, v):
        return _validate_text(v)


class NotificationUpdate(SQLModel):
    text: Optional[str] = None
    type: Optional[NotificationType] = None
    is_read: Optional[bool] = None

    @field_validator("text")
    @classmethod
    def validate_text(cls, v):
        return _validate_text(v)


# --- Validation helpers ---

def _validate_text(v: Optional[str]) -> Optional[str]:
    if v is not None:
        v = v.strip()
        if not v:
            raise ValueError("Notification text cannot be blank.")
    return v