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

      <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex flex-col lg:flex-row gap-4 items-stretch lg:items-center justify-between mb-6">
        
        <div class="flex-1">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="⌕  Pretraga po nazivu, kompaniji..."
            class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-orange-400"
          />
        </div>
        
        <div class="grid grid-cols-2 sm:flex sm:flex-wrap gap-2.5 text-sm items-center">
          <button class="w-full sm:w-auto px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg font-medium text-gray-700 hover:bg-gray-100 text-center text-xs sm:text-sm">
            Filter
          </button>
          <button class="w-full sm:w-auto px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg font-medium text-gray-700 hover:bg-gray-100 text-center text-xs sm:text-sm">
            Saradnik
          </button>
          
          <select class="w-full sm:w-auto px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg font-medium text-gray-700 focus:outline-none cursor-pointer text-xs sm:text-sm">
            <option>Oblast</option>
            <option>IT</option>
            <option>Telekomunikacije</option>
            <option>Elektronika</option>
          </select>
          
          <select class="w-full sm:w-auto px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg font-medium text-gray-700 focus:outline-none cursor-pointer text-xs sm:text-sm">
            <option>Datum</option>
            <option>Najnovije</option>
            <option>Uskoro ističe</option>
          </select>
          
          <div class="col-span-2 sm:col-span-1 flex items-center justify-between sm:justify-start gap-3 px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg">
            <span class="text-gray-700 font-medium text-xs sm:text-sm">Plaćeno</span>
            <button
              @click="placeno = !placeno"
              :class="['relative inline-flex h-5 w-10 items-center rounded-full transition-colors duration-200 focus:outline-none', placeno ? 'bg-orange-500' : 'bg-gray-300']"
            >
              <span :class="['inline-block h-4 w-4 transform rounded-full bg-white shadow transition-transform duration-200', placeno ? 'translate-x-5' : 'translate-x-0.5']"></span>
            </button>
          </div>
        </div>
      </div>

      <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3 mb-6">
        <h2 class="text-lg sm:text-xl font-bold text-gray-800 text-center sm:text-left">
          {{ filtriraniOglasi.length }} aktivnih oglasa
        </h2>
        <button class="w-full sm:w-auto bg-orange-500 hover:bg-orange-600 text-white text-xs sm:text-sm font-semibold px-4 py-2.5 rounded-lg transition shadow-sm text-center">
          Sačuvane prilike
        </button>
      </div>

      <div v-if="loading" class="text-center py-12 text-gray-500 font-medium text-sm">
        Učitavanje oglasa...
      </div>

      <div v-else-if="filtriraniOglasi.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        <OglasCard 
          v-for="oglas in filtriraniOglasi" 
          :key="oglas.id" 
          :oglas="oglas" 
        />
      </div>

      <div v-else class="text-center py-10 px-4 bg-white rounded-xl border border-dashed border-gray-300">
        <p class="text-gray-500 font-medium text-base sm:text-lg">Nema pronađenih oglasa za traženi pojam.</p>
        <p class="text-gray-400 text-xs sm:text-sm mt-1">Pokušajte sa nekom drugom ključnom riječi.</p>
      </div>

    </div>
  </div>
</template>

<script>
import HeroBanner from './HeroBanner.vue'
import OglasCard from './OglasCard.vue'
import axios from 'axios'

export default {
  name: 'OglasiPage',
  components: {
    HeroBanner,
    OglasCard
  },
  data() {
    return {
      loading: false, 
      currentTab: 'Sve',
      searchQuery: '',
      placeno: false,
      oglasi: [] 
    }
  },
  computed: {
    filtriraniOglasi() {
      if (!this.placeno) return this.oglasi
      return this.oglasi.filter(oglas => oglas.dodatno && oglas.dodatno.includes('KM'))
    }
  },
  methods: {
    async fetchOglasi() {
      this.loading = true
      try {
        const params = {}

        if (this.searchQuery) {
          params.search = this.searchQuery
        }

        if (this.currentTab === 'Prakse') {
          params.tip = 'praksa'
        } else if (this.currentTab === 'Edukacije') {
          params.tip = 'edukacija'
        } else if (this.currentTab === 'Stipendije') {
          params.tip = 'stipendija'
        } else if (this.currentTab === 'Aktuelno') {
          params.status = 'active'
        }

        const res = await axios.get('http://127.0.0.1:8000/oglasi/', { params })
        const data = res.data || []

        this.oglasi = data.map(o => ({
          id: o.id,
          naslov: o.naziv || o.naslov || '',
          kompanija: (o.kompanija && (o.kompanija.name || o.kompanija.naziv)) || o.company || (o.kompanija_id ? `Kompanija #${o.kompanija_id}` : ''),
          opis: o.opis || '',
          tagovi: o.tagovi || [],
          tip: o.tip ? (typeof o.tip === 'string' ? (o.tip.charAt(0).toUpperCase() + o.tip.slice(1)) : o.tip) : '',
          dodatno: o.naknada || o.dodatno || '',
          status: (o.status === 'active' ? 'Aktivan' : o.status === 'expired' ? 'Istekao' : o.status) || '',
          lokacija: o.lokacija || 'Nije navedeno',
          trajanje: o.trajanje || ''
        }))
      } catch (err) {
        console.error('Neuspješan dohvat oglasa', err)
      } finally {
        this.loading = false
      }
    }
  },
  watch: {
    searchQuery() {
      clearTimeout(this._searchTimer)
      this._searchTimer = setTimeout(() => this.fetchOglasi(), 400)
    },
    currentTab() {
      this.fetchOglasi()
    }
  },
  mounted() {
    this.fetchOglasi()
  }
}
</script>

<style scoped>
/* Sakriva scrollbar za tabove na mobilnom, ali zadržava mogućnost skrolovanja prstom */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>