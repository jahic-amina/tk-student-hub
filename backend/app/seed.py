from sqlmodel import SQLModel, Session, select

from app.database import engine
from app.models.user import User
from app.models.forum import ForumCategory, ForumTopic, ForumComment


FORUM_CATEGORIES = [
    {
        "name": "Opšta diskusija",
        "color": "#ff7a00",
        "description": "Opšte teme vezane za studij i studentski život."
    },
    {
        "name": "Pomoć sa predmetima",
        "color": "#2563eb",
        "description": "Pitanja, objašnjenja i pomoć oko predmeta."
    },
    {
        "name": "Studijske grupe",
        "color": "#16a34a",
        "description": "Organizacija grupa za učenje i pripremu ispita."
    },
    {
        "name": "Praksa i posao",
        "color": "#9333ea",
        "description": "Diskusije o praksama, poslovima i karijeri."
    },
    {
        "name": "Projekti",
        "color": "#dc2626",
        "description": "Ideje, pitanja i pomoć oko studentskih projekata."
    },
    {
        "name": "Off-Topic",
        "color": "#6b7280",
        "description": "Neformalne teme i razgovori van nastave."
    },
]


def seed_categories(session: Session):
    for category_data in FORUM_CATEGORIES:
        existing_category = session.exec(
            select(ForumCategory).where(ForumCategory.name == category_data["name"])
        ).first()

        if existing_category:
            continue

        category = ForumCategory(
            name=category_data["name"],
            color=category_data["color"],
            description=category_data["description"]
        )

        session.add(category)

    session.commit()


def get_or_create_test_user(session: Session) -> User:
    existing_user = session.exec(
        select(User).where(User.email == "forum.test@student.ba")
    ).first()

    if existing_user:
        return existing_user

    user = User(
        email="forum.test@student.ba",
        full_name="Forum Test Student",
        password_hash="seed-test-password"
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def seed_topics_and_comments(session: Session):
    user = get_or_create_test_user(session)
    
    # 1. Povlačimo sve kategorije koje imamo u bazi
    categories = session.exec(select(ForumCategory)).all()
    
    if not categories:
        print("Kategorije nisu pronađene. Prvo pokrenite seed_categories.")
        return

    print("Započeto masovno punjenje baze (seed)...")
    
    # 2. Prolazimo kroz SVAKU kategoriju
    for category in categories:
        
        # Ako je u pitanju "Praksa i posao", nju preskačemo da nam ostane prazna za testiranje UI-ja!
        if category.name == "Praksa i posao":
            continue
            
        # 3. Za svaku od ostalih kategorija generišemo po 10 tema
        for i in range(1, 11):
            title_text = f"Tema broj {i} u kategoriji {category.name}"
            
            # Provjeravamo da li ova tema već postoji u bazi da ne dupliramo podatke
            existing_topic = session.exec(
                select(ForumTopic).where(ForumTopic.title == title_text)
            ).first()
            
            if not existing_topic:
                topic = ForumTopic(
                    title=title_text,
                    content=f"Ovo je tekstualni sadržaj za testnu temu broj {i}. Ovdje simuliramo dugački studentski tekst kako bismo provjerili da li paginacija i filtriranje rade glatko.",
                    category_id=category.id,
                    user_id=user.id,
                    views_count=i * 12 # čisto da imamo različit broj pregleda
                )
                session.add(topic)
                
    session.commit()
    print("Baza uspješno napumpana! (Po 10 tema po kategoriji, osim za Praksu i posao)")

def seed_database():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        seed_categories(session)
        seed_topics_and_comments(session)

    print("Seed podaci za forum su uspješno dodani.")


if __name__ == "__main__":
    seed_database()