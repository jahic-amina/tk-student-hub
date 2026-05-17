from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, or_
from typing import List

from app.database import get_db
from app.models.ads_model import Oglas 

router = APIRouter(prefix="/oglasi", tags=["Oglasi"])

@router.get("/", response_model=List[Oglas])
def get_oglasi(
    search: str | None = Query(
        default=None, 
        description="Pretraga oglasa po naslovu, kompaniji ili opisu"
    ),
    db: Session = Depends(get_db)
):
    """
    Javni endpoint koji vraća listu svih oglasa.
    Podržava opcionu pretragu preko ?search= parametra.
    NEMA Security/Auth dependencija, što ga čini javno dostupnim.
    """
    statement = select(Oglas)
    
    if search:
        search_filter = f"%{search}%"
        
        statement = statement.where(
            or_(
                Oglas.title.ilike(search_filter),        # Case-insensitive pretraga za naslov
                Oglas.company.ilike(search_filter),      # za kompaniju
                Oglas.description.ilike(search_filter)   # za opis/tekst oglasa
            )
        )
    
    oglasi = db.exec(statement).all()
    return oglasi
