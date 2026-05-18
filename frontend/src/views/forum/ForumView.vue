<script setup>
import ForumSidebar from '../../components/ForumSidebar.vue';
import { ref, onMounted, computed } from 'vue';
import { getTopics } from '../../services/forum.js'; 

const teme = ref([]);
const isLoading = ref(true);


const odabraniKategorijaId = ref(null);

onMounted(async () => {
  try {
    
    teme.value = await getTopics(); 
  } catch (error) {
    console.warn("Backend rute nema, učitavam demo podatke...");
    
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
});


const filtrirajPoKategoriji = (id) => {
  if (odabraniKategorijaId.value === id) {
    odabraniKategorijaId.value = null; 
  } else {
    odabraniKategorijaId.value = id;
  }
};


const filtriraneTeme = computed(() => {
  if (!odabraniKategorijaId.value) {
    return teme.value;
  }
  return teme.value.filter(t => t.category_id === odabraniKategorijaId.value);
});
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

        <div class="flex-1 w-full">
          
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

          <div v-else class="space-y-4">
            <div 
              v-for="tema in filtriraneTeme" 
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

      </div>
    </div>
  </div>
</template>