"""
Testovi za app/models/notification.py:
  - Notification (tabela): defaultne vrijednosti, opcioni user_id/company_id
  - NotificationCreate: validacija text polja, defaultne vrijednosti
  - NotificationUpdate: parcijalni update, validacija text polja

Napomena: Notification je tabela (SQLModel, table=True), pa za testiranje
defaultnih vrijednosti i upisa u bazu treba prava (test) baza — zato ovaj
fajl sam pravi izolovanu in-memory SQLite bazu kroz fixture-e.
"""
import pytest
from datetime import datetime
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

# Ovi importi registruju tabele (users, companies, notifications...) u
# SQLModel.metadata. Potrebno je da bi create_all() mogao razriješiti FK-eve
# (notifications.user_id -> users.id, notifications.company_id -> companies.id)
# i relationship-e (npr. User.activity_logs -> "ActivityLog").
from app.models import user as _user_models  # noqa: F401
from app.models import company as _company_models  # noqa: F401
from app.models import activity_log as _activity_log_models  # noqa: F401
from app.models import notification as _notification_models  # noqa: F401

from app.models.notification import (
    Notification,
    NotificationCreate,
    NotificationUpdate,
    NotificationType,
)


# Fixture-i (baza)

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


# Notification (tabela)

class TestNotificationModel:

    def test_create_notification_sets_defaults(self, session):
        notification = Notification(
            user_id=1,
            text="Imate novu poruku.",
            type=NotificationType.NEW_OPPORTUNITY,
        )
        session.add(notification)
        session.commit()
        session.refresh(notification)

        assert notification.id is not None
        assert notification.is_read is False
        assert isinstance(notification.created_at, datetime)

    def test_user_id_and_company_id_can_both_be_none(self, session):
        """Notifikacija ne mora biti vezana ni za korisnika ni za kompaniju (npr. globalna)."""
        notification = Notification(
            text="Sistemska poruka.",
            type=NotificationType.DEADLINE_EXPIRING,
        )
        session.add(notification)
        session.commit()
        session.refresh(notification)

        assert notification.user_id is None
        assert notification.company_id is None

    def test_missing_text_raises_on_commit(self, session):
        """Table model ne validira obavezna polja pri kreiranju objekta (kao pydantic),
        nego tek pri upisu u bazu - kao NOT NULL constraint (IntegrityError)."""
        notification = Notification(type=NotificationType.STATUS_CHANGE)
        session.add(notification)
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

    def test_missing_type_raises_on_commit(self, session):
        notification = Notification(text="Poruka bez tipa.")
        session.add(notification)
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()


# NotificationCreate

class TestNotificationCreate:

    def test_valid_payload(self):
        data = NotificationCreate(
            user_id=1,
            text="Nova prilika za praksu!",
            type=NotificationType.NEW_OPPORTUNITY,
        )
        assert data.text == "Nova prilika za praksu!"
        assert data.is_read is False

    def test_text_whitespace_is_stripped(self):
        data = NotificationCreate(
            text="   Status prijave promijenjen.   ",
            type=NotificationType.STATUS_CHANGE,
        )
        assert data.text == "Status prijave promijenjen."

    def test_blank_text_after_strip_should_fail(self):
        with pytest.raises(ValidationError) as exc:
            NotificationCreate(text="     ", type=NotificationType.STATUS_CHANGE)
        assert "Notification text cannot be blank." in str(exc.value)

    def test_missing_text_should_fail(self):
        with pytest.raises(ValidationError):
            NotificationCreate(type=NotificationType.NEW_OPPORTUNITY)

    def test_missing_type_should_fail(self):
        with pytest.raises(ValidationError):
            NotificationCreate(text="Poruka bez tipa.")

    def test_user_id_and_company_id_default_to_none(self):
        data = NotificationCreate(text="Poruka.", type=NotificationType.DEADLINE_EXPIRING)
        assert data.user_id is None
        assert data.company_id is None


# NotificationUpdate

class TestNotificationUpdate:

    def test_partial_update_only_text(self):
        update = NotificationUpdate(text="Ažurirana poruka.")
        assert update.text == "Ažurirana poruka."
        assert update.type is None
        assert update.is_read is None

    def test_explicit_none_values_should_not_crash(self):
        """KRITIČAN EDGE CASE: polja su opciona, validator ne smije puknuti na eksplicitnom None."""
        update = NotificationUpdate(text=None, type=None, is_read=None)
        assert update.text is None
        assert update.type is None
        assert update.is_read is None

    def test_update_text_whitespace_is_stripped(self):
        update = NotificationUpdate(text="   Nova vrijednost   ")
        assert update.text == "Nova vrijednost"

    def test_update_blank_text_should_fail(self):
        with pytest.raises(ValidationError):
            NotificationUpdate(text="   ")

    def test_update_is_read_only(self):
        update = NotificationUpdate(is_read=True)
        assert update.is_read is True
        assert update.text is None