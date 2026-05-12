from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class Subject(SQLModel, table=True):
    __tablename__ = "subjects"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    study_year: int

class Material(SQLModel, table=True):
    __tablename__ = "materials"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    file_path: str
    file_type: str
    status: str = Field(default="active")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    number_of_downloads: int = Field(default=0)

    subject_id: int = Field(foreign_key="subjects.id")
    user_id: int = Field(foreign_key="users.id")

    subject: Optional[Subject] = Relationship(back_populates="materials")


class Rating(SQLModel, table=True):
    __tablename__ = "ratings"
    id: Optional[int] = Field(default=None, primary_key=True)
    rating: int = Field(ge=1, le=5)

    material_id: int = Field(foreign_key="materials.id")
    user_id: int = Field(foreign_key="users.id")

    material: Optional[Material] = Relationship(back_populates="ratings")


class Comment(SQLModel, table=True):
    __tablename__ = "comments"
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    material_id: int = Field(foreign_key="materials.id")
    user_id: int = Field(foreign_key="users.id")

    material: Optional[Material] = Relationship(back_populates="comments")
