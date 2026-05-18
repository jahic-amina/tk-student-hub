<template>
  <div class="bg-gray-50 min-h-screen font-sans">
    <div class="bg-gradient-to-r from-orange-500 to-orange-600 text-white py-12 px-6 relative overflow-hidden shadow-md">
      <div class="absolute -right-10 -top-10 w-40 h-40 bg-white/10 rounded-full blur-xl"></div>
      <div class="absolute left-10 -bottom-10 w-32 h-32 bg-black/10 rounded-full blur-lg"></div>

      <div class="max-w-6xl mx-auto flex flex-col items-center text-center relative z-10">
        <div class="bg-white/20 backdrop-blur-sm p-3 rounded-xl mb-4 font-bold text-xl tracking-wider border border-white/20">
          TK
        </div>
        <h1 class="text-4xl font-extrabold tracking-tight mb-2">Aktuelne prilike</h1>
        <p class="text-orange-100 text-lg">Filtriraj prakse, edukacije i stipendije prema TK oblasti</p>
      </div>
    </div>

    <div class="max-w-6xl mx-auto px-6 py-8">
      
      <div class="flex gap-6 border-b border-gray-200 pb-3 mb-6 overflow-x-auto text-sm font-medium">
        <button v-for="tab in ['Sve', 'Prakse', 'Edukacije', 'Stipendije', 'Aktuelno']" :key="tab"
                :class="['pb-3 px-1 transition-all', currentTab === tab ? 'border-b-2 border-orange-500 text-orange-600 font-bold' : 'text-gray-500 hover:text-gray-700']"
                @click="currentTab = tab">
          {{ tab }}
        </button>
      </div>

      <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex flex-wrap gap-4 items-center justify-between mb-8">
        <div class="flex-1 min-w-[250px]">
          <input type="text" v-model="searchQuery" placeholder="⌕ Pretraga po nazivu, kompaniji ili oblasti" 
                 class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-orange-400" />
        </div>
        <div class="flex flex-wrap gap-3 text-sm">
          <button class="px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg font-medium text-gray-700 hover:bg-gray-100">Filter</button>
          <button class="px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg font-medium text-gray-700 hover:bg-gray-100">Saradnik</button>
          <select class="px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg font-medium text-gray-700 focus:outline-none">
            <option>Oblast</option>
          </select>
          <select class="px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg font-medium text-gray-700 focus:outline-none">
            <option>Datum</option>
          </select>
          <div class="flex items-center gap-2 px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg">
            <span class="text-gray-700 font-medium">Plaćeno</span>
            <input type="checkbox" class="accent-orange-500 h-4 w-4 cursor-pointer" />
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
        Učitavanje oglasa sa backenda...
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="oglas in filtriraniOglasi" :key="oglas.id" 
             class="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm flex flex-col justify-between hover:shadow-md transition duration-200">
          
          <div>
            <div class="flex gap-2 mb-4 text-xs font-semibold">
              <span :class="getTipKlasa(oglas.tip)">{{ oglas.tip }}</span>
              <span :class="getStatusKlasa(oglas.status)">{{ oglas.status }}</span>
            </div>

            <h3 class="text-lg font-bold text-gray-900 mb-1 leading-snug">{{ oglas.naslov }}</h3>
            <p class="text-gray-400 text-sm mb-4 font-medium">{{ oglas.kompanija }}</p>

            <div class="flex flex-wrap gap-x-4 gap-y-1 text-gray-500 text-xs font-medium mb-4">
              <span>📍 {{ oglas.lokacija }}</span>
              <span>🕒 {{ oglas.trajanje }}</span>
              <span v-if="oglas.dodatno">💰 {{ oglas.dodatno }}</span>
            </div>
          </div>

          <div class="flex flex-wrap gap-2 mt-auto pt-2">
            <span v-for="tag in oglas.tagovi" :key="tag" 
                  class="bg-gray-100 text-gray-600 text-xs px-3 py-1 rounded-md font-semibold tracking-wide">
              {{ tag }}
            </span>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'OglasiPage',
  data() {
    return {
      oglasi: [],
      loading: true,
      currentTab: 'Sve',
      searchQuery: ''
    }
  },
  computed: {
    filtriraniOglasi() {
      return this.oglasi.filter(oglas => {
        // Filter po tabovima
        const mecapTab = this.currentTab === 'Sve' || oglas.tip + 's' === this.currentTab || oglas.tip === this.currentTab.slice(0, -1); // Jednostavna logika za množinu/jedninu
        
        // Filter po pretrazi
        const mecapSearch = oglas.naslov.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                            oglas.kompanija.toLowerCase().includes(this.searchQuery.toLowerCase());
        
        return mecapTab && mecapSearch;
      });
    }
  },
  mounted() {
    this.fetchOglasi();
  },
  methods: {
    fetchOglasi() {
      // NAPOMENA: Ruta mora biti JAVNA na backendu (bez provjere Bearer tokena)
      fetch('http://localhost:5000/api/oglasi') // Zamijeni sa tvojom stvarnom backend rutom
        .then(res => res.json())
        .then(data => {
          this.oglasi = data;
          this.loading = false;
        })
        .catch(err => {
          console.error("Greška pri povlačenju podataka:", err);
          this.loading = false;
        });
    },
    getTipKlasa(tip) {
      if (tip === 'Praksa') return 'bg-blue-50 text-blue-600 px-2.5 py-1 rounded-md';
      if (tip === 'Edukacija') return 'bg-indigo-50 text-indigo-600 px-2.5 py-1 rounded-md';
      return 'bg-amber-50 text-amber-600 px-2.5 py-1 rounded-md'; // Stipendija
    },
    getStatusKlasa(status) {
      if (status === 'Aktivan') return 'bg-green-50 text-green-600 px-2.5 py-1 rounded-md';
      if (status === 'Uskoro ističe') return 'bg-orange-50 text-orange-600 px-2.5 py-1 rounded-md';
      return 'bg-red-50 text-red-600 px-2.5 py-1 rounded-md'; // Istekao
    }
  }
}
</script>