from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from typing import List, Dict, Any

from app.database import get_db
from app.models.forum import ForumTag, ForumTopicTag

router = APIRouter(prefix="/forum/tags", tags=["Forum Tags"])


@router.get("/", response_model=List[Dict[str, Any]])
def get_popular_tags(db: Session = Depends(get_db), limit: int = 20):
    """Vraca tagove sortirane po popularnosti (koliko tema ih koristi)."""
    results = db.exec(
        select(
            ForumTag.id,
            ForumTag.name,
            func.count(ForumTopicTag.topic_id).label("usage_count")
        )
        .join(ForumTopicTag, ForumTopicTag.tag_id == ForumTag.id, isouter=True)
        .group_by(ForumTag.id)
        .order_by(func.count(ForumTopicTag.topic_id).desc())
        .limit(limit)
    ).all()

    return [{"id": r.id, "name": r.name, "usage_count": r.usage_count} for r in results]