from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.services.activity_log_service import log_activity
from app.enums.activity import ActivityType
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.forum import ForumTopic, ForumComment, ForumCommentVote, CommentAttachment
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

from app.services.forum_reputation import (
    get_user_forum_identity,
    register_answer_created,
    register_best_answer,
    register_comment_vote,
    rollback_comment_vote,
)

from app.models.forum_notification import (
    ForumNotification,
    ForumNotificationType,
)

from app.services.forum_notification_service import (
    create_forum_notification,
    hide_forum_notification,
    notify_mentions,
    get_user_display_name,
)

router = APIRouter(prefix="/forum/comments", tags=["Forum Comments"])

# Re-export helpers so existing imports from this module keep working
__all__ = [
    "get_comments_count",
    "has_best_answer",
    "get_topic_comments",
    "get_topic_votes_count",
]


# --- SHEME ---
class ForumCommentCreate(BaseModel):
    content: str = Field(min_length=2)
    topic_id: int
    is_admin_notice: Optional[bool] = False
    parent_id: Optional[int] = None

class VoteInput(BaseModel):
    value: int = Field(..., description="1 za like, -1 za dislike")

class ForumCommentUpdate(BaseModel):
    content: str = Field(min_length=2)

class AdminNoticeCreate(BaseModel):
    content: str = Field(min_length=3)


# --- POMOĆNE FUNKCIJE (Sa integracijom reputacije) ---
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
    all_comments = db.exec(select(ForumComment).where(ForumComment.topic_id == topic_id)).all()

    def build_comment_dict(comment: ForumComment) -> dict:
        votes_count = get_comment_votes_count(db, comment.id)
        likes_count = get_comment_likes_count(db, comment.id)
        dislikes_count = get_comment_dislikes_count(db, comment.id)

        if comment.is_deleted:
            return {
                "id": comment.id, "content": "deleted by user", "is_deleted": True, "is_best_answer": False,
                "is_admin_notice": comment.is_admin_notice,
                "parent_id": comment.parent_id, "created_at": comment.created_at, "updated_at": comment.updated_at,
                "votes_count": 0, "likes_count": 0, "dislikes_count": 0, "author": None, "replies": [],
                "attachments" : [],
            }

        return {
            "id": comment.id, "content": comment.content, "is_deleted": False, "is_best_answer": comment.is_best_answer,
            "is_admin_notice": comment.is_admin_notice,
            "parent_id": comment.parent_id, "created_at": comment.created_at, "updated_at": comment.updated_at,
            "votes_count": votes_count, "likes_count": likes_count, "dislikes_count": dislikes_count,
            "author": get_comment_author_data(db, comment.user_id), "replies": [],
            "attachments": [{"id": a.id, "filename": a.filename, "file_size": a.file_size, "mime_type": a.mime_type}
                            for a in db.exec(select(CommentAttachment).where(CommentAttachment.comment_id == comment.id)).all()],
        }

    comment_dict = {comment.id: build_comment_dict(comment) for comment in all_comments}
    top_level = []

    # SPAJANJE U BESKONAČNO STABLO (Podržava reply na reply na reply...)
    for comment in all_comments:
        comment_data = comment_dict[comment.id]
        if comment.parent_id is None:
            top_level.append(comment_data)
        else:
            parent = comment_dict.get(comment.parent_id)
            if parent:
                parent["replies"].append(comment_data)

    # Rekurzivno sortiranje svih podnivoa komentara
    def sort_replies_recursive(comment_data):
        if comment_data["replies"]:
            comment_data["replies"].sort(key=lambda c: (not c.get("is_admin_notice", False), c["created_at"]))
            for reply in comment_data["replies"]:
                sort_replies_recursive(reply)

    for root_comment in top_level:
        sort_replies_recursive(root_comment)

    # Sortiranje glavnih (top-level) komentara
    top_level.sort(key=lambda item: (
        not item.get("is_admin_notice", False),
        not item.get("is_best_answer", False),
        -item["votes_count"],
        item["created_at"]
    ))
    return top_level


# ---------------------------------------------------------------------------
# RUTE ZA KOMENTARE
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

    is_admin_notice = getattr(comment_data, "is_admin_notice", False)
    current_role = getattr(current_user.role, "value", current_user.role)

    if is_admin_notice and current_role != "admin":
        is_admin_notice = False

    # --- POSEBNA LOGIKA ZA ADMIN NOTICE ---
    # 1. Admin Notice NE SMIJE biti kreiran kao odgovor na bilo šta
    if is_admin_notice and comment_data.parent_id is not None:
        raise HTTPException(
            status_code=400, 
            detail="Administratorsko obavještenje mora biti glavni komentar i ne može biti odgovor."
        )

    # 2. Provjera ako se šalje običan odgovor da li je roditelj Admin Notice
    if comment_data.parent_id is not None:
        parent_comment = db.get(ForumComment, comment_data.parent_id)
        if not parent_comment or parent_comment.is_deleted:
            raise HTTPException(status_code=404, detail="Komentar na koji odgovarate ne postoji.")
        
        if parent_comment.is_admin_notice:
            raise HTTPException(
                status_code=400, 
                detail="Nije dozvoljeno odgovarati na zvanična administratorska obavještenja."
            )

    new_comment = ForumComment(
        content=comment_data.content,
        topic_id=comment_data.topic_id,
        user_id=current_user.id,
        is_admin_notice=is_admin_notice,
        parent_id=comment_data.parent_id
    )

    db.add(new_comment)
    db.flush()

    register_answer_created(db, user_id=current_user.id, comment_id=new_comment.id)

    actor_name = get_user_display_name(current_user)

    # 1. Ako je glavni komentar na temu, autor teme dobija notifikaciju.
    if new_comment.parent_id is None:
        create_forum_notification(
            db=db,
            recipient_user_id=topic.user_id,
            actor_user_id=current_user.id,
            topic_id=topic.id,
            comment_id=new_comment.id,
            notification_type=ForumNotificationType.TOPIC_REPLY,
            text=f"Kolega {actor_name} je odgovorio na vašu temu {topic.title}.",
        )

    # 2. Ako je reply na specifičan komentar, autor tog komentara dobija notifikaciju.
    else:
        parent_comment = db.get(ForumComment, new_comment.parent_id)

        if parent_comment and not parent_comment.is_deleted:
            create_forum_notification(
                db=db,
                recipient_user_id=parent_comment.user_id,
                actor_user_id=current_user.id,
                topic_id=topic.id,
                comment_id=new_comment.id,
                notification_type=ForumNotificationType.COMMENT_REPLY,
                text=f"Kolega {actor_name} je odgovorio na vaš komentar u temi {topic.title}.",
            )

    # 3. Ako komentar sadrži @username, označeni korisnik dobija mention notifikaciju.
    notify_mentions(
        db=db,
        text=new_comment.content,
        actor_user=current_user,
        topic=topic,
        comment_id=new_comment.id,
    )

    db.commit()
    db.refresh(new_comment)

    comments_count = get_comments_count(db, topic.id)
    log_activity(
        db,
        current_user.id,
        ActivityType.FORUM_COMMENT,
        topic.title,
        f"Diskusija · {comments_count} odgovora",
        topic.id
    )

    return {
        "id": new_comment.id,
        "content": new_comment.content,
        "topic_id": new_comment.topic_id,
        "parent_id": new_comment.parent_id,
        "is_admin_notice": new_comment.is_admin_notice,
        "created_at": new_comment.created_at,
        "author": get_comment_author_data(db, new_comment.user_id)
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

    # Ako je komentar već najbolji odgovor, sada ga skidamo.
    if comment.is_best_answer:
        comment.is_best_answer = False

        old_notification = db.exec(
            select(ForumNotification).where(
                ForumNotification.recipient_user_id == comment.user_id,
                ForumNotification.actor_user_id == current_user.id,
                ForumNotification.topic_id == topic.id,
                ForumNotification.comment_id == comment.id,
                ForumNotification.type == ForumNotificationType.BEST_ANSWER,
                ForumNotification.is_hidden == False,
            )
        ).first()

        if old_notification:
            old_notification.is_hidden = True
            db.add(old_notification)

    # Ako komentar nije najbolji odgovor, sada ga označavamo.
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

            old_notification = db.exec(
                select(ForumNotification).where(
                    ForumNotification.recipient_user_id == existing_best.user_id,
                    ForumNotification.actor_user_id == current_user.id,
                    ForumNotification.topic_id == topic.id,
                    ForumNotification.comment_id == existing_best.id,
                    ForumNotification.type == ForumNotificationType.BEST_ANSWER,
                    ForumNotification.is_read == False,
                    ForumNotification.is_hidden == False,
                )
            ).first()

            if old_notification:
                old_notification.is_hidden = True
                db.add(old_notification)

        comment.is_best_answer = True

        register_best_answer(
            db,
            user_id=comment.user_id,
            giver_id=topic.user_id,
            comment_id=comment.id,
        )

        create_forum_notification(
            db=db,
            recipient_user_id=comment.user_id,
            actor_user_id=current_user.id,
            topic_id=topic.id,
            comment_id=comment.id,
            notification_type=ForumNotificationType.BEST_ANSWER,
            text=f"Čestitamo! Autor teme {topic.title} je označio Vaš odgovor kao najbolji.",
            prevent_duplicate=True,
        )

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
    current_user: User = Depends(get_current_user),
):
    if vote_data.value not in (1, -1):
        raise HTTPException(status_code=400, detail="Vrijednost glasa mora biti 1 ili -1.")

    comment = db.get(ForumComment, comment_id)
    if not comment or comment.is_deleted:
        raise HTTPException(status_code=404, detail="Komentar nije pronađen.")

    topic = db.get(ForumTopic, comment.topic_id)
    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")

    existing_vote = db.exec(
        select(ForumCommentVote).where(
            ForumCommentVote.comment_id == comment_id,
            ForumCommentVote.user_id == current_user.id,
        )
    ).first()

    should_notify_comment_vote = False
    notification_type = None
    notification_text = None

    if existing_vote:
        if existing_vote.value == vote_data.value:
            previous_value = existing_vote.value

            db.delete(existing_vote)
            db.flush()

            rollback_comment_vote(
                db,
                user_id=comment.user_id,
                giver_id=current_user.id,
                comment_id=comment_id,
                previous_value=previous_value,
            )

            # Ako uklanja like, sakrij staru like notifikaciju.
            if previous_value == 1:
                hide_forum_notification(
                    db=db,
                    recipient_user_id=comment.user_id,
                    actor_user_id=current_user.id,
                    topic_id=topic.id,
                    comment_id=comment.id,
                    notification_type=ForumNotificationType.COMMENT_LIKE,
                    only_unread=False,
                )

            # Ako uklanja dislike, sakrij staru dislike notifikaciju.
            if previous_value == -1:
                hide_forum_notification(
                    db=db,
                    recipient_user_id=comment.user_id,
                    actor_user_id=current_user.id,
                    topic_id=topic.id,
                    comment_id=comment.id,
                    notification_type=ForumNotificationType.COMMENT_DISLIKE,
                    only_unread=False,
                )

            user_vote = 0

        else:
            previous_value = existing_vote.value
            existing_vote.value = vote_data.value

            db.add(existing_vote)
            db.flush()

            rollback_comment_vote(
                db,
                user_id=comment.user_id,
                giver_id=current_user.id,
                comment_id=comment_id,
                previous_value=previous_value,
            )

            register_comment_vote(
                db,
                user_id=comment.user_id,
                giver_id=current_user.id,
                comment_id=comment_id,
                vote_value=vote_data.value,
            )

            # Ako mijenja like u dislike, sakrij staru like notifikaciju.
            if previous_value == 1:
                hide_forum_notification(
                    db=db,
                    recipient_user_id=comment.user_id,
                    actor_user_id=current_user.id,
                    topic_id=topic.id,
                    comment_id=comment.id,
                    notification_type=ForumNotificationType.COMMENT_LIKE,
                    only_unread=False,
                )

            # Ako mijenja dislike u like, sakrij staru dislike notifikaciju.
            if previous_value == -1:
                hide_forum_notification(
                    db=db,
                    recipient_user_id=comment.user_id,
                    actor_user_id=current_user.id,
                    topic_id=topic.id,
                    comment_id=comment.id,
                    notification_type=ForumNotificationType.COMMENT_DISLIKE,
                    only_unread=False,
                )

            should_notify_comment_vote = True
            user_vote = vote_data.value

    else:
        new_vote = ForumCommentVote(
            comment_id=comment_id,
            user_id=current_user.id,
            value=vote_data.value,
        )

        db.add(new_vote)
        db.flush()

        register_comment_vote(
            db,
            user_id=comment.user_id,
            giver_id=current_user.id,
            comment_id=comment_id,
            vote_value=vote_data.value,
        )

        should_notify_comment_vote = True
        user_vote = vote_data.value

    if should_notify_comment_vote:
        actor_name = get_user_display_name(current_user)

        if vote_data.value == 1:
            notification_type = ForumNotificationType.COMMENT_LIKE
            notification_text = f"Kolega {actor_name} je lajkao/la vaš komentar u temi {topic.title}."
        else:
            notification_type = ForumNotificationType.COMMENT_DISLIKE
            notification_text = f"Kolega {actor_name} je dislajkao/la vaš komentar u temi {topic.title}."

        create_forum_notification(
            db=db,
            recipient_user_id=comment.user_id,
            actor_user_id=current_user.id,
            topic_id=topic.id,
            comment_id=comment.id,
            notification_type=notification_type,
            text=notification_text,
            prevent_duplicate=True,
        )

    db.commit()

    total_votes = get_comment_votes_count(db, comment_id)

    return {
        "comment_id": comment_id,
        "votes_count": total_votes,
        "user_vote": user_vote,
    }

@router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = db.get(ForumComment, comment_id)
    if not comment or comment.is_deleted:
        raise HTTPException(status_code=404, detail="Komentar nije pronađen.")
    
    current_role = getattr(current_user.role, "value", current_user.role)
    if comment.user_id != current_user.id and current_role != "admin":
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
        # Direktni SQL — zaobiđi ORM dependency resolver
        db.exec(
            ForumComment.__table__.update()
            .where(ForumComment.__table__.c.parent_id == comment_id)
            .values(parent_id=None)
        )
        db.flush()
        db.exec(
            ForumComment.__table__.delete()
            .where(ForumComment.__table__.c.id == comment_id)
        )
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
    
    current_role = getattr(current_user.role, "value", current_user.role)
    if comment.user_id != current_user.id and current_role != "admin":
        raise HTTPException(status_code=403, detail="Možete editovati samo vlastiti komentar.")

    topic = db.get(ForumTopic, comment.topic_id)
    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")

    old_content = comment.content
    
    comment.content = comment_data.content
    comment.updated_at = datetime.utcnow()

    db.add(comment)

    notify_mentions(
        db=db,
        text=comment.content,
        old_text=old_content,
        actor_user=current_user,
        topic=topic,
        comment_id=comment.id,
    )

    db.commit()
    db.refresh(comment)
    
    return {"id": comment.id, "content": comment.content, "updated_at": comment.updated_at}

@router.post("/{topic_id}/admin-notice", status_code=status.HTTP_201_CREATED)
def create_admin_notice(
    topic_id: int,
    data: AdminNoticeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_role = getattr(current_user.role, "value", current_user.role)
    if current_role != "admin":
        raise HTTPException(status_code=403, detail="Nemate ovlaštenje.")

    topic = db.get(ForumTopic, topic_id)
    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")

    notice = ForumComment(
        content=data.content,
        topic_id=topic_id,
        user_id=current_user.id,
        is_admin_notice=True,
        parent_id=None # Eksplicitno forsiramo da nema roditelja
    )
    db.add(notice)
    db.commit()
    db.refresh(notice)
    return {"success": True, "id": notice.id}