from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr
from app.database import get_db
from app.models.user import User
from app.models.company import Company
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


# --- Schemas ---

class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    company_name: str = None


# --- User endpoints ---

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.exec(select(User).where(User.email == data.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered.")

    user = User(
        email=data.email,
        full_name=data.full_name,
        password_hash=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponse)
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.email == data.username)).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


# --- Company endpoints ---

@router.post("/company/login", response_model=TokenResponse)
def company_login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    company = db.exec(select(Company).where(Company.email == data.username)).first()
    if not company or company.is_deleted:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    if not verify_password(data.password, company.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    if company.status != "approved":
        raise HTTPException(status_code=403, detail="Company account is not approved yet.")

    token = create_access_token({"sub": str(company.id)})
    return {"access_token": token, "token_type": "bearer", "company_name": company.company_name}