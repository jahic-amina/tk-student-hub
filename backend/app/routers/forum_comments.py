from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.models.notification import Notification, NotificationType
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.forum import ForumTopic, ForumComment, ForumCommentVote
from app.routers.forum_helpers import (
    get_author_data,
    get_comment_votes_count,
    get_comment_likes_count,
    get_comment_dislikes_count,
    get_comments_count,
    has_best_answer,
    get_topic_votes_count,
    get_topic_comments,
)
from app.services.activity_log_service import log_activity
from app.enums.activity import ActivityType

router = APIRouter(prefix="/forum/comments", tags=["Forum Comments"])


# Re-export helpers so existing imports from this module keep working
__all__ = [
    "get_comments_count",
    "has_best_answer",
    "get_topic_comments",
    "get_topic_votes_count",
]


class ForumCommentCreate(BaseModel):
    content: str = Field(min_length=2)
    topic_id: int
    is_admin_notice: Optional[bool] = False


class VoteInput(BaseModel):
    value: int = Field(..., description="1 za like, -1 za dislike")


class ForumCommentUpdate(BaseModel):
    content: str = Field(min_length=2)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_forum_comment(
    comment_data: ForumCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    topic = db.get(ForumTopic, comment_data.topic_id)
    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")

    is_admin_notice = bool(comment_data.is_admin_notice)
    if is_admin_notice and str(getattr(current_user, "role", "member")) != "admin":
        is_admin_notice = False

    new_comment = ForumComment(
        content=comment_data.content,
        topic_id=comment_data.topic_id,
        user_id=current_user.id,
        is_admin_notice=is_admin_notice,
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    comments_count = get_comments_count(db, topic.id)
    log_activity(
        db,
        current_user.id,
        ActivityType.forum_comment,
        f"Diskusija · {comments_count} odgovora",
        topic.id
    )
    return {
        "id": new_comment.id,
        "content": new_comment.content,
        "topic_id": new_comment.topic_id,
        "created_at": new_comment.created_at,
        "author": get_author_data(db, new_comment.user_id),
    }


@router.get("/topic/{topic_id}")
def get_comments(topic_id: int, db: Session = Depends(get_db)):
    topic = db.get(ForumTopic, topic_id)
    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")
    return get_topic_comments(db, topic_id)


@router.patch("/{comment_id}/best-answer", status_code=status.HTTP_200_OK)
def toggle_best_answer(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = db.get(ForumComment, comment_id)
    if not comment or comment.is_deleted:
        raise HTTPException(status_code=404, detail="Komentar nije pronađen.")

    topic = db.get(ForumTopic, comment.topic_id)
    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")

    if topic.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Samo autor teme može označiti najbolji odgovor.")

    if comment.is_best_answer:
        comment.is_best_answer = False
    else:
        existing_best = db.exec(
            select(ForumComment).where(
                ForumComment.topic_id == comment.topic_id,
                ForumComment.is_best_answer == True,
                ForumComment.is_deleted == False,
            )
        ).first()
        if existing_best:
            existing_best.is_best_answer = False
            db.add(existing_best)
        comment.is_best_answer = True

    db.add(comment)
    db.commit()
    db.refresh(comment)
    db.expire_all()

    if comment.is_best_answer:
        log_activity(
            db,
            comment.user_id,
            ActivityType.forum_answer,
            topic.title,
            "Označeno kao korisno",
            topic.id
        )

    return {"id": comment.id, "is_best_answer": comment.is_best_answer}


@router.post("/{comment_id}/vote", status_code=status.HTTP_200_OK)
def vote_on_comment(
    comment_id: int,
    vote_data: VoteInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if vote_data.value not in (1, -1):
        raise HTTPException(status_code=400, detail="Vrijednost glasa mora biti 1 ili -1.")

    comment = db.get(ForumComment, comment_id)
    if not comment or comment.is_deleted:
        raise HTTPException(status_code=404, detail="Komentar nije pronađen.")

    existing_vote = db.exec(
        select(ForumCommentVote).where(
            ForumCommentVote.comment_id == comment_id,
            ForumCommentVote.user_id == current_user.id,
        )
    ).first()

    novi_like = False
    
    if existing_vote:
        if existing_vote.value == vote_data.value:
            db.delete(existing_vote)
            db.commit()
            user_vote = 0
        else:
            existing_vote.value = vote_data.value
            db.add(existing_vote)
            db.commit()
            user_vote = vote_data.value
            if vote_data.value == 1:
                novi_like = True
    else:
        new_vote = ForumCommentVote(
            comment_id=comment_id,
            user_id=current_user.id,
            value=vote_data.value,
        )
        db.add(new_vote)
        db.commit()
        user_vote = vote_data.value
        if vote_data.value == 1:
            novi_like = True

    if novi_like and comment.user_id != current_user.id:
        db.add(Notification(
            user_id=comment.user_id,
            text="Vaš komentar na forumu je lajkovan.",
            type=NotificationType.COMMENT_LIKED
        ))
        db.commit()

    total_votes = get_comment_votes_count(db, comment_id)
    return {"comment_id": comment_id, "votes_count": total_votes, "user_vote": user_vote}


@router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = db.get(ForumComment, comment_id)
    if not comment or comment.is_deleted:
        raise HTTPException(status_code=404, detail="Komentar nije pronađen.")
    
    if comment.user_id != current_user.id and getattr(current_user, 'role', 'member') != 'admin':
        raise HTTPException(status_code=403, detail="Možete obrisati samo vlastiti komentar.")
    
    replies = db.exec(
        select(ForumComment).where(
            ForumComment.parent_id == comment_id,
            ForumComment.is_deleted == False
        )
    ).all()

    if replies:
        comment.is_deleted = True
        db.add(comment)
        db.commit()
    else:
        db.delete(comment)
        db.commit()
    
    return {"message": "Komentar je uspješno obrisan.", "comment_id": comment_id}


@router.put("/{comment_id}", status_code=status.HTTP_200_OK)
def update_comment(
    comment_id: int,
    comment_data: ForumCommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = db.get(ForumComment, comment_id)
    if not comment or comment.is_deleted:
        raise HTTPException(status_code=404, detail="Komentar nije pronađen.")
    
    if comment.user_id != current_user.id and getattr(current_user, 'role', 'member') != 'admin':
        raise HTTPException(status_code=403, detail="Možete editovati samo vlastiti komentar.")
    
    comment.content = comment_data.content
    comment.updated_at = datetime.utcnow()
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    return {"id": comment.id, "content": comment.content, "updated_at": comment.updated_at}