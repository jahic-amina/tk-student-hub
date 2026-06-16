from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from typing import List, Dict, Any
from app.database import get_db
from app.models.forum import ForumTag, ForumTopicTag

router = APIRouter(prefix="/forum/tags", tags=["Forum Tags"])


@router.get("/", response_model=List[Dict[str, Any]])
def get_popular_tags(db: Session = Depends(get_db), limit: int = 20):
    """Vraca tagove cija je popularnost iznad prosjeka koristenja."""
    
    # 1. Baza agregira i vraca top X tagova (maksimalno optimizovano)
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

    if not results:
        return []

    # 2. Mapiramo rezultate u listu rječnika
    mapped_tags = [
        {"id": r.id, "name": r.name, "usage_count": r.usage_count} 
        for r in results
    ]

    # 3. Izračunamo prosjek usage_count-a u Pythonu (operacija od 0.01ms)
    total_usage = sum(tag["usage_count"] for tag in mapped_tags)
    average_usage = total_usage / len(mapped_tags)

    # 4. Filtriramo samo one koji su STROGO iznad prosjeka
    filtered_tags = [tag for tag in mapped_tags if tag["usage_count"] > average_usage]

    return filtered_tags