<script setup>
import { ref, computed, onMounted } from 'vue';
import { voteOnComment, toggleBestAnswer, deleteComment } from '../services/forum';

const props = defineProps({
  comments: { type: Array, required: true },
  topicAuthorId: { type: Number, default: null },
});

const emit = defineEmits(['refresh']);

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
  } catch (e) {
    console.warn('Nije moguće dohvatiti korisnika.');
  }
});

const isTopicAuthor = computed(() => {
  return currentUserId.value && props.topicAuthorId && currentUserId.value === props.topicAuthorId;
});

const localVotes = ref({});

function getUserVote(comment) {
  if (localVotes.value[comment.id] !== undefined) return localVotes.value[comment.id];
  return comment.user_vote || 0;
}

function getLikesCount(comment) {
  const currentVote = localVotes.value[comment.id];
  if (currentVote === undefined) return comment.likes_count || 0;
  const previousVote = comment.user_vote || 0;
  let count = comment.likes_count || 0;
  if (previousVote === 1 && currentVote !== 1) count--;
  if (previousVote !== 1 && currentVote === 1) count++;
  return Math.max(0, count);
}

function getDislikesCount(comment) {
  const currentVote = localVotes.value[comment.id];
  if (currentVote === undefined) return comment.dislikes_count || 0;
  const previousVote = comment.user_vote || 0;
  let count = comment.dislikes_count || 0;
  if (previousVote === -1 && currentVote !== -1) count--;
  if (previousVote !== -1 && currentVote === -1) count++;
  return Math.max(0, count);
}

async function handleVote(comment, value) {
  if (!currentUserId.value) return alert('Morate biti prijavljeni da biste glasali.');
  const previousVote = getUserVote(comment);
  localVotes.value[comment.id] = previousVote === value ? 0 : value;
  try {
    const result = await voteOnComment(comment.id, value);
    localVotes.value[comment.id] = result.user_vote;
  } catch (e) {
    localVotes.value[comment.id] = previousVote;
    alert('Greška pri glasanju.');
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
  <div class="mb-6">
    <h2 class="text-lg font-semibold text-slate-700 dark:text-slate-200 mb-4">
      {{ comments.length }} {{ comments.length === 1 ? 'Odgovor' : 'Odgovora' }}
    </h2>

    <div class="space-y-4">
      <div
        v-for="comment in comments"
        :key="comment.id"
        class="bg-white dark:bg-slate-800 rounded-xl border p-5 flex gap-4 transition-all"
        :class="comment.is_best_answer ? 'border-yellow-300 dark:border-yellow-600 bg-yellow-50/30 dark:bg-yellow-950/20' : 'border-gray-200 dark:border-slate-700 shadow-sm'"
      >
        <div class="flex flex-col items-center gap-0.5 flex-shrink-0 pt-1">
          <button
            @click="handleVote(comment, 1)"
            class="w-7 h-7 flex items-center justify-center rounded-lg transition-all"
            :class="getUserVote(comment) === 1 ? 'text-orange-500' : 'text-slate-300 dark:text-slate-600 hover:text-orange-400 dark:hover:text-orange-400 hover:bg-orange-50 dark:hover:bg-slate-700'"
            title="Upvote"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
              <path d="M7.493 18.75c-.425 0-.82-.236-.975-.632A7.48 7.48 0 0 1 6 15.375c0-1.75.599-3.358 1.602-4.634.151-.192.373-.309.6-.397.473-.183.89-.514 1.212-.924a9.042 9.042 0 0 1 2.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 0 0 .322-1.672V3a.75.75 0 0 1 .75-.75 2.25 2.25 0 0 1 2.25 2.25c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 0 1-2.649 7.521c-.388.482-.987.729-1.605.729H14.23c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 0 0-1.423-.23h-.777ZM2.331 10.727a11.969 11.969 0 0 0-.831 4.398 12 12 0 0 0 .52 3.507C2.28 19.482 3.105 20.25 4.105 20.25H4.5c.395 0 .786-.04 1.167-.114.098-.018.192-.074.252-.15.06-.076.088-.174.088-.274V9.75a.75.75 0 0 0-.75-.75h-.765c-.782 0-1.5.432-1.961 1.077-.107.148-.197.306-.27.47Z" />
            </svg>
          </button>
          <span class="text-xs font-bold tabular-nums text-orange-500">{{ getLikesCount(comment) }}</span>

          <button
            @click="handleVote(comment, -1)"
            class="w-7 h-7 flex items-center justify-center rounded-lg transition-all"
            :class="getUserVote(comment) === -1 ? 'text-slate-600 dark:text-slate-400' : 'text-slate-300 dark:text-slate-600 hover:text-slate-500 dark:hover:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-700'"
            title="Downvote"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4 rotate-180">
              <path d="M7.493 18.75c-.425 0-.82-.236-.975-.632A7.48 7.48 0 0 1 6 15.375c0-1.75.599-3.358 1.602-4.634.151-.192.373-.309.6-.397.473-.183.89-.514 1.212-.924a9.042 9.042 0 0 1 2.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 0 0 .322-1.672V3a.75.75 0 0 1 .75-.75 2.25 2.25 0 0 1 2.25 2.25c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 0 1-2.649 7.521c-.388.482-.987.729-1.605.729H14.23c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 0 0-1.423-.23h-.777ZM2.331 10.727a11.969 11.969 0 0 0-.831 4.398 12 12 0 0 0 .52 3.507C2.28 19.482 3.105 20.25 4.105 20.25H4.5c.395 0 .786-.04 1.167-.114.098-.018.192-.074.252-.15.06-.076.088-.174.088-.274V9.75a.75.75 0 0 0-.75-.75h-.765c-.782 0-1.5.432-1.961 1.077-.107.148-.197.306-.27.47Z" />
            </svg>
          </button>
          <span class="text-xs font-bold tabular-nums text-slate-400 dark:text-slate-500">{{ getDislikesCount(comment) }}</span>
        </div>

        <div class="flex-1 min-w-0">
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center gap-2 text-xs text-slate-400 dark:text-slate-500">
              <span class="w-5 h-5 rounded-full bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300 flex items-center justify-center font-bold text-[8px]">
                {{ getInitials(comment.author?.full_name) }}
              </span>
              <strong class="text-slate-600 dark:text-slate-300">{{ comment.author?.full_name || 'Kolega' }}</strong>
              <span>•</span>
              <span>{{ formatDate(comment.created_at) }}</span>
              <span 
                v-if="comment.is_best_answer"
                class="text-[10px] bg-yellow-100 dark:bg-yellow-950 text-yellow-700 dark:text-yellow-400 px-2 py-0.5 rounded-full font-bold border border-yellow-200 dark:border-yellow-900"
              >
                ✓ Najbolji odgovor
              </span>
            </div>
            <div class="flex flex-col items-center gap-1">
              <button
                v-if="isTopicAuthor"
                @click="handleBestAnswer(comment)"
                class="w-7 h-7 flex items-center justify-center rounded-full transition-all"
                :class="comment.is_best_answer ? 'text-yellow-400 hover:text-red-400' : 'text-slate-300 dark:text-slate-600 hover:text-yellow-400 dark:hover:text-yellow-500'"
                :title="comment.is_best_answer ? 'Ukloni najbolji odgovor' : 'Označi kao najbolji odgovor'"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
                  <path fill-rule="evenodd" d="M10.788 3.21c.448-1.077 1.976-1.077 2.424 0l2.082 5.006 5.404.434c1.164.093 1.636 1.545.749 2.305l-4.117 3.527 1.257 5.273c.271 1.136-.964 2.033-1.96 1.425L12 18.354 7.373 21.18c-.996.608-2.231-.29-1.96-1.425l1.257-5.273-4.117-3.527c-.887-.76-.415-2.212.749-2.305l5.404-.434 2.082-5.005Z" clip-rule="evenodd" />
                </svg>
              </button>
              <button
                v-if="currentUserId === comment.author?.id"
                @click="handleDeleteComment(comment)"
                class="w-7 h-7 flex items-center justify-center rounded-full transition-all text-slate-300 dark:text-slate-600 hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/20"
                title="Obriši komentar"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
                  <path fill-rule="evenodd" d="M16.5 4.478v.227a48.816 48.816 0 0 1 3.878.512.75.75 0 1 1-.256 1.478l-.209-.035-1.005 13.07a3 3 0 0 1-2.991 2.77H8.084a3 3 0 0 1-2.991-2.77L4.087 6.66l-.209.035a.75.75 0 0 1-.256-1.478A48.567 48.567 0 0 1 7.5 4.705v-.227c0-1.564 1.213-2.9 2.816-2.951a52.662 52.662 0 0 1 3.369 0c1.603.051 2.815 1.387 2.815 2.951Zm-6.136-1.452a51.196 51.196 0 0 1 3.273 0C14.39 3.05 15 3.684 15 4.478v.113a49.488 49.488 0 0 0-6 0v-.113c0-.794.609-1.428 1.364-1.452Zm-.355 5.945a.75.75 0 1 0-1.5.058l.347 9a.75.75 0 1 0 1.499-.058l-.346-9Zm5.48.058a.75.75 0 1 0-1.498-.058l-.347 9a.75.75 0 0 0 1.5.058l.345-9Z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
          <p class="text-slate-700 dark:text-slate-300 leading-relaxed text-sm whitespace-pre-line">{{ comment.content }}</p>
        </div>

      </div>

      <div v-if="comments.length === 0" class="text-center py-8 text-slate-400 dark:text-slate-500 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 shadow-sm">
        Još nema odgovora. Budite prvi!
      </div>
    </div>
  </div>
</template>