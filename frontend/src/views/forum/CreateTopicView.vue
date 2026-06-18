<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router'; 
import { createTopic, getCategories, uploadTopicAttachments } from '../../services/forum';
import ForumTopicTagManager from '../../components/ForumTopicTagManager.vue';

const router = useRouter(); 
const route = useRoute(); 

const title = ref('');
const selectedCategory = ref('');
const tags = ref([]); 
const content = ref('');
const isSubmitting = ref(false);
const errors = ref({});
const categories = ref([]);

const isAdmin = computed(() => localStorage.getItem('role') === 'admin');

const selectedFiles = ref([]);
const fileError = ref('');

const ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.pdf', '.docx', '.txt'];
const MAX_FILE_SIZE = 5 * 1024 * 1024;
const MAX_FILES = 3;

onMounted(async () => {
  if (isAdmin.value) {
    alert("Administratori ne mogu praviti redovne teme.");
    router.push('/forum'); 
    return;
  }
  try {
    categories.value = await getCategories();
    if (route.query.categoryId) {
      selectedCategory.value = parseInt(route.query.categoryId);
    }
  } catch (error) {
    console.error('Greška pri učitavanju kategorija:', error);
    categories.value = [
      { id: 1, name: 'Opšta diskusija' },
      { id: 2, name: 'Pomoć sa predmetima' },
      { id: 3, name: 'Studijske grupe' },
      { id: 4, name: 'Praksa i posao' },
      { id: 5, name: 'Projekti' },
      { id: 6, name: 'Off-Topic' },
    ];
  }
});

const validate = () => {
  errors.value = {};
  if (!title.value.trim()) errors.value.title = 'Naslov je obavezan.';
  else if (title.value.trim().length < 5) errors.value.title = 'Naslov mora imati najmanje 5 karaktera.';
  if (!selectedCategory.value) errors.value.category = 'Odaberite kategoriju.';
  if (!content.value.trim()) errors.value.content = 'Sadržaj je obavezan.';
  else if (content.value.trim().length < 10) errors.value.content = 'Sadržaj mora imati najmanje 10 karaktera.';
  return Object.keys(errors.value).length === 0;
};

const goBack = () => {
  router.push('/forum');
};

function handleFileSelect(event) {
  fileError.value = '';
  const files = Array.from(event.target.files);
  
  for (const file of files) {
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(ext)) {
      fileError.value = `Format ${ext} nije dozvoljen.`;
      return;
    }
    if (file.size > MAX_FILE_SIZE) {
      fileError.value = `Fajl "${file.name}" je prevelik. Max 5 MB.`;
      return;
    }
  }

  if (selectedFiles.value.length + files.length > MAX_FILES) {
    fileError.value = `Možete priložiti maksimalno ${MAX_FILES} fajla.`;
    return;
  }

  selectedFiles.value = [...selectedFiles.value, ...files];
}

function removeFile(index) {
  selectedFiles.value.splice(index, 1);
}

const submitTopic = async () => {
  if (!validate()) return;
  isSubmitting.value = true;
  errors.value.general = '';
  
  try {
    const newTopic = await createTopic({
      title: title.value.trim(),
      content: content.value.trim(),
      category_id: parseInt(selectedCategory.value),
      tags: tags.value,
    });

    if (selectedFiles.value.length > 0) {
      await uploadTopicAttachments(newTopic.id, selectedFiles.value);
    }

    router.push('/forum');
  } catch (error) {
    console.error("Kompletna greška sa backenda:", error);
    
    if (error.response && error.response.data && error.response.data.detail) {
      if (typeof error.response.data.detail === 'string') {
        errors.value.general = error.response.data.detail;
      } else if (Array.isArray(error.response.data.detail)) {
        errors.value.general = error.response.data.detail.map(d => `${d.loc.join('.')}: ${d.msg}`).join(', ');
      }
    } else {
      errors.value.general = error.message || 'Došlo je do serverske greške.';
    }
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-slate-900 p-6 transition-colors duration-200">
    <div class="max-w-4xl mx-auto">

      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center gap-3">
          <span class="text-orange-500 text-xl">💬</span>
          <div>
            <h1 class="text-2xl font-bold text-slate-800 dark:text-slate-100">Kreiraj novu temu</h1>
            <p class="text-slate-500 dark:text-slate-400 text-sm mt-0.5">Popunite formu ispod da biste kreirali novu temu diskusije</p>
          </div>
        </div>
        <button
          @click="goBack"
          class="flex items-center gap-2 px-4 py-2 rounded-lg border border-gray-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:bg-gray-100 dark:hover:bg-slate-700 transition-colors text-sm bg-white dark:bg-slate-800 shadow-sm"
        >
          ← Nazad
        </button>
      </div>

      <div class="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 shadow-sm p-8 space-y-6">

        <div v-if="errors.general" class="bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-900 text-red-600 dark:text-red-400 px-4 py-3 rounded-lg text-sm">
          {{ errors.general }}
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
            Naslov teme <span class="text-red-500">*</span>
          </label>
          <input
            v-model="title"
            type="text"
            maxlength="200"
            placeholder="Npr. Pitanje oko Fourierove transformacije - Signali i sistemi"
            class="w-full border rounded-lg px-4 py-2.5 text-slate-800 dark:text-slate-100 placeholder-gray-400 dark:placeholder-slate-500 bg-white dark:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-orange-400 transition-all"
            :class="errors.title ? 'border-red-400' : 'border-gray-200 dark:border-slate-600'"
          />
          <p v-if="errors.title" class="text-red-500 text-xs mt-1">{{ errors.title }}</p>
          <p v-else class="text-slate-400 dark:text-slate-500 text-xs mt-1">Budite što precizniji - dobar naslov pomaže drugim studentima da pronađu vašu temu</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
            Kategorija <span class="text-red-500">*</span>
          </label>
          <select
            v-model="selectedCategory"
            class="w-full border rounded-lg px-4 py-2.5 text-slate-800 dark:text-slate-100 bg-white dark:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-orange-400 transition-all"
            :class="errors.category ? 'border-red-400' : 'border-gray-200 dark:border-slate-600'"
          >
            <option value="" disabled>Izaberite kategoriju</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
          <p v-if="errors.category" class="text-red-500 text-xs mt-1">{{ errors.category }}</p>
        </div>

        <ForumTopicTagManager v-model="tags" />

        <!-- Attachments -->
        <div>
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
            Prilozi
          </label>

          <div class="flex items-center gap-3">
            <label class="cursor-pointer flex items-center gap-2 px-4 py-2 bg-white dark:bg-slate-700 border border-gray-200 dark:border-slate-600 rounded-lg text-sm text-slate-600 dark:text-slate-300 hover:bg-gray-50 dark:hover:bg-slate-600 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M18.375 12.739l-7.693 7.693a4.5 4.5 0 01-6.364-6.364l10.94-10.94A3 3 0 1119.5 7.372L8.552 18.32m.009-.01l-.01.01m5.699-9.941l-7.81 7.81a1.5 1.5 0 002.112 2.13" />
              </svg>
              Dodaj fajl
              <input
                type="file"
                multiple
                class="hidden"
                accept=".jpg,.jpeg,.png,.pdf,.docx,.txt"
                @change="handleFileSelect"
              />
            </label>
            <span class="text-xs text-slate-400">Max 3 fajla, 5 MB svaki. (.jpg, .png, .pdf, .docx, .txt)</span>
          </div>

          <p v-if="fileError" class="text-red-500 text-xs mt-1">{{ fileError }}</p>

          <ul v-if="selectedFiles.length > 0" class="mt-2 space-y-1">
            <li v-for="(file, index) in selectedFiles" :key="index" class="flex items-center justify-between text-xs bg-slate-50 dark:bg-slate-700 px-3 py-1.5 rounded-lg border border-gray-200 dark:border-slate-600">
              <span class="text-slate-600 dark:text-slate-300 truncate">📎 {{ file.name }} <span class="text-slate-400">({{ (file.size / 1024).toFixed(1) }} KB)</span></span>
              <button @click="removeFile(index)" class="text-red-400 hover:text-red-600 ml-2 font-bold text-sm bg-transparent border-none cursor-pointer">✕</button>
            </li>
          </ul>
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
            Sadržaj teme <span class="text-red-500">*</span>
          </label>
          <textarea
            v-model="content"
            rows="8"
            placeholder="Opišite vaše pitanje ili temu diskusije..."
            class="w-full border rounded-lg px-4 py-2.5 text-slate-800 dark:text-slate-100 placeholder-gray-400 dark:placeholder-slate-500 bg-white dark:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-orange-400 transition-all resize-y"
            :class="errors.content ? 'border-red-400' : 'border-gray-200 dark:border-slate-600'"
          />
          <p v-if="errors.content" class="text-red-500 text-xs mt-1">{{ errors.content }}</p>
          <p v-else class="text-slate-400 dark:text-slate-500 text-xs mt-1">Koristite markdown za formatiranje teksta. Budite detaljni i jasni.</p>
        </div>

        <div class="flex items-center justify-between pt-4 border-t border-gray-100 dark:border-slate-700">
          <button
            @click="goBack"
            class="px-6 py-2.5 rounded-lg border border-gray-200 dark:border-slate-600 text-slate-600 dark:text-slate-300 hover:bg-gray-50 dark:hover:bg-slate-700 transition-colors"
          >
            Otkaži
          </button>
          <button
            @click="submitTopic"
            :disabled="isSubmitting"
            class="flex items-center gap-2 px-6 py-2.5 bg-orange-500 hover:bg-orange-400 text-white font-medium rounded-lg transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
          >
            <span v-if="isSubmitting" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></span>
            <span>{{ isSubmitting ? 'Objavljivanje...' : '✓ Objavi temu' }}</span>
          </button>
        </div>

      </div>
    </div>
  </div>
</template>