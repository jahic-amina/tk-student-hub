import pytest
from fastapi import status
from sqlmodel import Session, select
from app.main import app

# PAŽNJA: Prilagodi ovu putanju tvom projektu ako je ruter na drugom mjestu
from app.routers.notification import get_current_actor 

from app.models.notification import Notification, NotificationType
from app.models.user import User, UserRole
from app.models.company import Company
# ... tvoji postojeći importi na vrhu ...

@pytest.fixture
def student_user(session: Session):
    """Lokalni ispravljeni fixture za studenta"""
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
    """Lokalni ispravljeni fixture za admina"""
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
# --- POMOĆNA FUNKCIJA ZA POSTAVLJANJE AKTORA ---
def set_actor(actor):
    """Pomaže nam da simuliramo ulogovanog korisnika/kompaniju."""
    app.dependency_overrides[get_current_actor] = lambda: actor

# ==================== TESTOVI ZA KREIRANJE (POST /) ====================

def test_create_notification_admin_success(client, session: Session, admin_user: User):
    set_actor(admin_user)
    
    payload = {
        "user_id": admin_user.id,
        "text": "Nova prilika za praksu je dostupna!",
        "type": "new_opportunity",
        "is_read": False
    }
    
    response = client.post("/notifications/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["text"] == payload["text"]
    assert data["type"] == payload["type"]
    assert data["user_id"] == admin_user.id

def test_create_notification_forbidden_for_student(client, student_user: User):
    set_actor(student_user)
    
    payload = {
        "user_id": student_user.id,
        "text": "Student pokušava kreirati",
        "type": "status_change"
    }
    
    response = client.post("/notifications/", json=payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_create_notification_validation_error(client, admin_user: User):
    set_actor(admin_user)
    
    # Prazan tekst (blank text) treba da baci grešku zbog našeg @field_validator-a
    payload = {
        "text": "   ", 
        "type": "status_change"
    }
    response = client.post("/notifications/", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# ==================== TESTOVI ZA ČITANJE (GET /me) ====================

def test_get_my_notifications_student(client, session: Session, student_user: User):
    # Kreirajmo par notifikacija u bazi za ovog studenta
    n1 = Notification(user_id=student_user.id, text="Notifikacija 1", type=NotificationType.STATUS_CHANGE, is_read=True)
    n2 = Notification(user_id=student_user.id, text="Notifikacija 2", type=NotificationType.COMMENT_LIKED, is_read=False)
    session.add_all([n1, n2])
    session.commit()

    set_actor(student_user)
    response = client.get("/notifications/me")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == 2
    # Zbog order_by(is_read.asc(), created_at.desc()), nepročitana (is_read=False) mora biti prva
    assert data[0]["is_read"] is False
    assert data[1]["is_read"] is True


# ==================== TESTOVI ZA MARKIRENJE (READ-ALL i SINGLE READ) ====================

@pytest.mark.parametrize("method", ["POST", "PATCH", "PUT"])
def test_mark_all_as_read(client, session: Session, student_user: User, method):
    n1 = Notification(user_id=student_user.id, text="A", type=NotificationType.STATUS_CHANGE, is_read=False)
    session.add(n1)
    session.commit()

    set_actor(student_user)
    response = client.request(method, "/notifications/read-all")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["detail"] == "All notifications marked as read."

    # Provjera u bazi
    session.refresh(n1)
    assert n1.is_read is True

def test_mark_single_as_read_success(client, session: Session, student_user: User):
    n = Notification(user_id=student_user.id, text="Test", type=NotificationType.STATUS_CHANGE, is_read=False)
    session.add(n)
    session.commit()
    session.refresh(n)

    set_actor(student_user)
    response = client.patch(f"/notifications/{n.id}/read")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["is_read"] is True

def test_mark_single_as_read_forbidden(client, session: Session, student_user: User, company_user: Company):
    # Notifikacija pripada studentu
    n = Notification(user_id=student_user.id, text="Test", type=NotificationType.STATUS_CHANGE, is_read=False)
    session.add(n)
    session.commit()
    session.refresh(n)

    # Kompanija pokušava pročitati tuđu notifikaciju
    set_actor(company_user)
    response = client.patch(f"/notifications/{n.id}/read")
    assert response.status_code == status.HTTP_403_FORBIDDEN


# ==================== TESTOVI ZA DETALJE, UPDATE I BRISANJE ====================

def test_get_notification_by_id_success(client, session: Session, student_user: User):
    n = Notification(user_id=student_user.id, text="Specific", type=NotificationType.STATUS_CHANGE)
    session.add(n)
    session.commit()
    session.refresh(n)

    set_actor(student_user)
    response = client.get(f"/notifications/{n.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["text"] == "Specific"

def test_get_notification_not_found(client, student_user: User):
    set_actor(student_user)
    response = client.get("/notifications/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_notification_success(client, session: Session, student_user: User):
    n = Notification(user_id=student_user.id, text="Stari tekst", type=NotificationType.STATUS_CHANGE)
    session.add(n)
    session.commit()
    session.refresh(n)

    set_actor(student_user)
    payload = {"text": "Novi tekst nakon izmjene"}
    response = client.patch(f"/notifications/{n.id}", json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["text"] == "Novi tekst nakon izmjene"

def test_delete_notification_success(client, session: Session, student_user: User):
    n = Notification(user_id=student_user.id, text="Za brisanje", type=NotificationType.STATUS_CHANGE)
    session.add(n)
    session.commit()
    session.refresh(n)

    set_actor(student_user)
    response = client.delete(f"/notifications/{n.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Provjera da je stvarno obrisana iz baze
    deleted_n = session.get(Notification, n.id)
    assert deleted_n is None

def test_clear_all_notifications(client, session: Session, student_user: User):
    n1 = Notification(user_id=student_user.id, text="1", type=NotificationType.STATUS_CHANGE)
    n2 = Notification(user_id=student_user.id, text="2", type=NotificationType.STATUS_CHANGE)
    session.add_all([n1, n2])
    session.commit()

    set_actor(student_user)
    response = client.delete("/notifications/clear-all")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Baza mora biti prazna za tog korisnika
    res = session.exec(select(Notification).where(Notification.user_id == student_user.id)).all()
    assert len(res) == 0