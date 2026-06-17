<script setup>
import { ref, computed, onMounted } from 'vue';
import { voteOnComment, toggleBestAnswer, deleteComment, updateComment, createComment } from '../services/forum';
import ForumAvatar from './ForumAvatar.vue';
import ForumCommentNode from './ForumCommentNode.vue';
import { uploadCommentAttachments } from '../services/forum';

const props = defineProps({
  comments: { type: Array, required: true },
  topicAuthorId: { type: Number, default: null },
  topicId: { type: Number, default: null }
});

const emit = defineEmits(['refresh']);

// ── Search ────────────────────────────────────────────────────────────────────
const searchQuery = ref('');

const filteredComments = computed(() => {
  if (!searchQuery.value.trim()) return props.comments;
  
  const query = searchQuery.value.toLowerCase().trim();
  
  return props.comments.filter(comment => {
    const contentMatch = comment.content?.toLowerCase().includes(query);
    return contentMatch;
  });
}); 

// ─── Trenutni korisnik ────────────────────────────────────────────────────────
const currentUserId = ref(null);
const currentUserRole = ref(null);

const replyFiles = ref({}); 

onMounted(async () => {
  try {
    const token = localStorage.getItem('token') || localStorage.getItem('access_token');
    if (!token) return;
    const res = await fetch('http://127.0.0.1:8000/me', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (res.ok) {
      const data = await res.json();
      currentUserId.value = data.id;
      currentUserRole.value = data.role;
    }
  } catch (e) {
    console.warn('Nije moguće dohvatiti korisnika.');
  }
});

const isAdmin = computed(() => currentUserRole.value === 'admin');
const isTopicAuthor = computed(() =>
  !!(currentUserId.value && props.topicAuthorId && currentUserId.value === props.topicAuthorId)
);

// Admin ne može odgovarati na komentare (iz forum-main)
const canReply = computed(() => !!currentUserId.value && !isAdmin.value);

// ─── Reaktivno stanje glasova ─────────────────────────────────────────────────
const serverVoteState = ref({});

function getUserVote(comment) {
  return serverVoteState.value[comment.id]?.user_vote ?? comment.user_vote ?? 0;
}
function getLikesCount(comment) {
  return serverVoteState.value[comment.id]?.likes_count ?? comment.likes_count ?? 0;
}
function getDislikesCount(comment) {
  return serverVoteState.value[comment.id]?.dislikes_count ?? comment.dislikes_count ?? 0;
}

// ─── Dropdown za medalje ──────────────────────────────────────────────────────
const openMedalDropdown = ref(null);
function toggleMedalDropdown(key) {
  openMedalDropdown.value = openMedalDropdown.value === key ? null : key;
}
function closeMedalDropdown() {
  openMedalDropdown.value = null;
}

// ─── Edit ─────────────────────────────────────────────────────────────────────
const editingCommentId = ref(null);
const editContent = ref('');

function handleStartEdit(commentId) {
  const comment = findCommentById(props.comments, commentId);
  if (!comment) return;
  editingCommentId.value = commentId;
  editContent.value = comment.content;
}

function handleCancelEdit() {
  editingCommentId.value = null;
  editContent.value = '';
}

function handleReplyFiles(commentId, files) {
  replyFiles.value[commentId] = files;
}

async function handleSubmitReply(comment, replyText) {
  if (!replyText?.trim()) return;
  try {
    const newComment = await createComment({
      content: replyText.trim(),
      topic_id: props.topicId,
      parent_id: comment.id
    });

    // Upload fajlova ako ih ima
    const files = replyFiles.value[comment.id];
    if (files && files.length > 0) {
      await uploadCommentAttachments(newComment.id, files);
      delete replyFiles.value[comment.id];
    }

    replyingToId.value = null;
    emit('refresh');
  } catch (e) {
    alert('Greška pri slanju odgovora.');
  }
}

// ─── Reply ────────────────────────────────────────────────────────────────────
const replyingToId = ref(null);

function handleStartReply(commentId) {
  replyingToId.value = commentId;
}

function handleCancelReply() {
  replyingToId.value = null;
}

async function handleSubmitReply(comment, replyText) {
  if (!replyText?.trim()) return;
  try {
    await createComment({
      content: replyText.trim(),
      topic_id: props.topicId,
      parent_id: comment.id
    });
    replyingToId.value = null;
    emit('refresh');
  } catch (e) {
    alert('Greška pri slanju odgovora.');
  }
}

// ─── Vote ─────────────────────────────────────────────────────────────────────
async function handleVote(comment, value) {
  if (!currentUserId.value) return alert('Morate biti prijavljeni da biste glasali.');
  if (currentUserId.value === comment.author?.id) return alert('Ne možete glasati za vlastiti komentar.');
  try {
    const result = await voteOnComment(comment.id, value);
    serverVoteState.value[comment.id] = {
      user_vote: result.user_vote,
      likes_count: result.likes_count ?? (comment.likes_count + (result.user_vote === 1 ? 1 : 0)),
      dislikes_count: result.dislikes_count ?? (comment.dislikes_count + (result.user_vote === -1 ? 1 : 0))
    };
    emit('refresh');
  } catch (e) {
    alert(e.response?.data?.detail || 'Greška pri glasanju ili je dostignut dnevni limit.');
  }
}

// ─── Best answer ──────────────────────────────────────────────────────────────
async function handleBestAnswer(comment) {
  if (!isTopicAuthor.value) return;
  try {
    await toggleBestAnswer(comment.id);
    emit('refresh');
  } catch (e) {
    alert('Greška pri označavanju najboljeg odgovora.');
  }
}

// ─── Delete ───────────────────────────────────────────────────────────────────
async function handleDeleteComment(comment) {
  if (!confirm('Da li ste sigurni da želite obrisati ovaj komentar?')) return;
  try {
    await deleteComment(comment.id);
    emit('refresh');
  } catch (e) {
    alert('Greška pri brisanju komentara.');
  }
}

// ─── Helpers ──────────────────────────────────────────────────────────────────
function findCommentById(nodes, id) {
  for (const node of nodes) {
    if (node.id === id) return node;
    if (node.replies?.length) {
      const found = findCommentById(node.replies, id);
      if (found) return found;
    }
  }
  return null;
}

function getInitials(fullName) {
  if (!fullName) return '?';
  return fullName.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
}

function formatDate(dateValue) {
  if (!dateValue) return '';
  return new Intl.DateTimeFormat('bs-BA', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  }).format(new Date(dateValue));
}
</script>

<template>
  <div class="mb-6" @click="closeMedalDropdown">
    <div class="flex items-center justify-between mb-4 gap-4">
      <h2 class="text-lg font-semibold text-slate-700 dark:text-slate-200 whitespace-nowrap">
        {{ filteredComments.length }} {{ filteredComments.length === 1 ? 'Odgovor' : 'Odgovora' }}
      </h2>

      <div class="relative w-full max-w-xs">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Pretraži odgovore..."
          class="w-full text-xs bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 rounded-lg pl-8 pr-8 py-1.5 focus:outline-none focus:ring-2 focus:ring-orange-400 transition-colors"
        />
        <svg xmlns="http://www.w3.org/2000/svg" class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z" />
        </svg>
        <button
          v-if="searchQuery"
          @click="searchQuery = ''"
          class="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <div class="space-y-1">
      <template v-for="comment in filteredComments" :key="comment.id">

        <!-- ── Admin Notice ───────────────────── -->
        <div
          v-if="comment.is_admin_notice"
          class="rounded-xl border-2 border-red-400 dark:border-red-700 bg-red-50 dark:bg-red-950/30 p-5 flex gap-4 shadow-md ring-2 ring-red-300/30 dark:ring-red-800/30"
        >
          <div class="flex flex-col items-center justify-start pt-1 flex-shrink-0 w-7">
            <span class="text-2xl select-none">🛡️</span>
          </div>

          <div class="flex-1 min-w-0">
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

              <div class="flex items-center gap-1">
                <button
                  v-if="isAdmin && !comment.is_deleted"
                  @click="handleStartEdit(comment.id)"
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
                <button @click="handleSubmitEdit(comment.id, editContent)" class="px-3 py-1.5 bg-red-600 hover:bg-red-500 text-white text-xs font-bold rounded-lg transition-colors">
                  Sačuvaj
                </button>
                <button @click="handleCancelEdit()" class="px-3 py-1.5 bg-white dark:bg-slate-800 border border-red-200 dark:border-red-700 text-red-500 text-xs rounded-lg hover:bg-red-50 transition-colors">
                  Otkaži
                </button>
              </div>
            </div>
            <p v-else class="text-red-800 dark:text-red-300 leading-relaxed text-sm whitespace-pre-line font-medium">
              {{ comment.content }}
            </p>

            <p class="mt-2 text-[10px] text-red-400/60 dark:text-red-600/60 italic select-none">
              Nije dozvoljeno odgovarati na administratorska obavještenja.
            </p>
          </div>
        </div>

        <!-- ── Obični komentar → ForumCommentNode ──────────────── -->
        <ForumCommentNode
          v-else
          :comment="comment"
          :current-user-id="currentUserId"
          :is-admin="isAdmin"
          :is-topic-author="isTopicAuthor"
          :can-reply="canReply"
          :topic-id="topicId"
          :open-medal-dropdown="openMedalDropdown"
          :editing-comment-id="editingCommentId"
          :replying-to-id="replyingToId"
          :get-user-vote="getUserVote"
          :get-likes-count="getLikesCount"
          :get-dislikes-count="getDislikesCount"
          :depth="0"
          @vote="handleVote"
          @best-answer="handleBestAnswer"
          @delete="handleDeleteComment"
          @start-edit="handleStartEdit"
          @cancel-edit="handleCancelEdit"
          @submit-edit="handleSubmitEdit"
          @start-reply="handleStartReply"
          @cancel-reply="handleCancelReply"
          @submit-reply="handleSubmitReply"
          @toggle-medals="toggleMedalDropdown"
        />

      </template>

      <div
        v-if="filteredComments.length === 0"
        class="text-center py-8 text-slate-400 dark:text-slate-500 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 shadow-sm"
      >
        <span v-if="searchQuery">Nema komentara koji odgovaraju pretrazi "{{ searchQuery }}".</span>
        <span v-else>Još nema odgovora. Budite prvi!</span>
      </div>
    </div>
  </div>
</template>