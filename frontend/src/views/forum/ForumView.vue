<script setup>
import { ref, onMounted } from 'vue';
import { getTopics } from '../../services/forum';
import CreateTopicView from './CreateTopicView.vue';
import TopicDetailView from './TopicDetailView.vue';

const teme = ref([]);
const isLoading = ref(true);
const showCreateForm = ref(false);
const selectedTopic = ref(null);

const loadTopics = async () => {
  isLoading.value = true;
  try {
    teme.value = await getTopics();
  } catch (error) {
    console.warn("Backend ruta ne postoji, učitavam lažne podatke za dizajn...");
    teme.value = [];
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  await loadTopics();
});

const onTopicCreated = async () => {
  showCreateForm.value = false;
  await loadTopics();
};

const openTopic = (tema) => {
  selectedTopic.value = tema;
};

const onBack = () => {
  selectedTopic.value = null;
};
</script>

<template>
  <CreateTopicView
    v-if="showCreateForm"
    @topic-created="onTopicCreated"
    @cancel="showCreateForm = false"
  />

  <TopicDetailView
    v-else-if="selectedTopic"
    :topic="selectedTopic"
    @back="onBack"
  />

  <div v-else class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-4xl mx-auto">

      <!-- Search + Nova tema -->
      <div class="flex gap-3 mb-6">
        <input
          type="text"
          placeholder="Pretraži diskusije po ključnoj riječi..."
          class="flex-1 border border-gray-200 rounded-lg px-4 py-2.5 text-slate-700 placeholder-gray-400 bg-white focus:outline-none focus:ring-2 focus:ring-orange-400"
        />
        <button
          @click="showCreateForm = true"
          class="bg-orange-500 hover:bg-orange-400 text-white font-medium px-5 py-2.5 rounded-lg transition-colors flex items-center gap-2"
        >
          + Nova tema
        </button>
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="flex flex-col items-center justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mb-4"></div>
        <p class="text-slate-400">Učitavanje tema...</p>
      </div>

      <!-- Lista tema -->
      <div v-else class="space-y-3">
        <div
          v-for="tema in teme"
          :key="tema.id"
          @click="openTopic(tema)"
          class="p-5 bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md hover:border-gray-300 transition-all cursor-pointer"
        >
          <div class="flex items-center gap-2 mb-1 flex-wrap">
            <span class="text-xs bg-orange-100 text-orange-600 px-2 py-0.5 rounded font-medium">
              {{ tema.category || 'Opšta diskusija' }}
            </span>
          </div>

          <h2 class="text-base font-semibold text-slate-800 hover:text-orange-500 transition-colors">
            {{ tema.title }}
          </h2>

          <p class="text-slate-500 text-sm mt-1 line-clamp-2">
            {{ tema.content }}
          </p>

          <div class="flex items-center gap-4 text-xs text-slate-400 mt-3">
            <span>💬 {{ tema.comments_count || 0 }} odgovora</span>
            <span>•</span>
            <span>👁️ {{ tema.views_count }} pregleda</span>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>