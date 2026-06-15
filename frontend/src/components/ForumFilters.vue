<script setup>
import { ref, reactive, watch, onMounted, onUnmounted } from 'vue';

const emit = defineEmits(['filters-changed']);

const isPopoverOpen = ref(false);
const containerRef = ref(null);

// Početno stanje filtera izdvojeno radi lakšeg resetovanja
const getPocetniFilteri = () => ({
  sort_by: 'najnovije',
  unanswered: false,
  days_old: null
});

const filteri = reactive(getPocetniFilteri());

// Funkcija za kompletno poništavanje stanja na inicijalno kroz "Poništi sve"
const resetujFiltere = () => {
  Object.assign(filteri, getPocetniFilteri());
};

// Funkcija koja omogućava odznačavanje radio button-a na ponovni klik
const toggleSortBy = (vrijednost) => {
  if (filteri.sort_by === vrijednost) {
    // Ako kliknemo na već aktivno, vraćamo na podrazumijevano ('najnovije')
    filteri.sort_by = 'najnovije';
  } else {
    filteri.sort_by = vrijednost;
  }
};

watch(filteri, () => {
  emit('filters-changed', { ...filteri });
}, { deep: true });

const handleClickOutside = (event) => {
  if (containerRef.value && !containerRef.value.contains(event.target)) {
    isPopoverOpen.value = false;
  }
};

onMounted(() => document.addEventListener('click', handleClickOutside));
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<template>
  <div ref="containerRef" class="relative inline-block text-left">
    <button
      @click="isPopoverOpen = !isPopoverOpen"
      type="button"
      class="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-semibold rounded-lg border transition-colors focus:outline-none shadow-sm h-[38px]"
      :class="isPopoverOpen 
        ? 'bg-orange-50 dark:bg-slate-700/50 border-orange-400 text-orange-600 dark:text-orange-400 ring-2 ring-orange-400/20' 
        : 'bg-white dark:bg-slate-800 border-gray-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-gray-100 dark:hover:bg-slate-700/80'"
    >
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
      </svg>
      <span>Filteri</span>
      <span v-if="filteri.unanswered || filteri.days_old || filteri.sort_by !== 'najnovije'" class="w-2 h-2 rounded-full bg-orange-500"></span>
    </button>

    <div v-if="isPopoverOpen" class="absolute right-0 mt-2 w-72 divide-y divide-gray-100 dark:divide-slate-700/50 rounded-xl bg-white dark:bg-slate-800 shadow-2xl border border-gray-100 dark:border-slate-700 z-50">
      
      <div class="p-4 flex items-center justify-between bg-gray-50/50 dark:bg-slate-900/10 rounded-t-xl">
        <span class="block text-xs font-bold uppercase tracking-wider text-slate-400">Opcije filtriranja</span>
        <button 
          v-if="filteri.unanswered || filteri.days_old || filteri.sort_by !== 'najnovije'"
          @click="resetujFiltere"
          type="button"
          class="text-xs font-bold text-orange-500 hover:text-orange-600 dark:hover:text-orange-400 transition-colors"
        >
          Poništi sve
        </button>
      </div>

      <!-- SORTIRANJE (Radio dugmad sa podrškom za odznačavanje) -->
      <div class="p-4">
        <span class="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Sortiraj po</span>
        <div class="space-y-2">
          <label 
            @click.prevent="toggleSortBy('najnovije')" 
            class="flex items-center gap-2.5 text-sm font-medium text-slate-700 dark:text-slate-300 cursor-pointer select-none"
          >
            <input type="radio" :checked="filteri.sort_by === 'najnovije'" class="accent-orange-500" />
            <span>Najnovije</span>
          </label>
          <label 
            @click.prevent="toggleSortBy('najgledanije')" 
            class="flex items-center gap-2.5 text-sm font-medium text-slate-700 dark:text-slate-300 cursor-pointer select-none"
          >
            <input type="radio" :checked="filteri.sort_by === 'najgledanije'" class="accent-orange-500" />
            <span>Najgledanije</span>
          </label>
          <label 
            @click.prevent="toggleSortBy('najaktivnije')" 
            class="flex items-center gap-2.5 text-sm font-medium text-slate-700 dark:text-slate-300 cursor-pointer select-none"
          >
            <input type="radio" :checked="filteri.sort_by === 'najaktivnije'" class="accent-orange-500" />
            <span>Najaktivnije</span>
          </label>
        </div>
      </div>

      <!-- STANJE (Checkbox - on sam po sebi radi toggle na klik) -->
      <div class="p-4">
        <span class="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Stanje</span>
        <label class="flex items-center gap-2.5 text-sm font-medium text-slate-700 dark:text-slate-300 cursor-pointer select-none">
          <input type="checkbox" v-model="filteri.unanswered" class="accent-orange-500" />
          <span>Bez odgovora (0 replies)</span>
        </label>
      </div>

      <!-- MAKSIMALNA STAROST (Dodato malo "x" dugme za brzi reset unosa) -->
      <div class="p-4 bg-gray-50/50 dark:bg-slate-900/30 rounded-b-xl">
        <span class="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Maksimalna starost</span>
        <div class="relative flex items-center">
          <input 
            type="number" 
            placeholder="Sve teme" 
            min="1" 
            v-model.number="filteri.days_old" 
            class="w-full border border-gray-200 dark:border-slate-700 rounded-lg pl-3 pr-16 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400 bg-white dark:bg-slate-800" 
          />
          <!-- Malo dugme "x" koje se pojavljuje samo kada je unesen broj, za brisanje filtera na klik -->
          <button 
            v-if="filteri.days_old !== null" 
            @click="filteri.days_old = null"
            type="button"
            class="absolute right-10 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xs font-bold p-1 transition"
          >
            ✕
          </button>
          <span class="absolute right-3 text-xs font-medium text-gray-400 pointer-events-none">dana</span>
        </div>
      </div>

    </div>
  </div>
</template>