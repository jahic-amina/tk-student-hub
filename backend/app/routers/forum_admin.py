from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlmodel import Session, select
from typing import List, Dict, Any
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.forum import TopicReport, AdminAnnouncement, ForumTopic, ForumCategory
from datetime import datetime, timedelta

router = APIRouter(prefix="/admin", tags=["Admin"])

#Pomoćna funkcija za verifikaciju admina
def get_current_admin(current_user: User = Depends(get_current_user)):
    if getattr(current_user, "role", None) != "admin":
         raise HTTPException(status_code=403, detail="Pristup dozvoljen samo administratorima.")
    return current_user

#Korisnici (Lista i promjena uloge)
@router.get("/users")
def get_all_users(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    users = db.exec(select(User)).all()
    return [{"id": u.id, "email": u.email, "full_name": u.full_name, "role": getattr(u, "role", "member")} for u in users]

#Promjena uloge korisnika
@router.patch("/users/{user_id}/role")
def change_user_role(user_id: int, role: str, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    if role not in ["admin", "member"]:
        raise HTTPException(status_code=400, detail="Nevažeća uloga.")
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen.")
    user.role = role
    db.add(user)
    db.commit()
    return {"message": f"Uloga promijenjena u {role}"}

#Prijave (Reports)
@router.get("/reports")
def get_reports(status: str = "pending", db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    if status not in ["pending", "resolved"]:
        raise HTTPException(status_code=400, detail="Nevažeći status prijave. Dozvoljeno je 'pending' ili 'resolved'.")
        
    statement = select(TopicReport, ForumTopic).join(ForumTopic, TopicReport.topic_id == ForumTopic.id).where(TopicReport.status == status)
    results = db.exec(statement).all()
    output = []
    for report, topic in results:
        output.append({
            "report_id": report.id,
            "reason": report.reason,
            "created_at": report.created_at,
            "status": report.status,
            "topic": {"id": topic.id, "title": topic.title, "content": topic.content}
        })
    return output

@router.delete("/reports/{report_id}")
def dismiss_report(report_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    report = db.get(TopicReport, report_id)
    if report:
        report.status = "resolved"
        db.add(report)
        db.commit()
    return {"success": True}

#Zaključavanje teme
@router.patch("/topics/{topic_id}/lock")
def toggle_topic_lock(topic_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    topic = db.get(ForumTopic, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")
    topic.is_locked = not topic.is_locked
    db.add(topic)
    db.commit()
    return {"is_locked": topic.is_locked}

#Globalna obavještenja sa odabirom trajanja
@router.post("/announcements")
def create_announcement(content: dict = Body(...), db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    content_text = content.get("content", "")
    title = content.get("title")
    duration_days = content.get("duration_days", 0)  

    existing_active = db.exec(
        select(AdminAnnouncement).where(AdminAnnouncement.is_active == True)
    ).all()
    for old_ann in existing_active:
        old_ann.is_active = False
        db.add(old_ann)
    
    expires_at = None
    if duration_days and duration_days > 0:
        expires_at = datetime.utcnow() + timedelta(days=int(duration_days))
        
    new_ann = AdminAnnouncement(
        admin_id=admin.id, 
        title=title,
        content=content_text,
        expires_at=expires_at,
        is_active=True
    )
    db.add(new_ann)
    db.commit()
    return {"success": True, "announcement": new_ann}



#Admin ruta za dohvatanje svih obavještenja (uključujući neaktivna i istekla)
@router.get("/announcements/all")
def get_all_announcements(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    anns = db.exec(select(AdminAnnouncement).order_by(AdminAnnouncement.created_at.desc())).all()
    return anns

#Admin ruta za editovanje postojeceg obavjestenja
@router.patch("/announcements/{ann_id}")
def update_announcement(ann_id: int, payload: dict = Body(...), db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    ann = db.get(AdminAnnouncement, ann_id)
    if not ann:
        raise HTTPException(status_code=404, detail="Obavještenje nije pronađeno.")
    
    if "title" in payload:
        ann.title = payload["title"]

    if "content" in payload:
        ann.content = payload["content"]
        
    if "duration_days" in payload:
        duration_days = payload["duration_days"]
        if duration_days and duration_days > 0:
            ann.expires_at = datetime.utcnow() + timedelta(days=int(duration_days))
        else:
            ann.expires_at = None  # Postaje beskonačno
            
    if "is_active" in payload:
        ann.is_active = payload["is_active"]
        
    db.add(ann)
    db.commit()
    db.refresh(ann)
    return {"success": True, "announcement": ann}

@router.delete("/announcements/{ann_id}")
def delete_announcement(ann_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    ann = db.get(AdminAnnouncement, ann_id)
    if ann:
        ann.is_active = False
        db.add(ann)
        db.commit()
    return {"success": True}