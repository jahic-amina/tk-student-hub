from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, Field, Session, select, func
from sqlalchemy import UniqueConstraint

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.forum import ForumTopic


class TopicLike(SQLModel, table=True):
    __tablename__ = "topic_likes"

    __table_args__ = (
        UniqueConstraint("topic_id", "user_id", name="unique_topic_like_per_user"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    topic_id: int = Field(foreign_key="forum_topics.id", index=True)
    user_id: int = Field(foreign_key="users.id", index=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)


router = APIRouter(prefix="/forum/topics", tags=["Forum Topic Likes"])


def get_topic_likes_count(db: Session, topic_id: int) -> int:
    likes_count = db.exec(
        select(func.count(TopicLike.id)).where(TopicLike.topic_id == topic_id)
    ).one()

    return int(likes_count or 0)


def is_topic_liked_by_user(db: Session, topic_id: int, user_id: int) -> bool:
    like = db.exec(
        select(TopicLike).where(
            TopicLike.topic_id == topic_id,
            TopicLike.user_id == user_id
        )
    ).first()

    return like is not None


@router.post("/{topic_id}/like")
def toggle_topic_like(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    topic = db.get(ForumTopic, topic_id)

    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")

    existing_like = db.exec(
        select(TopicLike).where(
            TopicLike.topic_id == topic_id,
            TopicLike.user_id == current_user.id
        )
    ).first()

    if existing_like:
        db.delete(existing_like)
        db.commit()

        return {
            "liked": False,
            "likes_count": get_topic_likes_count(db, topic_id),
            "message": "Like je uklonjen."
        }

    new_like = TopicLike(
        topic_id=topic_id,
        user_id=current_user.id
    )

    db.add(new_like)
    db.commit()

    return {
        "liked": True,
        "likes_count": get_topic_likes_count(db, topic_id),
        "message": "Tema je lajkovana."
    }