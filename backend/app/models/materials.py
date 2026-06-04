from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from app.models.user import User 


class Subject(SQLModel, table=True):
    __tablename__ = "subjects"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    study_year: int
    
    materials: list["Material"] = Relationship(back_populates="subject")

class Material(SQLModel, table=True):
    __tablename__ = "materials"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    file_path: str
    file_type: str
    status: str = Field(default="pending")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    number_of_downloads: int = Field(default=0)

    subject_id: int = Field(foreign_key="subjects.id")
    user_id: int = Field(foreign_key="users.id")

    subject: Optional[Subject] = Relationship(back_populates="materials")
    comments: list["Comment"] = Relationship(back_populates="material")
    ratings: list["Rating"] = Relationship(back_populates="material")
    user: Optional["User"] = Relationship()


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
    user: Optional["User"] = Relationship()

class MaterialCreate(SQLModel):
    title: str
    description: Optional[str] = None
    file_type: str
    subject_id: int  
class CommentCreate(SQLModel):
    content: str
    material_id: int

class RatingCreate(SQLModel):
    rating: int = Field(ge=1, le=5)
    material_id: int
    
    

class UserResponse(SQLModel):
    id: int
    full_name: str
    
class CommentResponse(SQLModel):
    id: int
    user_id: int
    material_id: int
    content: str
    created_at: datetime
    user: UserResponse
    
class MaterialsResponse(SQLModel):
    id: int
    title: str
    file_type: str
    status: str
    created_at: datetime
    number_of_downloads: int
    subject: Optional[Subject] = None
    user: UserResponse  
    average_rating: Optional[float] = None
    rating_count: Optional[int] = None
    
class MaterialDetailResponse(SQLModel):
    id: int
    title: str
    description: Optional[str] = None
    file_type: str
    status: str
    created_at: datetime
    number_of_downloads: int
    subject: Subject
    user: UserResponse
    comments: list[CommentResponse] = []
    ratings: list[Rating] = []
    
    average_rating: Optional[float] = None
    rating_count: Optional[int] = None
    
def get_default_subjects():
    return [
        Subject(name="Matematika 1", study_year=1),
        Subject(name="Fizika 1", study_year=1),
        Subject(name="Osnovi elektrotehnike 1", study_year=1),
        Subject(name="Osnovi računarstva", study_year=1),
        Subject(name="Uvod u energetske sisteme", study_year=1),
        Subject(name="Matematika 2", study_year=1),
        Subject(name="Fizika 2", study_year=1),
        Subject(name="Osnovi elektrotehnike 2", study_year=1),
        Subject(name="Osnovi programiranja", study_year=1),
        Subject(name="Tehnologije za podršku tehničkom pisanju", study_year=1),
        Subject(name="Matematika 3", study_year=2),
        Subject(name="Signali i sistemi", study_year=2),
        Subject(name="Osnovi elektronike", study_year=2),
        Subject(name="Objektno orijentirano programiranje", study_year=2),
        Subject(name="Analogna integrisana elektronika", study_year=2),
        Subject(name="Statistička teorija telekomunikacija", study_year=2),
        Subject(name="Sekvencijalni sklopovi", study_year=2),
        Subject(name="Modeliranje i analiza podataka", study_year=2),
        Subject(name="Osnovi telekomunikacija", study_year=3),
        Subject(name="Teorija informacija i kodovanja", study_year=3),
        Subject(name="Telekomunikacijski protokoli", study_year=3),
        Subject(name="Obrada digitalnih signala", study_year=3),
        Subject(name="Baze podataka", study_year=3),
        Subject(name="Optičke telekomunikacije", study_year=3),
        Subject(name="Razvoj telekomunikacijske programske podrške", study_year=3),
        Subject(name="Telekomunikacione mreže", study_year=3),
        Subject(name="Radijski telekomunikacijski sistemi", study_year=3),
        Subject(name="Mobilne telekomunikacije", study_year=4),
        Subject(name="Mikroprocesorski sistemi u telekomunikacijama", study_year=4),
        Subject(name="Mjerenja u telekomunikacijama", study_year=4),
        Subject(name="Razvoj mobilnih aplikacija i servisa", study_year=4),
        Subject(name="Infrastruktura i servisi u oblaku", study_year=4),
        Subject(name="Projektovanje telekomunikacionih mreža", study_year=4),
        Subject(name="Multimedijski sistemi i komunikacije", study_year=4),
    ]