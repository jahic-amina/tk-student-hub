from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SAEnum, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from app.enums.activity import ActivityType

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_type = Column(SAEnum(ActivityType), nullable=False)
    title = Column(String, nullable=False)
    subtitle = Column(String, nullable=True)
    entity_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="activity_logs")

    __table_args__ = (
        Index("ix_activity_logs_user_created", "user_id", "created_at"),
    )