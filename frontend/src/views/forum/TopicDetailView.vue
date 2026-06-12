<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import ForumTopicMainCard from '../../components/ForumTopicMainCard.vue';
import ForumTopicCommentsList from '../../components/ForumTopicCommentsList.vue';
import ForumTopicCommentForm from '../../components/ForumTopicCommentForm.vue';
import ForumSidebar from '../../components/ForumSidebar.vue'; 
import ForumWidgets from '../../components/ForumWidgets.vue'; 
import { getTopicById, createComment, incrementTopicView } from '../../services/forum';

const props = defineProps({
  id: { type: [String, Number], required: true }
});

const router = useRouter();

const fullTopicData = ref(null);
const isLoading = ref(true);
const isSubmitting = ref(false);
const commentError = ref('');
const successMessage = ref('');

const isAdmin = computed(() => localStorage.getItem('role') === 'admin');

// Izvuci ID kategorije iz učitane teme kako bi sidebar znao šta da označi kao aktivno
const odabraniKategorijaId = computed(() => fullTopicData.value?.category?.id || null);

const sortedComments = computed(() => {
  const komentari = fullTopicData.value?.comments || [];
  return [...komentari].sort((a, b) => {
    if (a.is_best_answer && !b.is_best_answer) return -1;
    if (!a.is_best_answer && b.is_best_answer) return 1;
    return 0;
  });
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

// Ako korisnik klikne na kategoriju u sidebaru, vraćamo ga na forum
const preusmjeriNaKategoriju = (kategorijaId) => {
  if (kategorijaId === null) {
    router.push('/forum');
  } else {
    router.push('/forum'); 
  }
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

const handleNewComment = async ({ content, clearForm }) => {
  commentError.value = '';
  successMessage.value = '';

  if (!content.trim()) {
    commentError.value = 'Odgovor ne može biti prazan.';
    return;
  }
  if (content.trim().length < 2) {
    commentError.value = 'Odgovor mora imati najmanje 2 karaktera.';
    return;
  }

  isSubmitting.value = true;
  try {
    await createComment({
      content: content.trim(),
      topic_id: parseInt(props.id),
      is_admin_notice: isAdmin.value
    });
    
    successMessage.value = 'Odgovor uspješno objavljen!';
    clearForm(); 
    await loadTopicAndComments(props.id); 
  } catch (error) {
    commentError.value = 'Došlo je do greške. Pokušajte ponovo.';
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-slate-900 text-slate-900 dark:text-slate-100 p-6 transition-colors duration-200">
    <div class="max-w-7xl mx-auto">

      <div class="mb-8">
        <button
          @click="router.push('/forum')"
          class="inline-flex items-center gap-2 px-4 py-2 text-xs font-bold uppercase tracking-wider text-slate-600 dark:text-slate-300 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 shadow-sm hover:text-[#ff7a00] dark:hover:text-[#ff7a00] hover:border-[#ff7a00]/30 dark:hover:border-[#ff7a00]/30 hover:bg-orange-50/50 dark:hover:bg-orange-950/10 transition-all duration-200 cursor-pointer group"
        >
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke-width="2.5" 
            stroke="currentColor" 
            class="w-4 h-4 transform group-hover:-translate-x-1 transition-transform duration-200"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
          </svg>
          Nazad na forum
        </button>
      </div>

      <div class="grid grid-cols-12 gap-2 items-start w-full">

        <div 
          class="col-span-12 md:col-span-2 lg:col-span-2 xl:col-span-2"
          style="position: sticky; top: 140px; align-self: flex-start; z-index: 20;"
        >
          <ForumSidebar 
            :aktivna-kategorija-id="odabraniKategorijaId" 
            @kategorija-izabrana="preusmjeriNaKategoriju" 
          />
        </div>

        <div class="col-span-12 md:col-span-7 lg:col-span-7 xl:col-span-7 w-full">
          
          <div v-if="isLoading" class="flex justify-center py-12">
            <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-orange-500"></div>
          </div>

          <template v-else-if="fullTopicData">
            
            <ForumTopicMainCard :topic="fullTopicData" :is-admin="isAdmin" />

            <ForumTopicCommentsList 
              :comments="sortedComments" 
              :topic-author-id="topicAuthorId" 
              :topic-id="parseInt(props.id)" 
              @refresh="() => loadTopicAndComments(props.id)" 
            />

            <div v-if="fullTopicData.is_locked" class="bg-gray-100 dark:bg-slate-800 text-center text-gray-500 dark:text-slate-400 p-4 rounded-xl border border-gray-200 dark:border-slate-700 font-bold">
              🔒 Ova tema je zaključana za daljnje odgovore.
            </div>

            <div v-else>
              <ForumTopicCommentForm 
                :is-submitting="isSubmitting"
                :comment-error="commentError"
                :success-message="successMessage"
                @posaljiKomentar="handleNewComment"
              />
            </div>

          </template>
        </div>

        <div 
          class="col-span-12 md:col-span-3 lg:col-span-3 xl:col-span-3"
          style="position: sticky; top: 140px; align-self: flex-start; z-index: 20;"
        >
          <ForumWidgets />
        </div>

      </div>

    </div>
  </div>
</template>