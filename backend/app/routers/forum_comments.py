from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.forum import ForumTopic, ForumComment, ForumCommentVote

router = APIRouter(prefix="/forum/comments", tags=["Forum Comments"])

# Sheme

class ForumCommentCreate(BaseModel):
    content: str = Field(min_length=2)
    topic_id: int

# Pomocne funkcije za komentare
def get_comment_votes_count(db: Session, comment_id: int) -> int:
    result = db.exec(select(func.coalesce(func.sum(ForumCommentVote.value), 0)).where(ForumCommentVote.comment_id == comment_id)).one()
    return int(result or 0)

def get_comments_count(db: Session, topic_id: int) -> int:
    result = db.exec(select(func.count(ForumComment.id)).where(ForumComment.topic_id == topic_id, ForumComment.is_deleted == False)).one()
    return int(result or 0)

def has_best_answer(db: Session, topic_id: int) -> bool:
    best_answer = db.exec(select(ForumComment).where(ForumComment.topic_id == topic_id, ForumComment.is_deleted == False, ForumComment.is_best_answer == True)).first()
    return best_answer is not None

def get_topic_votes_count(db: Session, topic_id: int) -> int:
    comments = db.exec(select(ForumComment).where(ForumComment.topic_id == topic_id, ForumComment.is_deleted == False)).all()
    total = 0
    for comment in comments:
        total += get_comment_votes_count(db, comment.id)
    return total

def get_topic_comments(db: Session, topic_id: int) -> list[dict]:
    
    from app.routers.forum_topics import get_author_data
    
    comments = db.exec(select(ForumComment).where(ForumComment.topic_id == topic_id, ForumComment.is_deleted == False)).all()
    comment_items = []
    for comment in comments:
        votes_count = get_comment_votes_count(db, comment.id)
        comment_items.append({
            "id": comment.id, "content": comment.content, "is_best_answer": comment.is_best_answer,
            "created_at": comment.created_at, "updated_at": comment.updated_at, "votes_count": votes_count,
            "author": get_author_data(db, comment.user_id),
        })
    comment_items.sort(key=lambda item: (not item["is_best_answer"], -item["votes_count"], item["created_at"]))
    return comment_items

# Rute za komentare

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_forum_comment(
    comment_data: ForumCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.routers.forum_topics import get_author_data
    topic = db.get(ForumTopic, comment_data.topic_id)
    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")

    new_comment = ForumComment(content=comment_data.content, topic_id=comment_data.topic_id, user_id=current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return {"id": new_comment.id, "content": new_comment.content, "topic_id": new_comment.topic_id, "created_at": new_comment.created_at, "author": get_author_data(db, new_comment.user_id)}

@router.get("/topic/{topic_id}")
def get_comments(topic_id: int, db: Session = Depends(get_db)):
    topic = db.get(ForumTopic, topic_id)
    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")
    return get_topic_comments(db, topic_id)