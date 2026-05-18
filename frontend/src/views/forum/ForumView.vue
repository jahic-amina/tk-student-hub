<script setup>
import ForumSidebar from '../../components/ForumSidebar.vue';
import { ref, onMounted, watch, computed } from 'vue';
import { getTopics } from '../../services/forum.js'; 

const teme = ref([]);
const isLoading = ref(true);
const odabraniKategorijaId = ref(null);

const trenutnaStranica = ref(1);
const ukupnoTema = ref(0);
const velicinaStranice = 5;

const ukupnoStranica = computed(() => {
  return Math.ceil(ukupnoTema.value / velicinaStranice) || 1;
});

const ucitajTeme = async () => {
  isLoading.value = true;
  try {
    const data = await getTopics(odabraniKategorijaId.value, trenutnaStranica.value, velicinaStranice); 
    teme.value = data.items;      
    ukupnoTema.value = data.total;  
  } catch (error) {
    console.warn("Backend rute nema, učitavam demo podatke...");
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

onMounted(() => {
  ucitajTeme();
});

watch(odabraniKategorijaId, () => {
  trenutnaStranica.value = 1;
  ucitajTeme();
});

watch(trenutnaStranica, () => {
  ucitajTeme();
});

const filtrirajPoKategoriji = (id) => {
  odabraniKategorijaId.value = id;
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
        <button class="bg-[#ff7a00] hover:bg-[#e66e00] text-white font-bold px-6 py-2.5 rounded-lg transition-colors shadow-md">
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

        <div class="flex-1 w-full flex flex-col justify-between min-h-[500px]">
          
          <div>
            <div v-if="odabraniKategorijaId" class="mb-4 flex items-center justify-between bg-orange-50 border border-orange-100 p-3 rounded-xl">
              <p class="text-sm text-slate-700">Filtrirano po izabranoj kategoriji</p>
              <button @click="odabraniKategorijaId = null" class="text-xs font-bold text-slate-400 hover:text-slate-600">
                Prikaži sve
              </button>
            </div>

            <div v-if="isLoading" class="flex flex-col items-center justify-center py-12">
              <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#ff7a00] mb-4"></div>
              <p class="text-slate-500 italic">Učitavanje tema...</p>
            </div>

            <div v-else-if="teme.length === 0" class="text-center py-12 bg-white rounded-xl border border-gray-200 p-6">
              <p class="text-slate-400 italic">Nema objavljenih tema u ovoj kategoriji.</p>
            </div>

            <div v-else class="space-y-4">
              <div 
                v-for="tema in teme" 
                :key="tema.id" 
                class="p-6 bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow cursor-pointer"
              >
                <div class="flex justify-between items-start">
                  <h2 class="text-xl font-bold text-slate-800 hover:text-[#ff7a00] transition-colors">
                    {{ tema.title }}
                  </h2>
                  
                  <span class="bg-orange-50 text-[#ff7a00] text-[10px] font-bold uppercase px-2 py-1 rounded">
                     {{ tema.category_name || tema.category || 'Opšta diskusija' }}
                  </span>
                </div>
                
                <p class="text-slate-600 mt-3 text-sm leading-relaxed">
                  {{ tema.content }}
                </p>
                
                <div class="flex items-center space-x-4 text-xs text-slate-400 mt-6 pt-4 border-t border-gray-50">
                  <span>👁️ {{ tema.views_count || 0 }} pregleda</span>
                  <span>•</span>
                  <span class="text-[#ff7a00] font-medium">Odgovori (0)</span>
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
                class="px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm font-medium text-slate-700 hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm flex items-center"
              >
                ← Prethodna
              </button>

              <span class="text-sm font-semibold text-slate-700 px-3">
                Stranica {{ trenutnaStranica }} od {{ ukupnoStranica }}
              </span>

              <button 
                @click="trenutnaStranica++" 
                :disabled="trenutnaStranica === ukupnoStranica"
                class="px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm font-medium text-slate-700 hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm flex items-center"
              >
                Sljedeća →
              </button>
            </div>
          </div>

        </div>

      </div>
    </div>
  </div>
</template>