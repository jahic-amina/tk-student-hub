<script setup>
import { ref, onMounted, computed } from 'vue';
import { getTopicById, createComment, incrementTopicView } from '../../services/forum';

const props = defineProps({
  topic: {
    type: Object,
    required: true
  }
});

defineEmits(['back']);

const fullTopicData = ref(null);
const isLoading = ref(true);
const newComment = ref('');
const isSubmitting = ref(false);
const commentError = ref('');
const successMessage = ref('');

const sortedComments = computed(() => {
  return fullTopicData.value?.comments || [];
});

const loadTopicAndComments = async () => {
  isLoading.value = true;
  try {
    // Inkrementacija pregleda na backendu i povlačenje svježih podataka s komentarima
    await incrementTopicView(props.topic.id);
    fullTopicData.value = await getTopicById(props.topic.id);
  } catch (error) {
    console.warn("Greška pri asinhronom učitavanju detalja, koristim poslane propse...");
    fullTopicData.value = { ...props.topic, comments: [] };
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  await loadTopicAndComments();
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
    await loadTopicAndComments(); // Osvježava listu komentara nakon slanja
  } catch (error) {
    commentError.value = 'Došlo je do greške. Pokušajte ponovo.';
  } finally {
    isSubmitting.value = false;
  }
};

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
  <div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-4xl mx-auto">

      <button
        @click="$emit('back')"
        class="flex items-center gap-2 text-slate-500 hover:text-slate-700 mb-6 text-sm transition-colors font-semibold"
      >
        ← Nazad na listu
      </button>

      <div v-if="isLoading" class="flex justify-center py-12">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-orange-500"></div>
      </div>

      <template v-else-if="fullTopicData">
        <div class="bg-white rounded-xl border border-gray-200 shadow-sm p-6 mb-6">
          <h1 class="text-2xl font-bold text-slate-900 mb-4">{{ fullTopicData.title }}</h1>
          
          <div class="flex items-center gap-2 text-xs text-slate-500 mb-4 bg-slate-50 p-2 rounded-lg w-fit">
            <span class="w-6 h-6 rounded-full bg-orange-500 text-white flex items-center justify-center font-bold text-[10px]">
              {{ getInitials(fullTopicData.author?.full_name) }}
            </span>
            <span class="font-semibold text-slate-700">{{ fullTopicData.author?.full_name || 'Student' }}</span>
            <span>•</span>
            <span>{{ formatDate(fullTopicData.created_at) }}</span>
            <span>•</span>
            <span>👁️ {{ fullTopicData.views_count || 0 }} pregleda</span>
          </div>

          <p class="text-slate-700 leading-relaxed whitespace-pre-line">{{ fullTopicData.content }}</p>
        </div>

        <div class="mb-6">
          <h2 class="text-lg font-semibold text-slate-700 mb-4">
            {{ sortedComments.length }} {{ sortedComments.length === 1 ? 'Odgovor' : 'Odgovora' }}
          </h2>

          <div class="space-y-4">
            <div
              v-for="comment in sortedComments"
              :key="comment.id"
              class="bg-white rounded-xl border p-5 flex gap-4 transition-all"
              :class="comment.is_best_answer ? 'border-green-300 bg-green-50/20' : 'border-gray-200 shadow-sm'"
            >
              <div class="flex-1">
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center gap-2 text-xs text-slate-400">
                    <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-600 flex items-center justify-center font-bold text-[8px]">
                      {{ getInitials(comment.author?.full_name) }}
                    </span>
                    <strong class="text-slate-600">{{ comment.author?.full_name || 'Kolega' }}</strong>
                    <span>•</span>
                    <span>{{ formatDate(comment.created_at) }}</span>
                  </div>
                  <span v-if="comment.is_best_answer" class="text-[10px] bg-green-100 text-green-700 px-2 py-0.5 rounded-full font-bold">
                    Najbolji odgovor
                  </span>
                </div>
                <p class="text-slate-700 leading-relaxed text-sm whitespace-pre-line">{{ comment.content }}</p>
              </div>
            </div>

            <div v-if="sortedComments.length === 0" class="text-center py-8 text-slate-400 bg-white rounded-xl border border-gray-200 shadow-sm">
              Još nema odgovora. Budite prvi!
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
          <h3 class="text-base font-semibold text-slate-700 mb-3">Vaš odgovor</h3>

          <div v-if="successMessage" class="bg-green-50 border border-green-200 text-green-600 px-4 py-3 rounded-lg text-sm mb-4">
            {{ successMessage }}
          </div>

          <textarea
            v-model="newComment"
            rows="5"
            placeholder="Napišite vaš odgovor..."
            class="w-full border rounded-lg px-4 py-2.5 text-slate-800 placeholder-gray-400 bg-white focus:outline-none focus:ring-2 focus:ring-orange-400 transition-all resize-y"
            :class="commentError ? 'border-red-400' : 'border-gray-200'"
          />
          <p v-if="commentError" class="text-red-500 text-xs mt-1">{{ commentError }}</p>

          <div class="flex justify-end mt-4">
            <button
              @click="submitComment"
              :disabled="isSubmitting"
              class="flex items-center gap-2 px-6 py-2.5 bg-orange-500 hover:bg-orange-400 text-white font-medium rounded-lg transition-colors disabled:opacity-60 disabled:cursor-not-allowed shadow-sm"
            >
              <span v-if="isSubmitting" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></span>
              <span>{{ isSubmitting ? 'Slanje...' : 'Objavi odgovor' }}</span>
            </button>
          </div>
        </div>
      </template>

    </div>
  </div>
</template>