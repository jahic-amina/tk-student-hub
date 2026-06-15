<script setup>
import { ref, onMounted } from 'vue';
import { toggleTopicLike } from '../composables/useForumExtras.js';

const props = defineProps({
  tema: { type: Object, required: true },
  isAdmin: { type: Boolean, default: false }
});

const emit = defineEmits(['obrisi', 'like-updated']);

const currentUserId = ref(null);
const likeLoading = ref(false);

onMounted(async () => {
  try {
    const token = localStorage.getItem('token') || localStorage.getItem('access_token');
    if (token) {
      const res = await fetch('http://127.0.0.1:8000/me', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        currentUserId.value = data.id;
      }
    }
  } catch (e) {}
});

async function handleLike(tema) {
  if (likeLoading.value) return;
  
  // Anti-Abuse: Klijentska blokada lajkovanja sopstvene teme
  if (currentUserId.value === tema.author?.id) {
    alert('Ne možete lajkovati sopstvenu temu.');
    return;
  }

  try {
    likeLoading.value = true;
    const result = await toggleTopicLike(tema.id);

    emit('like-updated', {
      topicId: tema.id,
      likesCount: result.likes_count,
      liked: result.liked
    });
  } catch (error) {
    alert(error.message || 'Lajkovanje nije uspjelo ili je dostignut limit.');
  } finally {
    likeLoading.value = false;
  }
}

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
    
    <div class="flex items-center justify-between mt-5 pt-4 border-t border-gray-100 dark:border-slate-700 text-xs text-slate-500 dark:text-slate-400">
      <div class="flex items-center gap-2.5 font-medium">
        <span class="w-5.5 h-5.5 rounded-full bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 flex items-center justify-center font-bold text-[10px]">
          {{ getInitials(tema.author?.full_name) }}
        </span>
        <span class="text-slate-700 dark:text-slate-200 font-semibold">{{ tema.author?.full_name || 'Korisnik' }}</span>
        <span class="text-slate-300 dark:text-slate-600">•</span>
        <span>{{ formatDate(tema.created_at) }}</span>
      </div>

      <div class="flex items-center space-x-4 font-medium">
        <button
          v-if="!isAdmin"
          @click.prevent.stop="handleLike(tema)"
          :disabled="likeLoading || currentUserId === tema.author?.id"
          class="text-red-500 hover:text-red-600 disabled:opacity-40 transition-colors flex items-center gap-1 bg-transparent"
          :class="currentUserId === tema.author?.id ? 'cursor-not-allowed' : ''"
          :title="currentUserId === tema.author?.id ? 'Ne možete lajkovati sopstvenu temu' : 'Lajkuj temu'"
        >
          ❤️ <span class="font-semibold">{{ tema.likes_count || 0 }}</span>
        </button>

        <span class="flex items-center gap-1">👁️ {{ tema.views_count || 0 }}</span>
        <span class="text-[#ff7a00] dark:text-orange-400 flex items-center gap-1 font-semibold">
          💬 {{ tema.comments_count || 0 }}
        </span>
      </div>
    </div>
  </router-link>
</template>