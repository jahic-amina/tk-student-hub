from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.saved_opportunities import SavedOpportunity, SavedOpportunityCreate

router = APIRouter(
    prefix="/saved-opportunities",
    tags=["Saved Opportunities"]
)

@router.post("/", response_model=SavedOpportunity, status_code=status.HTTP_201_CREATED)
def save_opportunity(
    data: SavedOpportunityCreate, 
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    statement = select(SavedOpportunity).where(
        SavedOpportunity.user_id == current_user.id,
        SavedOpportunity.oglas_id == data.oglas_id
    )
    already_saved = session.exec(statement).first()
    if already_saved:
        raise HTTPException(status_code=400, detail="You have already saved this opportunity.")

    
    db_saved = SavedOpportunity(
        user_id=current_user.id,
        oglas_id=data.oglas_id
    )
    
    session.add(db_saved)
    session.commit()
    session.refresh(db_saved)
    return db_saved


@router.get("/", response_model=List[SavedOpportunity])
def get_my_saved_opportunities(
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    statement = select(SavedOpportunity).where(SavedOpportunity.user_id == current_user.id)
    return session.exec(statement).all()


@router.get("/{saved_id}", response_model=SavedOpportunity)
def get_saved_opportunity(
    saved_id: int, 
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_saved = session.get(SavedOpportunity, saved_id)
    if not db_saved:
        raise HTTPException(status_code=404, detail="Saved opportunity not found.")
    
    if db_saved.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this saved opportunity.")
        
    return db_saved


@router.delete("/{saved_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_saved_opportunity(
    saved_id: int, 
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_saved = session.get(SavedOpportunity, saved_id)
    if not db_saved:
        raise HTTPException(status_code=404, detail="Saved opportunity not found.")
    
    if db_saved.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this saved opportunity.")
    
    session.delete(db_saved)
    session.commit()
    return None