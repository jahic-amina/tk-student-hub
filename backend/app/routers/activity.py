from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, func
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.activity_log import ActivityLog, ActivityListResponse, ActivityResponse
from app.enums.activity import ActivityType

router = APIRouter(prefix="/api/users/me", tags=["activity"])


@router.get("/activity", response_model=ActivityListResponse)
def get_my_activity(
    limit: int = Query(default=3, le=20),
    offset: int = Query(default=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    base = select(ActivityLog).where(ActivityLog.user_id == current_user.id)

    total = db.exec(
        select(func.count(ActivityLog.id)).where(ActivityLog.user_id == current_user.id)
    ).one()

    items = db.exec(
        base.order_by(ActivityLog.created_at.desc()).offset(offset).limit(limit)
    ).all()

    return ActivityListResponse(
        items=items,
        total=total,
        has_more=offset + limit < total,
    )
