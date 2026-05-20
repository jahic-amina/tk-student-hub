from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
import sqlalchemy as sa

class NotificationType(str, Enum):
    NEW_OPPORTUNITY = "new_opportunity"
    STATUS_CHANGE = "status_change"
    DEADLINE_EXPIRING = "deadline_expiring"

class Notification(SQLModel, table=True):
    __tablename__ = "notifications" 
    __table_args__ = {"extend_existing": True} # Dodajemo za svaki slučaj da izbjegnemo duplanje u memoriji

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    
    # Prevodi polja na engleski
    text: str
    type: NotificationType
    is_read: bool = Field(default=False)
    
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": sa.text("CURRENT_TIMESTAMP")}
    )

class NotificationCreate(SQLModel):
    user_id: int
    text: str
    type: NotificationType
    is_read: bool = False

class NotificationUpdate(SQLModel):
    text: Optional[str] = None
    type: Optional[NotificationType] = None
    is_read: Optional[bool] = None