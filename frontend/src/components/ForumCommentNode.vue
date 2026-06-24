<script setup>
import { ref, computed } from 'vue';
import ForumAvatar from './ForumAvatar.vue';
import ForumAttachmentPreview from './ForumAttachmentPreview.vue';

defineOptions({ name: 'ForumCommentNode' })

const props = defineProps({
  comment:            { type: Object,   required: true },
  currentUserId:      { type: Number,   default: null },
  isAdmin:            { type: Boolean,  default: false },
  isTopicAuthor:      { type: Boolean,  default: false },
  canReply:           { type: Boolean,  default: false },
  topicId:            { type: Number,   default: null },
  openMedalDropdown:  { type: String,   default: null },
  editingCommentId:   { type: Number,   default: null },
  replyingToId:       { type: Number,   default: null },
  depth:              { type: Number,   default: 0 },
  getUserVote:        { type: Function, required: true },
  getLikesCount:      { type: Function, required: true },
  getDislikesCount:   { type: Function, required: true },
  activeHighlights:   { type: Object,   default: () => new Set() },
});

const emit = defineEmits([
  'vote', 'best-answer', 'delete',
  'start-edit', 'cancel-edit', 'submit-edit',
  'start-reply', 'cancel-reply', 'submit-reply',
  'toggle-medals'
]);

const replyContentLocal = ref('');
const editContentLocal  = ref('');
const replyFilesLocal   = ref([]);

const ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.pdf', '.docx', '.txt'];
const MAX_FILE_SIZE = 5 * 1024 * 1024;
const MAX_FILES = 3;

function handleReplyFileSelect(event) {
  const files = Array.from(event.target.files);
  for (const file of files) {
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(ext)) { alert(`Format ${ext} nije dozvoljen.`); return; }
    if (file.size > MAX_FILE_SIZE) { alert(`Fajl "${file.name}" je prevelik. Max 5 MB.`); return; }
  }
  if (replyFilesLocal.value.length + files.length > MAX_FILES) { alert('Maksimalno 3 fajla.'); return; }
  replyFilesLocal.value = [...replyFilesLocal.value, ...files];
}

const MAX_VISUAL_DEPTH = 3;
const shouldIndent = computed(() => props.depth > 0 && props.depth <= MAX_VISUAL_DEPTH);

const isHighlighted = computed(() => props.activeHighlights.has(props.comment.id));

const medalIcons = { gold: '🥇', silver: '🥈', bronze: '🥉' };
const medalThresholds = {
  best_answers:   { bronze: 1,   silver: 5,   gold: 15   },
  topics_started: { bronze: 3,   silver: 10,  gold: 25   },
  reputation:     { bronze: 100, silver: 500, gold: 1000 },
  night_owl:      { bronze: 1,   silver: 3,   gold: 10   }
};
const medalDetails = {
  best_answers:   { name: 'Najbolji odgovori',   desc: (n) => `Dobijate kada vaš odgovor bude označen kao najbolji ${n} ${n === 1 ? 'put' : 'puta'}.` },
  topics_started: { name: 'Pokrenute teme',       desc: (n) => `Dobijate kada pokrenete ${n} ${n === 1 ? 'temu' : 'tema'} na forumu.` },
  reputation:     { name: 'Ukupna reputacija',    desc: (n) => `Dobijate kada skupite ukupno ${n} XP reputacije.` },
  night_owl:      { name: 'Noćna ptica',          desc: (n) => `Tajna medalja — dobijate kada pokrenete ${n} ${n === 1 ? 'temu' : 'tema'} između 03:00 i 05:00h.` }
};

function parseMedal(medal) {
  if (!medal) return { icon: '🏅', tooltip: 'Medalja' };
  const icon    = medalIcons[medal.tier] || '🏅';
  const details = medalDetails[medal.category] || { name: medal.category_name || 'Priznanje', desc: () => '' };
  const prefix  = medal.tier === 'gold' ? 'Zlatna' : medal.tier === 'silver' ? 'Srebrna' : 'Bronzana';
  const threshold = medalThresholds[medal.category]?.[medal.tier];
  const fullName  = `${prefix} – ${details.name}`;
  const description = threshold != null ? details.desc(threshold) : '';
  return { icon, tooltip: description ? `${fullName}\n${description}` : fullName };
}

function getTierClass(title) {
  if (!title) return 'bg-slate-100 text-slate-600 border-slate-200 dark:bg-slate-700 dark:text-slate-300 dark:border-slate-600';
  const t = title.toLowerCase();
  if (t.includes('zlatni') || t.includes('expert') || t.includes('legenda'))
    return 'bg-amber-50 text-amber-700 border-amber-300 dark:bg-amber-950/40 dark:text-amber-400 dark:border-amber-800 font-bold';
  if (t.includes('srebrni') || t.includes('napredni') || t.includes('mentor'))
    return 'bg-slate-100 text-slate-700 border-slate-300 dark:bg-slate-700 dark:text-slate-300 dark:border-slate-600';
  return 'bg-orange-50 text-orange-700 border-orange-200 dark:bg-orange-950/30 dark:text-orange-400 dark:border-orange-900';
}

function getRoleBadgeClass(role) {
  if (!role) return 'bg-slate-100 text-slate-600 border-slate-200 dark:bg-slate-700 dark:text-slate-300 dark:border-slate-600';
  const r = role.toLowerCase();
  if (r === 'admin')
    return 'bg-red-50 text-red-700 border-red-300 dark:bg-red-950/40 dark:text-red-400 dark:border-red-800 font-bold';
  if (r === 'autor' || r === 'mentor')
    return 'bg-indigo-50 text-indigo-700 border-indigo-300 dark:bg-indigo-950/40 dark:text-indigo-400 dark:border-indigo-800';
  return 'bg-blue-50 text-blue-600 border-blue-200 dark:bg-blue-950/30 dark:text-blue-400 dark:border-blue-900';
}

function formatDate(dateValue) {
  if (!dateValue) return '';
  return new Intl.DateTimeFormat('bs-BA', {
    day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit'
  }).format(new Date(dateValue));
}

const medalKey = computed(() => `c-${props.comment.id}`);
</script>

<template>
  <div
    :class="[
      shouldIndent
        ? 'pl-4 border-l-2 border-gray-100 dark:border-slate-700 mt-2'
        : 'mt-3'
    ]"
  >
    <div
      :id="'comment-' + comment.id"
      class="bg-white dark:bg-slate-800 rounded-xl border p-4 flex gap-3 shadow-sm transition-all duration-700"
      :class="[
        isHighlighted
          ? 'border-yellow-400 dark:border-yellow-500 ring-2 ring-yellow-400/60 ring-offset-1 bg-yellow-50/60 dark:bg-yellow-950/20'
          : comment.is_best_answer
            ? 'border-yellow-400 dark:border-yellow-600 bg-yellow-50/40 dark:bg-yellow-950/20 ring-1 ring-yellow-400/30'
            : 'border-gray-200 dark:border-slate-700'
      ]"
    >
      <!-- Vote kolona -->
      <div class="flex flex-col items-center gap-0.5 flex-shrink-0 pt-1">
        <button
          @click="emit('vote', comment, 1)"
          :disabled="currentUserId === comment.author?.id || isAdmin === false"
          class="w-7 h-7 flex items-center justify-center rounded-lg transition-all"
          :class="[
            getUserVote(comment) === 1
              ? 'text-orange-500'
              : 'text-slate-300 dark:text-slate-600 hover:text-orange-400 hover:bg-orange-50 dark:hover:bg-slate-700',
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
          @click="emit('vote', comment, -1)"
          :disabled="currentUserId === comment.author?.id || isAdmin === false"
          class="w-7 h-7 flex items-center justify-center rounded-lg transition-all"
          :class="[
            getUserVote(comment) === -1
              ? 'text-slate-600 dark:text-slate-400'
              : 'text-slate-300 dark:text-slate-600 hover:text-slate-500 hover:bg-slate-50 dark:hover:bg-slate-700',
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
        <!-- Header -->
        <div class="flex items-center justify-between mb-2">
          <div class="flex items-center flex-wrap gap-2 text-xs text-slate-400 dark:text-slate-500">
            <ForumAvatar :author="comment.author" class="w-5 h-5 text-[8px]" />
            <strong class="text-slate-600 dark:text-slate-300">{{ comment.author?.full_name || 'Kolega' }}</strong>

            <span v-if="depth > 0 && comment.parent_author" class="text-slate-400 dark:text-slate-500">
              → <span class="text-orange-500 font-medium">@{{ comment.parent_author.full_name }}</span>
            </span>

            <span v-if="comment.author?.role" class="text-[10px] px-2 py-0.5 rounded border" :class="getRoleBadgeClass(comment.author.role)">
              {{ comment.author.role }}
            </span>
            <span v-if="comment.author?.title" class="text-[10px] px-2 py-0.5 rounded border" :class="getTierClass(comment.author.title)">
              Nivo {{ comment.author.level }} · {{ comment.author.title }} · {{ comment.author.reputation_points }} XP
            </span>

            <div v-if="comment.author?.medals?.length" class="flex items-center gap-1 relative medals-dropdown-container">
              <span
                v-for="medal in comment.author.medals.slice(0, 3)"
                :key="medal.code || medal.id"
                class="text-base cursor-help transition-transform hover:scale-125 leading-none"
                :title="parseMedal(medal).tooltip"
              >{{ parseMedal(medal).icon }}</span>

              <button
                v-if="comment.author.medals.length > 3"
                @click.stop="emit('toggle-medals', medalKey)"
                class="flex items-center gap-0.5 bg-slate-100 dark:bg-slate-600 hover:bg-slate-200 dark:hover:bg-slate-500 text-[10px] px-1.5 py-0.5 rounded font-bold text-slate-600 dark:text-slate-200 ml-0.5 border-none cursor-pointer"
              >+{{ comment.author.medals.length - 3 }} <span>{{ openMedalDropdown === medalKey ? '▲' : '▼' }}</span></button>

              <div
                v-if="openMedalDropdown === medalKey && comment.author.medals.length > 3"
                @click.stop
                class="absolute top-full left-0 mt-1 bg-white dark:bg-slate-700 border border-gray-200 dark:border-slate-600 shadow-xl rounded-lg p-2.5 w-44 z-30"
              >
                <p class="text-[9px] font-bold uppercase tracking-wider text-slate-400 mb-2 border-b pb-1 border-slate-100 dark:border-slate-600">Ostala priznanja</p>
                <div class="flex flex-wrap gap-1.5 max-h-32 overflow-y-auto">
                  <span
                    v-for="medal in comment.author.medals.slice(3)"
                    :key="medal.code || medal.id"
                    class="text-base cursor-help transition-transform hover:scale-125 p-1 rounded hover:bg-slate-50 dark:hover:bg-slate-600 leading-none"
                    :title="parseMedal(medal).tooltip"
                  >{{ parseMedal(medal).icon }}</span>
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
              v-if="isTopicAuthor && depth === 0"
              @click="emit('best-answer', comment)"
              class="w-7 h-7 flex items-center justify-center rounded-full transition-all"
              :class="comment.is_best_answer ? 'text-yellow-500 hover:text-red-400' : 'text-slate-300 dark:text-slate-600 hover:text-yellow-500'"
              :title="comment.is_best_answer ? 'Ukloni najbolji odgovor' : 'Označi kao najbolji odgovor'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
                <path fill-rule="evenodd" d="M10.788 3.21c.448-1.077 1.976-1.077 2.424 0l2.082 5.006 5.404.434c1.164.093 1.636 1.545.749 2.305l-4.117 3.527 1.257 5.273c.271 1.136-.964 2.033-1.96 1.425L12 18.354 7.373 21.18c-.996.608-2.231-.29-1.96-1.425l1.257-5.273-4.117-3.527c-.887-.76-.415-2.212.749-2.305l5.404-.434 2.082-5.005Z" clip-rule="evenodd" />
              </svg>
            </button>

            <button
              v-if="(currentUserId === comment.author?.id || isAdmin) && !comment.is_deleted"
              @click="editContentLocal = comment.content; emit('start-edit', comment.id)"
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
              @click="emit('delete', comment)"
              class="w-7 h-7 flex items-center justify-center rounded-full transition-all text-slate-300 dark:text-slate-600 hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/20"
              :title="isAdmin ? 'Admin: Obriši komentar' : 'Obriši komentar'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
                <path fill-rule="evenodd" d="M16.5 4.478v.227a48.816 48.816 0 0 1 3.878.512.75.75 0 1 1-.256 1.478l-.209-.035-1.005 13.07a3 3 0 0 1-2.991 2.77H8.084a3 3 0 0 1-2.991-2.77L4.087 6.66l-.209.035a.75.75 0 0 1-.256-1.478A48.567 48.567 0 0 1 7.5 4.705v-.227c0-1.564 1.213-2.9 2.816-2.951a52.662 52.662 0 0 1 3.369 0c1.603.051 2.815 1.387 2.815 2.951Zm-6.136-1.452a51.196 51.196 0 0 1 3.273 0C14.39 3.05 15 3.684 15 4.478v.113a49.488 49.488 0 0 0-6 0v-.113c0-.794.609-1.428 1.364-1.452Zm-.355 5.945a.75.75 0 1 0-1.5.058l.347 9a.75.75 0 1 0 1.499-.058l-.346-9Zm5.48.058a.75.75 0 1 0-1.498-.058l-.347 9a.75.75 0 0 0 1.5.058l.345-9Z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Sadržaj -->
        <div v-if="comment.is_deleted" class="text-slate-400 dark:text-slate-500 text-sm italic">
          deleted by user
        </div>

        <div v-else-if="editingCommentId === comment.id" class="mt-1">
          <textarea
            v-model="editContentLocal"
            class="w-full text-sm border border-gray-200 dark:border-slate-600 rounded-lg p-3 bg-white dark:bg-slate-700 text-slate-700 dark:text-slate-300 focus:outline-none focus:ring-2 focus:ring-orange-400 resize-none"
            rows="3"
          />
          <div class="flex gap-2 mt-2">
            <button @click="emit('submit-edit', comment.id, editContentLocal)" class="px-3 py-1.5 bg-orange-500 hover:bg-orange-400 text-white text-xs font-bold rounded-lg transition-colors">Sačuvaj</button>
            <button @click="emit('cancel-edit')" class="px-3 py-1.5 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-600 text-slate-500 text-xs rounded-lg hover:bg-gray-50 transition-colors">Otkaži</button>
          </div>
        </div>

        <template v-else>
          <p class="text-slate-700 dark:text-slate-300 leading-relaxed text-sm whitespace-pre-line">
            {{ comment.content }}
          </p>

          <!-- Attachments sa preview komponentom -->
          <div v-if="comment.attachments && comment.attachments.length > 0" class="mt-3">
            <ForumAttachmentPreview
              :attachments="comment.attachments"
              :download-base-url="`http://127.0.0.1:8000/forum/attachments/comment/${comment.id}`"
            />
          </div>
        </template>

        <!-- Reply dugme -->
        <div class="mt-2">
          <button
            v-if="canReply && !comment.is_deleted"
            @click="replyContentLocal = ''; emit('start-reply', comment.id)"
            class="text-xs text-slate-400 hover:text-orange-500 transition-colors font-medium"
          >↩ Odgovori</button>
        </div>

        <!-- Reply forma -->
        <div v-if="replyingToId === comment.id" class="mt-3">
          <textarea
            v-model="replyContentLocal"
            placeholder="Napišite odgovor..."
            class="w-full text-sm border border-gray-200 dark:border-slate-600 rounded-lg p-3 bg-white dark:bg-slate-700 text-slate-700 dark:text-slate-300 focus:outline-none focus:ring-2 focus:ring-orange-400 resize-none"
            rows="3"
          />

          <div class="mt-2">
            <label class="cursor-pointer inline-flex items-center gap-1.5 text-xs text-slate-500 hover:text-orange-500 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M18.375 12.739l-7.693 7.693a4.5 4.5 0 01-6.364-6.364l10.94-10.94A3 3 0 1119.5 7.372L8.552 18.32m.009-.01l-.01.01m5.699-9.941l-7.81 7.81a1.5 1.5 0 002.112 2.13" />
              </svg>
              Dodaj fajl (max 3, 5MB)
              <input type="file" multiple class="hidden" accept=".jpg,.jpeg,.png,.pdf,.docx,.txt" @change="handleReplyFileSelect" />
            </label>
            <ul v-if="replyFilesLocal.length > 0" class="mt-1 space-y-0.5">
              <li v-for="(file, i) in replyFilesLocal" :key="i" class="flex items-center gap-2 text-xs text-slate-500">
                📎 {{ file.name }}
                <button @click="replyFilesLocal.splice(i, 1)" class="text-red-400 hover:text-red-600 bg-transparent border-none cursor-pointer">✕</button>
              </li>
            </ul>
          </div>

          <div class="flex gap-2 mt-2">
            <button
              @click="emit('submit-reply', comment, replyContentLocal, replyFilesLocal); replyContentLocal = ''; replyFilesLocal = []"
              class="px-3 py-1.5 bg-orange-500 hover:bg-orange-400 text-white text-xs font-bold rounded-lg transition-colors"
            >Pošalji</button>
            <button
              @click="emit('cancel-reply')"
              class="px-3 py-1.5 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-600 text-slate-500 text-xs rounded-lg hover:bg-gray-50 transition-colors"
            >Otkaži</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Rekurzivni replies -->
    <div v-if="comment.replies?.length">
      <ForumCommentNode
        v-for="reply in comment.replies"
        :key="reply.id"
        :comment="reply"
        :current-user-id="currentUserId"
        :is-admin="isAdmin"
        :is-topic-author="isTopicAuthor"
        :can-reply="canReply"
        :topic-id="topicId"
        :open-medal-dropdown="openMedalDropdown"
        :editing-comment-id="editingCommentId"
        :replying-to-id="replyingToId"
        :depth="depth + 1"
        :get-user-vote="getUserVote"
        :get-likes-count="getLikesCount"
        :get-dislikes-count="getDislikesCount"
        :active-highlights="activeHighlights"
        @vote="(c, v) => emit('vote', c, v)"
        @best-answer="(c) => emit('best-answer', c)"
        @delete="(c) => emit('delete', c)"
        @start-edit="(id) => emit('start-edit', id)"
        @cancel-edit="emit('cancel-edit')"
        @submit-edit="(id, txt) => emit('submit-edit', id, txt)"
        @start-reply="(id) => emit('start-reply', id)"
        @cancel-reply="emit('cancel-reply')"
        @submit-reply="(c, txt, files) => emit('submit-reply', c, txt, files)"
        @toggle-medals="(key) => emit('toggle-medals', key)"
      />
    </div>
  </div>
</template>