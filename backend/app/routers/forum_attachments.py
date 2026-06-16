from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from typing import List
from datetime import datetime
import os
import shutil

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.forum import ForumTopic, ForumComment, TopicAttachment, CommentAttachment

router = APIRouter(prefix="/forum/attachments", tags=["Forum Attachments"])

UPLOAD_DIR = "uploads/forum"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf", ".docx", ".txt"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
MAX_FILES_PER_POST = 3

os.makedirs(UPLOAD_DIR, exist_ok=True)


def validate_file(file: UploadFile, content: bytes):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Format {ext} nije dozvoljen. Dozvoljeni: {', '.join(ALLOWED_EXTENSIONS)}")
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Fajl je prevelik. Maksimalna veličina je 5 MB.")


# ── TOPIC ATTACHMENTS ────────────────────────────────────────────────────────

@router.post("/topic/{topic_id}", status_code=status.HTTP_201_CREATED)
async def upload_topic_attachment(
    topic_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    topic = db.get(ForumTopic, topic_id)
    if not topic or topic.is_deleted:
        raise HTTPException(status_code=404, detail="Tema nije pronađena.")

    existing = db.exec(select(TopicAttachment).where(TopicAttachment.topic_id == topic_id)).all()
    if len(existing) + len(files) > MAX_FILES_PER_POST:
        raise HTTPException(status_code=400, detail=f"Maksimalan broj fajlova po temi je {MAX_FILES_PER_POST}.")

    saved = []
    for file in files:
        content = await file.read()
        validate_file(file, content)

        filename = f"{topic_id}_{datetime.utcnow().timestamp()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, "topics", filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as f:
            f.write(content)

        attachment = TopicAttachment(
            topic_id=topic_id,
            filename=file.filename,
            file_path=file_path,
            file_size=len(content),
            mime_type=file.content_type or "application/octet-stream",
            created_at=datetime.utcnow()
        )
        db.add(attachment)
        db.flush()
        saved.append({"id": attachment.id, "filename": file.filename, "file_size": len(content)})

    db.commit()
    return {"uploaded": saved}


@router.get("/topic/{topic_id}")
def get_topic_attachments(topic_id: int, db: Session = Depends(get_db)):
    attachments = db.exec(select(TopicAttachment).where(TopicAttachment.topic_id == topic_id)).all()
    return [{"id": a.id, "filename": a.filename, "file_size": a.file_size, "mime_type": a.mime_type} for a in attachments]


@router.get("/topic/{topic_id}/download/{attachment_id}")
def download_topic_attachment(topic_id: int, attachment_id: int, db: Session = Depends(get_db)):
    attachment = db.get(TopicAttachment, attachment_id)
    if not attachment or attachment.topic_id != topic_id:
        raise HTTPException(status_code=404, detail="Fajl nije pronađen.")
    if not os.path.exists(attachment.file_path):
        raise HTTPException(status_code=404, detail="Fajl nije pronađen na serveru.")
    return FileResponse(path=attachment.file_path, filename=attachment.filename, media_type=attachment.mime_type)


# ── COMMENT ATTACHMENTS ──────────────────────────────────────────────────────

@router.post("/comment/{comment_id}", status_code=status.HTTP_201_CREATED)
async def upload_comment_attachment(
    comment_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = db.get(ForumComment, comment_id)
    if not comment or comment.is_deleted:
        raise HTTPException(status_code=404, detail="Komentar nije pronađen.")

    existing = db.exec(select(CommentAttachment).where(CommentAttachment.comment_id == comment_id)).all()
    if len(existing) + len(files) > MAX_FILES_PER_POST:
        raise HTTPException(status_code=400, detail=f"Maksimalan broj fajlova po komentaru je {MAX_FILES_PER_POST}.")

    saved = []
    for file in files:
        content = await file.read()
        validate_file(file, content)

        filename = f"{comment_id}_{datetime.utcnow().timestamp()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, "comments", filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as f:
            f.write(content)

        attachment = CommentAttachment(
            comment_id=comment_id,
            filename=file.filename,
            file_path=file_path,
            file_size=len(content),
            mime_type=file.content_type or "application/octet-stream",
            created_at=datetime.utcnow()
        )
        db.add(attachment)
        db.flush()
        saved.append({"id": attachment.id, "filename": file.filename, "file_size": len(content)})

    db.commit()
    return {"uploaded": saved}


@router.get("/comment/{comment_id}")
def get_comment_attachments(comment_id: int, db: Session = Depends(get_db)):
    attachments = db.exec(select(CommentAttachment).where(CommentAttachment.comment_id == comment_id)).all()
    return [{"id": a.id, "filename": a.filename, "file_size": a.file_size, "mime_type": a.mime_type} for a in attachments]


@router.get("/comment/{comment_id}/download/{attachment_id}")
def download_comment_attachment(comment_id: int, attachment_id: int, db: Session = Depends(get_db)):
    attachment = db.get(CommentAttachment, attachment_id)
    if not attachment or attachment.comment_id != comment_id:
        raise HTTPException(status_code=404, detail="Fajl nije pronađen.")
    if not os.path.exists(attachment.file_path):
        raise HTTPException(status_code=404, detail="Fajl nije pronađen na serveru.")
    return FileResponse(path=attachment.file_path, filename=attachment.filename, media_type=attachment.mime_type)