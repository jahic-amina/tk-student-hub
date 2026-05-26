from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from typing import List, Dict, Any

from app.database import get_db
from app.models.forum import ForumCategory, ForumTopic

router = APIRouter(prefix="/forum/categories", tags=["Forum Categories"])

# Sheme
#...


# Pomocne funkcije

def get_category_data(db: Session, category_id: int) -> dict:
    category = db.get(ForumCategory, category_id)
    if not category:
        return {"id": None, "name": "Bez kategorije", "color": "#6b7280"}
    return {"id": category.id, "name": category.name, "color": category.color}

# Rute za kategorije

@router.get("/", response_model=List[Dict[str, Any]])
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