# TK Student Hub — Platforma

**TK Student Hub** — platforma za studente telekomunikacija koja omogućava dijeljenje materijala, korisnih linkova, učestvovanje u forumu i upravljaju svojim profilom.

## O projektu

TK Student Hub povezuje studente, kompanije i administratore platforme. Studenti mogu pratiti i dijeliti studijske materijale, prijavljivati se na prakse i oglase, učestvovati u diskusijama na forumu i pratiti vlastitu aktivnost na platformi. Kompanije mogu objavljivati oglase za prakse i upravljati prijavama. Administratori upravljaju korisnicima i kompanijama i odobravaju sadržaj.

## Korisničke uloge

| Uloga | Opis |
|---|---|
| Posjetilac | Neregistrovani korisnik koji pregledava javni sadržaj |
| Student | Registrovani korisnik s punim pristupom funkcionalnostima platforme |
| Administrator | Upravlja korisnicima i sadržajem platforme |

Pored toga, kompanije imaju zaseban tip naloga za objavu oglasa i upravljanje prijavama.

## Tehnologije

**Backend:** FastAPI, SQLModel, SQLAlchemy, Alembic, SQLite, JWT autentifikacija

**Frontend:** Vue 3, Vite, Tailwind CSS, Vue Router

## Struktura projekta

```
tk-student-hub/
  backend/       - FastAPI backend
  frontend/      - Vue 3 frontend
```

## Preuzimanje projekta

```bash
git clone <url-repozitorija>
cd tk-student-hub
```

## Brzi koraci za pokretanje (zsh)

Za pokretanje cijele platforme potrebno je pokrenuti backend i frontend odvojeno, svaki u svom terminalu.

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

- `frontend/README.md` - instalacija, struktura, povezivanje s backendom,
- `backend/README.md` - instalacija, konfiguracija, migracije, API.

## Autentifikacija

Platforma koristi JWT tokene. Nakon prijave token se čuva u `localStorage` i šalje sa svakim API pozivom u headeru:
```
Authorization: Bearer YOUR_TOKEN_HERE
```

## Timovi i funkcionalnosti

Projekat je razvijen kroz rad više timova, gdje je svaki tim odgovoran za zaseban funkcionalni dio platforme:

| PRojektni tim | Funkcionalnost | Folder | Članova tima |
|-----|---------------|--------|---|
| Tim 1 | Prakse i edukacije | `backend/app/routers/prakse.py`, `frontend/src/views/prakse/` | - |
| Tim 2 | Materijali | `backend/app/routers/materials.py`, `frontend/src/views/materials/` | Lejla Kadušić, Amer Imamović, Marinela Mitić |
| Tim 3 | Forum | `backend/app/routers/forum.py`, `frontend/src/views/forum/` | - |
| Tim 4 | Profili & Dashboard | `backend/app/routers/profiles.py`, `frontend/src/views/profiles/` | - |

**Tim 2 Opis:**
- **Lejla Kadušić** — Upload materijala, komentari (CRUD), paginacija
- **Amer Imamović** — Brisanje materijala, bookmark (omiljeni), filteri (godina, tip, predmet)
- **Marinela Mitić** — Forma za dodavanje materijala s validacijom, preuzimanje materijala, ocjenjivanje (zvjezdice), thumbnail sličice, dark mode