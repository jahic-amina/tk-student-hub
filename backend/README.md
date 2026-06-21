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

#### Migracije baze podataka

```bash
cd backend
source venv/bin/activate
alembic revision --autogenerate -m "opis promjene"
alembic upgrade head
```

U slučaju problema sa sinhronizacijom:
```bash
alembic stamp head
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
