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
const BASE_URL = "http://127.0.0.1:8000";
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

| Boja      | Heks kod  | Upotreba                       |
| --------- | --------- | ------------------------------ |
| Primary   | `#ff7a00` | Glavna narandžasta boja brenda |
| Secondary | `#ffb380` | Svjetlija varijanta, akcenti   |

Podržan je i tamni način rada (dark mode) putem Tailwind `dark:` varijanti klasa.

## Funkcionalnosti po modulima

| Modul                 | Opis                                                                                                           |
| --------------------- | -------------------------------------------------------------------------------------------------------------- |
| `profiles`            | Pregled i uređivanje korisničkog profila, upload profilne slike, historija aktivnosti, prikaz trenutnih praksi |
| `materials`           | Pregled, upload, ocjenjivanje i komentarisanje studijskih materijala                                           |
| `forum`               | Forum teme, komentari, kategorije, glasanje                                                                    |
| `ads` / `application` | Pregled oglasa za prakse, prijavljivanje, praćenje statusa prijave                                             |
| `company`             | Registracija i upravljanje profilom kompanije                                                                  |
| `admin`               | Administratorski panel za upravljanje korisnicima, oglasima i kompanijama                                      |

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
### Tim 2 — Materijali (Marinela Mitić)

#### Pregled

Ovaj dio dokumentacije opisuje frontend implementaciju koju je radila Marinela Mitić u okviru Tim 2 — modul Materijali. Implementacija obuhvata polja i validaciju forme za dodavanje materijala, preuzimanje materijala, ocjenjivanje (zvjezdice), prikaz thumbnail sličica i dorada izgleda detaljne kartice (ime predmeta, godina, tip) te dark mode stilizaciju svih komponenti modula.

Korištene tehnologije: **Vue 3** (Composition API i Options API), **Vue Router**, **Tailwind CSS**.

Relevantni fajlovi:
- `frontend/src/components/MaterialUploadForm.vue` — polja, validacija i drag&drop forme (dugme je rad kolegice)
- `frontend/src/components/DownloadButton.vue` — preuzimanje fajla
- `frontend/src/components/MaterialRating.vue` — ocjenjivanje zvjezdicama
- `frontend/src/views/materials/MaterialDetailView.vue` — prikaz thumbnaila i povezivanje preuzimanja s ocjenjivanjem
- `frontend/src/services/api.js` — API funkcije za komunikaciju s backendom

---

#### Sprint 1 — Forma (polja, validacija) i preuzimanje

##### `MaterialUploadForm.vue` — polja, validacija obaveznih polja i drag&drop

> **Podjela rada:** Dugme "+ DODAJTE MATERIJAL" i kostur forme rad su kolegice. Polja forme, validacija, drag&drop zona i slanje na backend su lično implementirani dio.

Forma za upload materijala s poljima: naziv, opis, tip materijala, godina studija, predmet i fajl.

**Validacija (`validateForm`)** se izvršava na strani klijenta prije slanja. U Sprintu 1 implementirana je provjera obaveznih polja — sva polja moraju biti popunjena, a prazna se označavaju crvenim okvirom:

| Polje | Pravilo (Sprint 1) |
|---|---|
| Naziv | Obavezno |
| Opis | Obavezno |
| Tip materijala | Obavezno |
| Godina studija | Obavezno |
| Predmet | Obavezno |
| Fajl | Obavezno |

Objekat `errors` koristi dvije vrste vrijednosti: `true` (polje je prazno — prikazuje se samo crveni okvir) i tekstualnu poruku (polje ima sadržaj ali je neispravan — prikazuje se okvir i poruka ispod). U templatu se poruka prikazuje samo kada vrijednost nije `true` (`errors.title !== true`). Detaljnija validacija dužine (minimalan broj karaktera) dodana je u Sprintu 3.

**Reaktivna validacija:** `watch` prati sva polja i ponovo pokreće validaciju čim korisnik počne ispravljati greške — ali tek nakon prvog pokušaja slanja, kako korisnik ne bi vidio greške prije nego što uopće pokuša poslati formu.

**Filtriranje predmeta:** `filteredSubjects` (`computed`) prikazuje samo predmete odabrane godine studija. Godina studija (`studyYear`) se ne šalje na backend — služi samo za sužavanje liste predmeta, jer je godina već vezana za predmet u bazi.

**Drag & drop:** Implementirana zona za prevlačenje fajla (`onFileDrop`, `triggerFileInput`, `onFileChange`). Stvarni `<input type="file">` je skriven (`class="hidden"`), a vidljiva drag zona programski pokreće njegov klik — čime se dobija prilagođen izgled umjesto stilski ograničenog nativnog inputa.

**Slanje (`handleSubmit`):** Kreira `FormData` (zbog `multipart/form-data` slanja fajla) i šalje na backend. Greške se mapiraju po HTTP statusu:

| Status | Poruka korisniku |
|---|---|
| `401` | Token istekao — korisnik se preusmjerava na login |
| `400` | Format fajla nije podržan |
| `409` | Materijal s tim nazivom/fajlom već postoji |

##### `DownloadButton.vue` — preuzimanje fajla (blob obrazac)

Komponenta koja preuzima fajl koristeći **blob download** obrazac. Kada korisnik klikne "PREUZMI":

1. Dugme se onemogućava (`isDownloading`) da spriječi dvostruki klik
2. Poziva se `downloadMaterial` (api.js) — šalje token kroz URL radi bilježenja preuzimanja
3. Provjerava se HTTP status (`403`, `404`) i mapira na korisničku poruku
4. Iz `Content-Disposition` zaglavlja se regexom izvlači originalni naziv fajla (sa `decodeURIComponent` za specijalne znakove), uz rezervni naziv `material-{id}`
5. Odgovor se pretvara u `blob`, kreira se privremeni objektni URL, pravi nevidljivi `<a download>` element koji se programski klikne — fajl se preuzima direktno na disk, bez otvaranja u browseru — te se memorija oslobađa s `revokeObjectURL`
6. Emituje se događaj `@downloaded` prema roditeljskoj komponenti

**Zašto blob umjesto običnog linka:** Direktan `<a href>` ne bi omogućio slanje tokena niti obradu grešaka (403/404) s prikazom poruke, niti bi garantovao da se fajl preuzme umjesto da se otvori u tabu. Blob pristup daje punu kontrolu nad zahtjevom i odgovorom.

---

#### Sprint 2 — Ocjenjivanje (komponenta zvjezdica)

##### `MaterialRating.vue`

Komponenta prikazuje prosječnu ocjenu materijala (read-only zvjezdice + brojčani prikaz, npr. "4.2 / 5.0 (12 ocjena)") i interaktivne zvjezdice za ocjenjivanje.

> **Napomena o rasporedu:** U Sprintu 2 implementiran je kompletan sistem ocjenjivanja — zvjezdice, slanje ocjene (`POST`), promjena ocjene (`PATCH`), modal za potvrdu promjene i sve poruke (neprijavljen korisnik ne može ocijeniti, već ste ocijenili, vlastiti materijal). Uslov "korisnik mora preuzeti materijal prije ocjenjivanja" (zaključavanje zvjezdica dok se ne preuzme) dodan je u Sprintu 3.

**Poruke ovisno o stanju korisnika:**

| Stanje korisnika | Prikaz |
|---|---|
| Prijavljen | Aktivne zvjezdice |
| Nije prijavljen | Link "Prijavite se da biste mogli ocijeniti." |

**Slanje ocjene (`submitRating`):** Ako korisnik nije prijavljen — ne radi ništa. Ako je već ocijenio (`selectedRating > 0`) — otvara se modal za potvrdu promjene. Provjera vlastitog materijala — poređenjem `user_id` iz JWT tokena s autorom materijala — sprječava ocjenjivanje vlastitog materijala uz poruku.

**Promjena ocjene:** Prvo ocjenjivanje koristi `rateMaterial` (`POST`). Ako korisnik već ima ocjenu i klikne ponovo, otvara se modal ("Želite li promijeniti ocjenu?"); potvrdom se poziva `updateRating` (`PATCH`).

**Razlikovanje statusa:** `rateMaterial` i `updateRating` vraćaju sirovi `response` (ne parsirani JSON), pa komponenta čita `response.status` da razlikuje greške — npr. `409` znači "već ste ocijenili ovaj materijal".

**Modali:** Komponenta sadrži modal za potvrdu promjene ocjene i modal uspjeha (poruka "Hvala na ocjeni!" / "Ocjena promijenjena!").

##### Prikaz broja preuzimanja

Na stranici detalja prikazuje se brojač preuzimanja ("Broj preuzimanja: X"), vezan za polje `number_of_downloads` koje backend povećava pri svakom preuzimanju. Nakon uspješnog preuzimanja brojač se ažurira i lokalno (`updateDownloadCount`), bez potrebe za osvježavanjem stranice.

---

#### Sprint 3 — Thumbnail, provjera preuzimanja, validacija dužine i dark mode

##### Provjera preuzimanja i otključavanje zvjezdica

U Sprintu 3 dodan je uslov "preuzmi pa ocijeni" na frontendu. Zvjezdice su aktivne samo kada je korisnik prijavljen **i** kada je preuzeo materijal:

```html
:class="(isLoggedIn && hasDownloaded) ? 'cursor-pointer' : 'cursor-not-allowed opacity-50'"
```

Ako je korisnik prijavljen ali nije preuzeo, prikazuje se poruka "Preuzmite materijal da biste mogli ocijeniti."

**Provjera preuzimanja (dva načina):**
- U `onMounted` se poziva `checkHasDownloaded` (backend `/has-downloaded`) i postavlja `hasDownloaded` — pokriva slučaj kada je korisnik preuzeo materijal u ranijoj posjeti.
- `watch` prati `parentHasDownloaded` prop — kada korisnik preuzme materijal na istoj stranici, zvjezdice se otključavaju u realnom vremenu, bez osvježavanja stranice.

##### Povezivanje preuzimanja i ocjenjivanja (`MaterialDetailView.vue`)

`MaterialDetailView.vue` povezuje `DownloadButton` i `MaterialRating` u jedinstven tok:

```html
<DownloadButton @downloaded="updateDownloadCount" />
<MaterialRating :parent-has-downloaded="hasDownloaded" />
```

Funkcija `updateDownloadCount` se okida na `@downloaded` događaj, povećava lokalni brojač preuzimanja i postavlja `hasDownloaded = true`. To se prosljeđuje `MaterialRating` komponenti kao prop, čime se zvjezdice odmah otključavaju — implementacija pravila "preuzmi pa ocijeni" bez osvježavanja stranice (komunikacija roditelj↔dijete: props naniže, emit naviše).

##### Prikaz thumbnail sličice i detalja materijala (`MaterialDetailView.vue`)

Thumbnail se prikazuje samo ako postoji (`v-if="material.thumbnail_path"`):

```html
<img :src="`http://127.0.0.1:8000/thumbnails/${material.thumbnail_path.split('/').pop()}`" ... />
```

Iz pune putanje koju vraća backend (`uploads/thumbnails/ime.png`) izvlači se samo naziv fajla (`split('/').pop()`) i lijepi na `/thumbnails/` statičku rutu servera.

Pored thumbnaila, na detaljnoj kartici sređen je izgled prikaza i dodate su informacije o materijalu — **ime predmeta, godina studija i tip materijala**:

```html
<p>{{ material.subject?.name }} • {{ material.subject?.study_year }}. godina • {{ material.file_type }}</p>
```

##### Dodatna validacija forme (dužina polja)

Osnovna validacija obaveznih polja (iz Sprinta 1) proširena je provjerom minimalne i maksimalne dužine teksta, uz konkretne poruke korisniku:

| Polje | Pravilo |
|---|---|
| Naziv | Najmanje 3, najviše 100 karaktera |
| Opis | Najmanje 10, najviše 1000 karaktera |

Ako polje ne zadovoljava dužinu, u `errors` se umjesto `true` upisuje tekstualna poruka (npr. "Naziv mora imati najmanje 3 karaktera."), koja se prikazuje ispod polja.

##### Dark mode stilizacija

Sam mehanizam prebacivanja teme (toggle koji postavlja `dark` klasu) razvio je drugi član tima. Lično implementirani dio je **dark mode stilizacija svih komponenti modula Materijali** — ručno dodavanje Tailwind `dark:` varijanti (`dark:bg-...`, `dark:text-...`, `dark:border-...`) na sve elemente: formu za upload, sve modale i poruke (potvrda ocjene, uspjeh, greške) pojedinačno, kartice materijala, stranicu s detaljima i komponentu ocjenjivanja. Svaka poruka i komponenta obrađena je zasebno, čime je osigurano da cijeli modul ispravno i čitljivo izgleda u tamnom režimu.

---

#### API funkcije (`services/api.js`)

| Funkcija | Endpoint | Opis |
|---|---|---|
| `uploadMaterial(formData)` | `POST /materials/upload` | Slanje novog materijala (FormData, bez ručnog Content-Type) |
| `downloadMaterial(materialId)` | `GET /materials/{id}/download` | Preuzimanje (token kroz URL + cache-busting `t=`) |
| `checkHasDownloaded(materialId)` | `GET /materials/{id}/has-downloaded` | Provjera da li je korisnik preuzeo |
| `rateMaterial(materialId, rating)` | `POST /materials/{id}/rate` | Slanje ocjene |
| `updateRating(materialId, rating)` | `PATCH /materials/{id}/rate` | Izmjena ocjene |

Funkcije `rateMaterial` i `updateRating` vraćaju sirovi `response` (ne parsirani JSON) kako bi komponenta mogla razlikovati statuse (npr. `409` — već ocijenjeno). `downloadMaterial` dodaje `t={timestamp}` na URL radi izbjegavanja keširanja preglednika — bez toga se ponovljeno preuzimanje ne bi zabilježilo na backendu (browser bi servirao iz keša, ne bi pozvao backend).


## Tim 2 — Materijali (Faris Ćosić) — Frontend

### Pregled

Ova dokumentacija opisuje frontend implementaciju koju je radio Faris Ćosić u okviru Tim 2 — modul Materijali. Implementacija obuhvata komponente za prikaz, pregled i upravljanje materijalima.

Kod se nalazi u `frontend/src/views/materials/` i `frontend/src/components/`.

---

### Sprint 1

#### Izrada MaterialCard komponente

Kreirana komponenta `MaterialCard.vue` koja prikazuje osnovne informacije o materijalu: naslov, autora, datum, predmet, thumbnail, prosječnu ocjenu (zvjezdice) i broj preuzimanja. Komponenta podržava dva moda — standardni prikaz s Download/Delete dugmadima i pending mod s Odobri/Odbij dugmadima.

**Props:**

| Prop | Tip | Default | Opis |
|---|---|---|---|
| `material` | Object | — | Objekat materijala |
| `pending` | Boolean | `false` | Ako je `true`, prikazuje Odobri/Odbij umjesto Download/Delete |
| `userRole` | String | `'member'` | Rola prijavljenog korisnika |

**Emits:** `click`, `deleted`, `approve`, `reject`, `toggle-bookmark`, `downloaded`

#### Pregled materijala bez prijave

Integrirana `getPublicMaterials()` API funkcija u `MaterialList.vue` za neprijavljene korisnike. Koristi `GET /materials/public` endpoint koji ne zahtijeva JWT token.

#### Pregled materijala sa prijavom

Integrirana `getMaterials()` API funkcija za prijavljene korisnike. Koristi `GET /materials/` endpoint koji uz svaki materijal vraća i `is_bookmarked` stanje. `MaterialList.vue` automatski bira između ova dva endpointa ovisno o tabu i prijavi korisnika.

#### Detaljne informacije za materijal

Kreirana komponenta `MaterialDetailView.vue` koja prikazuje sve detalje materijala: naslov, autora, datum, predmet, godinu, tip, thumbnail, opis, ocjene, komentare i broj preuzimanja. Integriran `DownloadButton`, `CommentList` i `MaterialRating`.

---

### Sprint 2

#### Pregled detalja materijala

Proširena `MaterialDetailView.vue` s dugmetom za inline pregled fajla u browseru bez preuzimanja. Dugme `PREGLEDAJ` prikazuje se samo za podržane ekstenzije (`.pdf`, `.txt`) i otvara fajl u novom tabu koristeći `GET /materials/{id}/preview` endpoint.

#### Admin upravljanje materijalima

Implementirana admin funkcionalnost u `MaterialDetailView.vue` — Odobri/Odbij dugmad vidljiva samo adminu kada je status materijala `pending`. Rola se čita iz `localStorage`. Nakon akcije prikazuje se `SuccessMessage` komponenta.


#### Prikaz materijala na čekanju

Kreirana komponenta `PendingMaterialList.vue` koja učitava sve pending materijale putem `GET /materials/pending` endpointa i prikazuje ih koristeći `MaterialCard` u pending modu.

#### Odobravanje materijala

Implementirana logika odobravanja i odbijanja u `PendingMaterialList.vue`. Nakon odobravanja ili odbijanja, materijal se lokalno uklanja iz liste bez ponovnog učitavanja stranice.

```javascript
async function handleApprove(id) {
    await approveMaterial(id)
    materials.value = materials.value.filter(m => m.id !== id)
}

async function handleReject(id) {
    await rejectMaterial(id)
    materials.value = materials.value.filter(m => m.id !== id)
}
```

---

### Sprint 3

#### Ažuriranje materijala

Dodana funkcionalnost inline uređivanja u `MaterialDetailView.vue`, vidljiva samo vlasniku materijala:

- Toggle između prikaza i editovanja (dugmad Uredi / Spremi / Odustani)
- Inline uređivanje naslova i opisa direktno u prikazu
- Odabir godine studija i predmeta iz dropdown menija (predmeti filtrirani po odabranoj godini)
- Drag-and-drop zamjena fajla ili odabir putem file input-a
- Čuvanje originalnih vrijednosti i vraćanje pri otkazivanju
- Nakon spremanja materijal se ponovo učitava s API-a

```javascript
function cancelEdit() {
    material.value.title = originalTitle.value
    material.value.description = originalDescription.value
    isEditing.value = false
    selectedFile.value = null
}

async function saveChanges() {
    await updateMaterial(material.value.id, material.value.title, 
        material.value.description, selectedFile.value, 
        editSubjectId.value, editMaterialType.value)
    material.value = await getMaterial(route.params.id)
    isEditing.value = false
}
```

#### - Preview materijala

Implementirana logika za inline pregled fajla u `MaterialDetailView.vue`. Dugme `PREGLEDAJ` prikazuje se uvjetno na osnovu ekstenzije fajla, a fajl se otvara u novom tabu bez pokretanja preuzimanja.
## Rute aplikacije

### Pregled svih ruta

| Putanja               | Ime                 | Komponenta                 | Pristup     |
| --------------------- | ------------------- | -------------------------- | ----------- |
| `/`                   | `home`              | `HomeView`                 | Javno       |
| `/login`              | `login`             | `LoginView`                | Samo gosti  |
| `/register`           | `register`          | `RegisterView`             | Samo gosti  |
| `/ads`                | `ads`               | `AdsView`                  | Javno       |
| `/ads/:id`            | `ad-detail`         | `AdView`                   | Javno       |
| `/ads/:id/apply`      | `application`       | `ApplicationView`          | Prijavljeni |
| `/companies/:id`      | `company`           | `CompanyView`              | Javno       |
| `/company/register`   | `company-register`  | `CompanyRegisterView`      | Javno       |
| `/company/login`      | `company-login`     | `CompanyLoginView`         | Samo gosti  |
| `/prakse-i-edukacije` | `prakse-edukacije`  | `AdsView`                  | Prijavljeni |
| `/prakse`             | `prakse`            | `PrakseView`               | Prijavljeni |
| `/workshops`          | `workshops`         | `WorkshopsView`            | Prijavljeni |
| `/materials`          | `materials`         | `MaterialsView`            | Javno       |
| `/materials/upload`   | `material-upload`   | `MaterialUploadView`       | Prijavljeni |
| `/materials/pending`  | `pending-materials` | `MaterialsView`            | Admin       |
| `/materials/:id`      | `material-details`  | `MaterialDetailView`       | Javno       |
| `/forum`              | `forum`             | `ForumView`                | Prijavljeni |
| `/forum/nova-tema`    | `create-topic`      | `CreateTopicView`          | Prijavljeni |
| `/forum/tema/:id`     | `topic-detail`      | `TopicDetailView`          | Prijavljeni |
| `/forum/admin`        | `admin-dashboard`   | `AdminDashboardView`       | Admin       |
| `/dashboard`          | `dashboard`         | `DashboardView`            | Prijavljeni |
| `/profiles`           | `profiles`          | `ProfilesView`             | Prijavljeni |
| `/admin`              | `admin`             | `AdminKorisniciView`       | Admin       |
| `/admin/companies`    | `admin-companies`   | `AdminCompanyApprovalView` | Admin       |
| `/admin/ads`          | `admin-ads`         | `AdminAdsView`             | Admin       |
| `/admin/users`        | `admin-users`       | `AdminKorisniciView`       | Admin       |

---

### Meta oznake ruta

| Meta oznaka           | Opis                                                                |
| --------------------- | ------------------------------------------------------------------- |
| `requiresAuth: true`  | Ruta zahtijeva prijavljenog korisnika — preusmjerava na `/login`    |
| `requiresAdmin: true` | Ruta zahtijeva administratorsku ulogu — preusmjerava na `/`         |
| `guestOnly: true`     | Ruta dostupna samo neprijavljenim korisnicima — preusmjerava na `/` |

---

### Guard logika (`beforeEach`)

Prije svake navigacije router provjerava sljedeće uslove redom:

1. Ruta ima `requiresAuth` i korisnik **nije prijavljen** → preusmjeri na `/login`
2. Ruta ima `requiresAdmin` i korisnik **nije admin** → preusmjeri na `/`
3. Ruta ima `guestOnly` i korisnik **jest prijavljen** → preusmjeri na `/`
4. Inače → nastavi normalnom navigacijom

Prijava se provjerava prisustvom ključa `token` u `localStorage`, a uloga čitanjem ključa `role`.

## API Servis (`src/services/api.js`)

Svi pozivi prema backend API-ju centralizovani su u jednom fajlu. Base URL je hardkodiran:

```js
const BASE_URL = "http://127.0.0.1:8000";
```

### Pomoćne funkcije

| Funkcija                                   | Opis                                                                                                                |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| `parseResponse(response)`                  | Parsira JSON response, baca grešku ako `response.ok` nije `true`                                                    |
| `authHeaders(token)`                       | Vraća headere s `Content-Type` i `Authorization: Bearer <token>`                                                    |
| `handleAdminFetch(response, errorMessage)` | Parsira admin response, automatski odjavljuje korisnika i preusmjerava na `/login` ako je nalog deaktiviran (`403`) |

---

### Auth

| Funkcija                                  | Metoda | Endpoint              | Opis                                      |
| ----------------------------------------- | ------ | --------------------- | ----------------------------------------- |
| `registerUser(email, fullName, password)` | `POST` | `/auth/register`      | Registracija studenta                     |
| `loginUser(email, password)`              | `POST` | `/auth/login`         | Prijava studenta (`multipart/form-data`)  |
| `loginCompany(email, password)`           | `POST` | `/auth/company/login` | Prijava kompanije (`multipart/form-data`) |

---

### Korisnici

| Funkcija                              | Metoda | Endpoint                 | Opis                                                           |
| ------------------------------------- | ------ | ------------------------ | -------------------------------------------------------------- |
| `getMe(token)`                        | `GET`  | `/me`                    | Dohvata podatke trenutno prijavljenog korisnika                |
| `getMyApplications(token)`            | `GET`  | `/applications/me/all`   | Lista svih prijava prijavljenog studenta                       |
| `getMyActivity(token, limit, offset)` | `GET`  | `/api/users/me/activity` | Historija aktivnosti korisnika (paginacija: `limit`, `offset`) |

---

### Kompanije

| Funkcija                                        | Metoda   | Endpoint                      | Opis                                                    |
| ----------------------------------------------- | -------- | ----------------------------- | ------------------------------------------------------- |
| `registerCompany(data, logoFile)`               | `POST`   | `/companies/`                 | Registracija kompanije s logoom (`multipart/form-data`) |
| `getApprovedCompanies()`                        | `GET`    | `/companies/`                 | Lista svih odobrenih kompanija                          |
| `getCompanyById(id)`                            | `GET`    | `/companies/{id}`             | Detalji jedne kompanije                                 |
| `getAdminCompanies(token)`                      | `GET`    | `/companies/admin`            | Lista svih kompanija (admin)                            |
| `updateCompanyStatus(companyId, status, token)` | `PATCH`  | `/companies/{id}/status`      | Promjena statusa kompanije                              |
| `uploadCompanyLogo(companyId, file, token)`     | `PATCH`  | `/companies/{id}/upload-logo` | Upload logoa kompanije                                  |
| `restoreCompany(companyId, token)`              | `PATCH`  | `/companies/{id}/restore`     | Vraćanje obrisane kompanije                             |
| `deleteCompany(companyId, token)`               | `DELETE` | `/companies/{id}`             | Soft delete kompanije                                   |

---

### Oglasi

| Funkcija                     | Metoda | Endpoint                | Opis                            |
| ---------------------------- | ------ | ----------------------- | ------------------------------- |
| `getAds()`                   | `GET`  | `/ads/`                 | Lista svih aktivnih oglasa      |
| `getAdById(id)`              | `GET`  | `/ads/{id}`             | Detalji jednog oglasa           |
| `getAdsByCompany(companyId)` | `GET`  | `/ads/?company_id={id}` | Lista oglasa određene kompanije |

---

### Prijave

| Funkcija                                                                     | Metoda  | Endpoint                                                           | Opis                                                  |
| ---------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------ | ----------------------------------------------------- |
| `uploadFile(file)`                                                           | `POST`  | `/applications/upload-cv`                                          | Upload CV-a (PDF, max 5 MB) — token iz `localStorage` |
| `createApplication(applicationData, token)`                                  | `POST`  | `/applications/`                                                   | Kreiranje prijave na oglas                            |
| `getApplicationsByAd(adId, token, isCompany)`                                | `GET`   | `/applications/company/by-ad/{id}` ili `/applications/?ad_id={id}` | Lista prijava za oglas (ruta ovisi o tipu aktera)     |
| `updateApplicationStatus(applicationId, status, feedback, token, isCompany)` | `PATCH` | `/applications/company/{id}` ili `/applications/{id}`              | Ažuriranje statusa prijave (ruta ovisi o tipu aktera) |

---

### Bookmarks

| Funkcija                            | Metoda   | Endpoint          | Opis                        |
| ----------------------------------- | -------- | ----------------- | --------------------------- |
| `getBookmarks(token)`               | `GET`    | `/bookmarks/`     | Lista sačuvanih oglasa      |
| `addBookmark(adId, token)`          | `POST`   | `/bookmarks/`     | Dodavanje oglasa u sačuvane |
| `removeBookmark(bookmarkId, token)` | `DELETE` | `/bookmarks/{id}` | Uklanjanje bookmarkа        |

---

### Notifikacije

Notifikacije su grupisane u `notificationService` objekat. Token se automatski čita iz `localStorage` (`token` ili `company_token`).

| Metoda                                     | HTTP     | Endpoint                   | Opis                                         |
| ------------------------------------------ | -------- | -------------------------- | -------------------------------------------- |
| `notificationService.getMyNotifications()` | `GET`    | `/notifications/me`        | Lista notifikacija trenutnog aktera          |
| `notificationService.markAsRead(id)`       | `PUT`    | `/notifications/{id}/read` | Označavanje jedne notifikacije kao pročitane |
| `notificationService.markAllAsRead()`      | `PUT`    | `/notifications/read-all`  | Označavanje svih kao pročitano               |
| `notificationService.clearAll()`           | `DELETE` | `/notifications/clear-all` | Brisanje svih notifikacija                   |

---

### Materijali

| Funkcija                                                                | Metoda   | Endpoint                         | Opis                                                         |
| ----------------------------------------------------------------------- | -------- | -------------------------------- | ------------------------------------------------------------ |
| `getMaterials(filters, page, perPage)`                                  | `GET`    | `/materials/`                    | Lista materijala s filterima i paginacijom (zahtijeva token) |
| `getPublicMaterials(filters, page, perPage)`                            | `GET`    | `/materials/public`              | Lista javnih materijala s filterima i paginacijom            |
| `getMaterial(id)`                                                       | `GET`    | `/materials/{id}`                | Detalji jednog materijala                                    |
| `getMaterialPreviewUrl(id)`                                             | —        | `/materials/{id}/preview`        | Vraća URL za preview materijala (ne šalje zahtjev)           |
| `uploadMaterial(formData)`                                              | `POST`   | `/materials/upload`              | Upload novog materijala                                      |
| `updateMaterial(id, title, description, file, subjectId, materialType)` | `PATCH`  | `/materials/{id}/update`         | Ažuriranje materijala                                        |
| `deleteMaterial(id)`                                                    | `DELETE` | `/materials/{id}`                | Brisanje materijala                                          |
| `getPendingMaterials()`                                                 | `GET`    | `/materials/pending`             | Lista materijala na čekanju (admin)                          |
| `approveMaterial(id)`                                                   | `PATCH`  | `/materials/{id}/approve`        | Odobravanje materijala (admin)                               |
| `rejectMaterial(id)`                                                    | `PATCH`  | `/materials/{id}/reject`         | Odbijanje materijala (admin)                                 |
| `downloadMaterial(materialId)`                                          | `GET`    | `/materials/{id}/download`       | Preuzimanje materijala (token se šalje kao query param)      |
| `checkHasDownloaded(materialId)`                                        | `GET`    | `/materials/{id}/has-downloaded` | Provjera da li je korisnik preuzeo materijal                 |
| `rateMaterial(materialId, rating)`                                      | `POST`   | `/materials/{id}/rate`           | Ocjenjivanje materijala                                      |
| `updateRating(materialId, rating)`                                      | `PATCH`  | `/materials/{id}/rate`           | Ažuriranje ocjene materijala                                 |
| `toggleBookmark(materialId)`                                            | `POST`   | `/materials/{id}/bookmark`       | Dodavanje / uklanjanje bookmarkа materijala                  |
| `getSubjects()`                                                         | `GET`    | `/materials/subjects`            | Lista predmeta                                               |

---

### Komentari na materijalima

| Funkcija                                        | Metoda   | Endpoint                               | Opis                          |
| ----------------------------------------------- | -------- | -------------------------------------- | ----------------------------- |
| `getComments(materialId)`                       | `GET`    | `/materials/{id}/comments`             | Lista komentara na materijalu |
| `postComment(materialId, content)`              | `POST`   | `/materials/{id}/comments`             | Dodavanje komentara           |
| `updateComment(materialId, commentId, content)` | `PATCH`  | `/materials/{id}/comments/{commentId}` | Uređivanje komentara          |
| `deleteComment(materialId, commentId)`          | `DELETE` | `/materials/{id}/comments/{commentId}` | Brisanje komentara            |

---

### Profil

| Funkcija                    | Metoda   | Endpoint              | Opis                                                          |
| --------------------------- | -------- | --------------------- | ------------------------------------------------------------- |
| `getMyProfile(token)`       | `GET`    | `/profiles/me`        | Dohvata profil prijavljenog korisnika                         |
| `uploadAvatar(token, file)` | `POST`   | `/profiles/me/avatar` | Upload profilne slike (dodaje cache-busting timestamp na URL) |
| `removeAvatar(token)`       | `DELETE` | `/profiles/me/avatar` | Brisanje profilne slike                                       |

---

### Admin — Korisnici

| Funkcija                                          | Metoda   | Endpoint                       | Opis                                           |
| ------------------------------------------------- | -------- | ------------------------------ | ---------------------------------------------- |
| `getAllUsers(token, { search, role, is_active })` | `GET`    | `/admin/users`                 | Lista svih korisnika s filterima               |
| `activateUser(token, userId)`                     | `POST`   | `/admin/users/{id}/activate`   | Aktivacija korisnika                           |
| `deactivateUser(token, userId)`                   | `POST`   | `/admin/users/{id}/deactivate` | Deaktivacija korisnika                         |
| `deleteUser(token, userId)`                       | `DELETE` | `/admin/users/{id}`            | Trajno brisanje korisnika                      |
| `changeUserRole(token, userId, roleData)`         | `PATCH`  | `/admin/users/{id}/role`       | Promjena uloge korisnika                       |
| `getPlatformStats(token, period)`                 | `GET`    | `/admin/stats?period={period}` | Statistika platforme (default period: `month`) |

---

### Napomene

- Većina funkcija prima `token` kao argument — izuzetak su funkcije unutar `notificationService` i neke funkcije za materijale koje token čitaju direktno iz `localStorage`
- `handleAdminFetch` automatski odjavljuje korisnika i preusmjerava na `/login` ako backend vrati `403` s porukom da je nalog deaktiviran
- `downloadMaterial` token šalje kao query parametar (`?token=...`) umjesto u headeru, zbog načina na koji browser inicira download

## Komponente

### `CompanyView.vue`

**Putanja:** `src/views/company/CompanyView.vue`  
**Ruta:** `/companies/:id`

Stranica profila kompanije. Prikazuje informacije o kompaniji i njene aktivne oglase. Ako je prijavljena kompanija vlasnik profila, omogućava uređivanje profila i kreiranje novih oglasa.

---

#### Props / Route params

| Param              | Opis                                  |
| ------------------ | ------------------------------------- |
| `$route.params.id` | ID kompanije koji se dohvata iz URL-a |

---

#### Data

| Polje               | Tip              | Opis                                           |
| ------------------- | ---------------- | ---------------------------------------------- |
| `loading`           | `bool`           | Indikator učitavanja podataka                  |
| `saving`            | `bool`           | Indikator aktivnog slanja forme                |
| `errorMessage`      | `str`            | Globalna greška pri učitavanju                 |
| `profileError`      | `str`            | Greška pri ažuriranju profila                  |
| `adError`           | `str`            | Greška pri kreiranju oglasa                    |
| `company`           | `object \| null` | Podaci o kompaniji dohvaćeni s API-ja          |
| `ads`               | `array`          | Lista aktivnih oglasa kompanije                |
| `loggedInCompanyId` | `str \| null`    | ID prijavljene kompanije iz `localStorage`     |
| `hasCompanyToken`   | `bool`           | Da li postoji `company_token` u `localStorage` |
| `isEditing`         | `bool`           | Da li je aktivan mod uređivanja profila        |
| `isCreatingAd`      | `bool`           | Da li je otvoren modal za kreiranje oglasa     |
| `editForm`          | `object`         | Forma za uređivanje profila kompanije          |
| `adForm`            | `object`         | Forma za kreiranje novog oglasa                |

---

#### Computed

| Svojstvo  | Opis                                                                                                                         |
| --------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `logoUrl` | Generiše puni URL logoa kompanije (`BASE_URL + logo_path`)                                                                   |
| `isOwner` | `true` ako je prijavljena kompanija vlasnik ovog profila — provjerava `company_token` i poklapa `company_id` s ID-em iz rute |

---

#### Metode

| Metoda           | Opis                                                                                                                       |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `fetchCompany()` | Paralelno dohvata podatke o kompaniji i njene oglase (`Promise.all`), mapira oglase kroz `mapAd` helper                    |
| `startEdit()`    | Popunjava `editForm` trenutnim podacima kompanije i aktivira mod uređivanja                                                |
| `saveProfile()`  | Šalje `PATCH /companies/{id}` s podacima iz `editForm`, ažurira lokalni `company` objekt bez ponovnog učitavanja           |
| `createAd()`     | Šalje `POST /ads` s podacima iz `adForm`, dodaje novi oglas na vrh liste odmah bez čekanja, zatim osvježava listu s API-ja |

---

#### API pozivi

| Metoda                      | Endpoint           | Servis                             |
| --------------------------- | ------------------ | ---------------------------------- |
| `GET /companies/{id}`       | Detalji kompanije  | `getCompanyById` iz `api.js`       |
| `GET /ads/?company_id={id}` | Oglasi kompanije   | `getAdsByCompany` iz `api.js`      |
| `PATCH /companies/{id}`     | Ažuriranje profila | Direktan `fetch` s `company_token` |
| `POST /ads`                 | Kreiranje oglasa   | Direktan `fetch` s `company_token` |

---

#### Komponente

| Komponenta | Opis                                                                   |
| ---------- | ---------------------------------------------------------------------- |
| `AdCard`   | Kartica oglasa, koristi se u gridu za prikaz aktivnih oglasa kompanije |

---

#### Lifecycle

| Hook      | Opis                                                                           |
| --------- | ------------------------------------------------------------------------------ |
| `mounted` | Poziva `fetchCompany()`, čita `company_token` i `company_id` iz `localStorage` |

---

#### Napomene

- `isOwner` kombinuje dvije provjere — prisustvo tokena i podudaranje ID-eva — što znači da samo vlasnik profila vidi dugmad za uređivanje i kreiranje oglasa
- `saveProfile` direktno ažurira lokalni `company` objekt (`this.company = { ...this.company, ...this.editForm }`) bez ponovnog poziva API-ja, za brži UX
- `createAd` odmah dodaje oglas u listu (`this.ads.unshift(newMappedAd)`) pa tek onda osvježava s API-ja — optimistični update
- Ako `adForm.deadline` nije popunjen, automatski se postavlja 30 dana unaprijed
- `BASE_URL` je hardkodiran lokalno unutar komponente pored centralnog u `api.js` — potencijalno mjesto za refaktor

---

### `CompanyRegisterView.vue`

**Putanja:** `src/views/company/CompanyRegisterView.vue`  
**Ruta:** `/company/register`

Stranica za registraciju kompanije. Sadrži formu s klijentskom validacijom, preview logoa i informativni panel s koracima nakon registracije.

---

#### Data (Composition API)

| Polje          | Tip        | Opis                                             |
| -------------- | ---------- | ------------------------------------------------ |
| `form`         | `reactive` | Podaci forme (sva polja kompanije)               |
| `errors`       | `reactive` | Greške validacije po polju                       |
| `logoFile`     | `ref`      | Odabrani fajl logoa                              |
| `logoPreview`  | `ref`      | Lokalni URL za preview logoa (`createObjectURL`) |
| `isLoading`    | `ref`      | Indikator aktivnog slanja forme                  |
| `submitStatus` | `ref`      | Status slanja: `null` / `'success'` / `'error'`  |
| `serverError`  | `ref`      | Poruka greške s backenda                         |

---

#### Polja forme

| Polje          | Tip      | Validacija                        |
| -------------- | -------- | --------------------------------- |
| `company_name` | `string` | Obavezno                          |
| `tin`          | `string` | Obavezno, tačno 13 cifara         |
| `website_url`  | `string` | Obavezno, validan URL             |
| `address`      | `string` | Obavezno                          |
| `description`  | `string` | Obavezno                          |
| `email`        | `string` | Obavezno, validan email format    |
| `phone_number` | `string` | Obavezno                          |
| `password`     | `string` | Obavezno, minimum 8 karaktera     |
| `logo`         | `file`   | Obavezno, PNG / JPG / JPEG / WebP |

---

#### Metode

| Metoda                 | Opis                                                                                |
| ---------------------- | ----------------------------------------------------------------------------------- |
| `handleLogoChange(e)`  | Validira tip fajla, postavlja `logoFile` i generiše `logoPreview`                   |
| `validateField(field)` | Validira jedno polje kroz `validators` mapu, rezultat upisuje u `errors`            |
| `handleSubmit()`       | Validira sva polja, provjerava logo, šalje formu kroz `registerCompany` iz `api.js` |
| `inputClass(error)`    | Helper koji vraća Tailwind klase inputa — crveni border ako postoji greška          |

---

#### API pozivi

| Endpoint           | Servis                        | Opis                                                  |
| ------------------ | ----------------------------- | ----------------------------------------------------- |
| `POST /companies/` | `registerCompany` iz `api.js` | Šalje `multipart/form-data` s podacima forme i logoom |

---

#### Napomene

- Validacija se okida `@blur` po polju — korisnik vidi grešku tek kad napusti polje
- `handleSubmit` validira sva polja odjednom prije slanja — sprječava slanje nepotpune forme
- Nakon uspješne registracije forma se skriva, prikazuje se zelena poruka o čekanju odobrenja
- Logo preview se generiše lokalno kroz `URL.createObjectURL` bez slanja na server
- Dozvoljeni formati logoa: `image/png`, `image/jpeg`, `image/webp`

---

### `CompanyLoginView.vue`

**Putanja:** `src/views/company/CompanyLoginView.vue`  
**Ruta:** `/company/login`  
**Meta:** `guestOnly: true`

Stranica za prijavu kompanije. Nakon uspješne prijave čuva token i podatke kompanije u `localStorage` te preusmjerava na početnu stranicu.

---

#### Data

| Polje        | Tip              | Opis                              |
| ------------ | ---------------- | --------------------------------- |
| `identifier` | `string`         | Email ili broj telefona kompanije |
| `password`   | `string`         | Lozinka                           |
| `loading`    | `bool`           | Indikator aktivnog zahtjeva       |
| `error`      | `string \| null` | Poruka greške pri prijavi         |

---

#### Metode

| Metoda          | Opis                                                                   |
| --------------- | ---------------------------------------------------------------------- |
| `handleLogin()` | Šalje zahtjev za prijavu, pri uspjehu čuva token i preusmjerava na `/` |

---

#### API pozivi

| Endpoint                   | Servis                     | Opis                                      |
| -------------------------- | -------------------------- | ----------------------------------------- |
| `POST /auth/company/login` | `loginCompany` iz `api.js` | Prijava kompanije (`multipart/form-data`) |

---

#### localStorage

Nakon uspješne prijave upisuju se sljedeći ključevi:

| Ključ           | Opis                |
| --------------- | ------------------- |
| `company_token` | JWT token kompanije |
| `company_name`  | Naziv kompanije     |
| `company_id`    | ID kompanije        |

---

#### Napomene

- Preusmjeravanje nakon prijave radi kroz `window.location.href = '/'` umjesto `router.push` — stranica se potpuno osvježava kako bi ostale komponente (npr. navbar) preuzele novi token
- Ruta ima `guestOnly: true` — prijavljene kompanije ne mogu pristupiti ovoj stranici

---

### `AdminCompanyApprovalView.vue`

**Putanja:** `src/views/company/AdminCompanyApprovalView.vue`  
**Ruta:** `/admin/companies`  
**Meta:** `requiresAuth: true`, `requiresAdmin: true`

Administratorska stranica za upravljanje kompanijama. Prikazuje sve registrovane kompanije s filterima po statusu i omogućava odobravanje, odbijanje, brisanje i vraćanje kompanija.

---

#### Data

| Polje          | Tip      | Opis                                                                                   |
| -------------- | -------- | -------------------------------------------------------------------------------------- |
| `companies`    | `array`  | Lista svih kompanija dohvaćenih s API-ja (svaka ima dodatno polje `updating`)          |
| `loading`      | `bool`   | Indikator učitavanja                                                                   |
| `errorMessage` | `string` | Poruka greške                                                                          |
| `activeFilter` | `string` | Aktivni filter (`'Sve'` / `'Na čekanju'` / `'Odobrene'` / `'Odbijene'` / `'Obrisane'`) |

---

#### Computed

| Svojstvo            | Opis                                                                                                   |
| ------------------- | ------------------------------------------------------------------------------------------------------ |
| `filteredCompanies` | Filtrira `companies` prema `activeFilter` — obrisane se filtriraju po `is_deleted`, ostale po `status` |

---

#### Metode

| Metoda                           | Opis                                                                                                      |
| -------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `fetchCompanies()`               | Dohvata sve kompanije kroz admin endpoint, dodaje `updating: null` na svaki objekt                        |
| `filterCount(filter)`            | Vraća broj kompanija za svaki filter — koristi se za prikaz brojača na dugmadima                          |
| `updateStatus(company, status)`  | Šalje `PATCH` za promjenu statusa (`approved` / `denied`), ažurira lokalni objekt bez ponovnog učitavanja |
| `deleteCompanyHandler(company)`  | Soft delete kompanije — postavlja `is_deleted` na `true` lokalno nakon uspješnog API poziva               |
| `restoreCompanyHandler(company)` | Vraća obrisanu kompaniju — postavlja `is_deleted` na `false` lokalno nakon uspješnog API poziva           |

---

#### API pozivi

| Endpoint                        | Servis                | Opis                                   |
| ------------------------------- | --------------------- | -------------------------------------- |
| `GET /me`                       | `getMe`               | Provjera uloge korisnika pri mountanju |
| `GET /companies/admin`          | `getAdminCompanies`   | Lista svih kompanija                   |
| `PATCH /companies/{id}/status`  | `updateCompanyStatus` | Promjena statusa kompanije             |
| `DELETE /companies/{id}`        | `deleteCompany`       | Soft delete kompanije                  |
| `PATCH /companies/{id}/restore` | `restoreCompany`      | Vraćanje obrisane kompanije            |

---

#### Komponente

| Komponenta                 | Opis                                                                         |
| -------------------------- | ---------------------------------------------------------------------------- |
| `AdminCompanyApprovalCard` | Kartica kompanije s dugmadima za odobravanje, odbijanje, brisanje i vraćanje |

#### Eventi od `AdminCompanyApprovalCard`

| Event      | Opis                                       |
| ---------- | ------------------------------------------ |
| `@approve` | Poziva `updateStatus(company, 'approved')` |
| `@reject`  | Poziva `updateStatus(company, 'denied')`   |
| `@delete`  | Poziva `deleteCompanyHandler(company)`     |
| `@restore` | Poziva `restoreCompanyHandler(company)`    |

---

#### Filter mapiranje

| Label        | Status                |
| ------------ | --------------------- |
| `Na čekanju` | `pending`             |
| `Odobrene`   | `approved`            |
| `Odbijene`   | `denied`              |
| `Obrisane`   | `is_deleted === true` |
| `Sve`        | bez filtera           |

---

#### Lifecycle

| Hook      | Opis                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------- |
| `mounted` | Dohvata trenutnog korisnika kroz `getMe`, ako nije admin preusmjerava na `/`, inače poziva `fetchCompanies()` |

---

#### Napomene

- Dvostruka zaštita pristupa — ruta ima `requiresAdmin` guard, ali `mounted` dodatno provjerava ulogu kroz API poziv
- Svaka kompanija ima polje `updating` koje se postavlja za vrijeme API poziva — `AdminCompanyApprovalCard` ga može koristiti za prikaz loading stanja na dugmadima
- Sve akcije (odobravanje, brisanje, vraćanje) ažuriraju lokalni objekt optimistično bez ponovnog učitavanja cijele liste

---

### `ApplicationView.vue`

**Putanja:** `src/views/application/ApplicationView.vue`  
**Ruta:** `/ads/:id/apply`  
**Meta:** `requiresAuth: true`

Stranica za prijavu na oglas. Sadrži formu s upload zonama za CV i motivaciono pismo (drag & drop), polje za telefon i opcioni LinkedIn URL. Nakon uspješne prijave preusmjerava na stranicu oglasa.

---

#### Data

| Polje                  | Tip              | Opis                                               |
| ---------------------- | ---------------- | -------------------------------------------------- |
| `ad`                   | `object \| null` | Podaci o oglasu dohvaćeni s API-ja                 |
| `loading`              | `bool`           | Indikator aktivnog slanja prijave                  |
| `error`                | `string`         | Poruka greške                                      |
| `successMessage`       | `string`         | Poruka uspjeha nakon slanja                        |
| `cvDragActive`         | `bool`           | Drag & drop stanje za CV zonu                      |
| `letterDragActive`     | `bool`           | Drag & drop stanje za zonu motivacionog pisma      |
| `cvUploadProgress`     | `number`         | Progress upload bara za CV (0–100)                 |
| `letterUploadProgress` | `number`         | Progress upload bara za motivaciono pismo (0–100)  |
| `form.phone`           | `string`         | Telefonski broj studenta                           |
| `form.linkedinUrl`     | `string`         | LinkedIn URL (opcionalno)                          |
| `form.cvFile`          | `File \| null`   | Odabrani CV fajl                                   |
| `form.letterFile`      | `File \| null`   | Odabrano motivaciono pismo                         |
| `form.cvPath`          | `string \| null` | Putanja CV-a nakon uploada na server               |
| `form.letterPath`      | `string \| null` | Putanja motivacionog pisma nakon uploada na server |

---

#### Metode

| Metoda                      | Opis                                                                                      |
| --------------------------- | ----------------------------------------------------------------------------------------- |
| `fetchAd()`                 | Paralelno dohvata oglas i listu odobrenih kompanija, mapira naziv kompanije na oglas      |
| `handleCvChange(event)`     | Postavlja `form.cvFile` iz file input eventa                                              |
| `handleCvDrop(event)`       | Postavlja `form.cvFile` iz drag & drop eventa, validira fajl                              |
| `handleLetterChange(event)` | Postavlja `form.letterFile` iz file input eventa                                          |
| `handleLetterDrop(event)`   | Postavlja `form.letterFile` iz drag & drop eventa, validira fajl                          |
| `isValidFile(file)`         | Validira tip (`application/pdf`), ekstenziju (`.pdf`) i veličinu (max 5 MB)               |
| `handleFileUpload(file)`    | Upload jednog fajla kroz `uploadFile` iz `api.js`, vraća putanju s servera                |
| `submitApplication()`       | Validira formu, sekvencijalno uploaduje CV i pismo, kreira prijavu, preusmjerava na oglas |

---

#### API pozivi

| Endpoint                       | Servis                 | Opis                                               |
| ------------------------------ | ---------------------- | -------------------------------------------------- |
| `GET /ads/{id}`                | `getAdById`            | Dohvata detalje oglasa                             |
| `GET /companies/`              | `getApprovedCompanies` | Dohvata kompanije za mapiranje naziva              |
| `POST /applications/upload-cv` | `uploadFile`           | Upload CV-a (poziva se dva puta — za CV i pismo)   |
| `POST /applications/`          | `createApplication`    | Kreiranje prijave s putanjama uploadovanih fajlova |

---

#### Tok slanja prijave (`submitApplication`)

1. Validacija obaveznih polja i formata fajlova
2. Upload CV-a → dobija se `cv_path`
3. Upload motivacionog pisma → dobija se `motivational_letter_path`
4. Kreiranje prijave s putanjama i ostalim podacima forme
5. Prikaz poruke uspjeha → preusmjeravanje na `/ads/{id}` nakon 2 sekunde

---

#### Lifecycle

| Hook      | Opis                                            |
| --------- | ----------------------------------------------- |
| `mounted` | Poziva `fetchAd()` za dohvatanje detalja oglasa |

---

#### Napomene

- Dugme za slanje je disabled dok nisu odabrani CV, motivaciono pismo i telefon
- `uploadFile` iz `api.js` koristi se i za CV i za motivaciono pismo — backend endpoint je isti (`/applications/upload-cv`)
- Naziv kompanije se ne dobija direktno s oglasa nego se mapira kroz paralelni poziv na `/companies/` koristeći `Map` za O(1) lookup
- Progress barovi (`cvUploadProgress`, `letterUploadProgress`) trenutno se postavljaju ručno na `50` nakon uploada, a ne prate stvarni napredak mrežnog zahtjeva

---

### `AdsView.vue`

**Putanja:** `src/views/ads/AdsView.vue`  
**Ruta:** `/ads`, `/prakse-i-edukacije`

Glavna stranica za pregled oglasa. Prikazuje listu aktivnih oglasa s tabovima, pretragom i filterima. Studentima omogućava čuvanje oglasa u bookmarke.

---

#### Data

| Polje           | Tip      | Opis                                                                               |
| --------------- | -------- | ---------------------------------------------------------------------------------- |
| `loading`       | `bool`   | Indikator učitavanja                                                               |
| `currentTab`    | `string` | Aktivni tab (`'Sve'` / `'Prakse'` / `'Edukacije'` / `'Stipendije'` / `'Aktuelno'`) |
| `searchQuery`   | `string` | Pojam za pretragu                                                                  |
| `isPaid`        | `bool`   | Filter za plaćene prilike                                                          |
| `selectedField` | `string` | Filter po oblasti                                                                  |
| `ads`           | `array`  | Lista svih oglasa mapiranih za prikaz                                              |
| `errorMessage`  | `string` | Poruka greške pri učitavanju                                                       |
| `savedAds`      | `object` | Mapa `{ ad_id: bookmark_id }` za trenutnog studenta                                |
| `showOnlySaved` | `bool`   | Filter za prikaz samo sačuvanih oglasa                                             |
| `userRole`      | `string` | Uloga korisnika iz `localStorage` (`member` / `company` / `admin` / `guest`)       |

---

#### Computed

| Svojstvo      | Opis                                                                                   |
| ------------- | -------------------------------------------------------------------------------------- |
| `isStudent`   | `true` ako je `userRole === 'member'` — kontroliše vidljivost bookmark funkcionalnosti |
| `fields`      | Jedinstvene vrijednosti `field` polja iz liste oglasa — koristi se za dropdown filter  |
| `filteredAds` | Oglasi filtrirani po tabu, pretrazi, plaćenosti, oblasti i bookmark statusu            |

##### Logika filtriranja u `filteredAds`

| Filter          | Opis                                                                    |
| --------------- | ----------------------------------------------------------------------- |
| Tab             | Mapiranje taba na `typeKey` ili `statusKey` oglasa                      |
| Pretraga        | Case-insensitive pretraga po `title`, `company`, `description` i `tags` |
| `isPaid`        | Prikazuje samo oglase koji imaju `compensation`                         |
| `selectedField` | Tačno podudaranje s `field` oglasom                                     |
| `showOnlySaved` | Prikazuje samo oglase čiji `id` postoji u `savedAds`                    |

---

#### Metode

| Metoda                          | Opis                                                                                         |
| ------------------------------- | -------------------------------------------------------------------------------------------- |
| `fetchAdsAndBookmarks()`        | Dohvata oglase i mapira ih za prikaz; ako je korisnik student, paralelno dohvata i bookmarke |
| `handleToggleBookmark(payload)` | Dodaje ili uklanja bookmark — prima `{ adId, bookmarkId }`, ažurira `savedAds` optimistično  |

---

#### Mapiranje oglasa

Svaki oglas s API-ja mapira se u lokalni objekt:

| Polje              | Izvor                     | Opis                                                     |
| ------------------ | ------------------------- | -------------------------------------------------------- |
| `id`               | `ad.id`                   | —                                                        |
| `title`            | `ad.title`                | —                                                        |
| `company`          | `ad.company_name`         | Fallback na `Kompanija #{id}`                            |
| `company_id`       | `ad.company_id`           | —                                                        |
| `description`      | `ad.description`          | —                                                        |
| `tags`             | `[ad.field, ad.location]` | Koriste se za prikaz i pretragu                          |
| `typeLabel`        | `formatType(ad.type)`     | Lokalizovani tip (`Praksa` / `Edukacija` / `Stipendija`) |
| `typeKey`          | `ad.type`                 | Originalna enum vrijednost za filtriranje                |
| `compensation`     | `formatCompensation(...)` | Formatirani iznos s valutom                              |
| `statusLabel`      | `formatStatus(ad.status)` | Lokalizovani status                                      |
| `statusKey`        | `ad.status`               | Originalna enum vrijednost za filtriranje                |
| `spots`            | `ad.spots`                | Broj slobodnih mjesta                                    |
| `applicants_count` | `ad.applicants_count`     | Broj prijavljenih                                        |

---

#### Helper funkcije (lokalne)

| Funkcija                              | Opis                                                                              |
| ------------------------------------- | --------------------------------------------------------------------------------- |
| `formatType(type)`                    | Mapira `internship / education / scholarship` u `Praksa / Edukacija / Stipendija` |
| `formatStatus(status)`                | Mapira status enum u bosanski naziv                                               |
| `formatCompensation(value, currency)` | Formatira iznos naknade s valutom, vraća prazan string ako nema naknade           |

---

#### Tab mapiranje

| Tab          | Filter                      |
| ------------ | --------------------------- |
| `Sve`        | Svi oglasi                  |
| `Prakse`     | `typeKey === 'internship'`  |
| `Edukacije`  | `typeKey === 'education'`   |
| `Stipendije` | `typeKey === 'scholarship'` |
| `Aktuelno`   | `statusKey === 'active'`    |

---

#### API pozivi

| Endpoint                 | Servis           | Opis                                      |
| ------------------------ | ---------------- | ----------------------------------------- |
| `GET /ads/`              | `getAds`         | Lista svih aktivnih oglasa                |
| `GET /bookmarks/`        | `getBookmarks`   | Bookmarki studenta (samo ako je `member`) |
| `POST /bookmarks/`       | `addBookmark`    | Dodavanje bookmarkа                       |
| `DELETE /bookmarks/{id}` | `removeBookmark` | Uklanjanje bookmarkа                      |

---

#### Komponente

| Komponenta   | Opis                                                                          |
| ------------ | ----------------------------------------------------------------------------- |
| `HeroBanner` | Hero sekcija na vrhu stranice                                                 |
| `AdFilter`   | Filter komponenta — `v-model` za `searchQuery`, `isPaid`, `selectedField`     |
| `AdCard`     | Kartica oglasa, prima `bookmarkId` i `canBookmark`, emituje `toggle-bookmark` |

---

#### Lifecycle

| Hook      | Opis                            |
| --------- | ------------------------------- |
| `mounted` | Poziva `fetchAdsAndBookmarks()` |

---

#### Napomene

- `savedAds` je mapa `{ ad_id: bookmark_id }` — `ad_id` za provjeru je li oglas sačuvan, `bookmark_id` za brisanje
- Bookmarki se dohvataju samo ako korisnik ima validan token i uloga mu je `member` — kompanije i admini ne vide bookmark funkcionalnost
- Tab `Aktuelno` filtrira po `statusKey === 'active'`, ne po datumu
- Horizontalni scroll tabova sakriven je custom CSS klasom `no-scrollbar`

---

### `AdView.vue`

**Putanja:** `src/views/ads/AdView.vue`  
**Ruta:** `/ads/:id`

Stranica s detaljima oglasa. Prikazuje sve informacije o oglasu, bookmark dugme za studente, i sekciju s prijavama za admina i kompaniju vlasnika oglasa.

---

#### Data

| Polje                 | Tip              | Opis                                            |
| --------------------- | ---------------- | ----------------------------------------------- |
| `loading`             | `bool`           | Indikator učitavanja oglasa                     |
| `errorMessage`        | `string`         | Poruka greške pri učitavanju                    |
| `ad`                  | `object \| null` | Mapiran oglas za prikaz                         |
| `isUserLoggedIn`      | `bool`           | Da li postoji `token` u `localStorage`          |
| `isCompanyLoggedIn`   | `bool`           | Da li postoji `company_token` u `localStorage`  |
| `userRole`            | `string \| null` | Uloga korisnika iz `localStorage`               |
| `applications`        | `array`          | Lista prijava na oglas                          |
| `loadingApplications` | `bool`           | Indikator učitavanja prijava                    |
| `applicationsError`   | `string`         | Poruka greške pri učitavanju prijava            |
| `companyToken`        | `string \| null` | Token kompanije iz `localStorage`               |
| `bookmarkId`          | `number \| null` | ID bookmarkа ako je oglas sačuvan, inače `null` |

---

#### Computed

| Svojstvo    | Opis                                                              |
| ----------- | ----------------------------------------------------------------- |
| `isAdmin`   | `true` ako je korisnik prijavljen i ima ulogu `admin`             |
| `userToken` | Vraća `company_token` ako je kompanija prijavljena, inače `token` |

---

#### Metode

| Metoda                        | Opis                                                                                                 |
| ----------------------------- | ---------------------------------------------------------------------------------------------------- |
| `fetchAd()`                   | Paralelno dohvata oglas i listu kompanija, mapira naziv kompanije, formatira polja za prikaz         |
| `fetchApplications()`         | Dohvata prijave za oglas — samo za admina ili kompaniju vlasnika, koristi odgovarajući token         |
| `checkBookmarkStatus()`       | Dohvata sve bookmarke studenta i provjerava da li je trenutni oglas sačuvan — postavlja `bookmarkId` |
| `toggleBookmark()`            | Dodaje ili uklanja bookmark ovisno o `bookmarkId` — optimistički ažurira lokalno stanje              |
| `getTypeClass(typeLabel)`     | Vraća Tailwind klase za badge tipa oglasa                                                            |
| `getStatusClass(statusLabel)` | Vraća Tailwind klase za badge statusa oglasa                                                         |

---

#### Mapiranje oglasa

| Polje          | Izvor                              | Opis                                          |
| -------------- | ---------------------------------- | --------------------------------------------- |
| `id`           | `ad.id`                            | —                                             |
| `title`        | `ad.title`                         | —                                             |
| `company`      | `companiesById.get(ad.company_id)` | Fallback na `Kompanija #{id}`                 |
| `company_id`   | `ad.company_id`                    | —                                             |
| `description`  | `ad.description`                   | —                                             |
| `tags`         | `[ad.field, ad.location]`          | —                                             |
| `typeLabel`    | `formatType(ad.type)`              | Lokalizovani tip                              |
| `statusLabel`  | `formatStatus(ad.status)`          | Lokalizovani status                           |
| `compensation` | `formatCompensation(...)`          | Formatirani iznos s valutom                   |
| `duration`     | `ad.duration_months`               | Format: `X mjeseci`, `null` ako nije navedeno |
| `location`     | `ad.location`                      | —                                             |
| `field`        | `ad.field`                         | —                                             |
| `requirements` | `ad.requirements`                  | —                                             |
| `benefits`     | `ad.benefits`                      | —                                             |
| `spots`        | `ad.spots`                         | —                                             |
| `deadline`     | `ad.deadline`                      | —                                             |

---

#### Prikaz prema ulozi

| Uloga              | Sidebar                            | Bookmark | Prijave            |
| ------------------ | ---------------------------------- | -------- | ------------------ |
| Neprijavljen gost  | Prikazuje se s pozivom na login    | Ne       | Ne                 |
| Student (`member`) | Prikazuje se s dugmetom za prijavu | Da       | Ne                 |
| Kompanija          | Ne prikazuje se                    | Ne       | Da (samo vlastite) |
| Admin              | Ne prikazuje se                    | Ne       | Da (sve)           |

---

#### API pozivi

| Endpoint                                                               | Servis                 | Opis                                   |
| ---------------------------------------------------------------------- | ---------------------- | -------------------------------------- |
| `GET /ads/{id}`                                                        | `getAdById`            | Detalji oglasa                         |
| `GET /companies/`                                                      | `getApprovedCompanies` | Mapiranje naziva kompanije             |
| `GET /applications/company/by-ad/{id}` ili `/applications/?ad_id={id}` | `getApplicationsByAd`  | Prijave za oglas (admin ili kompanija) |
| `GET /bookmarks/`                                                      | `getBookmarks`         | Provjera bookmark statusa              |
| `POST /bookmarks/`                                                     | `addBookmark`          | Dodavanje bookmarkа                    |
| `DELETE /bookmarks/{id}`                                               | `removeBookmark`       | Uklanjanje bookmarkа                   |

---

#### Komponente

| Komponenta        | Opis                                                                             |
| ----------------- | -------------------------------------------------------------------------------- |
| `ApplicationCard` | Kartica prijave — prima `application`, `token`, `is-company`, emituje `@updated` |

---

#### Lifecycle

| Hook      | Opis                                                                                                           |
| --------- | -------------------------------------------------------------------------------------------------------------- |
| `mounted` | Čita auth stanje iz `localStorage`, sekvencijalno poziva `fetchAd`, `fetchApplications`, `checkBookmarkStatus` |

---

#### Napomene

- Naziv kompanije se mapira kroz `Map` iz paralelnog poziva na `/companies/` — isti pattern kao u `ApplicationView`
- `checkBookmarkStatus` dohvata **sve** bookmarke studenta pa traži oglas po `ad_id` — nema direktan endpoint za provjeru jednog bookmarkа
- Sekcija s prijavama (`ApplicationCard`) prikazuje se samo adminima i kompanijama, a `fetchApplications` automatski bira endpoint i token ovisno o ulozi
- `toggleBookmark` je dostupan samo studentima — kompanijama i adminima bookmark ikona nije vidljiva

---

### `AdminAdsApprovalView.vue`

**Putanja:** `src/views/ads/AdminAdsApprovalView.vue`  
**Ruta:** `/admin/ads`  
**Meta:** `requiresAuth: true`, `requiresAdmin: true`

Administratorska stranica za upravljanje oglasima. Prikazuje sve oglase s filterima po statusu i omogućava odobravanje, odbijanje, brisanje i vraćanje oglasa.

---

#### Data

| Polje          | Tip      | Opis                                                                                   |
| -------------- | -------- | -------------------------------------------------------------------------------------- |
| `ads`          | `array`  | Lista svih oglasa (svaki ima dodatno polje `updating`)                                 |
| `loading`      | `bool`   | Indikator učitavanja                                                                   |
| `activeFilter` | `string` | Aktivni filter (`'Sve'` / `'Na čekanju'` / `'Odobreni'` / `'Odbijeni'` / `'Obrisani'`) |
| `errorMessage` | `string` | Poruka greške pri učitavanju                                                           |

---

#### Computed

| Svojstvo      | Opis                                                                               |
| ------------- | ---------------------------------------------------------------------------------- |
| `filteredAds` | Filtrira `ads` prema `activeFilter` — obrisani po `is_deleted`, ostali po `status` |

---

#### Metode

| Metoda                                 | Opis                                                                                           |
| -------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `fetchAds()`                           | Dohvata sve oglase kroz admin endpoint, dodaje `updating: null` i `is_deleted` na svaki objekt |
| `filterCount(filter)`                  | Vraća broj oglasa za svaki filter — koristi se za prikaz brojača na dugmadima                  |
| `statusLabel(status)`                  | Mapira status enum u bosanski naziv za prikaz                                                  |
| `statusBadgeClass(status)`             | Vraća Tailwind klase za badge statusa oglasa                                                   |
| `updateAdStatusHandler(ad, newStatus)` | Šalje `PATCH` za promjenu statusa (`active` / `rejected`), ažurira lokalni objekt              |
| `deleteAdHandler(ad)`                  | Soft delete oglasa — postavlja `is_deleted` na `true` lokalno nakon uspješnog API poziva       |
| `restoreAdHandler(ad)`                 | Vraća obrisani oglas — postavlja `is_deleted` na `false` i status na `pending`                 |

---

#### API pozivi

| Endpoint                 | Servis              | Opis                                   |
| ------------------------ | ------------------- | -------------------------------------- |
| `GET /me`                | `getMe` iz `api.js` | Provjera uloge korisnika pri mountanju |
| `GET /ads/admin/list`    | Direktan `fetch`    | Lista svih oglasa                      |
| `PATCH /ads/{id}/status` | Direktan `fetch`    | Promjena statusa oglasa                |
| `DELETE /ads/{id}`       | Direktan `fetch`    | Soft delete oglasa                     |
| `POST /ads/{id}/restore` | Direktan `fetch`    | Vraćanje obrisanog oglasa              |

---

#### Filter mapiranje

| Label        | Filter                  |
| ------------ | ----------------------- |
| `Sve`        | Svi oglasi              |
| `Na čekanju` | `status === 'pending'`  |
| `Odobreni`   | `status === 'active'`   |
| `Odbijeni`   | `status === 'rejected'` |
| `Obrisani`   | `is_deleted === true`   |

---

#### Status mapiranje

| Status     | Label      | Badge boja |
| ---------- | ---------- | ---------- |
| `pending`  | Na čekanju | Žuta       |
| `active`   | Odobren    | Zelena     |
| `rejected` | Odbijen    | Crvena     |
| —          | Obrisano   | Siva       |

---

#### Lifecycle

| Hook      | Opis                                                                                                    |
| --------- | ------------------------------------------------------------------------------------------------------- |
| `mounted` | Dohvata trenutnog korisnika kroz `getMe`, ako nije admin preusmjerava na `/`, inače poziva `fetchAds()` |

---

#### Napomene

- Dvostruka zaštita pristupa — ruta ima `requiresAdmin` guard, ali `mounted` dodatno provjerava ulogu kroz API poziv, identično kao `AdminCompanyApprovalView`
- Dugmad za odobravanje i odbijanje prikazuju se samo za oglase sa statusom `pending` koji nisu obrisani
- `BASE_URL` je hardkodiran lokalno unutar komponente pored centralnog u `api.js` — potencijalno mjesto za refaktor
- Sve akcije ažuriraju lokalni objekt optimistično bez ponovnog učitavanja cijele liste
- Polje `updating` na svakom oglasu koristi se za disabled stanje dugmadi i prikaz loading teksta za vrijeme API poziva


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
