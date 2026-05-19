from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status, Header
from sqlmodel import Session, select
from app.database import get_db
from app.models.company import Company, CompanyCreate, CompanyUpdate, CompanyStatus, CompanyRead
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/companies", tags=["Companies"])


def get_company_by_api_key(
    company_id: int,
    x_api_key: str = Header(..., description="Company API key"),
    db: Session = Depends(get_db),
) -> Company:
    """Validate company API key and return company"""
    company = db.get(Company, company_id)
    if not company or company.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found.",
        )
    
    if company.api_key != x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
        )
    
    return company

@router.get("/", response_model=List[CompanyRead])
def get_companies(db: Session = Depends(get_db)):
    """Get all approved companies - public endpoint"""
    query = select(Company)
    query = query.where(Company.status == CompanyStatus.approved)
    query = query.where(Company.is_deleted == False)
    return db.exec(query).all()


@router.get("/admin", response_model=List[CompanyRead])
def get_companies_admin(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all companies - admin only"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission for this.",
        )

    query = select(Company)
    query = query.where(Company.status != CompanyStatus.denied)

    return db.exec(query).all()


@router.post("/", response_model=Company, status_code=status.HTTP_201_CREATED)
def create_company(data: CompanyCreate, db: Session = Depends(get_db)):
    company = Company(**data.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.put("/{company_id}", response_model=CompanyRead)
def update_company(
    company_id: int,
    data: CompanyCreate,
    company: Company = Depends(get_company_by_api_key),
    db: Session = Depends(get_db),
):
    company_data = data.model_dump()
    for key, value in company_data.items():
        setattr(company, key, value)

    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.patch("/{company_id}", response_model=CompanyRead)
def patch_company(
    company_id: int,
    data: CompanyUpdate,
    company: Company = Depends(get_company_by_api_key),
    db: Session = Depends(get_db),
):
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(company, key, value)

    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission for this.",
        )

    company = db.get(Company, company_id)
    if not company or company.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found.",
        )

    company.is_deleted = True
    db.add(company)
    db.commit()