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

    general_category = session.exec(
        select(ForumCategory).where(ForumCategory.name == "Opšta diskusija")
    ).first()

    projects_category = session.exec(
        select(ForumCategory).where(ForumCategory.name == "Projekti")
    ).first()

    if not general_category or not projects_category:
        print("Kategorije nisu pronađene. Prvo se moraju dodati kategorije.")
        return

    first_topic = session.exec(
        select(ForumTopic).where(ForumTopic.title == "Dobrodošli na TK Student Hub forum")
    ).first()

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

        first_comment = ForumComment(
            content="Super, forum će biti koristan za pitanja oko predmeta i projekata.",
            topic_id=first_topic.id,
            user_id=user.id
        )

        session.add(first_comment)
        session.commit()

    second_topic = session.exec(
        select(ForumTopic).where(ForumTopic.title == "Ideje za projekte iz telekomunikacija")
    ).first()

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

        second_comment = ForumComment(
            content="Dobra tema, mogli bismo dodati primjere projekata sa Arduinom, STM32 i mrežnim alatima.",
            topic_id=second_topic.id,
            user_id=user.id
        )

        session.add(second_comment)
        session.commit()


def seed_database():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        seed_categories(session)
        seed_topics_and_comments(session)

    print("Seed podaci za forum su uspješno dodani.")


if __name__ == "__main__":
    seed_database()