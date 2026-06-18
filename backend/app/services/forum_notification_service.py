import re
from typing import Optional, Set

from sqlmodel import Session, select, func

from app.models.user import User
from app.models.forum import ForumTopic
from app.models.forum_notification import (
    ForumNotification,
    ForumNotificationType,
)


MENTION_REGEX = re.compile(r"(?<!\w)@([A-Za-z0-9_.-]{2,80})")


def get_user_display_name(user: User) -> str:
    return (
        getattr(user, "full_name", None)
        or getattr(user, "username", None)
        or "Kolega"
    )


def extract_mentions(text: str) -> Set[str]:
    if not text:
        return set()

    return {match.group(1).lower() for match in MENTION_REGEX.finditer(text)}


def create_forum_notification(
    db: Session,
    recipient_user_id: int,
    actor_user_id: int,
    topic_id: int,
    notification_type: ForumNotificationType,
    text: str,
    comment_id: Optional[int] = None,
    prevent_duplicate: bool = False,
) -> Optional[ForumNotification]:
    """
    Dodaje forum notifikaciju u trenutnu transakciju.
    Funkcija ne poziva commit. Commit radi endpoint.
    """

    # Korisnik ne dobija notifikaciju za vlastitu radnju.
    if recipient_user_id == actor_user_id:
        return None

    if prevent_duplicate:
        existing_notification = db.exec(
            select(ForumNotification).where(
                ForumNotification.recipient_user_id == recipient_user_id,
                ForumNotification.actor_user_id == actor_user_id,
                ForumNotification.topic_id == topic_id,
                ForumNotification.comment_id == comment_id,
                ForumNotification.type == notification_type,
                ForumNotification.is_hidden == False,
            )
        ).first()

        if existing_notification:
            return existing_notification

    notification = ForumNotification(
        recipient_user_id=recipient_user_id,
        actor_user_id=actor_user_id,
        topic_id=topic_id,
        comment_id=comment_id,
        text=text,
        type=notification_type,
        is_read=False,
        is_hidden=False,
    )

    db.add(notification)

    return notification

def hide_forum_notification(
    db: Session,
    recipient_user_id: int,
    actor_user_id: int,
    topic_id: int,
    notification_type: ForumNotificationType,
    comment_id: Optional[int] = None,
    only_unread: bool = False,
) -> None:
    query = select(ForumNotification).where(
        ForumNotification.recipient_user_id == recipient_user_id,
        ForumNotification.actor_user_id == actor_user_id,
        ForumNotification.topic_id == topic_id,
        ForumNotification.comment_id == comment_id,
        ForumNotification.type == notification_type,
        ForumNotification.is_hidden == False,
    )

    if only_unread:
        query = query.where(ForumNotification.is_read == False)

    notifications = db.exec(query).all()

    for notification in notifications:
        notification.is_hidden = True
        db.add(notification)

def notify_mentions(
    db: Session,
    text: str,
    actor_user: User,
    topic: ForumTopic,
    comment_id: Optional[int] = None,
    old_text: Optional[str] = None,
) -> None:
    """
    Pronalazi @username u tekstu i šalje notifikacije.
    Pošto User model nema username kolonu, koristimo dio emaila prije @.
    Primjer: korisnik ima email ima.osm@gmail.com -> mention je @ima.osm
    """

    new_mentions = extract_mentions(text)
    old_mentions = extract_mentions(old_text) if old_text else set()

    mentions_to_notify = new_mentions - old_mentions

    if not mentions_to_notify:
        return

    users = db.exec(select(User)).all()

    actor_name = get_user_display_name(actor_user)

    for mentioned_user in users:
        email = getattr(mentioned_user, "email", None)

        if not email or "@" not in email:
            continue

        mention_name = email.split("@")[0].lower()

        if mention_name not in mentions_to_notify:
            continue

        if mentioned_user.id == actor_user.id:
            continue

        notification_text = (
            f"Kolega {actor_name} vas je spomenuo "
            f"u temi {topic.title}"
        )

        create_forum_notification(
            db=db,
            recipient_user_id=mentioned_user.id,
            actor_user_id=actor_user.id,
            topic_id=topic.id,
            comment_id=comment_id,
            notification_type=ForumNotificationType.MENTION,
            text=notification_text,
            prevent_duplicate=True,
        )