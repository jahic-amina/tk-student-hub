from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.ad_bookmark import AdBookmark, AdBookmarkCreate, AdBookmarkRead

router = APIRouter(
    prefix="/bookmarks",
    tags=["Bookmarks"]
)

@router.post("/", response_model=AdBookmarkRead, status_code=status.HTTP_201_CREATED)
def bookmark_ad(
    data: AdBookmarkCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != UserRole.member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Permission denied. Only students can use bookmarks."
        )

    statement = select(AdBookmark).where(
        AdBookmark.user_id == current_user.id,
        AdBookmark.ad_id == data.ad_id
    )
    already_bookmarked = db.exec(statement).first()
    if already_bookmarked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="You have already bookmarked this ad."
        )

    db_bookmark = AdBookmark(
        user_id=current_user.id,
        ad_id=data.ad_id
    )
    
    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)
    return db_bookmark


@router.get("/", response_model=List[AdBookmarkRead])
def get_my_bookmarks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    if current_user.role != UserRole.member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Permission denied. Only students can use bookmarks."
        )

    statement = select(AdBookmark).where(AdBookmark.user_id == current_user.id)
    return db.exec(statement).all()


@router.get("/{bookmark_id}", response_model=AdBookmarkRead)
def get_bookmark(
    bookmark_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != UserRole.member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Permission denied. Only students can use bookmarks."
        )

    db_bookmark = db.get(AdBookmark, bookmark_id)
    if not db_bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Bookmark not found."
        )
    
    if db_bookmark.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Permission denied."
        )
        
    return db_bookmark


@router.delete("/{bookmark_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_bookmark(
    bookmark_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Permission denied. Only students can use bookmarks."
        )
    

    db_bookmark = db.get(AdBookmark, bookmark_id)
    if not db_bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Bookmark not found."
        )
    
    if db_bookmark.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Permission denied."
        )
    
    db.delete(db_bookmark)
    db.commit()
    return None