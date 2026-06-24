from sqlmodel import Session
from app.database import engine
from app.models.user import User, UserRole
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin():
    with Session(engine) as session:
        admin = User(
            email="admin@admin.com",
            full_name="Admin",
            password_hash=pwd_context.hash("admin123"),
            role=UserRole.admin
        )
        session.add(admin)
        session.commit()
        print("Admin kreiran!")

if __name__ == "__main__":
    create_admin()