<script setup>
import { ref, computed } from 'vue';
import { voteOnComment, toggleBestAnswer } from '../services/forum';

const props = defineProps({
  comments: { type: Array, required: true },
  topicAuthorId: { type: Number, default: null }, // ← dodaj ovaj prop
});

const emit = defineEmits(['refresh']);

const currentUserId = computed(() => {
  const id = localStorage.getItem('user_id');
  return id ? parseInt(id) : null;
});

const isTopicAuthor = computed(() => {
  return currentUserId.value && props.topicAuthorId && currentUserId.value === props.topicAuthorId;
});

const localVotes = ref({});

function getUserVote(comment) {
  if (localVotes.value[comment.id] !== undefined) return localVotes.value[comment.id];
  return comment.user_vote || 0;
}

function getVotesCount(comment) {
  const diff = (localVotes.value[comment.id] || 0) - (comment.user_vote || 0);
  return (comment.votes_count || 0) + diff;
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
    <h2 class="text-lg font-semibold text-slate-700 mb-4">
      {{ comments.length }} {{ comments.length === 1 ? 'Odgovor' : 'Odgovora' }}
    </h2>

    <div class="space-y-4">
      <div
        v-for="comment in comments"
        :key="comment.id"
        class="bg-white rounded-xl border p-5 flex gap-4 transition-all"
        :class="comment.is_best_answer ? 'border-yellow-300 bg-yellow-50/30' : 'border-gray-200 shadow-sm'"
      >
        <!-- Voting lijevo - thumbs kao na Figmi -->
        <div class="flex flex-col items-center gap-1 flex-shrink-0 pt-1">
          <button
            @click="handleVote(comment, 1)"
            class="w-8 h-8 flex items-center justify-center rounded-lg transition-all"
            :class="getUserVote(comment) === 1 ? 'text-orange-500' : 'text-slate-300 hover:text-orange-400 hover:bg-orange-50'"
            title="Upvote"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
              <path d="M7.493 18.75c-.425 0-.82-.236-.975-.632A7.48 7.48 0 0 1 6 15.375c0-1.75.599-3.358 1.602-4.634.151-.192.373-.309.6-.397.473-.183.89-.514 1.212-.924a9.042 9.042 0 0 1 2.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 0 0 .322-1.672V3a.75.75 0 0 1 .75-.75 2.25 2.25 0 0 1 2.25 2.25c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 0 1-2.649 7.521c-.388.482-.987.729-1.605.729H14.23c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 0 0-1.423-.23h-.777ZM2.331 10.727a11.969 11.969 0 0 0-.831 4.398 12 12 0 0 0 .52 3.507C2.28 19.482 3.105 20.25 4.105 20.25H4.5c.395 0 .786-.04 1.167-.114.098-.018.192-.074.252-.15.06-.076.088-.174.088-.274V9.75a.75.75 0 0 0-.75-.75h-.765c-.782 0-1.5.432-1.961 1.077-.107.148-.197.306-.27.47Z" />
            </svg>
          </button>
          <span
            class="text-xs font-bold tabular-nums"
            :class="getVotesCount(comment) > 0 ? 'text-orange-500' : getVotesCount(comment) < 0 ? 'text-slate-500' : 'text-slate-400'"
          >{{ getVotesCount(comment) }}</span>
          <button
            @click="handleVote(comment, -1)"
            class="w-8 h-8 flex items-center justify-center rounded-lg transition-all"
            :class="getUserVote(comment) === -1 ? 'text-slate-600' : 'text-slate-300 hover:text-slate-500 hover:bg-slate-50'"
            title="Downvote"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5 rotate-180">
              <path d="M7.493 18.75c-.425 0-.82-.236-.975-.632A7.48 7.48 0 0 1 6 15.375c0-1.75.599-3.358 1.602-4.634.151-.192.373-.309.6-.397.473-.183.89-.514 1.212-.924a9.042 9.042 0 0 1 2.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 0 0 .322-1.672V3a.75.75 0 0 1 .75-.75 2.25 2.25 0 0 1 2.25 2.25c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 0 1-2.649 7.521c-.388.482-.987.729-1.605.729H14.23c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 0 0-1.423-.23h-.777ZM2.331 10.727a11.969 11.969 0 0 0-.831 4.398 12 12 0 0 0 .52 3.507C2.28 19.482 3.105 20.25 4.105 20.25H4.5c.395 0 .786-.04 1.167-.114.098-.018.192-.074.252-.15.06-.076.088-.174.088-.274V9.75a.75.75 0 0 0-.75-.75h-.765c-.782 0-1.5.432-1.961 1.077-.107.148-.197.306-.27.47Z" />
            </svg>
          </button>
        </div>

        <!-- Sadrzaj desno -->
        <div class="flex-1 min-w-0">
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center gap-2 text-xs text-slate-400">
              <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-600 flex items-center justify-center font-bold text-[8px]">
                {{ getInitials(comment.author?.full_name) }}
              </span>
              <strong class="text-slate-600">{{ comment.author?.full_name || 'Kolega' }}</strong>
              <span>•</span>
              <span>{{ formatDate(comment.created_at) }}</span>
            </div>
            <div class="flex items-center gap-2">
              <span v-if="comment.is_best_answer" class="text-[10px] bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded-full font-bold border border-yellow-200">
                ✓ Najbolji odgovor
              </span>
              <button
                v-if="isTopicAuthor"
                @click="handleBestAnswer(comment)"
                class="text-[10px] px-2 py-0.5 rounded-full font-semibold border transition-all"
                :class="comment.is_best_answer
                  ? 'bg-yellow-50 text-yellow-600 border-yellow-200 hover:bg-red-50 hover:text-red-500 hover:border-red-200'
                  : 'bg-white text-slate-400 border-gray-200 hover:bg-yellow-50 hover:text-yellow-600 hover:border-yellow-200'"
              >{{ comment.is_best_answer ? '✓ Označen' : '☆ Označi' }}</button>
            </div>
          </div>
          <p class="text-slate-700 leading-relaxed text-sm whitespace-pre-line">{{ comment.content }}</p>
        </div>

      </div>

      <div v-if="comments.length === 0" class="text-center py-8 text-slate-400 bg-white rounded-xl border border-gray-200 shadow-sm">
        Još nema odgovora. Budite prvi!
      </div>
    </div>
  </div>
</template>