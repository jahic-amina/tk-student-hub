from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from typing import Optional, List, Dict, Any

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



@router.get("/topics", response_model=Dict[str, Any])
def get_all_topics(
    db: Session = Depends(get_db),
    category_id: Optional[int] = None,  # <-- PROVJERI: Mora biti tačno category_id
    page: int = 1,
    size: int = 5
):
    # 1. Osnovni upit za dovlačenje tema i naziva kategorije
    statement = (
        select(ForumTopic, ForumCategory.name.label("category_name"))
        .join(ForumCategory, ForumTopic.category_id == ForumCategory.id)
        .where(ForumTopic.is_deleted == False)
    )
    
    # 2. Osnovni upit za brojanje ukupnog broja zapisa
    count_statement = select(func.count(ForumTopic.id)).where(ForumTopic.is_deleted == False)

    # 3. FILTRIRANJE: Ako je proslijeđen category_id, OBA upita filtriramo u bazi!
    if category_id is not None:
        statement = statement.where(ForumTopic.category_id == category_id)
        count_statement = count_statement.where(ForumTopic.category_id == category_id)
        
    # Uzimamo ukupan broj tema za OVAL FILTER (bitno za ispravan broj stranica na frontendu)
    total_topics = db.exec(count_statement).one()

    # 4. PAGINACIJA
    skip = (page - 1) * size
    statement = statement.order_by(ForumTopic.created_at.desc()).offset(skip).limit(size)
    
    results = db.exec(statement).all()
    
    topics_list = []
    for topic, category_name in results:
        topic_dict = topic.model_dump()
        topic_dict["category_name"] = category_name
        topics_list.append(topic_dict)
        
    return {
        "items": topics_list,
        "total": total_topics,
        "page": page,
        "size": size
    }