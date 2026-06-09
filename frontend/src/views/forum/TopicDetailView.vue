<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import ForumTopicMainCard from '../../components/ForumTopicMainCard.vue';
import ForumTopicCommentsList from '../../components/ForumTopicCommentsList.vue';
import ForumTopicCommentForm from '../../components/ForumTopicCommentForm.vue';
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
    <div class="max-w-4xl mx-auto">

      <button
        @click="router.push('/forum')"
        class="flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 mb-6 text-sm transition-colors font-semibold bg-transparent border-none cursor-pointer"
      >
        ← Nazad na listu
      </button>

      <div v-if="isLoading" class="flex justify-center py-12">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-orange-500"></div>
      </div>

      <template v-else-if="fullTopicData">
        
        <ForumTopicMainCard :topic="fullTopicData" :is-admin="isAdmin" />

        <ForumTopicCommentsList :comments="sortedComments" :topic-author-id="topicAuthorId" :topic-id="parseInt(props.id)" @refresh="() => loadTopicAndComments(props.id)" />

        <div v-if="fullTopicData.is_locked" class="bg-gray-100 text-center text-gray-500 p-4 rounded-xl border border-gray-200 font-bold">
          🔒 Ova tema je zaključana za daljnje odgovore.
        </div>

        <div v-else>
          <ForumTopicCommentForm 
            v-if="!isAdmin"
            :is-submitting="isSubmitting"
            :comment-error="commentError"
            :success-message="successMessage"
            @posaljiKomentar="handleNewComment"
          />
          <div v-else class="bg-red-50 border border-red-200 p-6 rounded-xl">
            <h3 class="text-sm font-bold text-red-700 mb-2">🛡️ Ostavite moderacijsko obavještenje na temi</h3>
            <ForumTopicCommentForm 
              :is-submitting="isSubmitting"
              :comment-error="commentError"
              :success-message="successMessage"
              @posaljiKomentar="handleNewComment"
            />
          </div>
        </div>

      </template>

    </div>
  </div>
</template>