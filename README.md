# TK Student Hub — Platforma

**TK Student Hub** — platforma za studente telekomunikacija koja omogućava dijeljenje materijala, korisnih linkova, učestvovanje u forumu i upravljaju svojim profilom.

## Struktura projekta

```
telecommunications-student-hub/
  backend/       — FastAPI backend
  frontend/      — Vue 3 frontend
```

Brzi koraci za pokretanje (zsh)

Frontend:

```bash
cd /frontend
npm install
npm run dev
```

Backend (opcionalno):

```bash
cd /Users/amina.jahic/FET/RTPP/tk-student-hub/telecommunications-student-hub/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API dokumentacija (kad backend radi): `http://127.0.0.1:8000/docs`

Za detalje o frontend i backend specifičnim uputama pogledajte:

- `frontend/README.md`
- `backend/README.md`

## Timovi i funkcionalnosti

| PRojektni tim | Funkcionalnost | Folder |
|-----|---------------|--------|
| Tim 1 | Workshops | `backend/app/routers/workshops.py`, `frontend/src/views/workshops/` |
| Tim 2 | Materijali | `backend/app/routers/materials.py`, `frontend/src/views/materials/` |
| Tim 3 | Forum | `backend/app/routers/forum.py`, `frontend/src/views/forum/` |
| Tim 4 | Profili & Dashboard | `backend/app/routers/profiles.py`, `frontend/src/views/profiles/` |

## Tehnologije

- **Backend:** Python, FastAPI, SQLAlchemy, Alembic, JWT
- **Frontend:** Vue 3, Vite, Tailwind CSS, Vue Router
- **Baza:** SQLite (development), PostgreSQL (produkcija)

## Autentifikacija

Platforma koristi JWT tokene. Nakon prijave token se čuva u `localStorage` i šalje sa svakim API pozivom u headeru:
```
Authorization: Bearer YOUR_TOKEN_HERE
```
