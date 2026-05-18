<template>
  <div class="bg-gray-50 min-h-screen font-sans">
    
    <HeroBanner />

    <div class="max-w-6xl mx-auto px-6 py-8">

      <div class="flex gap-6 border-b border-gray-200 pb-0 mb-6 overflow-x-auto text-sm font-medium">
        <button
          v-for="tab in ['Sve', 'Prakse', 'Edukacije', 'Stipendije', 'Aktuelno']"
          :key="tab"
          :class="['pb-3 px-1 transition-all border-b-2', currentTab === tab ? 'border-orange-500 text-orange-600 font-bold' : 'border-transparent text-gray-500 hover:text-gray-700']"
          @click="currentTab = tab">
          {{ tab }}
        </button>
      </div>

      <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex flex-wrap gap-4 items-center justify-between mb-8">
        <div class="flex-1 min-w-[250px]">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="⌕  Pretraga po nazivu, kompaniji ili oblasti..."
            class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-orange-400"
          />
        </div>
        <div class="flex flex-wrap gap-3 text-sm items-center">
          <button class="px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg font-medium text-gray-700 hover:bg-gray-100">Filter</button>
          <button class="px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg font-medium text-gray-700 hover:bg-gray-100">Saradnik</button>
          <select class="px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg font-medium text-gray-700 focus:outline-none cursor-pointer">
            <option>Oblast</option>
            <option>IT</option>
            <option>Telekomunikacije</option>
            <option>Elektronika</option>
          </select>
          <select class="px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg font-medium text-gray-700 focus:outline-none cursor-pointer">
            <option>Datum</option>
            <option>Najnovije</option>
            <option>Uskoro ističe</option>
          </select>
          
          <div class="flex items-center gap-2 px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg">
            <span class="text-gray-700 font-medium">Plaćeno</span>
            <button
              @click="placeno = !placeno"
              :class="['relative inline-flex h-5 w-10 items-center rounded-full transition-colors duration-200 focus:outline-none', placeno ? 'bg-orange-500' : 'bg-gray-300']"
            >
              <span :class="['inline-block h-4 w-4 transform rounded-full bg-white shadow transition-transform duration-200', placeno ? 'translate-x-5' : 'translate-x-0.5']"></span>
            </button>
          </div>
        </div>
      </div>

      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-bold text-gray-800">{{ filtriraniOglasi.length }} aktivnih oglasa</h2>
        <button class="bg-orange-500 hover:bg-orange-600 text-white text-sm font-semibold px-4 py-2 rounded-lg transition shadow-sm">
          Sačuvane prilike
        </button>
      </div>

      <div v-if="loading" class="text-center py-12 text-gray-500 font-medium">
        Učitavanje oglasa...
      </div>

      <div v-else-if="filtriraniOglasi.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <OglasCard 
          v-for="oglas in filtriraniOglasi" 
          :key="oglas.id" 
          :oglas="oglas" 
        />
      </div>

      <div v-else class="text-center py-12 bg-white rounded-xl border border-dashed border-gray-300">
        <p class="text-gray-500 font-medium text-lg">Nema pronađenih oglasa za traženi pojam.</p>
        <p class="text-gray-400 text-sm mt-1">Pokušajte sa nekom drugom ključnom riječju.</p>
      </div>

    </div>
  </div>
</template>

<script>
import HeroBanner from '@/components/HeroBanner.vue'
import OglasCard from '@/components/OglasCard.vue'

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
      return this.oglasi.filter(oglas => {
        const tabMap = {
          'Sve': true,
          'Prakse': oglas.tip === 'Praksa',
          'Edukacije': oglas.tip === 'Edukacija',
          'Stipendije': oglas.tip === 'Stipendija',
          'Aktuelno': oglas.status === 'Aktivan'
        }
        const mecapTab = tabMap[this.currentTab] ?? true

        const q = this.searchQuery.toLowerCase()
        const mecapSearch = !q ||
          (oglas.naslov && oglas.naslov.toLowerCase().includes(q)) ||
          (oglas.kompanija && oglas.kompanija.toLowerCase().includes(q)) ||
          (oglas.opis && oglas.opis.toLowerCase().includes(q)) ||
          (oglas.tagovi && oglas.tagovi.some(t => t.toLowerCase().includes(q))) ||
          (Array.isArray(oglas.tagovi) && oglas.tagovi.some(t => t.toLowerCase().includes(q)))
        const mecapPlaceno = !this.placeno || (oglas.dodatno && oglas.dodatno.includes('KM'))

        return mecapTab && mecapSearch && mecapPlaceno
      })
    }
  },
  methods: {
    async fetchOglasi() {
      this.loading = true
      try {
        const res = await axios.get('http://127.0.0.1:8000/oglasi/')
        const data = res.data || []

        this.oglasi = data.map(o => ({
          id: o.id,
          naslov: o.naziv || o.naslov || '',
          kompanija: (o.kompanija && (o.kompanija.name || o.kompanija.naziv)) || o.company || '',
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
  mounted() {
    this.fetchOglasi()
  }
}
</script>