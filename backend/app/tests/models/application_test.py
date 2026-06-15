import pytest
from pydantic import ValidationError
from app.models.application import ApplicationCreate, ApplicationUpdate, ApplicationStatus


# --- Helper: validni osnovni podaci za ApplicationCreate ---

def valid_payload(**overrides):
    base = {
        "ad_id": 42,
        "cv_path": "/uploads/cvs/student_cv.pdf",
        "motivational_letter_path": "/uploads/letters/motivation.pdf",
        "linkedin_url": "https://www.linkedin.com/in/elnur-student-123",
        "phone": "+38761234567"
    }
    base.update(overrides)
    return base


# ============================================================
# ApplicationCreate — happy path (Uspješni scenariji)
# ============================================================

class TestApplicationCreateValid:

    def test_valid_application_create_full(self):
        """Testira kreiranje aplikacije sa svim popunjenim poljima."""
        app = ApplicationCreate(**valid_payload())
        assert app.ad_id == 42
        assert app.cv_path == "/uploads/cvs/student_cv.pdf"
        assert app.linkedin_url == "https://www.linkedin.com/in/elnur-student-123"
        assert app.phone == "+38761234567"

    def test_valid_application_create_without_linkedin(self):
        """Testira kreiranje kada je opcionalni LinkedIn URL izostavljen ili eksplicitno None."""
        payload = valid_payload()
        payload.pop("linkedin_url")
        
        app1 = ApplicationCreate(**payload)
        assert app1.linkedin_url is None

        app2 = ApplicationCreate(**valid_payload(linkedin_url=None))
        assert app2.linkedin_url is None

    def test_valid_linkedin_formats(self):
        """Testira različite ispravne formate za LinkedIn URL profile."""
        valid_urls = [
            "https://linkedin.com/in/username",
            "https://www.linkedin.com/in/user-name-123",
            "https://linkedin.com/in/user_name_99/",  # Sa kosom crtom na kraju
            "  https://linkedin.com/in/clean-me   "   # Sa razmacima koje strip() treba očistiti
        ]
        for url in valid_urls:
            app = ApplicationCreate(**valid_payload(linkedin_url=url))
            # Provjeravamo da li se strip-uje unutar validatora (ako se dodijeli nazad u objekat)
            assert "linkedin.com/in/" in app.linkedin_url

    def test_valid_phone_formats(self):
        """Testira različite dozvoljene formate telefonskih brojeva (dužina 7 do 20 karaktera, sa i bez plusa, crtica, zagrada)."""
        valid_phones = [
            "+38761234567",
            "061-234-567",
            "+1 (555) 123-4567",
            "1234567",                # Minimum od 7 cifara
            "12345678901234567890",   # Maksimum od 20 cifara
            "  +38761234567  "        # Sa razmacima koje strip() treba očistiti
        ]
        for phone in valid_phones:
            app = ApplicationCreate(**valid_payload(phone=phone))
            assert app.phone is not None


# ============================================================
# ApplicationCreate — linkedin_url edge case-ovi i validacija
# ============================================================

class TestApplicationCreateLinkedinValidation:

    def test_linkedin_invalid_protocol(self):
        """Http umjesto https ili potpuno bez protokola."""
        with pytest.raises(ValidationError) as exc:
            ApplicationCreate(**valid_payload(linkedin_url="http://linkedin.com/in/user"))
        assert "LinkedIn URL must be in format" in str(exc.value)

        with pytest.raises(ValidationError):
            ApplicationCreate(**valid_payload(linkedin_url="linkedin.com/in/user"))

    def test_linkedin_wrong_domain_or_path(self):
        """LinkedIn link ali nije direktno profil (npr. pogrešan poddomen ili fali /in/)."""
        wrong_urls = [
            "https://linkedin.com/company/some-company",
            "https://www.linkedin.com/jobs/123456",
            "https://facebook.com/in/username",
            "https://linkedin.com/in/"  # Prazan username na kraju
        ]
        for url in wrong_urls:
            with pytest.raises(ValidationError):
                ApplicationCreate(**valid_payload(linkedin_url=url))


# ============================================================
# ApplicationCreate — phone edge case-ovi i validacija
# ============================================================

class TestApplicationCreatePhoneValidation:

    def test_phone_too_short_should_fail(self):
        """Broj telefona kraći od 7 karaktera (granični slučaj ispod minimuma)."""
        with pytest.raises(ValidationError) as exc:
            ApplicationCreate(**valid_payload(phone="123456"))  # 6 karaktera
        assert "Phone number is not in a valid format." in str(exc.value)

    def test_phone_too_long_should_fail(self):
        """Broj telefona duži od 20 karaktera (granični slučaj iznad maksimuma)."""
        with pytest.raises(ValidationError):
            ApplicationCreate(**valid_payload(phone="123456789012345678901"))  # 21 karakter

    def test_phone_invalid_characters_should_fail(self):
        """Broj telefona koji sadrži slova ili nedozvoljene specijalne karaktere."""
        invalid_phones = [
            "+38761234abc",
            "061/234-567",   # Kosa crta nije u regexu r'[0-9\s\-\(\)]'
            "+38761@34567"
        ]
        for phone in invalid_phones:
            with pytest.raises(ValidationError):
                ApplicationCreate(**valid_payload(phone=phone))

    def test_phone_empty_string_should_fail(self):
        with pytest.raises(ValidationError):
            ApplicationCreate(**valid_payload(phone=""))


# ============================================================
# ApplicationUpdate — edge case-ovi (Sva polja su parcijalna/Optional)
# ============================================================

class TestApplicationUpdateEdgeCases:

    def test_update_only_status(self):
        update = ApplicationUpdate(status=ApplicationStatus.accepted)
        assert update.status == ApplicationStatus.accepted
        assert update.admin_feedback is None
        assert update.is_archived is None

    def test_update_only_admin_feedback(self):
        update = ApplicationUpdate(admin_feedback="CV je odličan, ali nemate dovoljno iskustva.")
        assert update.admin_feedback == "CV je odličan, ali nemate dovoljno iskustva."
        assert update.status is None

    def test_update_only_is_archived(self):
        update = ApplicationUpdate(is_archived=True)
        assert update.is_archived is True

    def test_update_empty_payload(self):
        """Provjerava da li je model validan kada se ništa ne pošalje (sva polja ostaju None)."""
        update = ApplicationUpdate()
        assert update.status is None
        assert update.admin_feedback is None
        assert update.is_archived is None