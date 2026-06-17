from sqlmodel import SQLModel, create_engine
from app.database import engine
from app.models.user import User
from app.models.activity_log import ActivityLog
from app.models.forum import ForumCategory, ForumTopic, ForumTag, ForumTopicTag, TopicReport, AdminAnnouncement, ForumComment, ForumCommentVote, ForumGuideline, TopicLike
from app.models.forum_reputation import ForumUserStats

print("Kreiram sve tabele direktno iz modela...")
SQLModel.metadata.create_all(engine)
print("Sve tabele su uspješno kreirane!")