<script setup>
import { ref, computed } from 'vue';
import ForumAvatar from './ForumAvatar.vue';

const props = defineProps({
  comment: { type: Object, required: true },
  currentUserId: { type: Number, default: null },
  isAdmin: { type: Boolean, default: false },
  isTopicAuthor: { type: Boolean, default: false },
  topicId: { type: Number, default: null },
  openMedalDropdown: { type: String, default: null },
  editingCommentId: { type: Number, default: null },
  replyingToId: { type: Number, default: null },
  // Pratimo dubinu kako bismo znali kada da prestanemo sa uvlačenjem (UX zaštita iz Jire!)
  depth: { type: Number, default: 0 }
});

const emit = defineEmits([
  'vote', 'best-answer', 'delete', 'start-edit', 'cancel-edit', 
  'submit-edit', 'start-reply', 'cancel-reply', 'submit-reply', 
  'toggle-medals', 'update:replyContent', 'update:editContent'
]);

// Lokalni proxy za v-model (pošto props ne smijemo mutirati)
const replyContentLocal = ref('');
const editContentLocal = ref('');

// Određivanje da li vizuelno uvlačimo komentar (maksimalno do 3-4 nivoa radi UX-a, a ostali ostaju poravnati na tom nivou)
const maxVisualDepth = 3;
const shouldIndent = computed(() => props.depth > 0 && props.depth <= maxVisualDepth);

// Pomoćne metode za klase i medalje (preslikane iz tvog koda)
const medalIcons = { gold: '🥇', silver: '🥈', bronze: '🥉' };
function parseMedal(medal) {
  if (!medal) return { icon: '🏅', tooltip: 'Medalja' };
  const icon = medalIcons[medal.tier] || '🏅';
  return { icon, tooltip: medal.category_name || 'Priznanje' };
}

function getTierClass(title) {
  if (!title) return 'bg-slate-100 text-slate-600 border-slate-200 dark:bg-slate-700 dark:text-slate-300 dark:border-slate-600';
  const t = title.toLowerCase();
  if (t.includes('zlatni') || t.includes('expert')) return 'bg-amber-50 text-amber-700 border-amber-300 dark:bg-amber-950/40 dark:text-amber-400 font-bold';
  return 'bg-orange-50 text-orange-700 border-orange-200 dark:bg-orange-950/30';
}

function getRoleBadgeClass(role) {
  if (!role) return 'bg-slate-100 border-slate-200';
  if (role.toLowerCase() === 'admin') return 'bg-red-50 text-red-700 border-red-300 font-bold';
  return 'bg-blue-50 text-blue-600 border-blue-200';
}

function formatDate(dateValue) {
  if (!dateValue) return "";
  return new Intl.DateTimeFormat("bs-BA", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" }).format(new Date(dateValue));
}
</script>

<template>
  <div 
    class="transition-all"
    :class="[
      shouldIndent ? 'pl-6 border-l-2 border-gray-100 dark:border-slate-700 mt-3' : 'mt-4'
    ]"
  >
    <div
      class="bg-white dark:bg-slate-800 rounded-xl border p-4 flex gap-3 shadow-sm"
      :class="[
        comment.is_admin_notice ? 'border-red-300 bg-red-50/30 dark:bg-red-950/20' : '',
        comment.is_best_answer ? 'border-yellow-400 bg-yellow-50/20 dark:bg-yellow-950/20' : 'border-gray-200 dark:border-slate-700'
      ]"
    >
      <div class="flex-shrink-0 pt-1">
        <ForumAvatar :author="comment.author" class="w-6 h-6 text-[9px]" />
      </div>

      <div class="flex-1 min-w-0">
        <div class="flex items-center justify-between mb-1">
          <div class="flex items-center flex-wrap gap-2 text-xs text-slate-400">
            <strong class="text-slate-600 dark:text-slate-300">{{ comment.author?.full_name || 'Kolega' }}</strong>
            
            <span v-if="comment.author?.role" class="text-[10px] px-1.5 py-0.5 rounded border" :class="getRoleBadgeClass(comment.author.role)">
              {{ comment.author.role }}
            </span>

            <span v-if="comment.author?.title" class="text-[10px] px-1.5 py-0.5 rounded border" :class="getTierClass(comment.author.title)">
              Nivo {{ comment.author.level }} · {{ comment.author.title }}
            </span>

            <div v-if="comment.author?.medals?.length" class="flex items-center gap-1 relative">
              <span v-for="medal in comment.author.medals.slice(0, 3)" :key="medal.id" class="text-sm cursor-help" :title="parseMedal(medal).tooltip">
                {{ parseMedal(medal).icon }}
              </span>
            </div>

            <span>•</span>
            <span>{{ formatDate(comment.created_at) }}</span>
          </div>

          <div class="flex items-center gap-1">
            <button v-if="isTopicAuthor && depth === 0" @click="emit('best-answer', comment)" class="text-slate-300 hover:text-yellow-500 p-1">
              ★
            </button>
            <button v-if="(currentUserId === comment.author?.id || isAdmin) && !comment.is_deleted" @click="editContentLocal = comment.content; emit('start-edit', comment.id)" class="text-slate-300 hover:text-blue-400 p-1">
              ✎
            </button>
            <button v-if="currentUserId === comment.author?.id || isAdmin" @click="emit('delete', comment)" class="text-slate-300 hover:text-red-400 p-1">
              🗑
            </button>
          </div>
        </div>

        <div v-if="comment.is_deleted" class="text-slate-400 text-xs italic">Komentar je obrisan.</div>
        
        <div v-else-if="editingCommentId === comment.id" class="mt-2">
          <textarea v-model="editContentLocal" class="w-full text-sm border rounded-lg p-2 bg-slate-50 dark:bg-slate-700 text-slate-300 resize-none" rows="2" />
          <div class="flex gap-2 mt-1">
            <button @click="emit('submit-edit', comment.id, editContentLocal)" class="px-2 py-1 bg-orange-500 text-white text-xs font-bold rounded">Sačuvaj</button>
            <button @click="emit('cancel-edit')" class="px-2 py-1 bg-gray-200 dark:bg-slate-600 text-xs rounded">Otkaži</button>
          </div>
        </div>
        
        <p v-else class="text-slate-700 dark:text-slate-300 text-sm whitespace-pre-line leading-relaxed">{{ comment.content }}</p>

        <div class="mt-2" v-if="currentUserId && !comment.is_deleted">
          <button @click="replyContentLocal = ''; emit('start-reply', comment.id)" class="text-xs text-slate-400 hover:text-orange-500 font-medium">
            ↩ Odgovori
          </button>
        </div>

        <div v-if="replyingToId === comment.id" class="mt-3">
          <textarea v-model="replyContentLocal" placeholder="Napišite odgovor..." class="w-full text-sm border rounded-lg p-2 bg-white dark:bg-slate-700 text-slate-300 resize-none" rows="2" />
          <div class="flex gap-2 mt-1">
            <button @click="emit('submit-reply', comment, replyContentLocal); replyContentLocal = ''" class="px-3 py-1 bg-orange-500 text-white text-xs font-bold rounded">Pošalji</button>
            <button @click="emit('cancel-reply')" class="px-3 py-1 bg-gray-200 dark:bg-slate-600 text-xs rounded">Otkaži</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="comment.replies && comment.replies.length > 0">
      <ForumCommentNode
        v-for="subReply in comment.replies"
        :key="subReply.id"
        :comment="subReply"
        :current-user-id="currentUserId"
        :is-admin="isAdmin"
        :is-topic-author="isTopicAuthor"
        :topic-id="topicId"
        :open-medal-dropdown="openMedalDropdown"
        :editing-commentId="editingCommentId"
        :replying-to-id="replyingToId"
        :depth="depth + 1" 
        @vote="(c, v) => emit('vote', c, v)"
        @best-answer="(c) => emit('best-answer', c)"
        @delete="(c) => emit('delete', c)"
        @start-edit="(id) => emit('start-edit', id)"
        @cancel-edit="emit('cancel-edit')"
        @submit-edit="(id, txt) => emit('submit-edit', id, txt)"
        @start-reply="(id) => emit('start-reply', id)"
        @cancel-reply="emit('cancel-reply')"
        @submit-reply="(c, txt) => emit('submit-reply', c, txt)"
      />
    </div>
  </div>
</template>