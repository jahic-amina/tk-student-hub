<template>
  <div class="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8 font-sans text-gray-800">
    <div class="max-w-6xl mx-auto">
      
      <div class="mb-8">
        <h1 class="text-2xl font-black text-gray-900">Upravljanje oglasima</h1>
        <p class="text-sm text-gray-500 mt-1">Pregled, odobravanje i odbijanje oglasa za praksu.</p>
      </div>

      <div class="flex gap-2 mb-6 overflow-x-auto pb-2">
        <button @click="currentTab = 'pending'" :class="tabClass('pending')">
          Na čekanju ({{ countStatus('pending') }})
        </button>
        <button @click="currentTab = 'active'" :class="tabClass('active')">
          Odobreni ({{ countStatus('active') }})
        </button>
        <button @click="currentTab = 'rejected'" :class="tabClass('rejected')">
          Odbijeni ({{ countStatus('rejected') }})
        </button>
        <button @click="currentTab = 'all'" :class="tabClass('all')">
          Svi oglasi ({{ ads.length }})
        </button>
      </div>

      <div v-if="errorMessage" class="p-4 mb-4 bg-red-50 border border-red-200 rounded-2xl text-red-700 text-sm">
        {{ errorMessage }}
      </div>

      <div v-if="loading" class="text-center py-12 text-gray-500 text-sm font-medium">
        Učitavanje oglasa...
      </div>

      <div v-else-if="filteredAds.length === 0" class="text-center py-12 bg-white rounded-3xl border border-dashed border-gray-200">
        <p class="text-gray-400 text-sm">Trenutno nema oglasa u ovoj kategoriji.</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div v-for="ad in filteredAds" :key="ad.id" class="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col justify-between">
          
          <div>
            <div class="flex justify-between items-start mb-2">
              <h3 class="text-lg font-bold text-gray-900 leading-tight">{{ ad.title }}</h3>
              <span :class="badgeClass(ad.status)">{{ ad.status }}</span>
            </div>
            <p class="text-sm text-orange-600 font-bold mb-4">{{ ad.company_name || `Kompanija ID: ${ad.company_id}` }}</p>
            
            <div class="text-sm text-gray-500 space-y-1 mb-6">
              <p>📍 {{ ad.location }} | 💼 {{ ad.field }}</p>
              <p>⏳ Rok prijave: <span class="font-semibold text-gray-700">{{ ad.deadline }}</span></p>
              <p v-if="ad.duration_months">📅 Trajanje: {{ ad.duration_months }} mj.</p>
            </div>
          </div>

          <div v-if="ad.status === 'pending'" class="flex gap-2 pt-4 border-t border-gray-100 mt-auto">
            <button @click="updateAdStatus(ad.id, 'active')" class="flex-1 py-2 bg-green-50 text-green-700 text-xs font-bold uppercase tracking-wide rounded-xl hover:bg-green-100 transition">
              Odobri
            </button>
            <button @click="updateAdStatus(ad.id, 'rejected')" class="flex-1 py-2 bg-red-50 text-red-700 text-xs font-bold uppercase tracking-wide rounded-xl hover:bg-red-100 transition">
              Odbiji
            </button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
const BASE_URL = 'http://127.0.0.1:8000'

export default {
  name: 'AdminAdsView',
  data() {
    return {
      ads: [],
      loading: false,
      currentTab: 'pending',
      errorMessage: ''
    }
  },
  computed: {
    filteredAds() {
      if (this.currentTab === 'all') return this.ads;
      return this.ads.filter(ad => ad.status === this.currentTab);
    }
  },
  methods: {
    tabClass(tabName) {
      const isActive = this.currentTab === tabName;
      return `px-4 py-2 text-sm font-bold rounded-xl transition ${
        isActive 
          ? 'bg-orange-600 text-white shadow-sm' 
          : 'bg-white text-gray-500 border border-gray-200 hover:bg-gray-50'
      }`;
    },
    badgeClass(status) {
      if (status === 'active') return 'text-xs font-semibold px-2.5 py-1 rounded-full bg-green-50 text-green-700';
      if (status === 'pending') return 'text-xs font-semibold px-2.5 py-1 rounded-full bg-yellow-50 text-yellow-700';
      if (status === 'rejected') return 'text-xs font-semibold px-2.5 py-1 rounded-full bg-red-50 text-red-700';
      return 'text-xs font-semibold px-2.5 py-1 rounded-full bg-gray-100 text-gray-700';
    },
    countStatus(status) {
      return this.ads.filter(ad => ad.status === status).length;
    },
    async fetchAds() {
      this.loading = true;
      this.errorMessage = '';
      const token = localStorage.getItem('token'); 
      try {
        const response = await fetch(`${BASE_URL}/ads/admin/list`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Greška pri dohvaćanju oglasa');
        this.ads = await response.json();
      } catch (err) {
        console.error(err);
        this.errorMessage = 'Neuspješno učitavanje oglasa sa servera.';
      } finally {
        this.loading = false;
      }
    },
    async updateAdStatus(adId, newStatus) {
      const token = localStorage.getItem('token');
      try {
        const response = await fetch(`${BASE_URL}/ads/${adId}/status`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ status: newStatus })
        });
        
        if (!response.ok) throw new Error('Greška pri promjeni statusa');
        
        const index = this.ads.findIndex(a => a.id === adId);
        if (index !== -1) {
          this.ads[index].status = newStatus;
        }
      } catch (err) {
        console.error(err);
        alert('Nije moguće promijeniti status oglasa.');
      }
    }
  },
  mounted() {
    this.fetchAds();
  }
}
</script>