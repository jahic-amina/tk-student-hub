<template>
  <div class="bg-gray-50 min-h-screen font-sans">

    <HeroBanner />

    <div class="max-w-6xl mx-auto px-4 sm:px-6 py-6 md:py-8">

      <div class="flex gap-4 md:gap-6 border-b border-gray-200 pb-0 mb-6 overflow-x-auto no-scrollbar text-sm font-medium whitespace-nowrap">
        <button
          v-for="tab in ['Sve', 'Prakse', 'Edukacije', 'Stipendije', 'Aktuelno']"
          :key="tab"
          :class="['pb-3 px-1 transition-all border-b-2 text-xs sm:text-sm', currentTab === tab ? 'border-orange-500 text-orange-600 font-bold' : 'border-transparent text-gray-500 hover:text-gray-700']"
          @click="currentTab = tab">
          {{ tab }}
        </button>
      </div>

      <AdFilter
        v-model:searchQuery="searchQuery"
        v-model:isPaid="isPaid"
        v-model:selectedField="selectedField"
        :fields="fields"
      />

      <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3 mb-6">
        <h2 class="text-base sm:text-lg font-bold text-gray-800 text-center sm:text-left">
          {{ filteredAds.length }} aktivnih oglasa
        </h2>
        
        <button 
          v-if="isStudent"
          @click="showOnlySaved = !showOnlySaved"
          :class="[
            'w-full sm:w-auto text-xs sm:text-sm font-semibold px-4 py-2.5 rounded-lg transition shadow-sm text-center',
            showOnlySaved ? 'bg-gray-800 hover:bg-gray-900 text-white' : 'bg-orange-500 hover:bg-orange-600 text-white'
          ]"
        >
          {{ showOnlySaved ? 'Prikaži sve oglase' : 'Sačuvane prilike' }}
        </button>
      </div>

      <div v-if="loading" class="text-center py-12 text-gray-500 font-medium text-sm">
        Učitavanje oglasa...
      </div>

      <div v-else-if="errorMessage" class="text-center py-10 px-4 bg-white rounded-xl border border-dashed border-red-300">
        <p class="text-red-500 font-medium text-base sm:text-lg">{{ errorMessage }}</p>
      </div>

      <div v-else-if="filteredAds.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        <AdCard
          v-for="ad in filteredAds"
          :key="ad.id"
          :ad="ad"
          :bookmarkId="savedAds[ad.id] || null"
          :canBookmark="isStudent"
          @toggle-bookmark="handleToggleBookmark"
        />
      </div>

      <div v-else class="text-center py-10 px-4 bg-white rounded-xl border border-dashed border-gray-300">
        <p class="text-gray-500 font-medium text-base sm:text-lg">
          {{ showOnlySaved ? 'Nemate nijednu sačuvanu priliku za odabrane filtere.' : 'Nema pronađenih oglasa za traženi pojam.' }}
        </p>
        <p class="text-gray-400 text-xs sm:text-sm mt-1">Pokušajte sa nekom drugom ključnom riječi ili filterom.</p>
      </div>

    </div>
  </div>
</template>

<script>
import HeroBanner from '../../components/HeroBanner.vue'
import AdFilter from '../../components/ads/AdFilter.vue'
import AdCard from '../../components/ads/AdCard.vue'
import { getAds, getBookmarks, addBookmark, removeBookmark } from '../../services/api.js'

const TAB_TO_TYPE = {
  Prakse: 'internship',
  Edukacije: 'education',
  Stipendije: 'scholarship'
}

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
  name: 'AdsView',
  components: {
    HeroBanner,
    AdFilter,
    AdCard
  },
  data() {
    return {
      loading: false,
      currentTab: 'Sve',
      searchQuery: '',
      isPaid: false,
      selectedField: '',
      ads: [],
      errorMessage: '',
      savedAds: {}, 
      showOnlySaved: false,
      userRole: localStorage.getItem('role') || 'guest' // Čitamo 'member', 'company', 'admin' ili 'guest'
    }
  },
  computed: {
    // Vraća true samo ako je ulogovani korisnik obični član / student
    isStudent() {
      return this.userRole === 'member'
    },
    fields() {
      const all = this.ads.map(ad => ad.field).filter(Boolean)
      return [...new Set(all)]
    },
    filteredAds() {
      return this.ads.filter(ad => {
        const tabMap = {
          'Sve': true,
          'Prakse': ad.typeKey === 'internship',
          'Edukacije': ad.typeKey === 'education',
          'Stipendije': ad.typeKey === 'scholarship',
          'Aktuelno': ad.statusKey === 'active'
        }
        const matchesTab = tabMap[this.currentTab] ?? true
        const q = this.searchQuery.toLowerCase()
        const matchesSearch = !q ||
          (ad.title && ad.title.toLowerCase().includes(q)) ||
          (ad.company && ad.company.toLowerCase().includes(q)) ||
          (ad.description && ad.description.toLowerCase().includes(q)) ||
          (Array.isArray(ad.tags) && ad.tags.some(t => t.toLowerCase().includes(q)))
        const matchesPaid = !this.isPaid || Boolean(ad.compensation)
        const matchesField = !this.selectedField || ad.field === this.selectedField

        // Filtriranje sačuvanih oglasa ukoliko je aktiviran filter
        const matchesSaved = this.showOnlySaved ? (this.savedAds[ad.id] !== undefined) : true;

        return matchesTab && matchesSearch && matchesPaid && matchesField && matchesSaved
      })
    }
  },
  methods: {
    async fetchAdsAndBookmarks() {
      this.loading = true
      this.errorMessage = ''
      
      const token = localStorage.getItem('token')

      try {
        const adsData = await getAds()
        this.ads = (adsData || []).map(ad => {
          return {
            id: ad.id,
            title: ad.title,
            company: ad.company_name || `Kompanija #${ad.company_id}`,
            company_id: ad.company_id,
            description: ad.description,
            tags: [ad.field, ad.location].filter(Boolean),
            typeLabel: formatType(ad.type),
            compensation: formatCompensation(ad.compensation, ad.currency),
            statusLabel: formatStatus(ad.status),
            statusKey: ad.status,
            typeKey: ad.type,
            location: ad.location,
            duration: ad.duration_months,
            field: ad.field,
            spots: ad.spots ?? null,
            applicants_count: ad.applicants_count ?? 0
          }
        })

        // Povuci bookmarke samo ako korisnik ima token i uloga mu je 'member'
        if (token && token !== 'null' && token !== 'undefined' && this.isStudent) {
          try {
            const bookmarks = await getBookmarks(token)
            const newSavedAds = {}
            bookmarks.forEach(bm => {
              newSavedAds[bm.ad_id] = bm.id 
            })
            this.savedAds = newSavedAds
          } catch (bmErr) {
            console.error('Nisam uspio učitati sačuvane oglase:', bmErr)
          }
        }
      } catch (err) {
        console.error('Failed to fetch ads:', err)
        this.errorMessage = 'Ne mogu učitati oglase sa backend-a. Provjeri da li je API pokrenut na 127.0.0.1:8000.'
      } finally {
        this.loading = false
      }
    },
    
    async handleToggleBookmark(payload) {
      const { adId, bookmarkId } = payload;
      const token = localStorage.getItem('token')

      if (!token || token === 'null' || token === 'undefined') {
        alert('Morate biti prijavljeni da biste sačuvali oglas.')
        return
      }

      try {
        if (bookmarkId) {
          await removeBookmark(bookmarkId, token)
          delete this.savedAds[adId];
        } else {
          const newBookmark = await addBookmark(adId, token)
          this.savedAds[adId] = newBookmark.id;
        }
      } catch (error) {
        console.error("Greška pri ažuriranju bookmarka:", error)
        alert("Došlo je do greške pri čuvanju oglasa. Pokušajte ponovo.")
      }
    }
  },
  mounted() {
    this.fetchAdsAndBookmarks()
  }
}
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>