from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func, or_
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta, timezone
import re

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.forum import ForumCategory, ForumTopic, ForumTag, ForumTopicTag, TopicReport, AdminAnnouncement
from app.routers.forum_categories import get_category_data 
from app.routers.forum_likes import get_topic_likes_count
from app.services.forum_reputation import (
    get_user_forum_identity,
    register_topic_created,
)
# Uvoz funkcija za komentare
from app.routers.forum_comments import get_comments_count, has_best_answer, get_topic_comments, get_topic_votes_count

router = APIRouter(prefix="/forum/topics", tags=["Forum Topics"])

# --- SCHEMAS ---
class ForumTopicCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    content: str = Field(min_length=10)
    category_id: int
    tags: Optional[List[Any]] = None

class ReportCreate(BaseModel):
    reason: str = Field(min_length=3, max_length=100)

class ForumTopicUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    content: Optional[str] = Field(None, min_length=3)

# --- HELPER FUNCTIONS ---
def make_summary(text: str, max_length: int = 150) -> str:
    clean_text = " ".join((text or "").split())
    if len(clean_text) <= max_length:
        return clean_text
    return clean_text[:max_length].rsplit(" ", 1)[0] + "..."

def get_author_data(db: Session, user_id: int) -> dict:
    user = db.get(User, user_id)

    if not user:
        return {
            "id": None,
            "full_name": "Nepoznat korisnik",
            "role": "Student",
            "level": 1,
            "title": "Novi član",
            "reputation_points": 0,
            "medals": [],
        }

    forum_identity = get_user_forum_identity(db, user)

    return {
        "id": user.id,
        "full_name": user.full_name,
        **forum_identity,
    }

def get_topic_tags(db: Session, topic_id: int) -> list[str]:
    # Optimizovano spajanje da izbjegnemo N+1 petlje u bazi
    statement = select(ForumTag.name).join(ForumTopicTag, ForumTopicTag.tag_id == ForumTag.id).where(ForumTopicTag.topic_id == topic_id)
    return list(db.exec(statement).all())

def build_topic_list_item(db: Session, topic: ForumTopic) -> dict:
    comments_count = get_comments_count(db, topic.id)
    return {
        "id": topic.id,
        "title": topic.title,
        "summary": make_summary(topic.content),
        "content": topic.content,
        "views_count": topic.views_count,
        "likes_count": get_topic_likes_count(db, topic.id),
        "comments_count": comments_count,
        "answers_count": comments_count,
        "created_at": topic.created_at,
        "updated_at": topic.updated_at,
        "author": get_author_data(db, topic.user_id),
        "category": get_category_data(db, topic.category_id),
        "tags": get_topic_tags(db, topic.id),
        "has_best_answer": has_best_answer(db, topic.id),
    }

# --- ROUTES ---

@router.get("/", response_model=Dict[str, Any])
def get_all_topics(
    db: Session = Depends(get_db),
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    page: int = 1,
    per_page: int = 5,
    sort_by: Optional[str] = "najnovije", 
    unanswered: Optional[bool] = False,   
    days_old: Optional[int] = None        
):
    statement = select(ForumTopic).where(ForumTopic.is_deleted == False)
    count_statement = select(func.count(ForumTopic.id)).where(ForumTopic.is_deleted == False)

    if category_id is not None:
        statement = statement.where(ForumTopic.category_id == category_id)
        count_statement = count_statement.where(ForumTopic.category_id == category_id)
        
    if search and search.strip():
        search_value = f"%{search.strip()}%"
        condition = (ForumTopic.title.ilike(search_value)) | (ForumTopic.content.ilike(search_value))
        statement = statement.where(condition)
        count_statement = count_statement.where(condition)

    if days_old is not None and days_old > 0:
        vremenska_granica = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=days_old)
        statement = statement.where(ForumTopic.created_at >= vremenska_granica)
        count_statement = count_statement.where(ForumTopic.created_at >= vremenska_granica)

    if unanswered:
        from app.models.forum import ForumComment
        subquery = select(ForumComment.topic_id).where(ForumComment.is_deleted == False).subquery()
        statement = statement.where(ForumTopic.id.not_in(subquery))
        count_statement = count_statement.where(ForumTopic.id.not_in(subquery))

    if sort_by == "najgledanije":
        statement = statement.order_by(ForumTopic.views_count.desc(), ForumTopic.id.desc())
    elif sort_by == "najaktivnije":
        from app.models.forum import ForumComment
        statement = (
            statement.join(ForumComment, ForumComment.topic_id == ForumTopic.id, isouter=True)
            .group_by(ForumTopic.id)
            .order_by(func.count(ForumComment.id).desc(), ForumTopic.created_at.desc())
        )
    else:  
        statement = statement.order_by(ForumTopic.created_at.desc())

    total_topics = db.exec(count_statement).one()
    skip = (page - 1) * per_page
    statement = statement.offset(skip).limit(per_page)
    topics = db.exec(statement).all()
    
    topics_list = [build_topic_list_item(db, topic) for topic in topics]
    return {"items": topics_list, "total": total_topics, "page": page, "per_page": per_page}


@router.get("/suggestions")
def get_suggestions(search: Optional[str] = None, db: Session = Depends(get_db)):
    if not search or not search.strip():
        popular_stmt = select(ForumTopic).where(ForumTopic.is_deleted == False).order_by(ForumTopic.views_count.desc(), ForumTopic.id.desc()).limit(3)
        popular_topics = db.exec(popular_stmt).all()
        
        active_stmt = select(ForumTopic).where(ForumTopic.is_deleted == False).order_by(ForumTopic.created_at.desc()).limit(3)
        active_topics = db.exec(active_stmt).all()
        
        return {
            "popular": [{"id": t.id, "title": t.title} for t in popular_topics],
            "active": [{"id": t.id, "title": t.title} for t in active_topics]
        }
    
    search_term = search.strip()
    starts_with_value = f"{search_term}%"
    filtered_stmt = select(ForumTopic).where(ForumTopic.is_deleted == False).where(ForumTopic.title.ilike(starts_with_value)).limit(5)
    filtered_topics = db.exec(filtered_stmt).all()
    
    if not filtered_topics:
        contains_value = f"%{search_term}%"
        filtered_stmt = select(ForumTopic).where(ForumTopic.is_deleted == False).where(ForumTopic.title.ilike(contains_value)).limit(5)
        filtered_topics = db.exec(filtered_stmt).all()
    
    return {"filtered": [{"id": t.id, "title": t.title} for t in filtered_topics]}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_forum_topic(
    topic_data: ForumTopicCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Provjeravamo postoji li odabrana kategorija.
    category = db.get(
        ForumCategory,
        topic_data.category_id
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Kategorija nije pronađena."
        )

    # Pravimo novu forum temu.
    new_topic = ForumTopic(
        title=topic_data.title,
        content=topic_data.content,
        category_id=topic_data.category_id,
        user_id=current_user.id
    )

    db.add(new_topic)

    # flush dodjeljuje ID temi, ali još ne završava transakciju.
    db.flush()

    # Automatski dodjeljujemo bodove i provjeravamo medalje.
    register_topic_created(
        db,
        user_id=current_user.id,
        topic_id=new_topic.id,
        created_at=new_topic.created_at,
    )

    # Dodavanje tagova.
    if topic_data.tags:
        for tag_input in topic_data.tags:

            # Ako frontend pošalje naziv taga kao tekst.
            if isinstance(tag_input, str):
                clean_tag_name = tag_input.strip()

                # Preskačemo prazan tag.
                if not clean_tag_name:
                    continue

                # Provjeravamo postoji li već tag sa tim nazivom.
                tag = db.exec(
                    select(ForumTag).where(
                        ForumTag.name == clean_tag_name
                    )
                ).first()

                # Ako tag ne postoji, pravimo novi.
                if not tag:
                    tag = ForumTag(
                        name=clean_tag_name
                    )

                    db.add(tag)

                    # Potrebno da novi tag dobije ID.
                    db.flush()

                tag_id = tag.id

            # Ako frontend direktno pošalje ID postojećeg taga.
            else:
                tag_id = tag_input

            topic_tag = ForumTopicTag(
                topic_id=new_topic.id,
                tag_id=tag_id
            )

            db.add(topic_tag)

    # Tema, tagovi, reputacija i medalje spremaju se zajedno.
    db.commit()
    db.refresh(new_topic)

    return build_topic_list_item(
        db,
        new_topic
    )


# --- WIDGET API ENDPOINTS ---

@router.get("/popular", response_model=List[Dict[str, Any]])
def get_popular_sidebar_topics(db: Session = Depends(get_db)):
    from app.models.forum import ForumComment
    vremenska_granica = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=7)
    
    comments_sub = (
        select(ForumComment.topic_id, func.count(ForumComment.id).label("c_count"))
        .where(ForumComment.is_deleted == False)
        .group_by(ForumComment.topic_id)
        .subquery()
    )
    
    statement = (
        select(ForumTopic)
        .where(ForumTopic.is_deleted == False)
        .where(ForumTopic.created_at >= vremenska_granica)
        .join(comments_sub, comments_sub.c.topic_id == ForumTopic.id, isouter=True)
        .order_by((ForumTopic.views_count + func.coalesce(comments_sub.c.c_count, 0)).desc(), ForumTopic.id.desc())
        .limit(5)
    )
    
    popular_topics = db.exec(statement).all()
    return [build_topic_list_item(db, topic) for topic in popular_topics]


@router.get("/category-popular/{category_id}", response_model=List[Dict[str, Any]])
def get_category_popular_topics(category_id: int, db: Session = Depends(get_db)):
    from app.models.forum import ForumComment

    comments_sub = (
        select(ForumComment.topic_id, func.count(ForumComment.id).label("c_count"))
        .where(ForumComment.is_deleted == False)
        .group_by(ForumComment.topic_id)
        .subquery()
    )

    statement = (
        select(ForumTopic)
        .where(ForumTopic.is_deleted == False)
        .where(ForumTopic.category_id == category_id)
        .join(comments_sub, comments_sub.c.topic_id == ForumTopic.id, isouter=True)
        .order_by((ForumTopic.views_count + func.coalesce(comments_sub.c.c_count, 0)).desc(), ForumTopic.id.desc())
        .limit(5)
    )

    category_topics = db.exec(statement).all()
    return [build_topic_list_item(db, topic) for topic in category_topics]


@router.get("/{topic_id}/related", response_model=List[Dict[str, Any]])
def get_related_topics_api(topic_id: int, db: Session = Depends(get_db)):
    trenutna_tema = db.get(ForumTopic, topic_id)
    if not trenutna_tema or trenutna_tema.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")

    cist_naslov = re.sub(r'[.,\/#!$%\^&\*;:{}=\-_`~()?]', '', trenutna_tema.title.lower())
    sve_rijeci = cist_naslov.split()
    kljucne_rijeci = [rijec.strip() for rijec in sve_rijeci if len(rijec.strip()) > 2]

    if not kljucne_rijeci:
        return []

    uvjeti_pretrage = [ForumTopic.title.ilike(f"%{rijec}%") for rijec in kljucne_rijeci]

    from app.models.forum import ForumComment
    comments_sub = (
        select(ForumComment.topic_id, func.count(ForumComment.id).label("c_count"))
        .where(ForumComment.is_deleted == False)
        .group_by(ForumComment.topic_id)
        .subquery()
    )

    statement = (
        select(ForumTopic)
        .where(ForumTopic.is_deleted == False)
        .where(ForumTopic.category_id == trenutna_tema.category_id)
        .where(ForumTopic.id != trenutna_tema.id)
        .where(or_(*uvjeti_pretrage))
        .join(comments_sub, comments_sub.c.topic_id == ForumTopic.id, isouter=True)
        .order_by((ForumTopic.views_count + func.coalesce(comments_sub.c.c_count, 0)).desc(), ForumTopic.id.desc())
        .limit(4) 
    )

    slicne_teme = db.exec(statement).all()
    return [build_topic_list_item(db, topic) for topic in slicne_teme]


# --- REPORTS & ANNOUNCEMENTS ---
@router.get("/reports/active", response_model=List[Dict[str, Any]])
def get_active_reports(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Nemate ovlaštenje.")
    
    reports = db.exec(select(TopicReport).where(TopicReport.status == "pending").order_by(TopicReport.created_at.desc())).all()
    output = []
    for report in reports:
        topic = db.get(ForumTopic, report.topic_id)
        if not topic or topic.is_deleted: continue
        reporter = db.get(User, report.user_id)
        output.append({
            "report_id": report.id, "reason": report.reason, "created_at": report.created_at, "status": report.status,
            "reporter_name": reporter.full_name if reporter else "Nepoznat korisnik", "topic": build_topic_list_item(db, topic) 
        })
    return output

@router.get("/reports/handled", response_model=List[Dict[str, Any]])
def get_handled_reports(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Nemate ovlaštenje.")
    
    reports = db.exec(select(TopicReport).where(TopicReport.status.in_(["resolved", "dismissed"])).order_by(TopicReport.created_at.desc())).all()
    output = []
    for report in reports:
        topic = db.get(ForumTopic, report.topic_id)
        if not topic or topic.is_deleted: continue
        reporter = db.get(User, report.user_id)
        output.append({
            "report_id": report.id, "reason": report.reason, "created_at": report.created_at, "status": report.status,
            "reporter_name": reporter.full_name if reporter else "Nepoznat korisnik", "topic": build_topic_list_item(db, topic) 
        })
    return output

@router.patch("/reports/{report_id}/action")
def handle_report_action(report_id: int, action: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Nemate ovlaštenje.")
    report = db.get(TopicReport, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Prijava nije pronađena.")
    
    if action == "dismiss": report.status = "dismissed"
    elif action == "resolve": report.status = "resolved"
    else: raise HTTPException(status_code=400, detail="Nevalidna akcija.")
        
    db.add(report)
    db.commit()
    return {"success": True, "new_status": report.status}

@router.get("/announcements/active")
def get_active_announcements(db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    statement = select(AdminAnnouncement).where(
        AdminAnnouncement.is_active == True,
        (AdminAnnouncement.expires_at == None) | (AdminAnnouncement.expires_at > now)
    ).order_by(AdminAnnouncement.created_at.desc())
    return db.exec(statement).all()

@router.get("/{topic_id}")
def get_topic_details(topic_id: int, db: Session = Depends(get_db)):
    topic = db.get(ForumTopic, topic_id)
    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")

    comments = get_topic_comments(db, topic.id)
    comments_count = len(comments)
    votes_count = get_topic_votes_count(db, topic.id)

    return {
        "id": topic.id, "title": topic.title, "content": topic.content, "views_count": topic.views_count,
        "is_locked": getattr(topic, "is_locked", False), "created_at": topic.created_at, "updated_at": topic.updated_at,
        "author": get_author_data(db, topic.user_id), "category": get_category_data(db, topic.category_id),
        "tags": get_topic_tags(db, topic.id), "comments": comments,
        "stats": {"comments_count": comments_count, "answers_count": comments_count, "views_count": topic.views_count, "votes_count": votes_count, "has_best_answer": any(comment["is_best_answer"] for comment in comments)}
    }

@router.patch("/{topic_id}/view")
def increment_topic_view(topic_id: int, db: Session = Depends(get_db)):
    topic = db.get(ForumTopic, topic_id)
    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")
    

    topic.views_count += 1
    db.add(topic)
    db.commit()
    db.refresh(topic) 
    
    return {"id": topic.id, "views_count": topic.views_count}

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_topic(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    topic = db.get(ForumTopic, id)
    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")
    if current_user.role != UserRole.admin and topic.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Možete obrisati samo vlastitu temu.")
    topic.is_deleted = True
    db.add(topic)
    db.commit()
    return {"message": "Tema je uspješno obrisana.", "topic_id": id}

@router.post("/{topic_id}/report")
def report_topic(topic_id: int, report_data: ReportCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    topic = db.get(ForumTopic, topic_id)
    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema ne postoji.")
    report = TopicReport(topic_id=topic_id, user_id=current_user.id, reason=report_data.reason)
    db.add(report)
    db.commit()
    return {"success": True}