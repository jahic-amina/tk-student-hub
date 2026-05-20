<<<<<<< HEAD
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
=======
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlmodel import Session, select

>>>>>>> origin/tim3/forum/detaljna-tema
from app.database import get_db
from app.models.user import User
from app.models.forum import (
    ForumCategory,
    ForumTopic,
<<<<<<< HEAD
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

=======
    ForumComment,
    ForumCommentVote,
    ForumTag,
    ForumTopicTag,
)

router = APIRouter(prefix="/forum", tags=["forum"])


def make_summary(text: str, max_length: int = 150) -> str:
    clean_text = " ".join((text or "").split())

    if len(clean_text) <= max_length:
        return clean_text

    return clean_text[:max_length].rsplit(" ", 1)[0] + "..."


def get_author_data(db: Session, user_id: int) -> dict:
    user = db.get(User, user_id)

    if not user:
        return {
            "id": None,
            "full_name": "Nepoznat korisnik",
        }

    return {
        "id": user.id,
        "full_name": user.full_name,
    }


def get_category_data(db: Session, category_id: int) -> dict:
    category = db.get(ForumCategory, category_id)

    if not category:
        return {
            "id": None,
            "name": "Bez kategorije",
            "color": "#6b7280",
        }

    return {
        "id": category.id,
        "name": category.name,
        "color": category.color,
    }


def get_topic_tags(db: Session, topic_id: int) -> list[str]:
    links = db.exec(
        select(ForumTopicTag).where(ForumTopicTag.topic_id == topic_id)
    ).all()

    tag_names = []

    for link in links:
        tag = db.get(ForumTag, link.tag_id)

        if tag:
            tag_names.append(tag.name)

    return tag_names


def get_comment_votes_count(db: Session, comment_id: int) -> int:
    result = db.exec(
        select(func.coalesce(func.sum(ForumCommentVote.value), 0)).where(
            ForumCommentVote.comment_id == comment_id
        )
    ).one()

    return int(result or 0)


def get_topic_comments(db: Session, topic_id: int) -> list[dict]:
    comments = db.exec(
        select(ForumComment).where(
            ForumComment.topic_id == topic_id,
            ForumComment.is_deleted == False,
        )
    ).all()

    comment_items = []

    for comment in comments:
        votes_count = get_comment_votes_count(db, comment.id)

        comment_items.append(
            {
                "id": comment.id,
                "content": comment.content,
                "is_best_answer": comment.is_best_answer,
                "created_at": comment.created_at,
                "updated_at": comment.updated_at,
                "votes_count": votes_count,
                "author": get_author_data(db, comment.user_id),
            }
        )

    comment_items.sort(
        key=lambda item: (
            not item["is_best_answer"],
            -item["votes_count"],
            item["created_at"],
        )
    )

    return comment_items


def get_comments_count(db: Session, topic_id: int) -> int:
    result = db.exec(
        select(func.count(ForumComment.id)).where(
            ForumComment.topic_id == topic_id,
            ForumComment.is_deleted == False,
        )
    ).one()

    return int(result or 0)


def get_topic_votes_count(db: Session, topic_id: int) -> int:
    comments = db.exec(
        select(ForumComment).where(
            ForumComment.topic_id == topic_id,
            ForumComment.is_deleted == False,
        )
    ).all()

    total = 0

    for comment in comments:
        total += get_comment_votes_count(db, comment.id)

    return total


def has_best_answer(db: Session, topic_id: int) -> bool:
    best_answer = db.exec(
        select(ForumComment).where(
            ForumComment.topic_id == topic_id,
            ForumComment.is_deleted == False,
            ForumComment.is_best_answer == True,
        )
    ).first()

    return best_answer is not None


def build_topic_list_item(db: Session, topic: ForumTopic) -> dict:
    comments_count = get_comments_count(db, topic.id)

    return {
        "id": topic.id,
        "title": topic.title,
        "summary": make_summary(topic.content),
        "views_count": topic.views_count,
        "comments_count": comments_count,
        "answers_count": comments_count,
        "created_at": topic.created_at,
        "updated_at": topic.updated_at,
        "author": get_author_data(db, topic.user_id),
        "category": get_category_data(db, topic.category_id),
        "tags": get_topic_tags(db, topic.id),
        "has_best_answer": has_best_answer(db, topic.id),
    }

>>>>>>> origin/tim3/forum/detaljna-tema

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
<<<<<<< HEAD
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
=======
def forum_root():
    return {"message": "Forum router radi"}


@router.get("/topics")
def get_topics(
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    statement = select(ForumTopic).where(ForumTopic.is_deleted == False)

    if search and search.strip():
        search_value = f"%{search.strip()}%"
        statement = statement.where(
            (ForumTopic.title.ilike(search_value))
            | (ForumTopic.content.ilike(search_value))
        )

    statement = statement.order_by(ForumTopic.created_at.desc())

    topics = db.exec(statement).all()

    return [
        build_topic_list_item(db, topic)
        for topic in topics
    ]


@router.patch("/topics/{topic_id}/view")
def increment_topic_view(topic_id: int, db: Session = Depends(get_db)):
    topic = db.get(ForumTopic, topic_id)

    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")

    topic.views_count += 1

    db.add(topic)
    db.commit()
    db.refresh(topic)

    return {
        "id": topic.id,
        "views_count": topic.views_count,
    }


@router.get("/topics/{topic_id}")
def get_topic_details(topic_id: int, db: Session = Depends(get_db)):
    topic = db.get(ForumTopic, topic_id)

    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")

    comments = get_topic_comments(db, topic.id)
    comments_count = len(comments)
    votes_count = get_topic_votes_count(db, topic.id)

    return {
        "id": topic.id,
        "title": topic.title,
        "content": topic.content,
        "views_count": topic.views_count,
        "is_locked": topic.is_locked,
        "created_at": topic.created_at,
        "updated_at": topic.updated_at,
        "author": get_author_data(db, topic.user_id),
        "category": get_category_data(db, topic.category_id),
        "tags": get_topic_tags(db, topic.id),
        "comments": comments,
        "stats": {
            "comments_count": comments_count,
            "answers_count": comments_count,
            "views_count": topic.views_count,
            "votes_count": votes_count,
            "has_best_answer": any(comment["is_best_answer"] for comment in comments),
        },
    }
>>>>>>> origin/tim3/forum/detaljna-tema
