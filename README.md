# TK Student Hub — Platforma

Ovo je kopija originalnog projekta "girls-in-science", rebrendirana i lokalizovana kao **TK Student Hub** — platforma za studente telekomunikacija.

## Struktura projekta

```
telecommunications-student-hub/
  backend/       — FastAPI backend
  frontend/      — Vue 3 frontend
```

Brzi koraci za pokretanje (zsh)

Frontend:

```bash
cd /Users/amina.jahic/FET/RTPP/tk-student-hub/telecommunications-student-hub/frontend
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

Napomene i daljnji koraci

- Frontend je već preimenovan i preveden na bosanski; još uvijek možete zatražiti potpunu reviziju sadržaja, poruka grešaka i validacije.
- Boje su promijenjene na primarnu narandžastu (#ff7a00) i bijelu za TK brend.
- Ako želite, mogu zamijeniti slike (hero, favicon) sa prilagođenim orange/white assetima.
- Kontakt forma i drugi vanjski servisi su ostali kao u originalu; javite ako želite podesiti Formspree ili backend endpoint za slanje poruka.

Za detalje o frontend i backend specifičnim uputama pogledajte:

- `frontend/README.md`
- `backend/README.md`