from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class ForumNotificationType(str, Enum):
    TOPIC_LIKE = "topic_like"
    TOPIC_REPLY = "topic_reply"


class ForumNotification(SQLModel, table=True):
    __tablename__ = "forum_notifications"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Korisnik koji prima notifikaciju
    recipient_user_id: int = Field(
        foreign_key="users.id",
        index=True,
    )

    # Korisnik koji je lajkovao ili odgovorio
    actor_user_id: int = Field(
        foreign_key="users.id",
        index=True,
    )

    topic_id: int = Field(
        foreign_key="forum_topics.id",
        index=True,
    )

    text: str
    type: ForumNotificationType

    is_read: bool = Field(default=False)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )