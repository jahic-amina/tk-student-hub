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

### Tim 2 — Materijali (Amer Imamović) — Frontend

#### Pregled

Ova dokumentacija opisuje frontend implementaciju koju je radio Amer Imamović u okviru Tim 2 — modul Materijali. Implementacija obuhvata brisanje materijala, toggle bookmark (omiljeni materijali) s vizuelnom povratnom informacijom, te kompletan filter sistem za pretragu materijala po godini studija, tipu materijala i predmetu.

Kod se nalazi u `frontend/src/views/materials/` i `frontend/src/components/`.

---

#### Sprint 1 — Brisanje materijala

**`DeleteMaterialButton.vue`**

Dugme za brisanje dostupno je samo autoru materijala ili administratoru. Komponenta provjerava:
- JWT token iz `localStorage`
- Korisničke podatke (`user` objekt ili `user_id`)
- Ulogu korisnika (`admin`, ili je autor)

Logika autorizacije:
```javascript
const mozeBrisati = computed(() => {
  if (!token || !currentUser) return false
  if (currentUser.role === 'admin' || currentUser.is_admin === true) return true
  if (currentUser.id === material.user_id) return true
  return false
})
```

**Prikaz brisanja:**
1. Dugme se prikazuje kao `<button>` s crvenom pozadinom (bg-red-100) i trash ikonom
2. Klik otvara `ConfirmModal` - "Potvrda brisanja: Da li ste sigurni da želite obrisati ovaj materijal?"
3. Nakon potvrde šalje se `DELETE /materials/{id}` zahtjev
4. Ako je uspješan (`204 No Content`) — materijal se uklanja iz liste
5. Ako je greška (`403 Forbidden`) — prikazuje se poruka "Nemate dozvolu za brisanje ovog materijala."

**API funkcija:**
- `deleteMaterial(materialId)` — briše materijal, zahtijeva JWT

---

#### Sprint 2 — Bookmark (Omiljeni materijali)

**Toggle bookmark dugme** — Zastavica (`MaterialCard.vue`)

Zastavica se prikazuje u gornjem desnom uglu `MaterialCard` komponente (osim za admin korisnike). Vizuelni izgled:
- **Narandžasta** (`bg-amber-400`) kada je materijal bookmarkovana — `is_bookmarked: true`
- **Siva** (`bg-gray-200`) kada nije bookmarkovana — `is_bookmarked: false`
- **Hover efekt** — Za sivu zastavicu postoji `hover:bg-gray-300` efekt

```vue
<button 
  v-if="userRole !== 'admin'"
  @click.stop="$emit('toggle-bookmark', material.id)"
>
  <div :class="[
    'w-8 h-10 transition-all duration-300',
    material.is_bookmarked ? 'bg-amber-400 shadow-md' : 'bg-gray-200 hover:bg-gray-300'
  ]">
    <!-- SVG ikona zastavice -->
  </div>
</button>
```

**Logika toggle bookmark-a** (`MaterialList.vue`):

```javascript
async function handleToggleBookmark(materialId) {
  try {
    const res = await toggleBookmark(materialId);
    const material = materials.value.find(m => m.id === materialId);
    if (material) {
      material.is_bookmarked = res.is_bookmarked;  // Ažurira state
    }
  } catch (error) {
    console.error("Greška kod bookmarka:", error);
  }
}
```

**Ključne napomene:**
- Klik na zastavicu odmah vizuelno ažurira boju (bez čekanja na backend)
- Materijal ostaje u listi čak i ako se togglea bookmark stanje
- `is_bookmarked` svojstvo dolazi iz backend API-ja pri učitavanju liste
- Tab "Najdraži materijali" filtrira samo materijale gdje je `is_bookmarked === true`

**API funkcija:**
- `toggleBookmark(materialId)` — toggle bookmark, vraća `{is_bookmarked: boolean}`

---

#### Sprint 3 — Filteri (Godina, Tip, Predmet)

**`MaterialFilter.vue`** — Sidebar komponenta s filterima

Prikazuje se samo na veličinama ekrana `md` i većim (`hidden md:block`). Komponenta je organizirana u tri sekcije:

**1. Filtriranje po godini studija**
```vue
<input type="checkbox" :value="year" v-model="filters.years">
```
Korisniku se prikazuje izbor godina 1-4. Odabrane godine se čuvaju u nizu `filters.years`.

**2. Filtriranje po tipu materijala**
```javascript
const typesMap = {
  'skripta': 'Skripte',
  'auditorne_vjezbe': 'Auditorne vježbe',
  'laboratorijske_vjezbe': 'Laboratorijske vježbe',
  'ispiti': 'Ispiti',
  'projekat': 'Projekat'
}
```
Prikazuje se checkbox za svaki tip. Odabrani tipovi se čuvaju u nizu `filters.types`.

**3. Filtriranje po predmetu**
```vue
<select v-model="filters.subject_id">
  <option :value="null">Svi predmeti</option>
  <option v-for="s in filteredSubjects" :key="s.id" :value="s.id">
    {{ s.name }}
  </option>
</select>
```
`<select>` dropdown je dinamički popunjen predmetima. Predmeti se prate po `study_year` — ako se odabere godinu 1, prikazuju se samo predmeti za godinu 1.

**Logika filtera:**
```javascript
const filteredSubjects = computed(() => {
  if (!filters.years.length) return subjects.value
  const selectedYears = filters.years.map(Number)
  return subjects.value.filter(subject => selectedYears.includes(Number(subject.study_year)))
})

watch(
  () => filters.years.slice(),
  () => {
    if (!filters.subject_id) return
    const isSelectedSubjectValid = filteredSubjects.value.some(
      subject => Number(subject.id) === Number(filters.subject_id)
    )
    if (!isSelectedSubjectValid) {
      filters.subject_id = null  // Reset ako predmet nije od odabrane godine
      update()
    }
  }
)
```

**Integracija filtera u `MaterialList.vue`:**

```vue
<MaterialFilter @change="handleFilterChange" />

async function handleFilterChange(newFilters) {
  trenutniFilteri.value = newFilters
  trenutnastranica.value = 1
  await loadMaterials(newFilters, 1);
}
```

Kada korisnik promijeni filter, komponenta emituje `@change` event s novim filterima. `MaterialList` tada poziva `loadMaterials()` s novim filterima i resetuje stranicu na 1.

**API pozivi s filterima:**

Backend prima filtere kao query parametare:
```
GET /materials/?years=1&years=2&types=skripta&subject_id=5&page=1
```

Parametri se prosleđuju kao:
```javascript
const params = new URLSearchParams();
if (filters.years?.length > 0) filters.years.forEach(y => params.append('years', y));
if (filters.types?.length > 0) filters.types.forEach(t => params.append('types', t));
if (filters.subject_id) params.append('subject_id', filters.subject_id);
```

**Napomena o autentifikaciji:** Za tab "Svi materijali" — ako je korisnik prijavljen, koristi se autorizirani endpoint `/materials/` koji vraća `is_bookmarked` stanje. Ako korisnik nije prijavljen, koristi se javni endpoint `/materials/public` (bez bookmark stanja).

---

