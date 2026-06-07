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
  <div v-if="activeAnnouncements.length > 0" class="w-full space-y-2 mb-6">
    <div 
      v-for="ann in activeAnnouncements" 
      :key="ann.id"
      class="bg-gradient-to-r from-orange-500 to-amber-500 text-white p-4 rounded-2xl shadow-md border-l-8 border-amber-700 flex items-start gap-3 animate-pulse-once transition-all duration-200"
    >
      <span class="text-xl select-none">📢</span>
      <div class="flex-1">
        <h4 class="text-xs font-black uppercase tracking-widest text-orange-100">Zvanično obavještenje administratora</h4>
        <p class="text-sm font-bold mt-0.5 leading-relaxed">
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