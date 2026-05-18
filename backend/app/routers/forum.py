from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from typing import List, Dict, Any

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User

from app.models.forum import ForumCategory, ForumTopic

router = APIRouter(prefix="/forum", tags=["forum"])

@router.get("/categories", response_model=List[Dict[str, Any]])

#Dohvat kategorija i broja tema za svaku kategoriju

@router.get("/categories", response_model=List[Dict[str, Any]])
def get_categories_with_topic_count(db: Session = Depends(get_db)):

    statement = (
        select(
            ForumCategory.id,
            ForumCategory.name,
            ForumCategory.color,
            ForumCategory.description,
            func.count(ForumTopic.id).label("topic_count")
        )
        .join(ForumTopic, ForumTopic.category_id == ForumCategory.id, isouter=True)

        .where((ForumTopic.is_deleted == False) | (ForumTopic.id == None))
        .group_by(ForumCategory.id)
    )
    
    results = db.exec(statement).all()
    
    output = []
    for row in results:
        output.append({
            "id": row.id,
            "name": row.name,
            "color": row.color,
            "description": row.description,
            "topic_count": row.topic_count
        })
        
    return output

#Dohvat svih aktivnih tema
@router.get("/topics", response_model=List[ForumTopic])
def get_all_topics(db: Session = Depends(get_db)):

    statement = select(ForumTopic).where(ForumTopic.is_deleted == False).order_by(ForumTopic.created_at.desc())
    topics = db.exec(statement).all()
    return topics