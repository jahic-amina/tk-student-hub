# TK Student Hub — Backend

Backend dio platforme TK Student Hub, razvijen u FastAPI frameworku. Pruža REST API za sve funkcionalnosti platforme - autentifikaciju, profile, materijale, forum, prakse i oglase, notifikacije i historiju aktivnosti.

## Tehnologije

- **FastAPI** - web framework za izradu API-ja
- **SQLModel** - ORM, kombinacija SQLAlchemy i Pydantic modela
- **SQLAlchemy** - rad s relacionom bazom podataka
- **Alembic** - upravljanje migracijama baze podataka
- **SQLite** - baza podataka za razvojno okruženje
- **JWT (JSON Web Token)** - autentifikacija i autorizacija korisnika
- **Pydantic Settings** - upravljanje konfiguracijom i environment varijablama

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
backend/
├── alembic/                   # Migracije baze podataka
│   └── versions/
├── app/
│   ├── core/                  # Konfiguracija i sigurnost (JWT, hashing)
│   ├── enums/                 # Enum tipovi (ActivityType i sl.)
│   ├── models/                # SQLModel modeli i Pydantic sheme
│   ├── routers/                # API rute (endpoints)
│   ├── services/                # Servisi (npr. activity_log_service)
│   ├── database.py            # Konekcija na bazu i sesije
│   ├── main.py                 # Ulazna tačka aplikacije
│   └── .env                    # Environment varijable (kreira se lokalno, nije u git-u)
├── uploads/                    # Uploadovani fajlovi (slike, dokumenti)
├── alembic.ini
├── requirements.txt
└── studenthub.db                # SQLite baza (generiše se automatski)
```

## Instalacija

### 1. Kloniranje repozitorija

```bash
git clone <url-repozitorija>
cd tk-student-hub/backend
```

### 2. Kreiranje virtualnog okruženja

```bash
python -m venv venv
```

Aktivacija na Windowsu:
```bash
venv\Scripts\activate
```

Aktivacija na macOS/Linuxu:
```bash
source venv/bin/activate
```

### 3. Instalacija zavisnosti

```bash
pip install -r requirements.txt
```

## Konfiguracija — Environment varijable

Prije pokretanja aplikacije potrebno je kreirati `.env` fajl **unutar `app` foldera**, na putanji:

```
backend/app/.env
```

Sadržaj fajla treba sadržavati sljedeće varijable:

```env
APP_NAME=TK Student Hub
SECRET_KEY=tvoj_tajni_kljuc
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./studenthub.db
```

**Napomena:** Sve navedene varijable su obavezne. Ako bilo koja nedostaje, aplikacija će prijaviti grešku pri pokretanju.

`SECRET_KEY` treba biti dovoljno dug i nasumičan string koji se koristi za potpisivanje JWT tokena. Generira se lokalno, na primjer pomoću komande:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

`.env` fajl se ne commituje u git repozitorij iz sigurnosnih razloga - svaki član tima kreira svoj lokalno.

## Autentifikacija

Svi zaštićeni endpointi zahtijevaju Bearer token u headeru:

```
Authorization: Bearer YOUR_TOKEN_HERE
```

Token se dobija pozivom `POST /auth/login`

## Migracije baze podataka (Alembic)
Nakon konfiguracije `.env` fajla, potrebno je pokrenuti migracije kako bi se kreirale sve tabele u bazi:

```bash
alembic upgrade head
```

### Kreiranje nove migracije (nakon izmjene modela)

```bash
# Iz backend/ foldera, s aktiviranim virtualnim okruženjem
alembic revision --autogenerate -m "opis_izmjene"
alembic upgrade head
```

## Pokretanje aplikacije

```bash
uvicorn app.main:app --reload
```

Aplikacija će biti dostupna na:

```
http://127.0.0.1:8000
```

## API dokumentacija

FastAPI automatski generiše interaktivnu dokumentaciju svih dostupnih endpointa:

- **Swagger UI:** http://127.0.0.1:8000/docs

## Korisničke uloge

| Uloga | Opis |
|---|---|
| Posjetilac | Neregistrovani korisnik koji pregledava javni sadržaj |
| Student | Registrovani korisnik s punim pristupom funkcionalnostima platforme |
| Administrator | Upravlja korisnicima i sadržajem platforme |

## Glavni moduli (routeri)

| Modul | Opis |
|---|---|
| `auth` | Registracija i prijava korisnika i kompanija |
| `profiles` | Pregled i uređivanje korisničkog profila, upload profilne slike |
| `materials` | Upload, pregled, ocjenjivanje i komentarisanje studijskih materijala |
| `forum` | Forum teme, komentari, kategorije, glasanje |
| `ads` | Oglasi za prakse i edukacije |
| `applications` | Prijave studenata na oglase |
| `companies` | Registracija i upravljanje profilima kompanija |
| `notifications` | Sistem notifikacija za korisnike i kompanije |
| `activity` | Historija nedavnih aktivnosti korisnika |
| `admin` | Pregled i upravljanje korisnicima od strane administratora |

Detaljan pregled svih dostupnih ruta i njihovih parametara dostupan je putem Swagger dokumentacije.

## Upload fajlova

Aplikacija lokalno čuva uploadovane fajlove (profilne slike, materijale, CV-jeve) u `uploads/` folderu, koji se automatski kreira pri pokretanju aplikacije ako ne postoji.


## Seed podaci

Ako želiš da napuniš bazu sa demo podacima, pokreni:

```bash
python -m app.seed
```

To će ubaciti 10 kompanija i 10 praksi za lokalno testiranje.


## Napomena o bazi podataka

Razvojno okruženje koristi SQLite (`studenthub.db`), koja se automatski generše pri prvom pokretanju aplikacije. Fajl baze se ne commituje u git repozitorij.

## Tim 4 funkcionalnosti

### Upravljanje korisničkim profilom — router `profiles.py`

Svi endpointi u ovom modulu zahtijevaju da korisnik bude autentifikovan. U zaglavlju (Headers) svakog zahtjeva potrebno je proslijediti JWT token: Authorization: Bearer <vaš_token>

| Metoda | Putanja | Funkcija | Opis | Responses |
|---|---|---|---|---|
| GET | `/profiles/me` | `get_my_profile` | Vraća sve podatke trenutno prijavljenog korisnika potrebne za prikaz profila (ime, email, biografija, godina studija, URL profilne slike, datum registracije) | 200 OK, 401 Unauthorized, 403 Forbidden, 422 Unprocessable Entity, 500 Internal Server Error |
| PATCH | `/profiles/me` | `update_profile_me` | Ažurira tekstualne podatke profila (ime, prezime, biografija, godina studija). Koristi `exclude_unset=True` kako bi se mijenjala samo polja koja su zaista poslana u zahtjevu | 200 OK, 422 Unprocessable Entity, 401 Unauthorized, 403 Forbidden, 500 Internal Server Error |
| PATCH | `/profiles/me/password` | `change_password` | Mijenja lozinku korisnika. Prije izmjene provjerava se ispravnost trenutne lozinke pomoću `pwd_context.verify()`, te da nova lozinka nije identična staroj |  200 OK, 400 Bad Request, 422 Unprocessable Entity, 500 Internal Server Error |
| POST | `/profiles/me/avatar` | `upload_avatar` | Prima fajl slike (`UploadFile`), validira format (JPEG/PNG) i veličinu (maksimalno 5 MB), sprema fajl lokalno na server u `uploads/` folder pod jedinstvenim imenom (UUID), te u bazi ažurira putanju do slike | 200 OK, 400 Bad Request, 422 Unprocessable Entity, 401 Unauthorized, 500 Internal Server Error |
| DELETE | `/profiles/me/avatar` | `delete_avatar` | Briše fajl profilne slike sa servera i postavlja vrijednost u bazi na `None` | 200 OK, 400 Bad Request, 401 Unauthorized, 500 Internal Server Error |

### Deaktivacija korisničkog profila od strane korisnika — router `account.py`

| Metoda | Putanja | Funkcija | Opis | Responses |
|---|---|---|---|---|
| POST | `/account/deactivate` | `deactivate_account` | Vrši deaktivaciju profila uz prethodnu provjeru lozinke | 200 OK, 400 Bad Request, 401 Unauthorized, 500 Internal Server Error |

### Upravljanje korisnicima od strane administratora — router `admin.py`

Sve rute u ovom modulu su zaštićene funkcijom `require_admin`. Za pristup je neophodno proslijediti važeći JWT token u zaglavlju (Authorization: Bearer <token>) korisnika koji ima ulogu admin.

| Metoda | Putanja | Funkcija | Opis | Responses |
|---|---|---|---|---|
| GET | `/admin/users` (opcioni query parametri) | `get_all_users` | Vraća listu svih registrovanih korisnika u sistemu uz mogućnost napredne pretrage i filtriranja | 200 OK, 401 Unauthorized, 403 Forbidden, 422 Unprocessable Entity, 500 Internal Server Error |
| PATCH | `/admin/users/{user_id}/role` | `change_user_role` | Omogućava administratoru da promijeni ulogu drugom korisniku | 200 OK, 400 Bad Request, 422 Unprocessable Entity, 401 Unauthorized, 403 Forbidden, 404 Not Found |
| POST | `/admin/users/{id}/deactivate` | `deactivate_user` | Omogućava administratoru da deaktivira korisnički račun (soft-delete) | 200 OK, 400 Bad Request, 422 Unprocessable Entity, 401 Unauthorized, 403 Forbidden, 404 Not Found |
| POST | `/admin/users/{id}/activate` | `activate_user` | Omogućava administratoru da ponovo aktivira prethodno deaktiviran profil | 200 OK, 400 Bad Request, 422 Unprocessable Entity, 401 Unauthorized, 403 Forbidden, 404 Not Found |
| DELETE | `/admin/users/{user_id}` | `delete_user` | Omogućava administratoru da potpuno i nepovratno uklanja korisnika (hard delete) iz baze podataka uz ugrađenu rollback zaštitu u slučaju greške na serveru | 200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error |
| GET | `/admin/stats` (opcioni query parametri) | `get_platform_statistics` | Generiše ključne ststističke podatke o bazi korisnika. Broj novih registracija se računa dinamički na osnovu proslijeđenog vremenskog perioda. | 200 OK, 401 Unauthorized, 403 Forbidden, 422 Unprocessable Entity, 500 Internal Server Error |
