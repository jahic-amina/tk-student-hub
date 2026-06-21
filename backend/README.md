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

| Uloga         | Opis                                                                |
| ------------- | ------------------------------------------------------------------- |
| Posjetilac    | Neregistrovani korisnik koji pregledava javni sadržaj               |
| Student       | Registrovani korisnik s punim pristupom funkcionalnostima platforme |
| Administrator | Upravlja korisnicima i sadržajem platforme                          |

## Glavni moduli (routeri)

| Modul           | Opis                                                                 |
| --------------- | -------------------------------------------------------------------- |
| `auth`          | Registracija i prijava korisnika i kompanija                         |
| `profiles`      | Pregled i uređivanje korisničkog profila, upload profilne slike      |
| `materials`     | Upload, pregled, ocjenjivanje i komentarisanje studijskih materijala |
| `forum`         | Forum teme, komentari, kategorije, glasanje                          |
| `ads`           | Oglasi za prakse i edukacije                                         |
| `applications`  | Prijave studenata na oglase                                          |
| `companies`     | Registracija i upravljanje profilima kompanija                       |
| `notifications` | Sistem notifikacija za korisnike i kompanije                         |
| `activity`      | Historija nedavnih aktivnosti korisnika                              |

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

## Modeli podataka

### Company (Kompanija)

#### Tabela: `companies`

---

#### SQLModel — `Company` (tabela)

| Polje             | Tip             | Opis                                  |
| ----------------- | --------------- | ------------------------------------- |
| `id`              | `int`           | Primarni ključ, auto-increment        |
| `company_name`    | `str`           | Naziv kompanije (indeksiran)          |
| `description`     | `str`           | Opis kompanije                        |
| `website_url`     | `str`           | Web stranica kompanije                |
| `logo_path`       | `str \| None`   | Putanja do logoa (opcionalno)         |
| `email`           | `str`           | Email adresa (indeksiran)             |
| `phone_number`    | `str`           | Broj telefona (indeksiran)            |
| `tin`             | `str`           | PDV/ID broj — 13 cifara (indeksiran)  |
| `hashed_password` | `str`           | Hashirana lozinka                     |
| `status`          | `CompanyStatus` | Status kompanije (default: `pending`) |
| `created_at`      | `datetime`      | Datum registracije (UTC, auto)        |
| `is_deleted`      | `bool`          | Soft delete flag (default: `false`)   |
| `address`         | `str`           | Adresa sjedišta                       |

---

#### Enum — `CompanyStatus`

| Vrijednost | Opis                                  |
| ---------- | ------------------------------------- |
| `pending`  | Registracija čeka odobrenje (default) |
| `approved` | Kompanija odobrena od administratora  |
| `denied`   | Registracija odbijena                 |

---

#### Pydantic shema — `CompanyCreate`

Koristi se pri **registraciji** kompanije (`POST /companies/register`).

| Polje          | Tip   | Validacija                    |
| -------------- | ----- | ----------------------------- |
| `company_name` | `str` | Minimum 2 karaktera           |
| `description`  | `str` | Minimum 10 karaktera          |
| `website_url`  | `str` | Format: `https://domena.tld`  |
| `email`        | `str` | Validan email format          |
| `phone_number` | `str` | Bez dodatne validacije        |
| `tin`          | `str` | Tačno 13 cifara, samo brojevi |
| `address`      | `str` | Više od 2 karaktera           |
| `password`     | `str` | Minimum 8 karaktera           |

---

#### Pydantic shema — `CompanyUpdate`

Koristi se pri **ažuriranju** profila kompanije (`PATCH /companies/{id}`). Sva polja su opcionalna — šalju se samo ona koja se mijenjaju.

| Polje          | Tip                     | Validacija                    |
| -------------- | ----------------------- | ----------------------------- |
| `company_name` | `str \| None`           | Minimum 2 karaktera           |
| `description`  | `str \| None`           | Minimum 10 karaktera          |
| `website_url`  | `str \| None`           | Format: `https://domena.tld`  |
| `email`        | `str \| None`           | Validan email format          |
| `phone_number` | `str \| None`           | —                             |
| `tin`          | `str \| None`           | Tačno 13 cifara, samo brojevi |
| `address`      | `str \| None`           | Više od 2 karaktera           |
| `status`       | `CompanyStatus \| None` | Enum vrijednost               |

---

#### Pydantic shema — `CompanyRead`

Vraća se kao response na API pozive. **Ne uključuje `hashed_password`.**

| Polje          | Tip             |
| -------------- | --------------- |
| `id`           | `int`           |
| `company_name` | `str`           |
| `description`  | `str`           |
| `website_url`  | `str`           |
| `logo_path`    | `str \| None`   |
| `email`        | `str`           |
| `phone_number` | `str`           |
| `tin`          | `str`           |
| `status`       | `CompanyStatus` |
| `created_at`   | `datetime`      |
| `is_deleted`   | `bool`          |
| `address`      | `str`           |

---

#### Napomene

- Brisanje kompanija je **soft delete** — polje `is_deleted` se postavlja na `true`, zapis ostaje u bazi
- `hashed_password` se nikad ne vraća kroz API response (`CompanyRead` ga ne sadrži)
- `created_at` se automatski postavlja na trenutni UTC timestamp pri kreiranju
- `logo_path` čuva relativnu putanju do fajla u `uploads/` folderu

---

### Ad (Oglas)

#### Tabela: `ads`

---

#### SQLModel — `Ad` (tabela)

| Polje                  | Tip                | Opis                                              |
| ---------------------- | ------------------ | ------------------------------------------------- |
| `id`                   | `int`              | Primarni ključ, auto-increment                    |
| `company_id`           | `int`              | FK → `companies.id`                               |
| `approved_by`          | `int \| None`      | FK → `users.id` (admin koji je odobrio)           |
| `title`                | `str`              | Naziv oglasa (max 100 karaktera)                  |
| `type`                 | `AdType`           | Tip oglasa (praksa / edukacija / stipendija)      |
| `field`                | `str`              | Oblast / smjer (max 100 karaktera)                |
| `location`             | `str`              | Lokacija (max 100 karaktera)                      |
| `description`          | `str`              | Opis oglasa                                       |
| `deadline`             | `date`             | Rok prijave (mora biti u budućnosti)              |
| `duration_months`      | `int \| None`      | Trajanje u mjesecima (opcionalno)                 |
| `compensation`         | `float \| None`    | Iznos naknade (opcionalno)                        |
| `currency`             | `str \| None`      | Valuta naknade (default: `BAM`, max 10 karaktera) |
| `spots`                | `int`              | Broj mjesta (default: `1`)                        |
| `requirements`         | `str \| None`      | Uslovi prijave (opcionalno)                       |
| `benefits`             | `str \| None`      | Benefiti (opcionalno)                             |
| `admin_comment`        | `str \| None`      | Komentar administratora (opcionalno)              |
| `changes_requested_at` | `datetime \| None` | Kada su zatražene izmjene (opcionalno)            |
| `status`               | `AdStatus`         | Status oglasa (default: `pending`)                |
| `is_deleted`           | `bool`             | Soft delete flag (default: `false`)               |
| `created_at`           | `datetime`         | Datum kreiranja (UTC, auto)                       |
| `updated_at`           | `datetime \| None` | Datum posljednje izmjene                          |

##### Relacije

| Relacija   | Model     | Opis                                |
| ---------- | --------- | ----------------------------------- |
| `company`  | `Company` | Kompanija koja je objavila oglas    |
| `approver` | `User`    | Administrator koji je odobrio oglas |

---

#### Enum — `AdStatus`

| Vrijednost          | Opis                                        |
| ------------------- | ------------------------------------------- |
| `pending`           | Oglas čeka odobrenje (default)              |
| `active`            | Oglas odobren i vidljiv studentima          |
| `expired`           | Rok prijave je istekao                      |
| `rejected`          | Oglas odbijen od administratora             |
| `changes_requested` | Administrator zatražio izmjene od kompanije |

---

#### Enum — `AdType`

| Vrijednost    | Opis       |
| ------------- | ---------- |
| `internship`  | Praksa     |
| `education`   | Edukacija  |
| `scholarship` | Stipendija |

---

#### Pydantic shema — `AdCreate`

Koristi se pri **kreiranju** oglasa (`POST /ads`).

| Polje             | Tip             | Validacija                                                 |
| ----------------- | --------------- | ---------------------------------------------------------- |
| `title`           | `str`           | Strip whitespace, ne smije biti prazno                     |
| `type`            | `AdType`        | Enum vrijednost                                            |
| `field`           | `str`           | Strip whitespace, ne smije biti prazno                     |
| `location`        | `str`           | Strip whitespace, ne smije biti prazno                     |
| `description`     | `str`           | Strip whitespace, ne smije biti prazno                     |
| `deadline`        | `date`          | Mora biti datum u budućnosti                               |
| `duration_months` | `int \| None`   | Minimum 1                                                  |
| `compensation`    | `float \| None` | Ne smije biti negativno                                    |
| `currency`        | `str \| None`   | Obavezno ako je `compensation` postavljen (default: `BAM`) |
| `spots`           | `int`           | Minimum 1 (default: `1`)                                   |
| `requirements`    | `str \| None`   | —                                                          |
| `benefits`        | `str \| None`   | —                                                          |

---

#### Pydantic shema — `AdUpdate`

Koristi se pri **potpunom ažuriranju** oglasa (`PUT /ads/{id}`). Sva polja su obavezna — ista validacija kao `AdCreate`.

| Polje             | Tip             | Validacija                                                 |
| ----------------- | --------------- | ---------------------------------------------------------- |
| `title`           | `str`           | Strip whitespace, ne smije biti prazno                     |
| `type`            | `AdType`        | Enum vrijednost                                            |
| `field`           | `str`           | Strip whitespace, ne smije biti prazno                     |
| `location`        | `str`           | Strip whitespace, ne smije biti prazno                     |
| `description`     | `str`           | Strip whitespace, ne smije biti prazno                     |
| `deadline`        | `date`          | Mora biti datum u budućnosti                               |
| `duration_months` | `int \| None`   | Minimum 1                                                  |
| `compensation`    | `float \| None` | Ne smije biti negativno                                    |
| `currency`        | `str \| None`   | Obavezno ako je `compensation` postavljen (default: `BAM`) |
| `spots`           | `int`           | Minimum 1 (default: `1`)                                   |
| `requirements`    | `str \| None`   | —                                                          |
| `benefits`        | `str \| None`   | —                                                          |

---

#### Pydantic shema — `AdPatch`

Koristi se pri **parcijalnom ažuriranju** oglasa (`PATCH /ads/{id}`). Sva polja su opcionalna.

| Polje             | Tip                | Validacija                             |
| ----------------- | ------------------ | -------------------------------------- |
| `title`           | `str \| None`      | Strip whitespace, ne smije biti prazno |
| `type`            | `AdType \| None`   | Enum vrijednost                        |
| `field`           | `str \| None`      | Strip whitespace, ne smije biti prazno |
| `location`        | `str \| None`      | Strip whitespace, ne smije biti prazno |
| `description`     | `str \| None`      | Strip whitespace, ne smije biti prazno |
| `deadline`        | `date \| None`     | Mora biti datum u budućnosti           |
| `duration_months` | `int \| None`      | Minimum 1                              |
| `compensation`    | `float \| None`    | Ne smije biti negativno                |
| `currency`        | `str \| None`      | —                                      |
| `spots`           | `int \| None`      | Minimum 1                              |
| `requirements`    | `str \| None`      | —                                      |
| `benefits`        | `str \| None`      | —                                      |
| `status`          | `AdStatus \| None` | Enum vrijednost                        |
| `admin_comment`   | `str \| None`      | —                                      |

---

#### Pydantic shema — `StatusUpdate`

Koristi se pri **promjeni statusa** oglasa od strane administratora (`PATCH /ads/{id}/status`).

| Polje           | Tip           | Opis                          |
| --------------- | ------------- | ----------------------------- |
| `status`        | `AdStatus`    | Novi status oglasa            |
| `admin_comment` | `str \| None` | Komentar uz promjenu statusa  |
| `approved_by`   | `int \| None` | ID admina koji mijenja status |

---

#### Pydantic shema — `AdRead`

Vraća se kao response na API pozive.

| Polje                  | Tip                | Opis                                       |
| ---------------------- | ------------------ | ------------------------------------------ |
| `id`                   | `int`              | —                                          |
| `company_id`           | `int`              | —                                          |
| `company_name`         | `str \| None`      | Naziv kompanije (iz relacije)              |
| `approved_by`          | `int \| None`      | —                                          |
| `approver_name`        | `str \| None`      | Ime admina koji je odobrio (iz relacije)   |
| `title`                | `str`              | —                                          |
| `type`                 | `AdType`           | —                                          |
| `field`                | `str`              | —                                          |
| `location`             | `str`              | —                                          |
| `description`          | `str`              | —                                          |
| `deadline`             | `date`             | —                                          |
| `duration_months`      | `int \| None`      | —                                          |
| `compensation`         | `float \| None`    | —                                          |
| `currency`             | `str \| None`      | —                                          |
| `spots`                | `int`              | —                                          |
| `requirements`         | `str \| None`      | —                                          |
| `benefits`             | `str \| None`      | —                                          |
| `admin_comment`        | `str \| None`      | —                                          |
| `changes_requested_at` | `datetime \| None` | —                                          |
| `status`               | `AdStatus`         | —                                          |
| `is_deleted`           | `bool`             | —                                          |
| `created_at`           | `datetime`         | —                                          |
| `updated_at`           | `datetime \| None` | —                                          |
| `applicants_count`     | `int`              | Broj prijavljenih studenata (default: `0`) |

---

#### Napomene

- Brisanje oglasa je **soft delete** — polje `is_deleted` se postavlja na `true`, zapis ostaje u bazi
- `deadline` mora uvijek biti datum u budućnosti pri kreiranju i ažuriranju
- `currency` je obavezno polje ako je `compensation` postavljen — validira se kroz `model_validator`
- `updated_at` se ne postavlja automatski — potrebno ga je ručno setovati u servisu pri svakom ažuriranju
- `applicants_count` nije kolona u bazi — računa se dinamički pri dohvatanju oglasa

---

### AdBookmark (Sačuvani oglas)

#### Tabela: `ad_bookmarks`

---

#### SQLModel — `AdBookmark` (tabela)

| Polje        | Tip        | Opis                           |
| ------------ | ---------- | ------------------------------ |
| `id`         | `int`      | Primarni ključ, auto-increment |
| `user_id`    | `int`      | FK → `users.id` (indeksiran)   |
| `ad_id`      | `int`      | FK → `ads.id` (indeksiran)     |
| `created_at` | `datetime` | Datum bookmarkanja (UTC, auto) |

##### Ograničenja

| Naziv                     | Polja              | Opis                                                      |
| ------------------------- | ------------------ | --------------------------------------------------------- |
| `unique_user_ad_bookmark` | `user_id`, `ad_id` | Jedan korisnik ne može bookmarkovati isti oglas više puta |

---

#### Pydantic shema — `AdBookmarkCreate`

Koristi se pri **dodavanju** oglasa u sačuvane (`POST /ads/bookmarks`).

| Polje   | Tip   | Opis                          |
| ------- | ----- | ----------------------------- |
| `ad_id` | `int` | ID oglasa koji se bookmarkuje |

---

#### Pydantic shema — `AdBookmarkRead`

Vraća se kao response na API pozive.

| Polje        | Tip        | Opis |
| ------------ | ---------- | ---- |
| `id`         | `int`      | —    |
| `user_id`    | `int`      | —    |
| `ad_id`      | `int`      | —    |
| `created_at` | `datetime` | —    |

---

#### Napomene

- Kombinacija `user_id` + `ad_id` je **unique** — dupli bookmark nije moguć, baza vraća grešku
- `user_id` se ne šalje kroz request body — uzima se iz JWT tokena trenutno prijavljenog korisnika
- `created_at` se automatski postavlja na trenutni UTC timestamp pri kreiranju

---

### Notification (Notifikacija)

#### Tabela: `notifications`

---

#### SQLModel — `Notification` (tabela)

| Polje        | Tip                | Opis                                               |
| ------------ | ------------------ | -------------------------------------------------- |
| `id`         | `int`              | Primarni ključ, auto-increment                     |
| `user_id`    | `int \| None`      | FK → `users.id` (indeksiran, opcionalno)           |
| `company_id` | `int \| None`      | FK → `companies.id` (indeksiran, opcionalno)       |
| `text`       | `str`              | Tekst notifikacije                                 |
| `type`       | `NotificationType` | Tip notifikacije                                   |
| `is_read`    | `bool`             | Da li je notifikacija pročitana (default: `false`) |
| `created_at` | `datetime`         | Datum kreiranja (UTC, auto)                        |

---

#### Enum — `NotificationType`

| Vrijednost                  | Opis                                |
| --------------------------- | ----------------------------------- |
| `new_opportunity`           | Nova praksa / oglas dostupan        |
| `status_change`             | Promjena statusa oglasa ili prijave |
| `deadline_expiring`         | Rok prijave uskoro ističe           |
| `comment_liked`             | Neko je lajkovao komentar korisnika |
| `material_graded`           | Materijal je ocijenjen              |
| `material_pending_approval` | Materijal čeka odobrenje (admin)    |

---

#### Pydantic shema — `NotificationCreate`

Koristi se pri **kreiranju** notifikacije (interno, kroz servis).

| Polje        | Tip                | Validacija                             |
| ------------ | ------------------ | -------------------------------------- |
| `user_id`    | `int \| None`      | —                                      |
| `company_id` | `int \| None`      | —                                      |
| `text`       | `str`              | Strip whitespace, ne smije biti prazno |
| `type`       | `NotificationType` | Enum vrijednost                        |
| `is_read`    | `bool`             | Default: `false`                       |

---

#### Pydantic shema — `NotificationUpdate`

Koristi se pri **ažuriranju** notifikacije (`PATCH /notifications/{id}`). Sva polja su opcionalna.

| Polje     | Tip                        | Validacija                             |
| --------- | -------------------------- | -------------------------------------- |
| `text`    | `str \| None`              | Strip whitespace, ne smije biti prazno |
| `type`    | `NotificationType \| None` | Enum vrijednost                        |
| `is_read` | `bool \| None`             | —                                      |

---

#### Napomene

- Notifikacija može biti upućena **korisniku** (`user_id`) ili **kompaniji** (`company_id`) — jedno od dva polja treba biti postavljeno
- `is_read` se postavlja na `true` kada korisnik / kompanija pročita notifikaciju
- `created_at` se automatski postavlja na trenutni UTC timestamp pri kreiranju
- Notifikacije se kreiraju interno kroz servis — nisu direktno dostupne kroz javni
