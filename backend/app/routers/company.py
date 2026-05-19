from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from app.database import get_db
from app.models.company import Company, CompanyCreate, CompanyUpdate, CompanyStatus
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


@router.post("/", response_model=Company, status_code=status.HTTP_201_CREATED)
def create_company(data: CompanyCreate, db: Session = Depends(get_db)):
    company = Company(**data.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.put("/{company_id}", response_model=Company)
def update_company(company_id: int, data: CompanyCreate, db: Session = Depends(get_db)):
    company = db.get(Company, company_id)
    if not company or company.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found.",
        )

    company_data = data.model_dump()
    for key, value in company_data.items():
        setattr(company, key, value)

    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.patch("/{company_id}", response_model=Company)
def patch_company(company_id: int, data: CompanyUpdate, db: Session = Depends(get_db)):
    company = db.get(Company, company_id)
    if not company or company.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found.",
        )

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(company, key, value)

    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    company = db.get(Company, company_id)
    if not company or company.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found.",
        )

    company.is_deleted = True
    db.add(company)
    db.commit()