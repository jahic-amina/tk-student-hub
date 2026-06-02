<script setup>
import { ref, computed, onMounted } from 'vue';
import { getPopularTags } from '../services/forum';

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['update:modelValue']);

const tagInput = ref('');

const addTag = () => {
  const tag = tagInput.value.trim();
  if (!tag || props.modelValue.length >= 5 || props.modelValue.includes(tag)) return;
  
  const noviTagovi = [...props.modelValue, tag];
  emit('update:modelValue', noviTagovi);
  tagInput.value = '';
};

const removeTag = (index) => {
  const noviTagovi = [...props.modelValue];
  noviTagovi.splice(index, 1);
  emit('update:modelValue', noviTagovi);
};

const handleTagKeydown = (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    addTag();
  }
};

const popularTags = ref([]);
const showSuggestions = ref(false);

onMounted(async () => {
  try {
    popularTags.value = await getPopularTags();
    console.log('Tagovi:', popularTags.value);
  } catch (e) {
    console.warn('Nije moguće učitati popularne tagove.', e);
  }
});

const filteredSuggestions = computed(() => {
  const query = tagInput.value.trim().toLowerCase();
  return popularTags.value
    .filter(t => !props.modelValue.includes(t.name))
    .filter(t => !query || t.name.toLowerCase().includes(query))
    .slice(0, 6);
});

const addTagFromSuggestion = (tagName) => {
  if (!tagName || props.modelValue.length >= 5 || props.modelValue.includes(tagName)) return;
  emit('update:modelValue', [...props.modelValue, tagName]);
  showSuggestions.value = false;
};

</script>

<template>
  <div>
    <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Tagovi</label>
    
    <div class="relative">
      <div class="flex gap-2">
        <input
          v-model="tagInput"
          @keydown="handleTagKeydown"
          @focus="showSuggestions = true"
          @blur="setTimeout(() => showSuggestions = false, 150)"
          type="text"
          placeholder="Dodaj tag (pritisni Enter)"
          :disabled="modelValue.length >= 5"
          class="flex-1 border border-gray-200 dark:border-slate-600 rounded-lg px-4 py-2.5 text-slate-800 dark:text-slate-100 placeholder-gray-400 dark:placeholder-slate-500 bg-white dark:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-orange-400 transition-all disabled:opacity-50"
        />
        <button
          type="button"
          @click="addTag"
          :disabled="modelValue.length >= 5"
          class="px-4 py-2.5 bg-gray-100 dark:bg-slate-700 hover:bg-gray-200 dark:hover:bg-slate-600 border border-gray-200 dark:border-slate-600 text-slate-600 dark:text-slate-300 transition-colors disabled:opacity-50"
        >
          +
        </button>
      </div>

      <div
        v-if="showSuggestions && filteredSuggestions.length > 0 && modelValue.length < 5"
        class="absolute top-full left-0 right-0 mt-1 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-lg shadow-lg z-10 p-2"
      >
        <p class="text-[10px] text-slate-400 dark:text-slate-500 font-semibold uppercase tracking-wider px-2 mb-1.5">Popularni tagovi</p>
        <div class="flex flex-wrap gap-1.5 px-1">
          <button
            v-for="tag in filteredSuggestions"
            :key="tag.id"
            type="button"
            @mousedown.prevent="addTagFromSuggestion(tag.name)"
            class="text-xs px-2.5 py-1 rounded-full bg-orange-50 dark:bg-orange-950/40 text-orange-600 dark:text-orange-400 border border-orange-200 dark:border-orange-900/60 hover:bg-orange-100 dark:hover:bg-orange-900/60 transition-colors font-medium"
          >
            #{{ tag.name }}
            <span class="text-orange-400 dark:text-orange-500 ml-0.5 text-[9px]">({{ tag.usage_count }})</span>
          </button>
        </div>
      </div>
    </div>

    <div v-if="modelValue.length > 0" class="flex flex-wrap gap-2 mt-2">
      <span
        v-for="(tag, index) in modelValue"
        :key="index"
        class="flex items-center gap-1.5 bg-orange-50 dark:bg-orange-950/40 text-orange-600 dark:text-orange-400 border border-orange-200 dark:border-orange-900/60 px-3 py-1 rounded-full text-sm"
      >
        {{ tag }}
        <button type="button" @click="removeTag(index)" class="hover:text-orange-800 dark:hover:text-orange-200 transition-colors">×</button>
      </span>
    </div>
    <p class="text-slate-400 dark:text-slate-500 text-xs mt-1">Dodajte tagove da bi vaša tema bila lakše pronađena (maksimalno 5 tagova)</p>
  </div>
</template>