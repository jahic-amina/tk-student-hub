from typing import List
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status, Body
from fastapi.params import File
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.database import get_db
from app.models.company import Company, CompanyCreate, CompanyUpdate, CompanyStatus, CompanyRead
from app.models.user import User, UserRole
from app.core.security import hash_password, get_current_user, get_current_company
import os
from uuid import uuid4

LOCAL_UPLOAD_DIR = os.path.join(os.getcwd(), "uploads", "companies")
os.makedirs(LOCAL_UPLOAD_DIR, exist_ok=True)

ALLOWED_LOGO_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.get("/", response_model=List[CompanyRead])
def get_companies(db: Session = Depends(get_db)):
    query = select(Company).where(
        Company.status == CompanyStatus.approved,
        Company.is_deleted == False
    )
    return db.exec(query).all()


@router.get("/admin", response_model=List[CompanyRead])
def get_companies_admin(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission for this.",
        )

    query = select(Company)
    return db.exec(query).all()


@router.get("/{company_id}", response_model=CompanyRead)
def get_company_by_id(company_id: int, db: Session = Depends(get_db)):
    company = db.get(Company, company_id)
    if not company or company.is_deleted or company.status != CompanyStatus.approved:
        raise HTTPException(status_code=404, detail="Company not found.")
    return company


@router.post("/", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
def create_company(
    company_name: str = Form(...),
    tin: str = Form(...),
    website_url: str = Form(...),
    address: str = Form(...),
    description: str = Form(...),
    email: str = Form(...),
    phone_number: str = Form(...),
    password: str = Form(...),
    logo: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if logo.content_type not in ["image/png", "image/jpeg", "image/webp"]:
        raise HTTPException(status_code=400, detail="Logo mora biti PNG, JPG, JPEG ili WebP.")

    existing = db.exec(select(Company).where(Company.email == email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email je već registrovan.")

    file_ext = logo.filename.split(".")[-1].lower()
    filename = f"{uuid4().hex}.{file_ext}"
    logo_path = f"uploads/companies/{filename}"
    dest = os.path.join(LOCAL_UPLOAD_DIR, filename)

    with open(dest, "wb") as f:
        f.write(logo.file.read())

    company = Company(
        company_name=company_name,
        tin=tin,
        website_url=website_url,
        address=address,
        description=description,
        email=email,
        phone_number=phone_number,
        hashed_password=hash_password(password),
        logo_path=logo_path,
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.put("/{company_id}", response_model=CompanyRead)
def update_company(
    company_id: int,
    data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):
    if current_company.id != company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this company.",
        )

    update_data = data.model_dump(exclude={"status"})
    for key, value in update_data.items():
        setattr(current_company, key, value)

    db.add(current_company)
    db.commit()
    db.refresh(current_company)
    return current_company


@router.patch("/{company_id}", response_model=CompanyRead)
def patch_company(
    company_id: int,
    data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):
    if current_company.id != company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this company.",
        )

    update_data = data.model_dump(exclude_unset=True, exclude={"status"})
    for key, value in update_data.items():
        setattr(current_company, key, value)

    db.add(current_company)
    db.commit()
    db.refresh(current_company)
    return current_company


@router.patch("/{company_id}/status", response_model=CompanyRead)
def update_company_status(
    company_id: int,
    status_update: CompanyStatus = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission for this.",
        )

    company = db.get(Company, company_id)
    if not company or company.is_deleted:
        raise HTTPException(status_code=404, detail="Company not found.")

    company.status = status_update
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.patch("/{company_id}/restore", response_model=CompanyRead)
def restore_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission for this.",
        )

    company = db.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found.")

    company.is_deleted = False
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.patch("/{company_id}/upload-logo")
def upload_company_logo(
    company_id: int,
    logo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):
    if current_company.id != company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nemate dozvolu da ažurirate logo ove kompanije.",
        )
    
    # Validacija datoteke
    if logo.content_type not in ["image/png", "image/jpeg", "image/webp"]:
        raise HTTPException(status_code=400, detail="Logo mora biti PNG, JPG, JPEG ili WebP.")
    
    # Obriši stari logo ako postoji
    if current_company.logo_path:
        old_filename = current_company.logo_path.split("/")[-1]
        old_dest = os.path.join(LOCAL_UPLOAD_DIR, old_filename)
        if os.path.exists(old_dest):
            os.remove(old_dest)
    
    # Spremi novu sliku
    file_ext = logo.filename.split(".")[-1].lower()
    filename = f"{uuid4().hex}.{file_ext}"
    logo_path = f"uploads/companies/{filename}"
    dest = os.path.join(LOCAL_UPLOAD_DIR, filename)
    
    with open(dest, "wb") as f:
        content = logo.file.read()
        f.write(content)
    
    # Ažuriraj kompaniju
    current_company.logo_path = logo_path
    db.add(current_company)
    db.commit()
    db.refresh(current_company)
    
    return current_company


@router.delete("/{company_id}", response_model=CompanyRead)
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission for this.",
        )

    company = db.get(Company, company_id)
    if not company or company.is_deleted:
        raise HTTPException(status_code=404, detail="Company not found.")

    company.is_deleted = True
    db.add(company)
    db.commit()
    db.refresh(company)
    return company