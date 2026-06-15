from sqlmodel import SQLModel, create_engine, Session, select
from app.core.config import settings
from app.models.materials import  Subject, get_default_subjects 

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    create_default_subjects(); 
    
def create_default_subjects():
    with Session(engine) as session:
        existing_subjects = session.exec(select(Subject)).first()
        if existing_subjects:
            return
        default_subjects = get_default_subjects()
        session.add_all(default_subjects)
        session.commit()

def get_db():
    with Session(engine) as session:
        yield session
