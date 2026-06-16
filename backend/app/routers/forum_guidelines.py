from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.forum import ForumGuideline

router = APIRouter(prefix="/forum/guidelines", tags=["Forum Guidelines"])


class GuidelineCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    content: str = Field(min_length=3)
    order: Optional[int] = 0


class GuidelineUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    content: Optional[str] = Field(None, min_length=3)
    order: Optional[int] = None


def require_admin(current_user: User):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Nemate ovlaštenje.")


@router.get("/", response_model=List[dict])
def get_guidelines(db: Session = Depends(get_db)):
    statement = select(ForumGuideline).order_by(ForumGuideline.order.asc(), ForumGuideline.id.asc())
    guidelines = db.exec(statement).all()
    return [
        {
            "id": g.id, "title": g.title, "content": g.content,
            "order": g.order, "created_at": g.created_at, "updated_at": g.updated_at,
        }
        for g in guidelines
    ]


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_guideline(
    data: GuidelineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)
    guideline = ForumGuideline(title=data.title, content=data.content, order=data.order or 0)
    db.add(guideline)
    db.commit()
    db.refresh(guideline)
    return guideline


@router.patch("/{guideline_id}")
def update_guideline(
    guideline_id: int,
    data: GuidelineUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)
    guideline = db.get(ForumGuideline, guideline_id)
    if not guideline:
        raise HTTPException(status_code=404, detail="Smjernica nije pronađena.")

    if data.title is not None:
        guideline.title = data.title
    if data.content is not None:
        guideline.content = data.content
    if data.order is not None:
        guideline.order = data.order

    guideline.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.add(guideline)
    db.commit()
    db.refresh(guideline)
    return guideline


@router.delete("/{guideline_id}")
def delete_guideline(
    guideline_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)
    guideline = db.get(ForumGuideline, guideline_id)
    if not guideline:
        raise HTTPException(status_code=404, detail="Smjernica nije pronađena.")
    db.delete(guideline)
    db.commit()
    return {"success": True, "message": "Smjernica je obrisana."}
