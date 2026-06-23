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

---

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

---


## Tim 4 funkcionalnosti

### Enum - `ActivityType`

Definiše dozvoljene tipove aktivnosti koje se mogu logovati.

| Vrijednost | Opis |
|---|---|
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
| `GET` | `/profiles/public` | `get_public_profiles` |Vraća listu svih aktivnih korisnika (`is_active = true`) kao javne profile. | 200 OK |
| `GET` | `/profiles/{user_id}/public` | `get_public_profile_by_id` | Vraća javni profil jednog korisnika po ID-u. Korisnik mora biti aktivan. | 200 OK, 404 Not Found |

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


## Dokumentacija modula

### Tim 2 — Materijali (Lejla Kadušić)


#### Pregled

Ova dokumentacija opisuje backend implementaciju koju je radila Lejla Kadušić u okviru Tim 2 — modul Materijali. Implementacija obuhvata upload materijala i kompletnu funkcionalnost komentara, uključujući paginaciju liste materijala.

Sav kod se nalazi u `backend/app/routers/materials.py` i `backend/app/models/materials.py`.

---

#### Sprint 1 — Upload materijala

### Dozvoljeni formati

```python
ALLOWED_FORMATS = {".pdf", ".doc", ".docx", ".ppt", ".pptx", ".zip", ".txt"}
```

Skup dozvoljenih ekstenzija fajlova. Pored PDF, DOC i DOCX koji su bili eksplicitno navedeni u zahtjevima, dodani su i PPT, PPTX i TXT kao uobičajeni akademski formati.

### `validate_file_format(file)`

Izvlači ekstenziju iz naziva fajla i poredi s `ALLOWED_FORMATS`. Baca `HTTP 400 Bad Request` ako format nije podržan, s porukom koja navodi dozvoljene formate.

### `save_file_to_disk(file)`

Sprema uploadovani fajl u `uploads/` direktorij. Direktorij se automatski kreira ako ne postoji (`os.makedirs(..., exist_ok=True)`). Svaki fajl dobija `uuid.uuid4()` prefiks kako bi se spriječila kolizija fajlova istog naziva — originalni naziv ostaje vidljiv korisnicima.

### `POST /materials/upload` — Zaštićen (JWT)

Upload novog materijala na platformu. Endpoint:
1. Validira format fajla
2. Provjerava duplikate (isti naziv od istog korisnika, ili isti fajl)
3. Sprema fajl na disk
4. Kreira zapis u bazi
5. Ako upis u bazu ne uspije — automatski briše fajl s diska (rollback mehanizam)
6. Šalje notifikaciju svim adminima o novom materijalu na čekanju

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request (form-data):**
```
title        string   — naziv materijala
description  string   — opis
subject_id   int      — ID predmeta
file_type    string   — tip (skripta, auditorne_vjezbe, laboratorijske_vjezbe, ispiti, projekat)
file         file     — fajl koji se uploaduje
```

**Response `200 OK`:** vraća `Material` objekt

**Moguće greške:**
| Status | Razlog |
|---|---|
| `400` | Nedozvoljeni format fajla |
| `401` | Korisnik nije prijavljen |
| `409` | Duplikat naziva ili fajla |
| `500` | Greška pri upisu u bazu |

---

#### Sprint 2 — Komentari (GET, POST, DELETE)

### Model — `Comment`

| Polje | Tip | Opis |
|---|---|---|
| `id` | int | Primarni ključ |
| `content` | str | Tekst komentara (max 500 karaktera) |
| `created_at` | datetime | Datum kreiranja (automatski) |
| `updated_at` | datetime/None | Datum izmjene (None dok se ne uredi) |
| `material_id` | int | FK → materials.id |
| `user_id` | int | FK → users.id |

### `GET /materials/{material_id}/comments` — Javno

Vraća listu svih komentara za materijal, sortiranih od najnovijeg prema najstarijem (`ORDER BY created_at DESC`). Koristi `selectinload(Comment.user)` za eager loading podataka o autoru. Endpoint je javan — komentare mogu vidjeti i neprijavljeni korisnici.

**Response `200 OK`:**
```json
[
  {
    "id": 3,
    "user_id": 7,
    "material_id": 1,
    "content": "Odličan materijal!",
    "created_at": "2026-05-18T22:00:00",
    "updated_at": null,
    "user": { "id": 7, "full_name": "Ime Prezime" }
  }
]
```

### `POST /materials/{material_id}/comments` — Zaštićen (JWT)

Kreira novi komentar. Tekst se trimuje (`strip()`), pa validira:
- Ne smije biti prazan → `400 Bad Request`
- Ne smije prelaziti 500 karaktera → `400 Bad Request`

Nakon uspješnog upisa vraća novi komentar s učitanim podacima o autoru.

**Request body:**
```json
{ "content": "Tekst komentara", "material_id": 1 }
```

**Response `201 Created`:**
```json
{
  "id": 4,
  "user_id": 7,
  "material_id": 1,
  "content": "Tekst komentara",
  "created_at": "2026-06-01T10:00:00",
  "updated_at": null,
  "user": { "id": 7, "full_name": "Ime Prezime" }
}
```

**Moguće greške:**
| Status | Razlog |
|---|---|
| `400` | Prazan tekst ili duži od 500 karaktera |
| `401` | Korisnik nije prijavljen |
| `404` | Materijal ne postoji |

### `DELETE /materials/{material_id}/comments/{comment_id}` — Zaštićen (JWT)

Briše komentar. Implementirana stroga autorizacija:
- Ako korisnik nije ni autor ni admin → `403 Forbidden`
- Ako komentar ne postoji ili ne pripada tom materijalu → `404 Not Found`
- Nakon uspješnog brisanja → `204 No Content` (bez tijela odgovora)

**Moguće greške:**
| Status | Razlog |
|---|---|
| `401` | Nije prijavljen |
| `403` | Nije autor komentara ni admin |
| `404` | Komentar ne postoji |

---

#### Sprint 3 — Uređivanje komentara i paginacija

### Izmjena modela — polje `updated_at`

Dodano polje `updated_at` u `Comment` model:
```python
updated_at: Optional[datetime] = Field(default=None)
```
Inicijalno je `None` i postavlja se tek pri prvom uređivanju. Pokrenuta Alembic migracija da se polje doda u bazu.

### `PATCH /materials/{material_id}/comments/{comment_id}` — Zaštićen (JWT)

Uređuje postojeći komentar. Samo autor komentara može ga urediti — pokušaj uređivanja tuđeg komentara vraća `403 Forbidden`. Primjenjuje se ista validacija kao pri kreiranju. Nakon uspješnog uređivanja upisuje se `datetime.utcnow()` u polje `updated_at`.

**Request body:**
```json
{ "content": "Ažurirani tekst", "material_id": 1 }
```

**Response `200 OK`:** vraća ažurirani `CommentResponse` s popunjenim `updated_at`

**Moguće greške:**
| Status | Razlog |
|---|---|
| `400` | Prazan tekst ili duži od 500 karaktera |
| `401` | Nije prijavljen |
| `403` | Nije autor komentara |
| `404` | Komentar ne postoji |

### Paginacija — `PaginatedMaterialsResponse` model

```python
class PaginatedMaterialsResponse(SQLModel):
    items: list[MaterialsResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
```

### `GET /materials/` — Zaštićen (JWT, opcionalno)

Dodan `page` i `per_page` query parametar. Paginacija se radi na nivou Python liste (ne SQL `LIMIT/OFFSET`) — dohvate se svi rezultati, pa se isjecaju:

```python
start = (page - 1) * per_page
end = start + per_page
return PaginatedMaterialsResponse(
    items=svi[start:end],
    total=total,
    page=page,
    per_page=per_page,
    total_pages=(total + per_page - 1) // per_page,
)
```

**Query parametri:**
```
page        int        — broj stranice (default: 1, min: 1)
per_page    int        — materijala po stranici (default: 10, max: 50)
years       list[int]  — filtriranje po godini studija
types       list[str]  — filtriranje po tipu materijala
subject_id  int        — filtriranje po predmetu
mine_only   bool       — samo vlastiti materijali (zahtijeva prijavu)
```

---

#### Autentifikacija i autorizacija

Svi zaštićeni endpointi koriste `Depends(get_current_user)` koji dekodira JWT iz `Authorization: Bearer <token>` headera. Ako token nedostaje ili je neispravan — automatski `401 Unauthorized`.

Autorizacija je implementirana unutar poslovne logike endpointa:
- Brisanje komentara: `komentar.user_id != current_user.id` i `current_user.role != UserRole.admin` → `403`
- Uređivanje komentara: `comment.user_id != current_user.id` → `403`

---

### Tim 2 — Materijali (Marinela Mitić)

#### Pregled

Ovaj dio dokumentacije opisuje backend implementaciju koju je radila Marinela Mitić u okviru Tim 2 — modul Materijali. Implementacija obuhvata preuzimanje materijala s bilježenjem korisnika, kompletnu funkcionalnost ocjenjivanja (sistem zvjezdica 1–5) i generisanje thumbnail sličica materijala.

Sav kod se nalazi u `backend/app/routers/materials.py` i `backend/app/models/materials.py`.

> **Napomena o podjeli rada unutar Tima 2:** Modul Materijali je razvijan u saradnji s kolegama. Sekcija opisana ispod odnosi se isključivo na lično implementirani dio: **preuzimanje, ocjenjivanje, thumbnail**. Funkcija `validate_file_format` je zajednički rad (validacija formata fajla).

---

#### Sprint 1 — Preuzimanje materijala

##### Model — `Download`

Tabela koja bilježi koji je korisnik preuzeo koji materijal. Predstavlja temelj za pravilo "korisnik mora preuzeti materijal prije nego što ga može ocijeniti".

| Polje | Tip | Opis |
|---|---|---|
| `id` | int | Primarni ključ |
| `material_id` | int | FK → materials.id |
| `user_id` | int | FK → users.id |
| `downloaded_at` | datetime | Vrijeme preuzimanja (automatski) |

##### Validacija formata fajla — `validate_file_format(file)` *(zajednički rad)*

```python
ALLOWED_FORMATS = {".pdf", ".doc", ".docx", ".ppt", ".pptx", ".zip", ".txt"}
```

Izvlači ekstenziju iz naziva fajla, pretvara je u mala slova i poredi sa skupom `ALLOWED_FORMATS`. Ako format nije podržan, baca `HTTP 400 Bad Request` s porukom koja navodi dozvoljene formate.

---

##### `GET /materials/{id}/download` — Javno (s opcionalnim tokenom)

Preuzimanje fajla materijala uz bilježenje korisnika i povećanje brojača preuzimanja.

**Auth:** Opcionalna — token se prosljeđuje kao **query parametar** (`?token=...`), a ne kroz `Authorization` zaglavlje, jer se preuzimanje pokreće direktno iz preglednika gdje nije moguće jednostavno dodati zaglavlje. Ako je token prisutan, preuzimanje se bilježi za tog korisnika; ako nije, materijal se i dalje može preuzeti (javni pristup), ali bez bilježenja.

**Tok izvršavanja:**
1. Provjera da materijal postoji (`404` ako ne)
2. Provjera da materijal nije obrisan — `status == "deleted"` → `404`
3. Provjera uloge preko tokena — administrator može preuzeti i neodobrene materijale
4. Ako materijal nije odobren i korisnik nije admin → `403`
5. Provjera da fajl fizički postoji na disku (`404` ako ne)
6. Povećanje brojača `number_of_downloads`
7. Bilježenje u `Download` tabelu — samo ako korisnik ranije nije zabilježen za isti materijal (sprječava duplikate)
8. Vraćanje fajla putem `FileResponse`

**Request:**
```
GET /materials/5/download?token=<token>
```

**Response `200 OK`:** vraća fajl (binarni sadržaj) sa zaglavljem `Content-Disposition` koje sadrži originalni naziv fajla.

**Mogući odgovori:**

| Status | Razlog |
|---|---|
| `200` | Uspješno — vraća fajl |
| `403` | Materijal nije odobren (a korisnik nije admin) |
| `404` | Materijal ne postoji, obrisan je, ili fajl nije pronađen na serveru |

> **Napomena:** Sam `Download` model bilježi preuzimanja već u Sprintu 1, ali se kao **uslov za ocjenjivanje** (provjera "je li korisnik preuzeo") koristi tek u Sprintu 3.

---

#### Sprint 2 — Ocjenjivanje materijala (sistem zvjezdica)

##### Model — `Rating`

| Polje | Tip | Opis |
|---|---|---|
| `id` | int | Primarni ključ |
| `rating` | int | Ocjena, validirana na nivou modela: `ge=1, le=5` |
| `material_id` | int | FK → materials.id |
| `user_id` | int | FK → users.id |

Validacija `Field(ge=1, le=5)` osigurava da ocjena uvijek bude cijeli broj između 1 i 5, na nivou samog modela (prije nego što podaci dođu do baze).

---

##### `POST /materials/{id}/rate` — Zaštićen (JWT)

Kreira novu ocjenu za materijal.

**Auth:** Obavezna (JWT).

**Tok provjera (redom):**
1. Postoji li materijal → `404` ako ne
2. Da li je korisnik već ocijenio ovaj materijal → `409`
3. Spremanje nove ocjene
4. Slanje notifikacije vlasniku materijala (osim ako korisnik ocjenjuje vlastiti materijal)

> **Napomena:** Provjera "da li je korisnik preuzeo materijal" (`403`) dodana je u Sprintu 3 i opisana je u tom dijelu. U Sprintu 2 endpoint je radio ocjenjivanje bez tog uslova.

**Request:**
```
POST /materials/5/rate
Authorization: Bearer <token>
Content-Type: application/json

{ "rating": 5, "material_id": 5 }
```

**Response `201 Created`:**
```json
{
  "id": 12,
  "rating": 5,
  "material_id": 5,
  "user_id": 7
}
```

**Mogući odgovori:**

| Status | Razlog |
|---|---|
| `201` | Ocjena uspješno kreirana |
| `401` | Korisnik nije prijavljen |
| `403` | Korisnik nije preuzeo materijal |
| `404` | Materijal ne postoji |
| `409` | Korisnik je već ocijenio materijal |

---

##### `PATCH /materials/{id}/rate` — Zaštićen (JWT)

Mijenja postojeću ocjenu korisnika. Provodi istu provjeru preuzimanja kao i kreiranje.

**Auth:** Obavezna (JWT).

**Tok provjera (redom):**
1. Da li je korisnik preuzeo materijal → `403` ako nije *(provjera dodana u Sprintu 3)*
2. Da li korisnik ima postojeću ocjenu koju mijenja → `404` ako ne postoji
3. Ažuriranje vrijednosti ocjene

**Request:**
```
PATCH /materials/5/rate
Authorization: Bearer <token>
Content-Type: application/json

{ "rating": 4, "material_id": 5 }
```

**Response `200 OK`:**
```json
{
  "id": 12,
  "rating": 4,
  "material_id": 5,
  "user_id": 7
}
```

**Mogući odgovori:**

| Status | Razlog |
|---|---|
| `200` | Ocjena uspješno izmijenjena |
| `401` | Korisnik nije prijavljen |
| `403` | Korisnik nije preuzeo materijal |
| `404` | Korisnik nema postojeću ocjenu |

---

##### Pravila ocjenjivanja (sažetak)

| Pravilo | Implementacija |
|---|---|
| Neprijavljeni korisnik ne može ocijeniti | Endpoint je zaštićen `Depends(get_current_user)` → `401` |
| Korisnik mora preuzeti materijal prije ocjenjivanja (vrijedi i za studenta i za admina) | Provjera u `Download` tabeli → `403` *(dodano u Sprintu 3)* |
| Korisnik može ocijeniti materijal samo jednom | Provjera postojeće ocjene → `409`; izmjena ide kroz `PATCH` |
| Korisnik može promijeniti svoju ocjenu | `PATCH /materials/{id}/rate` |
| Ocjena mora biti 1–5 | `Field(ge=1, le=5)` na modelu |

> **Napomena:** Pravilo "korisnik ne može ocijeniti vlastiti materijal" provodi se na frontendu. Na backendu se vlasništvo koristi samo za preskakanje notifikacije (vlasnik ne dobija obavijest da je vlastiti materijal ocijenjen). Provjera vlasništva i na backendu (`material.user_id == current_user.id → 403`) moguća je dopuna radi potpune dosljednosti zaštite.

---

#### Sprint 3 — Thumbnail, provjera preuzimanja za ocjenu

##### Provjera "korisnik mora preuzeti prije ocjenjivanja"

U Sprintu 3 dodan je uslov za ocjenjivanje: korisnik mora preuzeti materijal prije nego što ga može ocijeniti. U endpointima `POST /materials/{id}/rate` i `PATCH /materials/{id}/rate` dodana je provjera u `Download` tabeli — ako korisnik nije zabilježen kao da je preuzeo materijal, vraća se `403`:

```python
download = db.exec(
    select(Download).where(
        Download.material_id == id,
        Download.user_id == current_user.id
    )
).first()
if not download:
    raise HTTPException(status_code=403, detail="Morate preuzeti materijal prije ocjenjivanja.")
```

Ova provjera oslanja se na `Download` model (iz Sprinta 1) i vrijedi jednako za studenta i za admina.

##### `GET /materials/{id}/has-downloaded` — Zaštićen (JWT)

Pomoćni endpoint koji vraća `true`/`false` — da li je trenutno prijavljeni korisnik već preuzeo dati materijal. Frontend ga koristi da odluči hoće li zvjezdice za ocjenjivanje biti aktivne ili zaključane.

**Auth:** Obavezna (JWT kroz `Authorization: Bearer <token>` zaglavlje). Za razliku od `/download`, ovaj endpoint poziva frontend JavaScript, koji bez problema može poslati zaglavlje.

**Request:**
```
GET /materials/5/has-downloaded
Authorization: Bearer <token>
```

**Response `200 OK`:**
```json
{ "has_downloaded": true }
```

| Status | Razlog |
|---|---|
| `200` | Uspješno — vraća stanje |
| `401` | Korisnik nije prijavljen |

---

#### Sprint 3 — Thumbnail sličice materijala

##### Izmjena modela — polje `thumbnail_path`

Dodano polje u `Material` model za čuvanje putanje generisane thumbnail sličice:

```python
thumbnail_path: Optional[str] = Field(default=None, sa_column=Column(String, nullable=True))
```

Polje je opcionalno (`nullable`) jer se thumbnail ne generiše za svaki materijal — ako generisanje ne uspije ili format nije podržan, vrijednost ostaje `None`.

##### `generate_thumbnail(file_path)`

Funkcija generiše PNG sličicu prve stranice dokumenta. Logika ovisi o tipu fajla:

- **PDF** — otvara se bibliotekom `PyMuPDF` (`fitz`), uzima se prva stranica i renderuje u sliku na pola veličine (`Matrix(0.5, 0.5)`), te sprema kao PNG u `uploads/thumbnails/`.
- **Office formati (PPTX, PPT, DOCX, DOC)** — fajl se prvo konvertuje u PDF pomoću LibreOffice (`soffice`) u headless modu, a zatim se thumbnail generiše iz tog PDF-a. Privremeni PDF se briše nakon korištenja.
- **Ostali formati (ZIP, TXT)** — nemaju thumbnail; funkcija vraća `None`.

Cijela funkcija je obavijena `try/except` blokom kako neuspjeh generisanja thumbnaila ne bi prekinuo proces uploada — u tom slučaju materijal se sprema bez thumbnaila.

##### Prenosivost — pronalaženje LibreOffice instalacije

Putanja do `soffice` izvršne datoteke pronalazi se automatski, umjesto da bude fiksno zadana, kako bi generisanje thumbnaila radilo neovisno o operativnom sistemu:

```python
soffice_bin = shutil.which("soffice") or shutil.which("libreoffice")
if not soffice_bin:
    return None
```

- `shutil.which("soffice")` — automatsko pronalaženje LibreOffice u sistemskom PATH-u (macOS / Linux / Windows)
- `shutil.which("libreoffice")` — rezervna komanda (neke Linux distribucije koriste ovaj naziv)

Ako LibreOffice nije instaliran, funkcija graciozno vraća `None` — PDF thumbnaili i dalje rade, samo Office formati ostaju bez sličice. Ovim pristupom thumbnail za Office formate radi na svakom operativnom sistemu bez ručne konfiguracije.

##### Posluživanje thumbnail sličica

Generisane sličice se poslužuju kao statički sadržaj putem `/thumbnails/` rute (konfigurisano u `app/main.py`), kako bi ih frontend mogao prikazati direktno preko URL-a.

---

#### Autentifikacija i autorizacija

Zaštićeni endpointi (`/rate`, `/has-downloaded`) koriste `Depends(get_current_user)`, koji dekodira JWT iz `Authorization: Bearer <token>` zaglavlja i vraća `401` ako token nedostaje ili je neispravan.

Endpoint za preuzimanje (`/download`) namjerno koristi **opcionalni token kroz query parametar** umjesto obaveznog zaglavlja, jer se poziva direktno iz preglednika. Kada je token prisutan, preuzimanje se bilježi za tog korisnika; kada nije, materijal se i dalje može preuzeti (javni pristup), ali bez bilježenja.

---

#### Migracije baze podataka

```bash
cd backend
source venv/bin/activate
alembic revision --autogenerate -m "opis promjene"
alembic upgrade head
```

---

### Tim 2 — Materijali (Amer Imamović) — Backend

#### Pregled

Ova dokumentacija opisuje backend implementaciju koju je radio Amer Imamović u okviru Tim 2 — modul Materijali. Implementacija obuhvata brisanje materijala, toggle bookmark funkcionalnost i kompletne filtere za pretragu materijala po godini, tipu i predmetu.

Sav kod se nalazi u `backend/app/routers/materials.py` i `backend/app/models/materials.py`.

---

#### Sprint 1 — Brisanje materijala

### Model — `Material.status`

Brisanje je implementirano kao **soft delete** — materijal se označava kao obrisan a ne briše se iz baze:

```python
status: str = Field(default="pending")  # pending, approved, rejected, deleted
```

### `DELETE /materials/{id}` — Zaštićen (JWT)

Briše (označava kao obrisano) zadani materijal. Samo autor materijala ili admin mogu obrisati materijal.

**Autentifikacija:** Zahtijeva JWT token (korisnik mora biti prijavljen)

**Autorizacija:**
- Admin može obrisati bilo koji materijal
- Korisnik može obrisati samo vlastite materijale
- Neovlašteni pristup vraća `403 Forbidden`

**Request:**
```
DELETE /materials/{id}
Authorization: Bearer <token>
```

**Response `204 No Content`:** Materijal uspješno označen kao obrisan (bez tijela odgovora)

**Moguće greške:**
| Status | Razlog |
|---|---|
| `401` | Korisnik nije prijavljen |
| `403` | Nemate dozvolu za brisanje (nije autor ni admin) |
| `404` | Materijal ne postoji |

**Napomena:** Obrisani materijali nisu dostupni u javnom popisu, ali ako su ih već preuzeli korisnici, oni mogu pristupiti verziji koju su preuzeli.

---

#### Sprint 2 — Bookmark (Omiljeni materijali)

### Model — `Bookmark`

```python
class Bookmark(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    material_id: int = Field(foreign_key="material.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

Bookmark je vanjska tabela koja povezuje korisnike s materijalima kao "omiljeni". Svaki red predstavlja omiljenu relaciju između korisnika i materijala.

### `POST /materials/{material_id}/bookmark` — Zaštićen (JWT)

Toggle bookmark za materijal — ako je već bookmarkovan uklanja se, ako nije — dodaje se. Admini ne mogu bookmarkovati materijale.

**Autentifikacija:** Zahtijeva JWT token

**Request:**
```
POST /materials/42/bookmark
Authorization: Bearer <token>
```

**Response (Toggle — dva mogućnostna odgovora):**

Ako je materijal **dodat kao omiljeni**:
```json
{
  "is_bookmarked": true
}
```

Ako je materijal **uklonjen iz omiljenih**:
```json
{
  "is_bookmarked": false
}
```

**Moguće greške:**
| Status | Razlog |
|---|---|
| `401` | Korisnik nije prijavljen |

**Frontend integracija:** Kad korisnik klikne na zastavicu:
1. Šalje se `POST` zahtjev na `/materials/{id}/bookmark`
2. Backend vraća `is_bookmarked: true/false`
3. Frontend ažurira svojstvo `material.is_bookmarked` u listi
4. UI se osvježi da prikaže narandžastu (bookmarked) ili sivu (unbookmarked) zastavicu

---

#### Sprint 3 — Filteri (Godina, Tip, Predmet)

### Filteri u `GET /materials/` i `GET /materials/public`

Oba endpointa (`/materials/` za prijavljene i `/materials/public` za javni pristup) podržavaju sljedeće query parametare:

**Query parametri:**
```
years       list[int]  — filtriranje po godini studija (npr. ?years=1&years=2)
types       list[str]  — filtriranje po tipu materijala (npr. ?types=skripta&types=ispiti)
subject_id  int        — filtriranje po ID-u predmeta (npr. ?subject_id=5)
page        int        — broj stranice (default: 1, min: 1)
per_page    int        — materijala po stranici (default: 10, max: 50)
mine_only   bool       — samo vlastiti materijali (zahtijeva prijavu) — dostupno samo na /materials/
```

### Dozvoljeni tipovi materijala

```python
ALLOWED_TYPES = {
    'skripta': 'Skripte',
    'auditorne_vjezbe': 'Auditorne vježbe',
    'laboratorijske_vjezbe': 'Laboratorijske vježbe',
    'ispiti': 'Ispiti',
    'projekat': 'Projekat'
}
```

### Primjeri API poziva s filterima

**Primjer 1: Materijali za 1. i 2. godinu:**
```
GET /materials/?years=1&years=2&page=1&per_page=10
```

**Primjer 2: Samo skripte za predmet ID=5:**
```
GET /materials/?subject_id=5&types=skripta&page=1
```

**Primjer 3: Ispiti i laboratorijske vježbe:**
```
GET /materials/?types=ispiti&types=laboratorijske_vjezbe
```

**Primjer 4: Kombinovani filteri - godina 3, tip skripta, predmet 10:**
```
GET /materials/?years=3&types=skripta&subject_id=10&page=1&per_page=20
```

### Implementaciona logika filtera

Filteri se primjenjuju na SQL nivou prije paginacije:

```python
# Filtriranje po godini studija
if years:
    query = query.join(Subject, Material.subject_id == Subject.id).where(Subject.study_year.in_(years))

# Filtriranje po tipu materijala
if types:
    query = query.where(Material.file_type.in_(types))

# Filtriranje po predmetu
if subject_id:
    query = query.where(Material.subject_id == subject_id)
```

**Napomena:** Filteri se mogu kombinovati — svi aktivni filteri se primjenjuju zajedno (AND logika).

---

#### Bookmark stanje u listama materijala

Kada je korisnik prijavljen, svaki materijal u API odgovoru sadrži polje `is_bookmarked`:

```python
user_bookmarks = session.exec(
    select(Bookmark.material_id).where(Bookmark.user_id == current_user.id)
).all()

response = MaterialsResponse(
    **material.model_dump(),
    is_bookmarked=material.id in user_bookmarks,  # True ako je bookmarked
)
```

**Javni endpoint (`/materials/public`)** ne šalje bookmark stanje jer nema informacije o korisniku — korisnici koji žele vidjeti svoje bookmarke trebaju koristiti `/materials/` s autentifikacijom.

---

### Tim 2 — Materijali (Faris Ćosić)

### Modeli

#### `Material`
| Polje | Tip | Opis |
|---|---|---|
| `id` | int | Primarni ključ |
| `title` | str | Naziv materijala |
| `description` | str? | Opis materijala |
| `file_path` | str | Putanja do fajla na serveru |
| `file_type` | str | Tip materijala (npr. `PDF`, `PPT`) |
| `status` | str | `pending` / `approved` / `rejected` / `deleted` |
| `number_of_downloads` | int | Broj preuzimanja |
| `thumbnail_path` | str? | Putanja do thumbnail slike |
| `subject_id` | int | FK → `subjects.id` |
| `user_id` | int | FK → `users.id` |
| `created_at` | datetime | Datum kreiranja |

#### `Subject`
| Polje | Tip | Opis |
|---|---|---|
| `id` | int | Primarni ključ |
| `name` | str | Naziv predmeta |
| `study_year` | int | Godina studija (1–4) |

#### `Comment`
| Polje | Tip | Opis |
|---|---|---|
| `id` | int | Primarni ključ |
| `content` | str | Tekst komentara (maks. 500 znakova) |
| `material_id` | int | FK → `materials.id` |
| `user_id` | int | FK → `users.id` |
| `created_at` | datetime | Datum kreiranja |
| `updated_at` | datetime? | Datum izmjene |

#### `Rating`
| Polje | Tip | Opis |
|---|---|---|
| `id` | int | Primarni ključ |
| `rating` | int | Ocjena (1–5) |
| `material_id` | int | FK → `materials.id` |
| `user_id` | int | FK → `users.id` |

#### `Download`
| Polje | Tip | Opis |
|---|---|---|
| `id` | int | Primarni ključ |
| `material_id` | int | FK → `materials.id` |
| `user_id` | int | FK → `users.id` |
| `downloaded_at` | datetime | Datum preuzimanja |

#### `Bookmark`
| Polje | Tip | Opis |
|---|---|---|
| `id` | int | Primarni ključ |
| `material_id` | int | FK → `materials.id` |
| `user_id` | int | FK → `users.id` |

---

### Endpointi

#### `GET /materials/subjects`
Vraća listu svih predmeta.

- **Auth:** nije potrebna
- **Response:** `Subject[]`

---

#### `GET /materials/pending`
Vraća listu materijala koji čekaju odobrenje.

- **Auth:** admin
- **Response:** `MaterialsResponse[]`
- **Greške:** `403` ako korisnik nije admin

---

#### `GET /materials/`
Vraća paginirani spisak odobrenih materijala. Podržava filtriranje i prikaz samo vlastitih materijala.

- **Auth:** opcionalna (potrebna za `mine_only`)
- **Query params:**

| Param | Tip | Opis |
|---|---|---|
| `years` | int[] | Filtriranje po godini studija |
| `types` | str[] | Filtriranje po tipu fajla |
| `subject_id` | int | Filtriranje po predmetu |
| `mine_only` | bool | Prikazuje samo materijale prijavljenog korisnika |
| `page` | int | Stranica (default: 1) |
| `per_page` | int | Stavki po stranici (default: 10, maks: 50) |

- **Response:** `PaginatedMaterialsResponse`

---

#### `GET /materials/public`
Isti kao `GET /materials/` ali bez autentikacije — za neprijavljene korisnike.

- **Auth:** nije potrebna
- **Query params:** `years`, `types`, `subject_id`, `page`, `per_page`
- **Response:** `PaginatedMaterialsResponse`

---

#### `GET /materials/{id}`
Vraća detalje jednog materijala uključujući komentare i ocjene.

- **Auth:** nije potrebna
- **Response:** `MaterialDetailResponse`
- **Greške:** `404` ako materijal ne postoji

---

#### `GET /materials/{id}/preview`
Vraća fajl inline za pregled u browseru (bez preuzimanja).

- **Auth:** nije potrebna
- **Response:** `FileResponse` (inline)
- **Greške:** `404` ako materijal ili fajl ne postoje

---

#### `PATCH /materials/{material_id}/approve`
Admin odobrava materijal. Korisnik koji je postavio materijal dobiva notifikaciju.

- **Auth:** admin
- **Response:** `{ "message": "Materijal odobren." }`
- **Greške:** `403`, `404`

---

#### `PATCH /materials/{material_id}/reject`
Admin odbija materijal. Korisnik koji je postavio materijal dobiva notifikaciju.

- **Auth:** admin
- **Response:** `{ "message": "Materijal odbijen." }`
- **Greške:** `403`, `404`

---

#### `PATCH /materials/{material_id}/update`
Vlasnik materijala može izmijeniti naslov, opis, predmet, tip ili zamijeniti fajl. Ako se fajl zamijeni, status se vraća na `pending`.

- **Auth:** vlasnik materijala
- **Body (multipart/form-data):**

| Polje | Tip | Obavezno |
|---|---|---|
| `title` | str | ne |
| `description` | str | ne |
| `subject_id` | int | ne |
| `material_type` | str | ne |
| `file` | UploadFile | ne |

- **Dozvoljeni formati:** `.pdf`, `.doc`, `.docx`, `.ppt`, `.pptx`, `.zip`, `.txt`
- **Response:** `{ "message": "Materijal ažuriran." }`
- **Greške:** `403`, `404`, `400` (nedozvoljen format)


### Tim 3 - Forum
---
### Forum Modeli Podataka
---

### ForumCategory (Kategorija foruma)
#### Tabela: `forum_categories`

---

#### SQLModel — `ForumCategory` (tabela)

| Polje | Tip | Opis |
| :--- | :--- | :--- |
| `id` | `int \| None` | Primarni ključ, auto-increment (default: `None`) |
| `name` | `str` | Naziv kategorije (indeksiran, max 100 karaktera) |
| `color` | `str` | HEX kod boje za frontend prikaz (default: `#ff7a00`, max 20 karaktera) |
| `description` | `str \| None` | Opis kategorije (opcionalno, max 255 karaktera, default: `None`) |

##### Relacije
| Relacija | Model | Opis |
| :--- | :--- | :--- |
| `topics` | `List[ForumTopic]` | Lista svih tema koje pripadaju ovoj kategoriji |

---

#### Pydantic shema — `ForumCategoryCreate`
*Koristi se pri kreiranju nove kategorije (`POST /forum/categories`).*

| Polje | Tip | Validacija / Default |
| :--- | :--- | :--- |
| `name` | `str` | Obavezno polje, max 100 karaktera |
| `color` | `str` | Default: `#ff7a00`, max 20 karaktera |
| `description` | `str \| None` | Opcionalno, max 255 karaktera |

---

#### Pydantic shema — `ForumCategoryUpdate`
*Koristi se pri ažuriranju kategorije (`PATCH /forum/categories/{id}`). Sva polja su opcionalna.*

| Polje | Tip | Validacija / Default |
| :--- | :--- | :--- |
| `name` | `str \| None` | Max 100 karaktera |
| `color` | `str \| None` | Max 20 karaktera |
| `description` | `str \| None` | Max 255 karaktera |

---

#### Pydantic shema — `ForumCategoryRead`
*Vraća se kao response na API pozive.*

| Polje | Tip | Opis |
| :--- | :--- | :--- |
| `id` | `int` | Jedinstveni identifikator |
| `name` | `str` | Naziv kategorije |
| `color` | `str` | HEX boja kategorije |
| `description` | `str \| None` | Opis kategorije |

---

### ForumTopic (Tema foruma)
#### Tabela: `forum_topics`

---

#### SQLModel — `ForumTopic` (tabela)

| Polje | Tip | Opis |
| :--- | :--- | :--- |
| `id` | `int \| None` | Primarni ključ, auto-increment (default: `None`) |
| `title` | `str` | Naslov teme (indeksiran, max 200 karaktera) |
| `content` | `str` | Glavni tekst/sadržaj teme |
| `views_count` | `int` | Broj pregleda teme (default: `0`) |
| `is_locked` | `bool` | Flag da li je tema zaključana za nove komentare (default: `False`) |
| `is_deleted` | `bool` | Soft delete flag (default: `False`) |
| `created_at` | `datetime` | Datum kreiranja teme (auto generisano preko `datetime.utcnow`) |
| `updated_at` | `datetime \| None` | Datum posljednje izmjene (default: `None`) |
| `category_id` | `int` | Strani ključ -> `forum_categories.id` |
| `user_id` | `int` | Strani ključ -> `users.id` (Autor teme) |

##### Relacije
| Relacija | Model | Opis |
| :--- | :--- | :--- |
| `category` | `ForumCategory \| None` | Objekt kategorije kojoj tema pripada |
| `comments` | `List[ForumComment]` | Lista svih komentara na ovoj temi |

---

#### Pydantic shema — `ForumTopicCreate`
*Koristi se pri kreiranju nove teme (`POST /forum/topics`).*

| Polje | Tip | Validacija / Default |
| :--- | :--- | :--- |
| `title` | `str` | Obavezno, max 200 karaktera |
| `content` | `str` | Obavezno tekstualno polje |
| `category_id` | `int` | ID postojeće kategorije |

---

#### Pydantic shema — `ForumTopicRead`
*Vraća se kao response na API pozive za teme (ne uključuje `is_deleted`).*

| Polje | Tip | Opis |
| :--- | :--- | :--- |
| `id` | `int` | Jedinstveni identifikator teme |
| `title` | `str` | Naslov teme |
| `content` | `str` | Sadržaj teme |
| `views_count` | `int` | Broj pregleda |
| `is_locked` | `bool` | Status zaključavanja |
| `created_at` | `datetime` | Vrijeme kreiranja |
| `updated_at` | `datetime \| None` | Vrijeme izmjene |
| `category_id` | `int` | ID kategorije |
| `user_id` | `int` | ID autora |

---

### ForumComment (Komentar foruma)
#### Tabela: `forum_comments`

---

#### SQLModel — `ForumComment` (tabela)

| Polje | Tip | Opis |
| :--- | :--- | :--- |
| `id` | `int \| None` | Primarni ključ, auto-increment (default: `None`) |
| `content` | `str` | Tekstualni sadržaj komentara |
| `is_admin_notice` | `bool` | Da li je komentar zvanična napomena moderatora/admina (default: `False`) |
| `is_best_answer` | `bool` | Da li je komentar označen kao prihvaćeno rješenje (default: `False`) |
| `is_deleted` | `bool` | Soft delete flag (default: `False`) |
| `parent_id` | `int \| None` | Strani ključ -> `forum_comments.id` (Omogućava ugniježdene odgovore) |
| `created_at` | `datetime` | Datum kreiranja (auto generisano preko `datetime.utcnow`) |
| `updated_at` | `datetime \| None` | Datum posljednje izmjene (default: `None`) |
| `topic_id` | `int` | Strani ključ -> `forum_topics.id` |
| `user_id` | `int` | Strani ključ -> `users.id` (Autor komentara) |

##### Relacije
| Relacija | Model | Opis |
| :--- | :--- | :--- |
| `topic` | `ForumTopic \| None` | Tema na kojoj se nalazi komentar |
| `votes` | `List[ForumCommentVote]` | Svi glasovi (upvote/downvote) na ovom komentaru |
| `replies` | `List[ForumComment]` | Samoreferencirajuća relacija (odgovori na ovaj komentar sa `lazy="select"`) |

---

### Interakcije i prateći modeli (Glasovi, Lajkovi, Tagovi)

#### Tabela: `forum_comment_votes`
*Čuva pojedinačne glasove korisnika za komentare (Upvote / Downvote).*

| Polje | Tip | Opis |
| :--- | :--- | :--- |
| `id` | `int \| None` | Primarni ključ, auto-increment |
| `comment_id` | `int` | Strani ključ -> `forum_comments.id` |
| `user_id` | `int` | Strani ključ -> `users.id` |
| `value` | `int` | Vrijednost glasa (npr. `1` za upvote, `-1` za downvote, default: `1`) |
| `created_at` | `datetime` | Vrijeme glasanja |

##### Ograničenja i Relacije
- **Jedinstvenost:** `UniqueConstraint("comment_id", "user_id", name="unique_comment_vote_per_user")` sprečava duplo glasanje od strane istog korisnika.
- **Relacija:** `comment` -> Poveznica nazad na `ForumComment` objekat.

---

#### Tabela: `topic_likes`
*Čuva podatke o lajkovima na nivou cijele teme.*

| Polje | Tip | Opis |
| :--- | :--- | :--- |
| `id` | `int \| None` | Primarni ključ, auto-increment |
| `topic_id` | `int` | Strani ključ -> `forum_topics.id` (Indeksiran) |
| `user_id` | `int` | Strani ključ -> `users.id` (Indeksiran) |
| `created_at` | `datetime` | Vrijeme kreiranja lajka |

##### Ograničenja
- **Jedinstvenost:** `UniqueConstraint("topic_id", "user_id", name="unique_topic_like_per_user")`.

---

#### Tabela: `topic_dislikes`
*Čuva podatke o dislajkovima na nivou cijele teme.*

| Polje | Tip | Opis |
| :--- | :--- | :--- |
| `id` | `int \| None` | Primarni ključ, auto-increment |
| `topic_id` | `int` | Strani ključ -> `forum_topics.id` (Indeksiran) |
| `user_id` | `int` | Strani ključ -> `users.id` (Indeksiran) |
| `created_at` | `datetime` | Vrijeme kreiranja dislajka |

##### Ograničenja
- **Jedinstvenost:** `UniqueConstraint("topic_id", "user_id", name="unique_topic_dislike_per_user")`.

---

#### Tabela: `forum_tags`
*Katalog unikatnih tagova na forumu.*

| Polje | Tip | Opis |
| :--- | :--- | :--- |
| `id` | `int \| None` | Primarni ključ, auto-increment |
| `name` | `str` | Jedinstveno ime taga (indeksiran, unique, max 50 karaktera) |

---

#### Tabela: `forum_topic_tags`
*Pivot tabela za Many-to-Many relaciju između tema i tagova.*

| Polje | Tip | Opis |
| :--- | :--- | :--- |
| `topic_id` | `int \| None` | Primarni ključ i Strani ključ -> `forum_topics.id` |
| `tag_id` | `int \| None` | Primarni ključ i Strani ključ -> `forum_tags.id` |

---

### Prilozi (Attachments)

#### Tabela: `topic_attachments`
*Meta-podaci o fajlovima zakačenim uz forum teme.*

| Polje | Tip | Opis |
| :--- | :--- | :--- |
| `id` | `int \| None` | Primarni ključ, auto-increment |
| `topic_id` | `int` | Strani ključ -> `forum_topics.id` (Indeksiran) |
| `filename` | `str` | Originalni naziv fajla (max 255 karaktera) |
| `file_path` | `str` | Putanja do fajla na disku/storage-u (max 500 karaktera) |
| `file_size` | `int` | Veličina fajla u bajtovima (`bytes`) |
| `mime_type` | `str` | MIME tip fajla (max 100 karaktera, npr. `image/jpeg`) |
| `created_at` | `datetime` | Vrijeme uploada |

---

#### Tabela: `comment_attachments`
*Meta-podaci o fajlovima zakačenim uz pojedinačne komentare.*

| Polje | Tip | Opis |
| :--- | :--- | :--- |
| `id` | `int \| None` | Primarni ključ, auto-increment |
| `comment_id` | `int` | Strani ključ -> `forum_comments.id` (Indeksiran) |
| `filename` | `str` | Originalni naziv fajla (max 255 karaktera) |
| `file_path` | `str` | Putanja do fajla na disku/storage-u (max 500 karaktera) |
| `file_size` | `int` | Veličina fajla u bajtovima |
| `mime_type` | `str` | MIME tip fajla (max 100 karaktera) |
| `created_at` | `datetime` | Vrijeme uploada |

---

### Moderacija i administracija

#### Tabela: `topic_reports`
*Prijave korisnika za teme koje krše pravila.*

| Polje | Tip | Opis |
| :--- | :--- | :--- |
| `id` | `int \| None` | Primarni ključ, auto-increment |
| `topic_id` | `int` | Strani ključ -> `forum_topics.id` |
| `user_id` | `int` | Strani ključ -> `users.id` (Korisnik koji prijavljuje) |
| `reason` | `str` | Razlog prijave (max 100 karaktera) |
| `created_at` | `datetime` | Vrijeme kreiranja prijave |
| `status` | `str` | Status prijave (default: `"pending"`) |
| `action_taken` | `str \| None` | Akcija koju je admin preduzeo (default: `None`) |
| `admin_explanation` | `str \| None` | Obrazloženje od strane administracije (default: `None`) |

---

#### Tabela: `admin_announcements`
*Globalna obavještenja kreirana od strane administratora.*

| Polje | Tip | Opis |
| :--- | :--- | :--- |
| `id` | `int \| None` | Primarni ključ, auto-increment |
| `admin_id` | `int` | Strani ključ -> `users.id` (ID administratora) |
| `title` | `str` | Naslov obavještenja (max 150 karaktera) |
| `content` | `str` | Kompletan tekst/sadržaj obavještenja |
| `is_active` | `bool` | Da li je obavještenje aktivno (default: `True`) |
| `created_at` | `datetime` | Vrijeme kreiranja obavještenja |
| `expires_at` | `datetime \| None`| Datum kada obavještenje ističe (opcionalno, default: `None`) |

---

#### Tabela: `forum_guidelines`
*Pravilnik ponašanja na forumu.*

| Polje | Tip | Opis |
| :--- | :--- | :--- |
| `id` | `int \| None` | Primarni ključ, auto-increment |
| `title` | `str` | Naslov specifičnog pravila |
| `content` | `str` | Detaljan tekstualni opis pravila |
| `order` | `int` | Redoslijed sortiranja pri prikazu (default: `0`) |
| `created_at` | `datetime` | Vrijeme kreiranja |
| `updated_at` | `datetime` | Vrijeme zadnje izmjene |

---

#### Opšte napomene o sistemu modela
1. **Upravljanje Vremenom:** Sva polja sa datumima (`created_at`, `updated_at`) automatski koriste UTC zonu preko `datetime.utcnow` prilikom upisa u bazu, ukoliko vrijednost nije eksplicitno proslijeđena.
2. **Logičko Brisanje:** Teme (`ForumTopic`) i komentari (`ForumComment`) posjeduju polje `is_deleted`. Brisanje ovih entiteta na forumu treba raditi isključivo postavljanjem ovog flaga na `True` (soft delete) kako bi se očuvao integritet historije i povezanih relacija.

---

### ForumNotification (Notifikacije foruma)
#### Tabela: `forum_notifications`

---

#### SQLModel — `ForumNotification` (tabela)

| Polje | Tip | Opis |
| :--- | :--- | :--- |
| `id` | `int \| None` | Primarni ključ, auto-increment (default: `None`) |
| `recipient_user_id` | `int` | Strani ključ -> `users.id` (Korisnik koji prima notifikaciju, indeksiran) |
| `actor_user_id` | `int` | Strani ključ -> `users.id` (Korisnik koji je izazvao notifikaciju, indeksiran) |
| `topic_id` | `int` | Strani ključ -> `forum_topics.id` (Tema na koju se odnosi notifikacija, indeksirana) |
| `comment_id` | `int \| None` | Strani ključ -> `forum_comments.id` (Komentar na koji vodi klik, indeksiran, default: `None`) |
| `text` | `str` | Tekstualni sadržaj i poruka notifikacije |
| `type` | `ForumNotificationType` | Tip notifikacije (Enum vrijednost) |
| `is_read` | `bool` | Flag da li je korisnik pročitao notifikaciju (default: `False`) |
| `is_hidden` | `bool` | Flag za logičko sakrivanje nevažećih notifikacija (default: `False`) |
| `created_at` | `datetime` | Vrijeme kreiranja notifikacije (auto generisano u UTC preko `datetime.now(timezone.utc)`) |

---

#### Enum — `ForumNotificationType`
*Definiše sve podržane događaje koji okidaju slanje notifikacije unutar forum sistema.*

| Vrijednost | Tip | Opis |
| :--- | :--- | :--- |
| `"topic_like"` | `str` | Korisnik je lajkovao temu |
| `"topic_dislike"` | `str` | Korisnik je dislajkovao temu |
| `"topic_reply"` | `str` | Dodan je novi komentar na temu čiji je korisnik autor |
| `"comment_reply"` | `str` | Dodan je direktan odgovor (reply) na komentar korisnika |
| `"mention"` | `str` | Korisnik je tagovan/spomenut unutar teksta |
| `"best_answer"` | `str` | Korisnikov komentar je označen kao prihvaćeno rješenje teme |
| `"comment_like"` | `str` | Korisnik je dobio pozitivan glas (upvote) na komentar |
| `"comment_dislike"` | `str` | Korisnik je dobio negativan glas (downvote) na komentar |

---

#### Napomene o sistemu notifikacija
1. **Upotreba `is_hidden` polja:** Ovaj flag rješava specifične slučajeve poništavanja akcija. Na primjer, ako autor teme označi komentar kao *best answer*, a zatim unutar par sekundi ukloni tu oznaku, sistem neće obrisati zapis iz baze nego će staru, nepročitanu notifikaciju postaviti na `is_hidden = True` kako se ne bi prikazivala u korisnikovom inboxu.
2. **Rutiranje na frontendu:** Polje `comment_id` je opcionalno jer se za akcije poput `topic_like` i `topic_reply` (gdje se skače na vrh teme) koristi isključivo `topic_id`. Kada je `comment_id` prisutan, frontend ga koristi za automatsko skrolovanje i fokusiranje na tačan komentar u stablu diskusije.
3. **Generisanje datuma:** Za razliku od ostalih modela koji koriste zastarjeli `datetime.utcnow`, ovaj model pravilno koristi modernu `timezone.utc` svjesnu fabriku za bilježenje tačnog vremena kreiranja zapisa.

---

### ForumReputation (Reputacija i statistika korisnika)

#### Tabela: `forum_user_stats`

---

#### SQLModel — `ForumUserStats` (tabela)
*Čuva trenutne bodove, nivo reputacije i agregiranu aktivnost pojedinačnog korisnika.*

| Polje | Tip | Opis |
| :--- | :--- | :--- |
| `user_id` | `int` | Primarni ključ i Strani ključ -> `users.id` (1:1 veza sa korisnikom) |
| `reputation_points` | `int` | Trenutni ukupni bodovi reputacije korisnika (default: `0`) |
| `topics_started_count` | `int` | Ukupan broj tema koje je korisnik pokrenuo (default: `0`) |
| `answers_count` | `int` | Ukupan broj napisanih odgovora/komentara (default: `0`) |
| `best_answers_count` | `int` | Broj komentara koji su označeni kao najbolji odgovor (default: `0`) |
| `night_topics_count` | `int` | Broj tema pokrenutih tokom noćnih sati (default: `0`) |
| `updated_at` | `datetime` | Vrijeme posljednjeg ažuriranja zapisa (auto generisano preko `utc_now`) |

---

#### Tabela: `forum_user_medals`
*Čuva sve osvojene medalje i priznanja korisnika na forumu.*

---

#### SQLModel — `ForumUserMedal` (tabela)

| Polje | Tip | Opis |
| :--- | :--- | :--- |
| `id` | `int \| None` | Primarni ključ, auto-increment (default: `None`) |
| `user_id` | `int` | Strani ključ -> `users.id` (Vlasnik medalje, indeksiran) |
| `medal_code` | `str` | Jedinstveni identifikacioni kod medalje (indeksiran) |
| `category` | `str` | Kategorija medalje (npr. `activity`, `moderation`, `helpful`) |
| `tier` | `str` | Nivo/Rang medalje (npr. `bronze`, `silver`, `gold`) |
| `is_secret` | `bool` | Da li je medalja bila skrivena prije nego što je osvojena (default: `False`) |
| `awarded_at` | `datetime` | Vrijeme dodjele priznanja (auto generisano preko `utc_now`) |

##### Ograničenja
| Naziv | Polja | Opis |
| :--- | :--- | :--- |
| `uq_forum_user_medal` | `user_id`, `medal_code` | Korisnik može osvojiti specifičnu medalju samo jednom |

---

#### Tabela: `forum_reputation_events`
*Historijski dnevnik svih promjena reputacionih bodova radi transparentnosti i revizije.*

---

#### SQLModel — `ForumReputationEvent` (tabela)

| Polje | Tip | Opis |
| :--- | :--- | :--- |
| `id` | `int \| None` | Primarni ključ, auto-increment (default: `None`) |
| `user_id` | `int` | Strani ključ -> `users.id` (Korisnik kojem se mijenjaju bodovi, indeksiran) |
| `event_key` | `str` | Jedinstveni identifikator događaja radi sprečavanja dupliranja (indeksiran) |
| `points_delta` | `int` | Broj dodijeljenih ili oduzetih bodova (npr. `+10`, `-5`) |
| `reason` | `str` | Opis i razlog promjene (npr. `received_best_answer`) |
| `source_type` | `str \| None` | Tip entiteta koji je izvor promjene (npr. `comment`, `topic`, default: `None`) |
| `source_id` | `int \| None` | ID entiteta koji je uzrokovao promjenu (default: `None`) |
| `created_at` | `datetime` | Vrijeme upisa i obrade događaja (auto generisano preko `utc_now`) |

##### Ograničenja
| Naziv | Polja | Opis |
| :--- | :--- | :--- |
| `uq_forum_reputation_event_key` | `event_key` | Garantuje da se bodovi za isti kôd događaja ne mogu dodijeliti više puta |

---

#### Tabela: `forum_reputation_daily_logs`
*Dnevni log interakcija koji služi kao anti-abuse (mehanizam zaštite od zloupotrebe).*

---

#### SQLModel — `ForumReputationDailyLog` (tabela)

| Polje | Tip | Opis |
| :--- | :--- | :--- |
| `id` | `int \| None` | Primarni ključ, auto-increment (default: `None`) |
| `giver_id` | `int` | Strani ključ -> `users.id` (Korisnik koji daje bodove / lajkuje objavu) |
| `receiver_id` | `int` | Strani ključ -> `users.id` (Korisnik koji prima bodove / autor objave) |
| `points_given` | `int` | Ukupan broj bodova prenijetih u okviru ove transakcije |
| `created_at` | `datetime` | Vrijeme bilježenja aktivnosti (auto generisano preko `utc_now`) |

---

#### Napomene o reputacionom sistemu
1. **Idempotentnost i sigurnost (`event_key`):** Svaki put kada korisnik izvrši akciju koja donosi bodove (npr. lajkovanje teme), generiše se unikatni `event_key` u formatu `like_topic_{topic_id}_{voter_id}`. Ako sistem pokuša ponovo unijeti isti ključ uslijed mrežnog kašnjenja ili spama, baza podataka će odbiti upis i spriječiti duplo dobijanje bodova.
2. **Anti-Abuse sistem (Tiket 2):** Tabela `forum_reputation_daily_logs` se koristi za praćenje i limitiranje broja bodova koje Korisnik A može prenijeti Korisniku B unutar prozora od 24 sata. Ako se detektuje anomalija (npr. ciljano lajkovanje svih historijskih objava istog autora), sistem privremeno blokira prenos reputacije između ta dva računa.
3. **Trajnost medalja:** Za razliku od stanja u `forum_user_stats` gdje bodovi reputacije mogu rasti i opadati u zavisnosti od reakcija zajednice, jednom osvojene medalje u tabeli `forum_user_medals` su trajne prirode i ne povlače se automatski padom bodova.
4. **Vremenska sinkronizacija:** Svi modeli u ovom modulu koriste centralizovanu pomoćnu funkciju `utc_now()` koja osigurava vremensku zonu `timezone.utc` u skladu sa modernim standardima, čime se izbjegavaju problemi sa lokalnim vremenom servera.

---

### Forum API Rute

### Forum Topics (Teme na forumu)

**Base URL:** `/forum/topics`  
**Tag:** `Forum Topics`

> Većina ruta podržava opcionalnu autentifikaciju (`current_user: Optional[User]`) — neprijavljeni korisnici mogu pregledati teme, dok prijavljeni dobijaju dodatne podatke (`is_liked`, `is_disliked`).

---

| Metoda             | Putanja                                       | Opis                                        | Pristup                  |
| ------------------- | ---------------------------------------------- | -------------------------------------------- | ------------------------- |
| `GET`               | `/forum/topics/`                               | Lista svih tema (filter, sort, paginacija)  | Javno / Korisnik           |
| `GET`               | `/forum/topics/suggestions`                    | Prijedlozi tema (autocomplete)              | Javno                      |
| `POST`              | `/forum/topics/`                               | Kreiranje nove teme                          | Korisnik                   |
| `GET`               | `/forum/topics/popular`                        | Popularne teme za sidebar (zadnjih 7 dana)  | Javno / Korisnik           |
| `GET`               | `/forum/topics/category-popular/{category_id}` | Popularne teme po kategoriji                | Javno / Korisnik           |
| `GET`               | `/forum/topics/{topic_id}/related`             | Slične/povezane teme                         | Javno / Korisnik           |
| `GET`               | `/forum/topics/reports/active`                 | Lista aktivnih (na čekanju) prijava         | Admin                      |
| `GET`               | `/forum/topics/reports/handled`                | Lista riješenih prijava                      | Admin                      |
| `PATCH`             | `/forum/topics/reports/{report_id}/action`     | Rješavanje prijave (accept/dismiss/resolve) | Admin                      |
| `GET`               | `/forum/topics/announcements/active`           | Aktivne admin objave                         | Javno                      |
| `GET`               | `/forum/topics/{topic_id}`                     | Detalji jedne teme                           | Javno / Korisnik           |
| `PATCH`             | `/forum/topics/{topic_id}/view`                | Inkrementiranje broja pregleda               | Javno                      |
| `PUT`               | `/forum/topics/{topic_id}`                     | Ažuriranje teme                              | Vlasnik teme / Admin       |
| `DELETE`            | `/forum/topics/{id}`                           | Brisanje teme (soft delete)                  | Vlasnik teme / Admin       |
| `POST`              | `/forum/topics/{topic_id}/report`              | Prijava teme                                  | Korisnik                   |

---

#### `GET /forum/topics/`

Vraća paginiranu listu svih tema, sa mogućnošću filtriranja i sortiranja.

- **Autentifikacija:** Opciono (Korisnik JWT token)
- **Query parametri:**
  - `category_id` (int, opciono) — filter po kategoriji
  - `search` (str, opciono) — pretraga po naslovu i sadržaju (`ILIKE`)
  - `page` (int, default `1`)
  - `per_page` (int, default `5`)
  - `sort_by` (str, default `"najnovije"`) — opcije: `"najnovije"`, `"najgledanije"`, `"najaktivnije"`
  - `unanswered` (bool, default `False`) — prikazuje samo teme bez komentara
  - `days_old` (int, opciono) — filter po starosti teme (broj dana od kreiranja)
- **Response:** `{ "items": List[Topic], "total": int, "page": int, "per_page": int }`

---

#### `GET /forum/topics/suggestions`

Vraća prijedloge tema za autocomplete pretragu po naslovu.

- **Autentifikacija:** Nije potrebna
- **Query parametri:**
  - `search` (str, opciono)
- **Response (bez `search`):**
  `{ "popular": List[{id, title}], "active": List[{id, title}] }`
  — top 3 najgledanije i top 3 najnovije teme
- **Response (sa `search`):**
  `{ "filtered": List[{id, title}] }`
  — prvo pokušava pronaći teme čiji naslov *počinje* sa unesenim tekstom; ako nema rezultata, traži teme čiji naslov *sadrži* taj tekst (max 5 rezultata)

---

#### `POST /forum/topics/`

Kreira novu temu na forumu, uz opcionalno dodavanje tagova.

- **Autentifikacija:** Korisnik JWT token
- **Body:** `ForumTopicCreate`
  - `title` (str, 3–200 karaktera)
  - `content` (str, min 10 karaktera)
  - `category_id` (int)
  - `tags` (List[Any], opciono) — može sadržati nazive tagova (string) koji se kreiraju ako ne postoje, ili postojeće ID-eve tagova
- **Response:** `Topic` — `201 Created`
- **Greške:**
  - `404` — kategorija nije pronađena

---

#### `GET /forum/topics/popular`

Vraća top 5 popularnih tema iz posljednjih 7 dana, rangirano po zbiru pregleda i broja komentara.

- **Autentifikacija:** Opciono (Korisnik JWT token)
- **Response:** `List[Topic]`

---

#### `GET /forum/topics/category-popular/{category_id}`

Vraća top 5 popularnih tema unutar određene kategorije, rangirano po zbiru pregleda i broja komentara.

- **Autentifikacija:** Opciono (Korisnik JWT token)
- **Path parametri:** `category_id` (int)
- **Response:** `List[Topic]`

---

#### `GET /forum/topics/{topic_id}/related`

Vraća do 4 slične teme iz iste kategorije, na osnovu ključnih riječi iz naslova trenutne teme (riječi duže od 2 karaktera, bez interpunkcije).

- **Autentifikacija:** Opciono (Korisnik JWT token)
- **Path parametri:** `topic_id` (int)
- **Response:** `List[Topic]`
- **Greške:**
  - `404` — tema nije pronađena

---

#### `GET /forum/topics/reports/active`

Vraća listu prijava sa statusom `"pending"`, sortirano po datumu kreiranja (najnovije prvo). Isključivo za administratore.

- **Autentifikacija:** Admin JWT token
- **Response:** `List[{ report_id, reason, created_at, status, reporter_name, topic }]`
- **Greške:**
  - `403` — akter nije admin

---

#### `GET /forum/topics/reports/handled`

Vraća listu riješenih prijava (status `"accepted"` ili `"dismissed"`), sortirano po datumu kreiranja (najnovije prvo). Isključivo za administratore.

- **Autentifikacija:** Admin JWT token
- **Response:** `List[{ report_id, reason, created_at, status, reporter_name, topic }]`
- **Greške:**
  - `403` — akter nije admin

---

#### `PATCH /forum/topics/reports/{report_id}/action`

Rješava prijavu teme postavljanjem statusa i (opciono) admin objašnjenja. Ako je akcija `"accept"`, korisniku koji je prijavu podnio se povećava `reports_count`.

- **Autentifikacija:** Admin JWT token
- **Path parametri:** `report_id` (int)
- **Query parametri:** `action` (str) — `"accept"`, `"dismiss"`, ili druga vrijednost (postavlja status `"resolved"`)
- **Body:** `ReportActionPayload`
  - `explanation` (str, opciono, max 500 karaktera)
- **Response:** `{ "success": true, "message": str }`
- **Greške:**
  - `403` — akter nije admin
  - `404` — prijava nije pronađena

---

#### `GET /forum/topics/announcements/active`

Vraća sve aktivne admin objave koje nisu istekle, sortirano po datumu kreiranja (najnovije prvo).

- **Autentifikacija:** Nije potrebna
- **Response:** `List[AdminAnnouncement]`

---

#### `GET /forum/topics/{topic_id}`

Vraća detalje jedne teme, uključujući komentare, tagove, priloge i statistiku. Obrisane teme (`is_deleted`) su vidljive samo administratorima.

- **Autentifikacija:** Opciono (Korisnik JWT token)
- **Path parametri:** `topic_id` (int)
- **Response:** `{ id, title, content, views_count, likes_count, dislikes_count, is_liked, is_disliked, is_locked, created_at, updated_at, author, category, tags, attachments, comments, stats, is_deleted }`
- **Greške:**
  - `404` — tema nije pronađena (ili je obrisana, a korisnik nije admin)

---

#### `PATCH /forum/topics/{topic_id}/view`

Inkrementira broj pregleda teme za 1.

- **Autentifikacija:** Nije potrebna
- **Path parametri:** `topic_id` (int)
- **Response:** `{ "id": int, "views_count": int }`
- **Greške:**
  - `404` — tema nije pronađena ili je obrisana

---

#### `PUT /forum/topics/{topic_id}`

Ažurira naslov i/ili sadržaj teme. Dozvoljeno vlasniku teme ili administratoru.

- **Autentifikacija:** Korisnik JWT token
- **Path parametri:** `topic_id` (int)
- **Body:** `ForumTopicUpdate` (parcijalno)
  - `title` (str, opciono, 3–200 karaktera)
  - `content` (str, opciono, min 3 karaktera)
- **Response:** `Topic`
- **Greške:**
  - `403` — korisnik nije vlasnik teme niti admin
  - `404` — tema nije pronađena ili je obrisana

---

#### `DELETE /forum/topics/{id}`

Briše temu (soft delete — postavlja `is_deleted = True`). Dozvoljeno vlasniku teme ili administratoru.

- **Autentifikacija:** Korisnik JWT token
- **Path parametri:** `id` (int)
- **Response:** `{ "message": "Tema je uspješno obrisana.", "topic_id": int }`
- **Greške:**
  - `403` — korisnik nije vlasnik teme niti admin
  - `404` — tema nije pronađena ili je već obrisana

---

#### `POST /forum/topics/{topic_id}/report`

Prijavljuje temu administraciji uz razlog.

- **Autentifikacija:** Korisnik JWT token
- **Path parametri:** `topic_id` (int)
- **Body:** `ReportCreate`
  - `reason` (str, 3–100 karaktera)
- **Response:** `{ "success": true }`
- **Greške:**
  - `404` — tema ne postoji ili je obrisana

---

### Forum Topic Likes (Lajkovi/Dislajkovi tema)

**Base URL:** `/forum/topics`  
**Tag:** `Forum Topic Likes`

> Korisnik ne može lajkovati/dislajkovati sopstvenu temu. Lajk i dislajk se međusobno isključuju — postavljanje jednog automatski uklanja drugi. Akcije generišu/sakrivaju forum notifikacije vlasniku teme.

---

| Metoda | Putanja                          | Opis                          | Pristup  |
| ------ | --------------------------------- | ------------------------------ | -------- |
| `POST` | `/forum/topics/{topic_id}/like`    | Lajkovanje/uklanjanje lajka teme | Korisnik |
| `POST` | `/forum/topics/{topic_id}/dislike` | Dislajkovanje/uklanjanje dislajka teme | Korisnik |

---

#### `POST /forum/topics/{topic_id}/like`

Toggle akcija — ako korisnik već nije lajkovao temu, dodaje lajk (i uklanja postojeći dislajk ako postoji). Ako je tema već lajkovana od strane korisnika, lajk se uklanja. Vlasniku teme se kreira/sakriva notifikacija tipa `TOPIC_LIKE`.

- **Autentifikacija:** Korisnik JWT token
- **Path parametri:** `topic_id` (int)
- **Response:** `{ topic_id, is_liked, is_disliked, liked, disliked, likes_count, dislikes_count, message }`
- **Greške:**
  - `404` — tema nije pronađena ili je obrisana
  - `400` — korisnik pokušava lajkovati sopstvenu temu

---

#### `POST /forum/topics/{topic_id}/dislike`

Toggle akcija — ako korisnik već nije dislajkovao temu, dodaje dislajk (i uklanja postojeći lajk ako postoji). Ako je tema već dislajkovana od strane korisnika, dislajk se uklanja. Vlasniku teme se kreira/sakriva notifikacija tipa `TOPIC_DISLIKE`.

- **Autentifikacija:** Korisnik JWT token
- **Path parametri:** `topic_id` (int)
- **Response:** `{ topic_id, is_liked, is_disliked, liked, disliked, likes_count, dislikes_count, message }`
- **Greške:**
  - `404` — tema nije pronađena ili je obrisana
  - `400` — korisnik pokušava dislajkovati sopstvenu temu

---

#### Helper funkcije (interno, nisu izložene kao rute)

| Funkcija                          | Opis                                                              |
| ----------------------------------- | -------------------------------------------------------------------- |
| `get_topic_likes_count(db, topic_id)` | Vraća ukupan broj lajkova za temu                                |
| `is_topic_liked_by_user(db, topic_id, user_id)` | Provjerava da li je korisnik lajkovao temu                |
| `get_topic_dislikes_count(db, topic_id)` | Vraća ukupan broj dislajkova za temu                          |
| `is_topic_disliked_by_user(db, topic_id, user_id)` | Provjerava da li je korisnik dislajkovao temu          |
| `get_topic_reaction_response(db, topic_id, user_id)` | Sastavlja standardizovan odgovor sa statusom reakcija i brojevima |

---

### Forum Tags (Tagovi na forumu)

**Base URL:** `/forum/tags`  
**Tag:** `Forum Tags`

---

| Metoda | Putanja        | Opis                                  | Pristup |
| ------ | --------------- | --------------------------------------- | ------- |
| `GET`  | `/forum/tags/`   | Lista popularnih tagova (iznad prosjeka) | Javno   |

---

#### `GET /forum/tags/`

Vraća listu tagova čija je popularnost (broj korištenja na temama) strogo iznad prosječnog broja korištenja svih tagova. Tagovi se prvo sortiraju po broju korištenja (opadajuće), uzima se top `limit`, zatim se računa prosjek i filtriraju samo oni iznad njega.

- **Autentifikacija:** Nije potrebna
- **Query parametri:**
  - `limit` (int, default `20`) — maksimalan broj tagova koji se uzima u obzir prije filtriranja po prosjeku
- **Response:** `List[{ id, name, usage_count }]`

---

### Forum Notifications (Notifikacije na forumu)

**Base URL:** `/forum/notifications`  
**Tag:** `Forum Notifications`

---

| Metoda   | Putanja                              | Opis                                   | Pristup  |
| -------- | -------------------------------------- | ----------------------------------------- | -------- |
| `GET`    | `/forum/notifications/me`              | Lista mojih forum notifikacija            | Korisnik |
| `PATCH`  | `/forum/notifications/{notification_id}/read` | Označavanje jedne kao pročitano   | Korisnik |
| `PATCH`  | `/forum/notifications/read-all`        | Označavanje svih kao pročitano            | Korisnik |
| `DELETE` | `/forum/notifications/{notification_id}` | Brisanje notifikacije                  | Korisnik |

---

#### `GET /forum/notifications/me`

Vraća sve forum notifikacije trenutno prijavljenog korisnika koje nisu sakrivene (`is_hidden == False`).  
Sortiranje: nepročitane prve, zatim po datumu kreiranja (najnovije prvo).

- **Autentifikacija:** Korisnik JWT token
- **Response:** `List[ForumNotification]`

---

#### `PATCH /forum/notifications/{notification_id}/read`

Označava jednu forum notifikaciju kao pročitanu. Dozvoljeno samo vlasniku notifikacije.

- **Autentifikacija:** Korisnik JWT token
- **Path parametri:** `notification_id` (int)
- **Response:** `ForumNotification`
- **Greške:**
  - `403` — notifikacija ne pripada korisniku
  - `404` — notifikacija nije pronađena

---

#### `PATCH /forum/notifications/read-all`

Označava sve nepročitane i nesakrivene notifikacije trenutnog korisnika kao pročitane.

- **Autentifikacija:** Korisnik JWT token
- **Response:** `{ "message": "Sve forum notifikacije su označene kao pročitane.", "updated_count": int }`

---

#### `DELETE /forum/notifications/{notification_id}`

Trajno briše jednu forum notifikaciju iz baze. Dozvoljeno samo vlasniku notifikacije.

- **Autentifikacija:** Korisnik JWT token
- **Path parametri:** `notification_id` (int)
- **Response:** `204 No Content`
- **Greške:**
  - `403` — notifikacija ne pripada korisniku
  - `404` — notifikacija nije pronađena

---

### Forum Comments (Komentari na forumu)

**Base URL:** `/forum/comments`  
**Tag:** `Forum Comments`

> Komentari podržavaju neograničeno ugnježđavanje (reply na reply na reply...). Administratorska obavještenja (`is_admin_notice`) moraju biti glavni komentari i ne mogu primati odgovore. Akcije generišu forum notifikacije i bilježe aktivnost korisnika (`log_activity`) i reputaciju (`forum_reputation` servis).

---

| Metoda   | Putanja                                  | Opis                                          | Pristup           |
| -------- | ------------------------------------------ | ----------------------------------------------- | ------------------ |
| `POST`   | `/forum/comments/`                         | Kreiranje komentara/odgovora                    | Korisnik           |
| `GET`    | `/forum/comments/topic/{topic_id}`         | Lista komentara za temu (stablo)               | Javno              |
| `PATCH`  | `/forum/comments/{comment_id}/best-answer` | Označavanje/uklanjanje najboljeg odgovora      | Vlasnik teme       |
| `POST`   | `/forum/comments/{comment_id}/vote`        | Glasanje na komentar (like/dislike)             | Korisnik           |
| `DELETE` | `/forum/comments/{comment_id}`             | Brisanje komentara                              | Vlasnik / Admin    |
| `PUT`    | `/forum/comments/{comment_id}`             | Ažuriranje komentara                            | Vlasnik / Admin    |
| `POST`   | `/forum/comments/{topic_id}/admin-notice`  | Kreiranje administratorskog obavještenja        | Admin              |

---

#### `POST /forum/comments/`

Kreira novi komentar ili odgovor na temu. Generiše notifikacije autoru teme (ili roditeljskog komentara) i korisnicima spomenutim putem `@username` (mentions).

- **Autentifikacija:** Korisnik JWT token
- **Body:** `ForumCommentCreate`
  - `content` (str, min 2 karaktera)
  - `topic_id` (int)
  - `is_admin_notice` (bool, opciono, default `False`) — primjenjuje se samo ako je korisnik admin
  - `parent_id` (int, opciono) — ID komentara na koji se odgovara
- **Response:** `{ id, content, topic_id, parent_id, is_admin_notice, created_at, author }` — `201 Created`
- **Greške:**
  - `404` — tema nije pronađena ili je obrisana
  - `400` — `is_admin_notice=True` uz postavljen `parent_id` (obavještenje ne može biti odgovor)
  - `404` — komentar na koji se odgovara ne postoji
  - `400` — pokušaj odgovora na administratorsko obavještenje

---

#### `GET /forum/comments/topic/{topic_id}`

Vraća sve komentare teme organizovane u stablo (sa ugnježđenim odgovorima). Glavni komentari su sortirani po: admin obavještenja prva, zatim najbolji odgovor, zatim broj glasova (opadajuće), zatim datum kreiranja. Odgovori su rekurzivno sortirani po istom principu (bez glasova).

- **Autentifikacija:** Nije potrebna
- **Path parametri:** `topic_id` (int)
- **Response:** `List[Comment]` (svaki sa `replies: List[Comment]`)
- **Greške:**
  - `404` — tema nije pronađena ili je obrisana

---

#### `PATCH /forum/comments/{comment_id}/best-answer`

Postavlja ili uklanja status "najbolji odgovor" za komentar. Samo autor teme može označiti najbolji odgovor. Ako već postoji drugi najbolji odgovor, on se automatski poništava. Generiše/sakriva notifikaciju tipa `BEST_ANSWER` i ažurira reputaciju.

- **Autentifikacija:** Korisnik JWT token
- **Path parametri:** `comment_id` (int)
- **Response:** `{ "id": int, "is_best_answer": bool }`
- **Greške:**
  - `404` — komentar ili tema nisu pronađeni
  - `403` — korisnik nije autor teme

---

#### `POST /forum/comments/{comment_id}/vote`

Glasa na komentar (like = `1`, dislike = `-1`). Ako korisnik ponovo pošalje istu vrijednost, glas se uklanja. Ako pošalje suprotnu vrijednost, glas se mijenja. Ažurira reputaciju autora komentara i generiše/sakriva odgovarajuće notifikacije (`COMMENT_LIKE` / `COMMENT_DISLIKE`).

- **Autentifikacija:** Korisnik JWT token
- **Path parametri:** `comment_id` (int)
- **Body:** `VoteInput`
  - `value` (int) — `1` za like, `-1` za dislike
- **Response:** `{ "comment_id": int, "votes_count": int, "user_vote": int }` — `user_vote` je `0` ako je glas uklonjen
- **Greške:**
  - `400` — `value` nije `1` ili `-1`
  - `404` — komentar ili tema nisu pronađeni

---

#### `DELETE /forum/comments/{comment_id}`

Briše komentar. Ako komentar ima aktivne (neobrisane) odgovore, vrši se soft delete (`is_deleted = True`, sadržaj se prikazuje kao "deleted by user"). Ako nema odgovora, komentar se trajno briše iz baze, a njegovi eventualni obrisani odgovori se "otkače" (`parent_id = None`).

- **Autentifikacija:** Korisnik JWT token
- **Path parametri:** `comment_id` (int)
- **Response:** `{ "message": "Komentar je uspješno obrisan.", "comment_id": int }`
- **Greške:**
  - `404` — komentar nije pronađen ili je već obrisan
  - `403` — korisnik nije autor komentara niti admin

---

#### `PUT /forum/comments/{comment_id}`

Ažurira sadržaj komentara. Ponovo provjerava `@username` mentions u odnosu na stari sadržaj i šalje notifikacije novo spomenutim korisnicima.

- **Autentifikacija:** Korisnik JWT token
- **Path parametri:** `comment_id` (int)
- **Body:** `ForumCommentUpdate`
  - `content` (str, min 2 karaktera)
- **Response:** `{ "id": int, "content": str, "updated_at": datetime }`
- **Greške:**
  - `404` — komentar ili tema nisu pronađeni
  - `403` — korisnik nije autor komentara niti admin

---

#### `POST /forum/comments/{topic_id}/admin-notice`

Kreira administratorsko obavještenje kao glavni komentar teme (bez mogućnosti odgovora). Isključivo za administratore.

- **Autentifikacija:** Admin JWT token
- **Path parametri:** `topic_id` (int)
- **Body:** `AdminNoticeCreate`
  - `content` (str, min 3 karaktera)
- **Response:** `{ "success": true, "id": int }` — `201 Created`
- **Greške:**
  - `403` — akter nije admin
  - `404` — tema nije pronađena ili je obrisana

---

#### Helper funkcije (interno, nisu izložene kao rute)

| Funkcija                                  | Opis                                                                  |
| -------------------------------------------- | -------------------------------------------------------------------------- |
| `get_comment_author_data(db, user_id)`        | Vraća podatke o autoru komentara (uključujući forum identitet/reputaciju) |
| `get_comment_votes_count(db, comment_id)`      | Vraća zbir vrijednosti svih glasova na komentaru                       |
| `get_comment_likes_count(db, comment_id)`      | Vraća broj lajkova komentara                                            |
| `get_comment_dislikes_count(db, comment_id)`   | Vraća broj dislajkova komentara                                         |
| `get_comments_count(db, topic_id)`             | Vraća broj neobrisanih komentara na temi                                |
| `has_best_answer(db, topic_id)`                | Provjerava da li tema ima označen najbolji odgovor                     |
| `get_topic_votes_count(db, topic_id)`          | Vraća zbir glasova svih komentara na temi                               |
| `get_topic_comments(db, topic_id)`             | Vraća komentare teme organizovane u stablo (sa odgovorima i sortiranjem) |

---

### Forum Helpers (Zajedničke pomoćne funkcije)

**Modul:** `app/routers/forum_helpers.py`

> Ovaj modul ne sadrži API rute — sastoji se isključivo od pomoćnih funkcija koje koriste `forum_topics.py` i `forum_comments.py`, izdvojenih u zaseban modul radi izbjegavanja kružnog importa (circular import) između ta dva fajla.

| Funkcija                                  | Opis                                                                       |
| -------------------------------------------- | ----------------------------------------------------------------------------- |
| `get_author_data(db, user_id)`                | Vraća osnovne podatke o autoru (`id`, `full_name`)                       |
| `get_category_data(db, category_id)`          | Vraća podatke o kategoriji (`id`, `name`, `color`); fallback ako ne postoji |
| `get_topic_tags(db, topic_id)`                | Vraća listu naziva tagova povezanih sa temom                              |
| `get_comment_votes_count(db, comment_id)`      | Vraća zbir vrijednosti glasova na komentaru                               |
| `get_comment_likes_count(db, comment_id)`      | Vraća broj lajkova komentara                                               |
| `get_comment_dislikes_count(db, comment_id)`   | Vraća broj dislajkova komentara                                            |
| `get_comments_count(db, topic_id)`             | Vraća broj neobrisanih komentara na temi                                   |
| `has_best_answer(db, topic_id)`                | Provjerava da li tema ima označen najbolji odgovor                        |
| `get_topic_votes_count(db, topic_id)`          | Vraća zbir glasova svih komentara na temi                                  |
| `get_topic_comments(db, topic_id)`             | Vraća listu komentara teme (ravna lista, sortirana po najboljem odgovoru i broju glasova) |

---

### Forum Guidelines (Smjernice foruma)

**Base URL:** `/forum/guidelines`  
**Tag:** `Forum Guidelines`

---

| Metoda   | Putanja                          | Opis                          | Pristup |
| -------- | ----------------------------------- | -------------------------------- | ------- |
| `GET`    | `/forum/guidelines/`                | Lista svih smjernica            | Javno   |
| `POST`   | `/forum/guidelines/`                | Kreiranje nove smjernice         | Admin   |
| `PATCH`  | `/forum/guidelines/{guideline_id}`  | Ažuriranje smjernice             | Admin   |
| `DELETE` | `/forum/guidelines/{guideline_id}`  | Brisanje smjernice               | Admin   |

---

#### `GET /forum/guidelines/`

Vraća sve smjernice foruma, sortirane po polju `order` (rastuće), a zatim po `id`.

- **Autentifikacija:** Nije potrebna
- **Response:** `List[{ id, title, content, order, created_at, updated_at }]`

---

#### `POST /forum/guidelines/`

Kreira novu smjernicu. Isključivo za administratore.

- **Autentifikacija:** Admin JWT token
- **Body:** `GuidelineCreate`
  - `title` (str, 3–200 karaktera)
  - `content` (str, min 3 karaktera)
  - `order` (int, opciono, default `0`)
- **Response:** `ForumGuideline` — `201 Created`
- **Greške:**
  - `403` — akter nije admin

---

#### `PATCH /forum/guidelines/{guideline_id}`

Parcijalno ažurira smjernicu — šalju se samo polja koja se mijenjaju. Isključivo za administratore.

- **Autentifikacija:** Admin JWT token
- **Path parametri:** `guideline_id` (int)
- **Body:** `GuidelineUpdate` (parcijalno)
  - `title` (str, opciono, 3–200 karaktera)
  - `content` (str, opciono, min 3 karaktera)
  - `order` (int, opciono)
- **Response:** `ForumGuideline`
- **Greške:**
  - `403` — akter nije admin
  - `404` — smjernica nije pronađena

---

#### `DELETE /forum/guidelines/{guideline_id}`

Trajno briše smjernicu. Isključivo za administratore.

- **Autentifikacija:** Admin JWT token
- **Path parametri:** `guideline_id` (int)
- **Response:** `{ "success": true, "message": "Smjernica je obrisana." }`
- **Greške:**
  - `403` — akter nije admin
  - `404` — smjernica nije pronađena

---

### Forum Attachments (Prilozi na forumu)

**Base URL:** `/forum/attachments`  
**Tag:** `Forum Attachments`

> Dozvoljeni formati: `.jpg`, `.jpeg`, `.png`, `.pdf`, `.docx`, `.txt`. Maksimalna veličina fajla: **5 MB**. Maksimalan broj fajlova po temi/komentaru: **3**.

---

| Metoda | Putanja                                              | Opis                                  | Pristup  |
| ------ | ------------------------------------------------------- | ---------------------------------------- | -------- |
| `POST` | `/forum/attachments/topic/{topic_id}`                   | Upload priloga na temu                  | Korisnik |
| `GET`  | `/forum/attachments/topic/{topic_id}`                   | Lista priloga teme                      | Javno    |
| `GET`  | `/forum/attachments/topic/{topic_id}/download/{attachment_id}` | Preuzimanje priloga teme         | Javno    |
| `POST` | `/forum/attachments/comment/{comment_id}`               | Upload priloga na komentar              | Korisnik |
| `GET`  | `/forum/attachments/comment/{comment_id}`               | Lista priloga komentara                 | Javno    |
| `GET`  | `/forum/attachments/comment/{comment_id}/download/{attachment_id}` | Preuzimanje priloga komentara | Javno    |

---

#### `POST /forum/attachments/topic/{topic_id}`

Upload jednog ili više fajlova kao priloga teme. Fajlovi se čuvaju na disku (`uploads/forum/topics/`) sa jedinstvenim nazivom (`{topic_id}_{timestamp}_{original_filename}`).

- **Autentifikacija:** Korisnik JWT token
- **Path parametri:** `topic_id` (int)
- **Body:** `multipart/form-data` — `files: List[UploadFile]`
- **Response:** `{ "uploaded": List[{ id, filename, file_size }] }` — `201 Created`
- **Greške:**
  - `404` — tema nije pronađena ili je obrisana
  - `400` — prekoračen maksimalan broj fajlova po temi (3)
  - `400` — format fajla nije dozvoljen
  - `400` — fajl prelazi maksimalnu veličinu (5 MB)

---

#### `GET /forum/attachments/topic/{topic_id}`

Vraća listu priloga vezanih za temu.

- **Autentifikacija:** Nije potrebna
- **Path parametri:** `topic_id` (int)
- **Response:** `List[{ id, filename, file_size, mime_type }]`

---

#### `GET /forum/attachments/topic/{topic_id}/download/{attachment_id}`

Preuzima fajl priloga teme sa servera.

- **Autentifikacija:** Nije potrebna
- **Path parametri:** `topic_id` (int), `attachment_id` (int)
- **Response:** `FileResponse` (binarni sadržaj fajla)
- **Greške:**
  - `404` — prilog nije pronađen, ne pripada navedenoj temi, ili fajl ne postoji na serveru

---

#### `POST /forum/attachments/comment/{comment_id}`

Upload jednog ili više fajlova kao priloga komentara. Fajlovi se čuvaju na disku (`uploads/forum/comments/`) sa jedinstvenim nazivom (`{comment_id}_{timestamp}_{original_filename}`).

- **Autentifikacija:** Korisnik JWT token
- **Path parametri:** `comment_id` (int)
- **Body:** `multipart/form-data` — `files: List[UploadFile]`
- **Response:** `{ "uploaded": List[{ id, filename, file_size }] }` — `201 Created`
- **Greške:**
  - `404` — komentar nije pronađen ili je obrisan
  - `400` — prekoračen maksimalan broj fajlova po komentaru (3)
  - `400` — format fajla nije dozvoljen
  - `400` — fajl prelazi maksimalnu veličinu (5 MB)

---

#### `GET /forum/attachments/comment/{comment_id}`

Vraća listu priloga vezanih za komentar.

- **Autentifikacija:** Nije potrebna
- **Path parametri:** `comment_id` (int)
- **Response:** `List[{ id, filename, file_size, mime_type }]`

---

#### `GET /forum/attachments/comment/{comment_id}/download/{attachment_id}`

Preuzima fajl priloga komentara sa servera.

- **Autentifikacija:** Nije potrebna
- **Path parametri:** `comment_id` (int), `attachment_id` (int)
- **Response:** `FileResponse` (binarni sadržaj fajla)
- **Greške:**
  - `404` — prilog nije pronađen, ne pripada navedenom komentaru, ili fajl ne postoji na serveru

---

### Forum Admin (Administracija foruma)

**Base URL:** `/forum/admin`  
**Tag:** `Forum Admin`

> Sve rute zahtijevaju administratorsku ulogu kroz `get_current_admin` dependency, koji baca `403` ako akter nije admin.

---

| Metoda   | Putanja                                       | Opis                                          | Pristup |
| -------- | ------------------------------------------------ | ------------------------------------------------ | ------- |
| `GET`    | `/forum/admin/users`                             | Lista svih korisnika                             | Admin   |
| `PATCH`  | `/forum/admin/users/{user_id}/role`              | Promjena uloge korisnika                         | Admin   |
| `GET`    | `/forum/admin/reports`                           | Lista prijava (filter po statusu)                | Admin   |
| `DELETE` | `/forum/admin/reports/{report_id}`               | Odbacivanje prijave (status → resolved)         | Admin   |
| `PATCH`  | `/forum/admin/reports/{report_id}/resolve`       | Rješavanje prijave (accept/dismiss)             | Admin   |
| `PATCH`  | `/forum/admin/reports/{report_id}/reopen`        | Ponovno otvaranje riješene prijave              | Admin   |
| `PATCH`  | `/forum/admin/topics/{topic_id}/lock`            | Zaključavanje/otključavanje teme                | Admin   |
| `POST`   | `/forum/admin/announcements`                     | Kreiranje globalnog obavještenja                | Admin   |
| `GET`    | `/forum/admin/announcements/all`                 | Lista svih obavještenja (uključujući neaktivna) | Admin   |
| `PATCH`  | `/forum/admin/announcements/{ann_id}`            | Ažuriranje obavještenja                          | Admin   |
| `DELETE` | `/forum/admin/announcements/{ann_id}`            | Deaktiviranje obavještenja                       | Admin   |
| `POST`   | `/forum/admin/topics/{topic_id}/pull-to-reports` | Admin ručno povlači temu u prijave              | Admin   |

---

#### `GET /forum/admin/users`

Vraća listu svih korisnika u sistemu.

- **Autentifikacija:** Admin JWT token
- **Response:** `List[{ id, email, full_name, role }]`
- **Greške:**
  - `403` — akter nije admin

---

#### `PATCH /forum/admin/users/{user_id}/role`

Mijenja ulogu korisnika.

- **Autentifikacija:** Admin JWT token
- **Path parametri:** `user_id` (int)
- **Query parametri:** `role` (str) — mora odgovarati jednoj od vrijednosti enum-a `UserRole`
- **Response:** `{ "message": "Uloga promijenjena u {role}" }`
- **Greške:**
  - `403` — akter nije admin
  - `400` — nevažeća uloga
  - `404` — korisnik nije pronađen

---

#### `GET /forum/admin/reports`

Vraća listu prijava filtriranih po statusu, sa podacima o pripadajućoj temi.

- **Autentifikacija:** Admin JWT token
- **Query parametri:** `status` (str, default `"pending"`) — `"pending"` ili `"resolved"`
- **Response:** `List[{ id, report_id, reason, created_at, status, action_taken, admin_explanation, topic: { id, title, content } }]`
- **Greške:**
  - `403` — akter nije admin
  - `400` — nevažeći status

---

#### `DELETE /forum/admin/reports/{report_id}`

Odbacuje prijavu postavljanjem statusa na `"resolved"` (bez postavljanja `action_taken`/`admin_explanation`).

- **Autentifikacija:** Admin JWT token
- **Path parametri:** `report_id` (int)
- **Response:** `{ "success": true }`
- **Greške:**
  - `403` — akter nije admin

---

#### `PATCH /forum/admin/reports/{report_id}/resolve`

Rješava prijavu sa akcijom i objašnjenjem. Ako je akcija `"accept"`, prijavljena tema se soft-briše (`is_deleted = True`).

- **Autentifikacija:** Admin JWT token
- **Path parametri:** `report_id` (int)
- **Body:** `{ "action": "accept" | "dismiss", "explanation": str }`
- **Response:** `{ "success": true }`
- **Greške:**
  - `403` — akter nije admin
  - `404` — prijava nije pronađena
  - `400` — prijava je već riješena
  - `400` — nevažeća akcija

---

#### `PATCH /forum/admin/reports/{report_id}/reopen`

Ponovo otvara riješenu prijavu (status → `"pending"`, briše `action_taken` i `admin_explanation`). Ako je pripadajuća tema bila obrisana zbog te prijave, vraća se (`is_deleted = False`).

- **Autentifikacija:** Admin JWT token
- **Path parametri:** `report_id` (int)
- **Response:** `{ "success": true, "report_id": int }`
- **Greške:**
  - `403` — akter nije admin
  - `404` — prijava nije pronađena
  - `400` — prijava je već aktivna (status `"pending"`)

---

#### `PATCH /forum/admin/topics/{topic_id}/lock`

Mijenja status zaključanosti teme (toggle).

- **Autentifikacija:** Admin JWT token
- **Path parametri:** `topic_id` (int)
- **Response:** `{ "is_locked": bool }`
- **Greške:**
  - `403` — akter nije admin
  - `404` — tema nije pronađena

---

#### `POST /forum/admin/announcements`

Kreira novo globalno obavještenje. Sva prethodno aktivna obavještenja se automatski deaktiviraju (samo jedno može biti aktivno u datom trenutku).

- **Autentifikacija:** Admin JWT token
- **Body:** `{ "title": str, "content": str, "duration_days": int }` — `duration_days <= 0` znači da obavještenje ne ističe
- **Response:** `{ "success": true, "announcement": AdminAnnouncement }`
- **Greške:**
  - `403` — akter nije admin

---

#### `GET /forum/admin/announcements/all`

Vraća sva obavještenja (aktivna, neaktivna i istekla), sortirano po datumu kreiranja (najnovije prvo).

- **Autentifikacija:** Admin JWT token
- **Response:** `List[AdminAnnouncement]`
- **Greške:**
  - `403` — akter nije admin

---

#### `PATCH /forum/admin/announcements/{ann_id}`

Parcijalno ažurira obavještenje — šalju se samo polja koja se mijenjaju. Postavljanje `duration_days <= 0` ili izostavljanje uklanja datum isteka (obavještenje postaje beskonačno).

- **Autentifikacija:** Admin JWT token
- **Path parametri:** `ann_id` (int)
- **Body:** `{ "title"?: str, "content"?: str, "duration_days"?: int, "is_active"?: bool }`
- **Response:** `{ "success": true, "announcement": AdminAnnouncement }`
- **Greške:**
  - `403` — akter nije admin
  - `404` — obavještenje nije pronađeno

---

#### `DELETE /forum/admin/announcements/{ann_id}`

Deaktivira obavještenje (`is_active = False`), ne briše ga trajno iz baze.

- **Autentifikacija:** Admin JWT token
- **Path parametri:** `ann_id` (int)
- **Response:** `{ "success": true }`
- **Greške:**
  - `403` — akter nije admin

---

#### `POST /forum/admin/topics/{topic_id}/pull-to-reports`

Omogućava administratoru da ručno povuče temu u sistem prijava na pregled (bez čekanja na korisničku prijavu), kreiranjem nove prijave u njegovo ime.

- **Autentifikacija:** Admin JWT token
- **Path parametri:** `topic_id` (int)
- **Response:** `{ "success": true, "report_id": int }` — `201 Created`
- **Greške:**
  - `403` — akter nije admin
  - `404` — tema nije pronađena ili je obrisana
  - `400` — tema već ima aktivnu (pending) prijavu

---

### Forum Categories (Kategorije foruma)

**Base URL:** `/forum/categories`  
**Tag:** `Forum Categories`

---

| Metoda | Putanja              | Opis                                         | Pristup |
| ------ | ---------------------- | ----------------------------------------------- | ------- |
| `GET`  | `/forum/categories/`    | Lista kategorija sa brojem tema po kategoriji   | Javno   |

---

#### `GET /forum/categories/`

Vraća sve kategorije foruma sa brojem neobrisanih tema u svakoj.

- **Autentifikacija:** Nije potrebna
- **Response:** `List[{ id, name, color, description, topic_count }]`

---

#### Helper funkcije (interno, nisu izložene kao rute)

| Funkcija                              | Opis                                                                 |
| ---------------------------------------- | ------------------------------------------------------------------------- |
| `get_category_data(db, category_id)`      | Vraća podatke o kategoriji (`id`, `name`, `color`); fallback "Bez kategorije" ako ne postoji |

---

# Forum Services

---

## Forum Notification Service

**Fajl:** `app/services/forum_notification.py`

Servis za kreiranje i upravljanje notifikacijama unutar foruma, uključujući detekciju @mention-a u tekstu.

---

### Konstante i regex

| Konstanta | Vrijednost | Opis |
|-----------|-----------|------|
| `MENTION_REGEX` | `(?<!\w)@([A-Za-z0-9_.-]{2,80})` | Regex za detekciju @username mention-a u tekstu |

---

### Funkcije

---

#### `get_user_display_name(user: User) -> str`

Vraća ime korisnika za prikaz u notifikacijama.

- **Prioritet:** `full_name` → `username` → `"Kolega"` (fallback)
- **Povratna vrijednost:** `str`

---

#### `extract_mentions(text: str) -> Set[str]`

Pronalazi sve @mention-e u tekstu i vraća ih kao skup lowercased stringova.

- **Parametri:** `text` — tekst u kojem se traže mention-i
- **Povratna vrijednost:** `Set[str]` — skup korisničkih imena (bez `@`, lowercase)
- **Napomena:** Ako je `text` prazan ili `None`, vraća prazan skup

---

#### `create_forum_notification(...) -> Optional[ForumNotification]`

Kreira novu forum notifikaciju i dodaje je u trenutnu transakciju. **Ne poziva `commit`** — to radi endpoint koji ga poziva.

| Parametar | Tip | Opis |
|-----------|-----|------|
| `db` | `Session` | SQLModel sesija |
| `recipient_user_id` | `int` | ID korisnika koji prima notifikaciju |
| `actor_user_id` | `int` | ID korisnika koji je inicirao akciju |
| `topic_id` | `int` | ID teme vezane za notifikaciju |
| `notification_type` | `ForumNotificationType` | Tip notifikacije (enum) |
| `text` | `str` | Tekst notifikacije |
| `comment_id` | `Optional[int]` | ID komentara (opcionalno) |
| `prevent_duplicate` | `bool` | Ako je `True`, provjeri da li ista notifikacija već postoji |

- **Povratna vrijednost:** `ForumNotification` ili `None`
- **Vraća `None` ako:**
  - korisnik pokušava notificirati samog sebe (`recipient_user_id == actor_user_id`)
  - `prevent_duplicate=True` i identična notifikacija već postoji i nije skrivena

---

#### `hide_forum_notification(...) -> None`

Sakriva (soft-delete) notifikacije koje odgovaraju zadanim filterima postavljanjem `is_hidden = True`.

| Parametar | Tip | Opis |
|-----------|-----|------|
| `db` | `Session` | SQLModel sesija |
| `recipient_user_id` | `int` | ID primaoca |
| `actor_user_id` | `int` | ID aktera |
| `topic_id` | `int` | ID teme |
| `notification_type` | `ForumNotificationType` | Tip notifikacije |
| `comment_id` | `Optional[int]` | ID komentara (opcionalno) |
| `only_unread` | `bool` | Ako je `True`, sakriva samo nepročitane notifikacije |

- **Povratna vrijednost:** `None`
- **Napomena:** Funkcija ne poziva `commit` — to radi endpoint koji je poziva

---

#### `notify_mentions(db, text, actor_user, topic, comment_id, old_text) -> None`

Pronalazi nove @mention-e u tekstu i šalje notifikacije pogođenim korisnicima.

| Parametar | Tip | Opis |
|-----------|-----|------|
| `db` | `Session` | SQLModel sesija |
| `text` | `str` | Novi tekst (tema ili komentar) |
| `actor_user` | `User` | Korisnik koji je napravio izmjenu |
| `topic` | `ForumTopic` | Tema u kojoj se mention pojavljuje |
| `comment_id` | `Optional[int]` | ID komentara ako mention dolazi iz komentara |
| `old_text` | `Optional[str]` | Prethodni tekst — mention-i koji su već bili u njemu se ne šalju ponovo |

- **Povratna vrijednost:** `None`
- **Logika:** Šalju se notifikacije samo za `new_mentions - old_mentions` (novi mention-i koji ranije nisu bili prisutni)
- **Korisničko ime:** Izvlači se iz e-mail adrese korisnika (dio ispred `@`). Npr. `ima.osm@gmail.com` → mention je `@ima.osm`
- **Anti-duplikat:** Svaki mention šalje se s `prevent_duplicate=True` — isti mention neće biti poslan dva puta

---

---

## Forum Reputation Service

**Fajl:** `app/services/forum_reputation.py`

Servis za upravljanje reputacijom korisnika na forumu — dodjela i oduzimanje bodova, nivoi, medalje i anti-abuse zaštita.

---

### Konfiguracija

#### Timezone

```python
SARAJEVO_TIMEZONE = ZoneInfo("Europe/Sarajevo")
```

Koristi se za određivanje lokalnog vremena pri provjeri noćnih tema.

---

#### Nivoi i titule (`LEVEL_RULES`)

| Nivo | Min. bodova | Titula |
|------|------------|--------|
| 1 | 0 | Novi član |
| 2 | 101 | Aktivni član |
| 3 | 251 | Poznavalac |
| 4 | 501 | Mentor zajednice |
| 5 | 1001 | Legenda foruma |

---

#### Medalje (`MEDAL_RULES`)

| Kategorija | Bronze | Silver | Gold |
|------------|--------|--------|------|
| `best_answers` | 1 | 5 | 15 |
| `topics_started` | 3 | 10 | 25 |
| `reputation` | 100 | 500 | 1000 |
| `night_owl` | 1 | 3 | 10 |

> Medalja `night_owl` je tajna (`is_secret=True`) i ne prikazuje se korisniku dok je ne osvoji.

---

### Pomoćne funkcije

---

#### `get_level_info(points: int) -> dict`

Vraća nivo i titulu korisnika na osnovu broja bodova.

- **Povratna vrijednost:** `{ "level": int, "title": str }`
- **Napomena:** Negativni bodovi tretiraju se kao `0`

---

#### `get_role_label(role) -> str`

Prevodi internu ulogu korisnika u prikazni label.

| Interna uloga | Label |
|--------------|-------|
| `member`, `student` | Student |
| `mentor`, `author` | Autor |
| `admin` | Admin |

---

#### `get_or_create_stats(db, user_id) -> ForumUserStats`

Dohvata ili kreira `ForumUserStats` zapis za korisnika. Poziva `db.flush()` pri kreiranju.

---

#### `reputation_event_exists(db, event_key) -> bool`

Provjerava da li je reputacijski događaj s datim `event_key` već registrovan (idempotentnost).

---

#### `award_eligible_medals(db, stats) -> None`

Provjeri da li korisnik ispunjava uvjete za novu medalju i dodijeli je ako je još nema. Poziva se automatski nakon svake izmjene `ForumUserStats`.

---

#### `is_night_topic(created_at) -> bool`

Provjerava je li tema kreirana između **03:00 i 05:00** po sarajevskom vremenu.

- **Povratna vrijednost:** `bool`
- **Napomena:** Ako `created_at` nije zadano, koristi trenutno UTC vrijeme

---

### Glavna funkcija

---

#### `register_activity(db, *, user_id, event_key, points_delta, reason, source_type, source_id, counters, giver_id) -> ForumUserStats`

Centralna funkcija za sve dodjele i oduzimanja bodova. Sadrži anti-abuse zaštite.

| Parametar | Tip | Opis |
|-----------|-----|------|
| `db` | `Session` | SQLModel sesija |
| `user_id` | `int` | ID korisnika koji prima bodove |
| `event_key` | `str` | Jedinstveni ključ događaja (idempotentnost) |
| `points_delta` | `int` | Pozitivan ili negativan broj bodova |
| `reason` | `str` | Opis razloga dodjele |
| `source_type` | `Optional[str]` | Tip izvora (`"forum_topic"`, `"forum_comment"`) |
| `source_id` | `Optional[int]` | ID izvora |
| `counters` | `Optional[dict[str, int]]` | Brojači na `ForumUserStats` koje treba ažurirati (npr. `{"answers_count": 1}`) |
| `giver_id` | `Optional[int]` | ID korisnika koji inicira dodjelu bodova |

**Anti-abuse zaštite:**

1. **Idempotentnost** — ako `event_key` već postoji u bazi, funkcija odmah vraća trenutni `stats` bez ikakvih izmjena.
2. **Vlastiti sadržaj** — ako je `giver_id == user_id`, `points_delta` se postavlja na `0` (bodovi se ne dodjeljuju, ali se `counters` i dalje ažuriraju).
3. **Dnevni limit** — jedan korisnik može prenijeti maksimalno **+30 bodova** drugom korisniku u periodu od 24 sata. Ako je limit prekoračen, bodovi se proporcionalno reduciraju ili u potpunosti odbijaju. Svaki prenos koji prođe filter bilježi se u `ForumReputationDailyLog`.

- **Povratna vrijednost:** `ForumUserStats`
- **Napomena:** Automatski poziva `award_eligible_medals()` i `db.flush()` na kraju

---

### Registracija specifičnih aktivnosti

---

#### `register_topic_created(db, *, user_id, topic_id, created_at) -> ForumUserStats`

Dodjeljuje **+10 bodova** za kreiranje teme. Ako je tema kreirana između 03:00–05:00 po sarajevskom vremenu, uvećava i `night_topics_count`.

- **Uvijek koristi `giver_id=0`** (sistem, bez anti-abuse provjere per-giver)

---

#### `register_answer_created(db, *, user_id, comment_id) -> ForumUserStats`

Dodjeljuje **+3 boda** za pisanje odgovora na forumu. Uvećava `answers_count`.

---

#### `register_best_answer(db, *, user_id, giver_id, comment_id) -> ForumUserStats`

Dodjeljuje **+25 bodova** za odgovor označen kao najbolji. Uvećava `best_answers_count`.

- **`giver_id`** je autor teme — ako označi vlastiti komentar kao najbolji, bodovi se poništavaju (anti-abuse)

---

#### `remove_reputation_points(db, *, user_id, event_key, points, reason, source_type, source_id) -> ForumUserStats`

Oduzima bodove korisniku (npr. brisanje sadržaja). Interna omotač za `register_activity` s negativnim `points_delta`.

---

#### `register_comment_vote(db, *, user_id, giver_id, comment_id, vote_value) -> ForumUserStats`

Registruje lajk ili dislajk na komentar.

| `vote_value` | Bodovi | Razlog |
|-------------|--------|--------|
| `1` (lajk) | +5 | Dobijen lajk na komentar |
| `-1` (dislajk) | -2 | Dobijen dislajk na komentar |

- Podliježe svim anti-abuse zaštitama (vlastiti glas, dnevni limit)

---

#### `rollback_comment_vote(db, *, user_id, giver_id, comment_id, previous_value) -> ForumUserStats`

Poništava prethodni glas kada korisnik klikne ponovo na istu opciju (toggle ponašanje).

| `previous_value` | Rollback delta |
|-----------------|---------------|
| `1` (lajk) | -5 |
| `-1` (dislajk) | +2 |

- Koristi `giver_id=0` — ne bilježi se u dnevni limit (rollback je neutralna operacija)
- `event_key` sadrži timestamp kako bi bio jedinstven i prošao idempotentnost provjeru

---

### Frontend helper

---

#### `get_user_forum_identity(db, user) -> dict`

Vraća sve podatke potrebne frontendu za prikaz profila korisnika na forumu.

**Povratna vrijednost:**

```json
{
  "role": "Student | Autor | Admin",
  "level": 1,
  "title": "Novi član",
  "reputation_points": 120,
  "medals": [
    {
      "code": "topics_started_bronze",
      "category": "topics_started",
      "category_name": "Pokrenute teme",
      "tier": "bronze",
      "tier_name": "Bronzana",
      "icon_key": "topics_started_bronze",
      "is_secret": false,
      "awarded_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```
