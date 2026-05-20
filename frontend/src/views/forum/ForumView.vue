<script setup>
import ForumSidebar from '../../components/ForumSidebar.vue';
import CreateTopicView from './CreateTopicView.vue';
import TopicDetailView from './TopicDetailView.vue';
import { ref, onMounted, watch, computed } from 'vue';
import { getTopics, getCategories, deleteTopic as deleteTopicApi } from '../../services/forum.js';


const teme = ref([]);
const sveKategorije = ref([]); 
const isLoading = ref(true);
const odabraniKategorijaId = ref(null);
const trenutnaStranica = ref(1);
const ukupnoTema = ref(0);
const velicinaStranice = 5;


const showCreateForm = ref(false);
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
    const data = await getTopics(odabraniKategorijaId.value, trenutnaStranica.value, velicinaStranice); 
    if (data && data.items) {
      teme.value = data.items;      
      ukupnoTema.value = data.total;  
    } else {
      throw new Error("Nema ispravnih podataka.");
    }
  } catch (error) {
    console.warn("Backend rute nema ili niste ulogovani, učitavam demo podatke...");
    ukupnoTema.value = 2;
    teme.value = [
      { 
        id: 1, 
        title: "Dobrodošli na TK Student Hub forum", 
        content: "Ovo je prva testna tema na forumu. Ovdje studenti mogu postavljati pitanja i dijeliti iskustva.", 
        views_count: 42, 
        category: "Opšta diskusija",
        category_id: 1 
      },
      { 
        id: 2, 
        title: "Ideje za projekte iz telekomunikacija", 
        content: "Ovdje možemo dijeliti ideje za projekte iz mreža, elektronike i programiranja.", 
        views_count: 15, 
        category: "Projekti",
        category_id: 5
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
  showCreateForm.value = false;
  selectedTopic.value = null;
  odabraniKategorijaId.value = id;
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

const onTopicCreated = async () => {
  showCreateForm.value = false;
  await ucitajTeme();
};
</script>

<template>
  <div class="min-h-screen bg-gray-50 text-slate-900 p-6">
    <div class="max-w-7xl mx-auto">
      
      <div class="flex justify-between items-center mb-8 border-b border-gray-200 pb-4">
        <div>
          <h1 class="text-3xl font-bold tracking-tight text-slate-800">Studentski Forum</h1>
          <p class="text-slate-500 mt-1">Postavi pitanje, podijeli ideju ili pomogni kolegama.</p>
        </div>
        <button 
          @click="showCreateForm = true; selectedTopic = null;"
          class="bg-[#ff7a00] hover:bg-[#e66e00] text-white font-bold px-6 py-2.5 rounded-lg transition-colors shadow-md"
        >
          Nova tema
        </button>
      </div>

      <div class="flex flex-col md:flex-row gap-8 items-start">
        
        <div class="w-full md:w-72 flex-shrink-0">
          <ForumSidebar 
            :aktivna-kategorija-id="odabraniKategorijaId" 
            @kategorija-izabrana="filtrirajPoKategoriji" 
          />
        </div>

        <div class="flex-1 w-full">
          
          <CreateTopicView
            v-if="showCreateForm"
            @topic-created="onTopicCreated"
            @cancel="showCreateForm = false"
          />

          <TopicDetailView
            v-else-if="selectedTopic"
            :topic="selectedTopic"
            @back="selectedTopic = null"
          />

          <div v-else class="flex flex-col justify-between min-h-[500px]">
            <div>
              <div class="mb-6 flex">
                <span 
                  class="px-4 py-1.5 font-extrabold text-sm rounded-full border shadow-sm transition-all duration-300"
                  :style="{ 
                    backgroundColor: trenutnaKategorija.color + '15', 
                    borderColor: trenutnaKategorija.color, 
                    color: trenutnaKategorija.color
                  }"
                >
                  {{ trenutnaKategorija.name }}
                </span>
              </div>

              <div v-if="isLoading" class="flex flex-col items-center justify-center py-12">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#ff7a00] mb-4"></div>
                <p class="text-slate-500 italic">Učitavanje tema...</p>
              </div>

              <div v-else-if="teme.length === 0" class="text-center py-12 bg-white rounded-xl border border-gray-200 p-8">
                <p class="text-slate-500 text-base mb-4">
                   Trenutno nema tema u ovoj kategoriji. Započni temu!
                </p>
                <button
                   @click="showCreateForm = true"
                   class="bg-[#ff7a00] hover:bg-[#e66e00] text-white font-bold px-6 py-2.5 rounded-lg transition-colors shadow-md"
                >
                   Započni temu
                </button>
              </div>

              <div v-else class="space-y-4">
                <div 
                  v-for="tema in teme" 
                  :key="tema.id" 
                  @click="selectedTopic = tema"
                  class="p-6 bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                >
                  <div class="flex justify-between items-start">
                    <h2 class="text-xl font-bold text-slate-800 hover:text-[#ff7a00] transition-colors">
                      {{ topic ? topic.title : tema.title }}
                    </h2>
                    
                    <div class="flex items-center gap-2">
                     <span class="bg-orange-50 text-[#ff7a00] text-[10px] font-bold uppercase px-2 py-1 rounded">
                       {{ tema.category_name || tema.category || 'Opšta diskusija' }}
                     </span>

                     <button
                       v-if="isAdmin"
                       @click.stop="obrisiTemu(tema.id)"
                       class="w-8 h-8 flex items-center justify-center rounded-full text-red-600 hover:bg-red-50 hover:text-red-800 transition-colors"
                       title="Obriši temu"
                     >
                        🗑️
                     </button>
                   </div>
                  </div>
                  
                  <p class="text-slate-600 mt-3 text-sm leading-relaxed line-clamp-2">
                    {{ tema.content }}
                  </p>
                  
                  <div class="flex items-center space-x-4 text-xs text-slate-400 mt-6 pt-4 border-t border-gray-50">
                    <span>👁️ {{ tema.views_count || 0 }} pregleda</span>
                    <span>•</span>
                    <span class="text-[#ff7a00] font-medium">💬 Pogledaj odgovore</span>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="teme.length > 0 && !isLoading" class="mt-8 flex items-center justify-between border-t border-gray-200 pt-4 pb-8">
              <p class="text-sm text-slate-500">
                Prikazano <span class="font-medium">{{ teme.length }}</span> tema od ukupno <span class="font-medium">{{ ukupnoTema }}</span>
              </p>
              
              <div class="flex items-center space-x-2">
                <button 
                  @click="trenutnaStranica--" 
                  :disabled="trenutnaStranica === 1"
                  class="px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm font-medium text-slate-700 hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
                >
                  ← Prethodna
                </button>

                <span class="text-sm font-semibold text-slate-700 px-3">
                  Stranica {{ trenutnaStranica }} od {{ ukupnoStranica }}
                </span>

                <button 
                  @click="trenutnaStranica++" 
                  :disabled="trenutnaStranica === ukupnoStranica"
                  class="px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm font-medium text-slate-700 hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
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