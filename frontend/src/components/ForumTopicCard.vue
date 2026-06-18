<script setup>
import { ref, computed } from 'vue';

// 1. Uvozimo tvoju novu ForumAvatar komponentu (prilagodi putanju ako je potrebno)
import ForumAvatar from './ForumAvatar.vue'; 

const props = defineProps({
  tema: { type: Object, required: true },
  isAdmin: { type: Boolean, default: false }
});

const emit = defineEmits(['obrisi']);


const showAllMedalsDropdown = ref(false);



// MAPIRANJE MEDALJA (isti pattern kao TopicMainCard / ForumComments)
const medalIcons = { gold: '🥇', silver: '🥈', bronze: '🥉' };

const medalThresholds = {
  best_answers: { bronze: 1, silver: 5, gold: 15 },
  topics_started: { bronze: 3, silver: 10, gold: 25 },
  reputation: { bronze: 100, silver: 500, gold: 1000 },
  night_owl: { bronze: 1, silver: 3, gold: 10 }
};

const medalDetails = {
  best_answers: {
    name: 'Najbolji odgovori',
    desc: (n) => `Dobija se kada vaš odgovor bude označen kao najbolji ${n} ${n === 1 ? 'put' : 'puta'}.`
  },
  topics_started: {
    name: 'Pokrenute teme',
    desc: (n) => `Dobija se kada pokrenete ${n} ${n === 1 ? 'temu' : 'tema'} na forumu.`
  },
  reputation: {
    name: 'Ukupna reputacija',
    desc: (n) => `Dobija se kada skupite ukupno ${n} XP reputacije.`
  },
  night_owl: {
    name: 'Noćna ptica',
    desc: (n) => `Tajna medalja — dobija se kada pokrenete ${n} ${n === 1 ? 'temu' : 'tema'} između 03:00 i 05:00h.`
  }
};

function parseMedal(medal) {
  if (!medal) return { icon: '🏅', name: 'Medalja', description: '', tooltip: 'Medalja' };
  if (typeof medal !== 'object') return { icon: medal, name: 'Medalja', description: '', tooltip: 'Medalja' };

  const icon = medalIcons[medal.tier] || '🏅';
  const details = medalDetails[medal.category] || { name: medal.category_name || 'Priznanje', desc: () => '' };
  const tierPrefix = medal.tier === 'gold' ? 'Zlatna' : medal.tier === 'silver' ? 'Srebrna' : 'Bronzana';
  const threshold = medalThresholds[medal.category]?.[medal.tier];
  const fullName = `${tierPrefix} ${details.name}`;
  const description = threshold != null ? details.desc(threshold) : '';

  return {
    icon: icon,
    name: fullName,
    description: description,
    tooltip: description ? `${fullName}\n${description}` : fullName
  };
}

function getTierClass(title) {
  if (!title) return 'bg-slate-100 text-slate-600 border-slate-200 dark:bg-slate-700 dark:text-slate-300 dark:border-slate-600';
  const t = title.toLowerCase();
  if (t.includes('legenda') || t.includes('zlatni') || t.includes('expert')) {
    return 'bg-amber-50 text-amber-700 border-amber-300 dark:bg-amber-950/40 dark:text-amber-400 dark:border-amber-800 font-bold';
  }
  if (t.includes('srebrni') || t.includes('napredni')) {
    return 'bg-slate-100 text-slate-700 border-slate-300 dark:bg-slate-700 dark:text-slate-300 dark:border-slate-600';
  }
  return 'bg-orange-50 text-orange-700 border-orange-200 dark:bg-orange-950/30 dark:text-orange-400 dark:border-orange-900';
}

function getRoleBadgeClass(role) {
  if (!role) return 'bg-slate-100 text-slate-600 border-slate-200 dark:bg-slate-700 dark:text-slate-300 dark:border-slate-600';
  const r = role.toLowerCase();
  if (r === 'admin') {
    return 'bg-red-50 text-red-700 border-red-300 dark:bg-red-950/40 dark:text-red-400 dark:border-red-800 font-bold';
  }
  if (r === 'autor' || r === 'mentor') {
    return 'bg-indigo-50 text-indigo-700 border-indigo-300 dark:bg-indigo-950/40 dark:text-indigo-400 dark:border-indigo-800';
  }
  return 'bg-blue-50 text-blue-600 border-blue-200 dark:bg-blue-950/30 dark:text-blue-400 dark:border-blue-900';
}

const authorMedals = computed(() => props.tema?.author?.medals || []);
const featuredMedals = computed(() => authorMedals.value.slice(0, 3));
const remainingMedals = computed(() => authorMedals.value.slice(3));



function formatDate(dateValue) {
  if (!dateValue) return "";
  return new Intl.DateTimeFormat("bs-BA", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric"
  }).format(new Date(dateValue));
}
</script>

<template>
  <router-link 
    :to="`/forum/tema/${tema.id}`"
    class="block px-5 py-5 bg-white dark:bg-slate-800 rounded-xl border shadow-sm hover:shadow-md dark:hover:border-slate-600 transition-all cursor-pointer group"
    :class="tema.is_locked ? 'border-amber-200 dark:border-amber-900 bg-amber-50/5' : 'border-gray-200 dark:border-slate-700/60'"
  >
    <div class="flex justify-between items-start">
      <h2 class="text-lg font-bold text-slate-800 dark:text-slate-100 group-hover:text-[#ff7a00] dark:group-hover:text-orange-400 transition-colors line-clamp-1 flex-1 flex items-center gap-1.5">
        <span v-if="tema.is_locked" title="Zaključano">🔒</span>
        {{ tema.title }}
      </h2>
      
      <div class="flex items-center gap-2 flex-shrink-0 ml-4">
        <span class="bg-orange-50 dark:bg-orange-950/30 text-[#ff7a00] dark:text-orange-400 text-[10px] font-extrabold uppercase px-2 py-0.5 rounded tracking-wider">
          {{ tema.category?.name || 'Opšta diskusija' }}
        </span>

        <button
          v-if="isAdmin"
          @click.prevent="emit('obrisi', tema.id)"
          class="w-7 h-7 flex items-center justify-center rounded-full text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/30 hover:text-red-800 dark:hover:text-red-300 transition-colors text-xs bg-transparent"
          title="Obriši temu"
        >
          🗑️
        </button>
      </div>
    </div>
    
    <p class="text-slate-600 dark:text-slate-300 mt-3 text-sm leading-relaxed font-normal line-clamp-3">
      {{ tema.content }}
    </p>

    <div v-if="tema.tags && tema.tags.length > 0" class="flex flex-wrap gap-1.5 mt-3.5">
      <span 
        v-for="tag in tema.tags" 
        :key="tag.id" 
        @click.prevent
        class="text-[10px] font-medium px-2 py-0.5 bg-slate-50 text-slate-500 dark:bg-slate-700/50 dark:text-slate-400 border border-slate-100 dark:border-slate-600 rounded-md"
      >
        #{{ tag.name }}
      </span>
    </div>
    
    <div class="flex items-center justify-between mt-5 pt-4 border-t border-gray-100 dark:border-slate-700 text-xs text-slate-500 dark:text-slate-400">
  <div class="flex items-center gap-2 font-medium flex-wrap">
    <ForumAvatar :author="tema.author" class="w-5.5 h-5.5 text-[9px]" />

    <span class="text-slate-700 dark:text-slate-200 font-semibold">
      {{ tema.author?.full_name || 'Korisnik' }}
    </span>

    <span
      class="font-bold uppercase text-[10px] px-1.5 py-0.5 rounded border"
      :class="getRoleBadgeClass(tema.author?.role)"
    >
      {{ tema.author?.role || 'Student' }}
    </span>

    <span class="text-[10px] font-medium text-slate-400 dark:text-slate-500">
      Lvl {{ tema.author?.level || 1 }}
    </span>

    <span
      v-if="tema.author?.title"
      class="text-[10px] px-2 py-0.5 rounded border scale-95 origin-left"
      :class="getTierClass(tema.author.title)"
    >
      {{ tema.author.title }} ({{ tema.author.reputation_points }} XP)
    </span>

    <div
      v-if="authorMedals.length > 0"
      class="flex items-center gap-1 border-l pl-2 border-slate-200 dark:border-slate-700 relative medals-dropdown-container"
    >
      <span
        v-for="m in featuredMedals"
        :key="m.code || m.id"
        class="text-base cursor-help transition-transform hover:scale-125 leading-none"
        :title="parseMedal(m).tooltip"
      >
        {{ parseMedal(m).icon }}
      </span>

      <button
        v-if="remainingMedals.length > 0"
        @click.prevent.stop="showAllMedalsDropdown = !showAllMedalsDropdown"
        class="flex items-center gap-0.5 bg-slate-100 dark:bg-slate-600 hover:bg-slate-200 dark:hover:bg-slate-500 transition-colors text-[10px] px-1.5 py-0.5 rounded font-bold text-slate-600 dark:text-slate-200 ml-0.5 bg-transparent border-none cursor-pointer"
      >
        +{{ remainingMedals.length }}
        <span>{{ showAllMedalsDropdown ? '▲' : '▼' }}</span>
      </button>

      <div
        v-if="showAllMedalsDropdown && remainingMedals.length > 0"
        @click.prevent.stop
        class="absolute top-full left-0 mt-1 bg-white dark:bg-slate-700 border border-gray-200 dark:border-slate-600 shadow-xl rounded-lg p-2.5 w-44 z-30"
      >
        <p class="text-[9px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-400 mb-2 border-b pb-1 border-slate-100 dark:border-slate-600">
          Ostala priznanja
        </p>

        <div class="flex flex-wrap gap-1.5 max-h-32 overflow-y-auto">
          <span
            v-for="m in remainingMedals"
            :key="m.code || m.id"
            class="text-base cursor-help transition-transform hover:scale-125 p-1 rounded hover:bg-slate-50 dark:hover:bg-slate-600 leading-none"
            :title="parseMedal(m).tooltip"
          >
            {{ parseMedal(m).icon }}
          </span>
        </div>
      </div>
    </div>

    <span class="text-slate-300 dark:text-slate-600">•</span>
    <span>{{ formatDate(tema.created_at) }}</span>
  </div>

  <div class="flex items-center space-x-4 font-medium">
    <span class="flex items-center gap-1">
      👁️ {{ tema.views_count || 0 }}
    </span>

    <span class="text-[#ff7a00] dark:text-orange-400 flex items-center gap-1 font-semibold">
      💬 {{ tema.comments_count || 0 }}
    </span>
  </div>
</div>
  </router-link>
</template>