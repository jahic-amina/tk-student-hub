# TK Student Hub — Frontend

Izgrađeno sa Vue 3, Vite i Tailwind CSS. Frontend je lokalizovan na bosanski jezik i rebrendiran za TK Student Hub.

## Postavljanje projekta

1. Instaliraj zavisnosti:
```bash
cd frontend
npm install
```

2. Pokreni dev server:
```bash
npm run dev
```

3. Otvori u browseru:
```
http://localhost:5173
```

## Struktura projekta

```
src/
  components/
    NavBar.vue          — navigacija (ne mijenjati)
    FooterBar.vue       — footer (ne mijenjati)
  views/
    HomeView.vue        — početna stranica
    LoginView.vue       — forma za prijavu
    RegisterView.vue    — forma za registraciju
  workshops/          — Ekipa 1
  mentoring/          — Ekipa 2
  forum/              — Ekipa 3
  profiles/           — Ekipa 4
  router/
    index.js            — rute aplikacije
  services/
    api.js              — komunikacija sa backendom
```

## Autentifikacija

Token se čuva u `localStorage` nakon prijave.
Svaki API poziv koji zahtijeva auth šalje token u headeru:
```
Authorization: Bearer YOUR_TOKEN_HERE
```

## Za projektne timove

1. Vaš folder je već kreiran u `src/views/`
2. Kreirajte svoje komponente u `src/components/`
3. Dodajte svoje rute u `src/router/index.js`
4. Za API pozive koristite `src/services/api.js` kao primjer
5. Sve stranice vaše funkcionalnosti trebaju `meta: { requiresAuth: true }`

## Boje

```
Primary:   #ff7a00  (narandžasta)
Secondary: #ffb380  (svjetlija narandžasta)
```

Koristite Tailwind klase `text-primary`, `bg-primary` za konzistentan dizajn.