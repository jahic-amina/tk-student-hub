import pytest
from datetime import date, timedelta
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine, select

# Registruju tabele u SQLModel.metadata (potrebno za FK-eve i relationships).
from app.models import user as _user_models  # noqa: F401
from app.models import company as _company_models  # noqa: F401
from app.models import ad as _ad_models  # noqa: F401
from app.models import notification as _notification_models  # noqa: F401
from app.models import activity_log as _activity_log_models  # noqa: F401
from app.models import application as _application_models  # noqa: F401

from app.database import get_db
from app.core.security import get_current_company
from app.models.user import User, UserRole
from app.models.company import Company, CompanyStatus
from app.models.ad import Ad, AdType, AdStatus
from app.models.notification import Notification
from app.routers.ad import router as ad_router


# Fixture-i (baza, app, klijent, mock login)

@pytest.fixture(name="engine")
def engine_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture(name="test_app")
def test_app_fixture():
    """Minimalna FastAPI app koja sadrži samo ads router."""
    app = FastAPI()
    app.include_router(ad_router)
    return app


@pytest.fixture(name="client")
def client_fixture(test_app, session):
    def get_db_override():
        return session

    test_app.dependency_overrides[get_db] = get_db_override
    client = TestClient(test_app)
    yield client
    test_app.dependency_overrides.clear()


@pytest.fixture(name="login_as_company")
def login_as_company_fixture(test_app):
    """Helper za mock login kompanije, npr. login_as_company(company)."""
    def _login(company):
        test_app.dependency_overrides[get_current_company] = lambda: company
    return _login


# Helperi za test podatke

def _create_company(session, **overrides):
    defaults = dict(
        company_name="Test Kompanija",
        description="Opis kompanije.",
        website_url="https://test-kompanija.test",
        email="kompanija@test.com",
        phone_number="033123456",
        tin="12345678",
        hashed_password="hashed",
        address="Sarajevo",
        status=CompanyStatus.approved,
    )
    defaults.update(overrides)
    company = Company(**defaults)
    session.add(company)
    session.commit()
    session.refresh(company)
    return company


def _create_ad(session, company, status=AdStatus.active, is_deleted=False, **overrides):
    defaults = dict(
        company_id=company.id,
        title="Praksa - Backend Developer",
        type=AdType.internship,
        field="Informacione tehnologije",
        location="Sarajevo",
        description="Opis prakse.",
        deadline=date.today() + timedelta(days=10),
        spots=2,
        status=status,
        is_deleted=is_deleted,
    )
    defaults.update(overrides)
    ad = Ad(**defaults)
    session.add(ad)
    session.commit()
    session.refresh(ad)
    return ad


def _valid_ad_payload(**overrides):
    """JSON payload za POST /ads/ koji prolazi AdCreate validaciju."""
    base = {
        "company_id": 9999,  # router treba da ovo IGNORIŠE i koristi company_id iz tokena
        "title": "Junior Python Developer",
        "type": "internship",
        "field": "Informacione tehnologije",
        "location": "Sarajevo",
        "description": "Detaljan opis pozicije sa dovoljno informacija.",
        "deadline": str(date.today() + timedelta(days=5)),
        "duration_months": 3,
        "compensation": 500.0,
        "currency": "BAM",
        "spots": 1,
        "requirements": "Poznavanje Pythona.",
        "benefits": "Mentorstvo.",
    }
    base.update(overrides)
    return base


@pytest.fixture(name="company")
def company_fixture(session):
    return _create_company(session)


# GET /ads/ (happy path)

class TestGetAds:

    def test_returns_only_active_non_deleted_ads(self, client, session, company):
        _create_ad(session, company, status=AdStatus.active)
        _create_ad(session, company, status=AdStatus.pending)
        _create_ad(session, company, status=AdStatus.active, is_deleted=True)

        response = client.get("/ads/")

        assert response.status_code == 200
        body = response.json()
        assert len(body) == 1
        assert body[0]["status"] == "active"

    def test_returns_empty_list_when_no_ads(self, client):
        response = client.get("/ads/")

        assert response.status_code == 200
        assert response.json() == []


# POST /ads/ (happy path)

class TestCreateAd:

    def test_company_can_create_ad(self, client, login_as_company, company):
        login_as_company(company)
        response = client.post("/ads/", json=_valid_ad_payload())

        assert response.status_code == 201
        body = response.json()
        assert body["title"] == "Junior Python Developer"
        # company_id mora biti iz autentifikovane kompanije, ne iz payload-a (9999)
        assert body["company_id"] == company.id
        assert body["status"] == "pending"  # default status za novi oglas

    def test_create_ad_notifies_all_admins(self, client, session, login_as_company, company):
        admin = User(
            email="admin@test.com",
            full_name="Admin",
            password_hash="hash",
            role=UserRole.admin,
        )
        session.add(admin)
        session.commit()
        session.refresh(admin)

        login_as_company(company)
        payload = _valid_ad_payload(
            title="Marketing Internship",
            field="Marketing",
            location="Mostar",
        )

        response = client.post("/ads/", json=payload)
        assert response.status_code == 201

        notifications = session.exec(
            select(Notification).where(Notification.user_id == admin.id)
        ).all()
        assert len(notifications) == 1
        assert "novi oglas" in notifications[0].text.lower()