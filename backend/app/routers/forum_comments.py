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
    is_admin_notice: Optional[bool] = False

class VoteInput(BaseModel):
    value: int = Field(..., description="1 za like, -1 za dislike")

    
# Pomocne funkcije za komentare
def get_comment_votes_count(db: Session, comment_id: int) -> int:
    result = db.exec(select(func.coalesce(func.sum(ForumCommentVote.value), 0)).where(ForumCommentVote.comment_id == comment_id)).one()
    return int(result or 0)

def get_comment_likes_count(db: Session, comment_id: int) -> int:
    result = db.exec(select(func.count(ForumCommentVote.id)).where(ForumCommentVote.comment_id == comment_id, ForumCommentVote.value == 1)).one()
    return int(result or 0)

def get_comment_dislikes_count(db: Session, comment_id: int) -> int:
    result = db.exec(select(func.count(ForumCommentVote.id)).where(ForumCommentVote.comment_id == comment_id, ForumCommentVote.value == -1)).one()
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
        likes_count = get_comment_likes_count(db, comment.id)
        dislikes_count = get_comment_dislikes_count(db, comment.id)
        comment_items.append({
            "id": comment.id, "content": comment.content, "is_best_answer": comment.is_best_answer,
            "created_at": comment.created_at, "updated_at": comment.updated_at, 
            "votes_count": votes_count,
            "likes_count": likes_count,
            "dislikes_count": dislikes_count,
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

    is_admin_notice = getattr(comment_data, 'is_admin_notice', False)
    if is_admin_notice and getattr(current_user, 'role', 'member') != 'admin':
        is_admin_notice = False

    new_comment = ForumComment(content=comment_data.content, topic_id=comment_data.topic_id, user_id=current_user.id, is_admin_notice=is_admin_notice)
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

@router.patch("/{comment_id}/best-answer", status_code=status.HTTP_200_OK)
def toggle_best_answer(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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
                ForumComment.is_deleted == False
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
    return {"id": comment.id, "is_best_answer": comment.is_best_answer}


@router.post("/{comment_id}/vote", status_code=status.HTTP_200_OK)
def vote_on_comment(
    comment_id: int,
    vote_data: VoteInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if vote_data.value not in (1, -1):
        raise HTTPException(status_code=400, detail="Vrijednost glasa mora biti 1 ili -1.")

    comment = db.get(ForumComment, comment_id)
    if not comment or comment.is_deleted:
        raise HTTPException(status_code=404, detail="Komentar nije pronađen.")

    existing_vote = db.exec(
        select(ForumCommentVote).where(
            ForumCommentVote.comment_id == comment_id,
            ForumCommentVote.user_id == current_user.id
        )
    ).first()

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
    else:
        new_vote = ForumCommentVote(
            comment_id=comment_id,
            user_id=current_user.id,
            value=vote_data.value
        )
        db.add(new_vote)
        db.commit()
        user_vote = vote_data.value

    total_votes = get_comment_votes_count(db, comment_id)
    return {"comment_id": comment_id, "votes_count": total_votes, "user_vote": user_vote}

@router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = db.get(ForumComment, comment_id)
    if not comment or comment.is_deleted:
        raise HTTPException(status_code=404, detail="Komentar nije pronađen.")
    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Možete obrisati samo vlastiti komentar.")
    
    comment.is_deleted = True
    db.add(comment)
    db.commit()
    return {"message": "Komentar je uspješno obrisan.", "comment_id": comment_id}