<script setup>
import { ref, onMounted } from 'vue';
import { getTopicById, createComment } from '../../services/forum';

const props = defineProps({
  topic: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['back']);

const comments = ref([]);
const isLoadingComments = ref(true);
const newComment = ref('');
const isSubmitting = ref(false);
const commentError = ref('');
const successMessage = ref('');

const loadComments = async () => {
  isLoadingComments.value = true;
  try {
    const response = await fetch(`http://127.0.0.1:8000/forum/topics/${props.topic.id}/comments`);
    const data = await response.json();
    comments.value = data;
  } catch (error) {
    console.warn("Greška pri učitavanju komentara.");
  } finally {
    isLoadingComments.value = false;
  }
};

onMounted(async () => {
  await loadComments();
});

const submitComment = async () => {
  commentError.value = '';
  successMessage.value = '';

  if (!newComment.value.trim()) {
    commentError.value = 'Odgovor ne može biti prazan.';
    return;
  }
  if (newComment.value.trim().length < 2) {
    commentError.value = 'Odgovor mora imati najmanje 2 karaktera.';
    return;
  }

  isSubmitting.value = true;
  try {
    await createComment({
      content: newComment.value.trim(),
      topic_id: props.topic.id
    });
    newComment.value = '';
    successMessage.value = 'Odgovor uspješno objavljen!';
    await loadComments();
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

      <!-- Nazad -->
      <button
        @click="$emit('back')"
        class="flex items-center gap-2 text-slate-500 hover:text-slate-700 mb-6 text-sm transition-colors"
      >
        ← Nazad na listu
      </button>

      <!-- Tema -->
      <div class="bg-white rounded-xl border border-gray-200 shadow-sm p-6 mb-6">
        <h1 class="text-2xl font-bold text-slate-800 mb-4">{{ topic.title }}</h1>
        <p class="text-slate-600 leading-relaxed">{{ topic.content }}</p>
      </div>

      <!-- Komentari -->
      <div class="mb-6">
        <h2 class="text-lg font-semibold text-slate-700 mb-4">
          {{ comments.length }} {{ comments.length === 1 ? 'Odgovor' : 'Odgovora' }}
        </h2>

        <div v-if="isLoadingComments" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500"></div>
        </div>

        <div v-else class="space-y-4">
          <div
            v-for="comment in comments"
            :key="comment.id"
            class="bg-white rounded-xl border border-gray-200 shadow-sm p-5"
          >
            <p class="text-slate-700 leading-relaxed">{{ comment.content }}</p>
          </div>

          <div v-if="comments.length === 0" class="text-center py-8 text-slate-400">
            Još nema odgovora. Budite prvi!
          </div>
        </div>
      </div>

      <!-- Polje za odgovor -->
      <div class="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
        <h3 class="text-base font-semibold text-slate-700 mb-3">Vaš odgovor</h3>

        <div v-if="successMessage" class="bg-green-50 border border-green-200 text-green-600 px-4 py-3 rounded-lg text-sm mb-4">
          {{ successMessage }}
        </div>

        <textarea
          v-model="newComment"
          rows="5"
          placeholder="Napišite vaš odgovor..."
          class="w-full border border-gray-200 rounded-lg px-4 py-2.5 text-slate-800 placeholder-gray-400 bg-white focus:outline-none focus:ring-2 focus:ring-orange-400 transition-all resize-y"
          :class="commentError ? 'border-red-400' : 'border-gray-200'"
        />
        <p v-if="commentError" class="text-red-500 text-xs mt-1">{{ commentError }}</p>

        <div class="flex justify-end mt-4">
          <button
            @click="submitComment"
            :disabled="isSubmitting"
            class="flex items-center gap-2 px-6 py-2.5 bg-orange-500 hover:bg-orange-400 text-white font-medium rounded-lg transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
          >
            <span v-if="isSubmitting" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></span>
            <span>{{ isSubmitting ? 'Slanje...' : 'Objavi odgovor' }}</span>
          </button>
        </div>
      </div>

    </div>
  </div>
</template>