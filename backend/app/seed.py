from datetime import date, timedelta

from sqlmodel import Session, select

from app.core.security import hash_password
from app.database import create_db_and_tables, engine
from app.models.ad import Ad, AdStatus, AdType
from app.models.company import Company, CompanyStatus
from app.models.user import User, UserRole


def _build_companies() -> list[Company]:
    companies_data = [
        {
            "company_name": "Telekom Demo 1 d.o.o.",
            "description": "Kompanija za test podatke i demo oglase za studente.",
            "website_url": "https://demo1.example.com",
            "logo_url": "https://placehold.co/200x200/demo-1.png",
            "email": "demo1@company.test",
            "phone_number": "+38761100001",
            "jib": "1234567890001",
            "address": "Adresa 1, Sarajevo",
        },
        {
            "company_name": "Telekom Demo 2 d.o.o.",
            "description": "Kompanija za test podatke i demo oglase za studente.",
            "website_url": "https://demo2.example.com",
            "logo_url": "https://placehold.co/200x200/demo-2.png",
            "email": "demo2@company.test",
            "phone_number": "+38761100002",
            "jib": "1234567890002",
            "address": "Adresa 2, Sarajevo",
        },
        {
            "company_name": "Telekom Demo 3 d.o.o.",
            "description": "Kompanija za test podatke i demo oglase za studente.",
            "website_url": "https://demo3.example.com",
            "logo_url": "https://placehold.co/200x200/demo-3.png",
            "email": "demo3@company.test",
            "phone_number": "+38761100003",
            "jib": "1234567890003",
            "address": "Adresa 3, Mostar",
        },
        {
            "company_name": "Telekom Demo 4 d.o.o.",
            "description": "Kompanija za test podatke i demo oglase za studente.",
            "website_url": "https://demo4.example.com",
            "logo_url": "https://placehold.co/200x200/demo-4.png",
            "email": "demo4@company.test",
            "phone_number": "+38761100004",
            "jib": "1234567890004",
            "address": "Adresa 4, Tuzla",
        },
        {
            "company_name": "Telekom Demo 5 d.o.o.",
            "description": "Kompanija za test podatke i demo oglase za studente.",
            "website_url": "https://demo5.example.com",
            "logo_url": "https://placehold.co/200x200/demo-5.png",
            "email": "demo5@company.test",
            "phone_number": "+38761100005",
            "jib": "1234567890005",
            "address": "Adresa 5, Zenica",
        },
        {
            "company_name": "Telekom Demo 6 d.o.o.",
            "description": "Kompanija za test podatke i demo oglase za studente.",
            "website_url": "https://demo6.example.com",
            "logo_url": "https://placehold.co/200x200/demo-6.png",
            "email": "demo6@company.test",
            "phone_number": "+38761100006",
            "jib": "1234567890006",
            "address": "Adresa 6, Bihać",
        },
        {
            "company_name": "Telekom Demo 7 d.o.o.",
            "description": "Kompanija za test podatke i demo oglase za studente.",
            "website_url": "https://demo7.example.com",
            "logo_url": "https://placehold.co/200x200/demo-7.png",
            "email": "demo7@company.test",
            "phone_number": "+38761100007",
            "jib": "1234567890007",
            "address": "Adresa 7, Banja Luka",
        },
        {
            "company_name": "Telekom Demo 8 d.o.o.",
            "description": "Kompanija za test podatke i demo oglase za studente.",
            "website_url": "https://demo8.example.com",
            "logo_url": "https://placehold.co/200x200/demo-8.png",
            "email": "demo8@company.test",
            "phone_number": "+38761100008",
            "jib": "1234567890008",
            "address": "Adresa 8, Doboj",
        },
        {
            "company_name": "Telekom Demo 9 d.o.o.",
            "description": "Kompanija za test podatke i demo oglase za studente.",
            "website_url": "https://demo9.example.com",
            "logo_url": "https://placehold.co/200x200/demo-9.png",
            "email": "demo9@company.test",
            "phone_number": "+38761100009",
            "jib": "1234567890010",
            "address": "Adresa 9, Prijedor",
        },
        {
            "company_name": "Telekom Demo 10 d.o.o.",
            "description": "Kompanija za test podatke i demo oglase za studente.",
            "website_url": "https://demo10.example.com",
            "logo_url": "https://placehold.co/200x200/demo-10.png",
            "email": "demo10@company.test",
            "phone_number": "+38761100010",
            "jib": "1234567890011",
            "address": "Adresa 10, Trebinje",
        },
    ]

    return [
        Company(
            **company_data,
            hashed_password=hash_password("Demo12345!"),
            status=CompanyStatus.approved,
        )
        for company_data in companies_data
    ]


def _build_prakse_ads(companies: list[Company]) -> list[Ad]:
    ad_templates = [
        ("Praksa u mrežnom planiranju", "Telekomunikacije", "Sarajevo", 2, 250.0),
        ("Praksa u podršci korisnicima", "Customer Support", "Zenica", 3, 300.0),
        ("Praksa u razvoju web aplikacija", "Web razvoj", "Doboj", 4, 350.0),
        ("Praksa u analizi podataka", "Data analytics", "Sarajevo", 2, 400.0),
        ("Praksa u testiranju softvera", "QA / Testing", "Mostar", 3, 280.0),
        ("Praksa u administraciji sistema", "System Administration", "Banja Luka", 2, 320.0),
        ("Praksa u mrežnoj sigurnosti", "Cyber security", "Tuzla", 4, 450.0),
        ("Praksa u mobilnim aplikacijama", "Mobile development", "Bihać", 3, 380.0),
        ("Praksa u DevOps alatima", "DevOps", "Prijedor", 2, 420.0),
        ("Praksa u poslovnoj analizi", "Business analysis", "Trebinje", 3, 360.0),
    ]

    ads: list[Ad] = []
    for index, (title, field, location, duration_months, compensation) in enumerate(ad_templates):
        ads.append(
            Ad(
                company_id=companies[index].id,
                title=title,
                type=AdType.internship,
                field=field,
                location=location,
                description=f"Demo praksa broj {index + 1} za testiranje frontend liste i filtera.",
                deadline=date.today() + timedelta(days=30 + index),
                duration_months=duration_months,
                compensation=compensation,
                currency="BAM",
                spots=1 + (index % 3),
                requirements="Osnovno poznavanje rada na računaru i želja za učenjem.",
                benefits="Mentorstvo, praktičan rad i sertifikat po završetku.",
                status=AdStatus.active,
            )
        )

    return ads


def seed_prakse_demo_data(session: Session) -> dict[str, int]:
    existing_company = session.exec(
        select(Company).where(Company.email == "demo1@company.test")
    ).first()
    if existing_company:
        companies_count = len(session.exec(select(Company)).all())
        ads_count = len(session.exec(select(Ad)).all())
        return {"companies": companies_count, "ads": ads_count, "created": 0}

    companies = _build_companies()
    session.add_all(companies)
    session.commit()

    for company in companies:
        session.refresh(company)

    ads = _build_prakse_ads(companies)
    session.add_all(ads)
    session.commit()

    return {"companies": len(companies), "ads": len(ads), "created": len(companies) + len(ads)}


def seed_demo_data(session: Session) -> dict[str, int]:
    return seed_prakse_demo_data(session)


def ensure_admin_user(session: Session) -> dict[str, bool]:
    admin_email = "elnur@tkstudenthub.local"
    existing_admin = session.exec(
        select(User).where(User.email == admin_email)
    ).first()

    if existing_admin:
        return {"created": False}

    admin = User(
        email=admin_email,
        full_name="Elnur",
        password_hash=hash_password("elnur1234"),
        role=UserRole.admin,
    )
    session.add(admin)
    session.commit()

    return {"created": True}


def main() -> None:
    create_db_and_tables()

    with Session(engine) as session:
        result = seed_prakse_demo_data(session)

    print(
        f"Seed zavrsen: {result['companies']} kompanija, {result['ads']} praksi, ukupno {result['created']} novih redova."
    )


if __name__ == "__main__":
    main()