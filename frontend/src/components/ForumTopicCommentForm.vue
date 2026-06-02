<script setup>
import { ref } from 'vue';

defineProps({
  isSubmitting: { type: Boolean, default: false },
  commentError: { type: String, default: '' },
  successMessage: { type: String, default: '' }
});

const emit = defineEmits(['posaljiKomentar']);
const text = ref('');

const handleSubmit = () => {
  emit('posaljiKomentar', {
    content: text.value,
    clearForm: () => { text.value = ''; }
  });
};
</script>

<template>
  <div class="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 shadow-sm p-6 transition-colors duration-200">
    <h3 class="text-base font-semibold text-slate-700 dark:text-slate-200 mb-3">Vaš odgovor</h3>

    <div v-if="successMessage" class="bg-green-50 dark:bg-green-950/30 border border-green-200 dark:border-green-900 text-green-600 dark:text-green-400 px-4 py-3 rounded-lg text-sm mb-4">
      {{ successMessage }}
    </div>

    <textarea
      v-model="text"
      rows="5"
      placeholder="Napišite vaš odgovor..."
      class="w-full border rounded-lg px-4 py-2.5 text-slate-800 dark:text-slate-100 placeholder-gray-400 dark:placeholder-slate-500 bg-white dark:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-orange-400 transition-all resize-y"
      :class="commentError ? 'border-red-400' : 'border-gray-200 dark:border-slate-600'"
    />
    <p v-if="commentError" class="text-red-500 text-xs mt-1">{{ commentError }}</p>

    <div class="flex justify-end mt-4">
      <button
        @click="handleSubmit"
        :disabled="isSubmitting"
        class="flex items-center gap-2 px-6 py-2.5 bg-orange-500 hover:bg-orange-400 text-white font-medium rounded-lg transition-colors disabled:opacity-60 disabled:cursor-not-allowed shadow-sm"
      >
        <span v-if="isSubmitting" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></span>
        <span>{{ isSubmitting ? 'Slanje...' : 'Objavi odgovor' }}</span>
      </button>
    </div>
  </div>
</template>