<template>
  <div class="p-6 max-w-7xl mx-auto min-h-screen bg-slate-50 dark:bg-slate-900 text-gray-900 dark:text-slate-100 transition-colors duration-200">
    
    <!-- Narandžasti Baner (Tačan dizajn sa slike) -->
    <div class="bg-orange-500 text-white p-6 rounded-2xl shadow-sm mb-6 flex items-center gap-4">
      <div class="bg-white/20 backdrop-blur-md px-4 py-3 rounded-xl border border-white/30 font-bold text-xl tracking-wider select-none">
        TK
      </div>
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Aktuelne prilike</h1>
        <p class="text-orange-100 text-sm mt-0.5">Filtriraj prakse, edukacije i stipendije prema TK oblasti</p>
      </div>
    </div>

    <!-- Tabovi + Dugme za vreme pozicionirano pored Stipendije -->
    <div class="flex flex-wrap items-center gap-6 mb-6 text-sm font-semibold border-b border-gray-200/60 dark:border-slate-800 pb-3">
      <button @click="activeTab = 'sve'" :class="activeTab === 'sve' ? 'text-orange-500' : 'text-gray-400 dark:text-slate-400 hover:text-gray-600'" class="bg-transparent border-none cursor-pointer">Sve</button>
      <button @click="activeTab = 'prakse'" :class="activeTab === 'prakse' ? 'text-orange-500' : 'text-gray-400 dark:text-slate-400 hover:text-gray-600'" class="bg-transparent border-none cursor-pointer">Prakse</button>
      <button @click="activeTab = 'edukacije'" :class="activeTab === 'edukacije' ? 'text-orange-500' : 'text-gray-400 dark:text-slate-400 hover:text-gray-600'" class="bg-transparent border-none cursor-pointer">Edukacije</button>
      <button @click="activeTab = 'stipendije'" :class="activeTab === 'stipendije' ? 'text-orange-500' : 'text-gray-400 dark:text-slate-400 hover:text-gray-600'" class="bg-transparent border-none cursor-pointer">Stipendije</button>
      
      <!-- Dugme za Vreme (Ubačeno tačno pored stipendije) -->
      <div class="relative inline-block text-left">
        <button 
          @click="isTimeOpen = !isTimeOpen"
          @keydown.esc.stop.prevent="isTimeOpen = false"
          type="button"
          class="inline-flex items-center gap-1 bg-transparent border-none cursor-pointer transition-colors"
          :class="selectedTime ? 'text-orange-500 font-bold' : 'text-gray-400 dark:text-slate-400 hover:text-gray-600'"
        >
          <span>{{ selectedTimeLabel }}</span>
          <svg class="w-4 h-4 text-gray-400 transition-transform duration-200" :class="isTimeOpen ? 'rotate-180' : ''" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 0 1 1.06.02L10 11.168l3.71-3.938a.75.75 0 1 1 1.08 1.04l-4.24 4.5a.75.75 0 0 1-1.08 0l-4.24-4.5a.75.75 0 0 1 .02-1.06Z" clip-rule="evenodd" />
          </svg>
        </button>
        
        <!-- Padajući meni za Vreme -->
        <div v-if="isTimeOpen" class="absolute left-0 mt-2 z-30 w-44 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-xl shadow-lg overflow-hidden">
          <button 
            v-for="option in timeOptions" 
            :key="option.value"
            @click="selectTime(option.value)"
            type="button"
            class="w-full text-left px-4 py-2 text-xs sm:text-sm hover:bg-gray-50 dark:hover:bg-slate-700 block transition-colors bg-transparent border-none cursor-pointer"
            :class="selectedTime === option.value ? 'text-orange-600 dark:text-orange-400 font-semibold bg-orange-50 dark:bg-orange-950/40' : 'text-gray-700 dark:text-slate-300'"
          >
            {{ option.label }}
          </button>
        </div>
      </div>

      <button @click="activeTab = 'aktuelno'" :class="activeTab === 'aktuelno' ? 'text-orange-500' : 'text-gray-400 dark:text-slate-400 hover:text-gray-600'" class="bg-transparent border-none cursor-pointer">Aktuelno</button>
    </div>

    <!-- Filter Bar Komponenta (Pretraga, Oblast, Plaćeno) -->
    <AdFilter
      v-model:searchQuery="searchQuery"
      v-model:selectedField="selectedField"
      v-model:isPaid="isPaid"
      :fields="fieldsList"
    />

    <!-- Brojač aktivnih oglasa -->
    <h2 class="text-lg font-bold mb-5 text-gray-900 dark:text-slate-100">
      {{ filteredAds.length }} aktivnih oglasa
    </h2>

    <!-- Grid sa Karticama Oglasa (Preslikan dizajn sa tvoje slike) -->
    <div v-if="filteredAds.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      <div 
        v-for="ad in filteredAds" 
        :key="ad.id" 
        class="p-5 bg-white dark:bg-slate-800 rounded-2xl border border-gray-150 dark:border-slate-700/70 shadow-sm flex flex-col justify-between hover:shadow-md transition-all duration-200"
      >
        <div>
          <!-- Gornji tagovi -->
          <div class="flex items-center gap-1.5 mb-3">
            <span class="text-[11px] font-bold px-2 py-0.5 rounded bg-blue-50 dark:bg-blue-950/40 text-blue-600 dark:text-blue-400">
              {{ ad.typeLabel }}
            </span>
            <span class="text-[11px] font-bold px-2 py-0.5 rounded bg-green-50 dark:bg-green-950/40 text-green-600 dark:text-green-400">
              Aktivan
            </span>
            <span v-if="ad.isPaid" class="ml-auto text-[11px] font-bold px-2 py-0.5 rounded bg-orange-100 dark:bg-orange-950/50 text-orange-600 dark:text-orange-400">
              Plaćeno
            </span>
          </div>

          <!-- Naslov i Kompanija -->
          <h3 class="text-base font-bold text-gray-900 dark:text-slate-100 mb-0.5">{{ ad.title }}</h3>
          <p class="text-xs text-gray-400 dark:text-slate-400 mb-3">{{ ad.company }}</p>

          <!-- Detalji (Lokacija, Trajanje, Prijave) -->
          <div class="space-y-1.5 text-xs font-medium mb-3">
            <div class="flex items-center gap-1.5 text-gray-500 dark:text-slate-300">
              <span class="text-red-500">📍</span> {{ ad.location }}
            </div>
            <div class="flex items-center gap-1.5 text-gray-500 dark:text-slate-300">
              <span class="text-gray-400">🕒</span> {{ ad.duration }}
            </div>
            <div class="flex items-center gap-1.5 text-gray-500 dark:text-slate-300">
              <span class="text-blue-500">👥</span> <span class="text-red-500 font-semibold">{{ ad.applicants }}</span>
            </div>
          </div>

          <!-- Cena / Satnica -->
          <div class="text-sm font-bold text-gray-900 dark:text-slate-100 mb-4">
            {{ ad.price }}
          </div>
        </div>

        <!-- Donji tagovi / Oblasti -->
        <div class="flex flex-wrap gap-2 pt-3 border-t border-gray-100 dark:border-slate-700/50">
          <span class="text-[11px] font-semibold px-2 py-1 bg-gray-100/70 dark:bg-slate-700 text-gray-600 dark:text-slate-300 rounded-md">
            {{ ad.field }}
          </span>
          <span class="text-[11px] font-semibold px-2 py-1 bg-gray-100/70 dark:bg-slate-700 text-gray-600 dark:text-slate-300 rounded-md">
            {{ ad.location }}
          </span>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-16 text-gray-400 dark:text-slate-500 font-medium">
      Nema pronađenih oglasa za izabrane filtere.
    </div>
  </div>
</template>

<script>
import AdFilter from './../../components/ads/AdFilter.vue'

export default {
  name: 'AdsView',
  components: {
    AdFilter
  },
  data() {
    return {
      activeTab: 'sve', 
      searchQuery: '',
      selectedField: '',
      isPaid: false,
      selectedTime: '',
      isTimeOpen: false,
      timeOptions: [
        { value: '', label: 'Vreme' },
        { value: '24h', label: 'Zadnja 24 sata' },
        { value: '7d', label: 'Zadnjih 7 dana' },
        { value: '30d', label: 'Zadnjih 30 dana' }
      ],
      fieldsList: ['Web Development', 'Backend Development', 'Quality Assurance', 'Cybersecurity', 'Data Analytics', 'DevOps'],
      ads: [
        {
          id: 1,
          title: 'Junior Web Developer',
          company: 'Tech Solutions d.o.o.',
          type: 'prakse',
          typeLabel: 'Praksa',
          field: 'Web Development',
          location: 'Sarajevo',
          duration: '3 mjeseca',
          applicants: '10/2 prijava',
          price: '300 BAM',
          isPaid: true,
          createdAt: new Date().toISOString()
        },
        {
          id: 2,
          title: 'Backend Developer Internship',
          company: 'Digital Innovations d.o.o.',
          type: 'prakse',
          typeLabel: 'Praksa',
          field: 'Backend Development',
          location: 'Zenica',
          duration: '4 mjeseca',
          applicants: '10/1 prijava',
          price: '350 BAM',
          isPaid: false,
          createdAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
          id: 3,
          title: 'QA Engineer',
          company: 'Cloud Systems d.o.o.',
          type: 'prakse',
          typeLabel: 'Praksa',
          field: 'Quality Assurance',
          location: 'Tuzla',
          duration: '3 mjeseca',
          applicants: '10/3 prijava',
          price: '280 BAM',
          isPaid: true,
          createdAt: new Date(Date.now() - 12 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
          id: 4,
          title: 'Data Analytics Internship',
          company: 'Mobile First d.o.o.',
          type: 'stipendije',
          typeLabel: 'Stipendija',
          field: 'Data Analytics',
          location: 'Mostar',
          duration: '2 mjeseca',
          applicants: '10/1 prijava',
          price: '400 BAM',
          isPaid: false,
          createdAt: new Date(Date.now() - 25 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
          id: 5,
          title: 'Cybersecurity Specialist',
          company: 'Data Analytics Pro d.o.o.',
          type: 'edukacije',
          typeLabel: 'Edukacija',
          field: 'Cybersecurity',
          location: 'Banja Luka',
          duration: '6 mjeseca',
          applicants: '10/2 prijava',
          price: '450 BAM',
          isPaid: true,
          createdAt: new Date(Date.now() - 40 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
          id: 6,
          title: 'DevOps Engineer Intern',
          company: 'Security First d.o.o.',
          type: 'prakse',
          typeLabel: 'Praksa',
          field: 'DevOps',
          location: 'Doboj',
          duration: '4 mjeseca',
          applicants: '10/1 prijava',
          price: '420 BAM',
          isPaid: false,
          createdAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString()
        }
      ]
    }
  },
  computed: {
    selectedTimeLabel() {
      const option = this.timeOptions.find(o => o.value === this.selectedTime)
      return option && option.value !== '' ? option.label : 'Vreme'
    },
    filteredAds() {
      return this.ads.filter(ad => {
        if (this.activeTab !== 'sve' && ad.type !== this.activeTab && this.activeTab !== 'aktuelno') {
          return false
        }
        const matchesSearch = !this.searchQuery || 
          ad.title.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          ad.company.toLowerCase().includes(this.searchQuery.toLowerCase())
        const matchesField = !this.selectedField || ad.field === this.selectedField
        const matchesPaid = !this.isPaid || ad.isPaid === true
        let matchesTime = true
        if (this.selectedTime) {
          const adDate = new Date(ad.createdAt)
          const diffInDays = (new Date() - adDate) / (1000 * 60 * 60 * 24)
          if (this.selectedTime === '24h' && diffInDays > 1) matchesTime = false
          if (this.selectedTime === '7d' && diffInDays > 7) matchesTime = false
          if (this.selectedTime === '30d' && diffInDays > 30) matchesTime = false
        }
        return matchesSearch && matchesField && matchesPaid && matchesTime
      })
    }
  },
  methods: {
    selectTime(value) {
      this.selectedTime = value
      this.isTimeOpen = false
    }
  }
}
</script>