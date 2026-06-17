import os  
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.database import create_db_and_tables
from app.core.security import get_current_user
from app.models.user import User
from app.models.forum_notification import ForumNotification                


from app.models.forum_reputation import (
    ForumReputationEvent,
    ForumUserMedal,
    ForumUserStats,
)

from app.routers import (
    auth, dashboard, activity, admin, profiles, account, company, applications, materials,
    forum_categories, forum_topics, forum_comments, forum_tags, forum_admin, forum_likes,
    forum_guidelines, forum_attachments
)
from app.routers import forum_notifications

from app.routers.ad_bookmark import router as ad_bookmark_router
from app.routers.notification import router as notification_router  
from app.routers.ad import router as ads_router
from app.routers.prakse import router as prakse_router
from app.routers.workshops import router as workshops_router


# Inicijalizacija baze podataka
create_db_and_tables()

# Kreiranje foldera za upload ako ne postoji
LOCAL_UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(LOCAL_UPLOAD_DIR, exist_ok=True)

security = HTTPBearer()

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend platforme za TK Student Hub - studentski centar za telekomunikacije",
    version="1.0.0"
)

# CORS konfiguracija (Zadržan allow_credentials=False jer "*" origin ne dopušta True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montiranje statičkih fajlova za upload
app.mount("/uploads", StaticFiles(directory=LOCAL_UPLOAD_DIR), name="uploads")

# --- REGISTRACIJA SVIH RUTERA ---

# Autentifikacija i korisnički nalozi
app.include_router(auth.router)
app.include_router(account.router)
app.include_router(profiles.router)
app.include_router(company.router)

# Prakse, oglasi i prijave
app.include_router(ads_router)
app.include_router(applications.router)
app.include_router(ad_bookmark_router) 

# Forum i zajednica
app.include_router(forum_categories.router)
app.include_router(forum_topics.router)
app.include_router(forum_comments.router)
app.include_router(forum_tags.router)
app.include_router(forum_likes.router)
app.include_router(forum_guidelines.router)
app.include_router(forum_attachments.router)
app.include_router(forum_notifications.router)

# Sistem, administracija i ostalo
app.include_router(dashboard.router)
app.include_router(activity.router)
app.include_router(admin.router)
app.include_router(forum_admin.router)
app.include_router(materials.router)
app.include_router(notification_router)
app.include_router(prakse_router)
app.include_router(workshops_router)

# --- OSNOVNI ENDPOINTI ---

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