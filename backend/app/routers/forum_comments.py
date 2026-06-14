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

from app.services.forum_reputation import (
    get_user_forum_identity,
    register_answer_created,
    register_best_answer,
)

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
    parent_id: Optional[int] = None


class VoteInput(BaseModel):
    value: int = Field(..., description="1 za like, -1 za dislike")


class ForumCommentUpdate(BaseModel):
    content: str = Field(min_length=2)


# --- Pomocne funkcije i lokalne implementacije ---

def get_comment_author_data(db: Session, user_id: int) -> dict:
    user = db.get(User, user_id)

    if not user:
        return {
            "id": None,
            "full_name": "Nepoznat korisnik",
            "role": "Student",
            "level": 1,
            "title": "Novi član",
            "reputation_points": 0,
            "medals": [],
        }

    forum_identity = get_user_forum_identity(db, user)

    return {
        "id": user.id,
        "full_name": user.full_name,
        **forum_identity,
    } 

def local_get_comment_dislikes_count(db: Session, comment_id: int) -> int:
    result = db.exec(
        select(func.count(ForumCommentVote.id))
        .where(ForumCommentVote.comment_id == comment_id, ForumCommentVote.value == -1)
    ).one()
    return int(result or 0)

def local_get_comments_count(db: Session, topic_id: int) -> int:
    result = db.exec(
        select(func.count(ForumComment.id))
        .where(ForumComment.topic_id == topic_id, ForumComment.is_deleted == False)
    ).one()
    return int(result or 0)

def local_has_best_answer(db: Session, topic_id: int) -> bool:
    best_answer = db.exec(
        select(ForumComment)
        .where(ForumComment.topic_id == topic_id, ForumComment.is_deleted == False, ForumComment.is_best_answer == True)
    ).first()
    return best_answer is not None

def local_get_topic_votes_count(db: Session, topic_id: int) -> int:
    comments = db.exec(
        select(ForumComment).where(ForumComment.topic_id == topic_id, ForumComment.is_deleted == False)
    ).all()
    total = 0
    for comment in comments:
        total += get_comment_votes_count(db, comment.id)
    return total

def local_get_topic_comments(db: Session, topic_id: int) -> list[dict]:
    all_comments = db.exec(select(ForumComment).where(ForumComment.topic_id == topic_id)).all()
    
    def build_comment_dict(comment: ForumComment) -> dict:
        votes_count = get_comment_votes_count(db, comment.id)
        likes_count = get_comment_likes_count(db, comment.id)
        dislikes_count = local_get_comment_dislikes_count(db, comment.id)
        
        if comment.is_deleted:
            return {
                "id": comment.id,
                "content": "deleted by user",
                "is_deleted": True,
                "is_best_answer": False,
                "parent_id": comment.parent_id,
                "created_at": comment.created_at,
                "updated_at": comment.updated_at,
                "votes_count": 0,
                "likes_count": 0,
                "dislikes_count": 0,
                "author": None,
                "replies": [],
            }

        return {
            "id": comment.id,
            "content": comment.content,
            "is_deleted": False,
            "is_best_answer": comment.is_best_answer,
            "parent_id": comment.parent_id,
            "created_at": comment.created_at,
            "updated_at": comment.updated_at,
            "votes_count": votes_count,
            "likes_count": likes_count,
            "dislikes_count": dislikes_count,
            "author": get_comment_author_data(db, comment.user_id),
            "replies": [],
        }

    comment_dict = {
        comment.id: build_comment_dict(comment)
        for comment in all_comments
    }

    top_level = []

    for comment in all_comments:
        comment_data = comment_dict[comment.id]

        if comment.parent_id is None:
            top_level.append(comment_data)
        else:
            parent = comment_dict.get(comment.parent_id)
            if parent:
                parent["replies"].append(comment_data)

    top_level.sort(
        key=lambda item: (
            not item["is_best_answer"],
            -item["votes_count"],
            item["created_at"],
        )
    )

    return top_level


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
    current_role = getattr(current_user.role, "value", current_user.role)
    if is_admin_notice and current_role != "admin":
        is_admin_notice = False

    new_comment = ForumComment(
        content=comment_data.content, 
        topic_id=comment_data.topic_id, 
        user_id=current_user.id, 
        is_admin_notice=is_admin_notice, 
        parent_id=comment_data.parent_id
    )
    db.add(new_comment)

    # Dodjeljuje ID komentaru bez završavanja transakcije.
    db.flush()

    # Automatski dodaje bodove za napisani odgovor.
    register_answer_created(
        db,
        user_id=current_user.id,
        comment_id=new_comment.id,
    )

    # Komentar, bodovi i eventualne medalje spremaju se zajedno.
    db.commit()
    db.refresh(new_comment)

    comments_count = local_get_comments_count(db, topic.id)
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
        "author": get_comment_author_data(db, new_comment.user_id),
    }


@router.get("/topic/{topic_id}")
def get_comments(topic_id: int, db: Session = Depends(get_db)):
    topic = db.get(ForumTopic, topic_id)
    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")
    return local_get_topic_comments(db, topic_id)


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

    # Ako je već najbolji odgovor, uklanja se oznaka.
    if comment.is_best_answer:
        comment.is_best_answer = False
    else:
        # Na jednoj temi može postojati samo jedan najbolji odgovor.
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

        # Dodjeljuje bodove autoru komentara.
        register_best_answer(
            db,
            user_id=comment.user_id,
            comment_id=comment.id,
        )

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