from typing import Optional

from sqlmodel import Session

from app.models.forum_notification import (
    ForumNotification,
    ForumNotificationType,
)


def create_forum_notification(
    db: Session,
    recipient_user_id: int,
    actor_user_id: int,
    topic_id: int,
    notification_type: ForumNotificationType,
    text: str,
) -> Optional[ForumNotification]:
    """
    Dodaje forum notifikaciju u trenutnu transakciju.

    Funkcija ne poziva commit. Commit radi endpoint za lajk
    ili komentar.
    """

    # Korisnik ne dobija notifikaciju za vlastitu radnju.
    if recipient_user_id == actor_user_id:
        return None

    notification = ForumNotification(
        recipient_user_id=recipient_user_id,
        actor_user_id=actor_user_id,
        topic_id=topic_id,
        text=text,
        type=notification_type,
        is_read=False,
    )

    db.add(notification)

    return notification