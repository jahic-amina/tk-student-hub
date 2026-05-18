from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from typing import Optional
from sqlalchemy import func
from app.models.forum import (
    ForumCategory,
    ForumTopic,
    ForumComment,
    ForumCommentVote,
    ForumTag,
    ForumTopicTag,
)

router = APIRouter(prefix="/forum", tags=["forum"])

# -------------------------------------------------------
# Team 3 — Forum
# This is your router. All your endpoints go here.
#
# Example protected endpoint:
#
# @router.get("/")
# def get_posts(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return {"message": "your code here"}
#
# -------------------------------------------------------

def make_text_summary(text: str, max_length: int = 150) -> str:
    
    clean_text = " ".join((text or "").split())

    if len(clean_text) <= max_length:
        return clean_text

    return clean_text[:max_length].rsplit(" ", 1)[0] + "..."

def user_to_dict(user: Optional[User]) -> dict:
     if not user:
        return {
            "id": None,
            "full_name": "Nepoznat korisnik",
            "role": None,
        }

    return {
        "id": user.id,
        "full_name": user.full_name,
        "role": user.role,
    }

def category_to_dict(category: Optional[ForumCategory], topics_count: int = 0) -> dict:
    if not category:
        return {
            "id": None,
            "name": "Bez kategorije",
            "color": "#6b7280",
            "description": None,
            "topics_count": topics_count,
        }

    return {
        "id": category.id,
        "name": category.name,
        "color": category.color,
        "description": category.description,
        "topics_count": topics_count,
    }

def get_topic_tags(db: Session, topic_id: int) -> list[str]:
    statement = (
        select(ForumTag.name)
        .join(ForumTopicTag, ForumTopicTag.tag_id == ForumTag.id)
        .where(ForumTopicTag.topic_id == topic_id)
        .order_by(ForumTag.name)
    )

    return list(db.exec(statement).all())


@router.get("/")
def forum_placeholder():
    return {"message": "Forum router is working — Team 3 builds here"}

@router.get("/")
def forum_root():
    return {"message": "Forum router radi"}

#Sazetak tema za listu tema na glavnoj stranici foruma
@router.get("/topics/summary")
def get_topic_summaries(
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    statement = (
        select(
            ForumTopic,
            ForumCategory,
            User,
            func.count(ForumComment.id).label("comments_count"),
        )
        .join(ForumCategory, ForumCategory.id == ForumTopic.category_id)
        .join(User, User.id == ForumTopic.user_id)
        .join(
            ForumComment,
            (ForumComment.topic_id == ForumTopic.id)
            & (ForumComment.is_deleted == False),
            isouter=True,
        )
        .where(ForumTopic.is_deleted == False)
        .group_by(ForumTopic.id, ForumCategory.id, User.id)
        .order_by(ForumTopic.created_at.desc())
    )

    if category_id:
        statement = statement.where(ForumTopic.category_id == category_id)

    if search:
        search_pattern = f"%{search.strip()}%"
        statement = statement.where(
            (ForumTopic.title.ilike(search_pattern))
            | (ForumTopic.content.ilike(search_pattern))
        )

    rows = db.exec(statement).all()

    return [
        {
            "id": topic.id,
            "title": topic.title,
            "summary": make_text_summary(topic.content),
            "views_count": topic.views_count,
            "comments_count": comments_count,
            "created_at": topic.created_at,
            "updated_at": topic.updated_at,
            "category": category_to_dict(category),
            "author": user_to_dict(author),
            "tags": get_topic_tags(db, topic.id),
        }
        for topic, category, author, comments_count in rows
    ]

#kompatibilna ruta sa postojecim frontend servisom
@router.get("/topics")
def get_topics(
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return get_topic_summaries(
        category_id=category_id,
        search=search,
        db=db,
    )

#sazetak jedne teme
@router.get("/topics/{topic_id}/summary")
def get_single_topic_summary(topic_id: int, db: Session = Depends(get_db)):
    topic = db.get(ForumTopic, topic_id)

    if not topic or topic.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tema nije pronađena.",
        )

    category = db.get(ForumCategory, topic.category_id)
    author = db.get(User, topic.user_id)

    comments_count = db.exec(
        select(func.count(ForumComment.id)).where(
            ForumComment.topic_id == topic.id,
            ForumComment.is_deleted == False,
        )
    ).one()

    return {
        "id": topic.id,
        "title": topic.title,
        "summary": make_text_summary(topic.content),
        "views_count": topic.views_count,
        "comments_count": comments_count,
        "created_at": topic.created_at,
        "updated_at": topic.updated_at,
        "category": category_to_dict(category),
        "author": user_to_dict(author),
        "tags": get_topic_tags(db, topic.id),
    }

#detalji teme + odgovori
@router.get("/topics/{topic_id}")
def get_topic_details(topic_id: int, db: Session = Depends(get_db)):
    topic = db.get(ForumTopic, topic_id)

    if not topic or topic.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tema nije pronađena.",
        )

    category = db.get(ForumCategory, topic.category_id)
    author = db.get(User, topic.user_id)

    comments_statement = (
        select(
            ForumComment,
            User,
            func.coalesce(func.sum(ForumCommentVote.value), 0).label("votes_count"),
        )
        .join(User, User.id == ForumComment.user_id)
        .join(
            ForumCommentVote,
            ForumCommentVote.comment_id == ForumComment.id,
            isouter=True,
        )
        .where(
            ForumComment.topic_id == topic.id,
            ForumComment.is_deleted == False,
        )
        .group_by(ForumComment.id, User.id)
        .order_by(ForumComment.is_best_answer.desc(), ForumComment.created_at.asc())
    )

    comments_rows = db.exec(comments_statement).all()

    comments = [
        {
            "id": comment.id,
            "content": comment.content,
            "is_best_answer": comment.is_best_answer,
            "created_at": comment.created_at,
            "updated_at": comment.updated_at,
            "votes_count": votes_count,
            "author": user_to_dict(comment_author),
        }
        for comment, comment_author, votes_count in comments_rows
    ]

    return {
        "id": topic.id,
        "title": topic.title,
        "content": topic.content,
        "views_count": topic.views_count,
        "is_locked": topic.is_locked,
        "created_at": topic.created_at,
        "updated_at": topic.updated_at,
        "category": category_to_dict(category),
        "author": user_to_dict(author),
        "tags": get_topic_tags(db, topic.id),
        "comments_count": len(comments),
        "comments": comments,
    }

#povecanje broja pregleda teme
@router.patch("/topics/{topic_id}/view")
def increment_topic_view(topic_id: int, db: Session = Depends(get_db)):
    topic = db.get(ForumTopic, topic_id)

    if not topic or topic.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tema nije pronađena.",
        )

    topic.views_count += 1
    db.add(topic)
    db.commit()
    db.refresh(topic)

    return {
        "id": topic.id,
        "views_count": topic.views_count,
    }