from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Dict, Any
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.forum import TopicReport, AdminAnnouncement, ForumTopic, ForumCategory

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
def get_reports(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    statement = select(TopicReport, ForumTopic).join(ForumTopic, TopicReport.topic_id == ForumTopic.id).where(TopicReport.status == "pending")
    results = db.exec(statement).all()
    output = []
    for report, topic in results:
        output.append({
            "report_id": report.id,
            "reason": report.reason,
            "created_at": report.created_at,
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

#Globalna obavještenja
@router.post("/announcements")
def create_announcement(content: dict, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    ann = AdminAnnouncement(admin_id=admin.id, content=content.get("content", ""))
    db.add(ann)
    db.commit()
    return {"success": True}

@router.get("/announcements/active")
def get_active_announcements(db: Session = Depends(get_db)): # Ovo je public ruta da bi se obavjestenja prikazala svima
    anns = db.exec(select(AdminAnnouncement).where(AdminAnnouncement.is_active == True).order_by(AdminAnnouncement.created_at.desc())).all()
    return anns

@router.delete("/announcements/{ann_id}")
def delete_announcement(ann_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    ann = db.get(AdminAnnouncement, ann_id)
    if ann:
        ann.is_active = False
        db.add(ann)
        db.commit()
    return {"success": True}