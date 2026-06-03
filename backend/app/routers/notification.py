from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, delete
from typing import List
from app.database import get_db 
from app.models.notification import (
    Notification,
    NotificationCreate,
    NotificationUpdate
)
from app.models.user import User, UserRole
from app.models.company import Company
from app.core.security import oauth2_scheme, decode_access_token

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

def get_current_actor(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if not payload:
        raise credentials_exception
        
    sub = payload.get("sub")
    role = payload.get("role")
    
    if not sub:
        raise credentials_exception
        
    if "@" in str(sub):
        user = session.exec(select(User).where(User.email == str(sub))).first()
        if user:
            return user
        company = session.exec(select(Company).where(Company.email == str(sub))).first()
        if company:
            return company
        raise credentials_exception

    try:
        sub_id = int(sub)
    except (ValueError, TypeError):
        raise credentials_exception

    if role == "company":
        company = session.exec(select(Company).where(Company.id == sub_id)).first()
        if company:
            return company
            
    if role and ("admin" in str(role).lower() or "student" in str(role).lower()):
        user = session.exec(select(User).where(User.id == sub_id)).first()
        if user:
            return user

    user = session.exec(select(User).where(User.id == sub_id)).first()
    if user:
        return user
        
    company = session.exec(select(Company).where(Company.id == sub_id)).first()
    if company:
        return company

    raise credentials_exception


@router.post("/", response_model=Notification, status_code=status.HTTP_201_CREATED)
def create_notification(
    notification: NotificationCreate, 
    session: Session = Depends(get_db),
    current_actor = Depends(get_current_actor)
):
    if not current_actor or not isinstance(current_actor, User) or current_actor.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have permission to create notifications."
        )
        
    db_notification = Notification(**notification.model_dump())
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    return db_notification


@router.get("/me", response_model=List[Notification])
def get_my_notifications(
    session: Session = Depends(get_db),
    current_actor = Depends(get_current_actor)
):
    statement = select(Notification)
    if isinstance(current_actor, User):
        statement = statement.where(Notification.user_id == current_actor.id)
    else:
        statement = statement.where(Notification.company_id == current_actor.id)
        
    statement = statement.order_by(Notification.is_read.asc(), Notification.created_at.desc())
    return session.exec(statement).all()


@router.api_route("/read-all", methods=["POST", "PATCH", "PUT"], status_code=status.HTTP_200_OK)
def mark_all_as_read(
    session: Session = Depends(get_db),
    current_actor = Depends(get_current_actor)
):
    statement = select(Notification).where(Notification.is_read == False)
    if isinstance(current_actor, User):
        statement = statement.where(Notification.user_id == current_actor.id)
    else:
        statement = statement.where(Notification.company_id == current_actor.id)
        
    unread_notifications = session.exec(statement).all()
    for notification in unread_notifications:
        notification.is_read = True
        session.add(notification)
        
    session.commit()
    return {"detail": "All notifications marked as read."}


@router.api_route("/{notification_id}/read", methods=["POST", "PATCH", "PUT"], status_code=status.HTTP_200_OK)
def mark_single_as_read_path(
    notification_id: int,
    session: Session = Depends(get_db),
    current_actor = Depends(get_current_actor)
):
    db_notification = session.get(Notification, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found.")
        
    db_notification.is_read = True
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    return db_notification


@router.delete("/clear-all", status_code=status.HTTP_204_NO_CONTENT)
def clear_all_notifications(
    session: Session = Depends(get_db),
    current_actor = Depends(get_current_actor)
):
    if isinstance(current_actor, User):
        statement = delete(Notification).where(Notification.user_id == current_actor.id)
    else:
        statement = delete(Notification).where(Notification.company_id == current_actor.id)
        
    session.exec(statement)
    session.commit()
    return None


@router.get("/{notification_id}", response_model=Notification)
def get_notification(
    notification_id: int, 
    session: Session = Depends(get_db),
    current_actor = Depends(get_current_actor)
):
    db_notification = session.get(Notification, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found.")
    return db_notification


@router.patch("/{notification_id}", response_model=Notification)
def update_notification(
    notification_id: int, 
    notification_data: NotificationUpdate, 
    session: Session = Depends(get_db),
    current_actor = Depends(get_current_actor)
):
    db_notification = session.get(Notification, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found.")
    
    obj_data = notification_data.model_dump(exclude_unset=True)
    for key, value in obj_data.items():
        setattr(db_notification, key, value)
        
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    return db_notification


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
    notification_id: int, 
    session: Session = Depends(get_db),
    current_actor = Depends(get_current_actor)
):
    db_notification = session.get(Notification, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found.")
    
    session.delete(db_notification)
    session.commit()
    return None