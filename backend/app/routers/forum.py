from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from typing import List, Dict, Any

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User

from app.models.forum import ForumCategory, ForumTopic

router = APIRouter(prefix="/forum", tags=["forum"])


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

@router.get("/topics", response_model=Dict[str, Any]) # Vraćamo rječnik koji sadrži teme i ukupan broj
def get_all_topics(
    db: Session = Depends(get_db),
    category_id: Optional[int] = None,
    page: int = 1,  # Defaultno prva stranica
    size: int = 5   # Defaultno 5 tema po stranici
):
    # 1. Osnovni upit za teme
    statement = (
        select(ForumTopic, ForumCategory.name.label("category_name"))
        .join(ForumCategory, ForumTopic.category_id == ForumCategory.id)
        .where(ForumTopic.is_deleted == False)
    )
    
    # 2. Osnovni upit za brojanje UKUPNOG broja tema (treba nam da znamo ima li još stranica)
    count_statement = select(func.count(ForumTopic.id)).where(ForumTopic.is_deleted == False)

    # Ako je poslat category_id, filtriramo oba upita
    if category_id is not None:
        statement = statement.where(ForumTopic.category_id == category_id)
        count_statement = count_statement.where(ForumTopic.category_id == category_id)
        
    # Dobijamo ukupan broj filtriranih tema iz baze
    total_topics = db.exec(count_statement).one()

    # 3. IMPLEMENTACIJA PAGINACIJE (Računamo koliko preskačemo)
    skip = (page - 1) * size
    statement = statement.order_by(ForumTopic.created_at.desc()).offset(skip).limit(size)
    
    results = db.exec(statement).all()
    
    topics_list = []
    for topic, category_name in results:
        topic_dict = topic.model_dump()
        topic_dict["category_name"] = category_name
        topics_list.append(topic_dict)
        
    # Vraćamo podatke struktuirano
    return {
        "items": topics_list,     
        "total": total_topics,     
        "page": page,
        "size": size
    }