from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, or_
from typing import List
from datetime import datetime, timezone
from app.database import get_db
from app.models.ads_model import Oglas, OglasStatus

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
                Oglas.naziv.ilike(search_filter),        # Case-insensitive pretraga za naslov
                Oglas.kompanija_id.ilike(search_filter),      # za kompaniju
                Oglas.opis.ilike(search_filter)   # za opis/tekst oglasa
            )
        )
    oglasi = db.exec(statement).all()
    trenutno_vrijeme = datetime.now(timezone.utc)

    rezultat = []
    for oglas in oglasi:
        oglas_data = oglas.model_dump()
        
        if oglas.rok and oglas.rok < trenutno_vrijeme:
            oglas_data["status"] = OglasStatus.expired

        rezultat.append(oglas_data)
        
    return rezultat
  