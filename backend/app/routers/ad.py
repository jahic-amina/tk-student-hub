from typing import Optional, List
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlmodel import Session, select, or_
from app.models.ad import Ad, AdStatus, AdType, AdCreate, AdUpdate, AdPatch, StatusUpdate, AdRead
from app.models.user import User, UserRole
from app.core.security import get_current_user
from app.database import get_db
from app.models.company import Company 
from app.core.security import get_current_company
from app.models.notification import Notification, NotificationType

router = APIRouter(prefix="/ads", tags=["Ads"])

def expire_if_deadline_passed(ad: Ad, db: Session) -> None:
    """Automatski postavlja oglas na expired ako je deadline prošao."""
    from datetime import date
    if ad.status == AdStatus.active and ad.deadline < date.today():
        ad.status = AdStatus.expired
        ad.updated_at = datetime.now(timezone.utc)
        db.add(ad)
        db.commit()

def ad_to_read(ad: Ad) -> AdRead:
    """Helper function to convert Ad to AdRead with company_name and approver_name."""
    return AdRead(
        id=ad.id,
        company_id=ad.company_id,
        company_name=ad.company.company_name if ad.company else None,
        approved_by=ad.approved_by,
        approver_name=ad.approver.full_name if ad.approver else None,
        title=ad.title,
        type=ad.type,
        field=ad.field,
        location=ad.location,
        description=ad.description,
        deadline=ad.deadline,
        duration_months=ad.duration_months,
        compensation=ad.compensation,
        currency=ad.currency,
        spots=ad.spots,
        requirements=ad.requirements,
        benefits=ad.benefits,
        admin_comment=ad.admin_comment,
        changes_requested_at=ad.changes_requested_at,
        status=ad.status,
        is_deleted=ad.is_deleted,
        created_at=ad.created_at,
        updated_at=ad.updated_at,
    )


@router.get("/", response_model=List[AdRead])
def get_ads(
    type: Optional[AdType] = Query(default=None),
    field: Optional[str] = Query(default=None),
    location: Optional[str] = Query(default=None),
    company_id: Optional[int] = Query(default=None),
    search: Optional[str] = Query(default=None, description="Search by title or description"),
    db: Session = Depends(get_db),
):
    query = select(Ad).where(Ad.is_deleted == False, Ad.status == AdStatus.active)

    if type:
        query = query.where(Ad.type == type)
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

    ads = db.exec(query).all()
    # Run expiry check after fetching — committed lazily per-ad
    for ad in ads:
        expire_if_deadline_passed(ad, db)
    return [ad_to_read(ad) for ad in ads]


@router.get("/admin/list", response_model=List[AdRead])
def get_ads_admin(
    ad_status: Optional[AdStatus] = Query(default=None),
    type: Optional[AdType] = Query(default=None),
    field: Optional[str] = Query(default=None),
    location: Optional[str] = Query(default=None),
    company_id: Optional[int] = Query(default=None),
    search: Optional[str] = Query(default=None, description="Search by title or description"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied.")
    
    query = select(Ad)
    
    if ad_status:
        query = query.where(Ad.status == ad_status)
    if type:
        query = query.where(Ad.type == type)
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

    ads = db.exec(query).all()
    return [ad_to_read(ad) for ad in ads]


@router.get("/{ad_id}", response_model=AdRead)
def get_ad(ad_id: int, db: Session = Depends(get_db)):
    ad = db.get(Ad, ad_id)
    if not ad or ad.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ad not found.")
    expire_if_deadline_passed(ad, db)
    return ad_to_read(ad)


@router.post("/", response_model=AdRead, status_code=status.HTTP_201_CREATED)
def create_ad(
    data: AdCreate, 
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)  
):
    ad_data = data.model_dump()
    ad_data["company_id"] = current_company.id
    
    ad = Ad(**ad_data)
    db.add(ad)
    db.flush()  
    
    admini = db.exec(select(User).where(User.role == UserRole.admin)).all()
    for admin in admini:
        tekst = f"Kompanija '{current_company.company_name}' je objavila novi oglas '{ad.title}' koji čeka odobrenje."
        db.add(Notification(user_id=admin.id, text=tekst, type=NotificationType.NEW_OPPORTUNITY))

    db.commit()
    db.refresh(ad)
    return ad_to_read(ad)


@router.put("/{ad_id}", response_model=AdRead)
def update_ad(
    ad_id: int,
    data: AdUpdate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):
    ad = db.get(Ad, ad_id)
    if not ad or ad.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ad not found.")

    if ad.company_id != current_company.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied.")

    for field, value in data.model_dump().items():
        setattr(ad, field, value)

    ad.updated_at = datetime.now(timezone.utc)
    db.add(ad)
    db.commit()
    db.refresh(ad)
    return ad_to_read(ad)


@router.patch("/{ad_id}", response_model=AdRead)
def patch_ad(
    ad_id: int,
    data: AdPatch,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):
    ad = db.get(Ad, ad_id)
    if not ad or ad.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ad not found.")

    if ad.company_id != current_company.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied.")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ad, field, value)

    ad.updated_at = datetime.now(timezone.utc)
    db.add(ad)
    db.commit()
    db.refresh(ad)
    return ad_to_read(ad)


@router.patch("/{ad_id}/status", response_model=AdRead)
def update_status(
    ad_id: int,
    data: StatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied.")

    ad = db.get(Ad, ad_id)
    if not ad or ad.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ad not found.")

    stari_status = ad.status
    ad.status = data.status
    if data.admin_comment is not None:
        ad.admin_comment = data.admin_comment
    if data.approved_by is not None:
        ad.approved_by = data.approved_by
    if data.status == AdStatus.changes_requested:
        ad.changes_requested_at = datetime.now(timezone.utc)

    ad.updated_at = datetime.now(timezone.utc)
    db.add(ad)

    if stari_status != data.status:
        if data.status == AdStatus.active:
            tekst = f"Vaš oglas '{ad.title}' je odobren i sada je vidljiv studentima."
            db.add(Notification(company_id=ad.company_id, text=tekst, type=NotificationType.STATUS_CHANGE))
        elif data.status == AdStatus.rejected or data.status == AdStatus.changes_requested:
            komentar = f" Razlog: {data.admin_comment}" if data.admin_comment else ""
            tekst = f"Vaš oglas '{ad.title}' je odbijen ili vraćen na doradu.{komentar}"
            db.add(Notification(company_id=ad.company_id, text=tekst, type=NotificationType.STATUS_CHANGE))

    db.commit()
    db.refresh(ad)
    return ad_to_read(ad)


@router.delete("/{ad_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ad(
    ad_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):
    ad = db.get(Ad, ad_id)
    if not ad or ad.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ad not found.")

    if ad.company_id != current_company.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied.")

    ad.is_deleted = True
    ad.updated_at = datetime.now(timezone.utc)
    db.add(ad)
    db.commit()


@router.post("/{ad_id}/restore", response_model=AdRead)
def restore_ad(
    ad_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied.")

    ad = db.get(Ad, ad_id)
    if not ad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ad not found.")

    ad.is_deleted = False
    ad.status = AdStatus.pending 
    ad.updated_at = datetime.now(timezone.utc)
    
    db.add(ad)
    db.commit()
    db.refresh(ad)
    return ad_to_read(ad)