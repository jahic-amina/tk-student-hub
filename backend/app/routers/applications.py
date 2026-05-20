from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    boto3 = None

    class ClientError(Exception):
        pass
from app.core.security import get_current_user
from app.database import get_db
from app.models.application import Application, ApplicationCreate, ApplicationRead, ApplicationStatus, ApplicationUpdate
from app.models.user import User, UserRole
from fastapi import UploadFile, File
import os
from uuid import uuid4
from typing import Optional
from app.models.ad import Ad, AdStatus
from datetime import date

S3_BUCKET = os.getenv("S3_BUCKET")
S3_ENDPOINT = os.getenv("S3_ENDPOINT")
S3_REGION = os.getenv("S3_REGION")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")

LOCAL_UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(LOCAL_UPLOAD_DIR, exist_ok=True)


router = APIRouter(prefix="/applications", tags=["applications"])


def require_admin(current_user: User) -> None:
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Samo admin može da radi ovu akciju.",
        )


@router.post("/", response_model=ApplicationRead, status_code=status.HTTP_201_CREATED)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ad=db.get(Ad, payload.ad_id)
    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Oglas nije pronađen.",
        )
    if ad.status != AdStatus.active or ad.deadline < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Oglas nije aktivan.",
        )
    existing_application = db.exec(
        select(Application).where(
            Application.user_id == current_user.id,
            Application.ad_id == payload.ad_id,
        )
    ).first()

    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Već postoji prijava za ovaj oglas.",
        )

    application = Application(
        user_id=current_user.id,
        ad_id=payload.ad_id,
        motivational_letter_path=payload.motivational_letter_path,
        cv_path=payload.cv_path,
        linkedin=payload.linkedin,
        phone=payload.phone,
    )

    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.get("/", response_model=list[ApplicationRead])
def applications(
    status: ApplicationStatus | None = None,
    ad_id: int | None = None,
    include_archived: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in [UserRole.admin, UserRole.saradnik]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nemaš pristup ovom resursu.",
        )
    statement = select(Application)
    if current_user.role == UserRole.saradnik:
        if ad_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Saradnici moraju specificirati ad_id parametar.",
            )
        ad=db.get(Ad, ad_id)
        if not ad:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Oglas nije pronađen.",
            )
        if ad.company_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Saradnici mogu vidjeti samo prijave za svoje oglase.",
            )
    
        statement = statement.where(Application.ad_id == ad.id)
    elif current_user.role == UserRole.admin:
            if ad_id is not None:
              statement = statement.where(Application.ad_id == ad_id)
    if  status is not None:
        statement = statement.where(Application.status == status)
    if not include_archived:
        statement = statement.where(Application.is_archived == False)

    return db.exec(statement).all()


@router.get("/{application_id}", response_model=ApplicationRead)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    application = db.get(Application, application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prijava nije pronađena.",
        )

    if current_user.role != UserRole.admin and application.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nemaš pristup ovoj prijavi.",
        )

    return application


@router.patch("/{application_id}", response_model=ApplicationRead)
def update_application(
    application_id: int,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    application = db.get(Application, application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prijava nije pronađena.",
        )

    updates = payload.model_dump(exclude_unset=True)
    for field_name, field_value in updates.items():
        setattr(application, field_name, field_value)

    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.post("/presign", status_code=status.HTTP_200_OK)
def get_presigned_upload(
    filename: str,
    content_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
):
    safe_filename="".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()
    key = f"applications/{current_user.id}/{uuid4().hex}_{safe_filename}"

    
    try:
        import boto3

        if not S3_BUCKET:
            raise RuntimeError("S3 not configured")

        s3_client = boto3.client(
            "s3",
            endpoint_url=S3_ENDPOINT or None,
            region_name=S3_REGION or None,
            aws_access_key_id=S3_ACCESS_KEY or None,
            aws_secret_access_key=S3_SECRET_KEY or None,
        )

        params = {"Bucket": S3_BUCKET, "Key": key}
        if content_type:
            params["ContentType"] = content_type

        url = s3_client.generate_presigned_url(
            "put_object", Params=params, ExpiresIn=300
        )
        return {"upload_url": url, "method": "PUT", "key": key}
    except Exception:
        
        return {
            "upload_url": "/applications/upload-cv",
            "method": "POST",
            "field_name": "file",
            "key": key,
        }


@router.post("/upload-cv")
def upload_cv_local(
    file: UploadFile = File(...),
    key: Optional[str] = None,
    current_user: User = Depends(get_current_user),
):
    if key:
        filename = os.path.basename(key)
    else:
        filename = f"{uuid4().hex}_{file.filename}" 
    dest = os.path.join(LOCAL_UPLOAD_DIR, filename)
    with open(dest, "wb") as f:
        content = file.file.read()
        f.write(content)

    # Return path that can be stored in DB
    return {"path": f"uploads/{filename}", "key": key}


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)
    application = db.get(Application, application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prijava nije pronađena.",
        )

    application.is_archived = True
    db.add(application)
    db.commit()
    return 
