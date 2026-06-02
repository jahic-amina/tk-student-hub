<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { deleteTopic } from '../services/forum';

const router = useRouter();
const currentUserId = ref(null);

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

const props = defineProps({
  topic: { type: Object, required: true }
});

const formatDate = (dateValue) => {
  if (!dateValue) return "";
  return new Intl.DateTimeFormat("bs-BA", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(dateValue));
}

const getInitials = (name) => {
  if (!name) return "?";
  return name.split(" ").map((part) => part[0]).join("").slice(0, 2).toUpperCase();
}

const showShareBox = ref(false);
const copySuccess = ref(false);
const shareUrl = computed(() => window.location.href);

function toggleShare() {
  showShareBox.value = !showShareBox.value;
  copySuccess.value = false;
}

async function copyToClipboard() {
  try {
    await navigator.clipboard.writeText(shareUrl.value);
    copySuccess.value = true;
    setTimeout(() => { copySuccess.value = false; }, 3000);
  } catch {
    const el = document.createElement('textarea');
    el.value = shareUrl.value;
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
    copySuccess.value = true;
    setTimeout(() => { copySuccess.value = false; }, 3000);
  }
}

async function handleDeleteTopic() {
  if (!confirm('Da li ste sigurni da želite obrisati ovu temu?')) return;
  try {
    await deleteTopic(props.topic.id);
    router.push('/forum');
  } catch (e) {
    alert('Greška pri brisanju teme.');
  }
}

</script>

<template>
  <div class="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 shadow-sm p-6 mb-6 transition-colors duration-200">
    <h1 class="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-4">{{ topic.title }}</h1>
    
    <div class="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400 mb-4 bg-slate-50 dark:bg-slate-700 p-2 rounded-lg w-fit">
      <span class="w-6 h-6 rounded-full bg-orange-500 text-white flex items-center justify-center font-bold text-[10px]">
        {{ getInitials(topic.author?.full_name) }}
      </span>
      <span class="font-semibold text-slate-700 dark:text-slate-200">{{ topic.author?.full_name || 'Student' }}</span>
      <span>•</span>
      <span>{{ formatDate(topic.created_at) }}</span>
      <span>•</span>
      <span>👁️ {{ topic.views_count || 0 }} pregleda</span>
    </div>

    <p class="text-slate-700 dark:text-slate-300 leading-relaxed whitespace-pre-line">{{ topic.content }}</p>

    <div class="mt-4 pt-4 border-t border-gray-100 dark:border-slate-700 flex flex-col gap-2">
      <div class="flex items-center gap-2">
        <button
          @click="toggleShare"
          class="flex items-center gap-1.5 text-xs text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 transition-colors font-medium px-3 py-1.5 rounded-lg border border-gray-200 dark:border-slate-600 hover:bg-gray-50 dark:hover:bg-slate-700 bg-transparent"
        >
          🔗 Dijeli
        </button>
        <button
          v-if="currentUserId === topic.author?.id"
          @click="handleDeleteTopic"
          class="flex items-center gap-1.5 text-xs text-red-400 hover:text-red-600 transition-colors font-medium px-3 py-1.5 rounded-lg border border-red-200 dark:border-red-900/50 hover:bg-red-50 dark:hover:bg-red-950/20 bg-transparent"
        >
          🗑️ Obriši temu
        </button>
      </div>

      <div v-if="showShareBox" class="p-3 bg-slate-50 dark:bg-slate-700/50 rounded-lg border border-gray-200 dark:border-slate-700 flex flex-col gap-2">
        <p class="text-xs text-slate-500 dark:text-slate-400 font-medium">Link teme:</p>
        <div v-if="copySuccess" class="text-xs text-green-600 dark:text-green-400 font-semibold bg-green-50 dark:bg-green-950/30 border border-green-200 dark:border-green-900 px-3 py-2 rounded-lg">
          ✓ URL has successfully been copied to clipboard.
        </div>
        <div class="flex gap-2">
          <input
            :value="shareUrl"
            readonly
            class="flex-1 text-xs bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-600 dark:text-slate-300 focus:outline-none cursor-text"
            @click="($event.target).select()"
          />
          <button
            @click="copyToClipboard"
            class="px-3 py-2 bg-orange-500 hover:bg-orange-400 text-white text-xs font-bold rounded-lg transition-colors"
          >
            Copy
          </button>
          <button
            @click="showShareBox = false"
            class="px-3 py-2 bg-white dark:bg-slate-800 hover:bg-gray-100 dark:hover:bg-slate-700 text-slate-500 dark:text-slate-400 text-xs font-medium rounded-lg border border-gray-200 dark:border-slate-700 transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>