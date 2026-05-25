from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.activity_log import ActivityLog, ActivityListResponse, ActivityResponse

router = APIRouter(prefix="/api/users/me", tags=["activity"])

@router.get("/activity", response_model=ActivityListResponse)
def get_my_activity(
    limit: int = Query(default=3, le=20),
    offset: int = Query(default=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(ActivityLog).filter(
        ActivityLog.user_id == current_user.id
    ).order_by(ActivityLog.created_at.desc())

    total = query.count()
    items = query.offset(offset).limit(limit).all()

    return ActivityListResponse(
        items=items,
        total=total,
        has_more=offset + limit < total
    )