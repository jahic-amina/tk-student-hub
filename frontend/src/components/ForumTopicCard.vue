<script setup>
defineProps({
  tema: { type: Object, required: true },
  isAdmin: { type: Boolean, default: false }
});

const emit = defineEmits(['obrisi']);

function formatDate(dateValue) {
  if (!dateValue) return "";
  return new Intl.DateTimeFormat("bs-BA", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric"
  }).format(new Date(dateValue));
}

function getInitials(name) {
  if (!name) return "?";
  return name.split(" ").map((part) => part[0]).join("").slice(0, 2).toUpperCase();
}
</script>

<template>
  <router-link 
    :to="`/forum/tema/${tema.id}`"
    class="block p-5 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700/60 shadow-sm hover:shadow-md dark:hover:border-slate-600 transition-all cursor-pointer group"
  >
    <div class="flex justify-between items-start">
      <h2 class="text-lg font-bold text-slate-800 dark:text-slate-100 group-hover:text-[#ff7a00] dark:group-hover:text-orange-400 transition-colors line-clamp-1">
        {{ tema.title }}
      </h2>
      
      <div class="flex items-center gap-2 flex-shrink-0 ml-4">
        <span class="bg-orange-50 dark:bg-orange-950/30 text-[#ff7a00] dark:text-orange-400 text-[9px] font-extrabold uppercase px-2 py-0.5 rounded tracking-wider">
          {{ tema.category?.name || 'Opšta diskusija' }}
        </span>

        <button
          v-if="isAdmin"
          @click.prevent="emit('obrisi', tema.id)"
          class="w-7 h-7 flex items-center justify-center rounded-full text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/30 hover:text-red-800 dark:hover:text-red-300 transition-colors text-xs"
          title="Obriši temu"
        >
          🗑️
        </button>
      </div>
    </div>
    
    <p class="text-slate-500 dark:text-slate-400 mt-2 text-xs leading-relaxed line-clamp-2">
      {{ tema.content }}
    </p>
    
    <div class="flex items-center justify-between mt-5 pt-3 border-t border-gray-100 dark:border-slate-700 text-[11px] text-slate-400 dark:text-slate-500">
      <div class="flex items-center gap-1.5">
        <span class="w-5 h-5 rounded-full bg-slate-100 dark:bg-slate-700 text-slate-500 dark:text-slate-400 flex items-center justify-center font-bold text-[9px]">
          {{ getInitials(tema.author?.full_name) }}
        </span>
        <span class="text-slate-600 dark:text-slate-300 font-medium">{{ tema.author?.full_name || 'Korisnik' }}</span>
        <span>•</span>
        <span>{{ formatDate(tema.created_at) }}</span>
      </div>

      <div class="flex items-center space-x-3 font-semibold">
        <span>👁️ {{ tema.views_count || 0 }} pregleda</span>
        <span class="text-[#ff7a00] dark:text-orange-400">💬 {{ tema.comments_count || 0 }} odgovora</span>
      </div>
    </div>
  </router-link>
</template>