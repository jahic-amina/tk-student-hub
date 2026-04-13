# TK Student Hub — Backend

Izgrađeno sa FastAPI, SQLAlchemy i SQLite (za razvoj).

## Postavljanje projekta

1. Kreiraj i aktiviraj virtualno okruženje:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instaliraj zavisnosti:
```bash
pip install -r requirements.txt
```
3. Pokreni server:
```bash
cd backend
uvicorn app.main:app --reload
```

4. Otvori API dokumentaciju:
```bash
http://127.0.0.1:8000/docs
```

## Struktura projekta
```
app/
  core/
    config.py       — postavke aplikacije, čita iz .env fajla
    security.py     — hashiranje lozinki, JWT tokeni
  models/
    user.py         — tabela korisnika (dijele sve ekipe)
  routers/
    auth.py         — registracija i prijava (ne mijenjati)
    workshops.py    — Projektni tim 1
    mentoring.py    — Projektni tim 2
    forum.py        — Projektni tim 3
    profiles.py     — Projektni tim 4
  main.py           — ulazna tačka aplikacije
  database.py       — konekcija na bazu podataka
```
## Autentifikacija

Svi zaštićeni endpointi zahtijevaju Bearer token u headeru:
```
Authorization: Bearer YOUR_TOKEN_HERE
```
Token se dobija pozivom `POST /auth/login`

## Za projektne timove

1. Vaš router fajl je već kreiran i registrovan u aplikaciji
2. Dodajte svoje modele u `app/models/`
3. Dizajnirajte svoje tabele u bazi podataka
4. Dodajte svoje endpointe u vaš router fajl
5. Koristite `Depends(get_current_user)` da dobijete prijavljenog korisnika
6. Kreirajte vlastite `.env` varijable ako je potrebno