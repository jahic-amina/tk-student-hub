<script setup>
import ForumSidebar from '../../components/ForumSidebar.vue';
import TopicDetailView from './TopicDetailView.vue';
import { ref, onMounted, watch, computed } from 'vue';
import { getTopics, getCategories, deleteTopic as deleteTopicApi } from '../../services/forum.js';

// Reaktivna stanja za teme i kategorije
const teme = ref([]);
const sveKategorije = ref([]); 
const isLoading = ref(true);
const odabraniKategorijaId = ref(null);
const trenutnaStranica = ref(1);
const ukupnoTema = ref(0);
const velicinaStranice = 5;

// Držanje stanja pretrage i detalja
const search = ref("");
const selectedTopic = ref(null);

const ukupnoStranica = computed(() => {
  return Math.ceil(ukupnoTema.value / velicinaStranice) || 1;
});

const trenutnaKategorija = computed(() => {
  if (!odabraniKategorijaId.value) {
    return { name: 'General (Sve teme)', color: '#64748b' };
  }
  return sveKategorije.value.find(c => c.id === odabraniKategorijaId.value) || { name: 'Kategorija', color: '#ff7a00' };
});

const isAdmin = computed(() => {
  return localStorage.getItem('role') === 'admin';
});

const ucitajTeme = async () => {
  isLoading.value = true;
  try {
    const data = await getTopics({
      category_id: odabraniKategorijaId.value,
      page: trenutnaStranica.value,
      per_page: velicinaStranice,
      search: search.value
    }); 
    
    if (data && data.items) {
      teme.value = data.items;      
      ukupnoTema.value = data.total;  
    } else if (Array.isArray(data)) {
      teme.value = data;
      ukupnoTema.value = data.length;
    } else {
      throw new Error("Nema ispravnih podataka.");
    }
  } catch (error) {
    console.warn("Backend rute nisu dostupne, učitavam demo podatke...");
    ukupnoTema.value = 2;
    teme.value = [
      { 
        id: 1, 
        title: "Dobrodošli na TK Student Hub forum", 
        content: "Ovo je prva testna tema na forumu. Ovdje studenti mogu postavljati pitanja i dijeliti iskustva.", 
        views_count: 42, 
        comments_count: 3,
        category: { name: "Opšta diskusija" },
        author: { full_name: "Admin Hub" },
        created_at: new Date()
      },
      { 
        id: 2, 
        title: "Ideje za projekte iz telekomunikacija", 
        content: "Ovdje možemo dijeliti ideje za projekte iz mreža, elektronike i programiranja.", 
        views_count: 15, 
        comments_count: 0,
        category: { name: "Projekti" },
        author: { full_name: "Zijad Lekić" },
        created_at: new Date()
      }
    ];
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  await ucitajTeme();
  try {
    sveKategorije.value = await getCategories();
  } catch (e) {
    console.error("Greška pri učitavanju kategorija u ForumView:", e);
  }
});

watch(odabraniKategorijaId, () => {
  trenutnaStranica.value = 1;
  ucitajTeme();
});

watch(trenutnaStranica, () => {
  ucitajTeme();
});

const filtrirajPoKategoriji = (id) => {
  selectedTopic.value = null;
  odabraniKategorijaId.value = id;
};

const applySearch = () => {
  trenutnaStranica.value = 1;
  selectedTopic.value = null;
  ucitajTeme();
};

const obrisiTemu = async (temaId) => {
  const potvrda = confirm('Da li ste sigurni da želite obrisati ovu temu?');
  if (!potvrda) return;

  try {
    await deleteTopicApi(temaId);
    teme.value = teme.value.filter(tema => tema.id !== temaId);
    ukupnoTema.value = Math.max(0, ukupnoTema.value - 1);
  } catch (error) {
    alert(error.message || 'Brisanje teme nije uspjelo.');
  }
};

function formatDate(dateValue) {
  if (!dateValue) return "";
  return new Intl.DateTimeFormat("bs-BA", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric"
  }).format(new Date(dateValue));
}

function getInitials(name) {
  if (!name) return "?";
  return name.split(" ").map((part) => part[0]).join("").slice(0, 2).toUpperCase();
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 text-slate-900 p-6">
    <div class="max-w-7xl mx-auto">
      
      <div class="flex justify-between items-center mb-8 border-b border-gray-200 pb-4">
        <div>
          <h1 class="text-3xl font-bold tracking-tight text-slate-800">Studentski Forum</h1>
          <p class="text-slate-500 mt-1">Postavi pitanje, podijeli ideju ili pomogni kolegama.</p>
        </div>
        <router-link 
          to="/forum/nova-tema"
          class="bg-[#ff7a00] hover:bg-[#e66e00] text-white font-bold px-6 py-2.5 rounded-lg transition-colors shadow-md text-sm text-center"
        >
          Nova tema
        </router-link>
      </div>

      <div class="flex flex-col md:flex-row gap-8 items-start">
        
        <div class="w-full md:w-72 flex-shrink-0">
          <ForumSidebar 
            :aktivna-kategorija-id="odabraniKategorijaId" 
            @kategorija-izabrana="filtrirajPoKategoriji" 
          />
        </div>

        <div class="flex-1 w-full">
          
          <TopicDetailView
            v-if="selectedTopic"
            :topic="selectedTopic"
            @back="selectedTopic = null; ucitajTeme();"
          />

          <div v-else class="flex flex-col justify-between min-h-[500px]">
            <div>
              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
                <span 
                  class="px-4 py-1.5 font-extrabold text-xs rounded-full border shadow-sm transition-all duration-300"
                  :style="{ 
                    backgroundColor: trenutnaKategorija.color + '15', 
                    borderColor: trenutnaKategorija.color, 
                    color: trenutnaKategorija.color
                  }"
                >
                  {{ trenutnaKategorija.name }}
                </span>

                <div class="flex gap-2 w-full sm:w-80">
                  <input
                    v-model="search"
                    type="text"
                    placeholder="Pretraži teme na forumu..."
                    @keyup.enter="applySearch"
                    class="w-full border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400 bg-white"
                  />
                  <button @click="applySearch" class="bg-slate-800 text-white text-xs px-4 rounded-lg font-bold hover:bg-slate-700 transition-colors">
                    Traži
                  </button>
                </div>
              </div>

              <div v-if="isLoading" class="flex flex-col items-center justify-center py-12">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#ff7a00] mb-4"></div>
                <p class="text-slate-500 italic text-sm">Učitavanje tema...</p>
              </div>

              <div v-else-if="teme.length === 0" class="text-center py-12 bg-white rounded-xl border border-gray-200 p-8 shadow-sm">
                <p class="text-slate-500 text-sm mb-4">
                   Trenutno nema tema u ovoj kategoriji. Započni temu!
                </p>
                <router-link
                   :to="{ 
                     name: 'create-topic', 
                     query: odabraniKategorijaId ? { categoryId: odabraniKategorijaId } : {} 
                  }"
                  class="bg-[#ff7a00] hover:bg-[#e66e00] text-white font-bold px-6 py-2 rounded-lg text-xs transition-colors shadow-md inline-block text-center"
                >
                   Započni temu
                </router-link>
              </div>

              <div v-else class="space-y-4">
                <div 
                  v-for="tema in teme" 
                  :key="tema.id" 
                  @click="selectedTopic = tema"
                  class="p-5 bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all cursor-pointer group"
                >
                  <div class="flex justify-between items-start">
                    <h2 class="text-lg font-bold text-slate-800 group-hover:text-[#ff7a00] transition-colors line-clamp-1">
                      {{ tema.title }}
                    </h2>
                    
                    <div class="flex items-center gap-2 flex-shrink-0 ml-4">
                     <span class="bg-orange-50 text-[#ff7a00] text-[9px] font-extrabold uppercase px-2 py-0.5 rounded tracking-wider">
                       {{ tema.category?.name || tema.category || 'Opšta diskusija' }}
                     </span>

                     <button
                       v-if="isAdmin"
                       @click.stop="obrisiTemu(tema.id)"
                       class="w-7 h-7 flex items-center justify-center rounded-full text-red-600 hover:bg-red-50 hover:text-red-800 transition-colors text-xs"
                       title="Obriši temu"
                     >
                        🗑️
                     </button>
                   </div>
                  </div>
                  
                  <p class="text-slate-500 mt-2 text-xs leading-relaxed line-clamp-2">
                    {{ tema.content }}
                  </p>
                  
                  <div class="flex items-center justify-between mt-5 pt-3 border-t border-gray-100 text-[11px] text-slate-400">
                    <div class="flex items-center gap-1.5">
                      <span class="w-5 h-5 rounded-full bg-slate-100 text-slate-500 flex items-center justify-center font-bold text-[9px]">
                        {{ getInitials(tema.author?.full_name) }}
                      </span>
                      <span class="text-slate-600 font-medium">{{ tema.author?.full_name || 'Korisnik' }}</span>
                      <span>•</span>
                      <span>{{ formatDate(tema.created_at) }}</span>
                    </div>

                    <div class="flex items-center space-x-3 font-semibold">
                      <span>👁️ {{ tema.views_count || 0 }} pregleda</span>
                      <span class="text-[#ff7a00]">💬 {{ tema.comments_count || 0 }} odgovora</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="teme.length > 0 && !isLoading" class="mt-8 flex items-center justify-between border-t border-gray-200 pt-4 pb-4">
              <p class="text-xs text-slate-500">
                Prikazano <span class="font-medium">{{ teme.length }}</span> tema od ukupno <span class="font-medium">{{ ukupnoTema }}</span>
              </p>
              
              <div class="flex items-center space-x-2">
                <button 
                  @click="trenutnaStranica--" 
                  :disabled="trenutnaStranica === 1"
                  class="px-3 py-1.5 bg-white border border-gray-300 rounded-lg text-xs font-medium text-slate-700 hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
                >
                  ← Prethodna
                </button>

                <span class="text-xs font-semibold text-slate-700 px-2">
                  Stranica {{ trenutnaStranica }} od {{ ukupnoStranica }}
                </span>

                <button 
                  @click="trenutnaStranica++" 
                  :disabled="trenutnaStranica === ukupnoStranica"
                  class="px-3 py-1.5 bg-white border border-gray-300 rounded-lg text-xs font-medium text-slate-700 hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
                >
                  Sljedeća →
                </button>
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
</style>