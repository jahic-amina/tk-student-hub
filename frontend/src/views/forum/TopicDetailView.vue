<script setup>
import { ref, onMounted, computed } from 'vue';
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

const sortedComments = computed(() => {
  return fullTopicData.value?.comments || [];
});

const topicAuthorId = computed(() => fullTopicData.value?.author?.id || null);

const loadTopicAndComments = async () => {
  isLoading.value = true;
  try {
    await incrementTopicView(props.id);
    fullTopicData.value = await getTopicById(props.id);
  } catch (error) {
    console.error("Greška pri učitavanju detalja:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  await loadTopicAndComments();
});

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
      topic_id: parseInt(props.id)
    });
    
    successMessage.value = 'Odgovor uspješno objavljen!';
    clearForm(); 
    await loadTopicAndComments(); 
  } catch (error) {
    commentError.value = 'Došlo je do greške. Pokušajte ponovo.';
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-4xl mx-auto">

      <button
        @click="router.push('/forum')"
        class="flex items-center gap-2 text-slate-500 hover:text-slate-700 mb-6 text-sm transition-colors font-semibold bg-transparent border-none cursor-pointer"
      >
        ← Nazad na listu
      </button>

      <div v-if="isLoading" class="flex justify-center py-12">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-orange-500"></div>
      </div>

      <template v-else-if="fullTopicData">
        
        <ForumTopicMainCard :topic="fullTopicData" />

        <ForumTopicCommentsList :comments="sortedComments" :topic-author-id="topicAuthorId" @refresh="loadTopicAndComments" />

        <ForumTopicCommentForm 
          :is-submitting="isSubmitting"
          :comment-error="commentError"
          :success-message="successMessage"
          @posaljiKomentar="handleNewComment"
        />

      </template>

    </div>
  </div>
</template>