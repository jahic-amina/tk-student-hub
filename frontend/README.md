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

## TIM 4 - detaljan opis funkcionalnosti

Tim 4 je zadužen za dio platforme koji svakom registrovanom studentu pruža vlastiti profil i personalizovan pregled platforme - dashboard. Frontend ovog modula omogućava studentu da pregleda i uređuje svoje osnovne podatke i biografiju, postavi, promijeni ili ukloni profilnu sliku, te promijeni lozinku - sve direktno sa svoje profilne stranice. Na istoj stranici student ima pregled svoje nedavne aktivnosti na platformi (objavljeni materijali, komentari na forumu, prihvaćene prijave na prakse) i pregled praksi na koje je trenutno prijavljen.
Korisnicima s administratorskom ulogom omogućen je poseban, zaštićen dio sučelja za pregled svih registrovanih korisnika platforme, sa mogućnošću pretrage po imenu ili emailu i filtriranja po ulozi i statusu naloga. Osim toga, omogućeno mu je mijenjanje uloge i statusa korisnika, te trajno brisanje profila. Također ima i prikaz statistike registrovanih korisnika. 

### Struktura foldera

```
frontend/src/
├── components/
│   ├── UserProfileCard.vue       - prikaz osnovnih podataka profila
│   ├── AvatarUploadModal.vue     - modal za upload/brisanje avatara
│   ├── ActivityFeed.vue          - lista nedavnih aktivnosti
│   └── NotificationBell.vue     - zvonce s padajućom listom notifikacija
├── views/
│   ├── profiles/
│   │   └── ProfileView.vue      - glavna stranica profila/dashboarda
│   └── admin/
│       └── AdminKorisniciView.vue      - pregled korisnika na platformi
└── services/
    └── api.js                   - sve funkcije za pozive prema backendu
```

### Princip rada

Backend je izvor za sve podatke - frontend ih samo prikazuje i šalje korisničke akcije nazad. Tok podataka za svaku funkcionalnost slijedi isti obrazac:

1. Korisnik otvori stranicu profila (`ProfileView.vue`)
2. Pri učitavanju (`onMounted`), frontend paralelno poziva backend endpointe: podaci profila, historija aktivnosti, lista praksi
3. Backend dohvata podatke iz baze, filtrirane prema identitetu korisnika iz JWT tokena
4. Frontend prima JSON odgovore i renderuje ih kroz odgovarajuće komponente

### Organizacija API poziva

Svi pozivi prema backendu centralizovani su u `services/api.js`, koji izvozi pojedinačne `async` funkcije za svaku operaciju (npr. `getMyProfile`, `uploadAvatar`, `removeAvatar`). Komponente pozivaju gotove funkcije bez poznavanja detalja URL-ova, headera ili formata zahtjeva.

---

## Profil korisnika

### `UserProfileCard.vue`

Prikazuje gornju karticu profila:
- Avatar (sliku ili inicijale ako slika ne postoji)
- Puno ime, rola, email, telefon, datum učlanjenja

Inicijali se generišu automatski iz punog imena korisnika (npr. "Amina Hodžić" → "AH") i prikazuju se kao zamjena za avatar kad slika nije postavljena. Klik na avatar otvara modal za upload slike.

### `ProfileView.vue` - stranica profila

Glavna stranica profila ima **dva stanja**, kontrolisana varijablom `isEditing`:

**Prikaz profila** (`isEditing = false`)
- Kartica s osnovnim podacima korisnika
- Sekcija **"O meni"** - prikazuje biografiju korisnika, ili placeholder "Nije unesena biografija." ako nije unesena
- Sekcija **"Trenutne prakse"**
- Sekcija **"Nedavna aktivnost"**

**Uređivanje profila** (`isEditing = true`)
- Forma za izmjenu ličnih podataka
- Forma za promjenu lozinke
- Opcija za deaktivaciju naloga

Pri otvaranju stranice, automatski se dohvataju podaci s backenda (`GET /profiles/me`). Dok traje dohvat, prikazuje se indikator učitavanja. Ako dohvat ne uspije, prikazuje se poruka greške.

Komunikacija s backendom za profil ide kroz:
- Axios instance s interceptor-om koji automatski dodaje `Authorization` header
- Direktne funkcije iz `services/api.js` (`getMyProfile`, `uploadAvatar`, `removeAvatar`)

---

## Upload i uklanjanje profilne slike

### `AvatarUploadModal.vue`

Modal koji se otvara klikom na avatar u `UserProfileCard`. Sadrži:
- Prikaz trenutne slike ili inicijala
- Dugme za odabir nove slike (file picker)
- Preview odabrane slike prije slanja
- Klijentsku validaciju tipa i veličine fajla (s porukom greške ako fajl ne zadovoljava uslove)
- Dugmad za potvrdu uploada i uklanjanje postojeće slike

Modal prima trenutnu sliku i inicijale korisnika kao props, te emituje evente `save` (s odabranim fajlom) i `remove` prema roditeljskoj komponenti, koja zatim poziva odgovarajuće backend funkcije.

### Tok uploada slike

1. Korisnik klikne na avatar → otvara se modal
2. Korisnik bira fajl → klijentska validacija (tip, veličina) → prikazuje se preview
3. Klik na "Sačuvaj" → fajl se šalje prema stranici profila
4. Stranica poziva funkciju za upload iz `api.js`
5. Fajl se šalje kao `multipart/form-data` na `POST /profiles/me/avatar`
6. Backend validira, sprema fajl i vraća novi URL slike
7. Frontend odmah ažurira prikaz bez osvježavanja stranice

### Tok uklanjanja slike

Isti princip — poziva se `DELETE /profiles/me/avatar` bez tijela zahtjeva. Backend briše fajl s diska, a frontend reaktivno vraća prikaz inicijala umjesto slike.

---

## Historija aktivnosti

### `ActivityFeed.vue`

Samostalna, ponovno upotrebljiva komponenta koja prima dva propsa: `activities` (lista aktivnosti) i `loading` (boolean). Odgovorna isključivo za prikaz — ne sadrži logiku dohvatanja podataka.

Funkcionalnosti:
- Za svaki tip aktivnosti mapira odgovarajuću ikonu, boju i opisni label (npr. `material_uploaded` → „Uploadovao materijal", plava ikona)
- Prikazuje naslov, podnaslov i relativno vrijeme aktivnosti
- Funkcija `formatRelativeTime()` pretvara UTC timestamp u čitljiv tekst: „Pre 5 minuta", „Pre 3 sata", „Pre 2 dana"
- Dok se podaci učitavaju, prikazuje skeleton loader (animirani sivi pravougaonici)
- Ako je lista prazna, prikazuje se poruka „Nema nedavne aktivnosti"

### Integracija u `ProfileView.vue`

Definirane su reaktivne varijable `activities`, `activityLoading`, `hasMore` i `showingAll`, te dvije funkcije za dohvatanje:

- `loadPreview()` — dohvata 3 najnovije aktivnosti, poziva se automatski pri učitavanju stranice
- `loadAll()` / `handleShowAll()` — dohvata do 20 aktivnosti, poziva se klikom na dugme „Prikaži sve"

---

## Trenutne prakse

U sekciji „Trenutne prakse" na profilu, lista dobijena s backenda iterira se i prikazuje:
- Naziv prakse
- Naziv kompanije
- Status (prevedeno u čitljiv tekst — „Prihvaćeno" ili „U toku")

Ako korisnik nema aktivnih prijava, prikazuje se odgovarajuća poruka „Nema trenutnih praksi."

---

## Sistem notifikacija

### `NotificationBell.vue`

Komponenta prikazuje:
- Ikonu zvona s brojem nepročitanih notifikacija (izračunato lokalno iz dohvaćene liste)
- Padajuću listu s mogućnošću označavanja pojedinih ili svih notifikacija kao pročitanih
- Opciju brisanja historije notifikacija

Komponenta prikazuje isključivo polje `notif.text` koje stiže gotovo s backenda, bez mapiranja po tipu notifikacije na frontendu. To znači da se novi tipovi notifikacija mogu dodavati samo kroz backend izmjene, bez potrebe za dodatnim frontend radom.

---

## Administratorski panel

Dostupno samo korisnicima s ulogom `admin`. Pruža mogućnost pregleda svih registrovanih korisnika platforme.

### Čuvanje uloge pri prijavi (`LoginView`)

Nakon prijave, uz token i korisničko ime, sprema se i uloga:

```javascript
localStorage.setItem('token', response.access_token)
const user = await getMe(response.access_token)
localStorage.setItem('username', user.full_name)
localStorage.setItem('role', user.role)
```

### Uslovni prikaz Admin linka (`NavBar`)

Admin link u navigaciji prikazuje se samo administratorima:

```javascript
computed: {
  isAdmin() {
    return this.role === 'admin'
  }
}
```

```html
<router-link v-if="isAdmin" to="/admin">Admin</router-link>
```

### Zaštićena ruta (`Router`)

```javascript
{
  path: '/admin',
  name: 'admin',
  component: () => import('../views/admin/AdminKorisniciView.vue'),
  meta: { requiresAuth: true, requiresAdmin: true }
}
```

Vue Router `beforeEach` guard provjerava token i ulogu korisnika prije svakog pristupa `/admin` ruti. Korisnici bez admin uloge se preusmjeravaju na početnu stranicu.

### `AdminKorisniciView.vue`

Stranica administratorskog pregleda korisnika:

- Prikaz liste korisnika (ime, email, uloga, status)
- Pretraga po imenu ili email adresi (u realnom vremenu)
- Filtriranje po ulozi (`member` / `admin`)
- Filtriranje po statusu naloga (aktivan / deaktiviran)
- Aktivacija/deaktivacija naloga (Uz ograničenje da administrator ne može sam sebi deaktivirati nalog u admin panelu)
- Promjena uloge naloga (Uz ograničenje da administrator ne može sam sebi promijeniti ulogu)
- Trajno brisanje naloga (Uz ograničenje da administrator ne može obrisati svoj nalog)
- Prikaz statistike registrovanih naloga

Pretraga i filteri pozivaju `fetchUsers()` pri svakoj promjeni, bez osvježavanja stranice.

### API servis za admin (`api.js`)

```javascript
export async function getAllUsers(token, { search = '', role = '', is_active = '' } = {}) {
  const params = new URLSearchParams()
  if (search) params.append('search', search)
  if (role) params.append('role', role)
  if (is_active !== '') params.append('is_active', is_active)

  const response = await fetch(`${BASE_URL}/admin/users?${params.toString()}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  return response.json()
}
```

---

## Komunikacija s backendom

### Tok podataka — pregled profila

1. Korisnik otvori stranicu `/profiles`
2. Stranica poziva `GET /profiles/me` s JWT tokenom
3. Backend vraća podatke prema `UserProfileResponse` shemi
4. Frontend sprema podatke u reaktivnu varijablu i prikazuje stranicu
5. Ako token nije validan, backend vraća `401` i frontend prikazuje grešku

### Format komunikacije

Sva komunikacija odvija se putem JSON formata. GET zahtjevi ne nose tijelo, dok POST/PATCH/DELETE zahtjevi nose JSON tijelo (ili `multipart/form-data` za upload fajlova).

### Rukovanje greškama i stanjima učitavanja

Svaka funkcija koja dohvata podatke prati vlastito stanje učitavanja kroz `ref` varijablu (npr. `activityLoading`), koja se koristi za prikaz skeleton loadera. Greške se hvataju kroz `try/catch` blokove i bilježe u konzolu.

---
## Sigurnost i zaštita ruta

Zaštita postoji na dva nivoa:

| Nivo | Mehanizam | Svrha |
|---|---|---|
| Router guard | `meta.requiresAdmin` + `beforeEach` | Sprječava navigaciju na `/admin` za ne-admin korisnike |
| NavBar | `v-if="isAdmin"` | Admin link se ne prikazuje korisnicima koji nisu admin |

> **Napomena:** Frontend zaštita je isključivo UX mjera — poboljšava korisničko iskustvo, ali ne predstavlja stvarnu sigurnost jer se frontend kod može zaobići. Stvarna sigurnosna granica je backend `require_admin` dependency koji se izvršava na svakom zahtjevu prema `/admin/*` rutama.

---

## Pregled API ruta

**Base URL (lokalni razvoj):**
- Backend: `http://127.0.0.1:8000`
- Frontend (Vite dev server): `http://localhost:5173`

| Metoda | Ruta | Auth | Opis |
|---|---|---|---|
| `GET` | `/profiles/me` | ✅ JWT | Dohvat podataka trenutnog korisnika |
| `PATCH` | `/profiles/me` | ✅ JWT | Ažuriranje tekstualnih podataka profila |
| `POST` | `/profiles/me/avatar` | ✅ JWT | Upload profilne slike (`multipart/form-data`, polje `file`) |
| `DELETE` | `/profiles/me/avatar` | ✅ JWT | Uklanjanje profilne slike |
| `GET` | `/uploads/{filename}` | ❌ | Statički pristup uploadanim slikama |
| `PATCH` | `/profiles/me/password` | ✅ JWT | Promjena lozinke |
| `GET` | `/api/users/me/activity` | ✅ JWT | Historija aktivnosti korisnika (`limit`, `offset`) |
| `GET` | `/applications/me/all` | ✅ JWT | Aktivne prijave na prakse trenutnog korisnika |
| `GET` | `/notifications/me` | ✅ JWT | Sve notifikacije korisnika |
| `GET` | `/notifications/unread-count` | ✅ JWT | Broj nepročitanih notifikacija |
| `POST` | `/notifications/read-all` | ✅ JWT | Označavanje svih notifikacija kao pročitanih |
| `GET` | `/admin/users` | ✅ JWT (admin) | Lista svih korisnika, uz filtere (samo admin) |
| `POST` | `/account/deactivate` | ✅ JWT | Deaktivacija vlastitog naloga |
| `PATCH` | `/admin/users/{user_id}/role` | ✅ JWT (admin) | Promjena uloge korisnika |
| `POST` | `/admin/users/{id}/deactivate` | ✅ JWT (admin) | Deaktivacija naloga od strane admina |
| `POST` | `/admin/users/{id}/activate` | ✅ JWT (admin) | Aktivacija naloga od strane admina |
| `DELETE` | `/admin/users/{user_id}` | ✅ JWT (admin) | Trajno brisanje naloga od strane admina |
| `GET` | `/admin/stats` | ✅ JWT (admin) | Generiše statistike o regitrovanim nalozima |



---