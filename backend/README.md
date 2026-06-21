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

