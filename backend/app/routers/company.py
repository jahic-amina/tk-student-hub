from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from app.database import get_db
from app.models.company import Company, CompanyStatus
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.get("/", response_model=List[Company])
def get_companies(
    with_deleted: Optional[bool] = Query(default=None),
    with_pending: Optional[bool] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if (with_deleted is not None or with_pending is not None) and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission for this.",
        )

    query = select(Company)

    query = query.where(Company.status != CompanyStatus.denied)
    if not with_deleted:
        query = query.where(Company.is_deleted == False)
    if not with_pending:
        query = query.where(Company.status != CompanyStatus.pending)

    return db.exec(query).all()