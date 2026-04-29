# SQLModel Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace SQLAlchemy with SQLModel across the FastAPI backend so all DB models, sessions, and engine wiring use SQLModel conventions.

**Architecture:** `database.py` is rewritten with SQLModel's engine/session primitives. `models/user.py` becomes a `SQLModel` table class. All routers and security swap their `Session` import from `sqlalchemy.orm` to `sqlmodel`. No query logic changes.

**Tech Stack:** Python, FastAPI, SQLModel, SQLite, Pydantic v2

---

## File Map

| File | Action |
|------|--------|
| `backend/requirements.txt` | Modify — add `sqlmodel`, remove `SQLAlchemy`, remove `psycopg2-binary` |
| `backend/app/database.py` | Rewrite |
| `backend/app/main.py` | Modify — swap startup call |
| `backend/app/models/__init__.py` | Modify — add User import |
| `backend/app/models/user.py` | Rewrite |
| `backend/app/core/security.py` | Modify — Session import swap |
| `backend/app/routers/auth.py` | Modify — Session import swap |
| `backend/app/routers/prakse.py` | Modify — Session import swap |
| `backend/app/routers/workshops.py` | Modify — Session import swap |
| `backend/app/routers/materials.py` | Modify — Session import swap |
| `backend/app/routers/forum.py` | Modify — Session import swap |
| `backend/app/routers/profiles.py` | Modify — Session import swap |

---

## Task 1: Update Dependencies

**Files:**
- Modify: `backend/requirements.txt`

- [ ] **Step 1: Install sqlmodel**

Run from `backend/`:
```bash
pip install sqlmodel
```
Expected output: `Successfully installed sqlmodel-0.0.21 ...`

- [ ] **Step 2: Update requirements.txt**

Replace the contents of `backend/requirements.txt`. Remove `SQLAlchemy==2.0.49` and `psycopg2-binary==2.9.11`, add `sqlmodel`. The file should contain (order doesn't matter, just ensure these lines reflect reality):

```
alembic==1.18.4
annotated-types==0.7.0
anyio==4.13.0
bcrypt==4.0.1
certifi==2026.2.25
charset-normalizer==3.4.7
click==8.3.2
dnspython==2.8.0
ecdsa==0.19.2
email-validator==2.3.0
fastapi==0.135.3
h11==0.16.0
idna==3.11
Mako==1.3.10
multidict==6.7.1
passlib==1.7.4
pydantic==2.12.5
pydantic-settings==2.13.1
pydantic_core==2.41.5
python-dotenv==1.2.2
python-jose==3.5.0
python-multipart==0.0.26
requests==2.33.1
rich==14.3.4
rsa==4.9.1
six==1.17.0
sqlmodel
starlette==1.0.0
typing_extensions==4.15.0
uvicorn==0.44.0
```

- [ ] **Step 3: Verify import works**

```bash
python -c "import sqlmodel; print(sqlmodel.__version__)"
```
Expected: prints a version string like `0.0.21`

- [ ] **Step 4: Commit**

```bash
git add backend/requirements.txt
git commit -m "deps: replace SQLAlchemy with sqlmodel, drop psycopg2-binary"
```

---

## Task 2: Rewrite database.py

**Files:**
- Modify: `backend/app/database.py`

- [ ] **Step 1: Rewrite the file**

Replace the entire contents of `backend/app/database.py` with:

```python
from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session
```

- [ ] **Step 2: Verify syntax**

```bash
cd backend && python -c "from app.database import get_db, create_db_and_tables; print('OK')"
```
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add backend/app/database.py
git commit -m "refactor: rewrite database.py with SQLModel engine and session"
```

---

## Task 3: Rewrite models/user.py

**Files:**
- Modify: `backend/app/models/user.py`
- Modify: `backend/app/models/__init__.py`

- [ ] **Step 1: Rewrite models/user.py**

Replace the entire contents of `backend/app/models/user.py` with:

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime

class UserRole(str, Enum):
    member = "member"
    mentor = "mentor"
    admin = "admin"

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    full_name: str
    password_hash: str
    role: UserRole = Field(default=UserRole.member)
    created_at: Optional[datetime] = Field(default=None)
```

- [ ] **Step 2: Update models/__init__.py**

Replace the contents of `backend/app/models/__init__.py` with:

```python
from app.models.user import User
```

- [ ] **Step 3: Verify the model imports cleanly**

```bash
cd backend && python -c "from app.models.user import User, UserRole; print('OK')"
```
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add backend/app/models/user.py backend/app/models/__init__.py
git commit -m "refactor: rewrite User model as SQLModel table class"
```

---

## Task 4: Update main.py

**Files:**
- Modify: `backend/app/main.py`

- [ ] **Step 1: Swap startup wiring**

In `backend/app/main.py`, replace:

```python
from app.database import Base, engine
```

with:

```python
from app.database import create_db_and_tables
```

And replace:

```python
Base.metadata.create_all(bind=engine)
```

with:

```python
create_db_and_tables()
```

The final `backend/app/main.py` should look like:

```python
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
```

- [ ] **Step 2: Verify app loads**

```bash
cd backend && python -c "from app.main import app; print('OK')"
```
Expected: `OK` (and a `students.db` file created in the working directory if it didn't exist)

- [ ] **Step 3: Commit**

```bash
git add backend/app/main.py
git commit -m "refactor: replace Base.metadata.create_all with create_db_and_tables()"
```

---

## Task 5: Swap Session import in security.py

**Files:**
- Modify: `backend/app/core/security.py`

- [ ] **Step 1: Swap the import**

In `backend/app/core/security.py`, replace:

```python
from sqlalchemy.orm import Session
```

with:

```python
from sqlmodel import Session
```

- [ ] **Step 2: Verify**

```bash
cd backend && python -c "from app.core.security import get_current_user; print('OK')"
```
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add backend/app/core/security.py
git commit -m "refactor: swap sqlalchemy Session import for sqlmodel in security.py"
```

---

## Task 6: Swap Session import in all routers

**Files:**
- Modify: `backend/app/routers/auth.py`
- Modify: `backend/app/routers/prakse.py`
- Modify: `backend/app/routers/workshops.py`
- Modify: `backend/app/routers/materials.py`
- Modify: `backend/app/routers/forum.py`
- Modify: `backend/app/routers/profiles.py`

In every file listed above, replace:

```python
from sqlalchemy.orm import Session
```

with:

```python
from sqlmodel import Session
```

- [ ] **Step 1: Update auth.py**

Open `backend/app/routers/auth.py` and make the swap above.

- [ ] **Step 2: Update prakse.py**

Open `backend/app/routers/prakse.py` and make the swap above.

- [ ] **Step 3: Update workshops.py**

Open `backend/app/routers/workshops.py` and make the swap above.

- [ ] **Step 4: Update materials.py**

Open `backend/app/routers/materials.py` and make the swap above.

- [ ] **Step 5: Update forum.py**

Open `backend/app/routers/forum.py` and make the swap above.

- [ ] **Step 6: Update profiles.py**

Open `backend/app/routers/profiles.py` and make the swap above.

- [ ] **Step 7: Verify all routers import cleanly**

```bash
cd backend && python -c "
from app.routers import auth, forum, profiles
from app.routers import prakse, workshops, materials
print('OK')
"
```
Expected: `OK`

- [ ] **Step 8: Commit**

```bash
git add backend/app/routers/auth.py backend/app/routers/prakse.py backend/app/routers/workshops.py backend/app/routers/materials.py backend/app/routers/forum.py backend/app/routers/profiles.py
git commit -m "refactor: swap sqlalchemy Session import for sqlmodel in all routers"
```

---

## Task 7: Smoke Test the Running Server

- [ ] **Step 1: Start the server**

```bash
cd backend && uvicorn app.main:app --reload
```
Expected: server starts with no import errors, output includes `Application startup complete.`

- [ ] **Step 2: Test the root endpoint**

In a second terminal:
```bash
curl http://localhost:8000/
```
Expected:
```json
{"message":"TK Student Hub API radi"}
```

- [ ] **Step 3: Test registration**

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","full_name":"Test User","password":"secret123"}'
```
Expected: JSON with `access_token` and `token_type: "bearer"`

- [ ] **Step 4: Test login**

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=secret123"
```
Expected: JSON with `access_token` and `token_type: "bearer"`

- [ ] **Step 5: Stop the server and commit**

Stop with `Ctrl+C`. No code changes in this task — nothing to commit.

---

## Task 8: Final Verification Commit

- [ ] **Step 1: Confirm no SQLAlchemy imports remain in app code**

```bash
grep -r "from sqlalchemy" backend/app/
```
Expected: no output (zero matches)

- [ ] **Step 2: Confirm sqlmodel is used everywhere**

```bash
grep -r "from sqlmodel" backend/app/
```
Expected: matches in `database.py`, `models/user.py`, `core/security.py`, and all routers that use `Session`

- [ ] **Step 3: Tag migration complete**

```bash
git tag sqlmodel-migration-complete
```
