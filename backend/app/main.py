from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from app.core.config import settings
from app.database import create_db_and_tables
from app.routers import auth, mentoring, forum, prakse, profiles   
from app.core.security import get_current_user
from app.models.user import User

create_db_and_tables()

security = HTTPBearer()

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend platforme za TK Student Hub - studentski centar za telekomunikacije",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(prakse.router)
app.include_router(mentoring.router)
app.include_router(forum.router)
app.include_router(profiles.router)

@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} API radi"}

@app.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role
    }