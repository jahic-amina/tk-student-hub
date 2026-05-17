from typing import Optional, List
from datetime import datetime, date
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from pydantic import BaseModel

from app.models.ads_model import Oglas, OglasStatus, OglasTip
from app.models.user import User, UserRole
from app.core.security import get_current_user
from app.database import get_db

router = APIRouter(prefix="/oglasi", tags=["Oglasi"])


# Schemas

class OglasCreate(BaseModel):
    kompanija_id: int
    naziv: str
    tip: OglasTip
    oblast: str
    lokacija: str
    opis: str
    rok: date
    trajanje: Optional[str] = None
    naknada: Optional[str] = None
    broj_mjesta: int = 1
    placeno: bool = False
    requirements: Optional[str] = None
    benefits: Optional[str] = None


class OglasUpdate(BaseModel):
    """Full update – PUT (all fields required except those with defaults)."""
    naziv: str
    tip: OglasTip
    oblast: str
    lokacija: str
    opis: str
    rok: date
    trajanje: Optional[str] = None
    naknada: Optional[str] = None
    broj_mjesta: int = 1
    placeno: bool = False
    requirements: Optional[str] = None
    benefits: Optional[str] = None


class OglasPatch(BaseModel):
    """Partial update – PATCH (all fields optional)."""
    naziv: Optional[str] = None
    tip: Optional[OglasTip] = None
    oblast: Optional[str] = None
    lokacija: Optional[str] = None
    opis: Optional[str] = None
    rok: Optional[date] = None
    trajanje: Optional[str] = None
    naknada: Optional[str] = None
    broj_mjesta: Optional[int] = None
    placeno: Optional[bool] = None
    requirements: Optional[str] = None
    benefits: Optional[str] = None


# GET /oglasi  – list (with optional filters)

@router.get("/", response_model=List[Oglas])
def get_oglasi(
    tip: Optional[OglasTip] = Query(default=None),
    status: Optional[OglasStatus] = Query(default=None),
    oblast: Optional[str] = Query(default=None),
    lokacija: Optional[str] = Query(default=None),
    kompanija_id: Optional[int] = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_db),
):
    """Vrati listu oglasa. Podržava filtriranje i paginaciju."""
    query = select(Oglas).where(Oglas.is_deleted == False)

    if tip:
        query = query.where(Oglas.tip == tip)
    if status:
        query = query.where(Oglas.status == status)
    if oblast:
        query = query.where(Oglas.oblast == oblast)
    if lokacija:
        query = query.where(Oglas.lokacija == lokacija)
    if kompanija_id:
        query = query.where(Oglas.kompanija_id == kompanija_id)

    query = query.offset(skip).limit(limit)
    return session.exec(query).all()


# GET /oglasi/{id}  – single oglas

@router.get("/{oglas_id}", response_model=Oglas)
def get_oglas(oglas_id: int, session: Session = Depends(get_db)):
    """Vrati jedan oglas po ID-u."""
    oglas = session.get(Oglas, oglas_id)
    if not oglas or oglas.is_deleted:
        raise HTTPException(status_code=404, detail="Oglas nije pronađen.")
    return oglas


# POST /oglasi  – create

@router.post("/", response_model=Oglas, status_code=201)
def create_oglas(data: OglasCreate, session: Session = Depends(get_db)):
    """Kreiraj novi oglas. Status je automatski 'pending'."""
    oglas = Oglas(**data.model_dump())
    session.add(oglas)
    session.commit()
    session.refresh(oglas)
    return oglas


# PUT /oglasi/{id}  – full update

@router.put("/{oglas_id}", response_model=Oglas)
def update_oglas(
    oglas_id: int,
    data: OglasUpdate,
    session: Session = Depends(get_db),
):
    """Potpuno ažuriranje oglasa (sva polja moraju biti proslijeđena)."""
    oglas = session.get(Oglas, oglas_id)
    if not oglas or oglas.is_deleted:
        raise HTTPException(status_code=404, detail="Oglas nije pronađen.")

    for field, value in data.model_dump().items():
        setattr(oglas, field, value)

    oglas.updated_at = datetime.utcnow()
    session.add(oglas)
    session.commit()
    session.refresh(oglas)
    return oglas


# PATCH /oglasi/{id}  – partial update

@router.patch("/{oglas_id}", response_model=Oglas)
def patch_oglas(
    oglas_id: int,
    data: OglasPatch,
    session: Session = Depends(get_db),
):
    """Djelimično ažuriranje oglasa (samo proslijeđena polja se mijenjaju)."""
    oglas = session.get(Oglas, oglas_id)
    if not oglas or oglas.is_deleted:
        raise HTTPException(status_code=404, detail="Oglas nije pronađen.")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(oglas, field, value)

    # Ako se traže izmjene, zabilježi kada
    if data.status == OglasStatus.changes_requested:
        oglas.changes_requested_at = datetime.utcnow()

    oglas.updated_at = datetime.utcnow()
    session.add(oglas)
    session.commit()
    session.refresh(oglas)
    return oglas


# DELETE /oglasi/{id}  – soft delete

@router.delete("/{oglas_id}", status_code=204)
def delete_oglas(oglas_id: int, session: Session = Depends(get_db)):
    """Soft-delete oglasa (postavlja is_deleted=True, ne briše iz baze)."""
    oglas = session.get(Oglas, oglas_id)
    if not oglas or oglas.is_deleted:
        raise HTTPException(status_code=404, detail="Oglas nije pronađen.")

    oglas.is_deleted = True
    oglas.updated_at = datetime.utcnow()
    session.add(oglas)
    session.commit()


# PATCH /oglasi/{id}/status  – admin: change status

class StatusUpdate(BaseModel):
    status: OglasStatus
    admin_comment: Optional[str] = None
    approved_by: Optional[int] = None


@router.patch("/{oglas_id}/status", response_model=Oglas)
def update_status(
    oglas_id: int,
    data: StatusUpdate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Admin endpoint za promjenu statusa oglasa (approve, reject, itd.)."""
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Nemate dozvolu za ovu akciju.")

    oglas = session.get(Oglas, oglas_id)
    if not oglas or oglas.is_deleted:
        raise HTTPException(status_code=404, detail="Oglas nije pronađen.")

    oglas.status = data.status
    if data.admin_comment is not None:
        oglas.admin_comment = data.admin_comment
    if data.approved_by is not None:
        oglas.approved_by = data.approved_by
    if data.status == OglasStatus.changes_requested:
        oglas.changes_requested_at = datetime.utcnow()

    oglas.updated_at = datetime.utcnow()
    session.add(oglas)
    session.commit()
    session.refresh(oglas)
    return oglas
