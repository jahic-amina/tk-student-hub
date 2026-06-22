# TK Student Hub — Platforma

**TK Student Hub** — platforma za studente telekomunikacija koja omogućava dijeljenje materijala, korisnih linkova, učestvovanje u forumu i upravljaju svojim profilom.

## O projektu

TK Student Hub povezuje studente, kompanije i administratore platforme. Studenti mogu pratiti i dijeliti studijske materijale, prijavljivati se na prakse i oglase, učestvovati u diskusijama na forumu i pratiti vlastitu aktivnost na platformi. Kompanije mogu objavljivati oglase za prakse i upravljati prijavama. Administratori upravljaju korisnicima i kompanijama i odobravaju sadržaj.

## Korisničke uloge

| Uloga         | Opis                                                                           |
| ------------- | ------------------------------------------------------------------------------ |
| Posjetilac    | Neregistrovani korisnik koji pregledava javni sadržaj                          |
| Student       | Registrovani korisnik s punim pristupom funkcionalnostima platforme            |
| Kompanija     | Registrovana kompanija koja postavlja u pravlja oglasima za prakse i edukacije |
| Administrator | Upravlja korisnicima i sadržajem platforme                                     |

Pored toga, kompanije imaju zaseban tip naloga za objavu oglasa i upravljanje prijavama.

## Tehnologije

**Backend:** FastAPI, SQLModel, SQLAlchemy, Alembic, SQLite, JWT autentifikacija

**Frontend:** Vue 3, Vite, Tailwind CSS, Vue Router

## Struktura projekta

```
tk-student-hub/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── services/
|   |   └── tests/
│   └── tests/
└── frontend/
    ├── public/
    └── src/
        ├── assets/
        ├── components/
        │   ├── ads/
        |   ├── application/
        │   └── company/
        ├── composables/
        ├── router/
        └── views/
```

### Koraci za pokretanje projekta

#### Backend:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### Frontend:

```bash
cd frontend
npm install
npm run dev
```

#### Dodatna dokumentacija:

API dokumentacija (kad backend radi): `http://127.0.0.1:8000/docs`

Za detalje o frontend i backend specifičnim uputama pogledajte:

- `frontend/README.md` - instalacija, struktura, povezivanje s backendom,
- `backend/README.md` - instalacija, konfiguracija, migracije, API.

## Autentifikacija

Platforma koristi JWT tokene. Nakon prijave token se čuva u `localStorage` i šalje sa svakim API pozivom u headeru:

```
Authorization: Bearer YOUR_TOKEN_HERE
```

## Timovi i funkcionalnosti
                                                                                                                                                                                                            
| PRojektni tim | Funkcionalnost | Folder | Članova tima |
|-----|---------------|--------|---|
| Tim 1 | Prakse i edukacije | `backend/app/routers/ad.py`, `backend/app/routers/company.py`, `backend/app/routers/ad_bookmark.py`, `backend/app/routers/applications.py`, `backend/app/routers/notification.py`, `frontend/src/views/ads/`, `frontend/src/views/application/`, `frontend/src/views/company/` | Elnur Bjelic, Arslan Telarevic, Tahira Zukic, Nejla Kavazovic |
| Tim 2 | Materijali | `backend/app/routers/materials.py`, `frontend/src/views/materials/` | Lejla Kadušić, Amer Imamović, Marinela Mitić, Faris Ćosić  |
| Tim 3 | Forum | `backend/app/models/forum.py`,`backend/app/models/forum_notification.py`,`backend/app/models/forum_reputation.py` ,`backend/app/routers/forum_admin.py`,`backend/app/routers/forum_attachments.py`,`backend/app/routers/forum_categories.py`,`backend/app/routers/forum_comments.py`,`backend/app/routers/forum_guidelines.py`,`backend/app/routers/forum_helpers.py`,`backend/app/routers/forum_likes.py`,`backend/app/routers/forum_notifications.py`,`backend/app/routers/forum_tags.py`,`backend/app/routers/forum_topics.py`,`backend/app/services/forum_notification_service.py`,`backend/app/services/forum_reputation.py`,`frontend/src/components/ForumAdminAnnouncementBanner.vue`,`frontend/src/components/ForumAttachmentPreview.vue`,`frontend/src/components/ForumAvatar.vue`,`frontend/src/components/ForumCommentNode.vue`,`frontend/src/components/ForumFilters.vue`,`frontend/src/components/ForumGuidelines.vue`,`frontend/src/components/ForumPagination.vue`,`frontend/src/components/ForumSearchDropdown.vue`,`frontend/src/components/ForumSidebar.vue`,`frontend/src/components/ForumTopicCard.vue`,`frontend/src/components/ForumTopicCommentForm.vue`,`frontend/src/components/ForumTopicCommentsList.vue`,`frontend/src/components/ForumTopicMainCard.vue`,`frontend/src/components/ForumTopicTagManager.vue`,`frontend/src/components/ForumWidgets.vue`,`frontend/src/composables/useForumExtras.js`,`frontend/src/services/forum_admin.js`,`frontend/src/services/forum.js`,`frontend/src/services/forumNotifications.js`,`frontend/src/views/forum/` | Amar Ascic, Ehlimana Beganovic, Iman Osmic, Edin Hodzic |
| Tim 4 | Profili & Dashboard | `backend/app/routers/profiles.py`, `frontend/src/views/profiles/` | - |

**Tim 2 Opis:**
- **Lejla Kadušić** — Upload materijala, komentari (CRUD), paginacija
- **Amer Imamović** — Brisanje materijala, bookmark (omiljeni), filteri (godina, tip, predmet)
- **Marinela Mitić** — Forma za dodavanje materijala s validacijom, preuzimanje materijala, ocjenjivanje (zvjezdice), thumbnail sličice, dark mode
- **Faris Ćosić** - Pregled materijala, detaljan pregled materijala, odobravanje/odbijanje , preview, ažuriranje


