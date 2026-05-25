from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from app.enums.activity import ActivityType
import sqlalchemy as sa
from pydantic import BaseModel

if TYPE_CHECKING:
    from app.models.user import User

class ActivityLog(SQLModel, table=True):
    __tablename__ = "activity_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    activity_type: ActivityType = Field(
        sa_column=sa.Column(sa.Enum(ActivityType), nullable=False)
    )
    title: str
    subtitle: Optional[str] = None
    entity_id: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user: Optional["User"] = Relationship(back_populates="activity_logs")

class ActivityResponse(BaseModel):
    id: int
    activity_type: ActivityType
    title: str
    subtitle: Optional[str] = None
    entity_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ActivityListResponse(BaseModel):
    items: list[ActivityResponse]
    total: int
    has_more: bool