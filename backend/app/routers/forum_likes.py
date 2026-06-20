from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.forum import ForumTopic, TopicLike, TopicDislike
from app.models.forum_notification import ForumNotificationType
from app.services.forum_notification_service import (
    create_forum_notification,
    hide_forum_notification,
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

def get_topic_dislikes_count(
    db: Session,
    topic_id: int,
) -> int:
    dislikes_count = db.exec(
        select(func.count(TopicDislike.id)).where(
            TopicDislike.topic_id == topic_id
        )
    ).one()

    return int(dislikes_count or 0)


def is_topic_disliked_by_user(
    db: Session,
    topic_id: int,
    user_id: int,
) -> bool:
    dislike = db.exec(
        select(TopicDislike).where(
            TopicDislike.topic_id == topic_id,
            TopicDislike.user_id == user_id,
        )
    ).first()

    return dislike is not None


def get_topic_reaction_response(
    db: Session,
    topic_id: int,
    user_id: int,
):
    is_liked = is_topic_liked_by_user(db, topic_id, user_id)
    is_disliked = is_topic_disliked_by_user(db, topic_id, user_id)

    return {
        "topic_id": topic_id,

        # novo za trenutni frontend
        "is_liked": is_liked,
        "is_disliked": is_disliked,

        # staro/kompatibilno ako negdje još koristiš liked
        "liked": is_liked,
        "disliked": is_disliked,

        "likes_count": get_topic_likes_count(db, topic_id),
        "dislikes_count": get_topic_dislikes_count(db, topic_id),
    }


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

    if topic.user_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Ne možete lajkovati sopstvenu temu.",
        )

    existing_like = db.exec(
        select(TopicLike).where(
            TopicLike.topic_id == topic_id,
            TopicLike.user_id == current_user.id,
        )
    ).first()

    existing_dislike = db.exec(
        select(TopicDislike).where(
            TopicDislike.topic_id == topic_id,
            TopicDislike.user_id == current_user.id,
        )
    ).first()

    if existing_like:
        db.delete(existing_like)

        hide_forum_notification(
            db=db,
            recipient_user_id=topic.user_id,
            actor_user_id=current_user.id,
            topic_id=topic.id,
            comment_id=None,
            notification_type=ForumNotificationType.TOPIC_LIKE,
            only_unread=False,
        )

        db.commit()

        response = get_topic_reaction_response(db, topic_id, current_user.id)
        response["message"] = "Like je uklonjen."
        return response

    if existing_dislike:
        db.delete(existing_dislike)

        hide_forum_notification(
            db=db,
            recipient_user_id=topic.user_id,
            actor_user_id=current_user.id,
            topic_id=topic.id,
            comment_id=None,
            notification_type=ForumNotificationType.TOPIC_DISLIKE,
            only_unread=False,
        )

    new_like = TopicLike(
        topic_id=topic_id,
        user_id=current_user.id,
    )

    db.add(new_like)

    create_forum_notification(
        db=db,
        recipient_user_id=topic.user_id,
        actor_user_id=current_user.id,
        topic_id=topic.id,
        comment_id=None,
        notification_type=ForumNotificationType.TOPIC_LIKE,
        text=(
            current_user.full_name
            + ' je lajkao/la vašu temu "'
            + topic.title
            + '".'
        ),
        prevent_duplicate=True,
    )

    db.commit()

    response = get_topic_reaction_response(db, topic_id, current_user.id)
    response["message"] = "Tema je lajkovana."
    return response

@router.post("/{topic_id}/dislike")
def toggle_topic_dislike(
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

    if topic.user_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Ne možete dislajkovati sopstvenu temu.",
        )

    existing_like = db.exec(
        select(TopicLike).where(
            TopicLike.topic_id == topic_id,
            TopicLike.user_id == current_user.id,
        )
    ).first()

    existing_dislike = db.exec(
        select(TopicDislike).where(
            TopicDislike.topic_id == topic_id,
            TopicDislike.user_id == current_user.id,
        )
    ).first()

    if existing_like:
        db.delete(existing_like)

        hide_forum_notification(
            db=db,
            recipient_user_id=topic.user_id,
            actor_user_id=current_user.id,
            topic_id=topic.id,
            comment_id=None,
            notification_type=ForumNotificationType.TOPIC_LIKE,
            only_unread=False,
        )

    if existing_dislike:
        db.delete(existing_dislike)

        hide_forum_notification(
            db=db,
            recipient_user_id=topic.user_id,
            actor_user_id=current_user.id,
            topic_id=topic.id,
            comment_id=None,
            notification_type=ForumNotificationType.TOPIC_DISLIKE,
            only_unread=False,
        )

        db.commit()

        response = get_topic_reaction_response(db, topic_id, current_user.id)
        response["message"] = "Dislike je uklonjen."
        return response

    new_dislike = TopicDislike(
        topic_id=topic_id,
        user_id=current_user.id,
    )

    db.add(new_dislike)

    create_forum_notification(
        db=db,
        recipient_user_id=topic.user_id,
        actor_user_id=current_user.id,
        topic_id=topic.id,
        comment_id=None,
        notification_type=ForumNotificationType.TOPIC_DISLIKE,
        text=(
            current_user.full_name
            + ' je dislajkao/la vašu temu "'
            + topic.title
            + '".'
        ),
        prevent_duplicate=True,
    )

    db.commit()

    response = get_topic_reaction_response(db, topic_id, current_user.id)
    response["message"] = "Tema je dislajkovana."
    return response