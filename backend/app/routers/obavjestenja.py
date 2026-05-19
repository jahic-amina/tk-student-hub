from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.database import get_db  
from app.models.obavjestenja import (
    Notification,
    NotificationCreate,
    NotificationUpdate
)

router = APIRouter(
    prefix="/obavjestenja",
    tags=["Obavještenja"]
)

@router.post("/", response_model=Notification, status_code=status.HTTP_201_CREATED)
def create_notification(notification: NotificationCreate, session: Session = Depends(get_db)):
    db_notification = Notification.model_validate(notification)
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    return db_notification


@router.get("/user/{user_id}", response_model=List[Notification])
def get_user_notifications(user_id: int, session: Session = Depends(get_db)): 
    statement = select(Notification).where(Notification.user_id == user_id)
    notifications = session.exec(statement).all()
    return notifications


@router.get("/{notification_id}", response_model=Notification)
def get_notification(notification_id: int, session: Session = Depends(get_db)):
    db_notification = session.get(Notification, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Obavještenje nije pronađeno")
    return db_notification


@router.patch("/{notification_id}", response_model=Notification)
def update_notification(
    notification_id: int, 
    notification_data: NotificationUpdate, 
    session: Session = Depends(get_db) 
):
    db_notification = session.get(Notification, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Obavještenje nije pronađeno")
    
    obj_data = notification_data.model_dump(exclude_unset=True)
    
    for key, value in obj_data.items():
        setattr(db_notification, key, value)
        
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    return db_notification


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(notification_id: int, session: Session = Depends(get_db)):
    db_notification = session.get(Notification, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Obavještenje nije pronađeno")
    
    session.delete(db_notification)
    session.commit()
    return None