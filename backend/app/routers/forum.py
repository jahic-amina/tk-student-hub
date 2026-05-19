from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlmodel import Session, select

from app.database import get_db
from app.models.user import User
from app.models.forum import (
    ForumCategory,
    ForumTopic,
    ForumComment,
    ForumCommentVote,
    ForumTag,
    ForumTopicTag,
)

router = APIRouter(prefix="/forum", tags=["forum"])


def make_summary(text: str, max_length: int = 150) -> str:
    clean_text = " ".join((text or "").split())

    if len(clean_text) <= max_length:
        return clean_text

    return clean_text[:max_length].rsplit(" ", 1)[0] + "..."


def get_author_data(db: Session, user_id: int) -> dict:
    user = db.get(User, user_id)

    if not user:
        return {
            "id": None,
            "full_name": "Nepoznat korisnik",
        }

    return {
        "id": user.id,
        "full_name": user.full_name,
    }


def get_category_data(db: Session, category_id: int) -> dict:
    category = db.get(ForumCategory, category_id)

    if not category:
        return {
            "id": None,
            "name": "Bez kategorije",
            "color": "#6b7280",
        }

    return {
        "id": category.id,
        "name": category.name,
        "color": category.color,
    }


def get_topic_tags(db: Session, topic_id: int) -> list[str]:
    links = db.exec(
        select(ForumTopicTag).where(ForumTopicTag.topic_id == topic_id)
    ).all()

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


def get_topic_comments(db: Session, topic_id: int) -> list[dict]:
    comments = db.exec(
        select(ForumComment).where(
            ForumComment.topic_id == topic_id,
            ForumComment.is_deleted == False,
        )
    ).all()

    comment_items = []

    for comment in comments:
        votes_count = get_comment_votes_count(db, comment.id)

        comment_items.append(
            {
                "id": comment.id,
                "content": comment.content,
                "is_best_answer": comment.is_best_answer,
                "created_at": comment.created_at,
                "updated_at": comment.updated_at,
                "votes_count": votes_count,
                "author": get_author_data(db, comment.user_id),
            }
        )

    comment_items.sort(
        key=lambda item: (
            not item["is_best_answer"],
            -item["votes_count"],
            item["created_at"],
        )
    )

    return comment_items


def get_comments_count(db: Session, topic_id: int) -> int:
    result = db.exec(
        select(func.count(ForumComment.id)).where(
            ForumComment.topic_id == topic_id,
            ForumComment.is_deleted == False,
        )
    ).one()

    return int(result or 0)


def get_topic_votes_count(db: Session, topic_id: int) -> int:
    comments = db.exec(
        select(ForumComment).where(
            ForumComment.topic_id == topic_id,
            ForumComment.is_deleted == False,
        )
    ).all()

    total = 0

    for comment in comments:
        total += get_comment_votes_count(db, comment.id)

    return total


def has_best_answer(db: Session, topic_id: int) -> bool:
    best_answer = db.exec(
        select(ForumComment).where(
            ForumComment.topic_id == topic_id,
            ForumComment.is_deleted == False,
            ForumComment.is_best_answer == True,
        )
    ).first()

    return best_answer is not None


def build_topic_list_item(db: Session, topic: ForumTopic) -> dict:
    comments_count = get_comments_count(db, topic.id)

    return {
        "id": topic.id,
        "title": topic.title,
        "summary": make_summary(topic.content),
        "views_count": topic.views_count,
        "comments_count": comments_count,
        "answers_count": comments_count,
        "created_at": topic.created_at,
        "updated_at": topic.updated_at,
        "author": get_author_data(db, topic.user_id),
        "category": get_category_data(db, topic.category_id),
        "tags": get_topic_tags(db, topic.id),
        "has_best_answer": has_best_answer(db, topic.id),
    }


@router.get("/")
def forum_root():
    return {"message": "Forum router radi"}


@router.get("/topics")
def get_topics(
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    statement = select(ForumTopic).where(ForumTopic.is_deleted == False)

    if search and search.strip():
        search_value = f"%{search.strip()}%"
        statement = statement.where(
            (ForumTopic.title.ilike(search_value))
            | (ForumTopic.content.ilike(search_value))
        )

    statement = statement.order_by(ForumTopic.created_at.desc())

    topics = db.exec(statement).all()

    return [
        build_topic_list_item(db, topic)
        for topic in topics
    ]


@router.patch("/topics/{topic_id}/view")
def increment_topic_view(topic_id: int, db: Session = Depends(get_db)):
    topic = db.get(ForumTopic, topic_id)

    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")

    topic.views_count += 1

    db.add(topic)
    db.commit()
    db.refresh(topic)

    return {
        "id": topic.id,
        "views_count": topic.views_count,
    }


@router.get("/topics/{topic_id}")
def get_topic_details(topic_id: int, db: Session = Depends(get_db)):
    topic = db.get(ForumTopic, topic_id)

    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")

    comments = get_topic_comments(db, topic.id)
    comments_count = len(comments)
    votes_count = get_topic_votes_count(db, topic.id)

    return {
        "id": topic.id,
        "title": topic.title,
        "content": topic.content,
        "views_count": topic.views_count,
        "is_locked": topic.is_locked,
        "created_at": topic.created_at,
        "updated_at": topic.updated_at,
        "author": get_author_data(db, topic.user_id),
        "category": get_category_data(db, topic.category_id),
        "tags": get_topic_tags(db, topic.id),
        "comments": comments,
        "stats": {
            "comments_count": comments_count,
            "answers_count": comments_count,
            "views_count": topic.views_count,
            "votes_count": votes_count,
            "has_best_answer": any(comment["is_best_answer"] for comment in comments),
        },
    }