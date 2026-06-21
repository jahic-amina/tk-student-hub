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

### Enum - `ActivityType`

Definiše dozvoljene tipove aktivnosti koje se mogu logovati.

| Vrijednost | Opis |
|---|---|
| `material_posted` | Materijal je objavljen |
| `forum_comment` | Korisnik je komentarisao na forumu |
| `internship_accepted` | Prihvaćena stažiranja |
| `material_uploaded` | Materijal je uploadovan |
| `forum_answer` | Odgovor na forumu |

---

### SQLModel - `ActivityLog` (tabela: `activity_logs`)

Glavna tabela za čuvanje logova aktivnosti korisnika.

| Polje | Tip | Opis |
|---|---|---|
| `id` | `int` | Primarni ključ, auto-increment |
| `user_id` | `int (FK)` | ID korisnika (foreign key → users.id) |
| `activity_type` | `ActivityType` | Tip aktivnosti (enum) |
| `title` | `str` | Naslov aktivnosti |
| `subtitle` | `str \| None` | Podnaslov (opcionalno) |
| `entity_id` | `int \| None` | ID povezanog entiteta (opcionalno) |
| `created_at` | `datetime` | Datum kreiranja (UTC, auto) |

---

### Response Modeli

#### `ActivityResponse`

Pydantic model koji se vraća za pojedinačni log aktivnosti.

| Polje | Tip | Opis |
|---|---|---|
| `id` | `int` | ID aktivnosti |
| `activity_type` | `ActivityType` | Tip aktivnosti |
| `title` | `str` | Naslov |
| `subtitle` | `str \| None` | Podnaslov (opcionalno) |
| `entity_id` | `int \| None` | ID entiteta (opcionalno) |
| `created_at` | `datetime` | Datum kreiranja |

#### `ActivityListResponse`


| Polje | Tip | Opis |
|---|---|---|
| `items` | `list[ActivityResponse]` | Lista aktivnosti |
| `total` | `int` | Ukupan broj zapisa |
| `has_more` | `bool` | Da li ima još zapisa za učitati |

---

 ### API Rute 

**Base URL:** `/api/users/me`  
**Tag:** `activity`

| Metoda | Putanja | Opis | Pristup |
|---|---|---|---|
| `GET` | `/api/users/me/activity` | Lista aktivnosti trenutnog korisnika (paginirana) | Korisnik |

---

#### `GET /api/users/me/activity`

Vraća paginiranu listu aktivnosti trenutno prijavljenog korisnika, sortirano od najnovijeg.

**Query parametri:**

| Parametar | Tip | Default | Opis |
|---|---|---|---|
| `limit` | `int` | `3` | Broj rezultata po stranici (max: 20) |
| `offset` | `int` | `0` | Pomak od početka liste |

- **Autentifikacija:** JWT token (prijavljeni korisnik)
- **Response:** `ActivityListResponse`

---

### Servis - `log_activity`

Pomoćna funkcija koja se poziva iz ostalih servisa/rutera kako bi se zabilježila aktivnost korisnika. Interno hvata greške i radi rollback kako ne bi blokirala glavni tok aplikacije.

| Parametar | Tip | Opis |
|---|---|---|
| `db` | `Session` | SQLAlchemy sesija |
| `user_id` | `int` | ID korisnika čija se aktivnost loguje |
| `activity_type` | `ActivityType` | Tip aktivnosti (enum) |
| `title` | `str` | Naslov aktivnosti |
| `subtitle` | `str` | Podnaslov (opcionalno) |
| `entity_id` | `int` | ID entiteta (opcionalno) |

---

## Notifikacije

Modul za upravljanje notifikacijama korisnika. Notifikacije se kreiraju automatski od strane sistema i šalju korisnicima na osnovu različitih događaja na platformi.

---

### SQLAlchemy Model — `Notification` (tabela: `notifications`)

| Polje | Tip | Opis |
|---|---|---|
| `id` | `int` | Primarni ključ, auto-increment |
| `user_id` | `int (FK)` | ID korisnika (foreign key → users.id, CASCADE) |
| `type` | `NotificationTypes` | Tip notifikacije (enum) |
| `message` | `str (255)` | Tekst notifikacije |
| `link` | `str \| None` | Opcioni link na koji notifikacija upućuje |
| `reference_id` | `int \| None` | ID referenciranog entiteta (opcionalno) |
| `is_read` | `bool` | Da li je notifikacija pročitana (default: `false`) |
| `created_at` | `datetime` | Datum kreiranja (UTC, auto) |

> **Indeks:** `ix_notifications_user_unread` — kompozitni indeks na `(user_id, is_read)` za brzo dohvatanje nepročitanih notifikacija.

---

### Pydantic Modeli

#### `NotificationOut`

Response model koji se šalje klijentu.

| Polje | Tip | Opis |
|---|---|---|
| `id` | `int` | ID notifikacije |
| `type` | `NotificationType` | Tip notifikacije |
| `message` | `str` | Tekst notifikacije |
| `link` | `str \| None` | Opcioni link |
| `is_read` | `bool` | Status čitanja |
| `created_at` | `datetime` | Datum kreiranja |

#### `NotificationCreate`

Model za kreiranje nove notifikacije (interno, server-side).

| Polje | Tip | Opis |
|---|---|---|
| `user_id` | `int` | ID korisnika primatelja |
| `type` | `NotificationType` | Tip notifikacije |
| `message` | `str` | Tekst notifikacije |
| `link` | `str \| None` | Opcioni link (opcionalno) |
| `reference_id` | `int \| None` | ID entiteta (opcionalno) |

#### `UnreadCountOut` / `MarkAllReadOut`

| Model | Polje | Tip | Opis |
|---|---|---|---|
| `UnreadCountOut` | `count` | `int` | Broj nepročitanih notifikacija |
| `MarkAllReadOut` | `updated` | `int` | Broj ažuriranih (označenih kao pročitanih) |

---


## Profil Korisnika

Modul za upravljanje korisničkim profilom. Omogućava pregled i ažuriranje profila, upload i brisanje profilne slike, uređivanje profila, promjenu lozinke i deaktivaciju.

---

### SQLModel Modeli

#### `UserProfileResponse`

Response model za prikaz podataka korisničkog profila.

| Polje | Tip | Opis |
|---|---|---|
| `id` | `int` | ID korisnika |
| `email` | `str` | Email adresa |
| `full_name` | `str` | Puno ime |
| `role` | `str` | Uloga korisnika |
| `created_at` | `datetime \| None` | Datum registracije |
| `profilna_slika_url` | `str \| None` | URL profilne slike |
| `biografija` | `str \| None` | Biografija korisnika (opcionalno) |

#### `AvatarUploadResponse` / `AvatarDeleteResponse`

| Model | Polje | Tip | Opis |
|---|---|---|---|
| `AvatarUploadResponse` | `profilna_slika_url` | `str` | URL novopostavljene slike |
| `AvatarDeleteResponse` | `message` | `str` | Poruka potvrde brisanja |

#### `PublicProfileResponse`

Javni profil koji je vidljiv svim prijavljenim korisnicima.

| Polje | Tip | Opis |
|---|---|---|
| `id` | `int` | ID korisnika |
| `full_name` | `str` | Puno ime |
| `biografija` | `str \| None` | Biografija (opcionalno) |
| `godina_studija` | `str \| None` | Godina studija (opcionalno) |
| `profilna_slika_url` | `str \| None` | URL profilne slike |

--- 

### API Rute

#### Upravljanje korisničkim profilom — router `profiles.py`

Svi endpointi u ovom modulu zahtijevaju da korisnik bude autentifikovan. U zaglavlju (Headers) svakog zahtjeva potrebno je proslijediti JWT token: Authorization: Bearer <vaš_token>

| Metoda | Putanja | Funkcija | Opis | Responses |
|---|---|---|---|---|
| `GET` | `/profiles/me` | `get_my_profile` | Vraća sve podatke trenutno prijavljenog korisnika potrebne za prikaz profila (ime, email, biografija, godina studija, URL profilne slike, datum registracije) | 200 OK, 401 Unauthorized, 403 Forbidden, 422 Unprocessable Entity, 500 Internal Server Error |
| `PATCH` | `/profiles/me` | `update_profile_me` | Ažurira tekstualne podatke profila (ime, prezime, biografija, godina studija). Koristi `exclude_unset=True` kako bi se mijenjala samo polja koja su zaista poslana u zahtjevu | 200 OK, 422 Unprocessable Entity, 401 Unauthorized, 403 Forbidden, 500 Internal Server Error |
| `PATCH` | `/profiles/me/password` | `change_password` | Mijenja lozinku korisnika. Prije izmjene provjerava se ispravnost trenutne lozinke pomoću `pwd_context.verify()`, te da nova lozinka nije identična staroj |  200 OK, 400 Bad Request, 422 Unprocessable Entity, 500 Internal Server Error |
| `POST` | `/profiles/me/avatar` | `upload_avatar` | Prima fajl slike (`UploadFile`), validira format (JPEG/PNG) i veličinu (maksimalno 5 MB), sprema fajl lokalno na server u `uploads/` folder pod jedinstvenim imenom (UUID), te u bazi ažurira putanju do slike | 200 OK, 400 Bad Request, 422 Unprocessable Entity, 401 Unauthorized, 500 Internal Server Error |
| `DELETE` | `/profiles/me/avatar` | `delete_avatar` | Briše fajl profilne slike sa servera i postavlja vrijednost u bazi na `None` | 200 OK, 400 Bad Request, 401 Unauthorized, 500 Internal Server Error |
| `GET` | `/profiles/public` | `public_profile` |Vraća listu svih aktivnih korisnika (`is_active = true`) kao javne profile. | 200 OK |
| `GET` | `/profiles/{user_id}/public` | Vraća javni profil jednog korisnika po ID-u. Korisnik mora biti aktivan. | 200 OK, 404 Not Found |

#### Deaktivacija korisničkog profila od strane korisnika — router `account.py`

| Metoda | Putanja | Funkcija | Opis | Responses |
|---|---|---|---|---|
| POST | `/account/deactivate` | `deactivate_account` | Vrši deaktivaciju profila uz prethodnu provjeru lozinke | 200 OK, 400 Bad Request, 401 Unauthorized, 500 Internal Server Error |

---

## Admin

Modul za administraciju korisnika. Dostupan isključivo adminima.

---

### Pydantic Modeli

#### `UserAdminResponse`

Response model za prikaz korisnika u admin panelu.

| Polje | Tip | Opis |
|---|---|---|
| `id` | `int` | ID korisnika |
| `full_name` | `str` | Puno ime |
| `email` | `str` | Email adresa |
| `role` | `UserRole` | Uloga korisnika (enum) |
| `is_active` | `bool` | Status aktivnosti korisnika |

#### `UsersListResponse`

Model za listu korisnika s metapodacima.

| Polje | Tip | Opis |
|---|---|---|
| `users` | `list[UserAdminResponse]` | Lista korisnika |
| `total` | `int` | Ukupan broj korisnika u listi |
| `prikazano` | `int` | Broj prikazanih korisnika |

---


### API Rute

Sve rute u ovom modulu su zaštićene funkcijom `require_admin`. Za pristup je neophodno proslijediti važeći JWT token u zaglavlju (Authorization: Bearer <token>) korisnika koji ima ulogu admin.

| Metoda | Putanja | Funkcija | Opis | Responses |
|---|---|---|---|---|
| GET | `/admin/users` (opcioni query parametri) | `get_all_users` | Vraća listu svih registrovanih korisnika u sistemu uz mogućnost napredne pretrage i filtriranja | 200 OK, 401 Unauthorized, 403 Forbidden, 422 Unprocessable Entity, 500 Internal Server Error |
| PATCH | `/admin/users/{user_id}/role` | `change_user_role` | Omogućava administratoru da promijeni ulogu drugom korisniku | 200 OK, 400 Bad Request, 422 Unprocessable Entity, 401 Unauthorized, 403 Forbidden, 404 Not Found |
| POST | `/admin/users/{id}/deactivate` | `deactivate_user` | Omogućava administratoru da deaktivira korisnički račun (soft-delete) | 200 OK, 400 Bad Request, 422 Unprocessable Entity, 401 Unauthorized, 403 Forbidden, 404 Not Found |
| POST | `/admin/users/{id}/activate` | `activate_user` | Omogućava administratoru da ponovo aktivira prethodno deaktiviran profil | 200 OK, 400 Bad Request, 422 Unprocessable Entity, 401 Unauthorized, 403 Forbidden, 404 Not Found |
| DELETE | `/admin/users/{user_id}` | `delete_user` | Omogućava administratoru da potpuno i nepovratno uklanja korisnika (hard delete) iz baze podataka uz ugrađenu rollback zaštitu u slučaju greške na serveru | 200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error |
| GET | `/admin/stats` (opcioni query parametri) | `get_platform_statistics` | Generiše ključne stastističke podatke o bazi korisnika. Broj novih registracija se računa dinamički na osnovu proslijeđenog vremenskog perioda. | 200 OK, 401 Unauthorized, 403 Forbidden, 422 Unprocessable Entity, 500 Internal Server Error |

