from datetime import datetime, timezone, timedelta  # <-- Dodat timedelta za provjeru 24h
from typing import Optional
from zoneinfo import ZoneInfo

from sqlmodel import Session, select, func # <-- Dodat func za zbrajanje poena u bazi

from app.models.forum_reputation import (
    ForumReputationEvent,
    ForumUserMedal,
    ForumUserStats,
    ForumReputationDailyLog,  # <-- Uvezen novi model za dnevni limit
)

SARAJEVO_TIMEZONE = ZoneInfo("Europe/Sarajevo")


# PRAVILA ZA NIVOE I TITULE (Ostalo netaknuto)

LEVEL_RULES = [
    {"level": 1, "min_points": 0, "title": "Novi član"},
    {"level": 2, "min_points": 101, "title": "Aktivni član"},
    {"level": 3, "min_points": 251, "title": "Poznavalac"},
    {"level": 4, "min_points": 501, "title": "Mentor zajednice"},
    {"level": 5, "min_points": 1001, "title": "Legenda foruma"},
]

MEDAL_RULES = {
    "best_answers": [(1, "bronze"), (5, "silver"), (15, "gold")],
    "topics_started": [(3, "bronze"), (10, "silver"), (25, "gold")],
    "reputation": [(100, "bronze"), (500, "silver"), (1000, "gold")],
    "night_owl": [(1, "bronze"), (3, "silver"), (10, "gold")],
}

MEDAL_CATEGORY_NAMES = {
    "best_answers": "Najbolji odgovori",
    "topics_started": "Pokrenute teme",
    "reputation": "Ukupna reputacija",
    "night_owl": "Noćna ptica",
}

MEDAL_TIER_NAMES = {"bronze": "Bronzana", "silver": "Srebrna", "gold": "Zlatna"}
ROLE_LABELS = {"member": "Student", "student": "Student", "mentor": "Autor", "author": "Autor", "admin": "Admin"}

def get_level_info(points: int) -> dict:
    safe_points = max(0, points)
    selected_level = LEVEL_RULES[0]
    for level_rule in LEVEL_RULES:
        if safe_points >= level_rule["min_points"]:
            selected_level = level_rule
        else:
            break
    return {"level": selected_level["level"], "title": selected_level["title"]}

def get_role_label(role) -> str:
    if hasattr(role, "value"): raw_role = role.value
    else: raw_role = str(role)
    raw_role = raw_role.lower()
    return ROLE_LABELS.get(raw_role, raw_role.capitalize())

def get_or_create_stats(db: Session, user_id: int) -> ForumUserStats:
    stats = db.get(ForumUserStats, user_id)
    if stats is None:
        stats = ForumUserStats(user_id=user_id)
        db.add(stats)
        db.flush()
    return stats

def reputation_event_exists(db: Session, event_key: str) -> bool:
    existing_event = db.exec(select(ForumReputationEvent).where(ForumReputationEvent.event_key == event_key)).first()
    return existing_event is not None

def award_eligible_medals(db: Session, stats: ForumUserStats) -> None:
    existing_medals = db.exec(select(ForumUserMedal).where(ForumUserMedal.user_id == stats.user_id)).all()
    existing_codes = {medal.medal_code for medal in existing_medals}
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
            should_receive_medal = (current_value >= threshold and medal_code not in existing_codes)
            if should_receive_medal:
                new_medal = ForumUserMedal(user_id=stats.user_id, medal_code=medal_code, category=category, tier=tier, is_secret=(category == "night_owl"))
                db.add(new_medal)
                existing_codes.add(medal_code)


# REGISTRACIJA AKTIVNOSTI (IZMIJENJENO I NADOGRADJENO!)


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
    giver_id: Optional[int] = None,  # <-- DODATAK: Ko inicira dodjelu bodova
) -> ForumUserStats:
    """
    Glavna funkcija za dodavanje i oduzimanje bodova.
    Obezbjeđuje Anti-Abuse provjere za samog sebe i dnevne limite.
    """
    stats = get_or_create_stats(db, user_id)

    if reputation_event_exists(db, event_key):
        return stats

    # --- Glas na sopstveni sadržaj ne donosi bodove ---
    if giver_id is not None and giver_id == user_id:
        points_delta = 0  # Bodovi se poništavaju, ali se brojači (counters) i dalje ažuriraju!

    # --- Anti-Abuse dnevni limit (Maksimalno +30 bodova u 24h) ---
    adjusted_points_delta = points_delta
    
    if giver_id is not None and giver_id != 0 and points_delta > 0:
        time_limit = datetime.now(timezone.utc) - timedelta(hours=24)
        
        # Izračunaj koliko je bodova ovaj giver već prenio primaocu u zadnjih 24 sata
        past_points = db.exec(
            select(func.coalesce(func.sum(ForumReputationDailyLog.points_given), 0)).where(
                ForumReputationDailyLog.giver_id == giver_id,
                ForumReputationDailyLog.receiver_id == user_id,
                ForumReputationDailyLog.created_at >= time_limit
            )
        ).one() or 0

        if past_points >= 30:
            adjusted_points_delta = 0  # Limit je već popunjen
        elif past_points + points_delta > 30:
            adjusted_points_delta = 30 - past_points  # Daj mu samo razliku do 30

        # Ako je išta bodova prošlo kroz filter, upiši to u dnevnik dnevnog limita
        if adjusted_points_delta > 0:
            daily_log = ForumReputationDailyLog(giver_id=giver_id, receiver_id=user_id, points_given=adjusted_points_delta)
            db.add(daily_log)

    # Primjena preračunatih i osiguranih bodova
    new_points = stats.reputation_points + adjusted_points_delta
    stats.reputation_points = max(0, new_points)

    if counters:
        for counter_name, counter_change in counters.items():
            if not hasattr(stats, counter_name):
                raise ValueError(f"Nepoznata statistika: {counter_name}")
            current_value = getattr(stats, counter_name)
            setattr(stats, counter_name, max(0, current_value + counter_change))

    stats.updated_at = datetime.now(timezone.utc)

    reputation_event = ForumReputationEvent(
        user_id=user_id,
        event_key=event_key,
        points_delta=adjusted_points_delta,  # Bilježimo stvarni delta nakon filtera
        reason=reason,
        source_type=source_type,
        source_id=source_id,
    )

    db.add(stats)
    db.add(reputation_event)

    # Automatska dodjela kolegicih medalja na osnovu novog stanja
    award_eligible_medals(db, stats)
    db.flush()

    return stats


# OSTALE FUNKCIJE (Prilagođene da prosljeđuju giver_id)


def is_night_topic(created_at: Optional[datetime]) -> bool:
    if created_at is None: created_at = datetime.now(timezone.utc)
    if created_at.tzinfo is None: created_at = created_at.replace(tzinfo=timezone.utc)
    local_time = created_at.astimezone(SARAJEVO_TIMEZONE)
    return 3 <= local_time.hour < 5

def register_topic_created(db: Session, *, user_id: int, topic_id: int, created_at: Optional[datetime]) -> ForumUserStats:
    counters = {"topics_started_count": 1}
    if is_night_topic(created_at):
        counters["night_topics_count"] = 1

    return register_activity(
        db, user_id=user_id, giver_id=0, event_key=f"topic_created:{topic_id}",
        points_delta=10, reason="Pokrenuta nova forum tema", source_type="forum_topic", source_id=topic_id, counters=counters
    )

def register_answer_created(db: Session, *, user_id: int, comment_id: int) -> ForumUserStats:
    return register_activity(
        db, user_id=user_id, giver_id=0, event_key=f"answer_created:{comment_id}",
        points_delta=3, reason="Napisan odgovor na forumu", source_type="forum_comment", source_id=comment_id, counters={"answers_count": 1}
    )

def register_best_answer(db: Session, *, user_id: int, giver_id: int, comment_id: int) -> ForumUserStats:
    """Sada prima i giver_id (autora teme) da provjeri je li sam sebi označio odgovor"""
    return register_activity(
        db, user_id=user_id, giver_id=giver_id, event_key=f"best_answer:{comment_id}",
        points_delta=25, reason="Odgovor označen kao najbolji odgovor", source_type="forum_comment", source_id=comment_id, counters={"best_answers_count": 1}
    )

def remove_reputation_points(db: Session, *, user_id: int, event_key: str, points: int, reason: str, source_type: Optional[str] = None, source_id: Optional[int] = None) -> ForumUserStats:
    return register_activity(db, user_id=user_id, giver_id=0, event_key=event_key, points_delta=-abs(points), reason=reason, source_type=source_type, source_id=source_id)


# NOVO: PODRŠKA ZA LAJK / DISLAJK 

def register_comment_vote(db: Session, *, user_id: int, giver_id: int, comment_id: int, vote_value: int) -> ForumUserStats:
    """Računa +5 za lajk i -2 za dislajk kroz sve anti-abuse provjere."""
    points_delta = 5 if vote_value == 1 else -2
    reason = "Dobijen lajk na komentar" if vote_value == 1 else "Dobijen dislajk na komentar"
    
    return register_activity(
        db, user_id=user_id, giver_id=giver_id, event_key=f"vote:{giver_id}:comment:{comment_id}:{vote_value}",
        points_delta=points_delta, reason=reason, source_type="forum_comment", source_id=comment_id
    )

def rollback_comment_vote(db: Session, *, user_id: int, giver_id: int, comment_id: int, previous_value: int) -> ForumUserStats:
    """Oduzima ili vraća bodove unazad kada korisnik klikne ponovo na istu opciju i povuče glas."""
    points_delta = -5 if previous_value == 1 else 2
    reason = "Korisnik je povukao svoj glas sa komentara"
    
    return register_activity(
        db, user_id=user_id, giver_id=0, event_key=f"vote_rollback:{giver_id}:comment:{comment_id}:{datetime.now(timezone.utc).timestamp()}",
        points_delta=points_delta, reason=reason, source_type="forum_comment", source_id=comment_id
    )


# PODACI KOJE FRONTEND PRIKAZUJE (Ostalo netaknuto)

def get_user_forum_identity(db: Session, user) -> dict:
    stats = get_or_create_stats(db, user.id)
    level_info = get_level_info(stats.reputation_points)

    medals = db.exec(select(ForumUserMedal).where(ForumUserMedal.user_id == user.id).order_by(ForumUserMedal.awarded_at)).all()
    medals_output = []

    for medal in medals:
        medals_output.append({
            "code": medal.medal_code,
            "category": medal.category,
            "category_name": MEDAL_CATEGORY_NAMES.get(medal.category, medal.category),
            "tier": medal.tier,
            "tier_name": MEDAL_TIER_NAMES.get(medal.tier, medal.tier),
            "icon_key": medal.medal_code,
            "is_secret": medal.is_secret,
            "awarded_at": medal.awarded_at,
        })

    return {
        "role": get_role_label(user.role),
        "level": level_info["level"],
        "title": level_info["title"],
        "reputation_points": stats.reputation_points,
        "medals": medals_output,
    }