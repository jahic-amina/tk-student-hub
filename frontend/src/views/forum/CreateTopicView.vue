<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router'; 
import { createTopic, getCategories } from '../../services/forum';
import ForumTopicTagManager from './components/ForumTopicTagManager.vue'; // Nova komponenta

const router = useRouter(); 
const route = useRoute(); 

const title = ref('');
const selectedCategory = ref('');
const tags = ref([]); // Ovaj niz se sada puni direktno kroz v-model iz komponente
const content = ref('');
const isSubmitting = ref(false);
const errors = ref({});
const categories = ref([]);

onMounted(async () => {
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

const submitTopic = async () => {
  if (!validate()) return;
  isSubmitting.value = true;
  try {
    await createTopic({
      title: title.value.trim(),
      content: content.value.trim(),
      category_id: parseInt(selectedCategory.value),
      tags: tags.value, 
    });
    router.push('/forum');
  } catch (error) {
    errors.value.general = 'Došlo je do greške. Pokušajte ponovo.';
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-4xl mx-auto">

      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center gap-3">
          <span class="text-orange-500 text-xl">💬</span>
          <div>
            <h1 class="text-2xl font-bold text-slate-800">Kreiraj novu temu</h1>
            <p class="text-slate-500 text-sm mt-0.5">Popunite formu ispod da biste kreirali novu temu diskusije</p>
          </div>
        </div>
        <button
          @click="goBack"
          class="flex items-center gap-2 px-4 py-2 rounded-lg border border-gray-200 text-slate-600 hover:bg-gray-100 transition-colors text-sm bg-white"
        >
          ← Nazad
        </button>
      </div>

      <div class="bg-white rounded-xl border border-gray-200 shadow-sm p-8 space-y-6">

        <div v-if="errors.general" class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg text-sm">
          {{ errors.general }}
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">
            Naslov teme <span class="text-red-500">*</span>
          </label>
          <input
            v-model="title"
            type="text"
            maxlength="200"
            placeholder="Npr. Pitanje oko Fourierove transformacije - Signali i sistemi"
            class="w-full border rounded-lg px-4 py-2.5 text-slate-800 placeholder-gray-400 bg-white focus:outline-none focus:ring-2 focus:ring-orange-400 transition-all"
            :class="errors.title ? 'border-red-400' : 'border-gray-200'"
          />
          <p v-if="errors.title" class="text-red-500 text-xs mt-1">{{ errors.title }}</p>
          <p v-else class="text-slate-400 text-xs mt-1">Budite što precizniji - dobar naslov pomaže drugim studentima da pronađu vašu temu</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">
            Kategorija <span class="text-red-500">*</span>
          </label>
          <select
            v-model="selectedCategory"
            class="w-full border rounded-lg px-4 py-2.5 text-slate-800 bg-white focus:outline-none focus:ring-2 focus:ring-orange-400 transition-all"
            :class="errors.category ? 'border-red-400' : 'border-gray-200'"
          >
            <option value="" disabled>Izaberite kategoriju</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
          <p v-if="errors.category" class="text-red-500 text-xs mt-1">{{ errors.category }}</p>
        </div>

        <TopicTagManager v-model="tags" />

        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">
            Sadržaj teme <span class="text-red-500">*</span>
          </label>
          <textarea
            v-model="content"
            rows="8"
            placeholder="Opišite vaše pitanje ili temu diskusije..."
            class="w-full border rounded-lg px-4 py-2.5 text-slate-800 placeholder-gray-400 bg-white focus:outline-none focus:ring-2 focus:ring-orange-400 transition-all resize-y"
            :class="errors.content ? 'border-red-400' : 'border-gray-200'"
          />
          <p v-if="errors.content" class="text-red-500 text-xs mt-1">{{ errors.content }}</p>
          <p v-else class="text-slate-400 text-xs mt-1">Koristite markdown za formatiranje teksta. Budite detaljni i jasni.</p>
        </div>

        <div class="flex items-center justify-between pt-4 border-t border-gray-100">
          <button
            @click="goBack"
            class="px-6 py-2.5 rounded-lg border border-gray-200 text-slate-600 hover:bg-gray-50 transition-colors"
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