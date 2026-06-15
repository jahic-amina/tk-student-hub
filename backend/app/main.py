from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles  
import os                                    
from app.core.config import settings
from app.database import create_db_and_tables
from app.routers import auth, dashboard, activity, admin, forum_categories, forum_topics, forum_comments, prakse, profiles, forum_tags, forum_admin, forum_likes 
from app.core.security import get_current_user
from app.models.user import User
from app.routers import account

create_db_and_tables()

os.makedirs("uploads", exist_ok=True)

security = HTTPBearer()

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend platforme za TK Student Hub - studentski centar za telekomunikacije",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth.router)
app.include_router(prakse.router)
app.include_router(forum_categories.router)
app.include_router(forum_topics.router)
app.include_router(forum_comments.router)
app.include_router(profiles.router)
app.include_router(dashboard.router)
app.include_router(activity.router)
app.include_router(admin.router)
app.include_router(account.router)
app.include_router(materials.router)
app.include_router(forum_tags.router)
app.include_router(forum_admin.router)
app.include_router(forum_likes.router)

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