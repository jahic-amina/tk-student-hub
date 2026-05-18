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

    # 1. DOVLAČIMO SVE POTREBNE KATEGORIJE IZ BAZE
    general_category = session.exec(select(ForumCategory).where(ForumCategory.name == "Opšta diskusija")).first()
    projects_category = session.exec(select(ForumCategory).where(ForumCategory.name == "Projekti")).first()
    subjects_category = session.exec(select(ForumCategory).where(ForumCategory.name == "Pomoć sa predmetima")).first()
    groups_category = session.exec(select(ForumCategory).where(ForumCategory.name == "Studijske grupe")).first()
    offtopic_category = session.exec(select(ForumCategory).where(ForumCategory.name == "Off-Topic")).first()
    # "Praksa i posao" namjerno NE dovlačimo i NE dodajemo joj teme da ostane prazna!

    if not general_category or not projects_category:
        print("Kategorije nisu pronađene. Prvo se moraju dodati kategorije.")
        return

    # --- TEMA 1: Opšta diskusija (Tvoj postojeći kod) ---
    first_topic = session.exec(select(ForumTopic).where(ForumTopic.title == "Dobrodošli na TK Student Hub forum")).first()
    if not first_topic:
        first_topic = ForumTopic(
            title="Dobrodošli na TK Student Hub forum",
            content="Ovo je prva testna tema na forumu. Ovdje studenti mogu postavljati pitanja, dijeliti iskustva i pomagati jedni drugima.",
            category_id=general_category.id,
            user_id=user.id
        )
        session.add(first_topic)
        session.commit()
        session.refresh(first_topic)

        first_comment = ForumComment(content="Super, forum će biti koristan za pitanja oko predmeta i projekata.", topic_id=first_topic.id, user_id=user.id)
        session.add(first_comment)
        session.commit()

    # --- TEMA 2: Projekti (Tvoj postojeći kod) ---
    second_topic = session.exec(select(ForumTopic).where(ForumTopic.title == "Ideje za projekte iz telekomunikacija")).first()
    if not second_topic:
        second_topic = ForumTopic(
            title="Ideje za projekte iz telekomunikacija",
            content="Ovdje možemo dijeliti ideje za projekte iz mreža, elektronike, programiranja i telekomunikacijskih sistema.",
            category_id=projects_category.id,
            user_id=user.id
        )
        session.add(second_topic)
        session.commit()
        session.refresh(second_topic)

        second_comment = ForumComment(content="Dobra tema, mogli bismo dodati primjere projekata sa Arduinom, STM32 i mrežnim alatima.", topic_id=second_topic.id, user_id=user.id)
        session.add(second_comment)
        session.commit()

    # --- NOVO! TEMA 3: Pomoć sa predmetima ---
    if subjects_category:
        third_topic = session.exec(select(ForumTopic).where(ForumTopic.title == "Pomoć oko Fourierove transformacije - Signali i sistemi")).first()
        if not third_topic:
            third_topic = ForumTopic(
                title="Pomoć oko Fourierove transformacije - Signali i sistemi",
                content="Može li neko pojasniti prelazak sa kontinualnog na diskretni domen kod Fourierove transformacije? Primjeri sa rokova bi dobro došli.",
                category_id=subjects_category.id,
                user_id=user.id
            )
            session.add(third_topic)
            session.commit()

    # --- NOVO! TEMA 4: Studijske grupe ---
    if groups_category:
        fourth_topic = session.exec(select(ForumTopic).where(ForumTopic.title == "Formiranje grupe za učenje - Mreže računara")).first()
        if not fourth_topic:
            fourth_topic = ForumTopic(
                title="Formiranje grupe za učenje - Mreže računara",
                content="Planiramo se okupljati u čitaonici utorkom i četvrtkom da prelazimo laboratorijske vježbe iz Cisco Packet Tracera. Ko želi neka se javi.",
                category_id=groups_category.id,
                user_id=user.id
            )
            session.add(fourth_topic)
            session.commit()

    # --- NOVO! TEMA 5: Off-Topic ---
    if offtopic_category:
        fifth_topic = session.exec(select(ForumTopic).where(ForumTopic.title == "Koji ruter kupiti za studentski stan?")).first()
        if not fifth_topic:
            fifth_topic = ForumTopic(
                title="Koji ruter kupiti za studentski stan?",
                content="Ovaj fabrički ruter od operatera stalno puca čim se nas četvero nakači na Zoom predavanja. Treba mi neka stabilna preporuka.",
                category_id=offtopic_category.id,
                user_id=user.id
            )
            session.add(fifth_topic)
            session.commit()
            
def seed_database():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        seed_categories(session)
        seed_topics_and_comments(session)

    print("Seed podaci za forum su uspješno dodani.")


if __name__ == "__main__":
    seed_database()