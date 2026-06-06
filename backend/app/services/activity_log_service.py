from sqlalchemy.orm import Session
from app.models.activity_log import ActivityLog
from app.enums.activity import ActivityType
import logging

logger = logging.getLogger(__name__)

def log_activity(
        db: Session,
        user_id: int,
        activity_type: ActivityType,
        title: str,
        subtitle: str = None,
        entity_id: int = None
): 
    try:
        activity_log = ActivityLog(
            user_id=user_id,
            activity_type=activity_type,
            title=title,
            subtitle=subtitle,
            entity_id=entity_id
        )
        db.add(activity_log)
        db.commit()
    except Exception as e:
        logger.error(f"Greška prilikom logovanja aktivnosti za korisnika {user_id}: {e}")
        db.rollback()