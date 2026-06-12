<template>
  <div class="w-full flex flex-col gap-5 select-none animate-in fade-in duration-300">
    
    <div 
      v-if="isCategoryPage && categoryTopics.length >= 3" 
      class="bg-white dark:bg-slate-800 rounded-2xl border border-gray-100 dark:border-slate-700 p-4 shadow-sm transition-all hover:shadow-md"
    >
      <div class="flex items-center gap-2 mb-4 pb-2 border-b border-gray-100 dark:border-slate-700">
        <span class="text-base text-amber-500">⭐</span>
        <h3 class="text-xs font-black uppercase tracking-wider text-slate-800 dark:text-slate-200">
          Najpopularnije u kategoriji
        </h3>
      </div>

      <div v-if="isCategoryLoading" class="flex flex-col items-center justify-center py-4 gap-2">
        <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-amber-500"></div>
      </div>

      <div v-else class="space-y-4">
        <router-link 
          v-for="tema in categoryTopics" 
          :key="tema.id" 
          :to="`/forum/tema/${tema.id}`" 
          class="block group cursor-pointer"
        >
          <div class="text-sm font-bold text-slate-800 dark:text-slate-100 group-hover:text-amber-500 transition-colors line-clamp-2 leading-snug">
            {{ skratiNaslov(tema.title) }}
          </div>
          <div class="flex items-center gap-3 mt-2 text-[11px] text-slate-400 dark:text-slate-500 font-semibold">
            <span>👁️ {{ tema.views_count || 0 }}</span>
            <span>❤️ {{ tema.likes_count || 0 }}</span>
          </div>
        </router-link>
      </div>
    </div>

    <div class="bg-white dark:bg-slate-800 rounded-2xl border border-gray-100 dark:border-slate-700 p-4 shadow-sm transition-all hover:shadow-md">
      <div class="flex items-center gap-2 mb-4 pb-2 border-b border-gray-100 dark:border-slate-700">
        <span class="text-base text-orange-500">🔥</span>
        <h3 class="text-xs font-black uppercase tracking-wider text-slate-800 dark:text-slate-200">
          Popularne teme (7 dana)
        </h3>
      </div>

      <div v-if="isLoading" class="flex flex-col items-center justify-center py-6 gap-2">
        <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-orange-500"></div>
        <span class="text-[10px] text-slate-400 font-medium">Učitavanje...</span>
      </div>

      <div v-else-if="popularTopics.length === 0" class="text-center py-6 text-xs text-slate-400 dark:text-slate-500 font-medium">
        Nema aktivnih tema u proteklih 7 dana.
      </div>

      <div v-else class="space-y-4">
        <router-link 
          v-for="tema in popularTopics" 
          :key="tema.id" 
          :to="`/forum/tema/${tema.id}`" 
          class="block group cursor-pointer"
        >
          <div class="text-sm font-bold text-slate-800 dark:text-slate-100 group-hover:text-orange-500 transition-colors line-clamp-2 leading-snug">
            {{ skratiNaslov(tema.title) }}
          </div>
          <div class="flex items-center gap-3 mt-2 text-[11px] text-slate-400 dark:text-slate-500 font-semibold">
            <span class="flex items-center gap-1">💬 {{ tema.comments_count || 0 }}</span>
            <span 
              class="px-2 py-0.5 rounded text-[10px] font-bold"
              :style="{ backgroundColor: (tema.category?.color || '#ff7a00') + '15', color: tema.category?.color || '#ff7a00' }"
            >
              {{ tema.category?.name || 'Kategorija' }}
            </span>
          </div>
        </router-link>
      </div>
    </div>

    <div class="bg-white dark:bg-slate-800 rounded-2xl border border-gray-100 dark:border-slate-700 p-4 shadow-sm">
      <div class="flex items-center gap-2 mb-4 pb-2 border-b border-gray-100 dark:border-slate-700">
        <span class="text-base text-blue-500">📊</span>
        <h3 class="text-xs font-black uppercase tracking-wider text-slate-800 dark:text-slate-200">
          Statistika zajednice
        </h3>
      </div>
      <div class="grid grid-cols-2 gap-3">
        <div class="bg-gray-50 dark:bg-slate-700/40 p-3 rounded-xl border border-gray-100 dark:border-slate-700 text-center">
          <div class="text-base font-black text-slate-800 dark:text-white">1,240</div>
          <div class="text-[10px] text-slate-400 dark:text-slate-500 font-bold uppercase tracking-wider mt-0.5">Članova</div>
        </div>
        <div class="bg-gray-50 dark:bg-slate-700/40 p-3 rounded-xl border border-gray-100 dark:border-slate-700 text-center">
          <div class="text-base font-black text-slate-800 dark:text-white">4,821</div>
          <div class="text-[10px] text-slate-400 dark:text-slate-500 font-bold uppercase tracking-wider mt-0.5">Teme</div>
        </div>
      </div>
    </div>

    <div class="bg-white dark:bg-slate-800 rounded-2xl border border-gray-100 dark:border-slate-700 p-4 shadow-sm">
      <div class="flex items-center gap-2 mb-3 pb-2 border-b border-gray-100 dark:border-slate-700">
        <span class="text-base text-emerald-500">🟢</span>
        <h3 class="text-xs font-black uppercase tracking-wider text-slate-800 dark:text-slate-200">
          Aktivne kolege
        </h3>
      </div>
      <div class="flex flex-wrap gap-2.5 pt-1">
        <div v-for="user in ['amar', 'tarik', 'amina', 'elma', 'kenan']" :key="user" class="relative group cursor-pointer">
          <div class="w-9 h-9 rounded-full bg-gradient-to-tr from-orange-400 to-amber-500 text-white font-black text-xs flex items-center justify-center uppercase border-2 border-white dark:border-slate-800 shadow-sm">
            {{ user.substring(0, 2) }}
          </div>
          <span class="absolute bottom-0 right-0 block h-2.5 w-2.5 rounded-full bg-emerald-500 ring-2 ring-white dark:ring-slate-800"></span>
          <span class="absolute bottom-full left-1/2 -translate-x-1/2 mb-1.5 hidden group-hover:block bg-slate-900 text-white text-[11px] font-bold px-2 py-0.5 rounded shadow-md whitespace-nowrap z-30">
            {{ user }}
          </span>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import { getPopularTopics, getCategoryPopularTopics } from '../../services/forum.js';

const route = useRoute();


const popularTopics = ref([]);
const isLoading = ref(true);


const categoryTopics = ref([]);
const isCategoryLoading = ref(false);


const isCategoryPage = computed(() => !!(route.params.id || route.query.category_id));
const currentCategoryId = computed(() => route.params.id || route.query.category_id);

const skratiNaslov = (naslov) => {
  if (!naslov) return '';
  return naslov.length > 50 ? naslov.substring(0, 47) + '...' : naslov;
};


const ucitajKontekstualneTeme = async (categoryId) => {
  if (!categoryId) return;
  isCategoryLoading.value = true;
  try {
    const data = await getCategoryPopularTopics(categoryId);
    categoryTopics.value = Array.isArray(data) ? data : [];
  } catch (error) {
    console.error("Greška pri učitavanju tema kategorije:", error);
    categoryTopics.value = [];
  } finally {
    isCategoryLoading.value = false;
  }
};


watch(currentCategoryId, (newId) => {
  if (newId) {
    ucitajKontekstualneTeme(newId);
  } else {
    categoryTopics.value = [];
  }
});

onMounted(async () => {
  
  try {
    const data = await getPopularTopics();
    popularTopics.value = Array.isArray(data) ? data : [];
  } catch (error) {
    console.error("Greška pri učitavanju popularnih tema:", error);
    popularTopics.value = [];
  } finally {
    isLoading.value = false;
  }

  
  if (isCategoryPage.value) {
    ucitajKontekstualneTeme(currentCategoryId.value);
  }
});
</script>