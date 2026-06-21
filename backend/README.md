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

### Application (Prijava)

#### Tabela: `applications`

---

#### SQLModel — `Application` (tabela)

| Polje                      | Tip                 | Opis                                     |
| -------------------------- | ------------------- | ---------------------------------------- |
| `id`                       | `int`               | Primarni ključ, auto-increment           |
| `user_id`                  | `int`               | FK → `users.id` (indeksiran)             |
| `ad_id`                    | `int`               | FK → `ads.id` (indeksiran)               |
| `cv_path`                  | `str`               | Putanja do uploadovanog CV-a             |
| `motivational_letter_path` | `str`               | Putanja do motivacionog pisma            |
| `linkedin_url`             | `str \| None`       | LinkedIn profil (opcionalno)             |
| `phone`                    | `str`               | Broj telefona                            |
| `status`                   | `ApplicationStatus` | Status prijave (default: `pending`)      |
| `admin_feedback`           | `str \| None`       | Povratna informacija admina (opcionalno) |
| `is_archived`              | `bool`              | Arhivirana prijava (default: `false`)    |
| `created_at`               | `datetime`          | Datum kreiranja (UTC, auto)              |
| `updated_at`               | `datetime`          | Datum posljednje izmjene (UTC, auto)     |

##### Relacije

| Relacija | Model  | Opis                        |
| -------- | ------ | --------------------------- |
| `user`   | `User` | Student koji je aplicirao   |
| `ad`     | `Ad`   | Oglas na koji je aplicirano |

##### Ograničenja

| Naziv        | Polja              | Opis                                               |
| ------------ | ------------------ | -------------------------------------------------- |
| `uq_user_ad` | `user_id`, `ad_id` | Student ne može aplicirati na isti oglas više puta |

---

#### Enum — `ApplicationStatus`

| Vrijednost | Opis                            |
| ---------- | ------------------------------- |
| `pending`  | Prijava čeka pregled (default)  |
| `accepted` | Prijava prihvaćena od kompanije |
| `rejected` | Prijava odbijena od kompanije   |

---

#### Pydantic shema — `ApplicationCreate`

Koristi se pri **kreiranju** prijave (`POST /applications/`).

| Polje                      | Tip           | Validacija                                                      |
| -------------------------- | ------------- | --------------------------------------------------------------- |
| `ad_id`                    | `int`         | —                                                               |
| `cv_path`                  | `str`         | Putanja dobijena nakon `POST /applications/upload-cv`           |
| `motivational_letter_path` | `str`         | Putanja do motivacionog pisma                                   |
| `linkedin_url`             | `str \| None` | Format: `https://linkedin.com/in/username`                      |
| `phone`                    | `str`         | 7–20 karaktera, dozvoljeni: brojevi, `+`, `-`, razmaci, zagrade |

---

#### Pydantic shema — `ApplicationRead`

Vraća se kao response na API pozive.

| Polje                      | Tip                 | Opis |
| -------------------------- | ------------------- | ---- |
| `id`                       | `int`               | —    |
| `user_id`                  | `int`               | —    |
| `ad_id`                    | `int`               | —    |
| `cv_path`                  | `str`               | —    |
| `motivational_letter_path` | `str`               | —    |
| `linkedin_url`             | `str \| None`       | —    |
| `phone`                    | `str`               | —    |
| `status`                   | `ApplicationStatus` | —    |
| `admin_feedback`           | `str \| None`       | —    |
| `is_archived`              | `bool`              | —    |
| `created_at`               | `datetime`          | —    |
| `updated_at`               | `datetime`          | —    |

---

#### Pydantic shema — `ApplicationUpdate`

Koristi se pri **ažuriranju** prijave. Sva polja su opcionalna.

| Polje            | Tip                         | Opis                                     |
| ---------------- | --------------------------- | ---------------------------------------- |
| `status`         | `ApplicationStatus \| None` | Novi status prijave                      |
| `admin_feedback` | `str \| None`               | Povratna informacija uz promjenu statusa |
| `is_archived`    | `bool \| None`              | Arhiviranje prijave                      |

---

#### Napomene

- Kombinacija `user_id` + `ad_id` je **unique** — dupla prijava nije moguća, baza vraća grešku
- `cv_path` i `motivational_letter_path` čuvaju relativne putanje do fajlova u `uploads/` folderu
- `updated_at` se ne postavlja automatski pri izmjeni — potrebno ga je ručno setovati u servisu
- Brisanje prijava je **soft delete** kroz arhiviranje — polje `is_archived` se postavlja na `true`
- `linkedin_url` mora biti u formatu `https://linkedin.com/in/username` ili `https://www.linkedin.com/in/username`

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

---

## API Rute

### Companies (Kompanije)

**Base URL:** `/companies`  
**Tag:** `Companies`

---

| Metoda   | Putanja                               | Opis                                    | Pristup   |
| -------- | ------------------------------------- | --------------------------------------- | --------- |
| `GET`    | `/companies/`                         | Lista svih odobrenih kompanija          | Javno     |
| `GET`    | `/companies/admin`                    | Lista svih kompanija (bez filtera)      | Admin     |
| `GET`    | `/companies/{company_id}`             | Detalji jedne kompanije                 | Javno     |
| `POST`   | `/companies/`                         | Registracija nove kompanije             | Javno     |
| `PUT`    | `/companies/{company_id}`             | Potpuno ažuriranje profila kompanije    | Kompanija |
| `PATCH`  | `/companies/{company_id}`             | Parcijalno ažuriranje profila kompanije | Kompanija |
| `PATCH`  | `/companies/{company_id}/status`      | Promjena statusa kompanije              | Admin     |
| `PATCH`  | `/companies/{company_id}/restore`     | Vraćanje obrisane kompanije             | Admin     |
| `PATCH`  | `/companies/{company_id}/upload-logo` | Upload logoa kompanije                  | Kompanija |
| `DELETE` | `/companies/{company_id}`             | Soft delete kompanije                   | Admin     |

---

#### `GET /companies/`

Vraća listu svih kompanija sa statusom `approved` koje nisu obrisane.

- **Autentifikacija:** nije potrebna
- **Response:** `List[CompanyRead]`

---

#### `GET /companies/admin`

Vraća listu **svih** kompanija bez filtera po statusu ili `is_deleted`.

- **Autentifikacija:** Admin JWT token
- **Response:** `List[CompanyRead]`
- **Greške:**
  - `403` — korisnik nije admin

---

#### `GET /companies/{company_id}`

Vraća detalje jedne kompanije. Kompanija mora biti `approved` i nije obrisana.

- **Autentifikacija:** nije potrebna
- **Response:** `CompanyRead`
- **Greške:**
  - `404` — kompanija nije pronađena, obrisana je ili nije odobrena

---

#### `POST /companies/`

Registracija nove kompanije. Prima `multipart/form-data` zbog upload logoa.  
Nakon registracije, svim adminima se šalje notifikacija.

- **Autentifikacija:** nije potrebna
- **Content-Type:** `multipart/form-data`
- **Body:**

| Polje          | Tip             | Opis                                  |
| -------------- | --------------- | ------------------------------------- |
| `company_name` | `string` (Form) | Naziv kompanije                       |
| `tin`          | `string` (Form) | PDV/ID broj                           |
| `website_url`  | `string` (Form) | Web stranica                          |
| `address`      | `string` (Form) | Adresa sjedišta                       |
| `description`  | `string` (Form) | Opis kompanije                        |
| `email`        | `string` (Form) | Email adresa                          |
| `phone_number` | `string` (Form) | Broj telefona                         |
| `password`     | `string` (Form) | Lozinka                               |
| `logo`         | `file` (File)   | Logo kompanije (PNG, JPG, JPEG, WebP) |

- **Response:** `CompanyRead` — `201 Created`
- **Greške:**
  - `400` — email već postoji
  - `400` — logo nije ispravan format

---

#### `PUT /companies/{company_id}`

Potpuno ažuriranje profila kompanije. Polje `status` se ignoriše.

- **Autentifikacija:** Kompanija JWT token
- **Body:** `CompanyUpdate`
- **Response:** `CompanyRead`
- **Greške:**
  - `403` — kompanija nema dozvolu za ažuriranje tuđeg profila

---

#### `PATCH /companies/{company_id}`

Parcijalno ažuriranje profila — šalju se samo polja koja se mijenjaju. Polje `status` se ignoriše.

- **Autentifikacija:** Kompanija JWT token
- **Body:** `CompanyUpdate` (parcijalno)
- **Response:** `CompanyRead`
- **Greške:**
  - `403` — kompanija nema dozvolu za ažuriranje tuđeg profila

---

#### `PATCH /companies/{company_id}/status`

Promjena statusa kompanije od strane admina.  
Ako se status mijenja u `approved`, kompaniji se šalje notifikacija.

- **Autentifikacija:** Admin JWT token
- **Body:** `CompanyStatus` (raw enum vrijednost)
- **Response:** `CompanyRead`
- **Greške:**
  - `403` — korisnik nije admin
  - `404` — kompanija nije pronađena ili je obrisana

---

#### `PATCH /companies/{company_id}/restore`

Vraća soft-deletovanu kompaniju — postavlja `is_deleted` na `false`.

- **Autentifikacija:** Admin JWT token
- **Response:** `CompanyRead`
- **Greške:**
  - `403` — korisnik nije admin
  - `404` — kompanija nije pronađena

---

#### `PATCH /companies/{company_id}/upload-logo`

Upload novog logoa kompanije. Stari logo se briše sa diska.

- **Autentifikacija:** Kompanija JWT token
- **Content-Type:** `multipart/form-data`
- **Body:**

| Polje  | Tip           | Opis                             |
| ------ | ------------- | -------------------------------- |
| `logo` | `file` (File) | Novi logo (PNG, JPG, JPEG, WebP) |

- **Response:** `CompanyRead`
- **Greške:**
  - `403` — kompanija nema dozvolu za ažuriranje tuđeg logoa
  - `400` — logo nije ispravan format

---

#### `DELETE /companies/{company_id}`

Soft delete kompanije — postavlja `is_deleted` na `true`, zapis ostaje u bazi.

- **Autentifikacija:** Admin JWT token
- **Response:** `CompanyRead`
- **Greške:**
  - `403` — korisnik nije admin
  - `404` — kompanija nije pronađena ili je već obrisana

---

### Ads (Oglasi)

**Base URL:** `/ads`  
**Tag:** `Ads`

---

| Metoda   | Putanja                | Opis                                        | Pristup   |
| -------- | ---------------------- | ------------------------------------------- | --------- |
| `GET`    | `/ads/`                | Lista svih aktivnih oglasa (s filterima)    | Javno     |
| `GET`    | `/ads/admin/list`      | Lista svih oglasa bez filtera (s filterima) | Admin     |
| `GET`    | `/ads/{ad_id}`         | Detalji jednog oglasa                       | Javno     |
| `POST`   | `/ads/`                | Kreiranje novog oglasa                      | Kompanija |
| `PUT`    | `/ads/{ad_id}`         | Potpuno ažuriranje oglasa                   | Kompanija |
| `PATCH`  | `/ads/{ad_id}`         | Parcijalno ažuriranje oglasa                | Kompanija |
| `PATCH`  | `/ads/{ad_id}/status`  | Promjena statusa oglasa                     | Admin     |
| `DELETE` | `/ads/{ad_id}`         | Soft delete oglasa                          | Kompanija |
| `POST`   | `/ads/{ad_id}/restore` | Vraćanje obrisanog oglasa                   | Admin     |

---

#### `GET /ads/`

Vraća listu svih aktivnih oglasa koji nisu obrisani. Podržava filtriranje i pretragu.  
Pri dohvatanju automatski postavlja oglas na `expired` ako je deadline prošao.

- **Autentifikacija:** nije potrebna
- **Query parametri:**

| Parametar    | Tip              | Opis                                             |
| ------------ | ---------------- | ------------------------------------------------ |
| `type`       | `AdType \| None` | Filter po tipu oglasa                            |
| `field`      | `str \| None`    | Filter po oblasti                                |
| `location`   | `str \| None`    | Filter po lokaciji                               |
| `company_id` | `int \| None`    | Filter po kompaniji                              |
| `search`     | `str \| None`    | Pretraga po naslovu ili opisu (case-insensitive) |

- **Response:** `List[AdRead]`

---

#### `GET /ads/admin/list`

Vraća listu **svih** oglasa bez filtera po statusu ili `is_deleted`. Podržava iste filtere kao javna ruta uz dodatni filter po statusu.

- **Autentifikacija:** Admin JWT token
- **Query parametri:**

| Parametar    | Tip                | Opis                                             |
| ------------ | ------------------ | ------------------------------------------------ |
| `ad_status`  | `AdStatus \| None` | Filter po statusu oglasa                         |
| `type`       | `AdType \| None`   | Filter po tipu oglasa                            |
| `field`      | `str \| None`      | Filter po oblasti                                |
| `location`   | `str \| None`      | Filter po lokaciji                               |
| `company_id` | `int \| None`      | Filter po kompaniji                              |
| `search`     | `str \| None`      | Pretraga po naslovu ili opisu (case-insensitive) |

- **Response:** `List[AdRead]`
- **Greške:**
  - `403` — korisnik nije admin

---

#### `GET /ads/{ad_id}`

Vraća detalje jednog oglasa. Oglas ne smije biti obrisan.  
Automatski postavlja oglas na `expired` ako je deadline prošao.

- **Autentifikacija:** nije potrebna
- **Response:** `AdRead`
- **Greške:**
  - `404` — oglas nije pronađen ili je obrisan

---

#### `POST /ads/`

Kreiranje novog oglasa. `company_id` se automatski uzima iz JWT tokena kompanije.  
Nakon kreiranja, svim adminima se šalje notifikacija.

- **Autentifikacija:** Kompanija JWT token
- **Body:** `AdCreate`
- **Response:** `AdRead` — `201 Created`

---

#### `PUT /ads/{ad_id}`

Potpuno ažuriranje oglasa. Kompanija može ažurirati samo svoje oglase.  
`updated_at` se automatski postavlja na trenutni UTC timestamp.

- **Autentifikacija:** Kompanija JWT token
- **Body:** `AdUpdate`
- **Response:** `AdRead`
- **Greške:**
  - `403` — kompanija nije vlasnik oglasa
  - `404` — oglas nije pronađen ili je obrisan

---

#### `PATCH /ads/{ad_id}`

Parcijalno ažuriranje oglasa — šalju se samo polja koja se mijenjaju.  
`updated_at` se automatski postavlja na trenutni UTC timestamp.

- **Autentifikacija:** Kompanija JWT token
- **Body:** `AdPatch` (parcijalno)
- **Response:** `AdRead`
- **Greške:**
  - `403` — kompanija nije vlasnik oglasa
  - `404` — oglas nije pronađen ili je obrisan

---

#### `PATCH /ads/{ad_id}/status`

Promjena statusa oglasa od strane admina.  
Ovisno o novom statusu, kompaniji se šalje notifikacija:

- `active` → oglas je odobren
- `rejected` / `changes_requested` → oglas je odbijen ili vraćen na doradu (uz komentar ako postoji)

Ako je status `changes_requested`, automatski se postavlja `changes_requested_at`.

- **Autentifikacija:** Admin JWT token
- **Body:** `StatusUpdate`
- **Response:** `AdRead`
- **Greške:**
  - `403` — korisnik nije admin
  - `404` — oglas nije pronađen ili je obrisan

---

#### `DELETE /ads/{ad_id}`

Soft delete oglasa — postavlja `is_deleted` na `true`, zapis ostaje u bazi.  
`updated_at` se automatski postavlja na trenutni UTC timestamp.

- **Autentifikacija:** Kompanija JWT token
- **Response:** `204 No Content`
- **Greške:**
  - `403` — kompanija nije vlasnik oglasa
  - `404` — oglas nije pronađen ili je već obrisan

---

#### `POST /ads/{ad_id}/restore`

Vraća soft-deletovani oglas — postavlja `is_deleted` na `false` i status na `pending`.  
`updated_at` se automatski postavlja na trenutni UTC timestamp.

- **Autentifikacija:** Admin JWT token
- **Response:** `AdRead`
- **Greške:**
  - `403` — korisnik nije admin
  - `404` — oglas nije pronađen

---

### Applications (Prijave)

**Base URL:** `/applications`  
**Tag:** `Applications`

---

| Metoda   | Putanja                                              | Opis                                      | Pristup         |
| -------- | ---------------------------------------------------- | ----------------------------------------- | --------------- |
| `GET`    | `/applications/`                                     | Lista svih prijava (s filterima)          | Admin           |
| `GET`    | `/applications/company/all`                          | Lista svih prijava za oglase kompanije    | Kompanija       |
| `GET`    | `/applications/company/by-ad/{ad_id}`                | Lista prijava za određeni oglas kompanije | Kompanija       |
| `GET`    | `/applications/company/application/{application_id}` | Detalji jedne prijave (kompanija)         | Kompanija       |
| `GET`    | `/applications/{application_id}`                     | Detalji jedne prijave                     | Admin / Vlasnik |
| `POST`   | `/applications/`                                     | Kreiranje nove prijave                    | Student         |
| `POST`   | `/applications/upload-cv`                            | Upload CV-a                               | Student         |
| `PATCH`  | `/applications/company/{application_id}`             | Ažuriranje statusa prijave                | Kompanija       |
| `PATCH`  | `/applications/{application_id}`                     | Ažuriranje prijave                        | Admin           |
| `DELETE` | `/applications/{application_id}`                     | Arhiviranje prijave                       | Admin           |

---

#### `GET /applications/`

Vraća listu svih prijava. Podržava filtriranje po statusu, oglasu i arhiviranim prijavama.

- **Autentifikacija:** Admin JWT token
- **Query parametri:**

| Parametar          | Tip                         | Opis                                          |
| ------------------ | --------------------------- | --------------------------------------------- |
| `app_status`       | `ApplicationStatus \| None` | Filter po statusu prijave                     |
| `ad_id`            | `int \| None`               | Filter po oglasu                              |
| `include_archived` | `bool`                      | Uključi arhivirane prijave (default: `false`) |

- **Response:** `List[ApplicationRead]`
- **Greške:**
  - `403` — korisnik nije admin

---

#### `GET /applications/company/all`

Vraća sve prijave za oglase trenutno prijavljene kompanije. Ne uključuje arhivirane prijave.

- **Autentifikacija:** Kompanija JWT token
- **Query parametri:**

| Parametar    | Tip                         | Opis                      |
| ------------ | --------------------------- | ------------------------- |
| `app_status` | `ApplicationStatus \| None` | Filter po statusu prijave |

- **Response:** `List[ApplicationRead]`

---

#### `GET /applications/company/by-ad/{ad_id}`

Vraća prijave za određeni oglas koji pripada trenutnoj kompaniji. Podržava paginaciju.

- **Autentifikacija:** Kompanija JWT token
- **Query parametri:**

| Parametar | Tip   | Opis                                       |
| --------- | ----- | ------------------------------------------ |
| `limit`   | `int` | Maksimalan broj rezultata (default: `100`) |
| `offset`  | `int` | Pomak za paginaciju (default: `0`)         |

- **Response:** `List[ApplicationRead]`
- **Greške:**
  - `403` — oglas ne pripada kompaniji
  - `404` — oglas nije pronađen

---

#### `GET /applications/company/application/{application_id}`

Vraća detalje jedne prijave za oglas koji pripada trenutnoj kompaniji.

- **Autentifikacija:** Kompanija JWT token
- **Response:** `ApplicationRead`
- **Greške:**
  - `403` — oglas ne pripada kompaniji
  - `404` — prijava nije pronađena

---

#### `GET /applications/{application_id}`

Vraća detalje jedne prijave. Student može vidjeti samo svoje prijave.

- **Autentifikacija:** Admin ili Student JWT token
- **Response:** `ApplicationRead`
- **Greške:**
  - `403` — korisnik nije admin niti vlasnik prijave
  - `404` — prijava nije pronađena

---

#### `POST /applications/`

Kreiranje nove prijave na oglas. Samo studenti (`member`) mogu aplicirati.  
Oglas mora biti aktivan i deadline ne smije biti prošao.

- **Autentifikacija:** Student JWT token
- **Body:** `ApplicationCreate`
- **Response:** `ApplicationRead` — `201 Created`
- **Greške:**
  - `400` — oglas nije aktivan ili mu je istekao deadline
  - `403` — korisnik nije student
  - `404` — oglas nije pronađen
  - `409` — prijava za ovaj oglas već postoji

---

#### `POST /applications/upload-cv`

Upload CV-a u PDF formatu. Vraća putanju fajla koja se koristi pri kreiranju prijave.

- **Autentifikacija:** Student JWT token
- **Content-Type:** `multipart/form-data`
- **Body:**

| Polje  | Tip           | Opis                        |
| ------ | ------------- | --------------------------- |
| `file` | `file` (File) | CV u PDF formatu (max 5 MB) |

- **Response:** `{ "path": "uploads/applications/{filename}.pdf" }`
- **Greške:**
  - `400` — fajl nije PDF
  - `400` — fajl prelazi limit od 5 MB

---

#### `PATCH /applications/company/{application_id}`

Ažuriranje statusa prijave od strane kompanije.  
Ovisno o novom statusu, studentu se šalje notifikacija:

- `accepted` → prijava prihvaćena, loguje se aktivnost, oglas se automatski postavlja na `expired` ako su popunjena sva mjesta
- `rejected` → prijava odbijena

- **Autentifikacija:** Kompanija JWT token
- **Body:** `ApplicationUpdate`
- **Response:** `ApplicationRead`
- **Greške:**
  - `403` — oglas ne pripada kompaniji
  - `404` — prijava nije pronađena

---

#### `PATCH /applications/{application_id}`

Administratorsko ažuriranje prijave bez dodatnih provjera vlasništva.

- **Autentifikacija:** Admin JWT token
- **Body:** `ApplicationUpdate`
- **Response:** `ApplicationRead`
- **Greške:**
  - `403` — korisnik nije admin
  - `404` — prijava nije pronađena

---

#### `DELETE /applications/{application_id}`

Arhiviranje prijave — postavlja `is_archived` na `true`, zapis ostaje u bazi.

- **Autentifikacija:** Admin JWT token
- **Response:** `204 No Content`
- **Greške:**
  - `403` — korisnik nije admin
  - `404` — prijava nije pronađena

---

### Bookmarks (Sačuvani oglasi)

**Base URL:** `/bookmarks`  
**Tag:** `Bookmarks`

> Sve rute su dostupne isključivo korisnicima s ulogom `member` (student).

---

| Metoda   | Putanja                    | Opis                        | Pristup |
| -------- | -------------------------- | --------------------------- | ------- |
| `POST`   | `/bookmarks/`              | Dodavanje oglasa u sačuvane | Student |
| `GET`    | `/bookmarks/`              | Lista svih sačuvanih oglasa | Student |
| `GET`    | `/bookmarks/{bookmark_id}` | Detalji jednog bookmarkа    | Student |
| `DELETE` | `/bookmarks/{bookmark_id}` | Uklanjanje bookmarkа        | Student |

---

#### `POST /bookmarks/`

Dodaje oglas u sačuvane za trenutno prijavljenog studenta.

- **Autentifikacija:** Student JWT token
- **Body:** `AdBookmarkCreate`
- **Response:** `AdBookmarkRead` — `201 Created`
- **Greške:**
  - `400` — oglas je već bookmarkovan
  - `403` — korisnik nije student

---

#### `GET /bookmarks/`

Vraća listu svih sačuvanih oglasa trenutno prijavljenog studenta.

- **Autentifikacija:** Student JWT token
- **Response:** `List[AdBookmarkRead]`
- **Greške:**
  - `403` — korisnik nije student

---

#### `GET /bookmarks/{bookmark_id}`

Vraća detalje jednog bookmarkа. Student može vidjeti samo svoje bookmarke.

- **Autentifikacija:** Student JWT token
- **Response:** `AdBookmarkRead`
- **Greške:**
  - `403` — korisnik nije student ili bookmark ne pripada njemu
  - `404` — bookmark nije pronađen

---

#### `DELETE /bookmarks/{bookmark_id}`

Trajno briše bookmark iz baze. Student može obrisati samo svoje bookmarke.

- **Autentifikacija:** Student JWT token
- **Response:** `204 No Content`
- **Greške:**
  - `403` — korisnik nije student ili bookmark ne pripada njemu
  - `404` — bookmark nije pronađen

---

### Notifications (Notifikacije)

**Base URL:** `/notifications`  
**Tag:** `Notifications`

> Rute podržavaju i korisnike (`User`) i kompanije (`Company`) kroz zajednički `get_current_actor` dependency koji automatski određuje tip aktera iz JWT tokena.

---

| Metoda             | Putanja                                 | Opis                            | Pristup              |
| ------------------ | --------------------------------------- | ------------------------------- | -------------------- |
| `POST`             | `/notifications/`                       | Kreiranje notifikacije          | Admin                |
| `GET`              | `/notifications/me`                     | Lista mojih notifikacija        | Korisnik / Kompanija |
| `POST\|PATCH\|PUT` | `/notifications/read-all`               | Označavanje svih kao pročitano  | Korisnik / Kompanija |
| `POST\|PATCH\|PUT` | `/notifications/{notification_id}/read` | Označavanje jedne kao pročitano | Korisnik / Kompanija |
| `DELETE`           | `/notifications/clear-all`              | Brisanje svih notifikacija      | Korisnik / Kompanija |
| `GET`              | `/notifications/{notification_id}`      | Detalji jedne notifikacije      | Korisnik / Kompanija |
| `PATCH`            | `/notifications/{notification_id}`      | Ažuriranje notifikacije         | Korisnik / Kompanija |
| `DELETE`           | `/notifications/{notification_id}`      | Brisanje notifikacije           | Korisnik / Kompanija |

---

#### `POST /notifications/`

Ručno kreiranje notifikacije. Isključivo za administratore.

- **Autentifikacija:** Admin JWT token
- **Body:** `NotificationCreate`
- **Response:** `Notification` — `201 Created`
- **Greške:**
  - `403` — akter nije admin

---

#### `GET /notifications/me`

Vraća sve notifikacije trenutno prijavljenog korisnika ili kompanije.  
Sortiranje: nepročitane prve, zatim po datumu kreiranja (najnovije prvo).

- **Autentifikacija:** Korisnik ili Kompanija JWT token
- **Response:** `List[Notification]`

---

#### `POST|PATCH|PUT /notifications/read-all`

Označava sve nepročitane notifikacije trenutnog aktera kao pročitane.

- **Autentifikacija:** Korisnik ili Kompanija JWT token
- **Response:** `{ "detail": "All notifications marked as read." }`

---

#### `POST|PATCH|PUT /notifications/{notification_id}/read`

Označava jednu notifikaciju kao pročitanu.  
Admin može označiti bilo koju notifikaciju, ostali akteri samo svoje.

- **Autentifikacija:** Korisnik ili Kompanija JWT token
- **Response:** `Notification`
- **Greške:**
  - `403` — notifikacija ne pripada akteru
  - `404` — notifikacija nije pronađena

---

#### `DELETE /notifications/clear-all`

Trajno briše sve notifikacije trenutnog aktera iz baze.

- **Autentifikacija:** Korisnik ili Kompanija JWT token
- **Response:** `204 No Content`

---

#### `GET /notifications/{notification_id}`

Vraća detalje jedne notifikacije.  
Admin može vidjeti bilo koju notifikaciju, ostali akteri samo svoje.

- **Autentifikacija:** Korisnik ili Kompanija JWT token
- **Response:** `Notification`
- **Greške:**
  - `403` — notifikacija ne pripada akteru
  - `404` — notifikacija nije pronađena

---

#### `PATCH /notifications/{notification_id}`

Parcijalno ažuriranje notifikacije — šalju se samo polja koja se mijenjaju.  
Admin može ažurirati bilo koju notifikaciju, ostali akteri samo svoje.

- **Autentifikacija:** Korisnik ili Kompanija JWT token
- **Body:** `NotificationUpdate` (parcijalno)
- **Response:** `Notification`
- **Greške:**
  - `403` — notifikacija ne pripada akteru
  - `404` — notifikacija nije pronađena

---

#### `DELETE /notifications/{notification_id}`

Trajno briše jednu notifikaciju iz baze.  
Admin može obrisati bilo koju notifikaciju, ostali akteri samo svoje.

- **Autentifikacija:** Korisnik ili Kompanija JWT token
- **Response:** `204 No Content`
- **Greške:**
  - `403` — notifikacija ne pripada akteru
  - `404` — notifikacija nije pronađena
