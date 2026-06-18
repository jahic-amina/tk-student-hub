from typing import Optional, List
from datetime import datetime, timezone

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint


class ForumCategory(SQLModel, table=True):
    __tablename__ = "forum_categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    color: str = Field(default="#ff7a00", max_length=20)
    description: Optional[str] = Field(default=None, max_length=255)

    topics: List["ForumTopic"] = Relationship(back_populates="category")


class ForumTopic(SQLModel, table=True):
    __tablename__ = "forum_topics"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, max_length=200)
    content: str

    views_count: int = Field(default=0)
    is_locked: bool = Field(default=False)
    is_deleted: bool = Field(default=False)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    category_id: int = Field(foreign_key="forum_categories.id")
    user_id: int = Field(foreign_key="users.id")

    category: Optional[ForumCategory] = Relationship(back_populates="topics")
    comments: List["ForumComment"] = Relationship(back_populates="topic")


class ForumComment(SQLModel, table=True):
    __tablename__ = "forum_comments"

    id: Optional[int] = Field(default=None, primary_key=True)
    content: str

    is_admin_notice: bool = Field(default=False)

    is_best_answer: bool = Field(default=False)
    is_deleted: bool = Field(default=False)
    parent_id: Optional[int] = Field(default=None, foreign_key="forum_comments.id")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    topic_id: int = Field(foreign_key="forum_topics.id")
    user_id: int = Field(foreign_key="users.id")

    topic: Optional[ForumTopic] = Relationship(back_populates="comments")
    votes: List["ForumCommentVote"] = Relationship(back_populates="comment")
    replies: List["ForumComment"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "ForumComment.parent_id == foreign(ForumComment.id)",
            "lazy": "select"
        }
    )


class ForumCommentVote(SQLModel, table=True):
    __tablename__ = "forum_comment_votes"

    __table_args__ = (
        UniqueConstraint("comment_id", "user_id", name="unique_comment_vote_per_user"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    comment_id: int = Field(foreign_key="forum_comments.id")
    user_id: int = Field(foreign_key="users.id")

    value: int = Field(default=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    comment: Optional[ForumComment] = Relationship(back_populates="votes")


class ForumTag(SQLModel, table=True):
    __tablename__ = "forum_tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, max_length=50)


class ForumTopicTag(SQLModel, table=True):
    __tablename__ = "forum_topic_tags"

    topic_id: Optional[int] = Field(
        default=None,
        foreign_key="forum_topics.id",
        primary_key=True
    )

    tag_id: Optional[int] = Field(
        default=None,
        foreign_key="forum_tags.id",
        primary_key=True
    )


class TopicReport(SQLModel, table=True):
    __tablename__ = "topic_reports"

    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int = Field(foreign_key="forum_topics.id")
    user_id: int = Field(foreign_key="users.id")
    reason: str = Field(max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="pending") 
    action_taken: Optional[str] = None 
    admin_explanation: Optional[str] = None 
    

class AdminAnnouncement(SQLModel, table=True):
    __tablename__ = "admin_announcements"

    id: Optional[int] = Field(default=None, primary_key=True)
    admin_id: int = Field(foreign_key="users.id")
    title: str = Field(max_length=150)
    content: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = Field(default=None, nullable=True)


class ForumGuideline(SQLModel, table=True):
    __tablename__ = "forum_guidelines"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    order: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# --- NOVI MODEL OD KOLEGA ZA LAJKOVANJE TEME ---
class TopicLike(SQLModel, table=True):
    __tablename__ = "topic_likes"

    __table_args__ = (
        UniqueConstraint("topic_id", "user_id", name="unique_topic_like_per_user"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int = Field(foreign_key="forum_topics.id", index=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TopicDislike(SQLModel, table=True):
    __tablename__ = "topic_dislikes"

    __table_args__ = (
        UniqueConstraint("topic_id", "user_id", name="unique_topic_dislike_per_user"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int = Field(foreign_key="forum_topics.id", index=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TopicAttachment(SQLModel, table=True):
    __tablename__ = "topic_attachments"

    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int = Field(foreign_key="forum_topics.id", index=True)
    filename: str = Field(max_length=255)
    file_path: str = Field(max_length=500)
    file_size: int  # u bajtovima
    mime_type: str = Field(max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CommentAttachment(SQLModel, table=True):
    __tablename__ = "comment_attachments"

    id: Optional[int] = Field(default=None, primary_key=True)
    comment_id: int = Field(foreign_key="forum_comments.id", index=True)
    filename: str = Field(max_length=255)
    file_path: str = Field(max_length=500)
    file_size: int
    mime_type: str = Field(max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)