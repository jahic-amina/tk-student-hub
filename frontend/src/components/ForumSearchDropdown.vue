<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue';
import { getSearchSuggestions } from '../services/forum.js';

const emit = defineEmits(['search-submitted']);

const search = ref("");
const isOpen = ref(false);
const isLoading = ref(false);
const suggestions = ref({ popular: [], active: [], filtered: [] });
const rootRef = ref(null);
let debounceTimeout = null;

// Funkcija koja povlači podatke sa API-ja
const fetchSuggestions = async () => {
  isLoading.value = true;
  try {
    const data = await getSearchSuggestions(search.value);
    // Pretpostavka strukture: { popular: [], active: [], filtered: [] }
    suggestions.value = {
      popular: data.popular || [],
      active: data.active || [],
      filtered: data.filtered || []
    };
  } catch (error) {
    console.error("Greška sa sugestijama:", error);
    // Fallback/Demo podaci za lakše debugovanje
    if (!search.value) {
      suggestions.value.popular = [{ id: 1, title: "Popularna tema 1 (Demo)" }, { id: 2, title: "Popularna tema 2 (Demo)" }];
      suggestions.value.active = [{ id: 3, title: "Aktivna diskusija 1 (Demo)" }];
    } else {
      suggestions.value.filtered = [{ id: 1, title: `Rezultat za: ${search.value}` }];
    }
  } finally {
    isLoading.value = false;
  }
};

// Debounce logika za kucanje (štiti backend)
watch(search, (newVal) => {
  clearTimeout(debounceTimeout);
  
  // Ako je prazno, odmah povuci inicijalne popularne/aktivne teme
  if (!newVal.trim()) {
    fetchSuggestions();
    return;
  }

  // Inače čekaj 300ms pauze u kucanju prije slanja zahtjeva
  debounceTimeout = setTimeout(() => {
    fetchSuggestions();
  }, 300);
});

// Otvaranje dropdown-a na fokus
const onFocus = () => {
  isOpen.value = true;
  fetchSuggestions(); // Povuci čim klikne
};

// Zatvaranje na Enter ili klik na dugme "Traži"
const triggerSearch = () => {
  isOpen.value = false;
  emit('search-submitted', search.value);
};

// Zatvaranje klikom bilo gdje van komponente
const handleClickOutside = (event) => {
  if (rootRef.value && !rootRef.value.contains(event.target)) {
    isOpen.value = false;
  }
};

onMounted(() => document.addEventListener('click', handleClickOutside));
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
  clearTimeout(debounceTimeout);
});
</script>

<template>
  <div ref="rootRef" class="relative w-full max-w-xl mx-auto z-50">
    <div class="flex gap-2 w-full">
      <div class="relative flex-1">
        <input 
          v-model="search" 
          type="text" 
          placeholder="Pretraži teme (npr. ispit, literatura)..." 
          @focus="onFocus"
          @keyup.enter="triggerSearch"
          class="w-full border border-gray-200 dark:border-slate-700 rounded-lg pl-4 pr-10 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 shadow-sm" 
        />
        <div v-if="isLoading" class="absolute right-3 top-2.5 animate-spin rounded-full h-4 w-4 border-b-2 border-orange-500"></div>
      </div>
      <button @click="triggerSearch" class="bg-slate-800 dark:bg-slate-700 text-white text-xs px-5 rounded-lg font-bold hover:bg-slate-700 dark:hover:bg-slate-600 shadow-sm transition-colors">
        Traži
      </button>
    </div>

    <div v-if="isOpen" class="absolute left-0 right-0 mt-2 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-xl shadow-xl overflow-hidden max-h-[400px] overflow-y-auto z-50">
      
      <div v-if="!search.trim()">
        <div class="p-3 border-b border-gray-100 dark:border-slate-700/50">
          <div class="text-xs font-bold uppercase tracking-wider text-orange-500 mb-2 flex items-center gap-1">
            🔥 Najgledanije teme
          </div>
          <div class="space-y-1">
            <router-link 
              v-for="tema in suggestions.popular" 
              :key="'pop-'+tema.id" 
              :to="`/forum/tema/${tema.id}`"
              @click="isOpen = false"
              class="block p-2 text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/50 rounded-lg transition-colors truncate"
            >
              {{ tema.title }}
            </router-link>
            <p v-if="suggestions.popular.length === 0" class="text-xs text-slate-400 italic p-2">Nema podataka.</p>
          </div>
        </div>

        <div class="p-3">
          <div class="text-xs font-bold uppercase tracking-wider text-blue-500 mb-2 flex items-center gap-1">
            💬 Najaktivnije rasprave
          </div>
          <div class="space-y-1">
            <router-link 
              v-for="tema in suggestions.active" 
              :key="'act-'+tema.id" 
              :to="`/forum/tema/${tema.id}`"
              @click="isOpen = false"
              class="block p-2 text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/50 rounded-lg transition-colors truncate"
            >
              {{ tema.title }}
            </router-link>
            <p v-if="suggestions.active.length === 0" class="text-xs text-slate-400 italic p-2">Nema podataka.</p>
          </div>
        </div>
      </div>

      <div v-else class="p-3">
        <div class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
          🔍 Rezultati pretrage sugerisani za vas
        </div>
        <div class="space-y-1">
          <router-link 
            v-for="tema in suggestions.filtered" 
            :key="'filt-'+tema.id" 
            :to="`/forum/tema/${tema.id}`"
            @click="isOpen = false"
            class="block p-2 text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/50 rounded-lg transition-colors truncate"
          >
            {{ tema.title }}
          </router-link>
          <p v-if="suggestions.filtered.length === 0 && !isLoading" class="text-xs text-slate-400 italic p-2">
            Nema direktnih poklapanja za "{{ search }}"... Pritisnite Enter za punu pretragu.
          </p>
        </div>
      </div>

    </div>
  </div>
</template>