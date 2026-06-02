<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { getSearchSuggestions } from '../services/forum.js';

const emit = defineEmits(['search-submitted']);
const router = useRouter();

const search = ref("");
const isOpen = ref(false);
const isLoading = ref(false);

const popularTopics = ref([]);
const activeTopics = ref([]);
const filteredTopics = ref([]);

const rootRef = ref(null);
let debounceTimeout = null;
let trenutniKontroler = null;

// 1. Povlačenje top tema sa backenda
const ucitajPocetneSugestije = async () => {
  isLoading.value = true;
  try {
    const data = await getSearchSuggestions(""); 
    popularTopics.value = data.popular || [];
    activeTopics.value = data.active || [];
  } catch (error) {
    console.error("Greška pri učitavanju popularnih tema:", error);
  } finally {
    isLoading.value = false;
  }
};

// 2. Real-time pretraga (kucanje)
const ucitajFiltriraneSugestije = async (query) => {
  if (trenutniKontroler) {
    trenutniKontroler.abort();
  }

  trenutniKontroler = new AbortController();
  isLoading.value = true;

  try {
    const data = await getSearchSuggestions(query, { signal: trenutniKontroler.signal });
    filteredTopics.value = data.filtered || [];
  } catch (error) {
    if (error.name !== 'AbortError') {
      console.error("Greška pri real-time pretrazi:", error);
    }
  } finally {
    isLoading.value = false;
  }
};

// Prati kucanje korisnika
watch(search, (newVal) => {
  clearTimeout(debounceTimeout);
  
  if (!newVal.trim()) {
    filteredTopics.value = [];
    if (trenutniKontroler) trenutniKontroler.abort();
    return;
  }

  debounceTimeout = setTimeout(() => {
    ucitajFiltriraneSugestije(newVal.trim());
  }, 250); 
});

const onFocus = () => {
  isOpen.value = true;
  // Uvijek povuci svježe top teme kada korisnik klikne na prazan bar
  if (!search.value.trim()) {
    ucitajPocetneSugestije();
  }
};

const idiNaTemu = (id) => {
  isOpen.value = false;
  search.value = ""; 
  router.push(`/forum/topics/${id}`); 
};

const triggerSearch = () => {
  isOpen.value = false;
  emit('search-submitted', search.value);
};

const handleClickOutside = (event) => {
  if (rootRef.value && !rootRef.value.contains(event.target)) {
    isOpen.value = false;
  }
};

onMounted(() => document.addEventListener('click', handleClickOutside));
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
  clearTimeout(debounceTimeout);
  if (trenutniKontroler) trenutniKontroler.abort();
});
</script>

<template>
  <div ref="rootRef" class="relative w-full max-w-xl mx-auto z-50">
    <div class="flex gap-2 w-full">
      <div class="relative flex-1">
        <input 
          v-model="search" 
          type="text" 
          placeholder="Pretraži forum (kucaj za sugestije)..." 
          @focus="onFocus"
          @keyup.enter="triggerSearch"
          class="w-full border border-gray-200 dark:border-slate-700 rounded-lg pl-4 pr-10 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 shadow-sm" 
        />
        <div v-if="isLoading" class="absolute right-3 top-2.5">
          <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-orange-500"></div>
        </div>
      </div>
      <button @click="triggerSearch" class="bg-slate-800 dark:bg-slate-700 text-white text-xs px-5 rounded-lg font-bold hover:bg-slate-700 dark:hover:bg-slate-600 shadow-sm transition-colors">
        Traži
      </button>
    </div>

    <div v-if="isOpen" class="absolute left-0 right-0 mt-2 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-xl shadow-xl overflow-hidden max-h-[380px] overflow-y-auto z-50">
      
      <div v-if="!search.trim()">
        <div class="p-3 border-b border-gray-100 dark:border-slate-700/50">
          <div class="text-xs font-bold uppercase tracking-wider text-orange-500 mb-2 flex items-center gap-1">
            🔥 Najgledanije teme
          </div>
          <div class="space-y-1">
            <button 
              v-for="tema in popularTopics" 
              :key="'pop-'+tema.id" 
              @click="idiNaTemu(tema.id)"
              class="w-full text-left block p-2 text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700/50 rounded-lg transition-colors truncate"
            >
              {{ tema.title }}
            </button>
            <p v-if="popularTopics.length === 0 && !isLoading" class="text-xs text-slate-400 italic p-2">Nema tema u bazi.</p>
          </div>
        </div>

        <div class="p-3">
          <div class="text-xs font-bold uppercase tracking-wider text-blue-500 mb-2 flex items-center gap-1">
            💬 Najnovije rasprave
          </div>
          <div class="space-y-1">
            <button 
              v-for="tema in activeTopics" 
              :key="'act-'+tema.id" 
              @click="idiNaTemu(tema.id)"
              class="w-full text-left block p-2 text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700/50 rounded-lg transition-colors truncate"
            >
              {{ tema.title }}
            </button>
            <p v-if="activeTopics.length === 0 && !isLoading" class="text-xs text-slate-400 italic p-2">Nema aktivnih tema.</p>
          </div>
        </div>
      </div>

      <div v-else class="p-3">
        <div class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
          🔍 Predložene teme na osnovu vašeg unosa
        </div>
        <div class="space-y-1">
          <button 
            v-for="tema in filteredTopics" 
            :key="'filt-'+tema.id" 
            @click="idiNaTemu(tema.id)"
            class="w-full text-left block p-2 text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700/50 rounded-lg transition-colors truncate"
          >
            {{ tema.title }}
          </button>
          <p v-if="filteredTopics.length === 0 && !isLoading" class="text-xs text-slate-400 italic p-2">
            Nema pronađenih tema za "{{ search }}"
          </p>
        </div>
      </div>

    </div>
  </div>
</template>