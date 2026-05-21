from typing import Optional, List
from datetime import datetime, date, timezone
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select, or_

from app.models.ad import Ad, AdStatus, AdType, AdCreate, AdUpdate, AdPatch, StatusUpdate
from app.models.user import User, UserRole
from app.core.security import get_current_user
from app.database import get_db

router = APIRouter(prefix="/ads", tags=["Ads"])

@router.get("/", response_model=List[Ad])
def get_ads(
    type: Optional[AdType] = Query(default=None),
    status: Optional[AdStatus] = Query(default=None),
    field: Optional[str] = Query(default=None),
    location: Optional[str] = Query(default=None),
    company_id: Optional[int] = Query(default=None),
    search: Optional[str] = Query(default=None, description="Search by title or description"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=200),
    session: Session = Depends(get_db),
):
    query = select(Ad).where(Ad.is_deleted == False)

    if type:
        query = query.where(Ad.type == type)
    if status:
        query = query.where(Ad.status == status)
    if field:
        query = query.where(Ad.field == field)
    if location:
        query = query.where(Ad.location == location)
    if company_id:
        query = query.where(Ad.company_id == company_id)
    if search:
        search_filter = f"%{search}%"
        query = query.where(
            or_(
                Ad.title.ilike(search_filter),
                Ad.description.ilike(search_filter),
            )
        )

    query = query.offset(skip).limit(limit)
    return session.exec(query).all()



@router.get("/{ad_id}", response_model=Ad)
def get_ad(ad_id: int, session: Session = Depends(get_db)):
    """Get a single ad by ID."""
    ad = session.get(Ad, ad_id)
    if not ad or ad.is_deleted:
        raise HTTPException(status_code=404, detail="Ad not found.")
    return ad



@router.post("/", response_model=Ad, status_code=201)
def create_ad(data: AdCreate, session: Session = Depends(get_db)):
    """Create a new ad. Status is automatically 'pending'."""
    ad = Ad(**data.model_dump())
    session.add(ad)
    session.commit()
    session.refresh(ad)
    return ad



@router.put("/{ad_id}", response_model=Ad)
def update_ad(
    ad_id: int,
    data: AdUpdate,
    session: Session = Depends(get_db),
):
    ad = session.get(Ad, ad_id)
    if not ad or ad.is_deleted:
        raise HTTPException(status_code=404, detail="Ad not found.")

    for field, value in data.model_dump().items():
        setattr(ad, field, value)

    ad.updated_at = datetime.now(timezone.utc)
    session.add(ad)
    session.commit()
    session.refresh(ad)
    return ad



@router.patch("/{ad_id}", response_model=Ad)
def patch_ad(
    ad_id: int,
    data: AdPatch,
    session: Session = Depends(get_db),
):
    ad = session.get(Ad, ad_id)
    if not ad or ad.is_deleted:
        raise HTTPException(status_code=404, detail="Ad not found.")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ad, field, value)

    if data.status == AdStatus.changes_requested:
        ad.changes_requested_at = datetime.now(timezone.utc)

    ad.updated_at = datetime.now(timezone.utc)
    session.add(ad)
    session.commit()
    session.refresh(ad)
    return ad


@router.delete("/{ad_id}", status_code=204)
def delete_ad(ad_id: int, session: Session = Depends(get_db)):
    ad = session.get(Ad, ad_id)
    if not ad or ad.is_deleted:
        raise HTTPException(status_code=404, detail="Ad not found.")

    ad.is_deleted = True
    ad.updated_at = datetime.now(timezone.utc)
    session.add(ad)
    session.commit()



@router.patch("/{ad_id}/status", response_model=Ad)
def update_status(
    ad_id: int,
    data: StatusUpdate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Permission denied.")

    ad = session.get(Ad, ad_id)
    if not ad or ad.is_deleted:
        raise HTTPException(status_code=404, detail="Ad not found.")

    ad.status = data.status
    if data.admin_comment is not None:
        ad.admin_comment = data.admin_comment
    if data.approved_by is not None:
        ad.approved_by = data.approved_by
    if data.status == AdStatus.changes_requested:
        ad.changes_requested_at = datetime.now(timezone.utc)

    ad.updated_at = datetime.now(timezone.utc)
    session.add(ad)
    session.commit()
    session.refresh(ad)
    return ad