import pytest
from pydantic import ValidationError
from app.models.company import CompanyCreate, CompanyUpdate


# --- Helper: validni podaci za CompanyCreate ---

def valid_payload(**overrides):
    base = {
        "company_name": "Test Kompanija d.o.o.",
        "description": "Ovo je validna kompanija sa dovoljno dugim opisom.",
        "website_url": "https://test.ba",
        "email": "info@test.ba",
        "phone_number": "+38761000000",
        "tin": "1234567890123",
        "address": "Ulica bb, Sarajevo",
        "password": "sigurna123",
    }
    base.update(overrides)
    return base


# ============================================================
# CompanyCreate — happy path
# ============================================================

class TestCompanyCreateValid:

    def test_valid_company_create(self):
        company = CompanyCreate(**valid_payload())
        assert company.company_name == "Test Kompanija d.o.o."
        assert company.email == "info@test.ba"
        assert company.tin == "1234567890123"

    def test_valid_minimal_company_name(self):
        # Tačno 2 karaktera — granični slučaj koji treba proći
        company = CompanyCreate(**valid_payload(company_name="AB"))
        assert company.company_name == "AB"

    def test_valid_minimal_description(self):
        # Tačno 10 karaktera
        company = CompanyCreate(**valid_payload(description="1234567890"))
        assert company.description == "1234567890"

    def test_valid_website_url_with_path(self):
        company = CompanyCreate(**valid_payload(website_url="https://test.ba/o-nama"))
        assert company.website_url == "https://test.ba/o-nama"

    def test_valid_website_url_with_subdomain(self):
        company = CompanyCreate(**valid_payload(website_url="https://www.test.ba"))
        assert company.website_url == "https://www.test.ba"

    def test_valid_email_with_plus(self):
        company = CompanyCreate(**valid_payload(email="user+tag@test.ba"))
        assert company.email == "user+tag@test.ba"

    def test_valid_email_with_dots(self):
        company = CompanyCreate(**valid_payload(email="ime.prezime@kompanija.com"))
        assert company.email == "ime.prezime@kompanija.com"

    def test_valid_tin_exactly_13_digits(self):
        company = CompanyCreate(**valid_payload(tin="1234567890123"))
        assert company.tin == "1234567890123"

    def test_valid_password_exactly_8_chars(self):
        # Tačno 8 karaktera — granični slučaj koji treba proći
        company = CompanyCreate(**valid_payload(password="12345678"))
        assert company.password == "12345678"

    def test_valid_address_longer_than_2(self):
        company = CompanyCreate(**valid_payload(address="ABC"))
        assert company.address == "ABC"


# ============================================================
# CompanyCreate — company_name validacija
# ============================================================

class TestCompanyCreateName:

    def test_name_too_short_one_char(self):
        with pytest.raises(ValidationError) as exc:
            CompanyCreate(**valid_payload(company_name="A"))
        assert "Company name must be at least 2 characters" in str(exc.value)

    def test_name_empty_string(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(company_name=""))

    def test_name_only_whitespace(self):
        # Whitespace jedino — strip() čini ovo prekratkim
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(company_name="   "))

    def test_name_whitespace_padding_valid(self):
        # Sa paddingom ali sadržaj je duži od 2 — ovisi o implementaciji strip()
        company = CompanyCreate(**valid_payload(company_name="  AB  "))
        assert company.company_name == "  AB  "


# ============================================================
# CompanyCreate — description validacija
# ============================================================

class TestCompanyCreateDescription:

    def test_description_too_short(self):
        with pytest.raises(ValidationError) as exc:
            CompanyCreate(**valid_payload(description="Kratko"))
        assert "Description must be at least 10 characters" in str(exc.value)

    def test_description_empty_string(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(description=""))

    def test_description_exactly_9_chars(self):
        # Jedan ispod minimuma
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(description="123456789"))

    def test_description_only_whitespace(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(description="          "))


# ============================================================
# CompanyCreate — website_url validacija
# ============================================================

class TestCompanyCreateWebsiteUrl:

    def test_url_without_https(self):
        with pytest.raises(ValidationError) as exc:
            CompanyCreate(**valid_payload(website_url="http://test.ba"))
        assert "Website URL must be in format" in str(exc.value)

    def test_url_without_protocol(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(website_url="test.ba"))

    def test_url_empty_string(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(website_url=""))

    def test_url_only_https(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(website_url="https://"))

    def test_url_no_tld(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(website_url="https://test"))

    def test_url_ftp_protocol(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(website_url="ftp://test.ba"))

    def test_url_with_spaces(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(website_url="https://te st.ba"))


# ============================================================
# CompanyCreate — email validacija
# ============================================================

class TestCompanyCreateEmail:

    def test_email_without_at(self):
        with pytest.raises(ValidationError) as exc:
            CompanyCreate(**valid_payload(email="infotest.ba"))
        assert "Email is not in a valid format" in str(exc.value)

    def test_email_without_domain(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(email="info@"))

    def test_email_without_local_part(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(email="@test.ba"))

    def test_email_empty_string(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(email=""))

    def test_email_without_tld(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(email="info@test"))

    def test_email_with_spaces(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(email="in fo@test.ba"))

    def test_email_double_at(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(email="info@@test.ba"))


# ============================================================
# CompanyCreate — TIN validacija
# ============================================================

class TestCompanyCreateTin:

    def test_tin_too_short(self):
        with pytest.raises(ValidationError) as exc:
            CompanyCreate(**valid_payload(tin="123456"))
        assert "TIN must be exactly 13 digits" in str(exc.value)

    def test_tin_too_long(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(tin="12345678901234"))

    def test_tin_contains_letters(self):
        with pytest.raises(ValidationError) as exc:
            CompanyCreate(**valid_payload(tin="1234567890abc"))
        assert "TIN must contain only digits" in str(exc.value)

    def test_tin_empty_string(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(tin=""))

    def test_tin_with_spaces(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(tin="123 456 789 012 3"))

    def test_tin_with_dashes(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(tin="1234567-890123"))

    def test_tin_exactly_12_digits(self):
        # Jedan ispod minimuma
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(tin="123456789012"))

    def test_tin_exactly_14_digits(self):
        # Jedan iznad maksimuma
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(tin="12345678901234"))


# ============================================================
# CompanyCreate — address validacija
# ============================================================

class TestCompanyCreateAddress:

    def test_address_too_short_one_char(self):
        with pytest.raises(ValidationError) as exc:
            CompanyCreate(**valid_payload(address="A"))
        assert "Address must be longer than 2 characters" in str(exc.value)

    def test_address_exactly_2_chars(self):
        # Tačno 2 karaktera — nije duže od 2, treba pasti
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(address="AB"))

    def test_address_empty_string(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(address=""))

    def test_address_only_whitespace(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(address="  "))


# ============================================================
# CompanyCreate — password validacija
# ============================================================

class TestCompanyCreatePassword:

    def test_password_too_short(self):
        with pytest.raises(ValidationError) as exc:
            CompanyCreate(**valid_payload(password="kratko"))
        assert "Password must be at least 8 characters" in str(exc.value)

    def test_password_empty_string(self):
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(password=""))

    def test_password_exactly_7_chars(self):
        # Jedan ispod minimuma
        with pytest.raises(ValidationError):
            CompanyCreate(**valid_payload(password="1234567"))

    def test_password_with_spaces(self):
        # Razmaci su dozvoljeni — samo dužina se provjerava
        company = CompanyCreate(**valid_payload(password="lozinka sa razmakom"))
        assert company.password == "lozinka sa razmakom"

    def test_password_only_numbers(self):
        company = CompanyCreate(**valid_payload(password="12345678"))
        assert company.password == "12345678"

    def test_password_special_chars(self):
        company = CompanyCreate(**valid_payload(password="!@#$%^&*"))
        assert company.password == "!@#$%^&*"


# ============================================================
# CompanyUpdate — parcijalni update (sva polja su Optional)
# ============================================================

class TestCompanyUpdateValid:

    def test_update_only_name(self):
        update = CompanyUpdate(company_name="Nova Kompanija")
        assert update.company_name == "Nova Kompanija"
        assert update.email is None

    def test_update_only_email(self):
        update = CompanyUpdate(email="novi@email.ba")
        assert update.email == "novi@email.ba"

    def test_update_multiple_fields(self):
        update = CompanyUpdate(
            company_name="Ažurirana Kompanija",
            email="azurirani@email.ba",
            address="Nova adresa 123"
        )
        assert update.company_name == "Ažurirana Kompanija"
        assert update.email == "azurirani@email.ba"

    def test_update_empty_payload(self):
        # Sve None — validan jer je sve Optional
        update = CompanyUpdate()
        assert update.company_name is None
        assert update.email is None
        assert update.tin is None


class TestCompanyUpdateInvalid:

    def test_update_invalid_email(self):
        with pytest.raises(ValidationError):
            CompanyUpdate(email="nijevalidan")

    def test_update_invalid_tin(self):
        with pytest.raises(ValidationError):
            CompanyUpdate(tin="123")

    def test_update_invalid_website_url(self):
        with pytest.raises(ValidationError):
            CompanyUpdate(website_url="http://test.ba")

    def test_update_invalid_company_name_too_short(self):
        with pytest.raises(ValidationError):
            CompanyUpdate(company_name="A")

    def test_update_invalid_description_too_short(self):
        with pytest.raises(ValidationError):
            CompanyUpdate(description="Kratko")

    def test_update_invalid_address_too_short(self):
        with pytest.raises(ValidationError):
            CompanyUpdate(address="AB")

    def test_update_invalid_tin_with_letters(self):
        with pytest.raises(ValidationError):
            CompanyUpdate(tin="abc4567890123")