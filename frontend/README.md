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

## Forum API (src/services/forum.js)

Osnovni URL: http://127.0.0.1:8000 (hardkodiran). Token se čita iz **localStorage (token ili access_token)**. Svi zahtjevi uključuju **Authorization: Bearer <token>** i Content-Type: application/json (osim uploada).

| Funkcija                                          | Metoda   | Endpoint                       | Opis                                           |
| ------------------------------------------------- | -------- | ------------------------------ | ---------------------------------------------- |
| `getCategories()`                                 | `GET`    | `/forum/categories`            | Lista svih kategorija                          |
| `getTopics({ category_id, search, page, per_page, sort_by, unanswered, days_old })`                     | `GET`   | `/forum/topics`   | Paginirana lista tema sa filterima                           |
| `getTopicById(id)`                   | `GET`   | `/forum/topics/{id}` | Detalji jedne teme                        |
| `incrementTopicView(id)`                       | `PATCH` | `/forum/topics/{id}/view`            | Povećava broj pregleda                      |
|   `deleteTopic(topicId)`	                 |     `DELETE`	       |           `/forum/topics/{topicId}`	   |          Brisanje teme               |
|   `createTopic(topicData)`	        |        `POST`	    |    `/forum/topics`	      |    `Kreiranje nove teme`                                           |
|    `createComment(commentData)`	     |         `POST`	   |       `/forum/comments`	  |          Dodavanje komentara (moguć parent_id za odgovore)    |
|    `voteOnComment(commentId, value)`	|    `POST`	    |    `/forum/comments/{commentId}/vote`	  |    Glas za komentar (value: 1 ili -1)                |
|    `toggleTopicLike(topicId)`         | 	`POST`       |   	`/forum/topics/{topicId}/like`     | 	Like / uklanjanje like-a teme                         |
|    `toggleTopicDislike(topicId)`       |        	`POST`  |	`/forum/topics/{topicId}/dislike`  |	Dislike / uklanjanje dislike-a teme                         |
|    `toggleBestAnswer(commentId)`	|  `PATCH`  |	`/forum/comments/{commentId}/best-answer` |	Označava/uklanja najbolji odgovor                                 |
|    `getPopularTags()`	| `GET`	 | /forum/tags |	`Popularni tagovi`                                                           |
|    `deleteComment(commentId)` |	`DELETE` |	`/forum/comments/{commentId}` |	Brisanje komentara  |
|    `updateComment(commentId, content)` |	`PUT` |	`/forum/comments/{commentId}` |	Izmjena komentara    |
|    `reportTopic(topicId, reason)` |	`POST` |	`/forum/topics/{topicId}/report` |	Prijava teme za neprimjeren sadržaj     |
|    `getActiveAnnouncements()` |	`GET`	| `/forum/topics/announcements/active` |	Aktivna admin obaveštenja     |
|    `getActiveReports()` |	`GET` |	`/forum/topics/reports/active` |	Aktivne prijave (admin)        |
|    `handleReportAction(reportId, action, explanation)` |	`PATCH`	 | `/forum/topics/reports/{reportId}/action?action={action}` |	Rješavanje prijave    |
|    `getSearchSuggestions(query)` |	`GET` |	`/forum/topics/suggestions` |	Prijedlozi za pretragu (popularne, aktivne, filtrirane)             |
|    `getPopularTopics()` |	`GET` |	`/forum/topics/popular` |	Globalne popularne teme (7 dana)             |
|    `getCategoryPopularTopics(categoryId)` |	`GET`  |	`/forum/topics/category-popular/{categoryId}` |	Popularne teme u kategoriji           |
|    `getRelatedTopics(topicId)` |	`GET` |	`/forum/topics/{topicId}/related` |	Slične teme unutar otvorene teme                 |
|    `updateTopic(topicId, data)` |	`PUT` |	`/forum/topics/{topicId}` |	Izmjena teme                  |
|    `uploadTopicAttachments(topicId, files)` |	`POST` |	`/forum/attachments/topic/{topicId}` |	Upload priloga uz temu (multipart/form-data)         |
|    `uploadCommentAttachments(commentId, files)` |	`POST`	| `/forum/attachments/comment/{commentId}` |	Upload priloga uz komentar                      |
    
---

## Forum Admin API (src/services/forum_admin.js)


| Funkcija                                          | Metoda   | Endpoint                       | Opis                                           |
| ------------------------------------------------- | -------- | ------------------------------ | ---------------------------------------------- |
| `getUsers()`	| `GET`	| `/admin/users` |	Lista svih korisnika |
| `changeUserRole(userId, role)`	| `PATCH` |	`/admin/users/{userId}/role?role={role}` |	Promjena uloge |
| `getReports(status)` |	`GET`	| `/admin/reports?status={status}` |	Prijave po statusu |
| `dismissReport(reportId)` |	`DELETE` |	`/admin/reports/{reportId}` |	Odbacivanje prijave |
| `toggleTopicLock(topicId)` |	`PATCH` |	`/admin/topics/{topicId}/lock` |	Zaključavanje/otključavanje teme |
| `createAnnouncement(title, content, durationDays)` |	`POST` |	`/admin/announcements` |	Globalno obavještenje |
| `getAllAnnouncements()` |	`GET` |	`/admin/announcements/all` |	Sva obavještenja  |
| `updateAnnouncement(annId, data)` |	`PATCH` |	`/admin/announcements/{annId}` |	Izmjena obavještenja |
| `deleteAnnouncement(annId)` |	`DELETE` |	`/admin/announcements/{annId}` |	Brisanje obavještenja |
| `getHandledReports()` |	`GET` |	`/admin/reports?status=resolved` |	Riješene prijave |
| `getGuidelines()` |	`GET` |	`/forum/guidelines/` |	Pravila foruma |
| `createGuideline(title, content, order)` |	`POST` |	`/forum/guidelines/` |	Dodavanje pravila |
| `updateGuideline(id, data)` |	`PATCH` |	`/forum/guidelines/{id}` |	Izmjena pravila  |
| `deleteGuideline(id)` |	`DELETE` |	`/forum/guidelines/{id}` |	Brisanje pravila |
| `postAdminNotice(topicId, content)` |	`POST` |	`/forum/comments/{topicId}/admin-notice` |	Admin obavještenje unutar teme |
| `adminPullToReports(topicId)` |	`POST` |	`/admin/topics/{topicId}/pull-to-reports` |	Povlačenje teme u prijave |
| `reopenReport(reportId)` |	`PATCH` |	`/admin/reports/{reportId}/reopen` |	Vraćanje riješene prijave u aktivne |
| `resolveReport(reportId, action, explanation)` |	`PATCH` |	`/admin/reports/{reportId}/resolve` |	Rješavanje prijave uz objašnjenje |


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

---

### `ForumSidebar.vue`

**Putanja:** `src/components/ForumSidebar.vue`

Prikazuje listu kategorija foruma i popularne tagove. Klikom na kategoriju emituje kategorija-izabrana sa ID-jem 
(ili null za „Sve teme”). Klik na tag emituje njegovo ime. Podaci se pribavljaju paralelno pri mountovanju.

---

#### Props 

| Param              | Tip | Opis                                  |
| ------------------ | -------- | ------------------------------------- |
| `aktivnaKategorijaId` | Number/null | Trenutno odabrana kategorija |

---

#### Data

| Polje          | Tip      | Opis                                                                                   |
| -------------- | -------- | -------------------------------------------------------------------------------------- |
| `categories`   | `array`  | Lista kategorija sa `id`, `name`, `color`, `topic_count`                               |
| `popularTags`  | `array`  | Popularni tagovi (svaki sadrži `id`, `name`, `topics_count`                            |
| `loading`      | `Boolean`| Indikator učitavanja                                                                   |

---

#### Emitovani event-i

| Event             | Vrijednost                                  |
| ------------------ | ------------------------------------- |
| `kategorija-izabrana` | CategoryId (number) ili null |
| `tag-izabran` | tagName (String) |

---

#### API pozivi

| Endpoint                 | Servis              | Opis                                   |
| ------------------------ | ------------------- | -------------------------------------- |
| `GET /forum/categories`  | `getCategories`     | Dohvatanje svih kategorija na forumu   |
| `GET /forum/tags`        | `getPopularTags`    | Lista svih oglasa                      |

---

#### Lifecycle

| Hook      | Opis                                                                                                    |
| --------- | ------------------------------------------------------------------------------------------------------- |
| `mounted` | Paralelno poziva `getCategories()` i `getPopularTags()`                                                 |

---

### `ForumTopicCard.vue`

**Putanja:** `src/components/ForumTopicCard.vue`

Kartica teme u listi foruma. Prikazuje naslov, sadržaj, kategoriju, tagove, autora (sa medaljama i XP), broj pregleda, lajkova/dislajkova 
i komentara. Admin može obrisati temu direktno.

---

#### Props 

| Param              | Tip | Opis                                  |
| ------------------ | -------- | ------------------------------------- |
| `tema` | Object | Objekat teme sa svim poljima |
| `isAdmin` | Boolean | Da li je trenutni korisnik admin |

---

#### Emitovani event-i

| Event             | Vrijednost                                  |
| ------------------ | ------------------------------------- |
| `obrisi` | topicId |

---

#### Napomene
 - Medalje autora se prikazuju ikonama (🥇🥈🥉) uz tooltip sa punim naslovom i uslovom.
 - Padajući meni za preostale medalje (više od 3) kontroliše se lokalnim `showAllMedalsDropdown`.

---

### `ForumTopicMainCard.vue`

**Putanja:** `src/components/ForumTopicMainCard.vue`

Glavna kartica teme na stranici detalja teme. Prikazuje kompletan sadržaj teme, priloge (koristi `ForumAttachmentPreview`), akcije za interakciju (like/dislike, odgovori, dijeljenje, prijava, zaključavanje, uređivanje, brisanje). Podržava inline editovanje i formu za odgovor na temu.


---

#### Props 

| Param              | Tip | Opis                                  |
| ------------------ | -------- | ------------------------------------- |
| `topic` | Object | Objekat teme |
| `isAdmin` | Boolean | Da li je trenutni korisnik admin |

---

#### Emitovani event-i

| Event             | Vrijednost                                  |
| ------------------ | ------------------------------------- |
| `submit-topic-reply` | { content, files, onSuccess, onError } |
| `refresh` | - |

---

#### Data

| Polje          | Tip      | Opis                                                                                   |
| -------------- | -------- | -------------------------------------------------------------------------------------- |
| `currentUserId`| `Number/null`| ID prijavljenog korisnika (dohvaćen sa `me`)                               |
| `isReplyingToTopic`  | `Boolean`  | Da li je otvorena forma za odgovor na temu                            |
| `isEditingTopic`      | `Boolean`| Da li je aktivan inline edit                                                   |
| `showShareBox`  | `Boolean`  | Vidljivost opcija za dijeljenje                            |
| `showReportOptions`      | `Boolean`| Vidljivost padajućeg menija za prijavu                                       |

---

#### Metode

| Metoda                                 | Opis                                                                                           |
| -------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `handleTopicLike()`                           | Poziva `toggleTopicLike`, ažurira `topic.likes_count`, `is_liked`, itd. |
| `handleTopicDislike()`                  | Isto za dislike-ove           |
| `startEditTopic()`                  |    Aktivira inline edit (postavlja `isEditingTopic`, kopira naslov i sadržaj)                                               |
| `submitEditTopic()`             | Poziva `updateTopic` i ažurira lokalni objekat teme                                                  |
| `handleDeleteTopic()` | Poziva `deleteTopic` i preusmjerava na `/forum`           |


---

#### API pozivi

| Endpoint                 | Servis              | Opis                                   |
| ------------------------ | ------------------- | -------------------------------------- |
| `GET /me`  | fetch direktno     | Dohvatanje korisnika   |
| `POST /forum/topics/{id}/like`        | `toggleTopicLike`    | Za like-anje teme              |
| `POST /forum/topics/{id}/dislike`        | `toggleTopicDislikeLike`    | Za dislike-anje teme          |
| `PUT /forum/topics/{id}`        | `updateTopic`    | Update-anje teme              |
| `DELETE /forum/topics/{id}`        | `deleteTopic`    | Brisanje teme              |
| `POST /forum/topics/{id}/report`        | `reportTopic`    | Za report-anje teme              |
| `PATCH /admin/topics/{id}/lock`        | `toggleTopicLock`    | Zaključavanje teme od strane admina           |

---

#### Komponente

| Komponenta        | Opis                                                                             |
| ----------------- | -------------------------------------------------------------------------------- |
| `ForumAvatar` | Avatar autora |
| `ForumCommentForm` | Forma za odgovor na temu |
| `ForumAttachementPreview` | Pregled priloga teme |

---

#### Napomene
 - Like/dislike koriste optimistički update lokalnog objekta `topic`.
 - Dijeljenje podržava kopiranje linka i platforme: Facebook, Messenger, WhatsApp, Viber.
 - Samo admin vidi dugme za zaključavanje/otključavanje teme.
 - Samo autor (ili admin) može uređivati i brisati temu.

---


### `ForumTopicCommentsList.vue`

**Putanja:** `src/components/ForumTopicCommentsList.vue`

Lista komentara teme sa pretragom. Upravlja glasanjem, označavanjem najboljeg odgovora, odgovaranjem, uređivanjem i brisanjem komentara. Podržava highlight komentara iz URL heša (notifikacije).


##
---

#### Props 

| Param              | Tip | Opis                                  |
| ------------------ | -------- | ------------------------------------- |
| `comments` | Array | Niz komentara |
| `topicAuthorId` | Number/null | ID kreatora teme |
| `topicId` | Number/null | ID teme |
| `highlightedCommentId` | Number/null | ID komentara |

---

#### Emitovani event-i

| Event             | Vrijednost                                  |
| ------------------ | ------------------------------------- |
| `refresh` | - |

---

#### Data

| Polje          | Tip      | Opis                                                                                   |
| -------------- | -------- | -------------------------------------------------------------------------------------- |
| `searchQuery`| `String`| Tekst za pretragu komentara po sadržaju                               |
| `currentUserId`  | `Number/null`  | ID prijavljenog korisnika                            |
| `currentUserRole`  | `String` | Uloga korisnika                                             |
| `editingCommentId`  | `Number/null`  | ID komentara koji se trenutne uređuje                            |
| `replyingToId`      | `Number/null` | ID komentara na koji se odgovara                                       |

---


#### Metode

| Metoda                                 | Opis                                                            |
| -------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `handeVote(comment, value)`         | Poziva `voteOnComment`, ažurira lokalno stanje glasova i emituje refresh. |
| `handleBestAnswer(comment)`       | Poziva `toggleBestAnswer` (samo autor teme).        |
| `handleDeleteComment(comment)`      | Poziva `deleteComment` i emituje refresh.                      |
| `handleSubmitReply(comment, text, files)`      | Kreira komentar sa `parent_id`, uploaduje priloge, emituje refresh.                                                  |
| `handleSubmitEdit(commentId, newContent)` | Poziva `updateComment` i emituje refresh.           |


---

#### API pozivi

| Endpoint                 | Servis              | Opis                                   |
| ------------------------ | ------------------- | -------------------------------------- |
| `GET /me`  | fetch direktno     | Dohvatanje korisnika   |
| `POST /forum/comments/{id}/vote`        | `voteOnComment`    | Za like-anje komentara              |
| `PATCH /forum/comments/{id}/best-answer`  | `toggleBestAnswer`    | Najbolji odgovor          |
| `DELETE /forum/comments/{id}`        | `deleteComment`    | Brisanje komentara              |
| `PUT /forum/comments/{id}`        | `updateComment`    | Edit-ovanje komentara             |
| `POST /forum/comments`        | `createComment`    | Kreiranje komentara              |
| `POST /forum/attachments/comment/{id}`        | `uploadCommentAttachments`    | Dodavanje priloga komentaru |

---

#### Napomene
 - Admin vidi sve komentare (uključujući admin notice), ali ne može odgovarati.
 - Komentari tipa `is_admin_notice` imaju poseban stil i onemogućeno odgovaranje.

---

### `ForumCommentNode.vue`

**Putanja:** `src/components/ForumCommentNode.vue`

Rekurzivna komponenta za prikaz jednog komentara i njegovih odgovora. Podržava glasanje, označavanje najboljeg odgovora, uređivanje, brisanje, odgovaranje s prilozima, prikaz medalja autora.

---

#### Props 

| Param              | Tip | Opis                                  |
| ------------------ | -------- | ------------------------------------- |
| `comment` | Object | Komentar |
| `currentUserId` | Number/null | ID prijavljenog korisnika |
| `isAdmin` | Boolean | Admin status |
| `isTopicAuthor` | Boolean | Da li je korisnik autor teme |
| `depth` | Number | Nivo ugnježdenja (0 za root) |
| `getUserVote` | Function | Vraća trenutni glas korisnika za ovaj komentar |
| `getLikesCount` | Function | Vraća broj like-ova |
| `getDislikesCount` | Function | Vraća broj dislike-ova |


---

#### Emitovani event-i

| Event             | Vrijednost                                  |
| ------------------ | ------------------------------------- |
| `vote`  | { `comment`, `value` }         |
| `best-answer`  | { `comment` }         |
| `delete`  | { `comment` }         |
| `start-edit`  | { `commentId` }         |
| `cancel-edit`  | -         |
| `submit-edit`  | { `commentId`, `newContent` }         |
| `start-reply`  | { `commentId` }         |
| `cancel-reply`  | -         |
| `submit-reply`  | { `comment`, `replyText`, `files` }         |
| `toggle-medals`  | { `medalKey` }         |


---

#### Napomene
 - Ako je comment.is_best_answer, prikazuje se žuti badge i zvjezdica.
 - Ako je comment.is_deleted, prikazuje se "deleted by user" i sakrivaju se akcije.
 - Medalje se prikazuju do 3, a ostale u padajućem meniju.
 - Administratorska obavještenja (`is_admin_notice`) renderuju se izdvojeno u roditeljskoj komponenti, ne kroz ovaj čvor.


### `ForumTopicCommentForm.vue`

**Putanja:** `src/components/ForumTopicCommentsForm.vue`

Forma za unos odgovora (koristi se unutar `ForumTopicMainCard` i `ForumCommentNode`). Sadrži textarea i upload priloga (max 3 fajla, 5MB).

---

#### Props 

| Param              | Tip | Opis                                  |
| ------------------ | -------- | ------------------------------------- |
| `isSubmitting` | Boolean | Indikator slanja |
| `commentError` | String | Greška validacije |
| `successMessage` | String | Poruka uspjeha |

---

#### Emitovani event-i

| Event             | Vrijednost                                  |
| ------------------ | ------------------------------------- |
| `posaljiKomentar`  | { content, files, clearForm }         |
| `otkazi` | - |

---

#### Napomena
 - Validacija fajlova se vrši klijentski (ekstenzija, veličina, broj).
 - `clearForm` callback se poziva nakon uspješnog slanja da resetuje polja.

---

### `ForumAttachementPreview.vue`

**Putanja:** `src/components/ForumAttachementPreview.vue`

Prikazuje grid priloga (slike, PDF, TXT, DOCX) sa thumbnail-ovima. Klik otvara modal za pregled (slike, PDF) ili preuzimanje. Ostali tipovi prikazuju ikonu i nude direktno preuzimanje. Za TXT fajlove učitava se prvih 200 karaktera kao mini preview.

---

#### Props 

| Param              | Tip | Opis                                  |
| ------------------ | -------- | ------------------------------------- |
| `attachments` | Array | Niz objekata priloga (mime_type, filename, file_size, id) |
| `downloadBaseUrl` | String | Bazni URL za download |

---

#### Napomene
 - Modal se otvara pomoću `<teleport to="body">`.
 - U modalu se za slike koristi `<img>`, a za PDF `<iframe>`.
 - Komponenta ne emituje događaje; sve akcije (download) su samostalne.

### `ForumAvatar.vue`

**Putanja:** `src/components/ForumAvatar.vue`

Prikazuje avatar korisnika (sliku ili inicijale). Ako backend ne vrati URL, pokušava ga dohvatiti sa `/profiles/{id}/public` koristeći token iz localStorage-a.

---

#### Props 

| Param              | Tip | Opis                                  |
| ------------------ | -------- | ------------------------------------- |
| `author` | Object | Objekat autora |

---

#### Napomene
 - Koristi `axios` za dohvatanje javnog profila (sa `Authorization` headerom).
 - Ako slika ne može da se učita, pada nazad na inicijale (izračunate iz `full_name`).

---

### `ForumFilters.vue`

**Putanja:** `src/components/ForumFilters.vue`

Dropdown filteri za listu tema: 
 - Sortiranje: najnovije, najgledanije, najaktivnije (radio dugmad, moguće odznačiti ponovnim klikom).
 - Stanje: checkbox „Bez odgovora“.
 - Maksimalna starost: brojčani input sa ✕ za brisanje vrednosti.
 - Dugme „Poništi sve“ za reset na podrazumijevane vrednosti.

---

#### Emitovani event-i

| Event             | Vrijednost                                  |
| ------------------ | ------------------------------------- |
| `filters-changed`  | { sort_by, unanswered, days_old }         |

---

#### Napomene
 - Filteri su `reactive`; svaka promjena automatski emituje novi objekat filtera.
 - Klik van komponente zatvara popover.

### `ForumSearchDropdown.vue`

**Putanja:** `src/components/ForumSearchDropdown.vue`

Polje za pretragu sa padajućim sugestijama. Na prazan unos prikazuje najgledanije i najaktivnije teme. Tokom kucanja šalje zahtjev za filtrirane sugestije (sa debounce-om od 250 ms). Enter ili klik na lupu emituje `search-submitted` i zatvara dropdown.

---

#### Emitovani event-i

| Event             | Vrijednost                                  |
| ------------------ | ------------------------------------- |
| `search-submitted`  | query (String)         |

---

#### API pozivi

| Endpoint             | Servis                                  |
| ------------------ | ------------------------------------- |
| `GET /forum/topics/suggestions`  | `getSearchSuggestions`         |

---

#### Napomene
 - Koristi `AbortController` za otkazivanje prethodnog zahtjeva pri brzom kucanju.
 - Klik na stavku u dropdown-u vodi direktno na tu temu preko Vue Routera (named route `topic-detail`).

### `ForumPagination.vue`

**Putanja:** `src/components/ForumPagination.vue`

Navigacija kroz stranice foruma. Prikazuje „Stranica X od Y” i dugmad „Prethodna” / „Sljedeća”, sa informacijom o ukupnom broju prikazanih tema.

---

#### Props 

| Param              | Tip | Opis                                  |
| ------------------ | -------- | ------------------------------------- |
| `trenutnaStranica` | Number | Indikator trenutne stranice |
| `ukupnoStranica` | Number | Indikator ukupnog broja stranica |
| `prikazanoTema` | Number | Broj prikazanih tema |
| `ukupnoTema` | Number | Ukupan broj tema |

---

#### Emitovani event-i

| Event             | Vrijednost                                  |
| ------------------ | ------------------------------------- |
| `promijeniStranicu`  | stranica (Number)         |


---

### `ForumWidgets.vue`

**Putanja:** `src/components/ForumWidgets.vue`

Bočni widgeti za popularne/slične teme. Kontekst se mijenja: na glavnom forumu prikazuje globalno popularne, unutar kategorije najpopularnije u njoj, unutar teme prikazuje slične teme.

---

#### Props 

| Param              | Tip | Opis                                  |
| ------------------ | -------- | ------------------------------------- |
| `selectedCategoryId` | Number/null | ID kategorije |
| `currentTopicId` | Number/null | ID teme (ako je stranica sa detaljima) |
| `currentTopicTitle` | String | Naslov teme |

---

#### Data

| Polje          | Tip      | Opis                                                                                   |
| -------------- | -------- | -------------------------------------------------------------------------------------- |
| `widgetTopics`| `Array`| Lista tema za prikaz                               |
| `sveKategorije`  | `Array`  | Kategorije (za prikaz naslova)                            |
| `isLoading`  | `Boolean` | Indikator učitavanja                                             |

---

#### API pozivi

| Endpoint             | Servis                                  |
| ------------------ | ------------------------------------- |
| `GET /forum/topics/popular`  | `getPopularTopics`         |
| `GET /forum/topics/category-popular/{categoryId}`  | `getCategoryPopularTopics`         |
| `GET /forum/topics/{topicId}/related`  | `getRelatedTopics`         |
| `GET /forum/categories`  | `getCategories` (za nazive)         |

---

#### Napomene
 - Automatski detektuje kontekst na osnovu prisutnih propova.
 - Widget se ne prikazuje ako nema podataka za dati kontekst.

---

### `ForumGuidelines.vue`

**Putanja:** `src/components/ForumGuidelines.vue`

Prikazuje pravila foruma. Admin može dodavati, uređivati i brisati pravila kroz modal.

---

#### Data

| Polje          | Tip      | Opis                                                                                   |
| -------------- | -------- | -------------------------------------------------------------------------------------- |
| `guidelines`| `Array` | Lista pravila (`id, `title`, `content`, `order`)                   |
| `isAdmin`  | `Boolean`  | Da li je korisnik admin (iz `localStorage`)                         |
| `showModal`  | `Boolean` | Vidljivost modala za dodavanje/izmjenu                              |
| `isEditing`  | `Boolean`  | Da li je modal u režimu izmjene                         |
| `formData`  | `Object` | Trenutni podaci forme                              |

---

#### API pozivi

| Endpoint             | Servis                                  |
| ------------------ | ------------------------------------- |
| `GET /forum/guidelines/`  | `getGuidelines`         |
| `POST /forum/guidelines/`  | `createGuideline`         |
| `PATCH /forum/guidelines/{id}`  | `updateGuideline`         |
| `DELETE /forum/guidelines/{id}`  | `deleteGuideline`         |

---

### `ForumAdminAnnouncementBanner.vue`

**Putanja:** `src/components/ForumAdminAnnouncementBanner.vue`

Banner na vrhu foruma koji prikazuje aktivna globalna obaveštenja. Admin može uređivati i brisati obavještenja direktno sa bannera.

---

#### Props 

| Param              | Tip | Opis                                  |
| ------------------ | -------- | ------------------------------------- |
| `announcements` | Array | Niz aktivnih obavještenja |

---

#### Data

| Polje          | Tip      | Opis                                                                                   |
| -------------- | -------- | -------------------------------------------------------------------------------------- |
| `activeAnnouncements`| `Array` | Lokalna kopija obavještenja                    |
| `isAdmin`  | `Boolean`  | Da li je korisnik admin (iz `localStorage`)                         |
| `showEditModal`  | `Boolean` | Vidljivost modala za dodavanje/izmjenu                              |
| `showDeleteModal`  | `Boolean`  | Modal za potvrdu brisanja                         |

---

#### API pozivi

| Endpoint             | Servis                                  |
| ------------------ | ------------------------------------- |
| `GET /forum/topics/announcements/active`  | `getActiveAnnouncements`         |
| `PATCH /admin/announcements/{id}`  | `updateAnnouncement`         |
| `DELETE /admin/announcements/{id}`  | `deleteAnnouncement`         |

---

### `ForumTopicTagManager.vue`

**Putanja:** `src/components/ForumTopicTagManager.vue`

Input za dodavanje tagova tokom kreiranja teme (max 5). Prikazuje popularne tagove kao sugestije. Koristi `v-model` za dvosmjerno vezivanje niza tagova.

---

#### Props 

| Param              | Tip | Opis                                  |
| ------------------ | -------- | ------------------------------------- |
| `modelValue` | Array | Niz tagova |

---

#### Emitovani event-i

| Event             | Vrijednost                                  |
| ------------------ | ------------------------------------- |
| `update:modelValue`  | Array (novi niz tagova)         |

---

#### Data

| Polje          | Tip      | Opis                                                                                   |
| -------------- | -------- | -------------------------------------------------------------------------------------- |
| `tagInput`| `String` | Tekst unosa za novi tag                    |
| `popularTags`  | `Array`  | Lista popularnih tagova                         |
| `showSuggestions`  | `Boolean` | Vidljivost sugestija                              |

---

#### API pozivi

| Endpoint             | Servis                                  |
| ------------------ | ------------------------------------- |
| `GET /forum/tags`  | `getPopularTags`         |

---

### `ForumView.vue`

**Putanja:** `src/views/ForumView.vue`
**Ruta:** `/forum`
**Meta:** `requiresAuth: true`

Glavna forum stranica. Prikazuje listu tema u gridu (sa sidebar-om i widgetima). Za administratore postoje dodatni tabovi: Aktivne prijave i Riješene prijave, kao i mogućnost kreiranja globalnog obaveštenja. Podržava pretragu, filtere i beskonačno skrolovanje.

---

#### Specifičnosti

  -Korisnik vidi skraćeni prikaz svih tema, sidebar sa kategorijama, admin obavijesti...
  
  -Admin vidi tri taba: Sve teme, Aktivne prijave, Riješene prijave
  
  -Modal za kreiranje globalnog obaveštenja (admin)
  
  -Modal za rešavanje prijave uz objašnjenje (admin)
  
  -Podržava optimističko ažuriranje lajkova/dislajkova kroz composable

---

#### Data / State (ključni)

| Polje          | Tip      | Opis                                                                                   |
| -------------- | -------- | -------------------------------------------------------------------------------------- |
| `teme`| `Array` | Lista tema                    |
| `odabraniKategorijaId`  | `Number/null`  | ID aktivne kategorije                         |
| `currentMode`  | `String` | Trenutni mod prikaza (za admina) - `topics`, `active_reports`, `solved_reports`   |
| `svePrijave` | `Array` | Prijave za admin tabove                    |
| `announcements`| `Array` | Aktivna obavještenja                    |
| `showModalAnnouncement`| `Boolean` | Modal za novo obavještenje                    |
| `showReportModal`| `Boolean` | Modal za rješavanje prijave                    |

---

#### Metode (ključne)

| Metoda                                 | Opis                                                            |
| -------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `ucitajTeme(append)`         | Poziva `getTopics` sa svim filterima i paginacijom. |
| `ucitajPrijave(status)`       | Poziva `getAdminReports`.        |
| `podnesiNovoObavjestenje()`      | Kreira globalno obavještenje i osvježava listu.                      |
| `submitReportAction()`      | Rješava prijavu (prihvatanje ili odbijanje) uz obrazloženje odluke.                                                  |

---

#### API pozivi (ključni)

| Endpoint             | Servis                                  |
| ------------------ | ------------------------------------- |
| `GET /forum/topics`  | `getTopics`         |
| `GET /forum/categories`  | `getCategories`         |
| `GET /forum/topics/announcements/active`  | `getActiveAnnouncements`         |
| `GET /forum/topics/reports/active` (i drugi)  | `getActiveReports`         |
| `POST /admin/announcements`  | `createAnnouncement`         |
| `PATCH /admin/reports/{id}/resolve`  | `resolveReport`         |
| `DELETE /forum/topics/{id}`  | `deleteTopic`         |

---

#### Komponente

| Komponenta             | Uloga                                  |
| ------------------ | ------------------------------------- |
| `ForumSidebar`  | Kategorije i tagovi         |
| `ForumSearchDropdown`  | Pretraga i sugestije         |
| `ForumFilters`  | Sortiranje i filteri         |
| `ForumTopicCard`  | Kartica jedne teme         |
| `ForumWidgets`  | Popularne/slične teme         |
| `AdminAnnouncementBanner`  | Prikaz obavještenja         |

---

#### Napomene
 - Beskonačno skrolovanje se aktivira preko composable `useForumLazyLoading` kada je mod `topics`.
 - Admin tabovi potpuno mijenjaju sadržaj glavnog dijela (umjesto tema prikazuju prijave).


### `CreateTopicView.vue`

**Putanja:** `src/views/CreateTopicView.vue`
**Ruta:** `/forum/nova-tema`
**Meta:** `requiresAuth: true`

Forma za kreiranje nove teme. Validacija: naslov (min 5 karaktera), odabir kategorije, sadržaj (min 10 karaktera), tagovi (max 5), prilozi (max 3, 5MB, dozvoljeni tipovi: JPG, PNG, PDF, DOCX, TXT). Admin ne može kreirati temu – preusmerava se na /forum.

---

#### Data

| Polje          | Tip      | Opis                                                                                   |
| -------------- | -------- | -------------------------------------------------------------------------------------- |
| `title`| `String` | Naslov teme                    |
| `selectedCategory`  | `String`  | ID kategorije                         |
| `tags`  | `Array` | Niz tagova   |
| `content` | `String` | Sadržaj teme                     |
| `selectedFiles`| `Array` | Odabrani file-ovi (max 3)                    |
| `errors`| `Object` | objekat sa greškama po poljima                    |
| `categories`| `Array` | Lista kategorija                    |

---

#### API pozivi

| Endpoint             | Servis                                  |
| ------------------ | ------------------------------------- |
| `GET /forum/categories`  | `getCategories`         |
| `POST /forum/topics`  | `createTopics`         |
| `POST /forum/attachments/topic/{id}`  | `uploadTopicAttachments`         |

---

#### Komponente

| Komponenta             | Uloga                                  |
| ------------------ | ------------------------------------- |
| `ForumTopicTagManager`  | Upravljanje tagovima         |


---

#### Napomene
 - Ako u URL-u postoji query parametar `categoryId`, kategorija se automatski selektuje.
 - Greške sa backenda se parsiraju i prikazuju ispod forme.


### `TopicDetailView.vue`

**Putanja:** `src/views/TopicDetailView.vue`
**Ruta:** `/forum/tema/:id`
**Meta:** `requiresAuth: true`

Stranica detalja teme. Prikazuje glavnu karticu, sortiranje komentara (najbolje ocenjeni, najnoviji, najstariji), listu komentara sa highlight-om iz notifikacija, sidebar sa admin obaveštenjima (unutar teme), pravilima foruma i widgetima za slične teme.

---

#### Specifičnosti

  -Sortiranje komentara: admin notices i najbolji odgovor uvijek na vrhu
  
  -Admin može postaviti službeno obavještenje zakačeno na vrh komentara
  
  -Podržava `highlightedCommentId` iz URL hash-a za scroll i animaciju

---

#### Props

| Param          | Tip      | Opis                                                                                |
| -------------- | -------- | -------------------------------------------------------------------------------------- |
| `id`| `String/Number` | ID teme                    |

---

#### Data 

| Polje          | Tip      | Opis                                                                                   |
| -------------- | -------- | -------------------------------------------------------------------------------------- |
| `fullTopicData`| `Object/Null` | Kompletan objekat teme (sa komentarima)                    |
| `isLoading`  | `Boolean`  | Indikator učitavanja                         |
| `sortCriteria`  | `String` | Kriterij sortiranja   |
| `adminNoticeContent` | `String` | Tekst admin obavještenja unutar teme                    |


---

#### Computed

| Svojstvo                                 | Opis                                                            |
| -------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `highlightedCommentId`         | Izvlači ID komentara iz URL hash-a. |
| `sortedComments`       | Sortirani komentari (admin notice i best answer uvijek na vrhu).        |

---

#### Metode (ključne)

| Metoda                                 | Opis                                                            |
| -------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `loadTopicAndComments(id)`         | Povećava broj pregleda i dohvata temu. |
| `handleNewComment(...)`       | Kreira komentar na nivou teme.        |
| `handleAdminNotice()`       | Postavlja službeno admin obavještenje u temi.        |

---

#### API pozivi 

| Endpoint             | Servis                                  |
| ------------------ | ------------------------------------- |
| `GET /forum/topics/{id}`  | `getTopicsById`         |
| `PATCH /forum/topics/{id}/view`  | `incrementTopicView`         |
| `POST /forum/comments`  | `createComment`         |
| `POST /forum/attachments/comment/{id}`  | `uploadCommentAttachments`         |
| `POST /forum/comments/{topicId}/admin-notice`  | `postAdminNotice`         |

---

#### Komponente

| Komponenta             | Uloga                                  |
| ------------------ | ------------------------------------- |
| `ForumTopicMainCard`  | Glavna kartica teme         |
| `ForumTopicCommentsList`  | Lista komentara sa svim akcijama         |
| `ForumSidebar`  | Kategorije         |
| `ForumWidgets`  | Slične teme         |
| `ForumGuidelines`  | Pravila foruma         |

---

#### Napomene
 - `highlightedCommentId` se prosljeđuje u `ForumTopicCommentsList` radi animacije.
 - Admin sidebar sadrži dodatnu karticu za slanje službenog obavještenja.

---

### `AdminDashboardView.vue`

**Putanja:** `src/views/admin/AdminDashboardView.vue`
**Ruta:** `/forum/admin`
**Meta:** `requiresAuth: true`, `requiresAdmin: true`

Admin panel foruma. Tabovi: Aktivne prijave i Riješene prijave. Pretraga prijava po naslovu teme ili razlogu. Omogućava prihvatanje/odbijanje prijave uz objašnjenje, vraćanje riješenih prijava u aktivne, i kreiranje globalnog obavještenja.


---

#### Data 

| Polje          | Tip      | Opis                                                                                   |
| -------------- | -------- | -------------------------------------------------------------------------------------- |
| `activeTab`| `String` | `reports` ili `handled_reports`                    |
| `reports`  | `Array`  | Aktivne prijave                        |
| `handledReports`  | `Array` | Riješene prijave   |
| `searchQuery` | `String` | Filter za pretragu prijava                    |
| `showAnnouncementModal`  | `Boolean` | Modal za novo globalno obavještenje   |
| `showReportModal` | `Boolean` | Modal za rješavanje prijave                    |


---

#### Computed

| Svojstvo                                 | Opis                                                            |
| -------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `filteredReports`         | Prijave filtrirane po `searchQuery` |
| `filteredHandledReports`       | Isto za riješene prijave        |

---

#### Metode (ključne)

| Metoda                                 | Opis                                                            |
| -------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `loadData()`         | Učitava podatke za aktivni tab. |
| `submitReportAction()`       | Rješava prijavu (prihvati/odbij) uz objašnjenje i osvježavanje liste.        |
| `handleReopenReport(id)`       | Vraća riješenu prijavu u aktivne.        |
| `postAnnouncement()`       | Kreira globalno obavještenje.        |
| `goToTopic(topicId)`       | Navigira do teme unutar foruma.        |

---

#### API pozivi 

| Endpoint             | Servis                                  |
| ------------------ | ------------------------------------- |
| `GET /admin/reports?status=pending`  | `getReports`         |
| `GET /admin/reports?status=resolved`  | `getHandledReports`         |
| `PATCH /admin/reports/{id}/resolve`  | `resolveReport`         |
| `PATCH`/admin/reports/{id}/reopen  | `reopenReport`         |
| `POST /admin/announcements`  | `createAnnouncement`         |
| `GET /admin/announcements/all`  | `getAllAnnouncements`         |

---

#### Napomene
 - Dvostruka provjera admin prava: guard rute i ručna provjera u `mounted`.
 - Dugme za vraćanje prijave u aktivne pojavljuje se samo kod riješenih prijava.


---


























