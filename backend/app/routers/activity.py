from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
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

@router.post("/activity/test-data")
def create_test_activities(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from datetime import datetime, timedelta
    from app.services.activity_log_service import log_activity

    log_activity(db, current_user.id, ActivityType.material_posted, "React Hooks - Kompletan vodič", "Frontend Development", 1)
    log_activity(db, current_user.id, ActivityType.forum_comment, "Kako optimizovati React aplikaciju?", "Diskusija · 5 odgovora", 2)
    log_activity(db, current_user.id, ActivityType.internship_completed, "Frontend Development Internship", "Tech Corp · 3 meseca", 3)
    log_activity(db, current_user.id, ActivityType.material_uploaded, "TypeScript Best Practices", "Backend Development · PDF", 4)
    log_activity(db, current_user.id, ActivityType.forum_answer, "State management u velikim projektima", "Označeno kao korisno", 5)

    return {"message": "Testne aktivnosti uspješno dodane!"}