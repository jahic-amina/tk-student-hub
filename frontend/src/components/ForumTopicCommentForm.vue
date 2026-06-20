<script setup>
import { ref } from 'vue';

defineProps({
  isSubmitting: { type: Boolean, default: false },
  commentError: { type: String, default: '' },
  successMessage: { type: String, default: '' }
});

const emit = defineEmits(['posaljiKomentar', 'otkazi']);
const text = ref('');
const selectedFiles = ref([]);

const ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.pdf', '.docx', '.txt'];
const MAX_FILE_SIZE = 5 * 1024 * 1024;
const MAX_FILES = 3;

function handleFileSelect(event) {
  const files = Array.from(event.target.files);
  for (const file of files) {
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(ext)) { alert(`Format ${ext} nije dozvoljen.`); return; }
    if (file.size > MAX_FILE_SIZE) { alert(`Fajl "${file.name}" je prevelik. Max 5 MB.`); return; }
  }
  if (selectedFiles.value.length + files.length > MAX_FILES) { alert('Maksimalno 3 fajla.'); return; }
  selectedFiles.value = [...selectedFiles.value, ...files];
}

const handleSubmit = () => {
  emit('posaljiKomentar', {
    content: text.value,
    files: selectedFiles.value,
    clearForm: () => { text.value = ''; selectedFiles.value = []; }
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

    <!-- File upload -->
    <div class="mt-3">
      <label class="cursor-pointer inline-flex items-center gap-1.5 text-xs text-slate-500 hover:text-orange-500 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M18.375 12.739l-7.693 7.693a4.5 4.5 0 01-6.364-6.364l10.94-10.94A3 3 0 1119.5 7.372L8.552 18.32m.009-.01l-.01.01m5.699-9.941l-7.81 7.81a1.5 1.5 0 002.112 2.13" />
        </svg>
        Dodaj fajl (max 3, 5MB)
        <input type="file" multiple class="hidden" accept=".jpg,.jpeg,.png,.pdf,.docx,.txt" @change="handleFileSelect" />
      </label>
      <ul v-if="selectedFiles.length > 0" class="mt-1 space-y-0.5">
        <li v-for="(file, i) in selectedFiles" :key="i" class="flex items-center gap-2 text-xs text-slate-500">
          📎 {{ file.name }}
          <button @click="selectedFiles.splice(i, 1)" class="text-red-400 hover:text-red-600 bg-transparent border-none cursor-pointer">✕</button>
        </li>
      </ul>
    </div>

    <div class="flex justify-end items-center gap-3 mt-4">
      <button 
        type="button"
        @click="emit('otkazi')" 
        :disabled="isSubmitting"
        class="px-4 py-2.5 text-sm font-medium text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200 transition-colors bg-transparent border-none cursor-pointer disabled:opacity-50"
      >
        Otkaži
      </button>

      <button
        @click="handleSubmit"
        :disabled="isSubmitting"
        class="flex items-center gap-2 px-6 py-2.5 bg-orange-500 hover:bg-orange-400 text-white font-medium rounded-lg transition-colors disabled:opacity-60 disabled:cursor-not-allowed shadow-sm border-none cursor-pointer"
      >
        <span v-if="isSubmitting" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></span>
        <span>{{ isSubmitting ? 'Slanje...' : 'Objavi odgovor' }}</span>
      </button>
    </div>
  </div>
</template>