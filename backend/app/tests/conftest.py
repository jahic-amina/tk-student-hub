import pytest
from datetime import date, timedelta
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_db
from app.core.security import hash_password, create_access_token
from app.models.user import User, UserRole
from app.models.company import Company, CompanyStatus
from app.models.ad import Ad, AdStatus, AdType


@pytest.fixture(name="session")
def session_fixture():
    """Fixture for database session with in-memory SQLite."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Fixture for FastAPI TestClient with test database."""
    app.dependency_overrides[get_db] = lambda: session
    yield TestClient(app)
    app.dependency_overrides.clear()
   


@pytest.fixture
def student_user(session: Session):
    """Create a test student user."""
    user = User(
        email="student@test.ba",
        full_name="Test Student",
        password_hash=hash_password("password123"),
        role=UserRole.member,
        is_active=True,
    )
    session.add(user)
    session.flush()
    return user


@pytest.fixture
def admin_user(session: Session):
    """Create a test admin user."""
    user = User(
        email="admin@test.ba",
        full_name="Test Admin",
        password_hash=hash_password("password123"),
        role=UserRole.admin,
        is_active=True,
    )
    session.add(user)
    session.flush()
    return user


@pytest.fixture
def company_user(session: Session):
    """Create a test company."""
    company = Company(
        company_name="Test Company",
        description="A test company for testing.",
        website_url="https://test.ba",
        email="company@test.ba",
        phone_number="+38761234567",
        tin="1234567890123",
        hashed_password=hash_password("password123"),  # Kompanija ostaje hashed_password
        status=CompanyStatus.approved,
        address="Test Address",
    )
    session.add(company)
    session.flush()
    return company


@pytest.fixture
def student_token(student_user: User):
    """Create JWT token for student user."""
    return create_access_token({"sub": str(student_user.id), "role": "member"})


@pytest.fixture
def admin_token(admin_user: User):
    """Create JWT token for admin user."""
    return create_access_token({"sub": str(admin_user.id), "role": "admin"})


@pytest.fixture
def company_token(company_user: Company):
    """Create JWT token for company user."""
    return create_access_token({"sub": str(company_user.id), "role": "company"})


@pytest.fixture
def active_ad(session: Session, company_user: Company):
    """Create an active ad (internship type)."""
    ad = Ad(
        company_id=company_user.id,
        title="Software Engineer Internship",
        type=AdType.internship,
        field="Informatika",
        location="Sarajevo",
        description="Develop your skills.",
        deadline=date.today() + timedelta(days=30),
        duration_months=3,
        compensation=500.0,
        currency="BAM",
        spots=2,
        requirements="Know Python.",
        benefits="Mentorship",
        status=AdStatus.active,
    )
    session.add(ad)
    session.flush()
    return ad


@pytest.fixture
def pending_ad(session: Session, company_user: Company):
    """Create a pending ad (awaiting admin approval)."""
    ad = Ad(
        company_id=company_user.id,
        title="Data Science Internship",
        type=AdType.education,
        field="Data Science",
        location="Sarajevo",
        description="Learn data analysis.",
        deadline=date.today() + timedelta(days=45),
        duration_months=6,
        compensation=600.0,
        currency="BAM",
        spots=1,
        requirements="Math background.",
        benefits="Certificate",
        status=AdStatus.pending,
    )
    session.add(ad)
    session.flush()
    return ad


@pytest.fixture
def expired_ad(session: Session, company_user: Company):
    """Create an expired ad."""
    ad = Ad(
        company_id=company_user.id,
        title="Old Internship",
        type=AdType.internship,
        field="IT",
        location="Sarajevo",
        description="This is old.",
        deadline=date.today() - timedelta(days=1),
        duration_months=2,
        compensation=400.0,
        currency="BAM",
        spots=5,
        status=AdStatus.expired,
    )
    session.add(ad)
    session.flush()
    return ad

@pytest.fixture
def other_company_ad(session: Session):
    """CRITICAL FOR 403 TESTS: Creates an ad that belongs to a completely different company."""
    other_company = Company(
        company_name="Other Company LLC",
        description="Another company.",
        website_url="https://other.ba",
        email="other_company@test.ba",
        phone_number="+38761999999",
        tin="9876543210321",
        hashed_password=hash_password("password123"),
        status=CompanyStatus.approved,
        address="Other Address",
    )
    session.add(other_company)
    session.flush()

    ad = Ad(
        company_id=other_company.id,
        title="Tuđi Oglas (Forbidden Target)",
        type=AdType.internship,
        field="IT",
        location="Mostar",
        description="You should not see this.",
        deadline=date.today() + timedelta(days=10),
        duration_months=3,
        status=AdStatus.active,
    )
    session.add(ad)
    session.flush()
    return ad
