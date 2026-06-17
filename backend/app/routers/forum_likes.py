from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.forum import ForumTopic, TopicLike
from app.models.forum_notification import ForumNotificationType
from app.services.forum_notification_service import (
    create_forum_notification,
)


router = APIRouter(
    prefix="/forum/topics",
    tags=["Forum Topic Likes"],
)


def get_topic_likes_count(
    db: Session,
    topic_id: int,
) -> int:
    likes_count = db.exec(
        select(func.count(TopicLike.id)).where(
            TopicLike.topic_id == topic_id
        )
    ).one()

    return int(likes_count or 0)


def is_topic_liked_by_user(
    db: Session,
    topic_id: int,
    user_id: int,
) -> bool:
    like = db.exec(
        select(TopicLike).where(
            TopicLike.topic_id == topic_id,
            TopicLike.user_id == user_id,
        )
    ).first()

    return like is not None


@router.post("/{topic_id}/like")
def toggle_topic_like(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    topic = db.get(ForumTopic, topic_id)

    if not topic or topic.is_deleted:
        raise HTTPException(
            status_code=404,
            detail="Tema nije pronađena.",
        )

    existing_like = db.exec(
        select(TopicLike).where(
            TopicLike.topic_id == topic_id,
            TopicLike.user_id == current_user.id,
        )
    ).first()

    # Ako korisnik već lajkuje temu, uklanjamo lajk.
    if existing_like:
        db.delete(existing_like)
        db.commit()

        return {
            "liked": False,
            "likes_count": get_topic_likes_count(
                db,
                topic_id,
            ),
            "message": "Like je uklonjen.",
        }

    # Ako lajk ne postoji, kreiramo novi lajk.
    new_like = TopicLike(
        topic_id=topic_id,
        user_id=current_user.id,
    )

    db.add(new_like)

    # Kreiramo obavještenje autoru teme.
    # Servis neće napraviti obavještenje ako korisnik
    # lajkuje vlastitu temu.
    create_forum_notification(
        db=db,
        recipient_user_id=topic.user_id,
        actor_user_id=current_user.id,
        topic_id=topic.id,
        notification_type=ForumNotificationType.TOPIC_LIKE,
        text=(
            current_user.full_name
            + ' je lajkao/la vašu temu "'
            + topic.title
            + '".'
        ),
    )

    # Lajk i obavještenje se spremaju zajedno.
    db.commit()

    return {
        "liked": True,
        "likes_count": get_topic_likes_count(
            db,
            topic_id,
        ),
        "message": "Tema je lajkovana.",
    }