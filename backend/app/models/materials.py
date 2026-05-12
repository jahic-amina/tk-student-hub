from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class Subject(SQLModel, table=True):
    __tablename__ = "subjects"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    study_year: int

