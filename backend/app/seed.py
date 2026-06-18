from datetime import date, datetime, timedelta, timezone

from sqlmodel import SQLModel, Session, select

from app.core.security import hash_password
from app.database import create_db_and_tables, engine
from app.models.user import User, UserRole
from app.models.company import Company, CompanyStatus
from app.models.ad import Ad, AdStatus, AdType
from app.models.application import Application, ApplicationStatus
from app.models.notification import Notification, NotificationType
from app.models.ad_bookmark import AdBookmark
from app.models.forum import (
    ForumCategory,
    ForumTopic,
    ForumComment,
    ForumTag,
    ForumTopicTag,
    ForumCommentVote,
)


# ---------------------------------------------------------------------------
# Forum seed data
# ---------------------------------------------------------------------------

FORUM_CATEGORIES = [
    {
        "name": "Opšta diskusija",
        "color": "#ff7a00",
        "description": "Opšte teme vezane za studij i studentski život.",
    },
    {
        "name": "Pomoć sa predmetima",
        "color": "#2563eb",
        "description": "Pitanja, objašnjenja i pomoć oko predmeta.",
    },
    {
        "name": "Studijske grupe",
        "color": "#16a34a",
        "description": "Organizacija grupa za učenje i pripremu ispita.",
    },
    {
        "name": "Praksa i posao",
        "color": "#9333ea",
        "description": "Diskusije o praksama, poslovima i karijeri.",
    },
    {
        "name": "Projekti",
        "color": "#dc2626",
        "description": "Ideje, pitanja i pomoć oko studentskih projekata.",
    },
    {
        "name": "Off-Topic",
        "color": "#6b7280",
        "description": "Neformalne teme i razgovori van nastave.",
    },
]


def seed_forum_categories(session: Session) -> None:
    print("📂 Seeding forum kategorija...")
    for category_data in FORUM_CATEGORIES:
        existing = session.exec(
            select(ForumCategory).where(ForumCategory.name == category_data["name"])
        ).first()
        if existing:
            existing.color = category_data["color"]
            existing.description = category_data["description"]
            session.add(existing)
        else:
            session.add(ForumCategory(**category_data))
    session.commit()


def _get_or_create_forum_users(session: Session) -> list[User]:
    emails = ["forum.test@student.ba", "amra.begic@student.ba", "zijad.lekic@student.ba"]
    names = ["Forum Test Student", "Amra Begić", "Zijad Lekić"]
    users = []
    for email, name in zip(emails, names):
        user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            user = User(
                email=email,
                full_name=name,
                password_hash=hash_password("password123"),
            )
            session.add(user)
            session.commit()
            session.refresh(user)
        users.append(user)
    return users


def _get_or_create_tags(session: Session) -> dict:
    # Note: removed leading space from " hardware"
    tag_names = ["matematika", "programiranje", "fourier", "ispit", "hardware", "kafa"]
    tags_dict = {}
    for name in tag_names:
        tag = session.exec(select(ForumTag).where(ForumTag.name == name)).first()
        if not tag:
            tag = ForumTag(name=name)
            session.add(tag)
            session.commit()
            session.refresh(tag)
        tags_dict[name] = tag
    return tags_dict


def seed_forum_topics_and_comments(session: Session) -> None:
    users = _get_or_create_forum_users(session)
    main_user, student_user_1, student_user_2 = users[0], users[1], users[2]

    tags = _get_or_create_tags(session)
    categories = session.exec(select(ForumCategory)).all()

    if not categories:
        print("Kategorije nisu pronađene. Prvo pokrenite seed_forum_categories.")
        return

    print("Punjenje baze forum podacima (teme, tagovi, komentari, glasovi)...")

    for category in categories:
        # "Praksa i posao" ostaje prazna za testiranje UI stanja
        if category.name == "Praksa i posao":
            continue

        for i in range(1, 21):
            title_text = f"Tema broj {i} u kategoriji {category.name}"
            existing_topic = session.exec(
                select(ForumTopic).where(ForumTopic.title == title_text)
            ).first()

            if not existing_topic:
                time_offset = datetime.utcnow() - timedelta(days=21 - i, hours=i)
                topic = ForumTopic(
                    title=title_text,
                    content=(
                        f"Ovo je tekstualni sadržaj za testnu temu broj {i}. "
                        "Ovdje simuliramo dugački studentski tekst kako bismo provjerili "
                        "da li paginacija, filtriranje i detaljan prikaz rade glatko."
                    ),
                    category_id=category.id,
                    user_id=main_user.id,
                    views_count=i * 12,
                    created_at=time_offset,
                    is_deleted=False,
                )
                session.add(topic)
                session.commit()
                session.refresh(topic)

                if i == 1:
                    # Add tags
                    if category.name == "Pomoć sa predmetima":
                        session.add(ForumTopicTag(topic_id=topic.id, tag_id=tags["fourier"].id))
                        session.add(ForumTopicTag(topic_id=topic.id, tag_id=tags["matematika"].id))
                    elif category.name == "Projekti":
                        session.add(ForumTopicTag(topic_id=topic.id, tag_id=tags["programiranje"].id))
                    else:
                        session.add(ForumTopicTag(topic_id=topic.id, tag_id=tags["ispit"].id))

                    komentar_1 = ForumComment(
                        content=f"Ovo je prvi odgovor na temu '{topic.title}'. Slažem se sa postavljenim pitanjem.",
                        topic_id=topic.id,
                        user_id=student_user_1.id,
                        is_best_answer=False,
                        is_deleted=False,
                        created_at=time_offset + timedelta(minutes=30),
                    )
                    komentar_2 = ForumComment(
                        content="⚠️ EVE REŠENJA: Ovo je službeno proglašeno kao NAJBOLJI ODGOVOR. "
                                "Koristite Eulerovu formulu kako biste transformaciju sveli na jednostavne integrale.",
                        topic_id=topic.id,
                        user_id=student_user_2.id,
                        is_best_answer=True,
                        is_deleted=False,
                        created_at=time_offset + timedelta(hours=1),
                    )
                    session.add(komentar_1)
                    session.add(komentar_2)
                    session.commit()
                    session.refresh(komentar_1)
                    session.refresh(komentar_2)

                    session.add(ForumCommentVote(comment_id=komentar_1.id, user_id=main_user.id, value=1))
                    session.add(ForumCommentVote(comment_id=komentar_2.id, user_id=main_user.id, value=1))
                    session.add(ForumCommentVote(comment_id=komentar_2.id, user_id=student_user_1.id, value=1))

    session.commit()
    print("Forum podaci uspješno dodani!")


# ---------------------------------------------------------------------------
# Main app seed data
# ---------------------------------------------------------------------------

def _build_users() -> list[User]:
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
        {"email": "member10@test.local", "full_name": "Member Ten", "role": UserRole.member},
    ]
    return [
        User(
            email=d["email"],
            full_name=d["full_name"],
            password_hash=hash_password("password123"),
            role=d["role"],
        )
        for d in users_data
    ]


def _build_companies() -> list[Company]:
    companies_data = [
        {"company_name": "Tech Solutions d.o.o.", "description": "Leading IT solutions provider.", "website_url": "https://techsolutions.ba", "logo_path": "logos/tech1.png", "email": "hr@techsolutions.ba", "phone_number": "+38761111111", "tin": "1111111111111", "address": "Sarajevo, Zmaja od Bosne 1"},
        {"company_name": "Digital Innovations d.o.o.", "description": "Digital transformation experts.", "website_url": "https://digitalinnovations.ba", "logo_path": "logos/digital1.png", "email": "careers@digitalinnovations.ba", "phone_number": "+38761111112", "tin": "1111111111112", "address": "Sarajevo, Obala Kulina Bana 2"},
        {"company_name": "Cloud Systems d.o.o.", "description": "Cloud infrastructure and services.", "website_url": "https://cloudsystems.ba", "logo_path": "logos/cloud1.png", "email": "jobs@cloudsystems.ba", "phone_number": "+38761111113", "tin": "1111111111113", "address": "Zenica, Cara Dusana 3"},
        {"company_name": "Mobile First d.o.o.", "description": "Mobile app development company.", "website_url": "https://mobilefirst.ba", "logo_path": "logos/mobile1.png", "email": "recruitment@mobilefirst.ba", "phone_number": "+38761111114", "tin": "1111111111114", "address": "Tuzla, Kulina Bana 4"},
        {"company_name": "Data Analytics Pro d.o.o.", "description": "Business intelligence and analytics.", "website_url": "https://dataanalyticspro.ba", "logo_path": "logos/data1.png", "email": "hr@dataanalyticspro.ba", "phone_number": "+38761111115", "tin": "1111111111115", "address": "Mostar, Aleksa Santic 5"},
        {"company_name": "Security First d.o.o.", "description": "Cybersecurity and penetration testing.", "website_url": "https://securityfirst.ba", "logo_path": "logos/security1.png", "email": "careers@securityfirst.ba", "phone_number": "+38761111116", "tin": "1111111111116", "address": "Banja Luka, Drinska 6"},
        {"company_name": "DevOps Masters d.o.o.", "description": "Infrastructure automation and CI/CD.", "website_url": "https://devopsmasters.ba", "logo_path": "logos/devops1.png", "email": "jobs@devopsmasters.ba", "phone_number": "+38761111117", "tin": "1111111111117", "address": "Doboj, Baba Radisa 7"},
        {"company_name": "UI/UX Studio d.o.o.", "description": "User experience and interface design.", "website_url": "https://uiuxstudio.ba", "logo_path": "logos/uiux1.png", "email": "hello@uiuxstudio.ba", "phone_number": "+38761111118", "tin": "1111111111118", "address": "Bijeljina, Cara Aleksandra 8"},
        {"company_name": "Backend Specialists d.o.o.", "description": "Enterprise backend development.", "website_url": "https://backendspecialists.ba", "logo_path": "logos/backend1.png", "email": "recruitment@backendspecialists.ba", "phone_number": "+38761111119", "tin": "1111111111119", "address": "Trebinje, Nemanjina 9"},
        {"company_name": "QA Automation d.o.o.", "description": "Software testing and quality assurance.", "website_url": "https://qaautomation.ba", "logo_path": "logos/qa1.png", "email": "careers@qaautomation.ba", "phone_number": "+38761111120", "tin": "1111111111120", "address": "Bihac, Zivka Dakica 10"},
    ]
    return [
        Company(**d, hashed_password=hash_password("company123"), status=CompanyStatus.approved)
        for d in companies_data
    ]


def _build_ads(companies: list[Company], users: list[User]) -> list[Ad]:
    ad_templates = [
        {"title": "Junior Web Developer", "type": AdType.internship, "field": "Web Development", "location": "Sarajevo", "description": "Exciting opportunity to learn and grow as a web developer.", "deadline": 30, "duration_months": 3, "compensation": 300.0, "spots": 2},
        {"title": "Backend Developer Internship", "type": AdType.internship, "field": "Backend Development", "location": "Zenica", "description": "Build scalable backend systems with Python and Django.", "deadline": 35, "duration_months": 4, "compensation": 350.0, "spots": 1},
        {"title": "QA Engineer", "type": AdType.internship, "field": "Quality Assurance", "location": "Tuzla", "description": "Test and ensure software quality and reliability.", "deadline": 40, "duration_months": 3, "compensation": 280.0, "spots": 3},
        {"title": "Data Analytics Internship", "type": AdType.internship, "field": "Data Analytics", "location": "Mostar", "description": "Analyze business data and generate insights.", "deadline": 25, "duration_months": 2, "compensation": 400.0, "spots": 1},
        {"title": "Cybersecurity Specialist", "type": AdType.internship, "field": "Cybersecurity", "location": "Banja Luka", "description": "Learn cybersecurity best practices and protocols.", "deadline": 45, "duration_months": 6, "compensation": 450.0, "spots": 2},
        {"title": "DevOps Engineer Intern", "type": AdType.internship, "field": "DevOps", "location": "Doboj", "description": "Work on CI/CD pipelines and infrastructure automation.", "deadline": 32, "duration_months": 4, "compensation": 420.0, "spots": 1},
        {"title": "UI/UX Designer", "type": AdType.internship, "field": "Design", "location": "Bijeljina", "description": "Create beautiful and user-friendly interfaces.", "deadline": 28, "duration_months": 3, "compensation": 330.0, "spots": 2},
        {"title": "Mobile App Developer", "type": AdType.internship, "field": "Mobile Development", "location": "Trebinje", "description": "Develop iOS and Android applications.", "deadline": 38, "duration_months": 5, "compensation": 380.0, "spots": 1},
        {"title": "Full Stack Developer", "type": AdType.internship, "field": "Full Stack", "location": "Bihac", "description": "Work on both frontend and backend systems.", "deadline": 42, "duration_months": 4, "compensation": 370.0, "spots": 2},
        {"title": "Software Engineer Apprenticeship", "type": AdType.internship, "field": "Software Engineering", "location": "Sarajevo", "description": "Comprehensive software engineering training program.", "deadline": 50, "duration_months": 6, "compensation": 400.0, "spots": 3},
        {"title": "Python Bootcamp", "type": AdType.education, "field": "Programiranje", "location": "Sarajevo", "description": "Intenzivni kurs Python programiranja za studente.", "deadline": 30, "duration_months": 2, "compensation": None, "spots": 20},
        {"title": "Web Development Kurs", "type": AdType.education, "field": "Web Development", "location": "Tuzla", "description": "Naučite HTML, CSS i JavaScript od nule.", "deadline": 35, "duration_months": 3, "compensation": None, "spots": 15},
        {"title": "Data Science Radionica", "type": AdType.education, "field": "Data Science", "location": "Mostar", "description": "Uvod u analizu podataka i machine learning.", "deadline": 40, "duration_months": 1, "compensation": None, "spots": 10},
        {"title": "Stipendija za IT studente", "type": AdType.scholarship, "field": "Informacione tehnologije", "location": "Sarajevo", "description": "Stipendija namijenjena studentima IT fakulteta.", "deadline": 45, "duration_months": None, "compensation": 500.0, "spots": 5},
        {"title": "STEM Stipendija", "type": AdType.scholarship, "field": "STEM", "location": "Banja Luka", "description": "Stipendija za studente prirodnih i tehničkih nauka.", "deadline": 50,("title"): AdType.scholarship,("field"): "STEM",("location"): "Banja Luka",("description"): "Stipendija za studente prirodnih i tehničkih nauka.",("deadline"): 50,("duration_months"): None,("compensation"): 400.0,("spots"): 3},
    ]
    ads = []
    for index, template in enumerate(ad_templates):
        ads.append(
            Ad(
                company_id=companies[index % len(companies)].id,
                approved_by=users[0].id,
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
                user_id=users[(index + 1) % len(users)].id,
                text=messages[index],
                type=notification_types[index % len(notification_types)],
                is_read=index % 2 == 0,
            )
        )
    return notifications


def _build_bookmarks(users: list[User], ads: list[Ad]) -> list[AdBookmark]:
    bookmarks = []
    for index in range(10):
        bookmarks.append(
            AdBookmark(
                user_id=users[(index + 1) % len(users)].id,
                ad_id=ads[index].id,
            )
        )
    return bookmarks


def seed_demo_data(session: Session) -> dict[str, int]:
    existing_user = session.exec(select(User).where(User.email == "admin@test.local")).first()
    if existing_user:
        return {
            "users": len(session.exec(select(User)).all()),
            "companies": len(session.exec(select(Company)).all()),
            "ads": len(session.exec(select(Ad)).all()),
            "applications": len(session.exec(select(Application)).all()),
            "notifications": len(session.exec(select(Notification)).all()),
            "bookmarks": len(session.exec(select(AdBookmark)).all()),
            "created": 0,
        }

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
    create_db_and_tables()

    with Session(engine) as session:
        result = seed_demo_data(session)
        seed_forum_categories(session)
        seed_forum_topics_and_comments(session)

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
