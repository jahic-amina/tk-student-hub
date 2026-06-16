<script setup>
import { ref, computed, onMounted } from 'vue';
import { voteOnComment, toggleBestAnswer, deleteComment, updateComment, createComment } from '../services/forum';

const props = defineProps({
  comments: { type: Array, required: true },
  topicAuthorId: { type: Number, default: null },
  topicId: { type: Number, default: null  }
});

const emit = defineEmits(['refresh']);

const currentUserId = ref(null);
const currentUserRole = ref(null);

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
        currentUserRole.value = data.role;
      }
    }
  } catch (e) {
    console.warn('Nije moguće dohvatiti korisnika.');
  }
});

const isAdmin = computed(() => {
  return currentUserRole.value === 'admin';
});

const isTopicAuthor = computed(() => {
  return currentUserId.value && props.topicAuthorId && currentUserId.value === props.topicAuthorId;
});

const canReply = computed(() => !!currentUserId.value && !isAdmin.value);

// REAKTIVNO SKLADIŠTE ZA GLASOVE
const serverVoteState = ref({});

function getUserVote(comment) {
  if (serverVoteState.value[comment.id] !== undefined) return serverVoteState.value[comment.id].user_vote;
  return comment.user_vote || 0;
}

function getLikesCount(comment) {
  if (serverVoteState.value[comment.id] !== undefined) return serverVoteState.value[comment.id].likes_count;
  return comment.likes_count || 0;
}

function getDislikesCount(comment) {
  if (serverVoteState.value[comment.id] !== undefined) return serverVoteState.value[comment.id].dislikes_count;
  return comment.dislikes_count || 0;
}

// KODIRANJE I PARSIRANJE MEDALJA ZA KOMENTARE
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
    desc: (n) => `Dobijate kada vaš odgovor bude označen kao najbolji ${n} ${n === 1 ? 'put' : 'puta'}.`
  },
  topics_started: {
    name: 'Pokrenute teme',
    desc: (n) => `Dobijate kada pokrenete ${n} ${n === 1 ? 'temu' : 'tema'} na forumu.`
  },
  reputation: {
    name: 'Ukupna reputacija',
    desc: (n) => `Dobijate kada skupite ukupno ${n} XP reputacije.`
  },
  night_owl: {
    name: 'Noćna ptica',
    desc: (n) => `Tajna medalja — dobijate kada pokrenete ${n} ${n === 1 ? 'temu' : 'tema'} između 03:00 i 05:00h.`
  }
};

function parseMedal(medal) {
  if (!medal) return { icon: '🏅', name: 'Medalja', tierName: '', tooltip: 'Medalja' };
  if (typeof medal !== 'object') return { icon: medal, name: 'Medalja', tierName: '', tooltip: 'Medalja' };
  const icon = medalIcons[medal.tier] || '🏅';
  const details = medalDetails[medal.category] || { name: medal.category_name || 'Priznanje', desc: () => '' };
  const tierPrefix = medal.tier === 'gold' ? 'Zlatna' : medal.tier === 'silver' ? 'Srebrna' : 'Bronzana';
  const threshold = medalThresholds[medal.category]?.[medal.tier];
  const fullName = `${tierPrefix} – ${details.name}`;
  const description = threshold != null ? details.desc(threshold) : '';
  return {
    icon,
    name: details.name,
    tierName: tierPrefix,
    isSecret: medal.is_secret,
    tooltip: description ? `${fullName}\n${description}` : fullName
  };
}

function getTierClass(title) {
  if (!title) return 'bg-slate-100 text-slate-600 border-slate-200 dark:bg-slate-700 dark:text-slate-300 dark:border-slate-600';
  const t = title.toLowerCase();
  if (t.includes('zlatni') || t.includes('expert') || t.includes('legenda')) {
    return 'bg-amber-50 text-amber-700 border-amber-300 dark:bg-amber-950/40 dark:text-amber-400 dark:border-amber-800 font-bold';
  }
  if (t.includes('srebrni') || t.includes('napredni') || t.includes('mentor')) {
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

// DROPDOWN ZA MEDALJE
const openMedalDropdown = ref(null);

function toggleMedalDropdown(key) {
  openMedalDropdown.value = openMedalDropdown.value === key ? null : key;
}

function closeMedalDropdown() {
  openMedalDropdown.value = null;
}

// Edit komentar
const editingCommentId = ref(null);
const editContent = ref('');

function startEdit(comment) {
  editingCommentId.value = comment.id;
  editContent.value = comment.content;
}

function cancelEdit() {
  editingCommentId.value = null;
  editContent.value = '';
}

async function submitEdit(comment) {
  if (!editContent.value.trim()) return;
  try {
    await updateComment(comment.id, editContent.value);
    editingCommentId.value = null;
    emit('refresh');
  } catch (e) {
    alert('Greška pri editovanju komentara.');
  }
}

// Reply
const replyingToId = ref(null);
const replyContent = ref('');

function startReply(comment) {
  replyingToId.value = comment.id;
  replyContent.value = '';
}

function cancelReply() {
  replyingToId.value = null;
  replyContent.value = '';
}

async function submitReply(comment, topicId) {
  if (!replyContent.value.trim()) return;
  try {
    await createComment({
      content: replyContent.value,
      topic_id: topicId,
      parent_id: comment.id
    });
    replyingToId.value = null;
    emit('refresh');
  } catch (e) {
    alert('Greška pri slanju odgovora.');
  }
}

async function handleVote(comment, value) {
  if (!currentUserId.value) return alert('Morate biti prijavljeni da biste glasali.');
  if (currentUserId.value === comment.author?.id) {
    return alert('Ne možete glasati za vlastiti komentar.');
  }
  try {
    const result = await voteOnComment(comment.id, value);
    serverVoteState.value[comment.id] = {
      user_vote: result.user_vote,
      likes_count: result.likes_count !== undefined ? result.likes_count : (comment.likes_count + (result.user_vote === 1 ? 1 : 0)),
      dislikes_count: result.dislikes_count !== undefined ? result.dislikes_count : (comment.dislikes_count + (result.user_vote === -1 ? 1 : 0))
    };
    emit('refresh');
  } catch (e) {
    alert(e.response?.data?.detail || 'Greška pri glasanju ili je dostignut dnevni limit.');
  }
}

async function handleBestAnswer(comment) {
  if (!isTopicAuthor.value) return;
  try {
    await toggleBestAnswer(comment.id);
    emit('refresh');
  } catch (e) {
    alert('Greška pri označavanju najboljeg odgovora.');
  }
}

async function handleDeleteComment(comment) {
  if (!confirm('Da li ste sigurni da želite obrisati ovaj komentar?')) return;
  try {
    await deleteComment(comment.id);
    emit('refresh');
  } catch (e) {
    alert('Greška pri brisanju komentara.');
  }
}

function formatDate(dateValue) {
  if (!dateValue) return "";
  return new Intl.DateTimeFormat("bs-BA", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(dateValue));
}

function getInitials(name) {
  if (!name) return "?";
  return name.split(" ").map((part) => part[0]).join("").slice(0, 2).toUpperCase();
}
</script>

<template>
  <div class="mb-6" @click="closeMedalDropdown">
    <h2 class="text-lg font-semibold text-slate-700 dark:text-slate-200 mb-4">
      {{ comments.length }} {{ comments.length === 1 ? 'Odgovor' : 'Odgovora' }}
    </h2>

    <div class="space-y-4">
      <template v-for="comment in comments" :key="comment.id">

        <!-- ===================== ADMIN NOTICE ===================== -->
        <div
          v-if="comment.is_admin_notice"
          class="rounded-xl border-2 border-red-400 dark:border-red-700 bg-red-50 dark:bg-red-950/30 p-5 flex gap-4 shadow-md ring-2 ring-red-300/30 dark:ring-red-800/30"
        >
          <!-- Ikona umjesto vote stupca -->
          <div class="flex flex-col items-center justify-start pt-1 flex-shrink-0 w-7">
            <span class="text-2xl select-none">🛡️</span>
          </div>

          <div class="flex-1 min-w-0">
            <!-- Header -->
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center flex-wrap gap-2 text-xs">
                <span class="w-5 h-5 rounded-full bg-red-200 dark:bg-red-900 text-red-700 dark:text-red-300 flex items-center justify-center font-bold text-[8px]">
                  {{ getInitials(comment.author?.full_name) }}
                </span>
                <strong class="text-red-700 dark:text-red-300">{{ comment.author?.full_name || 'Admin' }}</strong>
                <span class="text-[10px] px-2 py-0.5 rounded border bg-red-100 text-red-700 border-red-300 dark:bg-red-950/60 dark:text-red-400 dark:border-red-800 font-bold">
                  🛡️ Admin Notice
                </span>
                <span class="text-red-400 dark:text-red-600">•</span>
                <span class="text-red-400 dark:text-red-600">{{ formatDate(comment.created_at) }}</span>
              </div>

              <!-- Admin može editovati i brisati notice -->
              <div class="flex items-center gap-1">
                <button
                  v-if="isAdmin && !comment.is_deleted"
                  @click="startEdit(comment)"
                  class="w-7 h-7 flex items-center justify-center rounded-full transition-all text-red-300 dark:text-red-700 hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-950/20"
                  title="Edituj obavještenje"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
                    <path d="M21.731 2.269a2.625 2.625 0 0 0-3.712 0l-1.157 1.157 3.712 3.712 1.157-1.157a2.625 2.625 0 0 0 0-3.712ZM19.513 8.199l-3.712-3.712-8.4 8.4a5.25 5.25 0 0 0-1.32 2.214l-.8 2.685a.75.75 0 0 0 .933.933l2.685-.8a5.25 5.25 0 0 0 2.214-1.32l8.4-8.4Z" />
                    <path d="M5.25 5.25a3 3 0 0 0-3 3v10.5a3 3 0 0 0 3 3h10.5a3 3 0 0 0 3-3V13.5a.75.75 0 0 0-1.5 0v5.25a1.5 1.5 0 0 1-1.5 1.5H5.25a1.5 1.5 0 0 1-1.5-1.5V8.25a1.5 1.5 0 0 1 1.5-1.5h5.25a.75.75 0 0 0 0-1.5H5.25Z" />
                  </svg>
                </button>
                <button
                  v-if="isAdmin"
                  @click="handleDeleteComment(comment)"
                  class="w-7 h-7 flex items-center justify-center rounded-full transition-all text-red-300 dark:text-red-700 hover:text-red-500 hover:bg-red-100 dark:hover:bg-red-950/40"
                  title="Obriši obavještenje"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
                    <path fill-rule="evenodd" d="M16.5 4.478v.227a48.816 48.816 0 0 1 3.878.512.75.75 0 1 1-.256 1.478l-.209-.035-1.005 13.07a3 3 0 0 1-2.991 2.77H8.084a3 3 0 0 1-2.991-2.77L4.087 6.66l-.209.035a.75.75 0 0 1-.256-1.478A48.567 48.567 0 0 1 7.5 4.705v-.227c0-1.564 1.213-2.9 2.816-2.951a52.662 52.662 0 0 1 3.369 0c1.603.051 2.815 1.387 2.815 2.951Zm-6.136-1.452a51.196 51.196 0 0 1 3.273 0C14.39 3.05 15 3.684 15 4.478v.113a49.488 49.488 0 0 0-6 0v-.113c0-.794.609-1.428 1.364-1.452Zm-.355 5.945a.75.75 0 1 0-1.5.058l.347 9a.75.75 0 1 0 1.499-.058l-.346-9Zm5.48.058a.75.75 0 1 0-1.498-.058l-.347 9a.75.75 0 0 0 1.5.058l.345-9Z" clip-rule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Sadržaj notice-a -->
            <div v-if="comment.is_deleted" class="text-red-400 dark:text-red-600 text-sm italic">
              deleted by user
            </div>
            <div v-else-if="editingCommentId === comment.id">
              <textarea
                v-model="editContent"
                class="w-full text-sm border border-red-200 dark:border-red-800 rounded-lg p-3 bg-white dark:bg-slate-700 text-slate-700 dark:text-slate-300 focus:outline-none focus:ring-2 focus:ring-red-400 resize-none"
                rows="3"
              />
              <div class="flex gap-2 mt-2">
                <button @click="submitEdit(comment)" class="px-3 py-1.5 bg-red-600 hover:bg-red-500 text-white text-xs font-bold rounded-lg transition-colors">
                  Sačuvaj
                </button>
                <button @click="cancelEdit()" class="px-3 py-1.5 bg-white dark:bg-slate-800 border border-red-200 dark:border-red-700 text-red-500 text-xs rounded-lg hover:bg-red-50 transition-colors">
                  Otkaži
                </button>
              </div>
            </div>
            <p v-else class="text-red-800 dark:text-red-300 leading-relaxed text-sm whitespace-pre-line font-medium">
              {{ comment.content }}
            </p>

            <!-- Nema reply opcije na admin notice -->
            <p class="mt-2 text-[10px] text-red-400/60 dark:text-red-600/60 italic select-none">
              Nije dozvoljeno odgovarati na administratorska obavještenja.
            </p>
          </div>
        </div>

        <!-- ===================== OBIČNI KOMENTAR ===================== -->
        <div
          v-else
          class="bg-white dark:bg-slate-800 rounded-xl border p-5 flex gap-4 transition-all shadow-sm"
          :class="[
            comment.is_best_answer
              ? 'border-yellow-400 dark:border-yellow-600 bg-yellow-50/40 dark:bg-yellow-950/20 ring-1 ring-yellow-400/30'
              : 'border-gray-200 dark:border-slate-700'
          ]"
        >
          <!-- Vote stupac -->
          <div class="flex flex-col items-center gap-0.5 flex-shrink-0 pt-1">
            <button
              @click="handleVote(comment, 1)"
              :disabled="currentUserId === comment.author?.id"
              class="w-7 h-7 flex items-center justify-center rounded-lg transition-all"
              :class="[
                getUserVote(comment) === 1 ? 'text-orange-500' : 'text-slate-300 dark:text-slate-600 hover:text-orange-400 dark:hover:text-orange-400 hover:bg-orange-50 dark:hover:bg-slate-700',
                currentUserId === comment.author?.id ? 'opacity-40 cursor-not-allowed' : ''
              ]"
              :title="currentUserId === comment.author?.id ? 'Ne možete glasati za sebe' : 'Upvote'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
                <path d="M7.493 18.75c-.425 0-.82-.236-.975-.632A7.48 7.48 0 0 1 6 15.375c0-1.75.599-3.358 1.602-4.634.151-.192.373-.309.6-.397.473-.183.89-.514 1.212-.924a9.042 9.042 0 0 1 2.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 0 0 .322-1.672V3a.75.75 0 0 1 .75-.75 2.25 2.25 0 0 1 2.25 2.25c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 0 1-2.649 7.521c-.388.482-.987.729-1.605.729H14.23c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 0 0-1.423-.23h-.777ZM2.331 10.727a11.969 11.969 0 0 0-.831 4.398 12 12 0 0 0 .52 3.507C2.28 19.482 3.105 20.25 4.105 20.25H4.5c.395 0 .786-.04 1.167-.114.098-.018.192-.074.252-.15.06-.076.088-.174.088-.274V9.75a.75.75 0 0 0-.75-.75h-.765c-.782 0-1.5.432-1.961 1.077-.107.148-.197.306-.27.47Z" />
              </svg>
            </button>
            <span class="text-xs font-bold tabular-nums text-orange-500">{{ getLikesCount(comment) }}</span>

            <button
              @click="handleVote(comment, -1)"
              :disabled="currentUserId === comment.author?.id"
              class="w-7 h-7 flex items-center justify-center rounded-lg transition-all"
              :class="[
                getUserVote(comment) === -1 ? 'text-slate-600 dark:text-slate-400' : 'text-slate-300 dark:text-slate-600 hover:text-slate-500 dark:hover:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-700',
                currentUserId === comment.author?.id ? 'opacity-40 cursor-not-allowed' : ''
              ]"
              :title="currentUserId === comment.author?.id ? 'Ne možete glasati za sebe' : 'Downvote'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4 rotate-180">
                <path d="M7.493 18.75c-.425 0-.82-.236-.975-.632A7.48 7.48 0 0 1 6 15.375c0-1.75.599-3.358 1.602-4.634.151-.192.373-.309.6-.397.473-.183.89-.514 1.212-.924a9.042 9.042 0 0 1 2.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 0 0 .322-1.672V3a.75.75 0 0 1 .75-.75 2.25 2.25 0 0 1 2.25 2.25c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 0 1-2.649 7.521c-.388.482-.987.729-1.605.729H14.23c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 0 0-1.423-.23h-.777ZM2.331 10.727a11.969 11.969 0 0 0-.831 4.398 12 12 0 0 0 .52 3.507C2.28 19.482 3.105 20.25 4.105 20.25H4.5c.395 0 .786-.04 1.167-.114.098-.018.192-.074.252-.15.06-.076.088-.174.088-.274V9.75a.75.75 0 0 0-.75-.75h-.765c-.782 0-1.5.432-1.961 1.077-.107.148-.197.306-.27.47Z" />
              </svg>
            </button>
            <span class="text-xs font-bold tabular-nums text-slate-400 dark:text-slate-500">{{ getDislikesCount(comment) }}</span>
          </div>

          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center flex-wrap gap-2 text-xs text-slate-400 dark:text-slate-500">
                <span class="w-5 h-5 rounded-full bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300 flex items-center justify-center font-bold text-[8px]">
                  {{ getInitials(comment.author?.full_name) }}
                </span>
                <strong class="text-slate-600 dark:text-slate-300">{{ comment.author?.full_name || 'Kolega' }}</strong>

                <span
                  v-if="comment.author?.role"
                  class="text-[10px] px-2 py-0.5 rounded border"
                  :class="getRoleBadgeClass(comment.author.role)"
                >
                  {{ comment.author.role }}
                </span>

                <span
                  v-if="comment.author?.title"
                  class="text-[10px] px-2 py-0.5 rounded border"
                  :class="getTierClass(comment.author.title)"
                >
                  Nivo {{ comment.author.level }} · {{ comment.author.title }} · {{ comment.author.reputation_points }} XP
                </span>

                <div v-if="comment.author?.medals && comment.author.medals.length" class="flex items-center gap-1 relative medals-dropdown-container">
                  <span
                    v-for="medal in comment.author.medals.slice(0, 3)"
                    :key="medal.code || medal.id"
                    class="text-base cursor-help transition-transform hover:scale-125 leading-none"
                    :title="parseMedal(medal).tooltip"
                  >
                    {{ parseMedal(medal).icon }}
                  </span>

                  <button
                    v-if="comment.author.medals.length > 3"
                    @click.stop="toggleMedalDropdown('c-' + comment.id)"
                    class="flex items-center gap-0.5 bg-slate-100 dark:bg-slate-600 hover:bg-slate-200 dark:hover:bg-slate-500 transition-colors text-[10px] px-1.5 py-0.5 rounded font-bold text-slate-600 dark:text-slate-200 ml-0.5 bg-transparent border-none cursor-pointer"
                  >
                    +{{ comment.author.medals.length - 3 }} <span>{{ openMedalDropdown === 'c-' + comment.id ? '▲' : '▼' }}</span>
                  </button>

                  <div
                    v-if="openMedalDropdown === 'c-' + comment.id && comment.author.medals.length > 3"
                    @click.stop
                    class="absolute top-full left-0 mt-1 bg-white dark:bg-slate-700 border border-gray-200 dark:border-slate-600 shadow-xl rounded-lg p-2.5 w-44 z-30"
                  >
                    <p class="text-[9px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-400 mb-2 border-b pb-1 border-slate-100 dark:border-slate-600">
                      Ostala priznanja
                    </p>
                    <div class="flex flex-wrap gap-1.5 max-h-32 overflow-y-auto">
                      <span
                        v-for="medal in comment.author.medals.slice(3)"
                        :key="medal.code || medal.id"
                        class="text-base cursor-help transition-transform hover:scale-125 p-1 rounded hover:bg-slate-50 dark:hover:bg-slate-600 leading-none"
                        :title="parseMedal(medal).tooltip"
                      >
                        {{ parseMedal(medal).icon }}
                      </span>
                    </div>
                  </div>
                </div>

                <span>•</span>
                <span>{{ formatDate(comment.created_at) }}</span>
                <span v-if="comment.is_best_answer" class="text-[10px] bg-yellow-100 dark:bg-yellow-950/60 text-yellow-700 dark:text-yellow-400 px-2 py-0.5 rounded-full font-bold border border-yellow-300 dark:border-yellow-800">
                  ✓ Najbolji odgovor
                </span>
              </div>

              <div class="flex items-center gap-1">
                <button
                  v-if="isTopicAuthor"
                  @click="handleBestAnswer(comment)"
                  class="w-7 h-7 flex items-center justify-center rounded-full transition-all"
                  :class="comment.is_best_answer ? 'text-yellow-500 hover:text-red-400' : 'text-slate-300 dark:text-slate-600 hover:text-yellow-500 dark:hover:text-yellow-400'"
                  :title="comment.is_best_answer ? 'Ukloni najbolji odgovor' : 'Označi kao najbolji odgovor'"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
                    <path fill-rule="evenodd" d="M10.788 3.21c.448-1.077 1.976-1.077 2.424 0l2.082 5.006 5.404.434c1.164.093 1.636 1.545.749 2.305l-4.117 3.527 1.257 5.273c.271 1.136-.964 2.033-1.96 1.425L12 18.354 7.373 21.18c-.996.608-2.231-.29-1.96-1.425l1.257-5.273-4.117-3.527c-.887-.76-.415-2.212.749-2.305l5.404-.434 2.082-5.005Z" clip-rule="evenodd" />
                  </svg>
                </button>

                <button
                  v-if="(currentUserId === comment.author?.id || isAdmin) && !comment.is_deleted"
                  @click="startEdit(comment)"
                  class="w-7 h-7 flex items-center justify-center rounded-full transition-all text-slate-300 dark:text-slate-600 hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-950/20"
                  title="Edituj komentar"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
                    <path d="M21.731 2.269a2.625 2.625 0 0 0-3.712 0l-1.157 1.157 3.712 3.712 1.157-1.157a2.625 2.625 0 0 0 0-3.712ZM19.513 8.199l-3.712-3.712-8.4 8.4a5.25 5.25 0 0 0-1.32 2.214l-.8 2.685a.75.75 0 0 0 .933.933l2.685-.8a5.25 5.25 0 0 0 2.214-1.32l8.4-8.4Z" />
                    <path d="M5.25 5.25a3 3 0 0 0-3 3v10.5a3 3 0 0 0 3 3h10.5a3 3 0 0 0 3-3V13.5a.75.75 0 0 0-1.5 0v5.25a1.5 1.5 0 0 1-1.5 1.5H5.25a1.5 1.5 0 0 1-1.5-1.5V8.25a1.5 1.5 0 0 1 1.5-1.5h5.25a.75.75 0 0 0 0-1.5H5.25Z" />
                  </svg>
                </button>

                <button
                  v-if="currentUserId === comment.author?.id || isAdmin"
                  @click="handleDeleteComment(comment)"
                  class="w-7 h-7 flex items-center justify-center rounded-full transition-all text-slate-300 dark:text-slate-600 hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/20"
                  :title="isAdmin ? 'Admin: Obriši komentar' : 'Obriši komentar'"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
                    <path fill-rule="evenodd" d="M16.5 4.478v.227a48.816 48.816 0 0 1 3.878.512.75.75 0 1 1-.256 1.478l-.209-.035-1.005 13.07a3 3 0 0 1-2.991 2.77H8.084a3 3 0 0 1-2.991-2.77L4.087 6.66l-.209.035a.75.75 0 0 1-.256-1.478A48.567 48.567 0 0 1 7.5 4.705v-.227c0-1.564 1.213-2.9 2.816-2.951a52.662 52.662 0 0 1 3.369 0c1.603.051 2.815 1.387 2.815 2.951Zm-6.136-1.452a51.196 51.196 0 0 1 3.273 0C14.39 3.05 15 3.684 15 4.478v.113a49.488 49.488 0 0 0-6 0v-.113c0-.794.609-1.428 1.364-1.452Zm-.355 5.945a.75.75 0 1 0-1.5.058l.347 9a.75.75 0 1 0 1.499-.058l-.346-9Zm5.48.058a.75.75 0 1 0-1.498-.058l-.347 9a.75.75 0 0 0 1.5.058l.345-9Z" clip-rule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>

            <div v-if="comment.is_deleted" class="text-slate-400 dark:text-slate-500 text-sm italic">
              deleted by user
            </div>

            <div v-else-if="editingCommentId === comment.id">
              <textarea
                v-model="editContent"
                class="w-full text-sm border border-gray-200 dark:border-slate-600 rounded-lg p-3 bg-white dark:bg-slate-700 text-slate-700 dark:text-slate-300 focus:outline-none focus:ring-2 focus:ring-orange-400 resize-none"
                rows="3"
              />
              <div class="flex gap-2 mt-2">
                <button @click="submitEdit(comment)" class="px-3 py-1.5 bg-orange-500 hover:bg-orange-400 text-white text-xs font-bold rounded-lg transition-colors">
                  Sačuvaj
                </button>
                <button @click="cancelEdit()" class="px-3 py-1.5 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-600 text-slate-500 text-xs rounded-lg hover:bg-gray-50 transition-colors">
                  Otkaži
                </button>
              </div>
            </div>

            <p v-else class="text-slate-700 dark:text-slate-300 leading-relaxed text-sm whitespace-pre-line">{{ comment.content }}</p>

            <!-- Reply dugme — sakriveno za admin -->
            <div class="mt-2">
              <button
                v-if="canReply && !comment.is_deleted"
                @click="startReply(comment)"
                class="text-xs text-slate-400 hover:text-orange-500 transition-colors font-medium"
              >
                ↩ Odgovori
              </button>
            </div>

            <div v-if="replyingToId === comment.id" class="mt-3">
              <textarea
                v-model="replyContent"
                placeholder="Napišite odgovor..."
                class="w-full text-sm border border-gray-200 dark:border-slate-600 rounded-lg p-3 bg-white dark:bg-slate-700 text-slate-700 dark:text-slate-300 focus:outline-none focus:ring-2 focus:ring-orange-400 resize-none"
                rows="3"
              />
              <div class="flex gap-2 mt-2">
                <button @click="submitReply(comment, props.topicId)" class="px-3 py-1.5 bg-orange-500 hover:bg-orange-400 text-white text-xs font-bold rounded-lg transition-colors">
                  Pošalji
                </button>
                <button @click="cancelReply()" class="px-3 py-1.5 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-600 text-slate-500 text-xs rounded-lg hover:bg-gray-50 transition-colors">
                  Otkaži
                </button>
              </div>
            </div>

            <!-- Replies -->
            <div v-if="comment.replies && comment.replies.length > 0" class="mt-4 space-y-3 pl-6 border-l-2 border-gray-100 dark:border-slate-700">
              <div
                v-for="reply in comment.replies"
                :key="reply.id"
                class="bg-slate-50 dark:bg-slate-700/50 rounded-xl border border-gray-200 dark:border-slate-600 p-4 flex gap-3"
              >
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center flex-wrap gap-2 text-xs text-slate-400 dark:text-slate-500">
                      <span class="w-5 h-5 rounded-full bg-slate-200 dark:bg-slate-600 text-slate-600 dark:text-slate-300 flex items-center justify-center font-bold text-[8px]">
                        {{ getInitials(reply.author?.full_name) }}
                      </span>
                      <strong class="text-slate-600 dark:text-slate-300">{{ reply.author?.full_name || 'Kolega' }}</strong>

                      <span
                        v-if="reply.author?.role"
                        class="text-[10px] px-2 py-0.5 rounded border"
                        :class="getRoleBadgeClass(reply.author.role)"
                      >
                        {{ reply.author.role }}
                      </span>

                      <span
                        v-if="reply.author?.title"
                        class="text-[10px] px-2 py-0.5 rounded border"
                        :class="getTierClass(reply.author.title)"
                      >
                        Nivo {{ reply.author.level }} · {{ reply.author.title }} · {{ reply.author.reputation_points }} XP
                      </span>

                      <div v-if="reply.author?.medals && reply.author.medals.length" class="flex items-center gap-1 relative medals-dropdown-container">
                        <span
                          v-for="medal in reply.author.medals.slice(0, 3)"
                          :key="medal.code || medal.id"
                          class="text-base cursor-help transition-transform hover:scale-125 leading-none"
                          :title="parseMedal(medal).tooltip"
                        >
                          {{ parseMedal(medal).icon }}
                        </span>

                        <button
                          v-if="reply.author.medals.length > 3"
                          @click.stop="toggleMedalDropdown('r-' + reply.id)"
                          class="flex items-center gap-0.5 bg-slate-100 dark:bg-slate-600 hover:bg-slate-200 dark:hover:bg-slate-500 transition-colors text-[10px] px-1.5 py-0.5 rounded font-bold text-slate-600 dark:text-slate-200 ml-0.5 bg-transparent border-none cursor-pointer"
                        >
                          +{{ reply.author.medals.length - 3 }} <span>{{ openMedalDropdown === 'r-' + reply.id ? '▲' : '▼' }}</span>
                        </button>

                        <div
                          v-if="openMedalDropdown === 'r-' + reply.id && reply.author.medals.length > 3"
                          @click.stop
                          class="absolute top-full left-0 mt-1 bg-white dark:bg-slate-700 border border-gray-200 dark:border-slate-600 shadow-xl rounded-lg p-2.5 w-44 z-30"
                        >
                          <p class="text-[9px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-400 mb-2 border-b pb-1 border-slate-100 dark:border-slate-600">
                            Ostala priznanja
                          </p>
                          <div class="flex flex-wrap gap-1.5 max-h-32 overflow-y-auto">
                            <span
                              v-for="medal in reply.author.medals.slice(3)"
                              :key="medal.code || medal.id"
                              class="text-base cursor-help transition-transform hover:scale-125 p-1 rounded hover:bg-slate-50 dark:hover:bg-slate-600 leading-none"
                              :title="parseMedal(medal).tooltip"
                            >
                              {{ parseMedal(medal).icon }}
                            </span>
                          </div>
                        </div>
                      </div>

                      <span>•</span>
                      <span>{{ formatDate(reply.created_at) }}</span>
                    </div>

                    <div class="flex items-center gap-1">
                      <button
                        v-if="(currentUserId === reply.author?.id || isAdmin) && !reply.is_deleted"
                        @click="startEdit(reply)"
                        class="w-6 h-6 flex items-center justify-center rounded-full transition-all text-slate-300 dark:text-slate-600 hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-950/20"
                        title="Edituj"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-3 h-3">
                          <path d="M21.731 2.269a2.625 2.625 0 0 0-3.712 0l-1.157 1.157 3.712 3.712 1.157-1.157a2.625 2.625 0 0 0 0-3.712ZM19.513 8.199l-3.712-3.712-8.4 8.4a5.25 5.25 0 0 0-1.32 2.214l-.8 2.685a.75.75 0 0 0 .933.933l2.685-.8a5.25 5.25 0 0 0 2.214-1.32l8.4-8.4Z" />
                          <path d="M5.25 5.25a3 3 0 0 0-3 3v10.5a3 3 0 0 0 3 3h10.5a3 3 0 0 0 3-3V13.5a.75.75 0 0 0-1.5 0v5.25a1.5 1.5 0 0 1-1.5 1.5H5.25a1.5 1.5 0 0 1-1.5-1.5V8.25a1.5 1.5 0 0 1 1.5-1.5h5.25a.75.75 0 0 0 0-1.5H5.25Z" />
                        </svg>
                      </button>
                      <button
                        v-if="currentUserId === reply.author?.id || isAdmin"
                        @click="handleDeleteComment(reply)"
                        class="w-6 h-6 flex items-center justify-center rounded-full transition-all text-slate-300 dark:text-slate-600 hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/20"
                        title="Obriši"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-3 h-3">
                          <path fill-rule="evenodd" d="M16.5 4.478v.227a48.816 48.816 0 0 1 3.878.512.75.75 0 1 1-.256 1.478l-.209-.035-1.005 13.07a3 3 0 0 1-2.991 2.77H8.084a3 3 0 0 1-2.991-2.77L4.087 6.66l-.209.035a.75.75 0 0 1-.256-1.478A48.567 48.567 0 0 1 7.5 4.705v-.227c0-1.564 1.213-2.9 2.816-2.951a52.662 52.662 0 0 1 3.369 0c1.603.051 2.815 1.387 2.815 2.951Zm-6.136-1.452a51.196 51.196 0 0 1 3.273 0C14.39 3.05 15 3.684 15 4.478v.113a49.488 49.488 0 0 0-6 0v-.113c0-.794.609-1.428 1.364-1.452Zm-.355 5.945a.75.75 0 1 0-1.5.058l.347 9a.75.75 0 1 0 1.499-.058l-.346-9Zm5.48.058a.75.75 0 1 0-1.498-.058l-.347 9a.75.75 0 0 0 1.5.058l.345-9Z" clip-rule="evenodd" />
                        </svg>
                      </button>
                    </div>
                  </div>

                  <div v-if="reply.is_deleted" class="text-slate-400 dark:text-slate-500 text-sm italic">
                    deleted by user
                  </div>
                  <div v-else-if="editingCommentId === reply.id">
                    <textarea
                      v-model="editContent"
                      class="w-full text-sm border border-gray-200 dark:border-slate-600 rounded-lg p-3 bg-white dark:bg-slate-700 text-slate-700 dark:text-slate-300 focus:outline-none focus:ring-2 focus:ring-orange-400 resize-none"
                      rows="3"
                    />
                    <div class="flex gap-2 mt-2">
                      <button @click="submitEdit(reply)" class="px-3 py-1.5 bg-orange-500 hover:bg-orange-400 text-white text-xs font-bold rounded-lg transition-colors">
                        Sačuvaj
                      </button>
                      <button @click="cancelEdit()" class="px-3 py-1.5 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-600 text-slate-500 text-xs rounded-lg hover:bg-gray-50 transition-colors">
                        Otkaži
                      </button>
                    </div>
                  </div>
                  <p v-else class="text-slate-700 dark:text-slate-300 leading-relaxed text-sm whitespace-pre-line">{{ reply.content }}</p>

                  <!-- Reply na reply — sakriveno za admin -->
                  <div class="mt-2">
                    <button
                      v-if="canReply && !reply.is_deleted"
                      @click="startReply(reply)"
                      class="text-xs text-slate-400 hover:text-orange-500 transition-colors font-medium"
                    >
                      ↩ Odgovori
                    </button>
                  </div>

                  <div v-if="replyingToId === reply.id" class="mt-3">
                    <textarea
                      v-model="replyContent"
                      placeholder="Napišite odgovor..."
                      class="w-full text-sm border border-gray-200 dark:border-slate-600 rounded-lg p-3 bg-white dark:bg-slate-700 text-slate-700 dark:text-slate-300 focus:outline-none focus:ring-2 focus:ring-orange-400 resize-none"
                      rows="3"
                    />
                    <div class="flex gap-2 mt-2">
                      <button @click="submitReply(reply, props.topicId)" class="px-3 py-1.5 bg-orange-500 hover:bg-orange-400 text-white text-xs font-bold rounded-lg transition-colors">
                        Pošalji
                      </button>
                      <button @click="cancelReply()" class="px-3 py-1.5 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-600 text-slate-500 text-xs rounded-lg hover:bg-gray-50 transition-colors">
                        Otkaži
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </template>

      <div v-if="comments.length === 0" class="text-center py-8 text-slate-400 dark:text-slate-500 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 shadow-sm">
        Još nema odgovora. Budite prvi!
      </div>
    </div>
  </div>
</template>