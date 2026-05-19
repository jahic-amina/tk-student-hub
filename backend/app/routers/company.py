from typing import Optional, List
import re
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from app.database import get_db
from app.models.company import Company, CompanyCreate, CompanyUpdate, CompanyStatus
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/companies", tags=["Companies"])


def _validate_company_payload(data: CompanyCreate) -> None:
    if len(data.company_name.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company name must be at least 2 characters long.",
        )

    if len(data.description.strip()) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Description must be at least 10 characters long.",
        )

    website_pattern = r"^https://[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+(/.*)?$"
    if not re.match(website_pattern, data.website_url.strip()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Website URL must be in format https://something.something.",
        )

    logo_pattern = r"^https://.+\.(png|jpg|jpeg|webp)(\?.*)?$"
    if not re.match(logo_pattern, data.logo_url.strip(), flags=re.IGNORECASE):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Logo URL must point to a .png, .jpg, .jpeg or .webp image.",
        )

    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    if not re.match(email_pattern, data.email.strip()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is not in a valid format.",
        )

    if not data.jib.isdigit():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="JIB must contain only digits.",
        )

    if len(data.address.strip()) <= 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Address must be longer than 2 characters.",
        )


def _validate_company_partial_payload(data: CompanyUpdate) -> None:
    payload = data.model_dump(exclude_unset=True)

    if "company_name" in payload and len(payload["company_name"].strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company name must be at least 2 characters long.",
        )

    if "description" in payload and len(payload["description"].strip()) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Description must be at least 10 characters long.",
        )

    website_pattern = r"^https://[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+(/.*)?$"
    if "website_url" in payload and not re.match(website_pattern, payload["website_url"].strip()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Website URL must be in format https://something.something.",
        )

    logo_pattern = r"^https://.+\.(png|jpg|jpeg|webp)(\?.*)?$"
    if "logo_url" in payload and not re.match(logo_pattern, payload["logo_url"].strip(), flags=re.IGNORECASE):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Logo URL must point to a .png, .jpg, .jpeg or .webp image.",
        )

    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    if "email" in payload and not re.match(email_pattern, payload["email"].strip()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is not in a valid format.",
        )

    if "jib" in payload and not payload["jib"].isdigit():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="JIB must contain only digits.",
        )

    if "address" in payload and len(payload["address"].strip()) <= 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Address must be longer than 2 characters.",
        )

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
    _validate_company_payload(data)

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

    _validate_company_payload(data)

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

    _validate_company_partial_payload(data)

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