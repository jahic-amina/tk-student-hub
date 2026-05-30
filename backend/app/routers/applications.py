from typing import Optional, List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.params import File
from sqlmodel import Session, select
from app.models.application import Application, ApplicationCreate, ApplicationRead, ApplicationStatus, ApplicationUpdate
from app.models.ad import Ad, AdStatus
from app.models.user import User, UserRole
from app.core.security import get_current_user
from app.database import get_db
import os
from uuid import uuid4

LOCAL_UPLOAD_DIR = os.path.join(os.getcwd(), "uploads", "applications")
os.makedirs(LOCAL_UPLOAD_DIR, exist_ok=True)

ALLOWED_FILE_EXTENSIONS = {"pdf"}

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.get("/", response_model=List[ApplicationRead])
def applications(
    app_status: Optional[ApplicationStatus] = None,
    ad_id: Optional[int] = None,
    include_archived: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in [UserRole.admin, UserRole.saradnik]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this resource.",
        )
    
    statement = select(Application)
    
    if current_user.role == UserRole.saradnik:
        if ad_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contributors must specify the ad_id parameter.",
            )
        ad = db.get(Ad, ad_id)
        if not ad:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ad not found.",
            )
        statement = statement.where(Application.ad_id == ad.id)
    elif current_user.role == UserRole.admin:
        if ad_id is not None:
            statement = statement.where(Application.ad_id == ad_id)
    
    if app_status is not None:
        statement = statement.where(Application.status == app_status)
    if not include_archived:
        statement = statement.where(Application.is_archived == False)

    return db.exec(statement).all()


@router.post("/", response_model=ApplicationRead, status_code=status.HTTP_201_CREATED)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ad = db.get(Ad, payload.ad_id)
    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ad not found.",
        )
    if ad.status != AdStatus.active or ad.deadline < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ad is not active.",
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
            detail="An application for this ad already exists.",
        )

    application = Application(
        user_id=current_user.id,
        ad_id=payload.ad_id,
        motivational_letter_path=payload.motivational_letter_path,
        cv_path=payload.cv_path,
        linkedin_url=payload.linkedin_url,
        phone=payload.phone,
    )

    db.add(application)
    db.commit()
    db.refresh(application)
    return application


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
            detail="Application not found.",
        )

    if current_user.role != UserRole.admin and application.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this application.",
        )

    return application


@router.patch("/{application_id}", response_model=ApplicationRead)
def update_application(
    application_id: int,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can perform this action.",
        )

    application = db.get(Application, application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        )

    updates = payload.model_dump(exclude_unset=True)
    for field_name, field_value in updates.items():
        setattr(application, field_name, field_value)

    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.post("/upload-cv")
def upload_cv_local(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    # Validacija datoteke
    if file.content_type not in ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="File must be PDF, DOC or DOCX.")
    
    # Spremi fajl sa UUID imenom
    file_ext = file.filename.split(".")[-1].lower()
    filename = f"{uuid4().hex}.{file_ext}"
    cv_path = f"uploads/applications/{filename}"
    dest = os.path.join(LOCAL_UPLOAD_DIR, filename)
    
    with open(dest, "wb") as f:
        content = file.file.read()
        f.write(content)

    return {"path": cv_path}


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can perform this action.",
        )
    
    application = db.get(Application, application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        )

    application.is_archived = True
    db.add(application)
    db.commit() 
