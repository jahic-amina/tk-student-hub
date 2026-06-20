import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine, select

from app.models import user as _user_models          # noqa: F401
from app.models import company as _company_models    # noqa: F401
from app.models import notification as _notification_models  # noqa: F401
from app.models import activity_log as _activity_log_models  # noqa: F401

from app.database import get_db
from app.core.security import get_current_user, get_current_company
from app.models.user import User, UserRole
from app.models.company import Company, CompanyStatus
from app.models.notification import Notification
from app.routers.company import router as company_router


# Fixture-i

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
    app = FastAPI()
    app.include_router(company_router)
    return app


@pytest.fixture(name="client")
def client_fixture(test_app, session):
    def get_db_override():
        return session

    test_app.dependency_overrides[get_db] = get_db_override
    client = TestClient(test_app)
    yield client
    test_app.dependency_overrides.clear()


@pytest.fixture(name="login_as_user")
def login_as_user_fixture(test_app):
    """Mock login za User (admin ili member)."""
    def _login(user):
        test_app.dependency_overrides[get_current_user] = lambda: user
    return _login


@pytest.fixture(name="login_as_company")
def login_as_company_fixture(test_app):
    """Mock login za Company."""
    def _login(company):
        test_app.dependency_overrides[get_current_company] = lambda: company
    return _login


# Helperi za test podatke

def _create_company(session, **overrides):
    defaults = dict(
        company_name="Test Kompanija",
        description="Opis kompanije.",
        website_url="https://test.ba",
        email="kompanija@test.com",
        phone_number="033123456",
        tin="1234567890123",
        hashed_password="hashed",
        address="Sarajevo",
        status=CompanyStatus.approved,
        is_deleted=False,
    )
    defaults.update(overrides)
    company = Company(**defaults)
    session.add(company)
    session.commit()
    session.refresh(company)
    return company


def _create_admin(session, email="admin@test.com"):
    admin = User(
        email=email,
        full_name="Admin",
        password_hash="hash",
        role=UserRole.admin,
    )
    session.add(admin)
    session.commit()
    session.refresh(admin)
    return admin


def _create_member(session, email="member@test.com"):
    member = User(
        email=email,
        full_name="Member",
        password_hash="hash",
        role=UserRole.member,
    )
    session.add(member)
    session.commit()
    session.refresh(member)
    return member


# GET /companies/
#vraća samo approved, neobrisane kompanije

class TestGetCompanies:

    def test_returns_only_approved_non_deleted_companies(self, client, session):
        _create_company(session, email="a@test.com", status=CompanyStatus.approved)
        _create_company(session, email="b@test.com", status=CompanyStatus.pending)
        _create_company(session, email="c@test.com", status=CompanyStatus.approved, is_deleted=True)

        response = client.get("/companies/")

        assert response.status_code == 200
        body = response.json()
        assert len(body) == 1
        assert body[0]["status"] == "approved"

    def test_returns_empty_list_when_no_approved_companies(self, client, session):
        _create_company(session, email="a@test.com", status=CompanyStatus.pending)

        response = client.get("/companies/")

        assert response.status_code == 200
        assert response.json() == []

    def test_returns_empty_list_when_no_companies(self, client):
        response = client.get("/companies/")

        assert response.status_code == 200
        assert response.json() == []


# GET /companies/admin
#samo admin može pristupiti

class TestGetCompaniesAdmin:

    def test_admin_can_get_all_companies(self, client, session, login_as_user):
        admin = _create_admin(session)
        _create_company(session, email="a@test.com", status=CompanyStatus.approved)
        _create_company(session, email="b@test.com", status=CompanyStatus.pending)
        _create_company(session, email="c@test.com", status=CompanyStatus.approved, is_deleted=True)

        login_as_user(admin)
        response = client.get("/companies/admin")

        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_member_cannot_access_admin_endpoint(self, client, session, login_as_user):
        member = _create_member(session)

        login_as_user(member)
        response = client.get("/companies/admin")

        assert response.status_code == 403


# GET /companies/{company_id}
#vraća kompaniju ili 404

class TestGetCompanyById:

    def test_returns_approved_company(self, client, session):
        company = _create_company(session)

        response = client.get(f"/companies/{company.id}")

        assert response.status_code == 200
        assert response.json()["id"] == company.id

    def test_returns_404_for_non_existent_company(self, client):
        response = client.get("/companies/99999")

        assert response.status_code == 404

    def test_returns_404_for_deleted_company(self, client, session):
        company = _create_company(session, is_deleted=True)

        response = client.get(f"/companies/{company.id}")

        assert response.status_code == 404

    def test_returns_404_for_pending_company(self, client, session):
        company = _create_company(session, status=CompanyStatus.pending)

        response = client.get(f"/companies/{company.id}")

        assert response.status_code == 404


# PATCH /companies/{company_id}/status
#admin mijenja status, kompanija dobija notifikaciju

class TestUpdateCompanyStatus:

    def test_admin_can_approve_company(self, client, session, login_as_user):
        admin = _create_admin(session)
        company = _create_company(session, status=CompanyStatus.pending)

        login_as_user(admin)
        response = client.patch(
            f"/companies/{company.id}/status",
            json="approved"
        )

        assert response.status_code == 200
        assert response.json()["status"] == "approved"

    def test_admin_approve_sends_notification_to_company(self, client, session, login_as_user):
        admin = _create_admin(session)
        company = _create_company(session, status=CompanyStatus.pending)

        login_as_user(admin)
        client.patch(f"/companies/{company.id}/status", json="approved")

        notifications = session.exec(
            select(Notification).where(Notification.company_id == company.id)
        ).all()
        assert len(notifications) == 1
        assert "odobren" in notifications[0].text.lower()

    def test_no_notification_if_status_unchanged(self, client, session, login_as_user):
        admin = _create_admin(session)
        company = _create_company(session, status=CompanyStatus.approved)

        login_as_user(admin)
        client.patch(f"/companies/{company.id}/status", json="approved")

        notifications = session.exec(
            select(Notification).where(Notification.company_id == company.id)
        ).all()
        assert len(notifications) == 0

    def test_member_cannot_update_status(self, client, session, login_as_user):
        member = _create_member(session)
        company = _create_company(session, status=CompanyStatus.pending)

        login_as_user(member)
        response = client.patch(f"/companies/{company.id}/status", json="approved")

        assert response.status_code == 403

    def test_returns_404_for_non_existent_company(self, client, session, login_as_user):
        admin = _create_admin(session)

        login_as_user(admin)
        response = client.patch("/companies/99999/status", json="approved")

        assert response.status_code == 404


# DELETE /companies/{company_id}
#soft delete, samo admin može obrisati 

class TestDeleteCompany:

    def test_admin_can_soft_delete_company(self, client, session, login_as_user):
        admin = _create_admin(session)
        company = _create_company(session)

        login_as_user(admin)
        response = client.delete(f"/companies/{company.id}")

        assert response.status_code == 200
        session.refresh(company)
        assert company.is_deleted == True

    def test_member_cannot_delete_company(self, client, session, login_as_user):
        member = _create_member(session)
        company = _create_company(session)

        login_as_user(member)
        response = client.delete(f"/companies/{company.id}")

        assert response.status_code == 403

    def test_returns_404_for_non_existent_company(self, client, session, login_as_user):
        admin = _create_admin(session)

        login_as_user(admin)
        response = client.delete("/companies/99999")

        assert response.status_code == 404

    def test_returns_404_for_already_deleted_company(self, client, session, login_as_user):
        admin = _create_admin(session)
        company = _create_company(session, is_deleted=True)

        login_as_user(admin)
        response = client.delete(f"/companies/{company.id}")

        assert response.status_code == 404