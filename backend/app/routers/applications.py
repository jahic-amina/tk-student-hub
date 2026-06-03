from typing import Optional, List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.params import File
from sqlmodel import Session, select
from app.models.application import Application, ApplicationCreate, ApplicationRead, ApplicationStatus, ApplicationUpdate
from app.models.ad import Ad, AdStatus
from app.models.user import User, UserRole
from app.models.company import Company
from app.core.security import get_current_user, get_current_company
from app.database import get_db
from app.models.notification import Notification, NotificationType
import os
from uuid import uuid4

LOCAL_UPLOAD_DIR = os.path.join(os.getcwd(), "uploads", "applications")
os.makedirs(LOCAL_UPLOAD_DIR, exist_ok=True)

ALLOWED_FILE_EXTENSIONS = {"pdf"}
ALLOWED_CONTENT_TYPES = {"application/pdf"}

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.get("/", response_model=List[ApplicationRead])
def applications(
    app_status: Optional[ApplicationStatus] = None,
    ad_id: Optional[int] = None,
    include_archived: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this resource.",
        )
    
    statement = select(Application)
    
    if ad_id is not None:
        statement = statement.where(Application.ad_id == ad_id)
    
    if app_status is not None:
        statement = statement.where(Application.status == app_status)
    if not include_archived:
        statement = statement.where(Application.is_archived == False)

    return db.exec(statement).all()

@router.get("/company/all", response_model=List[ApplicationRead])
def get_all_company_applications(
    app_status: Optional[ApplicationStatus] = None,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):
    """Get all applications for ads that belong to the current company, with optional status filtering."""

    statement = select(Application).join(Ad, Application.ad_id == Ad.id).where(
        Ad.company_id == current_company.id,
        Application.is_archived == False
    )
    
    if app_status is not None:
        statement = statement.where(Application.status == app_status)

    return db.exec(statement).all()

@router.get("/company/by-ad/{ad_id}", response_model=List[ApplicationRead])
def get_company_applications(
    ad_id: int,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):
    """Get applications for a specific ad that belongs to the current company."""
    ad = db.get(Ad, ad_id)
    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ad not found.",
        )
    
    
    if ad.company_id != current_company.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to applications for this ad.",
        )
    
    
    statement = (select(Application).where(
            Application.ad_id == ad_id,
            Application.is_archived == False
        )
        .limit(limit)
        .offset(offset)
    )
    
    return db.exec(statement).all()

@router.get("/company/application/{application_id}", response_model=ApplicationRead)
def get_company_application(
    application_id: int,
    db: Session=Depends(get_db),
    current_company: Company=Depends(get_current_company),                              
    ):
    application = db.get(Application, application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        )
    ad = db.get(Ad, application.ad_id)
    if not ad or ad.company_id != current_company.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this application.",
        )

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
    MAX_FILE_SIZE = 5 * 1024 * 1024  

    file_ext= file.filename.split(".")[-1].lower()
    if file_ext not in ALLOWED_FILE_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File must have a .pdf extension.") 
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="File must be a PDF.") 
     
    content = file.file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 5 MB limit.")    
    
    filename = f"{uuid4().hex}.{file_ext}"
    cv_path = f"uploads/applications/{filename}"
    dest = os.path.join(LOCAL_UPLOAD_DIR, filename)
    
    with open(dest, "wb") as f:
        f.write(content)

    return {"path": cv_path}

@router.patch("/company/{application_id}", response_model=ApplicationRead)
def update_application_company(
    application_id: int,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):
    application = db.get(Application, application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        )

    ad = db.get(Ad, application.ad_id)
    if not ad or ad.company_id != current_company.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to alter this application.",
        )

    stari_status = application.status

    updates = payload.model_dump(exclude_unset=True)
    for field_name, field_value in updates.items():
        setattr(application, field_name, field_value)

    db.add(application)

    if stari_status != application.status:
        if application.status == ApplicationStatus.accepted:
            tekst = f"Čestitamo! Vaša prijava za oglas '{ad.title}' kod kompanije '{current_company.company_name}' je prihvaćena."
            db.add(Notification(user_id=application.user_id, text=tekst, type=NotificationType.STATUS_CHANGE))
        elif application.status == ApplicationStatus.rejected:
            tekst = f"Vaša prijava za oglas '{ad.title}' kod kompanije '{current_company.company_name}' ovaj put nije odabrana."
            db.add(Notification(user_id=application.user_id, text=tekst, type=NotificationType.STATUS_CHANGE))

    db.commit()
    db.refresh(application)
    return application

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