# TK Student Hub — Frontend

Frontend dio platforme TK Student Hub, izgrađen u Vue 3. Pruža korisničko sučelje za sve funkcionalnosti platforme - autentifikaciju, profile, materijale, forum, prakse i oglase te notifikacije.
Frontend je lokalizovan na bosanski jezik i rebrendiran za TK Student Hub.

## Tehnologije

- **Vue 3** — JavaScript framework (Composition API)
- **Vite** — build alat i razvojni server
- **Tailwind CSS** — utility-first CSS framework
- **Vue Router** — rutiranje unutar aplikacije
- **Axios / Fetch API** — komunikacija s backend API-jem

## Struktura projekta

```
frontend/
├── src/
│   ├── assets/            # Statički resursi (slike, fontovi)
│   ├── components/         # Reusable Vue komponente
│   ├── composables/         # Vue 3 composables (dijeljena logika)
│   ├── router/                # Konfiguracija ruta aplikacije
│   ├── services/                # API pozivi prema backendu
│   ├── views/                     # Stranice aplikacije, organizirane po modulima
│   ├── App.vue                     # Root komponenta
│   ├── main.js                      # Ulazna tačka aplikacije
│   └── style.css                     # Globalni stilovi
├── public/                              # Javni statički fajlovi
├── index.html
├── package.json
├── tailwind.config.js
└── vite.config.js
```

### Organizacija `views/` foldera

Stranice su organizirane po funkcionalnim modulima platforme:

```
views/
├── admin/          # Administratorski panel
├── ads/             # Oglasi za prakse i edukacije
├── application/      # Prijave na oglase
├── company/            # Profili kompanija
├── forum/               # Forum - teme i komentari
├── materials/             # Studijski materijali
├── prakse/                  # Prikaz praksi
├── profiles/                  # Korisnički profil i dashboard
└── workshops/                   # Radionice/edukacije
```

## Instalacija

```bash
cd frontend
npm install
```

## Pokretanje razvojnog servera

```bash
npm run dev
```

Aplikacija će biti dostupna na:

```
http://localhost:5173
```

## Povezivanje s backendom

Frontend komunicira s backend API-jem putem fajla `src/services/api.js`, gdje je definirana osnovna adresa backend servera:

```js
const BASE_URL = 'http://127.0.0.1:8000'
```

Backend mora biti pokrenut lokalno na portu `8000` da bi frontend mogao dohvatati podatke. 

Pogledajte `backend/README.md` za uputstvo o pokretanju backenda.

## Autentifikacija

Nakon uspješne prijave, JWT token se čuva u `localStorage` pod ključem `token` (za studente/administratore) ili `company_token` (za kompanije). Svaki API poziv koji zahtijeva autorizaciju šalje token u zaglavlju zahtjeva:

```
Authorization: Bearer <token>
```

Rute koje zahtijevaju prijavljenog korisnika označene su u `src/router/index.js` pomoću `meta: { requiresAuth: true }`.

## Stilizacija

Projekt koristi Tailwind CSS s prilagođenom bojom teme definiranom u `tailwind.config.js`:

| Boja | Heks kod | Upotreba |
|---|---|---|
| Primary | `#ff7a00` | Glavna narandžasta boja brenda |
| Secondary | `#ffb380` | Svjetlija varijanta, akcenti |

Podržan je i tamni način rada (dark mode) putem Tailwind `dark:` varijanti klasa.

## Funkcionalnosti po modulima

| Modul | Opis |
|---|---|
| `profiles` | Pregled i uređivanje korisničkog profila, upload profilne slike, historija aktivnosti, prikaz trenutnih praksi |
| `materials` | Pregled, upload, ocjenjivanje i komentarisanje studijskih materijala |
| `forum` | Forum teme, komentari, kategorije, glasanje |
| `ads` / `application` | Pregled oglasa za prakse, prijavljivanje, praćenje statusa prijave |
| `company` | Registracija i upravljanje profilom kompanije |
| `admin` | Administratorski panel za upravljanje korisnicima, oglasima i kompanijama |

## Napomena

Trenutno backend URL nije konfigurabilan putem environment varijabli - adresa je hardkodirana u `src/services/api.js`. 

## Dokumentacija modula

### Tim 2 — Materijali (Lejla Kadušić) — Frontend

#### Pregled

Ova dokumentacija opisuje frontend implementaciju koju je radila Lejla Kadušić u okviru Tim 2 — modul Materijali. Implementacija obuhvata dugme i kostur forme za upload materijala, kompletnu funkcionalnost komentara i paginacijsku navigaciju.

Kod se nalazi u `frontend/src/views/materials/` i `frontend/src/components/`.

---

#### Sprint 1 — Upload (dugme i kostur forme)

**Dugme `+ DODAJTE MATERIJAL`** (`MaterialUploadForm.vue`)

Dugme se prikazuje svim korisnicima osim adminu. Klik na dugme provjerava da li je korisnik prijavljen:
- Ako **nije prijavljen** → preusmjerava na `/login`
- Ako **jest prijavljen** → preusmjerava na `/materials/upload`

**Kostur forme i modal uspjeha**

Postavljen osnovni layout forme s prikazom poruke uspjeha kao modal (overlay s checkmark ikonom) nakon što backend potvrdi upload, te prikazom poruke greške u slučaju neuspjeha.

**`uploadMaterial()` u `api.js`**

Šalje `POST` zahtjev na `/materials/upload` s JWT tokenom iz `localStorage`.

---

#### Sprint 2 — Komentari (prikaz, dodavanje, brisanje)

**`CommentList.vue`**

Kontejner komponenta koja upravlja kompletnim stanjem komentara. Pri učitavanju stranice dohvaća komentare s backenda i prikazuje odgovarajući state:
- **Loading state** — prikazuje se dok se komentari učitavaju
- **Error state** — prikazuje se ako dohvaćanje ne uspije
- **Empty state** — "Još uvijek nema komentara. Budite prvi koji će ostaviti komentar."
- **Lista komentara** — `CommentCard` komponenta za svaki komentar

Upravljanje listom bez refresha stranice:
- Novi komentar se dodaje na vrh liste odmah nakon slanja
- Obrisani komentar se uklanja iz liste odmah nakon brisanja

**`CommentCard.vue`**

Prikazuje jedan komentar s imenom autora, relativnim vremenom i tekstom komentara.

Relativno vrijeme prikazuje se u čitljivom formatu:
- Manje od minute → "Upravo sada"
- Manje od sat vremena → "Prije N minuta"
- Manje od dan → "Prije N sati"
- Jedan dan → "Jučer"
- Manje od sedmice → "Prije N dana"
- Stariji komentari → standardni datum (DD.MM.YYYY)

Prikaz dugmadi ovisi o ulozi korisnika — podaci se čitaju iz JWT tokena u `localStorage`:
- Dugme **"Uredi"** vidljivo je samo autoru komentara
- Dugme **"Obriši"** vidljivo je autoru komentara i administratoru

Brisanje komentara otvara `ConfirmModal` za potvrdu. Nakon potvrde komentar se uklanja iz liste bez refresha. Prikazuje se kratka toast poruka o uspjehu ili grešci.

**Napomena — ispravka timezone buga:** Backend vraća UTC timestamp bez oznake vremenske zone, što je uzrokovalo pogrešan prikaz relativnog vremena. Ispravka je implementirana dodavanjem `Z` sufiksa na timestamp string prije parsiranja.

**`CommentForm.vue`**

- Neprijavljenom korisniku prikazuje se poruka s linkom za prijavu umjesto forme
- Prijavljenom korisniku prikazuje se `textarea` za unos komentara
- Ispod textarea prikazuje se brojač unesenih karaktera (max 500)
- Dugme "Objavi" onemogućeno je dok tekst nije validan (minimalno 1 karakter bez razmaka, maksimalno 500)
- Nakon uspješnog slanja forma se čisti i novi komentar se odmah pojavljuje na vrhu liste

**`ConfirmModal.vue`**

Generalna reusable komponenta za potvrdu destruktivnih akcija — može se koristiti na više mjesta u projektu. Prima naslov, poruku i dvije funkcije: jednu za potvrdu i jednu za odustajanje.

Zatvara se na tri načina:
- Klik na dugme "Odustani"
- Klik van modala
- Pritisak tipke `ESC`

**API funkcije (Sprint 2)**

- `getComments(materialId)` — dohvaća komentare, javni endpoint bez tokena
- `postComment(materialId, content)` — dodaje komentar, zahtijeva JWT
- `deleteComment(materialId, commentId)` — briše komentar, zahtijeva JWT

---

#### Sprint 3 — Uređivanje komentara i paginacija

**Uređivanje komentara (`CommentCard.vue`)**

Klikom na "Uredi" tekst komentara se zamjenjuje poljem za unos s postojećim sadržajem — inline uređivanje bez otvaranja novog prozora. Dugme "Spremi" onemogućeno je dok tekst nije validan. "Odustani" vraća originalni prikaz bez izmjena.

Nakon uspješnog uređivanja ispod teksta komentara prikazuje se oznaka "uređeno · datum i vrijeme izmjene" u sivom manjem fontu.

**Paginacija (`MaterialsView.vue`)**

Materijali su organizirani u tri taba s različitim tipovima paginacije:

| Tab | Tip paginacije | Opis |
|---|---|---|
| Svi | Server-side | Stranica po stranica s backenda |
| Moji materijali | Server-side | Stranica po stranica, samo vlastiti |
| Najdraži | Lokalna | Svi dohvaćeni odjednom, filtrira se po bookmarku |

Paginacijska navigacija prikazuje klikabilne brojeve stranica sa strelicama ← i →. Strelice su onemogućene na prvoj i zadnjoj stranici. Paginacija se resetuje na stranicu 1 pri promjeni filtera ili taba.

**API funkcije (Sprint 3)**

- `updateComment(materialId, commentId, content)` — uređuje komentar, zahtijeva JWT
- `getMaterials(filters, page, perPage)` — lista materijala s paginacijom, za prijavljene korisnike
- `getPublicMaterials(filters, page, perPage)` — lista materijala s paginacijom, javni endpoint

---

