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
### Tim 2 — Materijali (Marinela Mitić)

#### Pregled

Ovaj dio dokumentacije opisuje frontend implementaciju koju je radila Marinela Mitić u okviru Tim 2 — modul Materijali. Implementacija obuhvata formu za dodavanje materijala s validacijom, dugme za preuzimanje, komponentu za ocjenjivanje (zvjezdice), prikaz thumbnail sličica te dark mode stilizaciju svih komponenti modula.

Korištene tehnologije: **Vue 3** (Composition API i Options API), **Vue Router**, **Tailwind CSS**.

Relevantne komponente:
- `components/MaterialUploadForm.vue` — forma za dodavanje materijala
- `components/DownloadButton.vue` — preuzimanje fajla
- `components/MaterialRating.vue` — ocjenjivanje zvjezdicama
- `views/materials/MaterialDetail.vue` — prikaz thumbnaila i povezivanje komponenti
- `services/api.js` — API funkcije za komunikaciju s backendom

---

#### Sprint 1 — Forma za dodavanje materijala i preuzimanje

##### `MaterialUploadForm.vue` — forma s validacijom obaveznih polja

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

**Drag & drop:** Implementirana zona za prevlačenje fajla (`onFileDrop`, `triggerFileInput`, `onFileChange`). Stvarni `<input type="file">` je skriven (`class="hidden"`), a vidljiva drag zona programski pokreće njegov klik — čime se dobija prilagođen izgled umjesto stilski ograničenog nativnog inputa.

**Slanje (`handleSubmit`):** Kreira `FormData` (zbog `multipart/form-data` slanja fajla) i šalje na backend. Greške se mapiraju po HTTP statusu:

| Status | Poruka korisniku |
|---|---|
| `401` | Token istekao — korisnik se preusmjerava na login |
| `400` | Format fajla nije podržan |
| `409` | Materijal s tim nazivom/fajlom već postoji |

> **Napomena:** Godina studija (`studyYear`) se ne šalje na backend — služi samo kao filter za sužavanje liste predmeta (`filteredSubjects`), jer je godina već vezana za predmet u bazi.

##### `DownloadButton.vue` — preuzimanje fajla

Komponenta koja preuzima fajl koristeći **blob download** obrazac. Kada korisnik klikne "PREUZMI":

1. Dugme se onemogućava (`isDownloading`) da spriječi dvostruki klik
2. Poziva se `downloadMaterial` (api.js) — šalje token kroz URL radi bilježenja preuzimanja
3. Provjerava se HTTP status (`403`, `404`) i mapira na korisničku poruku
4. Iz `Content-Disposition` zaglavlja se regexom izvlači originalni naziv fajla (sa `decodeURIComponent` za specijalne znakove), uz rezervni naziv `material-{id}`
5. Odgovor se pretvara u `blob`, kreira se privremeni objektni URL, pravi nevidljivi `<a download>` element koji se programski klikne da pokrene preuzimanje, te se memorija oslobađa s `revokeObjectURL`
6. Emituje se događaj `@downloaded` prema roditeljskoj komponenti

**Zašto blob umjesto običnog linka:** Direktan `<a href>` ne bi omogućio slanje tokena niti obradu grešaka (403/404) s prikazom poruke. Blob pristup daje punu kontrolu nad zahtjevom i odgovorom.

---

#### Sprint 2 — Ocjenjivanje (komponenta zvjezdica)

##### `MaterialRating.vue`

Komponenta prikazuje prosječnu ocjenu materijala (read-only zvjezdice + brojčani prikaz, npr. "4.2 / 5.0 (12 ocjena)") i interaktivne zvjezdice za ocjenjivanje.

**Zaključavanje zvjezdica** ovisi o stanju korisnika. Zvjezdice su aktivne samo kada je korisnik prijavljen i kada je preuzeo materijal:

```html
:class="(isLoggedIn && hasDownloaded) ? 'cursor-pointer' : 'cursor-not-allowed opacity-50'"
```

Prikazuju se i odgovarajuće poruke ovisno o stanju:

| Stanje korisnika | Prikaz |
|---|---|
| Prijavljen, preuzeo materijal | Aktivne zvjezdice |
| Prijavljen, nije preuzeo | Poruka "Preuzmite materijal da biste mogli ocijeniti." |
| Nije prijavljen | Link "Prijavite se..." |

**Provjera preuzimanja:** U `onMounted` se poziva `checkHasDownloaded` (backend `/has-downloaded`) i postavlja `hasDownloaded`. Dodatno, `watch` prati `parentHasDownloaded` prop — kada korisnik preuzme materijal na istoj stranici, zvjezdice se otključavaju u realnom vremenu, bez osvježavanja stranice.

**Promjena ocjene:** Ako korisnik već ima ocjenu i klikne ponovo, otvara se modal za potvrdu ("Želite li promijeniti ocjenu?"). Potvrdom se poziva `updateRating` (`PATCH`), dok prvo ocjenjivanje koristi `rateMaterial` (`POST`).

**Vlastiti materijal:** Komponenta provjerava vlasništvo (poređenjem `user_id` iz JWT tokena s autorom materijala) i sprječava ocjenjivanje vlastitog materijala uz poruku.

> **Napomena o slojevima zaštite:** Zaključavanje zvjezdica na frontendu služi korisničkom iskustvu, ali stvarna zaštita je na backendu — endpoint `/rate` neovisno provjerava `Download` tabelu i vraća `403` čak i ako se frontend zaobiđe (npr. direktnim API pozivom). Provjera vlasništva materijala trenutno se provodi na frontendu.

##### Prikaz broja preuzimanja

Na kartici materijala prikazuje se brojač preuzimanja ("Broj preuzimanja: X"), vezan za polje `number_of_downloads` koje backend povećava pri svakom preuzimanju. Nakon uspješnog preuzimanja brojač se ažurira i lokalno (`updateDownloadCount`), bez potrebe za osvježavanjem stranice.

---

#### Sprint 3 — Thumbnail prikaz, validacija dužine i dark mode

##### Dodatna validacija forme (dužina polja)

U Sprintu 3 osnovna validacija obaveznih polja (iz Sprinta 1) proširena je provjerom minimalne i maksimalne dužine teksta, uz konkretne poruke korisniku:

| Polje | Pravilo |
|---|---|
| Naziv | Najmanje 3, najviše 100 karaktera |
| Opis | Najmanje 10, najviše 1000 karaktera |

Ako polje ne zadovoljava dužinu, u `errors` se umjesto `true` upisuje tekstualna poruka (npr. "Naziv mora imati najmanje 3 karaktera."), koja se prikazuje ispod polja. Validacija se ponovo pokreće reaktivno (`watch`) čim korisnik ispravlja unos.

##### Prikaz thumbnail sličice (`MaterialDetail.vue`)

Thumbnail se prikazuje samo ako postoji (`v-if="material.thumbnail_path"`):

```html
<img :src="`http://127.0.0.1:8000/thumbnails/${material.thumbnail_path.split('/').pop()}`" ... />
```

Iz pune putanje koju vraća backend (`uploads/thumbnails/ime.png`) izvlači se samo naziv fajla (`split('/').pop()`) i lijepi na `/thumbnails/` statičku rutu servera.

##### Povezivanje preuzimanja i ocjenjivanja

`MaterialDetail.vue` povezuje `DownloadButton` i `MaterialRating` u jedinstven tok:

```html
<DownloadButton @downloaded="updateDownloadCount" />
<MaterialRating :parent-has-downloaded="hasDownloaded" />
```

Funkcija `updateDownloadCount` se okida na `@downloaded` događaj, povećava lokalni brojač preuzimanja i postavlja `hasDownloaded = true`. To se prosljeđuje `MaterialRating` komponenti kao prop, čime se zvjezdice odmah otključavaju — implementacija pravila "preuzmi pa ocijeni" bez osvježavanja stranice (komunikacija roditelj↔dijete: props naniže, emit naviše).

##### Dark mode stilizacija

Sam mehanizam prebacivanja teme (toggle koji postavlja `dark` klasu) razvio je drugi član tima. Lično implementirani dio je **dark mode stilizacija svih komponenti modula Materijali** — ručno dodavanje Tailwind `dark:` varijanti (`dark:bg-...`, `dark:text-...`, `dark:border-...`) na sve elemente: formu za upload, sve modale i poruke (potvrda ocjene, uspjeh, greške) pojedinačno, kartice materijala (i detaljna kartica i obična kartica u listi), stranicu s detaljima i komponentu ocjenjivanja. Svaka poruka i komponenta gdje je bilo potrebno obrađena je zasebno, čime je osigurano da cijeli modul ispravno i čitljivo izgleda u tamnom režimu.

---

#### API funkcije (`services/api.js`)

| Funkcija | Endpoint | Opis |
|---|---|---|
| `uploadMaterial(formData)` | `POST /materials/upload` | Slanje novog materijala |
| `downloadMaterial(materialId)` | `GET /materials/{id}/download` | Preuzimanje (token + cache-busting `t=`) |
| `checkHasDownloaded(materialId)` | `GET /materials/{id}/has-downloaded` | Provjera da li je korisnik preuzeo |
| `rateMaterial(materialId, rating)` | `POST /materials/{id}/rate` | Slanje ocjene |
| `updateRating(materialId, rating)` | `PATCH /materials/{id}/rate` | Izmjena ocjene |

Funkcije `rateMaterial` i `updateRating` vraćaju sirovi `response` (ne parsirani JSON) kako bi komponenta mogla razlikovati statuse (npr. `409` — već ocijenjeno). `downloadMaterial` dodaje `t={timestamp}` na URL radi izbjegavanja keširanja preglednika — bez toga se ponovljeno preuzimanje ne bi zabilježilo na backendu.
