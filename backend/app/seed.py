from datetime import date, datetime, timedelta, timezone

from sqlmodel import Session, select

from app.core.security import hash_password
from app.database import create_db_and_tables, engine
from app.models.user import User, UserRole
from app.models.company import Company, CompanyStatus
from app.models.ad import Ad, AdStatus, AdType
from app.models.application import Application, ApplicationStatus
from app.models.notification import Notification, NotificationType
from app.models.ad_bookmark import AdBookmark


def _build_users() -> list[User]:
    """Create 10 test users."""
    users_data = [
        {"email": "admin@test.local", "full_name": "Admin User", "role": UserRole.admin},
        {"email": "member1@test.local", "full_name": "Member One", "role": UserRole.member},
        {"email": "member2@test.local", "full_name": "Member Two", "role": UserRole.member},
        {"email": "member3@test.local", "full_name": "Member Three", "role": UserRole.member},
        {"email": "member4@test.local", "full_name": "Member Four", "role": UserRole.member},
        {"email": "member5@test.local", "full_name": "Member Five", "role": UserRole.member},
        {"email": "member6@test.local", "full_name": "Member Six", "role": UserRole.member},
        {"email": "member7@test.local", "full_name": "Member Seven", "role": UserRole.member},
        {"email": "member8@test.local", "full_name": "Member Eight", "role": UserRole.member},
        {"email": "member9@test.local", "full_name": "Member Nine", "role": UserRole.member},
        {"email": "member10@test.local","full_name": "Member Ten",    "role": UserRole.member},
    ]

    return [
        User(
            email=data["email"],
            full_name=data["full_name"],
            password_hash=hash_password("password123"),
            role=data["role"],
        )
        for data in users_data
    ]


def _build_companies() -> list[Company]:
    """Create 10 test companies."""
    companies_data = [
        {
            "company_name": "Tech Solutions d.o.o.",
            "description": "Leading IT solutions provider.",
            "website_url": "https://techsolutions.ba",
            "logo_path": "logos/tech1.png",
            "email": "hr@techsolutions.ba",
            "phone_number": "+38761111111",
            "tin": "1111111111111",
            "address": "Sarajevo, Zmaja od Bosne 1",
        },
        {
            "company_name": "Digital Innovations d.o.o.",
            "description": "Digital transformation experts.",
            "website_url": "https://digitalinnovations.ba",
            "logo_path": "logos/digital1.png",
            "email": "careers@digitalinnovations.ba",
            "phone_number": "+38761111112",
            "tin": "1111111111112",
            "address": "Sarajevo, Obala Kulina Bana 2",
        },
        {
            "company_name": "Cloud Systems d.o.o.",
            "description": "Cloud infrastructure and services.",
            "website_url": "https://cloudsystems.ba",
            "logo_path": "logos/cloud1.png",
            "email": "jobs@cloudsystems.ba",
            "phone_number": "+38761111113",
            "tin": "1111111111113",
            "address": "Zenica, Cara Dusana 3",
        },
        {
            "company_name": "Mobile First d.o.o.",
            "description": "Mobile app development company.",
            "website_url": "https://mobilefirst.ba",
            "logo_path": "logos/mobile1.png",
            "email": "recruitment@mobilefirst.ba",
            "phone_number": "+38761111114",
            "tin": "1111111111114",
            "address": "Tuzla, Kulina Bana 4",
        },
        {
            "company_name": "Data Analytics Pro d.o.o.",
            "description": "Business intelligence and analytics.",
            "website_url": "https://dataanalyticspro.ba",
            "logo_path": "logos/data1.png",
            "email": "hr@dataanalyticspro.ba",
            "phone_number": "+38761111115",
            "tin": "1111111111115",
            "address": "Mostar, Aleksa Santic 5",
        },
        {
            "company_name": "Security First d.o.o.",
            "description": "Cybersecurity and penetration testing.",
            "website_url": "https://securityfirst.ba",
            "logo_path": "logos/security1.png",
            "email": "careers@securityfirst.ba",
            "phone_number": "+38761111116",
            "tin": "1111111111116",
            "address": "Banja Luka, Drinska 6",
        },
        {
            "company_name": "DevOps Masters d.o.o.",
            "description": "Infrastructure automation and CI/CD.",
            "website_url": "https://devopsmasters.ba",
            "logo_path": "logos/devops1.png",
            "email": "jobs@devopsmasters.ba",
            "phone_number": "+38761111117",
            "tin": "1111111111117",
            "address": "Doboj, Baba Radisa 7",
        },
        {
            "company_name": "UI/UX Studio d.o.o.",
            "description": "User experience and interface design.",
            "website_url": "https://uiuxstudio.ba",
            "logo_path": "logos/uiux1.png",
            "email": "hello@uiuxstudio.ba",
            "phone_number": "+38761111118",
            "tin": "1111111111118",
            "address": "Bijeljina, Cara Aleksandra 8",
        },
        {
            "company_name": "Backend Specialists d.o.o.",
            "description": "Enterprise backend development.",
            "website_url": "https://backendspecialists.ba",
            "logo_path": "logos/backend1.png",
            "email": "recruitment@backendspecialists.ba",
            "phone_number": "+38761111119",
            "tin": "1111111111119",
            "address": "Trebinje, Nemanjina 9",
        },
        {
            "company_name": "QA Automation d.o.o.",
            "description": "Software testing and quality assurance.",
            "website_url": "https://qaautomation.ba",
            "logo_path": "logos/qa1.png",
            "email": "careers@qaautomation.ba",
            "phone_number": "+38761111120",
            "tin": "1111111111120",
            "address": "Bihac, Zivka Dakica 10",
        },
    ]

    return [
        Company(
            **data,
            hashed_password=hash_password("company123"),
            status=CompanyStatus.approved,
        )
        for data in companies_data
    ]


def _build_ads(companies: list[Company], users: list[User]) -> list[Ad]:
    """Create 10 test ads."""
    ad_templates = [
        {
            "title": "Junior Web Developer",
            "type": AdType.internship,
            "field": "Web Development",
            "location": "Sarajevo",
            "description": "Exciting opportunity to learn and grow as a web developer.",
            "deadline": 30,
            "duration_months": 3,
            "compensation": 300.0,
            "spots": 2,
        },
        {
            "title": "Backend Developer Internship",
            "type": AdType.internship,
            "field": "Backend Development",
            "location": "Zenica",
            "description": "Build scalable backend systems with Python and Django.",
            "deadline": 35,
            "duration_months": 4,
            "compensation": 350.0,
            "spots": 1,
        },
        {
            "title": "QA Engineer",
            "type": AdType.internship,
            "field": "Quality Assurance",
            "location": "Tuzla",
            "description": "Test and ensure software quality and reliability.",
            "deadline": 40,
            "duration_months": 3,
            "compensation": 280.0,
            "spots": 3,
        },
        {
            "title": "Data Analytics Internship",
            "type": AdType.internship,
            "field": "Data Analytics",
            "location": "Mostar",
            "description": "Analyze business data and generate insights.",
            "deadline": 25,
            "duration_months": 2,
            "compensation": 400.0,
            "spots": 1,
        },
        {
            "title": "Cybersecurity Specialist",
            "type": AdType.internship,
            "field": "Cybersecurity",
            "location": "Banja Luka",
            "description": "Learn cybersecurity best practices and protocols.",
            "deadline": 45,
            "duration_months": 6,
            "compensation": 450.0,
            "spots": 2,
        },
        {
            "title": "DevOps Engineer Intern",
            "type": AdType.internship,
            "field": "DevOps",
            "location": "Doboj",
            "description": "Work on CI/CD pipelines and infrastructure automation.",
            "deadline": 32,
            "duration_months": 4,
            "compensation": 420.0,
            "spots": 1,
        },
        {
            "title": "UI/UX Designer",
            "type": AdType.internship,
            "field": "Design",
            "location": "Bijeljina",
            "description": "Create beautiful and user-friendly interfaces.",
            "deadline": 28,
            "duration_months": 3,
            "compensation": 330.0,
            "spots": 2,
        },
        {
            "title": "Mobile App Developer",
            "type": AdType.internship,
            "field": "Mobile Development",
            "location": "Trebinje",
            "description": "Develop iOS and Android applications.",
            "deadline": 38,
            "duration_months": 5,
            "compensation": 380.0,
            "spots": 1,
        },
        {
            "title": "Full Stack Developer",
            "type": AdType.internship,
            "field": "Full Stack",
            "location": "Bihac",
            "description": "Work on both frontend and backend systems.",
            "deadline": 42,
            "duration_months": 4,
            "compensation": 370.0,
            "spots": 2,
        },
        {
            "title": "Software Engineer Apprenticeship",
            "type": AdType.internship,
            "field": "Software Engineering",
            "location": "Sarajevo",
            "description": "Comprehensive software engineering training program.",
            "deadline": 50,
            "duration_months": 6,
            "compensation": 400.0,
            "spots": 3,
        },
    ]

    ads = []
    for index, template in enumerate(ad_templates):
        ads.append(
            Ad(
                company_id=companies[index].id,
                approved_by=users[0].id,  # Admin approves
                title=template["title"],
                type=template["type"],
                field=template["field"],
                location=template["location"],
                description=template["description"],
                deadline=date.today() + timedelta(days=template["deadline"]),
                duration_months=template["duration_months"],
                compensation=template["compensation"],
                currency="BAM",
                spots=template["spots"],
                requirements="Strong motivation and willingness to learn.",
                benefits="Mentorship, practical experience, and certificate.",
                admin_comment="Approved for posting.",
                status=AdStatus.active,
            )
        )

    return ads


# Distribution pattern for 10 applications per ad:
#   index 0 -> pending   (no feedback)
#   index 1 -> pending   (no feedback)
#   index 2 -> pending   (no feedback)
#   index 3 -> pending   (no feedback)
#   index 4 -> accepted  (positive feedback)
#   index 5 -> accepted  (positive feedback)
#   index 6 -> accepted  (positive feedback)
#   index 7 -> rejected  (constructive feedback)
#   index 8 -> rejected  (constructive feedback)
#   index 9 -> rejected  (constructive feedback)
_APP_STATUS_PATTERN = [
    ApplicationStatus.pending,
    ApplicationStatus.pending,
    ApplicationStatus.pending,
    ApplicationStatus.pending,
    ApplicationStatus.accepted,
    ApplicationStatus.accepted,
    ApplicationStatus.accepted,
    ApplicationStatus.rejected,
    ApplicationStatus.rejected,
    ApplicationStatus.rejected,
]

_ACCEPTED_FEEDBACK = [
    "Odlican kandidat, pokazuje veliko interesovanje i potencijal.",
    "Profil kandidata odgovara svim trazenim kriterijima.",
    "Impresivno motivacijsko pismo i relevantno iskustvo.",
]

_REJECTED_FEEDBACK = [
    "Nedovoljno iskustvo u trazenim tehnologijama.",
    "Kandidat ne ispunjava minimalne uslove za poziciju.",
    "Pozicija je popunjena prikladnijim kandidatom.",
]


def _build_applications(users: list[User], ads: list[Ad]) -> list[Application]:
    """Create 10 applications per ad (100 total) with varied statuses."""
    # members are users[1..9] — skip admin at index 0
    members = users[1:]
    applications = []
    global_index = 0

    for ad in ads:
        for slot in range(10):
            status = _APP_STATUS_PATTERN[slot]
            user = members[slot % len(members)]

            if status == ApplicationStatus.accepted:
                feedback = _ACCEPTED_FEEDBACK[slot % len(_ACCEPTED_FEEDBACK)]
            elif status == ApplicationStatus.rejected:
                feedback = _REJECTED_FEEDBACK[slot % len(_REJECTED_FEEDBACK)]
            else:
                feedback = None

            applications.append(
                Application(
                    user_id=user.id,
                    ad_id=ad.id,
                    cv_path=f"uploads/applications/cv_{global_index}.pdf",
                    motivational_letter_path=f"uploads/applications/letter_{global_index}.pdf",
                    linkedin_url=f"https://linkedin.com/in/user{global_index}" if global_index % 2 == 0 else None,
                    phone=f"+38761{200000 + global_index:06d}",
                    status=status,
                    admin_feedback=feedback,
                    is_archived=False,
                )
            )
            global_index += 1

    return applications


def _build_notifications(users: list[User]) -> list[Notification]:
    """Create 10 test notifications."""
    notification_types = [
        NotificationType.NEW_OPPORTUNITY,
        NotificationType.STATUS_CHANGE,
        NotificationType.DEADLINE_EXPIRING,
    ]
    messages = [
        "New job opportunity matching your profile!",
        "Your application status has been updated.",
        "Application deadline is expiring soon!",
        "New internship posted in your field.",
        "Your profile has been reviewed.",
        "Congratulations! You've been shortlisted.",
        "Thank you for applying.",
        "New networking event available.",
        "Your CV has been downloaded.",
        "Mentor assignment confirmation.",
    ]

    notifications = []
    for index in range(10):
        notifications.append(
            Notification(
                user_id=users[(index + 1) % len(users)].id,  # Skip admin
                text=messages[index],
                type=notification_types[index % len(notification_types)],
                is_read=index % 2 == 0,
            )
        )

    return notifications


def _build_bookmarks(users: list[User], ads: list[Ad]) -> list[AdBookmark]:
    """Create 10 test bookmarks."""
    bookmarks = []
    for index in range(10):
        bookmarks.append(
            AdBookmark(
                user_id=users[(index + 1) % len(users)].id,  # Skip admin
                ad_id=ads[index].id,
            )
        )

    return bookmarks


def seed_demo_data(session: Session) -> dict[str, int]:
    """Seed database with demo data."""
    # Check if data already exists
    existing_user = session.exec(select(User).where(User.email == "admin@test.local")).first()
    if existing_user:
        user_count = len(session.exec(select(User)).all())
        company_count = len(session.exec(select(Company)).all())
        ad_count = len(session.exec(select(Ad)).all())
        app_count = len(session.exec(select(Application)).all())
        notif_count = len(session.exec(select(Notification)).all())
        bookmark_count = len(session.exec(select(AdBookmark)).all())
        return {
            "users": user_count,
            "companies": company_count,
            "ads": ad_count,
            "applications": app_count,
            "notifications": notif_count,
            "bookmarks": bookmark_count,
            "created": 0,
        }

    # Create entities
    users = _build_users()
    session.add_all(users)
    session.commit()
    for user in users:
        session.refresh(user)

    companies = _build_companies()
    session.add_all(companies)
    session.commit()
    for company in companies:
        session.refresh(company)

    ads = _build_ads(companies, users)
    session.add_all(ads)
    session.commit()
    for ad in ads:
        session.refresh(ad)

    applications = _build_applications(users, ads)
    session.add_all(applications)
    session.commit()

    notifications = _build_notifications(users)
    session.add_all(notifications)
    session.commit()

    bookmarks = _build_bookmarks(users, ads)
    session.add_all(bookmarks)
    session.commit()

    total = len(users) + len(companies) + len(ads) + len(applications) + len(notifications) + len(bookmarks)

    return {
        "users": len(users),
        "companies": len(companies),
        "ads": len(ads),
        "applications": len(applications),
        "notifications": len(notifications),
        "bookmarks": len(bookmarks),
        "created": total,
    }


def main() -> None:
    """Main seed function."""
    create_db_and_tables()

    with Session(engine) as session:
        result = seed_demo_data(session)

    print(
        f"Seed zavrsen:\n"
        f"  - {result['users']} korisnika\n"
        f"  - {result['companies']} kompanija\n"
        f"  - {result['ads']} oglasa\n"
        f"  - {result['applications']} aplikacija\n"
        f"  - {result['notifications']} notifikacija\n"
        f"  - {result['bookmarks']} bookmarkova\n"
        f"  - ukupno {result['created']} novih redova"
    )


if __name__ == "__main__":
    main()