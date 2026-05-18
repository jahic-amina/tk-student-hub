from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.database import get_db
from app.models.sacuvane_prilike import (
    SacuvanaPrilika,
    SacuvanaPrilikaCreate,
    SacuvanaPrilikaUpdate
)

router = APIRouter(
    prefix="/sacuvane-prilike",
    tags=["Sačuvane Prilike"]
)

# 1. CREATE - Spasi oglas za korisnika (Bookmark)
@router.post("/", response_model=SacuvanaPrilika, status_code=status.HTTP_201_CREATED)
def save_opportunity(data: SacuvanaPrilikaCreate, session: Session = Depends(get_db)):
    # Provjera da korisnik nije već ranije spasio isti oglas
    statement = select(SacuvanaPrilika).where(
        SacuvanaPrilika.user_id == data.user_id,
        SacuvanaPrilika.oglas_id == data.oglas_id
    )
    already_saved = session.exec(statement).first()
    if already_saved:
        raise HTTPException(status_code=400, detail="Ovaj oglas je već sačuvan za ovog korisnika")

    db_saved = SacuvanaPrilika.model_validate(data)
    session.add(db_saved)
    session.commit()
    session.refresh(db_saved)
    return db_saved


# 2. READ ALL - Dohvati sve sačuvane oglase za određenog korisnika
@router.get("/user/{user_id}", response_model=List[SacuvanaPrilika])
def get_user_saved_opportunities(user_id: int, session: Session = Depends(get_db)):
    statement = select(SacuvanaPrilika).where(SacuvanaPrilika.user_id == user_id)
    return session.exec(statement).all()


# 3. READ ONE - Dohvati specifičan zapis preko ID-ja
@router.get("/{saved_id}", response_model=SacuvanaPrilika)
def get_saved_opportunity(saved_id: int, session: Session = Depends(get_db)):
    db_saved = session.get(SacuvanaPrilika, saved_id)
    if not db_saved:
        raise HTTPException(status_code=404, detail="Zapis nije pronađen")
    return db_saved


# 4. UPDATE - Izmjena zapisa (Puni CRUD standard)
@router.patch("/{saved_id}", response_model=SacuvanaPrilika)
def update_saved_opportunity(
    saved_id: int, 
    update_data: SacuvanaPrilikaUpdate, 
    session: Session = Depends(get_db)
):
    db_saved = session.get(SacuvanaPrilika, saved_id)
    if not db_saved:
        raise HTTPException(status_code=404, detail="Zapis nije pronađen")
    
    obj_data = update_data.model_dump(exclude_unset=True)
    for key, value in obj_data.items():
        setattr(db_saved, key, value)
        
    session.add(db_saved)
    session.commit()
    session.refresh(db_saved)
    return db_saved


# 5. DELETE - Ukloni iz sačuvanih (Unbookmark)
@router.delete("/{saved_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_saved_opportunity(saved_id: int, session: Session = Depends(get_db)):
    db_saved = session.get(SacuvanaPrilika, saved_id)
    if not db_saved:
        raise HTTPException(status_code=404, detail="Zapis nije pronađen")
    
    session.delete(db_saved)
    session.commit()
    return None