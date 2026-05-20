<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router'; // 🚀 Uvozimo ruter za navigaciju
import { createTopic } from '../../services/forum';

const router = useRouter(); // 🚀 Inicijalizacija rutera

const title = ref('');
const selectedCategory = ref('');
const tagInput = ref('');
const tags = ref([]);
const content = ref('');
const isSubmitting = ref(false);
const errors = ref({});

const categories = [
  { id: 1, name: 'Opšta diskusija' },
  { id: 2, name: 'Pomoć sa predmetima' },
  { id: 3, name: 'Studijske grupe' },
  { id: 4, name: 'Praksa i posao' },
  { id: 5, name: 'Projekti' },
  { id: 6, name: 'Off-Topic' },
];

const addTag = () => {
  const tag = tagInput.value.trim();
  if (!tag || tags.value.length >= 5 || tags.value.includes(tag)) return;
  tags.value.push(tag);
  tagInput.value = '';
};

const removeTag = (index) => {
  tags.value.splice(index, 1);
};

const handleTagKeydown = (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    addTag();
  }
};

const validate = () => {
  errors.value = {};
  if (!title.value.trim()) errors.value.title = 'Naslov je obavezan.';
  else if (title.value.trim().length < 5) errors.value.title = 'Naslov mora imati najmanje 5 karaktera.';
  if (!selectedCategory.value) errors.value.category = 'Odaberite kategoriju.';
  if (!content.value.trim()) errors.value.content = 'Sadržaj je obavezan.';
  else if (content.value.trim().length < 10) errors.value.content = 'Sadržaj mora imati najmanje 10 karaktera.';
  return Object.keys(errors.value).length === 0;
};

// 🚀 Funkcija za povratak na forum
const goBack = () => {
  router.push('/forum');
};

const submitTopic = async () => {
  if (!validate()) return;
  isSubmitting.value = true;
  try {
    // 🚀 Sada šaljemo stvarne tagove iz niza (tags.value), a ne prazan niz []
    await createTopic({
      title: title.value.trim(),
      content: content.value.trim(),
      category_id: parseInt(selectedCategory.value),
      tags: tags.value, 
    });
    
    // 🚀 Nakon uspješne objave, ruter nas vraća na listu tema
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

        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Tagovi</label>
          <div class="flex gap-2">
            <input
              v-model="tagInput"
              @keydown="handleTagKeydown"
              type="text"
              placeholder="Dodaj tag (pritisni Enter)"
              :disabled="tags.length >= 5"
              class="flex-1 border border-gray-200 rounded-lg px-4 py-2.5 text-slate-800 placeholder-gray-400 bg-white focus:outline-none focus:ring-2 focus:ring-orange-400 transition-all disabled:opacity-50"
            />
            <button
              @click="addTag"
              :disabled="tags.length >= 5"
              class="px-4 py-2.5 bg-gray-100 hover:bg-gray-200 border border-gray-200 rounded-lg text-slate-600 transition-colors disabled:opacity-50"
            >
              +
            </button>
          </div>
          <div v-if="tags.length > 0" class="flex flex-wrap gap-2 mt-2">
            <span
              v-for="(tag, index) in tags"
              :key="index"
              class="flex items-center gap-1.5 bg-orange-50 text-orange-600 border border-orange-200 px-3 py-1 rounded-full text-sm"
            >
              {{ tag }}
              <button @click="removeTag(index)" class="hover:text-orange-800 transition-colors">×</button>
            </span>
          </div>
          <p class="text-slate-400 text-xs mt-1">Dodajte tagove da bi vaša tema bila lakše pronađena (maksimalno 5 tagova)</p>
        </div>

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