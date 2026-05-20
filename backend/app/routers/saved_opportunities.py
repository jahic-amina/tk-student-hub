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
    # Provjeravamo da li je oglas već spašen (promijenjeno oglas_id u ad_id)
    statement = select(SavedOpportunity).where(
        SavedOpportunity.user_id == current_user.id,
        SavedOpportunity.ad_id == data.ad_id
    )
    already_saved = session.exec(statement).first()
    if already_saved:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="You have already saved this opportunity."
        )

    # Kreiranje novog zapisa sa ispravnim poljem ad_id
    db_saved = SavedOpportunity(
        user_id=current_user.id,
        ad_id=data.ad_id
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Saved opportunity not found."
        )
    
    if db_saved.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to view this saved opportunity."
        )
        
    return db_saved


@router.delete("/{saved_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_saved_opportunity(
    saved_id: int, 
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_saved = session.get(SavedOpportunity, saved_id)
    if not db_saved:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Saved opportunity not found."
        )
    
    if db_saved.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to delete this saved opportunity."
        )
    
    session.delete(db_saved)
    session.commit()
    return None