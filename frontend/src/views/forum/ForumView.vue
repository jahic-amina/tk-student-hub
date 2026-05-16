<script setup>
import { ref, onMounted } from 'vue';
import { getTopics } from '@/services/forum'; 

const teme = ref([]);
const isLoading = ref(true);

onMounted(async () => {
  try {
    // 1. Pokušavamo da povučemo stvarne podatke sa bekenda
    teme.value = await getTopics(); 
  } catch (error) {
    console.warn("Backend ruta ne postoji, učitavam lažne podatke za dizajn...");
    
    // 2. PRIVREMENO: Pošto API rute još nema, punimo listu lažnim podacima da vidiš dizajn
    teme.value = [
      {
        id: 1,
        title: "Dobrodošli na TK Student Hub forum",
        content: "Ovo je prva testna tema na forumu. Ovdje studenti mogu postavljati pitanja, dijeliti iskustva i pomagati jedni drugima.",
        views_count: 42
      },
      {
        id: 2,
        title: "Ideje za projekte iz telekomunikacija",
        content: "Ovdje možemo dijeliti ideje za projekte iz mreža, elektronike, programiranja i telekomunikacijskih sistema.",
        views_count: 15
      }
    ];
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
  <div class="min-h-screen bg-slate-900 text-slate-100 p-6">
    <div class="max-w-4xl mx-auto">
      
      <div class="flex justify-between items-center mb-8 border-b border-slate-800 pb-4">
        <div>
          <h1 class="text-3xl font-bold tracking-tight text-white">Studentski Forum</h1>
          <p class="text-slate-400 mt-1">Postavi pitanje, podijeli ideju ili pomogni kolegama.</p>
        </div>
        <button class="bg-blue-600 hover:bg-blue-500 text-white font-medium px-4 py-2 rounded-lg transition-colors shadow-lg shadow-blue-600/20">
          Nova tema
        </button>
      </div>

      <div v-if="isLoading" class="flex flex-col items-center justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"></div>
        <p class="text-slate-400">Učitavanje tema...</p>
      </div>

      <div v-else class="space-y-4">
        <div 
          v-for="tema in teme" 
          :key="tema.id" 
          class="p-5 bg-slate-800 rounded-xl border border-slate-700/50 shadow-md hover:border-slate-600 transition-all cursor-pointer"
        >
          <div class="flex justify-between items-start">
            <h2 class="text-xl font-semibold text-blue-400 hover:text-blue-300 transition-colors">
              {{ tema.title }}
            </h2>
          </div>
          
          <p class="text-slate-300 mt-2 line-clamp-2">
            {{ tema.content }}
          </p>
          
          <div class="flex items-center space-x-4 text-xs text-slate-500 mt-4 pt-3 border-t border-slate-700/30">
            <div class="flex items-center space-x-1">
              <span>👁️ {{ tema.views_count }} pregleda</span>
            </div>
            <span>•</span>
            <span class="bg-slate-700/50 text-slate-300 px-2 py-0.5 rounded">Opšta diskusija</span>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>