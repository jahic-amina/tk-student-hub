"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func
from typing import Optional, List, Dict, Any

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.forum import (
    ForumCategory,
    ForumTopic,
    ForumTopicCreate,
    ForumComment,
    ForumCommentCreate,
    ForumTag,
    ForumTopicTag,
    ForumCommentVote,
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
        comment_items.append({
            "id": comment.id,
            "content": comment.content,
            "is_best_answer": comment.is_best_answer,
            "created_at": comment.created_at,
            "updated_at": comment.updated_at,
            "votes_count": votes_count,
            "author": get_author_data(db, comment.user_id),
        })

    # Sortiranje: Najbolji odgovor na vrh, pa po glasovima, pa po datumu kreiranja
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
        "content": topic.content,
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


# ==========================================
#               API RUTE
# ==========================================

@router.get("/")
def forum_root():
    return {"message": "Forum router radi"}


@router.get("/categories", response_model=List[Dict[str, Any]])
def get_categories_with_topic_count(db: Session = Depends(get_db)):
    statement = (
        select(
            ForumCategory.id,
            ForumCategory.name,
            ForumCategory.color,
            ForumCategory.description,
            func.count(ForumTopic.id).label("topic_count")
        )
        .join(ForumTopic, ForumTopic.category_id == ForumCategory.id, isouter=True)
        .where((ForumTopic.is_deleted == False) | (ForumTopic.id == None))
        .group_by(ForumCategory.id)
    )
    
    results = db.exec(statement).all()
    
    output = []
    for row in results:
        output.append({
            "id": row.id,
            "name": row.name,
            "color": row.color,
            "description": row.description,
            "topic_count": row.topic_count
        })
        
    return output


@router.get("/topics", response_model=Dict[str, Any])
def get_all_topics(
    db: Session = Depends(get_db),
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    page: int = 1,
    per_page: int = 5
):
    # Osnovni upit za teme
    statement = select(ForumTopic).where(ForumTopic.is_deleted == False)
    count_statement = select(func.count(ForumTopic.id)).where(ForumTopic.is_deleted == False)

    # Filtriranje po kategoriji
    if category_id is not None:
        statement = statement.where(ForumTopic.category_id == category_id)
        count_statement = count_statement.where(ForumTopic.category_id == category_id)
        
    # Filtriranje kroz pretragu (bilo u naslovu ili sadržaju)
    if search and search.strip():
        search_value = f"%{search.strip()}%"
        statement = statement.where(
            (ForumTopic.title.ilike(search_value)) | (ForumTopic.content.ilike(search_value))
        )
        count_statement = count_statement.where(
            (ForumTopic.title.ilike(search_value)) | (ForumTopic.content.ilike(search_value))
        )

    # Ukupan broj za izračunatu paginaciju na frontendu
    total_topics = db.exec(count_statement).one()

    # Paginacija i sortiranje od najnovijih
    skip = (page - 1) * per_page
    statement = statement.order_by(ForumTopic.created_at.desc()).offset(skip).limit(per_page)
    topics = db.exec(statement).all()
    
    topics_list = [build_topic_list_item(db, topic) for topic in topics]
        
    return {
        "items": topics_list,
        "total": total_topics,
        "page": page,
        "per_page": per_page
    }


@router.post("/topics", status_code=status.HTTP_201_CREATED)
def create_forum_topic(
    topic_data: ForumTopicCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = db.get(ForumCategory, topic_data.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Kategorija nije pronađena.")

    new_topic = ForumTopic(
        title=topic_data.title,
        content=topic_data.content,
        category_id=topic_data.category_id,
        user_id=current_user.id
    )
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)

    # Procesiranje i mapiranje tagova (ako su proslijeđeni stringovi ili id-jevi)
    if topic_data.tags:
        for tag_input in topic_data.tags:
            # Ako frontend šalje stringove (nazive tagova), provjeravamo ili ih kreiramo
            if isinstance(tag_input, str):
                tag = db.exec(select(ForumTag).where(ForumTag.name == tag_input.strip())).first()
                if not tag:
                    tag = ForumTag(name=tag_input.strip())
                    db.add(tag)
                    db.commit()
                    db.refresh(tag)
                tag_id = tag.id
            else:
                tag_id = tag_input

            # Vežemo tag za temu
            topic_tag = ForumTopicTag(topic_id=new_topic.id, tag_id=tag_id)
            db.add(topic_tag)

        db.commit()
        db.refresh(new_topic)

    return build_topic_list_item(db, new_topic)


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
        "is_locked": getattr(topic, "is_locked", False),
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


@router.delete("/topics/{id}", status_code=status.HTTP_200_OK)
def delete_topic(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Samo administrator može obrisati temu."
        )

    topic = db.get(ForumTopic, id)
    if not topic or topic.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tema nije pronađena."
        )

    topic.is_deleted = True
    db.add(topic)
    db.commit()

    return {
        "message": "Tema je uspešno obrisana.",
        "topic_id": id
    }


@router.post("/comments", status_code=status.HTTP_201_CREATED)
def create_forum_comment(
    comment_data: ForumCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    topic = db.get(ForumTopic, comment_data.topic_id)
    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")

    new_comment = ForumComment(
        content=comment_data.content,
        topic_id=comment_data.topic_id,
        user_id=current_user.id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return {
        "id": new_comment.id,
        "content": new_comment.content,
        "topic_id": new_comment.topic_id,
        "created_at": new_comment.created_at,
        "author": get_author_data(db, new_comment.user_id)
    }


@router.get("/topics/{topic_id}/comments")
def get_comments(topic_id: int, db: Session = Depends(get_db)):
    topic = db.get(ForumTopic, topic_id)
    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")
        
    return get_topic_comments(db, topic_id)
"""