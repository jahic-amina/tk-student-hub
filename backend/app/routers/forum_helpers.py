"""
Shared helper functions for forum routers.
Kept in a separate module to break the circular import between
forum_topics.py and forum_comments.py.
"""
from sqlmodel import Session, select, func

from app.models.user import User
from app.models.forum import ForumComment, ForumCommentVote, ForumTag, ForumTopicTag
from app.models.forum import ForumCategory


def get_author_data(db: Session, user_id: int) -> dict:
    user = db.get(User, user_id)
    if not user:
        return {"id": None, "full_name": "Nepoznat korisnik"}
    return {"id": user.id, "full_name": user.full_name}


def get_category_data(db: Session, category_id: int) -> dict:
    category = db.get(ForumCategory, category_id)
    if not category:
        return {"id": None, "name": "Bez kategorije", "color": "#6b7280"}
    return {"id": category.id, "name": category.name, "color": category.color}


def get_topic_tags(db: Session, topic_id: int) -> list[str]:
    links = db.exec(select(ForumTopicTag).where(ForumTopicTag.topic_id == topic_id)).all()
    tag_names = []
    for link in links:
        tag = db.get(ForumTag, link.tag_id)
        if tag:
            tag_names.append(tag.name)
    return tag_names


def get_comment_votes_count(db: Session, comment_id: int) -> int:
    result = db.exec(
        select(func.coalesce(func.sum(ForumCommentVote.value), 0)).where(
            ForumCommentVote.comment_id == comment_id
        )
    ).one()
    return int(result or 0)


def get_comment_likes_count(db: Session, comment_id: int) -> int:
    result = db.exec(
        select(func.count(ForumCommentVote.id)).where(
            ForumCommentVote.comment_id == comment_id,
            ForumCommentVote.value == 1,
        )
    ).one()
    return int(result or 0)


def get_comment_dislikes_count(db: Session, comment_id: int) -> int:
    result = db.exec(
        select(func.count(ForumCommentVote.id)).where(
            ForumCommentVote.comment_id == comment_id,
            ForumCommentVote.value == -1,
        )
    ).one()
    return int(result or 0)


def get_comments_count(db: Session, topic_id: int) -> int:
    result = db.exec(
        select(func.count(ForumComment.id)).where(
            ForumComment.topic_id == topic_id,
            ForumComment.is_deleted == False,
        )
    ).one()
    return int(result or 0)


def has_best_answer(db: Session, topic_id: int) -> bool:
    best = db.exec(
        select(ForumComment).where(
            ForumComment.topic_id == topic_id,
            ForumComment.is_deleted == False,
            ForumComment.is_best_answer == True,
        )
    ).first()
    return best is not None


def get_topic_votes_count(db: Session, topic_id: int) -> int:
    comments = db.exec(
        select(ForumComment).where(
            ForumComment.topic_id == topic_id,
            ForumComment.is_deleted == False,
        )
    ).all()
    return sum(get_comment_votes_count(db, c.id) for c in comments)


def get_topic_comments(db: Session, topic_id: int) -> list[dict]:
    comments = db.exec(
        select(ForumComment).where(
            ForumComment.topic_id == topic_id,
            ForumComment.is_deleted == False,
        )
    ).all()
    comment_items = []
    for comment in comments:
        comment_items.append({
            "id": comment.id,
            "content": comment.content,
            "is_best_answer": comment.is_best_answer,
            "created_at": comment.created_at,
            "updated_at": comment.updated_at,
            "votes_count": get_comment_votes_count(db, comment.id),
            "likes_count": get_comment_likes_count(db, comment.id),
            "dislikes_count": get_comment_dislikes_count(db, comment.id),
            "author": get_author_data(db, comment.user_id),
        })
    comment_items.sort(
        key=lambda item: (not item["is_best_answer"], -item["votes_count"], item["created_at"])
    )
    return comment_items
