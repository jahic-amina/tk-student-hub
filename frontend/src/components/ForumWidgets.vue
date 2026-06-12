<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { getPopularTopics, getTopics, getCategories } from '../services/forum.js';

const props = defineProps({
  selectedCategoryId: {
    type: [Number, String, null],
    default: null
  },
  currentTopicId: {
    type: [Number, String, null],
    default: null
  },
  currentTopicTitle: {
    type: String,
    default: ""
  }
});

const popularTopics = ref([]);       
const categoryTopics = ref([]);      
const sveKategorije = ref([]); 

const isLoading = ref(true);

const isTopicMode = computed(() => props.currentTopicId !== null && props.currentTopicId !== undefined);
const isCategoryMode = computed(() => !isTopicMode.value && props.selectedCategoryId !== null && props.selectedCategoryId !== undefined);

const naslovWidgeta = computed(() => {
  if (isTopicMode.value) return 'Slične teme';
  if (isCategoryMode.value) {
    const kat = sveKategorije.value.find(c => c.id === Number(props.selectedCategoryId));
    return kat ? `${kat.name} - Najpopularnije` : 'Kategorija - Najpopularnije';
  }
  return 'Najpopularnije';
});

const slicneTemeAlgoritam = computed(() => {
  if (!props.currentTopicTitle || categoryTopics.value.length === 0) return [];

  const kljucneRijeci = props.currentTopicTitle
    .toLowerCase()
    .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()?]/g, "") 
    .split(/\s+/)
    .filter(rijec => rijec.length > 2); 

  return categoryTopics.value
    .filter(tema => Number(tema.id) !== Number(props.currentTopicId)) 
    .map(tema => {
      const naslovDrugeTeme = tema.title.toLowerCase();
      let brojPoklapanja = 0;
      
      kljucneRijeci.forEach(rijec => {
        if (naslovDrugeTeme.includes(rijec)) {
          brojPoklapanja++;
        }
      });

      return { ...tema, score: brojPoklapanja };
    })
    .sort((a, b) => b.score - a.score || (b.comments_count || 0) - (a.comments_count || 0))
    .slice(0, 4); 
});

// POPRAVLJENO: Ograničavanje prikaza na top 5 najpopularnijih tema u modu kategorije
const trenutneTeme = computed(() => {
  if (isTopicMode.value) return slicneTemeAlgoritam.value;
  if (isCategoryMode.value) {
    return [...categoryTopics.value]
      .sort((a, b) => (b.comments_count + b.views_count) - (a.comments_count + a.views_count))
      .slice(0, 5); 
  }
  return popularTopics.value.slice(0, 5);
});

const trebaPrikazatiWidget = computed(() => {
  if (isTopicMode.value) return slicneTemeAlgoritam.value.length > 0; 
  if (isCategoryMode.value) return categoryTopics.value.length >= 3;  
  return true; 
});

const skratiNaslov = (naslov) => {
  if (!naslov) return '';
  return naslov.length > 50 ? naslov.substring(0, 47) + '...' : naslov;
};

const ucitajGlobalno = async () => {
  isLoading.value = true;
  try {
    const data = await getPopularTopics();
    popularTopics.value = Array.isArray(data) ? data : [];
  } catch (e) {} finally { isLoading.value = false; }
};

const ucitajTemeKategorije = async (catId) => {
  isLoading.value = true;
  try {
    const data = await getTopics({ category_id: catId, per_page: 20, sort_by: 'najnovije' });
    categoryTopics.value = data && data.items ? data.items : (Array.isArray(data) ? data : []);
  } catch (e) {
    categoryTopics.value = [];
  } finally { isLoading.value = false; }
};

watch(() => props.selectedCategoryId, (newCatId) => {
  if (!isTopicMode.value) {
    if (newCatId) ucitajTemeKategorije(newCatId);
    else ucitajGlobalno();
  }
});

onMounted(async () => {
  try { sveKategorije.value = await getCategories(); } catch (e) {}
  
  if (isTopicMode.value && props.selectedCategoryId) {
    await ucitajTemeKategorije(props.selectedCategoryId);
  } else if (isCategoryMode.value) {
    await ucitajTemeKategorije(props.selectedCategoryId);
  } else {
    await ucitajGlobalno();
  }
});
</script>

<template>
  <div v-if="trebaPrikazatiWidget" class="w-full flex flex-col gap-5 select-none animate-in fade-in duration-300">
    <div class="bg-white dark:bg-slate-800 rounded-2xl border border-gray-100 dark:border-slate-700 p-4 shadow-sm transition-all hover:shadow-md">
      
      <div class="flex items-center gap-2 mb-4 pb-2 border-b border-gray-100 dark:border-slate-700">
        <span class="text-base">
          {{ isTopicMode ? '📚' : isCategoryMode ? '⭐' : '🔥' }}
        </span>
        <h3 class="text-xs font-black uppercase tracking-wider text-slate-800 dark:text-slate-200">
          {{ naslovWidgeta }}
        </h3>
      </div>

      <div v-if="isLoading" class="flex flex-col items-center justify-center py-6 gap-2">
        <div class="animate-spin rounded-full h-5 w-5 border-b-2" :class="isTopicMode ? 'border-blue-500' : isCategoryMode ? 'border-amber-500' : 'border-orange-500'"></div>
      </div>

      <div v-else-if="trenutneTeme.length === 0" class="text-center py-6 text-xs text-slate-400 dark:text-slate-500 font-medium">
        {{ isTopicMode ? 'Nema sličnih tema.' : 'Nema aktivnih tema.' }}
      </div>

      <div v-else class="space-y-4">
        <router-link 
          v-for="tema in trenutneTeme" 
          :key="tema.id" 
          :to="`/forum/tema/${tema.id}`" 
          class="block group cursor-pointer"
        >
          <div class="text-sm font-bold text-slate-800 dark:text-slate-100 group-hover:text-amber-500 dark:group-hover:text-orange-500 transition-colors line-clamp-2 leading-snug">
            {{ skratiNaslov(tema.title) }}
          </div>
          
          <div class="flex flex-wrap items-center gap-3 mt-2 text-[11px] text-slate-400 dark:text-slate-500 font-semibold">
            <span class="flex items-center gap-1">👁️ {{ tema.views_count || 0 }}</span>
            <span class="flex items-center gap-1">💬 {{ tema.comments_count || 0 }}</span>
            
            <span v-if="isTopicMode && tema.author" class="text-[10px] text-slate-400 dark:text-slate-500 font-medium ml-auto">
              ✍️ {{ tema.author.full_name || 'Kolega' }}
            </span>

            <span 
              v-if="!isCategoryMode && !isTopicMode && tema.category"
              class="px-2 py-0.5 rounded text-[10px] font-bold ml-auto"
              :style="{ backgroundColor: (tema.category.color || '#ff7a00') + '15', color: tema.category.color || '#ff7a00' }"
            >
              {{ tema.category.name }}
            </span>
          </div>
        </router-link>
      </div>

    </div>

    <div class="bg-white dark:bg-slate-800 rounded-2xl border border-gray-100 dark:border-slate-700 p-4 shadow-sm">
      <div class="flex items-center gap-2 mb-4 pb-2 border-b border-gray-100 dark:border-slate-700">
        <span class="text-base text-blue-500">📊</span>
        <h3 class="text-xs font-black uppercase tracking-wider text-slate-800 dark:text-slate-200">Statistika</h3>
      </div>
      <div class="grid grid-cols-2 gap-3">
        <div class="bg-gray-50 dark:bg-slate-700/40 p-3 rounded-xl text-center">
          <div class="text-base font-black text-slate-800 dark:text-white">1,240</div>
          <div class="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Članova</div>
        </div>
        <div class="bg-gray-50 dark:bg-slate-700/40 p-3 rounded-xl text-center">
          <div class="text-base font-black text-slate-800 dark:text-white">4,821</div>
          <div class="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Teme</div>
        </div>
      </div>
    </div>
  </div>
</template>