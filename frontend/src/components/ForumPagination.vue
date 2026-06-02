<script setup>
defineProps({
  trenutnaStranica: { type: Number, required: true },
  ukupnoStranica: { type: Number, required: true },
  prikazanoTema: { type: Number, required: true },
  ukupnoTema: { type: Number, required: true }
});

const emit = defineEmits(['promijeniStranicu']);
</script>

<template>
  <div class="mt-8 flex items-center justify-between border-t border-gray-200 dark:border-slate-800 pt-4 pb-4">
    <p class="text-xs text-slate-500 dark:text-slate-400">
      Prikazano <span class="font-medium text-slate-700 dark:text-slate-200">{{ prikazanoTema }}</span> tema od ukupno <span class="font-medium text-slate-700 dark:text-slate-200">{{ ukupnoTema }}</span>
    </p>
    
    <div class="flex items-center space-x-2">
      <button 
        @click="emit('promijeniStranicu', trenutnaStranica - 1)" 
        :disabled="trenutnaStranica === 1"
        class="px-3 py-1.5 bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-700 rounded-lg text-xs font-medium text-slate-700 dark:text-slate-200 hover:bg-gray-50 dark:hover:bg-slate-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
      >
        ← Prethodna
      </button>

      <span class="text-xs font-semibold text-slate-700 dark:text-slate-300 px-2">
        Stranica {{ trenutnaStranica }} od {{ ukupnoStranica }}
      </span>

      <button 
        @click="emit('promijeniStranicu', trenutnaStranica + 1)" 
        :disabled="trenutnaStranica === ukupnoStranica"
        class="px-3 py-1.5 bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-700 rounded-lg text-xs font-medium text-slate-700 dark:text-slate-200 hover:bg-gray-50 dark:hover:bg-slate-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
      >
        Sljedeća →
      </button>
    </div>
  </div>
</template>