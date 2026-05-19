from fastapi import APIRouter, Depends, HTTPException, status
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

router = APIRouter(prefix="/forum", tags=["forum"])

# -------------------------------------------------------
# Team 3 — Forum
# This is your router. All your endpoints go here.
#
# Example protected endpoint:
#
# @router.get("/")
# def get_posts(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return {"message": "your code here"}
#
# -------------------------------------------------------

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
