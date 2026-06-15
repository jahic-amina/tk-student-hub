from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from app.core.config import settings
from app.database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
oauth2_scheme_company = OAuth2PasswordBearer(tokenUrl="/auth/company/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from app.models.user import User
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.exec(select(User).where(User.id == int(user_id))).first()
    if user is None:
        raise credentials_exception

    # Check that the account is still active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vaš profil je deaktiviran. Kontaktirajte administratora.",
        )

    return user


def get_current_company(token: str = Depends(oauth2_scheme_company), db: Session = Depends(get_db)):
    from app.models.company import Company
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    company_id = payload.get("sub")
    if company_id is None:
        raise credentials_exception

    company = db.exec(select(Company).where(Company.id == int(company_id))).first()
    if company is None or company.is_deleted:
        raise credentials_exception

    return company


def get_current_actor(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Decodes the token and returns either a User or a Company instance,
    based on the 'role' claim in the JWT payload.
    """
    from app.models.user import User
    from app.models.company import Company

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    actor_id = payload.get("sub")
    role = payload.get("role")

    if actor_id is None:
        raise credentials_exception

    try:
        actor_id_int = int(actor_id)
    except (ValueError, TypeError):
        raise credentials_exception

    if role == "company":
        company = db.exec(select(Company).where(Company.id == actor_id_int)).first()
        if company and not company.is_deleted:
            return company
        raise credentials_exception

    if role and ("admin" in str(role).lower() or "member" in str(role).lower()):
        user = db.exec(select(User).where(User.id == actor_id_int)).first()
        if user:
            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Vaš profil je deaktiviran. Kontaktirajte administratora.",
                )
            return user
        raise credentials_exception

    # Fallback: try user first, then company
    user = db.exec(select(User).where(User.id == actor_id_int)).first()
    if user:
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vaš profil je deaktiviran. Kontaktirajte administratora.",
            )
        return user

    company = db.exec(select(Company).where(Company.id == actor_id_int)).first()
    if company and not company.is_deleted:
        return company

    raise credentials_exception
