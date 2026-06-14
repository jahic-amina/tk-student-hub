from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ForumUserStats(SQLModel, table=True):
    """
    Čuva trenutne bodove i statistiku jednog korisnika.

    user_id je ujedno primarni ključ, tako da svaki korisnik
    može imati samo jedan zapis statistike.
    """

    __tablename__ = "forum_user_stats"

    user_id: int = Field(
        foreign_key="users.id",
        primary_key=True
    )

    reputation_points: int = Field(
        default=0,
        nullable=False
    )

    topics_started_count: int = Field(
        default=0,
        nullable=False
    )

    answers_count: int = Field(
        default=0,
        nullable=False
    )

    best_answers_count: int = Field(
        default=0,
        nullable=False
    )

    night_topics_count: int = Field(
        default=0,
        nullable=False
    )

    updated_at: datetime = Field(
        default_factory=utc_now,
        nullable=False
    )


class ForumUserMedal(SQLModel, table=True):
    """
    Čuva sve osvojene medalje.

    Medalje se nikada ne brišu kada korisniku padnu bodovi.
    """

    __tablename__ = "forum_user_medals"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "medal_code",
            name="uq_forum_user_medal"
        ),
    )

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    user_id: int = Field(
        foreign_key="users.id",
        index=True
    )

    medal_code: str = Field(
        index=True,
        nullable=False
    )

    category: str = Field(
        nullable=False
    )

    tier: str = Field(
        nullable=False
    )

    is_secret: bool = Field(
        default=False,
        nullable=False
    )

    awarded_at: datetime = Field(
        default_factory=utc_now,
        nullable=False
    )


class ForumReputationEvent(SQLModel, table=True):
    """
    Historija svih promjena bodova.

    event_key mora biti jedinstven kako korisnik ne bi dobio
    bodove više puta za istu temu ili isti komentar.
    """

    __tablename__ = "forum_reputation_events"

    __table_args__ = (
        UniqueConstraint(
            "event_key",
            name="uq_forum_reputation_event_key"
        ),
    )

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    user_id: int = Field(
        foreign_key="users.id",
        index=True
    )

    event_key: str = Field(
        index=True,
        nullable=False
    )

    points_delta: int = Field(
        nullable=False
    )

    reason: str = Field(
        nullable=False
    )

    source_type: Optional[str] = Field(
        default=None
    )

    source_id: Optional[int] = Field(
        default=None
    )

    created_at: datetime = Field(
        default_factory=utc_now,
        nullable=False
    )