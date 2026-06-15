<template>
  <div class="min-h-screen bg-gray-50 py-10 px-4 font-sans text-gray-800">
    <div class="max-w-6xl mx-auto">
      
      <!-- Zaglavlje usklađeno sa stilom kompanija -->
      <div class="mb-8">
        <h1 class="text-2xl sm:text-3xl font-black text-gray-900">Upravljanje oglasima</h1>
        <p class="text-gray-500 mt-1 text-sm">Pregled, odobravanje i odbijanje oglasa za praksu.</p>
      </div>

      <div v-if="loading" class="text-center py-12 text-gray-500 text-sm font-medium">
        Učitavanje oglasa...
      </div>

      <div v-else-if="errorMessage" class="p-6 bg-red-50 border border-red-200 rounded-2xl text-red-700 text-sm">
        {{ errorMessage }}
      </div>

      <template v-else>
        <!-- Tabovi / Filteri posloženi identično kao kod kompanija -->
        <div class="flex gap-3 mb-6 flex-wrap">
          <button
            v-for="filter in ['Sve', 'Na čekanju', 'Odobreni', 'Odbijeni', 'Obrisani']"
            :key="filter"
            @click="activeFilter = filter"
            :class="['px-4 py-2 rounded-lg text-xs sm:text-sm font-semibold transition', activeFilter === filter ? 'bg-orange-500 text-white shadow-sm' : 'bg-white border border-gray-200 text-gray-600 hover:bg-gray-50']"
          >
            {{ filter }}
            <span class="ml-1 opacity-70">({{ filterCount(filter) }})</span>
          </button>
        </div>

        <!-- Poruka ako je kategorija prazna -->
        <div v-if="filteredAds.length === 0" class="text-center py-10 text-gray-400 text-sm">
          Nema oglasa u ovoj kategoriji.
        </div>

        <!-- Grid sa karticama (Usklađeno na 3 kolone za velike ekrane) -->
        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          <div 
            v-for="ad in filteredAds" 
            :key="ad.id" 
            class="relative bg-white rounded-2xl border border-gray-100 shadow-sm p-6 flex flex-col gap-4 justify-between"
          >
            <!-- Gornji dio kartice: Naslov i Status -->
            <div class="flex items-start justify-between gap-2">
              <div>
                <h2 class="text-base font-bold text-gray-900 leading-tight line-clamp-2">{{ ad.title }}</h2>
                <p class="text-xs font-bold text-orange-500 mt-0.5">
                  {{ ad.company_name || `Kompanija ID: ${ad.company_id}` }}
                </p>
              </div>
              
              <span v-if="ad.is_deleted" class="text-xs font-semibold px-2.5 py-1 rounded-full whitespace-nowrap bg-gray-100 text-gray-700">
                Obrisano
              </span>
              <span v-else :class="statusBadgeClass(ad.status)">
                {{ statusLabel(ad.status) }}
              </span>
            </div>

            <!-- Srednji dio kartice: Detalji oglasa -->
            <div class="text-xs text-gray-500 space-y-1">
              <p><span class="font-semibold text-gray-700">📍 Lokacija:</span> {{ ad.location }}</p>
              <p><span class="font-semibold text-gray-700">💼 Oblast:</span> {{ ad.field }}</p>
              <p><span class="font-semibold text-gray-700">⏳ Rok prijave:</span> <span class="text-gray-700 font-medium">{{ ad.deadline }}</span></p>
              <p v-if="ad.duration_months"><span class="font-semibold text-gray-700">📅 Trajanje:</span> {{ ad.duration_months }} mj.</p>
            </div>

            <!-- Akcije za odobravanje/odbijanje (Prikazuju se samo ako oglas čeka i nije obrisan) -->
            <div v-if="!ad.is_deleted && ad.status === 'pending'" class="flex gap-2 mt-auto pr-10">
              <button
                @click="updateAdStatusHandler(ad, 'active')"
                :disabled="ad.updating"
                class="flex-1 py-2 rounded-lg bg-green-50 text-green-700 text-xs font-semibold hover:bg-green-100 transition disabled:opacity-50"
              >
                {{ ad.updating === 'active' ? 'Slanje...' : 'Odobri' }}
              </button>
              <button
                @click="updateAdStatusHandler(ad, 'rejected')"
                :disabled="ad.updating"
                class="flex-1 py-2 rounded-lg bg-red-50 text-red-700 text-xs font-semibold hover:bg-red-100 transition disabled:opacity-50"
              >
                {{ ad.updating === 'rejected' ? 'Slanje...' : 'Odbij' }}
              </button>
            </div>

            <!-- Dugmad za brisanje i vraćanje (Apsolutno pozicionirana u donjem desnom uglu kao kod kompanija) -->
            <div class="absolute bottom-4 right-4 flex gap-2">
              <button
                v-if="!ad.is_deleted"
                @click="deleteAdHandler(ad)"
                :disabled="ad.updating"
                class="p-2 rounded-full bg-red-50 text-red-600 hover:bg-red-100 transition disabled:opacity-50"
                :title="ad.updating === 'deleting' ? 'Brisanje...' : 'Obriši'"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
              <button
                v-else
                @click="restoreAdHandler(ad)"
                :disabled="ad.updating"
                class="p-2 rounded-full bg-green-50 text-green-600 hover:bg-green-100 transition disabled:opacity-50"
                :title="ad.updating === 'restoring' ? 'Vraćanje...' : 'Vrati'"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </button>
            </div>

          </div>
        </div>
      </template>

    </div>
  </div>
</template>

<script>
import { getMe } from '../../services/api.js'

const BASE_URL = 'http://127.0.0.1:8000'

const STATUS_LABEL = {
  pending: 'Na čekanju',
  active: 'Odobren',
  rejected: 'Odbijen'
}

const FILTER_TO_STATUS = {
  'Na čekanju': 'pending',
  'Odobreni': 'active',
  'Odbijeni': 'rejected'
}

export default {
  name: 'AdminAdsView',
  data() {
    return {
      ads: [],
      loading: false,
      activeFilter: 'Sve',
      errorMessage: ''
    }
  },
  computed: {
    filteredAds() {
      if (this.activeFilter === 'Sve') return this.ads
      if (this.activeFilter === 'Obrisani') return this.ads.filter(a => a.is_deleted)
      const status = FILTER_TO_STATUS[this.activeFilter]
      return this.ads.filter(a => !a.is_deleted && a.status === status)
    }
  },
  methods: {
    statusLabel(status) {
      return STATUS_LABEL[status] || status
    },
    statusBadgeClass(status) {
      const base = 'text-xs font-semibold px-2.5 py-1 rounded-full whitespace-nowrap'
      if (status === 'active') return `${base} bg-green-50 text-green-700`
      if (status === 'rejected') return `${base} bg-red-50 text-red-700`
      return `${base} bg-yellow-50 text-yellow-700`
    },
    filterCount(filter) {
      if (filter === 'Sve') return this.ads.length
      if (filter === 'Obrisani') return this.ads.filter(a => a.is_deleted).length
      const status = FILTER_TO_STATUS[filter]
      return this.ads.filter(a => !a.is_deleted && a.status === status).length
    },
    async fetchAds() {
      this.loading = true
      this.errorMessage = ''
      const token = localStorage.getItem('token')
      try {
        const response = await fetch(`${BASE_URL}/ads/admin/list`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        if (!response.ok) throw new Error('Greška pri dohvaćanju oglasa')
        const data = await response.json()
        
        // Mapiramo podatke tako da svaki oglas dobije polje is_deleted i updating
        this.ads = data.map(a => ({ ...a, is_deleted: a.is_deleted || false, updating: null }))
      } catch (err) {
        console.error(err)
        this.errorMessage = 'Neuspješno učitavanje oglasa sa servera.'
      } finally {
        this.loading = false
      }
    },
    async updateAdStatusHandler(ad, newStatus) {
      const token = localStorage.getItem('token')
      ad.updating = newStatus
      try {
        const response = await fetch(`${BASE_URL}/ads/${ad.id}/status`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ status: newStatus })
        })
        
        if (!response.ok) throw new Error('Greška pri promjeni statusa')
        ad.status = newStatus
      } catch (err) {
        console.error(err)
        alert('Nije moguće promijeniti status oglasa.')
      } finally {
        ad.updating = null
      }
    },
    async deleteAdHandler(ad) {
      const token = localStorage.getItem('token')
      ad.updating = 'deleting'
      try {
        // SLANJE BRISANJA NA BACKEND (Prilagodi rutu ako se razlikuje na oglasima)
        const response = await fetch(`${BASE_URL}/ads/${ad.id}`, {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${token}` }
        })
        if (!response.ok) throw new Error('Greška pri brisanju')
        
        ad.is_deleted = true
      } catch (err) {
        console.error(err)
        alert(`Greška pri brisanju oglasa.`)
      } finally {
        ad.updating = null
      }
    },
    async restoreAdHandler(ad) {
      const token = localStorage.getItem('token')
      ad.updating = 'restoring'
      try {
        // SLANJE VRAĆANJA NA BACKEND (Prilagodi rutu ako se razlikuje na oglasima)
        const response = await fetch(`${BASE_URL}/ads/${ad.id}/restore`, {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}` }
        })
        if (!response.ok) throw new Error('Greška pri vraćanju')
        
        ad.is_deleted = false
      } catch (err) {
        console.error(err)
        alert(`Greška pri vraćanju oglasa.`)
      } finally {
        ad.updating = null
      }
    }
  },
  async mounted() {
    // Sigurnosna provjera uloge (identično kao na kompanijama)
    const token = localStorage.getItem('token')
    try {
      const user = await getMe(token)
      if (user.role !== 'admin') {
        this.$router.push('/')
        return
      }
    } catch {
      this.$router.push('/')
      return
    }

    this.fetchAds()
  }
}
</script>