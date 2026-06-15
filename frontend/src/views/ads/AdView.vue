<template>
  <div class="min-h-screen bg-gradient-to-b from-orange-50 via-white to-white">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-8 md:py-12">
      <div class="mb-6">
        <router-link to="/ads" class="text-sm font-semibold text-orange-600 hover:text-orange-700 transition">
          ← Nazad na listu oglasa
        </router-link>
      </div>

      <div v-if="loading" class="rounded-3xl border border-gray-100 bg-white shadow-sm p-8 text-center text-gray-500">
        Učitavanje detalja oglasa...
      </div>

      <div v-else-if="errorMessage" class="rounded-3xl border border-red-100 bg-red-50 p-8 text-red-700">
        {{ errorMessage }}
      </div>

      <div v-else-if="ad" class="flex flex-col gap-6">
        
        <div class="grid gap-6 lg:grid-cols-[1.6fr_0.9fr] items-start">
          
          <section class="rounded-3xl border border-gray-100 bg-white shadow-sm p-6 sm:p-8 relative">
            
            <button 
              v-if="isUserLoggedIn && !isCompanyLoggedIn && !isAdmin"
              @click.prevent="toggleBookmark" 
              class="absolute top-6 right-6 focus:outline-none transition-transform hover:scale-110 active:scale-95 z-10"
              title="Sačuvaj oglas"
            >
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                :fill="bookmarkId ? 'currentColor' : 'none'" 
                viewBox="0 0 24 24" 
                stroke-width="1.5" 
                stroke="currentColor" 
                :class="[
                  'w-8 h-8 transition-colors duration-300', 
                  bookmarkId ? 'text-orange-500' : 'text-gray-300 hover:text-orange-400'
                ]"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M17.593 3.322c1.1.128 1.907 1.077 1.907 2.185V21L12 17.25 4.5 21V5.507c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0111.186 0z" />
              </svg>
            </button>

            <div class="flex flex-wrap gap-2 mb-4 text-xs font-semibold pr-12">
              <span :class="getTypeClass(ad.typeLabel)">{{ ad.typeLabel }}</span>
              <span :class="getStatusClass(ad.statusLabel)">{{ ad.statusLabel }}</span>
            </div>

            <h1 class="text-2xl sm:text-4xl font-black text-gray-900 leading-tight mb-3 pr-12">
              {{ ad.title }}
            </h1>

            <p class="text-base sm:text-lg text-gray-600 font-medium mb-6">
              <router-link :to="`/companies/${ad.company_id}`" class="hover:text-orange-500 transition-colors">
                {{ ad.company }}
              </router-link>
            </p>

            <div class="grid sm:grid-cols-3 gap-3 mb-8">
              <div class="rounded-2xl bg-gray-50 border border-gray-100 p-4">
                <p class="text-xs uppercase tracking-wide text-gray-400 font-semibold mb-1">Lokacija</p>
                <p class="text-sm font-bold text-gray-900">{{ ad.location || 'Nije navedeno' }}</p>
              </div>
              <div class="rounded-2xl bg-gray-50 border border-gray-100 p-4">
                <p class="text-xs uppercase tracking-wide text-gray-400 font-semibold mb-1">Trajanje</p>
                <p class="text-sm font-bold text-gray-900">{{ ad.duration || 'Nije navedeno' }}</p>
              </div>
              <div class="rounded-2xl bg-gray-50 border border-gray-100 p-4">
                <p class="text-xs uppercase tracking-wide text-gray-400 font-semibold mb-1">Naknada</p>
                <p class="text-sm font-bold text-gray-900">{{ ad.compensation || 'Nije navedeno' }}</p>
              </div>
            </div>

            <div class="space-y-6 text-gray-700">
              <div>
                <h2 class="text-lg font-bold text-gray-900 mb-2">Opis oglasa</h2>
                <p class="leading-7 whitespace-pre-line">{{ ad.description }}</p>
              </div>

              <div v-if="ad.requirements">
                <h2 class="text-lg font-bold text-gray-900 mb-2">Uslovi</h2>
                <p class="leading-7 whitespace-pre-line">{{ ad.requirements }}</p>
              </div>

              <div v-if="ad.benefits">
                <h2 class="text-lg font-bold text-gray-900 mb-2">Benefiti</h2>
                <p class="leading-7 whitespace-pre-line">{{ ad.benefits }}</p>
              </div>
            </div>
          </section>

          <aside v-if="!isCompanyLoggedIn" class="rounded-3xl border border-gray-100 bg-white shadow-sm p-6 sm:p-8">
            <template v-if="isUserLoggedIn && !isCompanyLoggedIn">
              <h2 class="text-lg font-bold text-gray-900 mb-4">Brzi pregled</h2>

              <div class="space-y-4 text-sm">
                <div>
                  <p class="text-gray-400 font-semibold mb-1">Oblast</p>
                  <p class="text-gray-900 font-medium">{{ ad.field || 'Nije navedeno' }}</p>
                </div>
                <div>
                  <p class="text-gray-400 font-semibold mb-1">Tagovi</p>
                  <div class="flex flex-wrap gap-2">
                    <span
                      v-for="tag in ad.tags"
                      :key="tag"
                      class="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-xs font-semibold"
                    >
                      {{ tag }}
                    </span>
                  </div>
                </div>
                <div>
                  <p class="text-gray-400 font-semibold mb-1">Broj mjesta</p>
                  <p class="text-gray-900 font-medium">{{ ad.spots || 'Nije navedeno' }}</p>
                </div>
                <div>
                  <p class="text-gray-400 font-semibold mb-1">Rok prijave</p>
                  <p class="text-gray-900 font-medium">{{ ad.deadline || 'Nije navedeno' }}</p>
                </div>
              </div>

              <router-link
                :to="`/ads/${ad.id}/apply`"
                class="block mt-6 bg-orange-600 text-white py-3 rounded-lg hover:bg-orange-700 transition font-semibold text-center"
              >
                Pošalji prijavu
              </router-link>
            </template>

            <template v-else-if="!isUserLoggedIn && !isCompanyLoggedIn">
              <h2 class="text-lg font-bold text-gray-900 mb-4">Zainteresovan?</h2>
              <div class="rounded-2xl bg-orange-50 border border-orange-100 p-4 mb-4">
                <p class="text-sm font-semibold text-orange-900 mb-2">Prijavite se za ovu poziciju</p>
                <p class="text-sm text-orange-800 leading-6 mb-4">
                  Trebate biti prijavljeni da biste poslali prijavu za ovu poziciju.
                </p>
                <router-link
                  to="/login"
                  class="block bg-orange-600 text-white py-2 rounded-lg hover:bg-orange-700 transition font-semibold text-center"
                >
                  Prijavi se
                </router-link>
              </div>

              <h2 class="text-lg font-bold text-gray-900 mb-4 mt-6">Brzi pregled</h2>
              <div class="space-y-4 text-sm">
                <div>
                  <p class="text-gray-400 font-semibold mb-1">Oblast</p>
                  <p class="text-gray-900 font-medium">{{ ad.field || 'Nije navedeno' }}</p>
                </div>
                <div>
                  <p class="text-gray-400 font-semibold mb-1">Tagovi</p>
                  <div class="flex flex-wrap gap-2">
                    <span
                      v-for="tag in ad.tags"
                      :key="tag"
                      class="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-xs font-semibold"
                    >
                      {{ tag }}
                    </span>
                  </div>
                </div>
                <div>
                  <p class="text-gray-400 font-semibold mb-1">Broj mjesta</p>
                  <p class="text-gray-900 font-medium">{{ ad.spots || 'Nije navedeno' }}</p>
                </div>
                <div>
                  <p class="text-gray-400 font-semibold mb-1">Rok prijave</p>
                  <p class="text-gray-900 font-medium">{{ ad.deadline || 'Nije navedeno' }}</p>
                </div>
              </div>
            </template>
          </aside>
        </div>

        <section v-if="isAdmin || isCompanyLoggedIn" class="rounded-3xl border border-gray-100 bg-white shadow-sm p-6 sm:p-8 w-full">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">Prijave ({{ applications.length }}) · Broj mjesta: {{ ad.spots }}</h2>
          <div v-if="loadingApplications" class="text-center text-gray-500 py-8">
            Učitavanje prijava...
          </div>

          <div v-else-if="applicationsError" class="rounded-2xl border border-red-200 bg-red-50 p-4 text-red-700">
            {{ applicationsError }}
          </div>

          <div v-else-if="applications.length === 0" class="rounded-2xl border border-yellow-200 bg-yellow-50 p-4 text-yellow-700">
            <p class="text-sm font-medium">Nema prijava za ovaj oglas.</p>
          </div>

          <div v-else class="space-y-4">
            <ApplicationCard 
              v-for="app in applications" 
              :key="app.id" 
              :application="app" 
              :token="userToken"
              :is-company="isCompanyLoggedIn" 
              @updated="fetchApplications" 
            />
          </div>
        </section>

      </div>
    </div>
  </div>
</template>

<script>
// Dodane funkcije za bookmarke iz api.js
import { getAdById, getApprovedCompanies, getApplicationsByAd, getBookmarks, addBookmark, removeBookmark } from '../../services/api.js'
import ApplicationCard from '../../components/application/ApplicationCard.vue'

const BASE_BADGE = 'px-3 py-1.5 rounded-full'

function formatType(type) {
  const map = {
    internship: 'Praksa',
    education: 'Edukacija',
    scholarship: 'Stipendija'
  }
  return map[type] || 'Prilika'
}

function formatStatus(status) {
  const map = {
    active: 'Aktivan',
    pending: 'Na čekanju',
    expired: 'Istekao',
    rejected: 'Odbijen',
    changes_requested: 'Potrebne izmjene'
  }
  return map[status] || 'Aktivan'
}

function formatCompensation(value, currency) {
  if (value === null || value === undefined) return ''
  return `${value} ${currency || 'BAM'}`
}

export default {
  name: 'AdDetailView',
  components: {
    ApplicationCard
  },
  data() {
    return {
      loading: false,
      errorMessage: '',
      ad: null,
      isUserLoggedIn: false,
      isCompanyLoggedIn: false,
      userRole: null,
      applications: [],
      loadingApplications: false,
      applicationsError: '',
      companyToken: localStorage.getItem('company_token'),
      bookmarkId: null 
    }
  },
  computed: {
    isAdmin() {
      return this.isUserLoggedIn && this.userRole === 'admin'
    },
    userToken() {
    return this.isCompanyLoggedIn ? this.companyToken : localStorage.getItem('token')
  }
  },
  methods: {
    getTypeClass(typeLabel) {
      if (typeLabel === 'Praksa') return `bg-blue-50 text-blue-600 ${BASE_BADGE}`
      if (typeLabel === 'Edukacija') return `bg-indigo-50 text-indigo-600 ${BASE_BADGE}`
      return `bg-amber-50 text-amber-600 ${BASE_BADGE}`
    },
    getStatusClass(statusLabel) {
      if (statusLabel === 'Aktivan') return `bg-green-50 text-green-600 ${BASE_BADGE}`
      if (statusLabel === 'Istekao') return `bg-orange-50 text-orange-600 ${BASE_BADGE}`
      return `bg-red-50 text-red-600 ${BASE_BADGE}`
    },
    async fetchAd() {
      this.loading = true
      this.errorMessage = ''

      const adId = Number(this.$route.params.id)
      let found, companies

      try {
        [found, companies] = await Promise.all([
          getAdById(adId),
          getApprovedCompanies()
        ])
      } catch (err) {
        console.error('Failed to fetch ad details:', err)
        this.errorMessage = 'Ne mogu učitati detalje oglasa. Provjeri da li je API pokrenut.'
        this.loading = false
        return
      }

      if (!found) {
        this.errorMessage = 'Oglas nije pronađen.'
        this.loading = false
        return
      }

      const companiesById = new Map(
        (companies || []).map(company => [company.id, company.company_name])
      )

      this.ad = {
        id: found.id,
        title: found.title,
        company: companiesById.get(found.company_id) || `Kompanija #${found.company_id}`,
        company_id: found.company_id,
        description: found.description,
        tags: [found.field, found.location].filter(Boolean),
        typeLabel: formatType(found.type),
        compensation: formatCompensation(found.compensation, found.currency),
        statusLabel: formatStatus(found.status),
        location: found.location,
        duration: found.duration_months ? `${found.duration_months} mjeseci` : null,
        field: found.field,
        requirements: found.requirements,
        benefits: found.benefits,
        spots: found.spots,
        deadline: found.deadline
      }

      this.loading = false
    },
    async fetchApplications() {
      const adId = Number(this.$route.params.id)
      const isAdmin = this.isAdmin
      const isCompany = this.isCompanyLoggedIn
      
      if (!isAdmin && !isCompany) return

      const token = isCompany
        ? localStorage.getItem('company_token')
        : localStorage.getItem('token')

      if (!token || token === 'null' || token === 'undefined') return
      
      this.loadingApplications = true
      this.applicationsError = ''
      
      try {
        const apps = await getApplicationsByAd(adId, token, isCompany)
        this.applications = apps || []
      } catch (err) {
        console.error('Failed to fetch applications:', err)
        this.applicationsError = 'Ne mogu učitati prijave.'
      } finally {
        this.loadingApplications = false
      }
    },

    // --- PRAVA LOGIKA ZA SAČUVANE OGLASE SA API-JEM ---
    async checkBookmarkStatus() {
      if (!this.isUserLoggedIn || this.isCompanyLoggedIn || this.isAdmin) return;
      
      const token = localStorage.getItem('token')
      if (!token || token === 'null' || token === 'undefined') return;

      const adId = Number(this.$route.params.id)

      try {
        const bookmarks = await getBookmarks(token)
        // Tražimo da li postoji bookmark sa istim ad_id
        const foundBookmark = bookmarks.find(bm => bm.ad_id === adId)
        
        if (foundBookmark) {
          // Ako je nađen, čuvamo ID iz baze kako bismo ga mogli obrisati
          this.bookmarkId = foundBookmark.id;
        } else {
          this.bookmarkId = null;
        }
      } catch (err) {
        console.error('Nisam uspio provjeriti status bookmarka:', err)
      }
    },
    
    async toggleBookmark() {
      const token = localStorage.getItem('token')
      
      if (!token || token === 'null' || token === 'undefined') {
        alert('Morate biti prijavljeni da biste sačuvali oglas.')
        return
      }

      const adId = Number(this.$route.params.id)

      try {
        if (this.bookmarkId) {
          // Ako već postoji bookmarkId, brišemo ga iz baze
          await removeBookmark(this.bookmarkId, token)
          this.bookmarkId = null;
        } else {
          // Ako ne postoji, dodajemo u bazu i uzimamo generisani ID
          const newBookmark = await addBookmark(adId, token)
          this.bookmarkId = newBookmark.id;
        }
      } catch (err) {
        console.error('Greška prilikom promjene statusa bookmarka:', err)
        alert('Došlo je do greške pri čuvanju oglasa. Molimo pokušajte ponovo.')
      }
    }
  },
  async mounted() {
    this.isUserLoggedIn = !!localStorage.getItem('token')
    this.isCompanyLoggedIn = !!localStorage.getItem('company_token')
    this.userRole = localStorage.getItem('role')
    
    await this.fetchAd()
    await this.fetchApplications()
    // Pokrećemo provjeru nakon što se komponenta učita
    await this.checkBookmarkStatus()
  }
}
</script>