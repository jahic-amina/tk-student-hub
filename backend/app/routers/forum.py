from fastapi import APIRouter, Depends, HTTPException, status
<<<<<<< HEAD
from sqlmodel import Session, select, func
from typing import Optional, List, Dict, Any

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole

from app.models.forum import ForumCategory, ForumTopic
=======
from sqlmodel import Session, select
from typing import List
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.forum import (
    ForumCategory,
    ForumTopic,
    ForumTopicCreate,
    ForumTopicRead,
    ForumTag,
    ForumTopicTag,
    ForumComment,
    ForumCommentCreate,
    ForumCommentRead,
)   
>>>>>>> origin/tim3/forum/kreiranje-teme

router = APIRouter(prefix="/forum", tags=["forum"])


<<<<<<< HEAD
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

@router.delete("/topics/{id}", status_code=status.HTTP_200_OK)
def delete_topic(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Samo admin može brisati teme
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Samo administrator može obrisati temu."
        )

    # Pronađi temu u bazi
    topic = db.get(ForumTopic, id)

    if not topic or topic.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tema nije pronađena."
        )

    # Soft delete - tema nestaje iz svih GET prikaza
    topic.is_deleted = True

    db.add(topic)
    db.commit()
    db.refresh(topic)

    return {
        "message": "Tema je uspješno obrisana.",
        "topic_id": id
    }
=======
@router.get("/")
def forum_placeholder():
    return {"message": "Forum router is working — Team 3 builds here"}

@router.get("/topics", response_model=List[ForumTopicRead])
def list_forum_topics(db: Session = Depends(get_db)):
    topics = db.exec(select(ForumTopic)).all()
    return topics

@router.post("/topics", response_model=ForumTopicRead, status_code=status.HTTP_201_CREATED)
def create_forum_topic(
    topic_data: ForumTopicCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Provjera da li kategorija postoji
    category = db.get(ForumCategory, topic_data.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Kategorija nije pronađena.")

    # Kreiranje nove teme
    new_topic = ForumTopic(
        title=topic_data.title,
        content=topic_data.content,
        category_id=topic_data.category_id,
        user_id=current_user.id
    )
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)

    # Dodavanje tagova ako su navedeni
    tags = []
    if topic_data.tags:
        for tag_id in topic_data.tags:
            tag = db.get(ForumTag, tag_id)
            if tag:
                topic_tag = ForumTopicTag(topic_id=new_topic.id, tag_id=tag_id)
                db.add(topic_tag)
                tags.append(tag.name)
    db.commit()
    db.refresh(new_topic)

    return new_topic

@router.post("/comments", response_model=ForumCommentRead, status_code=status.HTTP_201_CREATED)
def create_forum_comment(
    comment_data: ForumCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    #Provjera da li tema postoji
    topic = db.get(ForumTopic, comment_data.topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")

    #Kreiranje novog komentara
    new_comment = ForumComment(
        content=comment_data.content,
        topic_id=comment_data.topic_id,
        user_id=current_user.id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

@router.get("/topics/{topic_id}/comments", response_model=List[ForumCommentRead])
def get_comments(
    topic_id: int,
    db: Session = Depends(get_db)
):
    comments = db.exec(select(ForumComment).where(ForumComment.topic_id == topic_id)).all()
    return comments
>>>>>>> origin/tim3/forum/kreiranje-teme
