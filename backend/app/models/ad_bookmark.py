from sqlmodel import SQLModel, Field, UniqueConstraint
from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel


class AdBookmark(SQLModel, table=True):
    __tablename__ = "bookmarks"
    __table_args__ = (
        UniqueConstraint("user_id", "ad_id", name="unique_user_ad_bookmark"),
        {"extend_existing": True},
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    ad_id: int = Field(foreign_key="ads.id", index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AdBookmarkCreate(SQLModel):
    ad_id: int


class AdBookmarkRead(BaseModel):
    id: int
    user_id: int
    ad_id: int
    created_at: datetime

    class Config:
        from_attributes = True