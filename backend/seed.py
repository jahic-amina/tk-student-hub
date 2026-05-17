from sqlmodel import Session, create_engine, select
from app.database import engine
from app.models.materials import Subject, Material
from app.models.user import User 
from datetime import datetime

def seed_data():
    with Session(engine) as session:
        # 1. Provjera da li već postoje podaci da ne pravimo duplikate
        if session.exec(select(Subject)).first():
            print("Baza već ima podatke. Preskačem seeding.")
            return

        print("Punim bazu testnim podacima...")

        # 2. Kreiranje testnog korisnika (Prilagođeno polju password_hash)
        test_user = User(
            email="student@test.com", 
            full_name="Marko Marković", 
            password_hash="obican_tekst_ili_hash_za_test", # Promijenjeno sa hashed_password na password_hash
            role="admin"  
        )
        session.add(test_user)
        session.commit()
        session.refresh(test_user)

        # 3. Kreiranje Predmeta
        sub1 = Subject(name="Digitalne komunikacije", study_year=1)
        sub2 = Subject(name="Telekomunikacijske mreže", study_year=2)
        sub3 = Subject(name="Računarske mreže", study_year=3)
        sub4 = Subject(name="Signali i sistemi", study_year=4)
        
        session.add_all([sub1, sub2, sub3, sub4])
        session.commit()
        session.refresh(sub1)
        session.refresh(sub2)
        session.refresh(sub3)
        session.refresh(sub4)

        # 4. Kreiranje Materijala
        m1 = Material(
            title="Digitalne komunikacije",
            description="Kompletne skripte za prvi kolokvijum - osnove digitalne modulacije",
            file_path="uploads/test1.pdf",
            file_type="SKRIPTE",
            status="approved",
            subject_id=sub1.id,
            user_id=test_user.id
        )
        
        m2 = Material(
            title="Telekomunikacijske mreže",
            description="Bilješke sa predavanja - OSI model i TCP/IP protokoli",
            file_path="uploads/test2.pdf",
            file_type="BILJEŠKE",
            status="approved",
            subject_id=sub2.id,
            user_id=test_user.id
        )

        m3 = Material(
            title="Računarske mreže",
            description="Riješeni ispitni zadaci od 2020-2025",
            file_path="uploads/test3.pdf",
            file_type="ISPITI",
            status="approved",
            subject_id=sub3.id,
            user_id=test_user.id
        )

        m4 = Material(
            title="Signali i sistemi",
            description="Skripte sa primjerima - Fourierova transformacija i praktična primjena",
            file_path="uploads/test4.pdf",
            file_type="VJEŽBE",
            status="approved",
            subject_id=sub4.id,
            user_id=test_user.id
        )

        session.add_all([m1, m2, m3, m4])
        session.commit()
        print("Baza uspješno napunjena!")

if __name__ == "__main__":
    seed_data()