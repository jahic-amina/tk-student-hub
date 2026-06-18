<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import ForumTopicMainCard from '../../components/ForumTopicMainCard.vue';
import ForumTopicCommentsList from '../../components/ForumTopicCommentsList.vue';
import ForumSidebar from '../../components/ForumSidebar.vue'; 
import ForumWidgets from '../../components/ForumWidgets.vue'; 
import ForumGuidelines from '../../components/ForumGuidelines.vue'; 
import { postAdminNotice } from '../../services/forum_admin.js';
import { getTopicById, createComment, incrementTopicView, uploadCommentAttachments } from '../../services/forum';

const props = defineProps({
  id: { type: [String, Number], required: true }
});

const router = useRouter();
const route = useRoute();

const fullTopicData = ref(null);
const isLoading = ref(true);
const isSubmitting = ref(false);
const commentError = ref('');
const successMessage = ref('');

const adminNoticeContent = ref('');
const isSubmittingNotice = ref(false);
const noticeError = ref('');

const isAdmin = computed(() => localStorage.getItem('role') === 'admin');

const odabraniKategorijaId = computed(() => fullTopicData.value?.category?.id || null);

const sortCriteria = ref('top'); // 'top' | 'newest' | 'oldest'

// Izvuci comment_id iz URL hasha (#comment-123 → 123)
const highlightedCommentId = computed(() => {
  const hash = route.hash; // npr. '#comment-456'
  if (!hash || !hash.startsWith('#comment-')) return null;
  const parsed = parseInt(hash.replace('#comment-', ''), 10);
  return isNaN(parsed) ? null : parsed;
});

const sortedComments = computed(() => {
  const komentari = fullTopicData.value?.comments || [];
  const sorted = [...komentari];

  // Admin notice i best answer uvijek ostaju na vrhu bez obzira na sort
  sorted.sort((a, b) => {
    if (a.is_admin_notice !== b.is_admin_notice) return a.is_admin_notice ? -1 : 1;
    if (a.is_best_answer !== b.is_best_answer) return a.is_best_answer ? -1 : 1;

    if (sortCriteria.value === 'top') {
      return (b.votes_count ?? 0) - (a.votes_count ?? 0);
    } else if (sortCriteria.value === 'newest') {
      return new Date(b.created_at) - new Date(a.created_at);
    } else if (sortCriteria.value === 'oldest') {
      return new Date(a.created_at) - new Date(b.created_at);
    }
    return 0;
  });

  return sorted;
});

const topicAuthorId = computed(() => fullTopicData.value?.author?.id || null);

const loadTopicAndComments = async (topicId) => {
  if (!topicId) return;
  isLoading.value = true;
  try {
    await incrementTopicView(topicId);
    fullTopicData.value = await getTopicById(topicId);
  } catch (error) {
    console.error("Greška pri učitavanju detalja:", error);
  } finally {
    isLoading.value = false;
  }
};

const preusmjeriNaKategoriju = (kategorijaId) => {
  router.push('/forum');
};

onMounted(async () => {
  await loadTopicAndComments(props.id);
});

watch(
  () => props.id,
  async (noviId) => {
    if (noviId) {
      await loadTopicAndComments(noviId);
    }
  }
);

// ---- PRILAGOĐENO ZA RAD SA KARTICOM ----
const handleNewComment = async ({ content, files = [], onSuccess, onError }) => {
  commentError.value = '';
  successMessage.value = '';

  if (!content.trim()) {
    if (onError) onError('Odgovor ne može biti prazan.');
    return;
  }

  isSubmitting.value = true;
  try {
    const newComment = await createComment({
      content: content.trim(),
      topic_id: parseInt(props.id),
      is_admin_notice: false
    });

    if (files && files.length > 0 && newComment?.id) {
      await uploadCommentAttachments(newComment.id, files);
    }

    successMessage.value = 'Odgovor uspješno objavljen!';
    if (onSuccess) onSuccess();
    await loadTopicAndComments(props.id);
  } catch (error) {
    if (onError) onError('Došlo je do greške. Pokušajte ponovo.');
  } finally {
    isSubmitting.value = false;
  }
};

const handleAdminNotice = async () => {
  if (!adminNoticeContent.value.trim()) {
    noticeError.value = 'Unesite tekst obavještenja.';
    return;
  }
  isSubmittingNotice.value = true;
  noticeError.value = '';
  try {
    await postAdminNotice(props.id, adminNoticeContent.value);
    adminNoticeContent.value = '';
    await loadTopicAndComments(props.id);
  } catch (error) {
    noticeError.value = 'Greška pri objavi obavještenja.';
  } finally {
    isSubmittingNotice.value = false;
  }
};

</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-slate-900 text-slate-900 dark:text-slate-100 p-6 transition-colors duration-200">
    <div class="max-w-7xl mx-auto">

      <div class="mb-8">
        <button
          @click="router.push('/forum')"
          class="inline-flex items-center gap-2 px-4 py-2 text-xs font-bold uppercase tracking-wider text-slate-600 dark:text-slate-300 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 shadow-sm hover:text-[#ff7a00] transition-all duration-200"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
          </svg>
          Nazad na forum
        </button>
      </div>

      <div class="grid grid-cols-12 gap-2 items-start w-full">

        <div class="col-span-12 md:col-span-2 lg:col-span-2 xl:col-span-2" style="position: sticky; top: 140px; align-self: flex-start; z-index: 20;">
          <ForumSidebar :aktivna-kategorija-id="odabraniKategorijaId" @kategorija-izabrana="preusmjeriNaKategoriju" />
        </div>

        <div class="col-span-12 md:col-span-7 lg:col-span-7 xl:col-span-7 w-full">
          
          <div v-if="isLoading" class="flex justify-center py-12">
            <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-orange-500"></div>
          </div>

          <template v-else-if="fullTopicData">
            <ForumTopicMainCard 
              :topic="fullTopicData" 
              :is-admin="isAdmin" 
              @submit-topic-reply="handleNewComment"
               @refresh="() => loadTopicAndComments(props.id)"
            />

            <!-- Sort dropdown -->
             <div class="flex items-center justify-end gap-2 mb-3">
              <span class="text-xs text-slate-500 dark:text-slate-400 font-medium">Sortiraj:</span>
              <select
              v-model="sortCriteria"
              class="text-xs font-semibold bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-orange-400 cursor-pointer transition-colors"
              >
              <option value="top">⬆ Najbolje ocijenjeni</option>
              <option value="newest">🕐 Najnoviji</option>
              <option value="oldest">🕓 Najstariji</option>
            </select>
          </div>

          <!-- Prosljeđujemo highlighted comment id da lista zna koji da highlightuje -->
          <ForumTopicCommentsList 
            :comments="sortedComments" 
            :topic-author-id="topicAuthorId" 
            :topic-id="parseInt(props.id)"
            :highlighted-comment-id="highlightedCommentId"
            @refresh="() => loadTopicAndComments(props.id)" 
          />

            <div v-if="fullTopicData.is_locked" class="bg-gray-100 dark:bg-slate-800 text-center text-gray-500 p-4 rounded-xl font-bold mt-4">
              🔒 Ova tema je zaključana za daljnje odgovore.
            </div>

            <div v-else-if="isAdmin" class="bg-indigo-50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300 text-center p-4 rounded-xl border border-indigo-200 dark:border-indigo-800 font-bold text-[13px] mt-4">
              👑 Prijavljeni ste kao administrator. Koristite formu sa desne strane za postavljanje službenih obavještenja.
            </div>
            
            </template>
        </div>

        <div v-if="fullTopicData" class="col-span-12 md:col-span-3 lg:col-span-3 xl:col-span-3 flex flex-col gap-4" style="position: sticky; top: 140px; align-self: flex-start; z-index: 20;">
          
          <div v-if="isAdmin" class="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl p-4 shadow-lg text-white">
            <h3 class="font-extrabold text-xs uppercase tracking-wide mb-3 flex items-center gap-1.5">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
                <path fill-rule="evenodd" d="M10.5 3.75a6.75 6.75 0 0111.493 4.776A11.948 11.948 0 0122.5 15.63a.75.75 0 01-.75.75h-7.682a2.25 2.25 0 01-4.136 0H2.25a.75.75 0 01-.75-.75 11.948 11.948 0 01.507-7.104A6.75 6.75 0 0110.5 3.75zm1.5 15.397a.75.75 0 01.75.75 2.25 2.25 0 01-4.5 0 .75.75 0 01.75-.75h3z" clip-rule="evenodd" />
              </svg>
              Službeno Obavještenje
            </h3>
            
            <textarea 
              v-model="adminNoticeContent"
              class="w-full bg-white/10 border border-white/20 rounded-lg p-2.5 text-xs text-white placeholder-white/60 focus:ring-2 focus:ring-white focus:outline-none resize-none h-20 mb-2 transition-all"
              placeholder="Ovo obavještenje će biti zakačeno na vrhu teme..."
            ></textarea>
            
            <p v-if="noticeError" class="text-red-200 text-[11px] mb-2 font-bold">{{ noticeError }}</p>
            
            <button 
              @click="handleAdminNotice"
              :disabled="isSubmittingNotice"
              class="w-full bg-white text-indigo-600 hover:bg-indigo-50 font-extrabold text-[11px] uppercase tracking-wider py-2.5 px-4 rounded-lg transition-colors shadow-sm disabled:opacity-50"
            >
              {{ isSubmittingNotice ? 'Objavljujem...' : 'Zakači na vrh' }}
            </button>
          </div>

          <ForumGuidelines />

          <ForumWidgets 
            :current-topic-id="fullTopicData.id" 
            :selected-category-id="fullTopicData.category_id || fullTopicData.category?.id"
            :current-topic-title="fullTopicData.title" 
          />
        </div>

      </div>
    </div>
  </div>
</template>