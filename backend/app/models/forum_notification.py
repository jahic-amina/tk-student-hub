from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class ForumNotificationType(str, Enum):
    TOPIC_LIKE = "topic_like"
    TOPIC_DISLIKE = "topic_dislike"
    TOPIC_REPLY = "topic_reply"
    COMMENT_REPLY = "comment_reply"
    MENTION = "mention"
    BEST_ANSWER = "best_answer"
    COMMENT_LIKE = "comment_like"
    COMMENT_DISLIKE = "comment_dislike"


class ForumNotification(SQLModel, table=True):
    __tablename__ = "forum_notifications"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Korisnik koji prima notifikaciju
    recipient_user_id: int = Field(
        foreign_key="users.id",
        index=True,
    )

    # Korisnik koji je izazvao notifikaciju
    actor_user_id: int = Field(
        foreign_key="users.id",
        index=True,
    )

    topic_id: int = Field(
        foreign_key="forum_topics.id",
        index=True,
    )

    # Komentar na koji treba odvesti korisnika kada klikne notifikaciju
    comment_id: Optional[int] = Field(
        default=None,
        foreign_key="forum_comments.id",
        index=True,
    )

    text: str
    type: ForumNotificationType

    is_read: bool = Field(default=False)

    # Koristi se kada se npr. ukloni best answer,
    # pa staru nepročitanu notifikaciju treba sakriti.
    is_hidden: bool = Field(default=False)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )