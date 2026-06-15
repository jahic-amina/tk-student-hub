from datetime import datetime, timedelta, timezone
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

from app.models.forum_reputation import (
    ForumUserStats,
    ForumUserMedal,
    ForumReputationEvent
)

FORUM_CATEGORIES = [
    {"name": "Opšta diskusija", "color": "#ff7a00", "description": "Opšte teme vezane za studij i studentski život."},
    {"name": "Pomoć sa predmetima", "color": "#2563eb", "description": "Pitanja, objašnjenja i pomoć oko predmeta."},
    {"name": "Studijske grupe", "color": "#16a34a", "description": "Organizacija grupa za učenje i pripremu ispita."},
    {"name": "Praksa i posao", "color": "#9333ea", "description": "Diskusije o praksama, poslovima i karijeri."},
    {"name": "Projekti", "color": "#dc2626", "description": "Ideje, pitanja i pomoć oko studentskih projekata."},
    {"name": "Off-Topic", "color": "#6b7280", "description": "Neformalne teme i razgovori van nastave."},
]


def seed_categories(session: Session):
    print("📂 Seeding kategorija...")
    for category_data in FORUM_CATEGORIES:
        existing_category = session.exec(
            select(ForumCategory).where(ForumCategory.name == category_data["name"])
        ).first()

        if existing_category:
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
    
    total_topics_created_by_main = 0
    total_answers_by_user1 = 0
    total_answers_by_user2 = 0
    
    for category in categories:
        if category.name == "Praksa i posao":
            continue
            
        for i in range(1, 21):
            title_text = f"Tema broj {i} u kategoriji {category.name}"
            
            existing_topic = session.exec(
                select(ForumTopic).where(ForumTopic.title == title_text)
            ).first()
            
            if not existing_topic:
                time_offset = datetime.now(timezone.utc) - timedelta(days=21-i, hours=i)
                
                topic = ForumTopic(
                    title=title_text,
                    content=f"Ovo je tekstualni sadržaj za testnu temu broj {i}.",
                    category_id=category.id,
                    user_id=main_user.id,
                    views_count=i * 12,
                    created_at=time_offset,
                    is_deleted=False
                )
                session.add(topic)
                session.commit()
                session.refresh(topic)
                total_topics_created_by_main += 1
                
                if i == 1:
                    if category.name == "Pomoć sa predmetima":
                        session.add(ForumTopicTag(topic_id=topic.id, tag_id=tags["fourier"].id))
                        session.add(ForumTopicTag(topic_id=topic.id, tag_id=tags["matematika"].id))
                    elif category.name == "Projekti":
                        session.add(ForumTopicTag(topic_id=topic.id, tag_id=tags["programiranje"].id))
                    else:
                        session.add(ForumTopicTag(topic_id=topic.id, tag_id=tags["ispit"].id))
                    
                    komentar_1 = ForumComment(
                        content=f"Ovo je prvi odgovor na temu '{topic.title}'.",
                        topic_id=topic.id,
                        user_id=student_user_1.id,
                        is_best_answer=False,
                        created_at=time_offset + timedelta(minutes=30)
                    )
                    komentar_2 = ForumComment(
                        content=f"⚠️ EVE REŠENJA: Ovo je službeno proglašeno kao NAJBOLJI ODGOVOR.",
                        topic_id=topic.id,
                        user_id=student_user_2.id,
                        is_best_answer=True, 
                        created_at=time_offset + timedelta(hours=1)
                    )
                    session.add(komentar_1)
                    session.add(komentar_2)
                    session.commit()
                    
                    total_answers_by_user1 += 1
                    total_answers_by_user2 += 1
                    
                    session.add(ForumCommentVote(comment_id=komentar_1.id, user_id=main_user.id, value=1))
                    session.add(ForumCommentVote(comment_id=komentar_2.id, user_id=main_user.id, value=1))
                    session.add(ForumCommentVote(comment_id=komentar_2.id, user_id=student_user_1.id, value=1))
                    
    session.commit()

    print("🏅 Seeding sistema reputacije, statistike i medalja...")
    
    main_stats = session.exec(select(ForumUserStats).where(ForumUserStats.user_id == main_user.id)).first()
    if not main_stats:
        main_stats = ForumUserStats(
            user_id=main_user.id,
            reputation_points=total_topics_created_by_main * 10,
            topics_started_count=total_topics_created_by_main,
            answers_count=0,
            best_answers_count=0,
            night_topics_count=5 
        )
        session.add(main_stats)

    amra_stats = session.exec(select(ForumUserStats).where(ForumUserStats.user_id == student_user_1.id)).first()
    if not amra_stats:
        amra_stats = ForumUserStats(
            user_id=student_user_1.id,
            reputation_points=total_answers_by_user1 * 3,
            topics_started_count=0,
            answers_count=total_answers_by_user1,
            best_answers_count=0
        )
        session.add(amra_stats)

    zijad_reputation = (total_answers_by_user2 * 3) + (5 * 25)
    zijad_stats = session.exec(select(ForumUserStats).where(ForumUserStats.user_id == student_user_2.id)).first()
    if not zijad_stats:
        zijad_stats = ForumUserStats(
            user_id=student_user_2.id,
            reputation_points=zijad_reputation,
            topics_started_count=0,
            answers_count=total_answers_by_user2,
            best_answers_count=5
        )
        session.add(zijad_stats)
    
    session.commit()

    if not session.exec(select(ForumUserMedal).where(ForumUserMedal.user_id == main_user.id, ForumUserMedal.medal_code == "topics_gold")).first():
        session.add(ForumUserMedal(user_id=main_user.id, medal_code="topics_gold", category="topics_started", tier="gold"))
    
    if not session.exec(select(ForumUserMedal).where(ForumUserMedal.user_id == student_user_2.id, ForumUserMedal.medal_code == "best_answers_bronze")).first():
        session.add(ForumUserMedal(user_id=student_user_2.id, medal_code="best_answers_bronze", category="best_answers", tier="bronze"))
        
    if not session.exec(select(ForumUserMedal).where(ForumUserMedal.user_id == student_user_1.id, ForumUserMedal.medal_code == "night_owl")).first():
        session.add(ForumUserMedal(user_id=student_user_1.id, medal_code="night_owl", category="secret", tier="bronze", is_secret=True))

    session.commit()
    print("Baza je uspješno napumpana i reputacija je izračunata!")


def seed_database():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        seed_categories(session)
        seed_topics_and_comments(session)
    print("Svi seed podaci za forum i reputaciju su spremni.")


if __name__ == "__main__":
    seed_database()
