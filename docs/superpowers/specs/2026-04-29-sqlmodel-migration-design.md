# SQLModel Migration Design

**Date:** 2026-04-29  
**Scope:** Replace SQLAlchemy with SQLModel across the FastAPI backend

---

## Context

The backend is early-stage: one real model (`User`), one real router (`auth`), and four stub routers (educations, materials, forum, profiles). This is the ideal moment to migrate cleanly before teams build their features on top.

---

## Approach

Full SQLModel replacement (Option A). All SQLAlchemy-style models and session wiring are replaced with SQLModel equivalents. No mixed ORM styles.

---

## Section 1: Database & Engine

`database.py` is rewritten using SQLModel's engine and session primitives:

- `create_engine` from `sqlmodel` (wraps SQLAlchemy, same args)
- `Session` from `sqlmodel` used as context manager in `get_db`
- `Base.metadata.create_all` replaced by `SQLModel.metadata.create_all`
- `declarative_base()` and `SessionLocal`/`sessionmaker` removed entirely
- `main.py` calls a `create_db_and_tables()` function on startup; the `Base` import is removed

## Section 2: Models

`models/user.py` is rewritten as a `SQLModel` table class:

- `class User(SQLModel, table=True)` replaces `class User(Base)`
- Fields use `Field(...)` instead of `Column(...)`
- `UserRole` becomes `str, Enum` (required for SQLModel compatibility)
- `created_at` uses Python `datetime` with `default=None` (no `server_default`)
- `models/__init__.py` imports `User` so `SQLModel.metadata` sees the table at startup

Team model files (`educations.py`, `materials.py`, `forum.py`, `profiles.py`) are **not** created — each team creates their own when they build their features. They must import their models in `models/__init__.py` when ready.

## Section 3: Routers & Security

- All files that do `from sqlalchemy.orm import Session` are updated to `from sqlmodel import Session`
- No query rewrites needed — SQLModel sessions support the same `.query()`, `.add()`, `.commit()`, `.refresh()` API
- `auth.py` request/response schemas (`RegisterRequest`, `TokenResponse`) remain as Pydantic `BaseModel` — they are not DB tables
- `security.py` gets only the Session import swap

Affected files: `app/core/security.py`, `app/routers/auth.py`, `app/routers/prakse.py`, `app/routers/workshops.py`, `app/routers/materials.py`, `app/routers/forum.py`, `app/routers/profiles.py`

> Note: router files are currently named after their original Bosnian/workshop names. Renaming them to English (`educations.py`, etc.) is out of scope for this migration — that can be done separately.

## Section 4: Dependencies & Cleanup

`requirements.txt` changes:
- Add `sqlmodel`
- Remove `SQLAlchemy` (bundled inside SQLModel)
- Remove `psycopg2-binary` (SQLite is the target database)

No changes to: `core/config.py`, frontend, router logic, auth flow.

---

## Files Changed

| File | Change |
|------|--------|
| `backend/requirements.txt` | Add sqlmodel, remove SQLAlchemy + psycopg2-binary |
| `backend/app/database.py` | Full rewrite with SQLModel engine/session |
| `backend/app/main.py` | Replace `Base.metadata.create_all` with `create_db_and_tables()` |
| `backend/app/models/user.py` | Rewrite as SQLModel table class |
| `backend/app/models/__init__.py` | Import User only |
| `backend/app/core/security.py` | Session import swap |
| `backend/app/routers/auth.py` | Session import swap |
| `backend/app/routers/*.py` (stubs) | Session import swap |
