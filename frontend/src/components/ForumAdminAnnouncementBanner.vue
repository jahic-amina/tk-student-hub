<script setup>
import { ref, onMounted } from 'vue';
import { getActiveAnnouncements } from '../services/forum'; 

const activeAnnouncements = ref([]);
const isLoading = ref(true);

onMounted(async () => {
  try {
    activeAnnouncements.value = await getActiveAnnouncements();
  } catch (error) {
    console.error("Greška pri učitavanju globalnih obavještenja:", error);
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
  <div v-if="activeAnnouncements.length > 0" class="w-full space-y-3 mb-6">
    <div 
      v-for="ann in activeAnnouncements" 
      :key="ann.id"
      class="bg-orange-50/90 dark:bg-slate-800/95 border border-orange-200 dark:border-orange-900/40 rounded-2xl p-5 shadow-sm flex items-start gap-4 transition-all duration-300 backdrop-blur-sm"
    >
      <div class="p-2.5 bg-orange-100 dark:bg-orange-950/40 text-orange-600 dark:text-orange-400 rounded-xl flex items-center justify-center text-xl shadow-inner select-none">
        📢
      </div>
      
      <div class="flex-1">
        <h3 class="text-base font-bold text-slate-800 dark:text-slate-100 tracking-tight leading-snug">
          {{ ann.title || 'Zvanično obavještenje administratora' }}
        </h3>
        <p class="text-sm text-slate-600 dark:text-slate-300 mt-1.5 leading-relaxed font-medium whitespace-pre-line">
          {{ ann.content }}
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/*Vizuelni efekat pulsiranja za nova obavjestenja*/
.animate-pulse-once {
  animation: pulseOnce 1.5s ease-in-out 1;
}
@keyframes pulseOnce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.01); }
}
</style>