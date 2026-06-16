<script setup>
import { ref, computed, onMounted } from 'vue';
import { voteOnComment, toggleBestAnswer, deleteComment, updateComment, createComment } from '../services/forum';
import ForumAvatar from './ForumAvatar.vue';
import ForumCommentNode from './ForumCommentNode.vue';

const props = defineProps({
  comments: { type: Array, required: true },
  topicAuthorId: { type: Number, default: null },
  topicId: { type: Number, default: null }
});

const emit = defineEmits(['refresh']);

// ─── Trenutni korisnik ────────────────────────────────────────────────────────
const currentUserId = ref(null);
const currentUserRole = ref(null);

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
  // Pronađi komentar po ID-u u cijelom stablu
  const comment = findCommentById(props.comments, commentId);
  if (!comment) return;
  editingCommentId.value = commentId;
  editContent.value = comment.content;
}

function handleCancelEdit() {
  editingCommentId.value = null;
  editContent.value = '';
}

async function handleSubmitEdit(commentId, newContent) {
  if (!newContent?.trim()) return;
  try {
    await updateComment(commentId, newContent.trim());
    editingCommentId.value = null;
    editContent.value = '';
    emit('refresh');
  } catch (e) {
    alert('Greška pri editovanju komentara.');
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

// ─── Pomoćna funkcija: pretraži stablo po ID-u ───────────────────────────────
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
    <h2 class="text-lg font-semibold text-slate-700 dark:text-slate-200 mb-4">
      {{ comments.length }} {{ comments.length === 1 ? 'Odgovor' : 'Odgovora' }}
    </h2>

    <div class="space-y-1">
      <template v-for="comment in comments" :key="comment.id">
        <!-- 
          Svaki root komentar prolazi kroz ForumCommentNode na depth=0.
          Node rekurzivno renderuje replies na depth+1.
          Svi eventi "plutaju" gore do ovog kontrolera.
        -->
        <ForumCommentNode
          :comment="comment"
          :current-user-id="currentUserId"
          :is-admin="isAdmin"
          :is-topic-author="isTopicAuthor"
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
        v-if="comments.length === 0"
        class="text-center py-8 text-slate-400 dark:text-slate-500 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 shadow-sm"
      >
        Još nema odgovora. Budite prvi!
      </div>
    </div>
  </div>
</template>