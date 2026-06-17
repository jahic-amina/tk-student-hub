"""
Testovi za app/models/ad_bookmark.py:
  - AdBookmark (tabela): defaultne vrijednosti, UniqueConstraint
  - AdBookmarkCreate: validacija inputa
  - AdBookmarkRead: serijalizacija iz ORM objekta

Napomena: AdBookmark je tabela (SQLModel, table=True) sa UniqueConstraint,
pa za njegovo testiranje treba prava (test) baza — zato ovaj fajl sam pravi
izolovanu in-memory SQLite bazu i test korisnike kroz fixture-e, umjesto da
se oslanja samo na čiste Pydantic objekte.
"""
import pytest
from datetime import datetime
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine, select

# Ovi importi registruju tabele (users, companies, ads, ad_bookmarks...) u
# SQLModel.metadata. Potrebno je da bi create_all() mogao razriješiti FK-eve
# (npr. ad_bookmarks.ad_id -> ads.id, ads.company_id -> companies.id) i
# relationship-e (npr. User.activity_logs -> "ActivityLog").
from app.models import user as _user_models  # noqa: F401
from app.models import company as _company_models  # noqa: F401
from app.models import ad as _ad_models  # noqa: F401
from app.models import activity_log as _activity_log_models  # noqa: F401
from app.models import ad_bookmark as _ad_bookmark_models  # noqa: F401

from app.models.user import User, UserRole
from app.models.ad_bookmark import AdBookmark, AdBookmarkCreate, AdBookmarkRead


# Fixture-i (baza + test korisnici)

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


def _create_user(session, role, email):
    user = User(
        email=email,
        full_name="Test User",
        password_hash="not-a-real-hash",
        role=role,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="member_user")
def member_user_fixture(session):
    return _create_user(session, UserRole.member, "student@test.com")


@pytest.fixture(name="other_member_user")
def other_member_user_fixture(session):
    return _create_user(session, UserRole.member, "drugi_student@test.com")


# AdBookmark (tabela)

class TestAdBookmarkModel:

    def test_create_bookmark_sets_defaults(self, session, member_user):
        bookmark = AdBookmark(user_id=member_user.id, ad_id=1)

        # Provjera default_factory-ja PRIJE upisa u bazu: SQLite (test baza)
        # ne čuva timezone offset, pa bi nakon session.refresh() tzinfo bio
        # None bez obzira što je kod ispravan (u Postgresu npr. ne bi bio).
        assert bookmark.created_at.tzinfo is not None

        session.add(bookmark)
        session.commit()
        session.refresh(bookmark)

        assert bookmark.id is not None
        assert bookmark.user_id == member_user.id
        assert bookmark.ad_id == 1
        assert isinstance(bookmark.created_at, datetime)

    def test_unique_constraint_same_user_same_ad(self, session, member_user):
        """Isti korisnik ne smije imati dva bookmark-a za isti ad_id."""
        session.add(AdBookmark(user_id=member_user.id, ad_id=5))
        session.commit()

        session.add(AdBookmark(user_id=member_user.id, ad_id=5))
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

    def test_same_user_can_bookmark_different_ads(self, session, member_user):
        session.add(AdBookmark(user_id=member_user.id, ad_id=1))
        session.add(AdBookmark(user_id=member_user.id, ad_id=2))
        session.commit()  # ne smije puknuti

        rows = session.exec(
            select(AdBookmark).where(AdBookmark.user_id == member_user.id)
        ).all()
        assert len(rows) == 2

    def test_different_users_can_bookmark_same_ad(self, session, member_user, other_member_user):
        """Unique constraint je po (user_id, ad_id) paru, ne samo po ad_id."""
        session.add(AdBookmark(user_id=member_user.id, ad_id=10))
        session.add(AdBookmark(user_id=other_member_user.id, ad_id=10))
        session.commit()  # ne smije puknuti

        rows = session.exec(
            select(AdBookmark).where(AdBookmark.ad_id == 10)
        ).all()
        assert len(rows) == 2


# AdBookmarkCreate

class TestAdBookmarkCreate:

    def test_valid_payload(self):
        data = AdBookmarkCreate(ad_id=42)
        assert data.ad_id == 42

    def test_ad_id_is_required(self):
        with pytest.raises(ValidationError):
            AdBookmarkCreate()

    def test_ad_id_must_be_valid_int(self):
        with pytest.raises(ValidationError):
            AdBookmarkCreate(ad_id="nije_broj")


# AdBookmarkRead

class TestAdBookmarkRead:

    def test_serializes_from_orm_object(self, session, member_user):
        bookmark = AdBookmark(user_id=member_user.id, ad_id=7)
        session.add(bookmark)
        session.commit()
        session.refresh(bookmark)

        read_data = AdBookmarkRead.model_validate(bookmark)

        assert read_data.id == bookmark.id
        assert read_data.user_id == member_user.id
        assert read_data.ad_id == 7
        assert read_data.created_at == bookmark.created_at

    def test_missing_required_field_should_fail(self):
        with pytest.raises(ValidationError):
            AdBookmarkRead(user_id=1, ad_id=2, created_at=datetime.now())  # nedostaje 'id'