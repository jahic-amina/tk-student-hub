from datetime import datetime, timedelta
from sqlmodel import SQLModel, Session, select

from app.database import engine
from app.models.user import User
from app.models.forum import (
    ForumCategory, 
    ForumTopic, 
    ForumComment, 
    ForumTag, 
    ForumTopicTag, 
    ForumCommentVote
)

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
    print("📂 Seeding kategorija...")
    for category_data in FORUM_CATEGORIES:
        existing_category = session.exec(
            select(ForumCategory).where(ForumCategory.name == category_data["name"])
        ).first()

        if existing_category:
            # Ažuriramo boju i opis ako su se promijenili u kodu
            existing_category.color = category_data["color"]
            existing_category.description = category_data["description"]
            session.add(existing_category)
            continue

        category = ForumCategory(
            name=category_data["name"],
            color=category_data["color"],
            description=category_data["description"]
        )
        session.add(category)

    session.commit()


def get_or_create_test_users(session: Session) -> list[User]:
    # Kreiramo tri različita korisnika kako bi komentari i teme izgledali prirodno
    emails = ["forum.test@student.ba", "amra.begic@student.ba", "zijad.lekic@student.ba"]
    names = ["Forum Test Student", "Amra Begić", "Zijad Lekić"]
    users = []

    for email, name in zip(emails, names):
        existing_user = session.exec(select(User).where(User.email == email)).first()
        if existing_user:
            users.append(existing_user)
        else:
            user = User(
                email=email,
                full_name=name,
                password_hash="seed-test-password"
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            users.append(user)
            
    return users


def get_or_create_tags(session: Session) -> dict[str, ForumTag]:
    # Definišemo set osnovnih tagova za forum
    tag_names = ["matematika", "programiranje", "fourier", "ispit", " hardware", "kafa"]
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


def seed_topics_and_comments(session: Session):
    users = get_or_create_test_users(session)
    main_user = users[0]
    student_user_1 = users[1]
    student_user_2 = users[2]
    
    tags = get_or_create_tags(session)
    categories = session.exec(select(ForumCategory)).all()
    
    if not categories:
        print("Kategorije nisu pronađene. Prvo pokrenite seed_categories.")
        return

    print("Započeto masovno punjenje baze (seed) sa podrškom za komentare i tagove...")
    
    for category in categories:
        # "Praksa i posao" ostaje prazna za testiranje UI stanja kada nema tema
        if category.name == "Praksa i posao":
            continue
            
        # Generišemo po 10 tema za svaku ostalu kategoriju zbog paginacije
        for i in range(1, 11):
            title_text = f"Tema broj {i} u kategoriji {category.name}"
            
            existing_topic = session.exec(
                select(ForumTopic).where(ForumTopic.title == title_text)
            ).first()
            
            if not existing_topic:
                # Simuliramo objave u različito vrijeme kako bi sortiranje po datumu imalo smisla
                time_offset = datetime.utcnow() - timedelta(days=11-i, hours=i*2)
                
                topic = ForumTopic(
                    title=title_text,
                    content=f"Ovo je tekstualni sadržaj za testnu temu broj {i}. Ovdje simuliramo dugački studentski tekst kako bismo provjerili da li paginacija, filtriranje i detaljan prikaz rade glatko.",
                    category_id=category.id,
                    user_id=main_user.id,
                    views_count=i * 12,
                    created_at=time_offset,
                    is_deleted=False
                )
                session.add(topic)
                session.commit()
                session.refresh(topic)
                
                # --- DODATAK ZA DETALJNI PRIKAZ (Samo za prvu temu u kategoriji dodajemo tagove i komentare) ---
                if i == 1:
                    # 1. Dodavanje tagova na temu
                    if category.name == "Pomoć sa predmetima":
                        session.add(ForumTopicTag(topic_id=topic.id, tag_id=tags["fourier"].id))
                        session.add(ForumTopicTag(topic_id=topic.id, tag_id=tags["matematika"].id))
                    elif category.name == "Projekti":
                        session.add(ForumTopicTag(topic_id=topic.id, tag_id=tags["programiranje"].id))
                    else:
                        session.add(ForumTopicTag(topic_id=topic.id, tag_id=tags["ispit"].id))
                    
                    # 2. Dodavanje komentara (odgovora) na tu temu
                    komentar_1 = ForumComment(
                        content=f"Ovo je prvi odgovor na temu '{topic.title}'. Slažem se sa postavljenim pitanjem i smatram da je ključno provjeriti literaturu.",
                        topic_id=topic.id,
                        user_id=student_user_1.id,
                        is_best_answer=False,
                        is_deleted=False,
                        created_at=time_offset + timedelta(minutes=30)
                    )
                    komentar_2 = ForumComment(
                        content=f"⚠️ EVE REŠENJA: Ovo je službeno proglašeno kao NAJBOLJI ODGOVOR za ovu temu. Koristite Eulerovu formulu kako biste transformaciju sveli na jednostavne integrale.",
                        topic_id=topic.id,
                        user_id=student_user_2.id,
                        is_best_answer=True, # Odlično za testiranje zelenog okvira na frontu!
                        is_deleted=False,
                        created_at=time_offset + timedelta(hours=1)
                    )
                    session.add(komentar_1)
                    session.add(komentar_2)
                    session.commit()
                    session.refresh(komentar_1)
                    session.refresh(komentar_2)
                    
                    # 3. Dodavanje glasova (Votes) na komentare radi testiranja rejtinga
                    session.add(ForumCommentVote(comment_id=komentar_1.id, user_id=main_user.id, value=1))
                    session.add(ForumCommentVote(comment_id=komentar_2.id, user_id=main_user.id, value=1))
                    session.add(ForumCommentVote(comment_id=komentar_2.id, user_id=student_user_1.id, value=1)) # Najbolji odgovor ima 2 glasa
                    
    session.commit()
    print("Baza uspješno napumpana! (Dodane teme, tagovi, komentari i glasovi)")


def seed_database():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        seed_categories(session)
        seed_topics_and_comments(session)

    print("Svi seed podaci za forum su uspješno dodani i sinhronizovani.")


if __name__ == "__main__":
    seed_database()