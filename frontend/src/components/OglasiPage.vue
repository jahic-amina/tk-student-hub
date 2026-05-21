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

      <OglasFilters 
        v-model:searchQuery="searchQuery"
        v-model:placeno="placeno"
        v-model:selectedOblast="selectedOblast"
        :oblasti="oblasti"
      />

      <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3 mb-6">
        <h2 class="text-base sm:text-lg font-bold text-gray-800 text-center sm:text-left">
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
        <p class="text-gray-400 text-xs sm:text-sm mt-1">Pokušajte sa nekom drugom ključnom riječi ili filterom.</p>
      </div>

    </div>
  </div>
</template>

<script>
import HeroBanner from './HeroBanner.vue'
import OglasFilters  from './OglasFilter.vue'
import OglasCard from './OglasCard.vue' //
import { getApprovedCompanies, getPublicAds } from '../services/api.js'

const TAB_TO_TYPE = {
  Prakse: 'internship',
  Edukacije: 'education',
  Stipendije: 'scholarship'
}

function formatTip(type) {
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
  name: 'OglasiPage',
  components: {
    HeroBanner,
    OglasFilters,
    OglasCard 
  },
  data() {
    return {
      loading: false, 
      currentTab: 'Sve',
      searchQuery: '',
      placeno: false,
      selectedOblast: '', 
      oglasi: [],
      oblasti: [],
      errorMessage: ''
    }
  },
  computed: {
    filtriraniOglasi() {
      return this.oglasi.filter(oglas => {
        const tabMap = {
          'Sve': true,
          'Prakse': oglas.typeKey === 'internship',
          'Edukacije': oglas.typeKey === 'education',
          'Stipendije': oglas.typeKey === 'scholarship',
          'Aktuelno': oglas.statusKey === 'active'
        }
        const mecapTab = tabMap[this.currentTab] ?? true

        const q = this.searchQuery.toLowerCase()
        const mecapSearch = !q ||
          (oglas.naslov && oglas.naslov.toLowerCase().includes(q)) ||
          (oglas.kompanija && oglas.kompanija.toLowerCase().includes(q)) ||
          (oglas.opis && oglas.opis.toLowerCase().includes(q)) ||
          (Array.isArray(oglas.tagovi) && oglas.tagovi.some(t => t.toLowerCase().includes(q)))

        const mecapPlaceno = !this.placeno || Boolean(oglas.dodatno)

        const mecapOblast = !this.selectedOblast || oglas.oblast === this.selectedOblast

        return mecapTab && mecapSearch && mecapPlaceno && mecapOblast
      })
    }
  },
  methods: {
    async fetchOglasi() {
      this.loading = true
      this.errorMessage = ''
      try {
        const [ads, companies] = await Promise.all([
          getPublicAds(),
          getApprovedCompanies()
        ])

        const companiesById = new Map(
          (companies || []).map(company => [company.id, company.company_name])
        )

        this.oglasi = (ads || []).map(ad => {
          const companyName = companiesById.get(ad.company_id) || `Kompanija #${ad.company_id}`
          const additionalInfo = formatCompensation(ad.compensation, ad.currency)

          return {
            id: ad.id,
            naslov: ad.title || '',
            kompanija: companyName,
            opis: ad.description || '',
            tagovi: [ad.field, ad.location].filter(Boolean),
            tip: formatTip(ad.type),
            dodatno: additionalInfo,
            status: formatStatus(ad.status),
            statusKey: ad.status,
            typeKey: ad.type,
            lokacija: ad.location || 'Nije navedeno',
            trajanje: ad.duration_months ? `${ad.duration_months} mjeseci` : '',
            oblast: ad.field || ''
          }
        })

        if (this.currentTab !== 'Sve') {
          const wantedType = TAB_TO_TYPE[this.currentTab]
          this.oglasi = this.oglasi.filter(oglas => {
            if (this.currentTab === 'Aktuelno') return oglas.statusKey === 'active'
            return oglas.typeKey === wantedType
          })
        }

        const sveOblasti = this.oglasi.map(o => o.oblast).filter(Boolean)
        this.oblasti = [...new Set(sveOblasti)]

      } catch (err) {
        console.error('Neuspješan dohvat oglasa', err)
        this.errorMessage = 'Ne mogu učitati oglase sa backend-a. Provjeri da li je API pokrenut na 127.0.0.1:8000.'
      } finally {
        this.loading = false
      }
    }
  },
  watch: {
    currentTab() {
      if (!this.oglasi.length) {
        this.fetchOglasi()
      }
    }
  },
  mounted() {
    this.fetchOglasi()
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