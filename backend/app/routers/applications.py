from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.security import get_current_user
from app.database import get_db
from app.models.application import Application, ApplicationCreate, ApplicationStatus, ApplicationUpdate
from app.models.user import User, UserRole


router = APIRouter(prefix="/applications", tags=["applications"])


def require_admin(current_user: User) -> None:
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Samo admin može da radi ovu akciju.",
        )


@router.post("/{ad_id}", response_model=Application, status_code=status.HTTP_201_CREATED)
def create_application(
    ad_id: int,
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_application = db.exec(
        select(Application).where(
            Application.user_id == current_user.id,
            Application.ad_id == ad_id,
        )
    ).first()

    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Već postoji prijava za ovaj oglas.",
        )

    application = Application(
        user_id=current_user.id,
        ad_id=ad_id,
        motivational_letter_path=payload.motivational_letter_path,
        cv_path=payload.cv_path,
        linkedin=payload.linkedin,
        phone=payload.phone,
    )

    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.get("/", response_model=list[Application])
def list_applications(
    status: ApplicationStatus | None = None,
    include_archived: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = select(Application)
    if current_user.role != UserRole.admin:
        statement = statement.where(Application.user_id == current_user.id)

    if status is not None:
        statement = statement.where(Application.status == status)

    if not include_archived:
        statement = statement.where(Application.is_archived == False)

    return db.exec(statement).all()


@router.get("/{application_id}", response_model=Application)
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


@router.patch("/{application_id}", response_model=Application)
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


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
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

    application.is_archived = True
    db.add(application)
    db.commit()
    return None