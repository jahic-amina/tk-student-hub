from sqlmodel import SQLModel, Field
from pydantic import field_validator
from typing import Optional
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from app.database import Base

class NotificationTypes(str, enum.Enum):
    NOVA_PRAKSA = "nova_praksa"
    STATUS_PRIJAVE = "status_prijave"
    LAJK_KOMENTAR = "lajk_komentar"
    OCJENA_MATERIJALA = "ocjena_materijala"
    MATERIJAL_NA_CEKANJU = "materijal_na_cekanju"

class Notification(Base):
    __tablename__ = "notifications"
 
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(SQLEnum(NotificationTypes), nullable=False)
    message = Column(String(255), nullable=False)
    link = Column(String(255), nullable=True)
    reference_id = Column(Integer, nullable=True)
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    user = relationship("User", back_populates="notifications")
    __table_args__ = (
        Index("ix_notifications_user_unread", "user_id", "is_read"),
    )

    def __repr__(self) -> str:
        return f"<Notification id={self.id} type={self.type} user_id={self.user_id} read={self.is_read}>"

