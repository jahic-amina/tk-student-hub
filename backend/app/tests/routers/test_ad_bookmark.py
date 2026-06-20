import pytest
from fastapi import status
from sqlmodel import Session
from app.main import app

from app.core.security import get_current_user
from app.models.ad_bookmark import AdBookmark
from app.models.user import User
from app.models.company import Company
from app.models.ad import Ad

# ==================== LOKALNI FIXTURES (OVERRIDE) ====================

@pytest.fixture
def student_user(session: Session):
    """Lokalni ispravljeni fixture za studenta (popravljen password_hash)"""
    from app.core.security import hash_password
    from app.models.user import User, UserRole
    
    user = User(
        email="student@test.ba",
        full_name="Test Student",
        password_hash=hash_password("password123"),
        role=UserRole.member,
        is_active=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@pytest.fixture
def admin_user(session: Session):
    """Lokalni ispravljeni fixture za admina (popravljen password_hash)"""
    from app.core.security import hash_password
    from app.models.user import User, UserRole
    
    user = User(
        email="admin@test.ba",
        full_name="Test Admin",
        password_hash=hash_password("password123"),
        role=UserRole.admin,
        is_active=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# --- POMOĆNA FUNKCIJA ZA POSTAVLJANJE KORISNIKA ---
def set_current_user(user):
    app.dependency_overrides[get_current_user] = lambda: user

# ==================== TESTOVI ZA KREIRANJE BOOKMARKA ====================

def test_bookmark_ad_success(client, session: Session, student_user: User, active_ad: Ad):
    set_current_user(student_user)
    
    payload = {"ad_id": active_ad.id}
    response = client.post("/bookmarks/", json=payload)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["ad_id"] == active_ad.id
    assert data["user_id"] == student_user.id

def test_bookmark_ad_already_bookmarked(client, session: Session, student_user: User, active_ad: Ad):
    # Prvo ručno ubacimo bookmark u bazu
    bookmark = AdBookmark(user_id=student_user.id, ad_id=active_ad.id)
    session.add(bookmark)
    session.commit()
    
    set_current_user(student_user)
    payload = {"ad_id": active_ad.id}
    
    # Pokušaj ponovnog bookmarkovanja istog oglasa -> 400 Bad Request
    response = client.post("/bookmarks/", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "You have already bookmarked this ad."

def test_bookmark_ad_forbidden_for_company(client, session: Session, active_ad: Ad):
    from app.models.user import User, UserRole
    
    # Umjesto Company, kreiramo korisnika koji nije 'member' (npr. mentor) kako bismo testirali zabranu
    non_student_user = User(
        email="mentor_test@test.ba",
        full_name="Test Mentor",
        password_hash="nebitno_za_ovaj_test",
        role=UserRole.mentor,  # Ovo nije 'member', pa će ruta odbiti pristup
        is_active=True,
    )
    session.add(non_student_user)
    session.commit()
    session.refresh(non_student_user)
    
    set_current_user(non_student_user)
    
    payload = {"ad_id": active_ad.id}
    response = client.post("/bookmarks/", json=payload)
    
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Permission denied. Only students can use bookmarks."


# ==================== TESTOVI ZA PREUZIMANJE BOOKMARKA ====================

def test_get_my_bookmarks(client, session: Session, student_user: User, active_ad: Ad):
    bookmark = AdBookmark(user_id=student_user.id, ad_id=active_ad.id)
    session.add(bookmark)
    session.commit()
    
    set_current_user(student_user)
    response = client.get("/bookmarks/")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == 1
    assert data[0]["ad_id"] == active_ad.id

def test_get_specific_bookmark_success(client, session: Session, student_user: User, active_ad: Ad):
    bookmark = AdBookmark(user_id=student_user.id, ad_id=active_ad.id)
    session.add(bookmark)
    session.commit()
    session.refresh(bookmark)
    
    set_current_user(student_user)
    response = client.get(f"/bookmarks/{bookmark.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == bookmark.id

def test_get_specific_bookmark_not_found(client, student_user: User):
    set_current_user(student_user)
    response = client.get("/bookmarks/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_specific_bookmark_permission_denied(client, session: Session, admin_user: User, student_user: User, active_ad: Ad):
    # Bookmark pripada studentu
    bookmark = AdBookmark(user_id=student_user.id, ad_id=active_ad.id)
    session.add(bookmark)
    session.commit()
    session.refresh(bookmark)
    
    # Kreiramo lažnog studenta (drugog korisnika) koji će pokušati vidjeti tuđi bookmark
    drugi_student = User(email="other@test.ba", full_name="Drugi Student", password_hash="123", role="member")
    session.add(drugi_student)
    session.commit()
    session.refresh(drugi_student)
    
    set_current_user(drugi_student)
    response = client.get(f"/bookmarks/{bookmark.id}")
    # Ruta vraća 403 ako korisnik nije vlasnik bookmarka
    assert response.status_code == status.HTTP_403_FORBIDDEN


# ==================== TESTOVI ZA BRISANJE BOOKMARKA ====================

def test_remove_bookmark_success(client, session: Session, student_user: User, active_ad: Ad):
    bookmark = AdBookmark(user_id=student_user.id, ad_id=active_ad.id)
    session.add(bookmark)
    session.commit()
    session.refresh(bookmark)
    
    set_current_user(student_user)
    response = client.delete(f"/bookmarks/{bookmark.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Provjera da je obrisano iz baze
    assert session.get(AdBookmark, bookmark.id) is None