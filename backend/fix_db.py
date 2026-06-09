from sqlalchemy import text
from app.database import engine, create_db_and_tables

# Učitaj sve modele/rutere da SQLModel zna za nove tabele
import app.models.forum
import app.routers.forum_likes

create_db_and_tables()

with engine.connect() as conn:
    columns = conn.execute(text("PRAGMA table_info(forum_comments)")).fetchall()
    column_names = [col[1] for col in columns]

    if "is_admin_notice" not in column_names:
        conn.execute(
            text("ALTER TABLE forum_comments ADD COLUMN is_admin_notice BOOLEAN DEFAULT 0")
        )
        conn.commit()
        print("Dodana kolona forum_comments.is_admin_notice")
    else:
        print("Kolona is_admin_notice već postoji")

print("Baza je popravljena.")