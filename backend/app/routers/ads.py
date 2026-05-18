from typing import Optional, List
from datetime import datetime, date
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from pydantic import BaseModel
from app.models.ads_model import Ad, AdStatus, AdType
from app.database import get_session

router = APIRouter(prefix="/ads", tags=["Ads"])


@router.get("/", response_model=List[Ad])
def get_ads(
    type: Optional[AdType] = Query(default=None),
    status: Optional[AdStatus] = Query(default=None),
    field: Optional[str] = Query(default=None),
    location: Optional[str] = Query(default=None),
    company_id: Optional[int] = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    """Return a list of ads. Supports filtering and pagination."""
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

    query = query.limit(limit)
    return session.exec(query).all()


@router.get("/{ad_id}", response_model=Ad)
def get_ad(
    ad_id: int,
    session: Session = Depends(get_session),
    current_user: TokenData = Depends(get_current_user),
):
    """Return a single ad by ID.
    Admins can see deleted ads, regular users cannot."""
    ad = session.get(Ad, ad_id)

    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found.")

    if ad.is_deleted and current_user.role != "admin":
        raise HTTPException(status_code=404, detail="Ad not found.")

    return ad


@router.post("/", response_model=Ad, status_code=201)
def create_ad(data: AdCreate, session: Session = Depends(get_session)):
    """Create a new ad. Status is automatically set to 'pending'."""
    ad = Ad(**data.model_dump())
    session.add(ad)
    session.commit()
    session.refresh(ad)
    return ad


@router.put("/{ad_id}", response_model=Ad)
def update_ad(
    ad_id: int,
    data: AdUpdate,
    session: Session = Depends(get_session),
):
    """Full update of an ad (all fields must be provided)."""
    ad = session.get(Ad, ad_id)
    if not ad or ad.is_deleted:
        raise HTTPException(status_code=404, detail="Ad not found.")

    for field, value in data.model_dump().items():
        setattr(ad, field, value)

    ad.updated_at = datetime.utcnow()
    session.add(ad)
    session.commit()
    session.refresh(ad)
    return ad


@router.patch("/{ad_id}", response_model=Ad)
def patch_ad(
    ad_id: int,
    data: AdPatch,
    session: Session = Depends(get_session),
):
    """Partial update of an ad (only provided fields are changed)."""
    ad = session.get(Ad, ad_id)
    if not ad or ad.is_deleted:
        raise HTTPException(status_code=404, detail="Ad not found.")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ad, field, value)

    if data.status == AdStatus.changes_requested:
        ad.changes_requested_at = datetime.utcnow()

    ad.updated_at = datetime.utcnow()
    session.add(ad)
    session.commit()
    session.refresh(ad)
    return ad


@router.delete("/{ad_id}", status_code=204)
def delete_ad(ad_id: int, session: Session = Depends(get_session)):
    """Soft-delete an ad (sets is_deleted=True, does not remove from database)."""
    ad = session.get(Ad, ad_id)
    if not ad or ad.is_deleted:
        raise HTTPException(status_code=404, detail="Ad not found.")

    ad.is_deleted = True
    ad.updated_at = datetime.utcnow()
    session.add(ad)
    session.commit()


@router.patch("/{ad_id}/status", response_model=Ad)
def update_status(
    ad_id: int,
    data: StatusUpdate,
    session: Session = Depends(get_session),
):
    """Admin endpoint for changing ad status (approve, reject, etc.)."""
    ad = session.get(Ad, ad_id)
    if not ad or ad.is_deleted:
        raise HTTPException(status_code=404, detail="Ad not found.")

    ad.status = data.status
    if data.admin_comment is not None:
        ad.admin_comment = data.admin_comment
    if data.approved_by is not None:
        ad.approved_by = data.approved_by
    if data.status == AdStatus.changes_requested:
        ad.changes_requested_at = datetime.utcnow()

    ad.updated_at = datetime.utcnow()
    session.add(ad)
    session.commit()
    session.refresh(ad)
    return ad