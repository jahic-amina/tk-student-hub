<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { deleteTopic, reportTopic, toggleTopicLike, toggleTopicDislike } from '../services/forum';
import { toggleTopicLock } from '../services/forum_admin';
import { updateTopic } from '../services/forum';
import ForumAvatar from './ForumAvatar.vue';
import ForumCommentForm from './ForumTopicCommentForm.vue';
import ForumAttachmentPreview from './ForumAttachmentPreview.vue';

const router = useRouter();
const currentUserId = ref(null);
const showAllMedalsDropdown = ref(false);

const isReplyingToTopic = ref(false);
const isSubmittingReply = ref(false);
const replyError = ref('');
const replySuccess = ref('');
const isVotingTopic = ref(false);

const isEditingTopic = ref(false);
const editTitle = ref('');
const editContent = ref('');

const closeDropdown = (e) => {
  if (!e.target.closest('.medals-dropdown-container')) {
    showAllMedalsDropdown.value = false;
  }
};

onMounted(async () => {
  window.addEventListener('click', closeDropdown);
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

onBeforeUnmount(() => {
  window.removeEventListener('click', closeDropdown);
});

const props = defineProps({
  topic: { type: Object, required: true },
  isAdmin: { type: Boolean, default: false }
});

const emit = defineEmits(['submit-topic-reply', 'refresh']);

const authorMedals = computed(() => props.topic?.author?.medals || []);
const featuredMedals = computed(() => authorMedals.value.slice(0, 3));
const remainingMedals = computed(() => authorMedals.value.slice(3));

const medalIcons = { gold: '🥇', silver: '🥈', bronze: '🥉' };
const medalThresholds = {
  best_answers: { bronze: 1, silver: 5, gold: 15 },
  topics_started: { bronze: 3, silver: 10, gold: 25 },
  reputation: { bronze: 100, silver: 500, gold: 1000 },
  night_owl: { bronze: 1, silver: 3, gold: 10 }
};
const medalDetails = {
  best_answers: { name: 'Najbolji odgovori', desc: (n) => `Dobija se kada vaš odgovor bude označen kao najbolji ${n} ${n === 1 ? 'put' : 'puta'}.` },
  topics_started: { name: 'Pokrenute teme', desc: (n) => `Dobija se kada pokrenete ${n} ${n === 1 ? 'temu' : 'tema'} na forumu.` },
  reputation: { name: 'Ukupna reputacija', desc: (n) => `Dobija se kada skupite ukupno ${n} XP reputacije.` },
  night_owl: { name: 'Noćna ptica', desc: (n) => `Tajna medalja — dobija se kada pokrenete ${n} ${n === 1 ? 'temu' : 'tema'} između 03:00 i 05:00h.` }
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
  return { icon, name: fullName, description, tooltip: description ? `${fullName}\n${description}` : fullName };
}

const formatDate = (dateValue) => {
  if (!dateValue) return "";
  return new Intl.DateTimeFormat("bs-BA", {
    day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit",
  }).format(new Date(dateValue));
};

function getTierClass(title) {
  if (!title) return 'bg-slate-100 text-slate-600 border-slate-200 dark:bg-slate-700 dark:text-slate-300 dark:border-slate-600';
  const t = title.toLowerCase();
  if (t.includes('legenda') || t.includes('zlatni') || t.includes('expert')) return 'bg-amber-50 text-amber-700 border-amber-300 dark:bg-amber-950/40 dark:text-amber-400 dark:border-amber-800 font-bold';
  if (t.includes('srebrni') || t.includes('napredni')) return 'bg-slate-100 text-slate-700 border-slate-300 dark:bg-slate-700 dark:text-slate-300 dark:border-slate-600';
  return 'bg-orange-50 text-orange-700 border-orange-200 dark:bg-orange-950/30 dark:text-orange-400 dark:border-orange-900';
}

function getRoleBadgeClass(role) {
  if (!role) return 'bg-slate-100 text-slate-600 border-slate-200 dark:bg-slate-700 dark:text-slate-300 dark:border-slate-600';
  const r = role.toLowerCase();
  if (r === 'admin') return 'bg-red-50 text-red-700 border-red-300 dark:bg-red-950/40 dark:text-red-400 dark:border-red-800 font-bold';
  if (r === 'autor' || r === 'mentor') return 'bg-indigo-50 text-indigo-700 border-indigo-300 dark:bg-indigo-950/40 dark:text-indigo-400 dark:border-indigo-800';
  return 'bg-blue-50 text-blue-600 border-blue-200 dark:bg-blue-950/30 dark:text-blue-400 dark:border-blue-900';
}

const showShareBox = ref(false);
const copySuccess = ref(false);
const shareUrl = computed(() => window.location.href);
const showReportOptions = ref(false);
const reportReasons = ['Spam', 'Neprimjeren rječnik / Vrijeđanje', 'Off-topic', 'Netačne informacije'];

function toggleShare() { showShareBox.value = !showShareBox.value; copySuccess.value = false; }
function shareOnFacebook() { window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl.value)}`, '_blank'); }
function shareOnWhatsApp() { window.open(`https://wa.me/?text=${encodeURIComponent(shareUrl.value)}`, '_blank'); }
function shareOnViber() { window.open(`viber://forward?text=${encodeURIComponent(shareUrl.value)}`, '_blank'); }
function shareOnMessenger() { window.open(`fb-messenger://share/?link=${encodeURIComponent(shareUrl.value)}`, '_blank'); }

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
  try { await deleteTopic(props.topic.id); router.push('/forum'); } catch (e) { alert('Greška pri brisanju teme.'); }
}

async function handleReport(reason) {
  try { await reportTopic(props.topic.id, reason); alert('Tema je uspješno prijavljena adminima.'); showReportOptions.value = false; } catch (e) { alert('Greška pri prijavi.'); }
}

async function handleLockTopic() {
  try { await toggleTopicLock(props.topic.id); props.topic.is_locked = !props.topic.is_locked; } catch (e) { alert('Greška pri promjeni statusa zaključavanja.'); }
}

async function handleTopicLike() {
  if (isVotingTopic.value) return;
  isVotingTopic.value = true;
  try {
    const response = await toggleTopicLike(props.topic.id);
    props.topic.likes_count = response.likes_count;
    props.topic.dislikes_count = response.dislikes_count;
    props.topic.is_liked = response.is_liked;
    props.topic.is_disliked = response.is_disliked;
  } catch (e) {
    alert('Greška pri lajkanju teme.');
  } finally {
    isVotingTopic.value = false;
  }
}

async function handleTopicDislike() {
  if (isVotingTopic.value) return;
  isVotingTopic.value = true;
  try {
    const response = await toggleTopicDislike(props.topic.id);
    props.topic.likes_count = response.likes_count;
    props.topic.dislikes_count = response.dislikes_count;
    props.topic.is_liked = response.is_liked;
    props.topic.is_disliked = response.is_disliked;
  } catch (e) {
    alert('Greška pri dislajkanju teme.');
  } finally {
    isVotingTopic.value = false;
  }
}

function startEditTopic() {
  isEditingTopic.value = true;
  editTitle.value = props.topic.title;
  editContent.value = props.topic.content;
}

function cancelEditTopic() {
  isEditingTopic.value = false;
  editTitle.value = '';
  editContent.value = '';
}

async function submitEditTopic() {
  if (!editTitle.value.trim() || !editContent.value.trim()) return;
  try {
    const updated = await updateTopic(props.topic.id, {
      title: editTitle.value,
      content: editContent.value
    });
    props.topic.title = updated.title;
    props.topic.content = updated.content;
    isEditingTopic.value = false;
  } catch (e) {
    alert('Greška pri editovanju teme.');
  }
}

function handleFormSubmit({ content, files = [], clearForm }) {
  if (!content.trim()) {
    replyError.value = 'Tekst komentara ne može biti prazan.';
    return;
  }
  replyError.value = '';
  isSubmittingReply.value = true;
  emit('submit-topic-reply', {
    content,
    files,
    onSuccess: () => {
      isSubmittingReply.value = false;
      clearForm();
      replySuccess.value = 'Odgovor uspješno objavljen!';
      setTimeout(() => {
        replySuccess.value = '';
        isReplyingToTopic.value = false;
      }, 2000);
    },
    onError: (errMgs) => {
      isSubmittingReply.value = false;
      replyError.value = errMgs || 'Došlo je do greške prilikom slanja.';
    }
  });
}
</script>

<template>
  <div
    class="bg-white dark:bg-slate-900 rounded-xl border shadow-sm p-6 mb-6 transition-colors duration-200"
    :class="topic.is_locked ? 'border-amber-300 dark:border-amber-900 bg-amber-50/10' : 'border-gray-200 dark:border-slate-700'"
  >
    <div v-if="isEditingTopic" class="flex flex-col gap-3 mb-4">
      <input 
        v-model="editTitle" 
        type="text" 
        class="w-full text-xl font-bold p-2 border rounded-lg dark:bg-slate-700 dark:text-slate-100 dark:border-slate-600 focus:outline-none focus:ring-2 focus:ring-orange-500"
        placeholder="Naslov teme..."
      />
      <textarea 
        v-model="editContent" 
        rows="5" 
        class="w-full p-2 border rounded-lg dark:bg-slate-700 dark:text-slate-100 dark:border-slate-600 focus:outline-none focus:ring-2 focus:ring-orange-500 resize-y"
        placeholder="Sadržaj teme..."
      ></textarea>
      <div class="flex gap-2 justify-end">
        <button @click="cancelEditTopic" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-100 text-slate-600 hover:bg-slate-200 dark:bg-slate-700 dark:text-slate-300 dark:hover:bg-slate-600 cursor-pointer">Otkaži</button>
        <button @click="submitEditTopic" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-orange-500 text-white hover:bg-orange-600 cursor-pointer">Spasi izmjene</button>
      </div>
    </div>

    <h1 v-else class="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-4 flex items-center gap-2">
      <span v-if="topic.is_locked" title="Tema je zaključana">🔒</span>
      {{ topic.title }}
    </h1>

    <div class="flex items-center flex-wrap gap-2 text-xs text-slate-500 dark:text-slate-400 mb-4 bg-slate-50 dark:bg-slate-700 p-2 rounded-lg w-fit">
      <ForumAvatar :author="topic.topic_author || topic.author" />
      <span class="font-semibold text-slate-700 dark:text-slate-200">{{ topic.author?.full_name || 'Korisnik' }}</span>
      <span class="font-bold uppercase text-[10px] px-1.5 py-0.5 rounded border" :class="getRoleBadgeClass(topic.author?.role)">{{ topic.author?.role || 'Student' }}</span>
      <span class="text-[10px] font-medium text-slate-400 dark:text-slate-500">Lvl {{ topic.author?.level || 1 }}</span>
      <span v-if="topic.author?.title" class="text-[10px] px-2 py-0.5 rounded border scale-95 origin-left" :class="getTierClass(topic.author.title)">{{ topic.author.title }} ({{ topic.author.reputation_points }} XP)</span>
      <span v-if="topic.is_locked" class="ml-2 bg-amber-100 dark:bg-amber-950/60 text-amber-700 dark:text-amber-400 px-2 py-0.5 rounded-full font-bold text-[10px]">Zaključano</span>

      <div v-if="authorMedals.length > 0" class="flex items-center gap-1 ml-2 border-l pl-2 border-slate-200 dark:border-slate-600 relative medals-dropdown-container">
        <span v-for="rawMedal in featuredMedals" :key="rawMedal.code || rawMedal.id" class="text-base cursor-help transition-transform hover:scale-125 leading-none" :title="parseMedal(rawMedal).tooltip">{{ parseMedal(rawMedal).icon }}</span>
        <button v-if="remainingMedals.length > 0" @click.stop="showAllMedalsDropdown = !showAllMedalsDropdown" class="flex items-center gap-0.5 bg-slate-100 dark:bg-slate-600 hover:bg-slate-200 dark:hover:bg-slate-500 transition-colors text-[10px] px-1.5 py-0.5 rounded font-bold text-slate-600 dark:text-slate-200 ml-0.5 bg-transparent border-none cursor-pointer">+{{ remainingMedals.length }} <span>{{ showAllMedalsDropdown ? '▲' : '▼' }}</span></button>
        <div v-if="showAllMedalsDropdown && remainingMedals.length > 0" class="absolute top-full left-0 mt-1 bg-white dark:bg-slate-700 border border-gray-200 dark:border-slate-600 shadow-xl rounded-lg p-2.5 w-44 z-30">
          <p class="text-[9px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-400 mb-2 border-b pb-1 border-slate-100 dark:border-slate-600">Ostala priznanja</p>
          <div class="flex flex-wrap gap-1.5 max-h-32 overflow-y-auto">
            <span v-for="rawMedal in remainingMedals" :key="rawMedal.code || rawMedal.id" class="text-base cursor-help transition-transform hover:scale-125 p-1 rounded hover:bg-slate-50 dark:hover:bg-slate-600 leading-none" :title="parseMedal(rawMedal).tooltip">{{ parseMedal(rawMedal).icon }}</span>
          </div>
        </div>
      </div>
    </div>

    <p v-if="!isEditingTopic" class="text-slate-700 dark:text-slate-300 leading-relaxed whitespace-pre-line mb-4">{{ topic.content }}</p>

    <div v-if="topic.tags && topic.tags.length > 0" class="flex flex-wrap gap-1.5 mb-4">
      <span v-for="tag in topic.tags" :key="tag.id" class="text-[11px] font-medium px-2.5 py-1 bg-slate-100 text-slate-600 dark:bg-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-600 rounded-md shadow-sm">#{{ tag.name }}</span>
    </div>

    <div v-if="topic.attachments && topic.attachments.length > 0" class="mt-2 mb-4">
      <ForumAttachmentPreview
        :attachments="topic.attachments"
        :download-base-url="`http://127.0.0.1:8000/forum/attachments/topic/${topic.id}`"
      />
    </div>

    <div class="mt-4 pt-4 border-t border-gray-100 dark:border-slate-700 flex flex-col gap-2">
      <div class="flex items-center w-full gap-2">
        
        <div v-if="!isAdmin" class="topic-votes">
          <button
            type="button"
            class="topic-vote-btn"
            :class="{ active: topic.is_liked }"
            :disabled="isVotingTopic"
            @click="handleTopicLike"
            title="Lajkaj temu"
          >
            <svg viewBox="0 0 24 24" class="topic-vote-icon" aria-hidden="true">
              <path fill="currentColor" d="M7 10.5v9H4.8A2.8 2.8 0 0 1 2 16.7v-3.4a2.8 2.8 0 0 1 2.8-2.8H7Zm2 9h7.6c1.1 0 2.1-.7 2.4-1.8l1.4-5.2A2.5 2.5 0 0 0 18 9.4h-3.3V6.2A2.7 2.7 0 0 0 12 3.5c-.5 0-.9.3-1.1.8L9.5 8.5 7 10.8v8.7h2Z" />
            </svg>
          </button>
          <span class="topic-vote-count" :class="{ active: topic.is_liked }">{{ topic.likes_count ?? 0 }}</span>
          <button
            type="button"
            class="topic-vote-btn"
            :class="{ active: topic.is_disliked }"
            :disabled="isVotingTopic"
            @click="handleTopicDislike"
            title="Dislajkuj temu"
          >
            <svg viewBox="0 0 24 24" class="topic-vote-icon topic-vote-icon-down" aria-hidden="true">
              <path fill="currentColor" d="M7 10.5v9H4.8A2.8 2.8 0 0 1 2 16.7v-3.4a2.8 2.8 0 0 1 2.8-2.8H7Zm2 9h7.6c1.1 0 2.1-.7 2.4-1.8l1.4-5.2A2.5 2.5 0 0 0 18 9.4h-3.3V6.2A2.7 2.7 0 0 0 12 3.5c-.5 0-.9.3-1.1.8L9.5 8.5 7 10.8v8.7h2Z" />
            </svg>
          </button>
          <span class="topic-vote-count" :class="{ active: topic.is_disliked }">{{ topic.dislikes_count ?? 0 }}</span>
        </div>

        <button
          v-if="!topic.is_locked && !isAdmin"
          @click="isReplyingToTopic = !isReplyingToTopic"
          class="flex items-center gap-1 text-[11px] font-bold uppercase tracking-wider text-white bg-orange-500 hover:bg-orange-400 transition-all duration-200 px-2 py-1 rounded-md shadow-sm border-none cursor-pointer"
          :class="{ 'bg-orange-600 ring-2 ring-orange-300 dark:ring-orange-900': isReplyingToTopic }"
        >
          ↩ Odgovori
        </button>

        <button @click="toggleShare" class="flex items-center gap-1.5 text-xs text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 transition-colors font-medium px-3 py-1.5 rounded-lg border border-gray-200 dark:border-slate-600 hover:bg-gray-50 dark:hover:bg-slate-700 bg-transparent">🔗 Dijeli</button>

        <div v-if="!isAdmin && !topic.is_locked" class="relative">
          <button @click="showReportOptions = !showReportOptions" class="flex items-center gap-1.5 text-xs text-red-400 hover:text-red-600 transition-colors font-medium px-3 py-1.5 rounded-lg border border-red-200 hover:bg-red-50 bg-transparent">🚩 Prijavi</button>
          <div v-if="showReportOptions" class="absolute top-full mt-1 left-0 bg-white dark:bg-slate-700 border dark:border-slate-600 shadow-lg rounded-lg w-48 z-10 text-xs overflow-hidden">
            <button v-for="reason in reportReasons" :key="reason" @click="handleReport(reason)" class="block w-full text-left px-4 py-2 hover:bg-gray-50 dark:hover:bg-slate-600 text-slate-600 dark:text-slate-200 bg-transparent">{{ reason }}</button>
          </div>
        </div>

        <button v-if="isAdmin" @click="handleLockTopic" class="flex items-center gap-1.5 text-xs text-orange-500 hover:text-orange-700 transition-colors font-medium px-3 py-1.5 rounded-lg border border-orange-200 hover:bg-orange-50 bg-transparent">🔒 {{ topic.is_locked ? 'Otključaj temu' : 'Zaključaj temu' }}</button>
        
        <button v-if="(currentUserId === topic.author?.id || isAdmin) && !isEditingTopic" @click="startEditTopic" class="flex items-center gap-1.5 text-xs text-blue-500 hover:text-blue-700 transition-colors font-medium px-3 py-1.5 rounded-lg border border-blue-200 dark:border-blue-900/50 hover:bg-blue-50 dark:hover:bg-slate-700 bg-transparent cursor-pointer">✏️ Uredi temu</button>
        
        <button v-if="currentUserId === topic.author?.id || isAdmin" @click="handleDeleteTopic" class="flex items-center gap-1.5 text-xs text-red-400 hover:text-red-600 transition-colors font-medium px-3 py-1.5 rounded-lg border border-red-200 dark:border-red-900/50 hover:bg-red-50 dark:hover:bg-red-950/20 bg-transparent">🗑️ Obriši temu</button>

        <div class="ml-auto flex items-center gap-3 text-xs text-slate-400 dark:text-slate-500 font-medium">
          <span title="Ukupan broj pregleda ove teme">👁️ {{ topic.views_count || 0 }} pregleda</span>
          <span class="text-slate-300 dark:text-slate-600">•</span>
          <span>📅 Objavljeno: {{ formatDate(topic.created_at) }}</span>
        </div>
      </div>

      <div v-if="isReplyingToTopic" class="mt-4 transition-all">
        <ForumCommentForm
          :is-submitting="isSubmittingReply"
          :comment-error="replyError"
          :success-message="replySuccess"
          @posalji-komentar="handleFormSubmit"
          @otkazi="isReplyingToTopic = false; replyError = ''; replySuccess = ''"
        />
      </div>

      <div v-if="showShareBox" class="p-3 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 shadow-lg flex flex-col gap-2">
        <p class="text-xs text-slate-500 dark:text-slate-400 font-semibold px-1">Podijeli temu</p>
        <div class="flex items-center gap-2">
          <button @click="copyToClipboard" class="flex flex-col items-center gap-1 p-2 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors bg-transparent border-none" title="Kopiraj link">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 00-5.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" /></svg>
            <span class="text-[10px] text-slate-500">{{ copySuccess ? 'Kopirano!' : 'Kopiraj' }}</span>
          </button>
          <button @click="shareOnFacebook" class="flex flex-col items-center gap-1 p-2 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors bg-transparent border-none" title="Facebook">
            <svg class="w-8 h-8" viewBox="0 0 24 24" fill="#1877F2"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
            <span class="text-[10px] text-slate-500">Facebook</span>
          </button>
          <button @click="shareOnMessenger" class="flex flex-col items-center gap-1 p-2 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors bg-transparent border-none" title="Messenger">
            <svg class="w-8 h-8" viewBox="0 0 24 24" fill="#0099FF"><path d="M12 0C5.373 0 0 4.974 0 11.111c0 3.498 1.744 6.614 4.469 8.654V24l4.088-2.242c1.092.3 2.246.464 3.443.464 6.627 0 12-4.974 12-11.111C24 4.974 18.627 0 12 0zm1.191 14.963l-3.055-3.26-5.963 3.26L10.732 8.1l3.131 3.26L19.752 8.1l-6.561 6.863z"/></svg>
            <span class="text-[10px] text-slate-500">Messenger</span>
          </button>
          <button @click="shareOnWhatsApp" class="flex flex-col items-center gap-1 p-2 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors bg-transparent border-none" title="WhatsApp">
            <svg class="w-8 h-8" viewBox="0 0 24 24" fill="#25D366"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
            <span class="text-[10px] text-slate-500">WhatsApp</span>
          </button>
          <button @click="shareOnViber" class="flex flex-col items-center gap-1 p-2 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors bg-transparent border-none" title="Viber">
            <img src="https://cdn.simpleicons.org/viber/7360F2" class="w-8 h-8" alt="Viber" />
            <span class="text-[10px] text-slate-500">Viber</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.topic-votes {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 30px;
  margin-right: 10px;
}
.topic-vote-btn {
  border: none;
  background: transparent;
  color: #cbd5e1;
  padding: 2px;
  cursor: pointer;
  transition: all 0.18s ease;
  line-height: 1;
}
.topic-vote-btn:hover { color: #ff7a00; transform: scale(1.12); }
.topic-vote-btn.active { color: #ff7a00; }
.topic-vote-btn:disabled { cursor: not-allowed; opacity: 0.65; }
.topic-vote-icon { width: 18px; height: 18px; display: block; }
.topic-vote-icon-down { transform: rotate(180deg); }
.topic-vote-count { font-size: 12px; font-weight: 700; color: #94a3b8; line-height: 1.1; margin: 1px 0 4px; }
.topic-vote-count.active { color: #ff7a00; }
</style>