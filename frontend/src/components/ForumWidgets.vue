<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { 
  getPopularTopics, 
  getCategoryPopularTopics, 
  getRelatedTopics, 
  getCategories 
} from '../services/forum.js';

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

const widgetTopics = ref([]);       
const sveKategorije = ref([]); 
const isLoading = ref(true);

const isTopicMode = computed(() => props.currentTopicId !== null && props.currentTopicId !== undefined);
const isCategoryMode = computed(() => !isTopicMode.value && props.selectedCategoryId !== null && props.selectedCategoryId !== undefined);

const naslovWidgeta = computed(() => {
  if (isTopicMode.value) return 'Slične teme';
  if (isCategoryMode.value) {
    const kat = sveKategorije.value.find(c => c.id === Number(props.selectedCategoryId));
    return kat ? `${kat.name} - Popularno` : 'Kategorija - Popularno';
  }
  return 'Najpopularnije ove sedmice';
});

const trebaPrikazatiWidget = computed(() => {
  if (isLoading.value) return true;
  if (isTopicMode.value) return widgetTopics.value.length > 0;
  if (isCategoryMode.value) return widgetTopics.value.length >= 1; 
  return widgetTopics.value.length > 0;
});

const skratiNaslov = (naslov) => {
  if (!naslov) return '';
  return naslov.length > 50 ? naslov.substring(0, 47) + '...' : naslov;
};

const osveziPodatkeWidgeta = async () => {
  isLoading.value = true;
  try {
    if (isTopicMode.value) {
      widgetTopics.value = await getRelatedTopics(props.currentTopicId);
    } else if (isCategoryMode.value) {
      widgetTopics.value = await getCategoryPopularTopics(props.selectedCategoryId);
    } else {
      widgetTopics.value = await getPopularTopics();
    }
  } catch (e) {
    widgetTopics.value = [];
  } finally {
    isLoading.value = false;
  }
};

watch(() => [props.selectedCategoryId, props.currentTopicId], () => {
  osveziPodatkeWidgeta();
}, { immediate: false });

onMounted(async () => {
  try { 
    sveKategorije.value = await getCategories(); 
  } catch (e) {}
  await osveziPodatkeWidgeta();
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

      <div v-if="isLoading" class="flex items-center justify-center py-6">
        <div class="animate-spin rounded-full h-5 w-5 border-b-2" :class="isTopicMode ? 'border-blue-500' : isCategoryMode ? 'border-amber-500' : 'border-orange-500'"></div>
      </div>

      <div v-else-if="widgetTopics.length === 0" class="text-center py-6 text-xs text-slate-400 dark:text-slate-500 font-medium">
        {{ isTopicMode ? 'Nema sličnih tema.' : 'Nema aktivnih tema u ovoj kategoriji.' }}
      </div>

      <div v-else class="space-y-4">
        <router-link 
          v-for="tema in widgetTopics" 
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
  </div>
</template>