from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, or_
from typing import List
from datetime import datetime, timezone
from app.database import get_db
from app.models.ad import Ad, AdStatus
from app.models.company import Company

router = APIRouter(prefix="/public-ads", tags=["Public Ads"])

@router.get("/", response_model=List[Ad])
def get_public_ads(
    search: str | None = Query(
        default=None, 
        description="Search jobs by title, company, or description"
    ),
    db: Session = Depends(get_db)
):
    """
    Javni endpoint koji vraća listu svih oglasa.
    Podržava opcionu pretragu preko ?search= parametra.
    NEMA Security/Auth dependencija, što ga čini javno dostupnim.
    """
    statement = select(Ad).join(Company, Ad.company_id == Company.id).where(Ad.status == AdStatus.active, Ad.is_deleted == False)
    
    if search:
        search_filter = f"%{search}%"
        
        statement = statement.where(
            or_(
                Ad.title.ilike(search_filter),        
                Company.company_name.ilike(search_filter),      
                Ad.description.ilike(search_filter)   
            )
        )
    ads = db.exec(statement).all()
    

    rezultat = []
    for ad in ads:
        ad_data = ad.model_dump()
        
        
        if ad.deadline and ad.deadline < datetime.now(timezone.utc).date():
            ad_data["status"] = AdStatus.expired

        rezultat.append(ad_data)
        
    return rezultat
  