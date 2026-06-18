from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.security import get_current_user
from app.database import get_db
from app.models.forum_notification import ForumNotification
from app.models.user import User


router = APIRouter(
    prefix="/forum/notifications",
    tags=["Forum Notifications"],
)


@router.get("/me", response_model=list[ForumNotification])
def get_my_forum_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = (
        select(ForumNotification)
        .where(

            ForumNotification.recipient_user_id == current_user.id,
            ForumNotification.is_hidden == False,
            
        )
        .order_by(
            ForumNotification.is_read.asc(),
            ForumNotification.created_at.desc(),
        )
    )

    return db.exec(statement).all()


@router.patch(
    "/{notification_id}/read",
    response_model=ForumNotification,
)
def mark_forum_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification = db.get(
        ForumNotification,
        notification_id,
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Forum notifikacija nije pronađena.",
        )

    if notification.recipient_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nemate pristup ovoj notifikaciji.",
        )

    notification.is_read = True

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification


@router.patch("/read-all")
def mark_all_forum_notifications_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notifications = db.exec(
        select(ForumNotification).where(
            ForumNotification.recipient_user_id == current_user.id,
            ForumNotification.is_read == False,
            ForumNotification.is_hidden == False,

        )
    ).all()

    for notification in notifications:
        notification.is_read = True
        db.add(notification)

    db.commit()

    return {
        "message": "Sve forum notifikacije su označene kao pročitane.",
        "updated_count": len(notifications),
    }


@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_forum_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification = db.get(
        ForumNotification,
        notification_id,
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Forum notifikacija nije pronađena.",
        )

    if notification.recipient_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nemate pristup ovoj notifikaciji.",
        )

    db.delete(notification)
    db.commit()

    return None