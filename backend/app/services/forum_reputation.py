from datetime import datetime, timezone
from typing import Optional
from zoneinfo import ZoneInfo

from sqlmodel import Session, select

from app.models.forum_reputation import (
    ForumReputationEvent,
    ForumUserMedal,
    ForumUserStats,
)


SARAJEVO_TIMEZONE = ZoneInfo("Europe/Sarajevo")


# ---------------------------------------------------------
# PRAVILA ZA NIVOE I TITULE
# ---------------------------------------------------------

LEVEL_RULES = [
    {
        "level": 1,
        "min_points": 0,
        "title": "Novi član",
    },
    {
        "level": 2,
        "min_points": 101,
        "title": "Aktivni član",
    },
    {
        "level": 3,
        "min_points": 251,
        "title": "Poznavalac",
    },
    {
        "level": 4,
        "min_points": 501,
        "title": "Mentor zajednice",
    },
    {
        "level": 5,
        "min_points": 1001,
        "title": "Legenda foruma",
    },
]


# ---------------------------------------------------------
# PRAVILA ZA MEDALJE
# ---------------------------------------------------------

MEDAL_RULES = {
    # Broj najboljih odgovora
    "best_answers": [
        (1, "bronze"),
        (5, "silver"),
        (15, "gold"),
    ],

    # Broj pokrenutih tema
    "topics_started": [
        (3, "bronze"),
        (10, "silver"),
        (25, "gold"),
    ],

    # Ukupna reputacija
    "reputation": [
        (100, "bronze"),
        (500, "silver"),
        (1000, "gold"),
    ],

    # Teme napisane između 03:00 i 05:00
    "night_owl": [
        (1, "bronze"),
        (3, "silver"),
        (10, "gold"),
    ],
}


MEDAL_CATEGORY_NAMES = {
    "best_answers": "Najbolji odgovori",
    "topics_started": "Pokrenute teme",
    "reputation": "Ukupna reputacija",
    "night_owl": "Noćna ptica",
}


MEDAL_TIER_NAMES = {
    "bronze": "Bronzana",
    "silver": "Srebrna",
    "gold": "Zlatna",
}


# Vrijednosti koje već postoje u UserRole enumu
ROLE_LABELS = {
    "member": "Student",
    "student": "Student",
    "mentor": "Autor",
    "author": "Autor",
    "admin": "Admin",
}


# ---------------------------------------------------------
# NIVOU I ULOGE
# ---------------------------------------------------------

def get_level_info(points: int) -> dict:
    """
    Na osnovu trenutnog broja bodova vraća nivo i titulu.
    """

    safe_points = max(0, points)
    selected_level = LEVEL_RULES[0]

    for level_rule in LEVEL_RULES:
        if safe_points >= level_rule["min_points"]:
            selected_level = level_rule
        else:
            break

    return {
        "level": selected_level["level"],
        "title": selected_level["title"],
    }


def get_role_label(role) -> str:
    """
    Pretvara backend rolu u naziv koji će frontend prikazivati.

    member -> Student
    mentor -> Autor
    admin -> Admin
    """

    if hasattr(role, "value"):
        raw_role = role.value
    else:
        raw_role = str(role)

    raw_role = raw_role.lower()

    return ROLE_LABELS.get(
        raw_role,
        raw_role.capitalize()
    )


# ---------------------------------------------------------
# STATISTIKA KORISNIKA
# ---------------------------------------------------------

def get_or_create_stats(
    db: Session,
    user_id: int,
) -> ForumUserStats:
    """
    Dohvata statistiku korisnika.

    Ako korisnik još nema zapis, automatski pravi zapis
    sa nulom bodova.
    """

    stats = db.get(ForumUserStats, user_id)

    if stats is None:
        stats = ForumUserStats(user_id=user_id)
        db.add(stats)
        db.flush()

    return stats


def reputation_event_exists(
    db: Session,
    event_key: str,
) -> bool:
    """
    Provjerava da li je neka aktivnost već obračunata.
    """

    existing_event = db.exec(
        select(ForumReputationEvent).where(
            ForumReputationEvent.event_key == event_key
        )
    ).first()

    return existing_event is not None


# ---------------------------------------------------------
# DODJELA MEDALJA
# ---------------------------------------------------------

def award_eligible_medals(
    db: Session,
    stats: ForumUserStats,
) -> None:
    """
    Provjerava da li je korisnik prešao neki prag medalje.

    Funkcija samo dodaje medalje.
    Ne postoji kod koji briše osvojene medalje.
    """

    existing_medals = db.exec(
        select(ForumUserMedal).where(
            ForumUserMedal.user_id == stats.user_id
        )
    ).all()

    existing_codes = {
        medal.medal_code
        for medal in existing_medals
    }

    metric_values = {
        "best_answers": stats.best_answers_count,
        "topics_started": stats.topics_started_count,
        "reputation": stats.reputation_points,
        "night_owl": stats.night_topics_count,
    }

    for category, category_rules in MEDAL_RULES.items():
        current_value = metric_values[category]

        for threshold, tier in category_rules:
            medal_code = f"{category}_{tier}"

            should_receive_medal = (
                current_value >= threshold
                and medal_code not in existing_codes
            )

            if should_receive_medal:
                new_medal = ForumUserMedal(
                    user_id=stats.user_id,
                    medal_code=medal_code,
                    category=category,
                    tier=tier,
                    is_secret=(category == "night_owl"),
                )

                db.add(new_medal)
                existing_codes.add(medal_code)


# ---------------------------------------------------------
# REGISTRACIJA AKTIVNOSTI
# ---------------------------------------------------------

def register_activity(
    db: Session,
    *,
    user_id: int,
    event_key: str,
    points_delta: int,
    reason: str,
    source_type: Optional[str] = None,
    source_id: Optional[int] = None,
    counters: Optional[dict[str, int]] = None,
) -> ForumUserStats:
    """
    Glavna funkcija za dodavanje i oduzimanje bodova.

    event_key sprečava duplo obračunavanje iste aktivnosti.
    """

    stats = get_or_create_stats(db, user_id)

    if reputation_event_exists(db, event_key):
        return stats

    new_points = stats.reputation_points + points_delta

    # Reputacija nikada ne ide ispod nule.
    stats.reputation_points = max(0, new_points)

    if counters:
        for counter_name, counter_change in counters.items():
            if not hasattr(stats, counter_name):
                raise ValueError(
                    f"Nepoznata statistika: {counter_name}"
                )

            current_value = getattr(stats, counter_name)

            setattr(
                stats,
                counter_name,
                max(0, current_value + counter_change),
            )

    stats.updated_at = datetime.now(timezone.utc)

    reputation_event = ForumReputationEvent(
        user_id=user_id,
        event_key=event_key,
        points_delta=points_delta,
        reason=reason,
        source_type=source_type,
        source_id=source_id,
    )

    db.add(stats)
    db.add(reputation_event)

    award_eligible_medals(db, stats)

    db.flush()

    return stats


# ---------------------------------------------------------
# TEMA
# ---------------------------------------------------------

def is_night_topic(created_at: Optional[datetime]) -> bool:
    """
    Vraća True ako je tema kreirana između 03:00 i 05:00
    po vremenskoj zoni Bosne i Hercegovine.
    """

    if created_at is None:
        created_at = datetime.now(timezone.utc)

    # SQLite često vrati datetime bez timezone informacije.
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)

    local_time = created_at.astimezone(SARAJEVO_TIMEZONE)

    return 3 <= local_time.hour < 5


def register_topic_created(
    db: Session,
    *,
    user_id: int,
    topic_id: int,
    created_at: Optional[datetime],
) -> ForumUserStats:
    """
    Dodjeljuje:
    +10 bodova za kreiranje teme
    +1 topics_started_count
    +1 night_topics_count ako je tema kreirana od 03:00 do 05:00
    """

    counters = {
        "topics_started_count": 1,
    }

    if is_night_topic(created_at):
        counters["night_topics_count"] = 1

    return register_activity(
        db,
        user_id=user_id,
        event_key=f"topic_created:{topic_id}",
        points_delta=10,
        reason="Pokrenuta nova forum tema",
        source_type="forum_topic",
        source_id=topic_id,
        counters=counters,
    )


# ---------------------------------------------------------
# ODGOVOR
# ---------------------------------------------------------

def register_answer_created(
    db: Session,
    *,
    user_id: int,
    comment_id: int,
) -> ForumUserStats:
    """
    Dodjeljuje:
    +3 boda za napisani odgovor
    +1 answers_count
    """

    return register_activity(
        db,
        user_id=user_id,
        event_key=f"answer_created:{comment_id}",
        points_delta=3,
        reason="Napisan odgovor na forumu",
        source_type="forum_comment",
        source_id=comment_id,
        counters={
            "answers_count": 1,
        },
    )


# ---------------------------------------------------------
# NAJBOLJI ODGOVOR
# ---------------------------------------------------------

def register_best_answer(
    db: Session,
    *,
    user_id: int,
    comment_id: int,
) -> ForumUserStats:
    """
    Dodjeljuje:
    +25 bodova za najbolji odgovor
    +1 best_answers_count
    """

    return register_activity(
        db,
        user_id=user_id,
        event_key=f"best_answer:{comment_id}",
        points_delta=25,
        reason="Odgovor označen kao najbolji odgovor",
        source_type="forum_comment",
        source_id=comment_id,
        counters={
            "best_answers_count": 1,
        },
    )


# ---------------------------------------------------------
# ODUZIMANJE BODOVA
# ---------------------------------------------------------

def remove_reputation_points(
    db: Session,
    *,
    user_id: int,
    event_key: str,
    points: int,
    reason: str,
    source_type: Optional[str] = None,
    source_id: Optional[int] = None,
) -> ForumUserStats:
    """
    Oduzima bodove, ali ne uklanja ranije osvojene medalje.
    """

    return register_activity(
        db,
        user_id=user_id,
        event_key=event_key,
        points_delta=-abs(points),
        reason=reason,
        source_type=source_type,
        source_id=source_id,
    )


# ---------------------------------------------------------
# PODACI KOJE FRONTEND PRIKAZUJE PORED IMENA
# ---------------------------------------------------------

def get_user_forum_identity(
    db: Session,
    user,
) -> dict:
    """
    Vraća ulogu, nivo, titulu, bodove i osvojene medalje.
    """

    stats = get_or_create_stats(db, user.id)
    level_info = get_level_info(stats.reputation_points)

    medals = db.exec(
        select(ForumUserMedal)
        .where(ForumUserMedal.user_id == user.id)
        .order_by(ForumUserMedal.awarded_at)
    ).all()

    medals_output = []

    for medal in medals:
        medals_output.append(
            {
                "code": medal.medal_code,
                "category": medal.category,
                "category_name": MEDAL_CATEGORY_NAMES.get(
                    medal.category,
                    medal.category,
                ),
                "tier": medal.tier,
                "tier_name": MEDAL_TIER_NAMES.get(
                    medal.tier,
                    medal.tier,
                ),
                "icon_key": medal.medal_code,
                "is_secret": medal.is_secret,
                "awarded_at": medal.awarded_at,
            }
        )

    return {
        "role": get_role_label(user.role),
        "level": level_info["level"],
        "title": level_info["title"],
        "reputation_points": stats.reputation_points,
        "medals": medals_output,
    }