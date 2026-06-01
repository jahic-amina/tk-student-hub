from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.forum import ForumCategory, ForumTopic, ForumTag, ForumTopicTag, TopicReport
from app.routers.forum_categories import get_category_data 

router = APIRouter(prefix="/forum/topics", tags=["Forum Topics"])

# Sheme

class ForumTopicCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    content: str = Field(min_length=10)
    category_id: int
    tags: Optional[List[Any]] = None

class ReportCreate(BaseModel):
    reason: str

# Pomocne funkcije

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

def get_topic_tags(db: Session, topic_id: int) -> list[str]:
    links = db.exec(select(ForumTopicTag).where(ForumTopicTag.topic_id == topic_id)).all()
    tag_names = []
    for link in links:
        tag = db.get(ForumTag, link.tag_id)
        if tag:
            tag_names.append(tag.name)
    return tag_names

# Ove funkcije ce implementirati ko radi komentare
from app.routers.forum_comments import get_comments_count, has_best_answer, get_topic_comments, get_topic_votes_count

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

# Rute za teme

@router.get("/", response_model=Dict[str, Any])
def get_all_topics(
    db: Session = Depends(get_db),
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    page: int = 1,
    per_page: int = 5
):
    statement = select(ForumTopic).where(ForumTopic.is_deleted == False)
    count_statement = select(func.count(ForumTopic.id)).where(ForumTopic.is_deleted == False)

    if category_id is not None:
        statement = statement.where(ForumTopic.category_id == category_id)
        count_statement = count_statement.where(ForumTopic.category_id == category_id)
        
    if search and search.strip():
        search_value = f"%{search.strip()}%"
        statement = statement.where((ForumTopic.title.ilike(search_value)) | (ForumTopic.content.ilike(search_value)))
        count_statement = count_statement.where((ForumTopic.title.ilike(search_value)) | (ForumTopic.content.ilike(search_value)))

    total_topics = db.exec(count_statement).one()
    skip = (page - 1) * per_page
    statement = statement.order_by(ForumTopic.created_at.desc()).offset(skip).limit(per_page)
    topics = db.exec(statement).all()
    
    topics_list = [build_topic_list_item(db, topic) for topic in topics]
    return {"items": topics_list, "total": total_topics, "page": page, "per_page": per_page}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_forum_topic(
    topic_data: ForumTopicCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = db.get(ForumCategory, topic_data.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Kategorija nije pronađena.")

    new_topic = ForumTopic(title=topic_data.title, content=topic_data.content, category_id=topic_data.category_id, user_id=current_user.id)
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)

    if topic_data.tags:
        for tag_input in topic_data.tags:
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

            topic_tag = ForumTopicTag(topic_id=new_topic.id, tag_id=tag_id)
            db.add(topic_tag)
        db.commit()
        db.refresh(new_topic)

    return build_topic_list_item(db, new_topic)


@router.get("/{topic_id}")
def get_topic_details(topic_id: int, db: Session = Depends(get_db)):
    topic = db.get(ForumTopic, topic_id)
    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")

    comments = get_topic_comments(db, topic.id)
    comments_count = len(comments)
    votes_count = get_topic_votes_count(db, topic.id)

    return {
        "id": topic.id, "title": topic.title, "content": topic.content, "views_count": topic.views_count,
        "is_locked": getattr(topic, "is_locked", False), "created_at": topic.created_at, "updated_at": topic.updated_at,
        "author": get_author_data(db, topic.user_id), "category": get_category_data(db, topic.category_id),
        "tags": get_topic_tags(db, topic.id), "comments": comments,
        "stats": {"comments_count": comments_count, "answers_count": comments_count, "views_count": topic.views_count, "votes_count": votes_count, "has_best_answer": any(comment["is_best_answer"] for comment in comments)}
    }


@router.patch("/{topic_id}/view")
def increment_topic_view(topic_id: int, db: Session = Depends(get_db)):
    topic = db.get(ForumTopic, topic_id)
    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")
    topic.views_count += 1
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return {"id": topic.id, "views_count": topic.views_count}


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_topic(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    topic = db.get(ForumTopic, id)
    if not topic or topic.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tema nije pronađena.")
    
    if current_user.role != UserRole.admin and topic.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Možete obrisati samo vlastitu temu.")
    
    topic.is_deleted = True
    db.add(topic)
    db.commit()
    return {"message": "Tema je uspješno obrisana.", "topic_id": id}


@router.post("/{topic_id}/report")
def report_topic(topic_id: int, report_data: ReportCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    report = TopicReport(topic_id=topic_id, user_id=current_user.id, reason=report_data.reason)
    db.add(report)
    db.commit()
    return {"success": True}