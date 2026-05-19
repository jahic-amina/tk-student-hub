# TK Student Hub — Platforma

**TK Student Hub** — platforma za studente telekomunikacija koja omogućava dijeljenje materijala, korisnih linkova, učestvovanje u forumu i upravljaju svojim profilom.

## Struktura projekta

```
tk-student-hub/
  backend/       — FastAPI backend
  frontend/      — Vue 3 frontend
```

Brzi koraci za pokretanje (zsh)

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Backend (opcionalno):

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API dokumentacija (kad backend radi): `http://127.0.0.1:8000/docs`

Za detalje o frontend i backend specifičnim uputama pogledajte:

- `frontend/README.md`
- `backend/README.md`

## Git Workflow

- Radite na grani `dev` — ne raditi commit direktno na `main`
- Konvencija za imenovanje grana: `timX/naziv-funkcionalnosti/naziv-featurea`
  - Primjeri: `tim1/prakse/lista`, `tim2/materijali/upload`, `tim3/forum/novi-post`
- Commit poruke trebaju biti smislene i opisivati šta je promijenjeno
- Radite commit često — ne čekajte da sve bude gotovo pa onda jedan veliki commit
- Pull request prema `main` grani se radi tek na kraju sprinta, nakon pregleda asistentice

## Timovi i funkcionalnosti

| PRojektni tim | Funkcionalnost | Folder |
|-----|---------------|--------|
| Tim 1 | Prakse i edukacije | `backend/app/routers/prakse.py`, `frontend/src/views/prakse/` |
| Tim 2 | Materijali | `backend/app/routers/materials.py`, `frontend/src/views/materials/` |
| Tim 3 | Forum | `backend/app/routers/forum.py`, `frontend/src/views/forum/` |
| Tim 4 | Profili & Dashboard | `backend/app/routers/profiles.py`, `frontend/src/views/profiles/` |

## Tehnologije

- **Backend:** Python, FastAPI, SQLModel, JWT
- **Frontend:** Vue 3, Vite, Tailwind CSS, Vue Router
- **Baza:** SQLite

## Autentifikacija

Platforma koristi JWT tokene. Nakon prijave token se čuva u `localStorage` i šalje sa svakim API pozivom u headeru:
```
Authorization: Bearer YOUR_TOKEN_HERE
```
