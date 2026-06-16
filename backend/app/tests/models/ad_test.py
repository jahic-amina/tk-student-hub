import pytest
from datetime import date, timedelta
from pydantic import ValidationError
from app.models.ad import AdCreate, AdUpdate, AdPatch, AdType, AdStatus


# --- Helper: validni osnovni podaci ---
def valid_payload(**overrides):
    base = {
        "company_id": 1,
        "title": "Software Engineer Internship",
        "type": AdType.internship,
        "field": "Informacione tehnologije",
        "location": "Sarajevo",
        "description": "Detaljan opis oglasa sa dovoljno informacija.",
        "deadline": date.today() + timedelta(days=1),  # Sutra (granični ispravan slučaj)
        "duration_months": 3,
        "compensation": 500.0,
        "currency": "BAM",
        "spots": 2,
        "requirements": "Poznavanje Pythona.",
        "benefits": "Mentorstvo."
    }
    base.update(overrides)
    return base


# ============================================================
# 1. AdCreate — SVI EDGE CASE-OVI
# ============================================================

class TestAdCreateEdgeCases:

    def test_valid_minimal_allowed_values(self):
        """Testira najniže dozvoljene granične vrijednosti (1 mjesec, 0 kompenzacija, 1 mjesto)."""
        ad = AdCreate(**valid_payload(
            duration_months=1,    # Minimum je 1
            compensation=0.0,     # Može biti besplatno (0.0)
            spots=1               # Minimum je 1 mjesto
        ))
        assert ad.duration_months == 1
        assert ad.compensation == 0.0
        assert ad.spots == 1

    def test_title_whitespace_stripping(self):
        """Testira da li validator čisti razmake i ostavlja ispravan tekst."""
        ad = AdCreate(**valid_payload(title="   Razvojem Softvera   "))
        assert ad.title == "Razvojem Softvera"

    def test_title_blank_after_strip_should_fail(self):
        """Testira string koji ima samo razmake i nakon strip() postaje prazan."""
        with pytest.raises(ValidationError) as exc:
            AdCreate(**valid_payload(title="     "))
        assert "Field cannot be blank." in str(exc.value)

    def test_deadline_exactly_today_should_fail(self):
        """Testira granicu datuma: danas je neispravno (mora biti isključivo budućnost)."""
        with pytest.raises(ValidationError) as exc:
            AdCreate(**valid_payload(deadline=date.today()))
        assert "Deadline must be a future date." in str(exc.value)

    def test_deadline_past_should_fail(self):
        """Testira datum u prošlosti."""
        past_date = date.today() - timedelta(days=1)
        with pytest.raises(ValidationError):
            AdCreate(**valid_payload(deadline=past_date))

    def test_duration_just_below_minimum_should_fail(self):
        """Testira trajanje 0 mjeseci (granica ispod minimuma)."""
        with pytest.raises(ValidationError) as exc:
            AdCreate(**valid_payload(duration_months=0))
        assert "Duration must be at least 1 month." in str(exc.value)

    def test_compensation_just_below_zero_should_fail(self):
        """Testira negativnu kompenzaciju (npr. -0.01)."""
        with pytest.raises(ValidationError) as exc:
            AdCreate(**valid_payload(compensation=-0.01))
        assert "Compensation cannot be negative." in str(exc.value)

    def test_currency_missing_when_compensation_is_present_should_fail(self):
        """Testira među-zavisnost: ako ima para, valuta ne smije biti prazna/None."""
        with pytest.raises(ValidationError) as exc:
            AdCreate(**valid_payload(compensation=100.0, currency=""))
        assert "Currency is required when compensation is set." in str(exc.value)

    def test_currency_can_be_none_if_no_compensation(self):
        """Testira među-zavisnost: ako nema kompenzacije, valuta može biti prazna."""
        ad = AdCreate(**valid_payload(compensation=None, currency=None))
        assert ad.compensation is None
        assert ad.currency is None

    def test_spots_just_below_minimum_should_fail(self):
        """Testira 0 mjesta (granica ispod minimuma)."""
        with pytest.raises(ValidationError) as exc:
            AdCreate(**valid_payload(spots=0))
        assert "Number of spots must be at least 1." in str(exc.value)


# ============================================================
# 2. AdUpdate — SVI EDGE CASE-OVI
# ============================================================

class TestAdUpdateEdgeCases:

    def test_valid_update_full_payload(self):
        """Provjerava da AdUpdate radi kada su poslana sva obavezna polja (bez company_id)."""
        payload = valid_payload()
        payload.pop("company_id")  # AdUpdate nema company_id
        update = AdUpdate(**payload)
        assert update.title == "Software Engineer Internship"

    def test_update_blank_field_should_fail(self):
        payload = valid_payload()
        payload.pop("company_id")
        payload["location"] = "   "  # Samo razmaci
        with pytest.raises(ValidationError):
            AdUpdate(**payload)

    def test_update_missing_currency_with_compensation_should_fail(self):
        """Provjerava da li model_validator radi i na AdUpdate klasi."""
        payload = valid_payload()
        payload.pop("company_id")
        payload["compensation"] = "300.0"
        payload["currency"] = ""  # Prazno
        with pytest.raises(ValidationError) as exc:
            AdUpdate(**payload)
        assert "Currency is required when compensation is set." in str(exc.value)


# ============================================================
# 3. AdPatch — PARCIJALNI UPDATE EDGE CASE-OVI (Veoma važno!)
# ============================================================

class TestAdPatchEdgeCases:

    def test_patch_with_explicit_none_values(self):
        """
        KRITIČAN EDGE CASE: Pošto su polja u AdPatch opciona (Optional), 
        validatori ne smiju puknuti (Crash) ako im se eksplicitno proslijedi None.
        """
        patch = AdPatch(
            title=None, 
            deadline=None, 
            duration_months=None, 
            compensation=None, 
            spots=None
        )
        assert patch.title is None
        assert patch.deadline is None
        assert patch.spots is None

    def test_patch_valid_partial_fields(self):
        """Testira slanje samo nekih polja."""
        patch = AdPatch(title="Novi Naslov", spots=5)
        assert patch.title == "Novi Naslov"
        assert patch.spots == 5
        assert patch.deadline is None  # Ostala polja moraju ostati None

    def test_patch_blank_title_should_fail(self):
        """Ako se title ipak pošalje kao string, ne smije biti prazan nakon strip-a."""
        with pytest.raises(ValidationError):
            AdPatch(title="     ")

    def test_patch_invalid_deadline_today_should_fail(self):
        """Ako se deadline pošalje, mora pratiti pravilo budućeg datuma."""
        with pytest.raises(ValidationError):
            AdPatch(deadline=date.today())

    def test_patch_invalid_spots_should_fail(self):
        with pytest.raises(ValidationError):
            AdPatch(spots=0)

    def test_patch_invalid_compensation_should_fail(self):
        with pytest.raises(ValidationError):
            AdPatch(compensation=-5.0)