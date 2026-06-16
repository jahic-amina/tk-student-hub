from sqlmodel import SQLModel, create_engine
# Importuj engine iz tvoje aplikacije (prilagodi putanju ako je potrebno)
from app.database import engine 
# VEOMA VAŽNO: Moramo importovati modele da bi ih SQLModel uopšte vidio
from app.models.user import User
from app.models.forum import ForumCategory, ForumTopic, ForumTag, ForumTopicTag, TopicReport, AdminAnnouncement

print("Kreiram sve tabele direktno iz modela...")
SQLModel.metadata.create_all(engine)
print("Sve tabele su uspješno kreirane!")