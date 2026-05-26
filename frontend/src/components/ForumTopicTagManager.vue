<script setup>
import { ref } from 'vue';

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
</script>

<template>
  <div>
    <label class="block text-sm font-medium text-slate-700 mb-1">Tagovi</label>
    <div class="flex gap-2">
      <input
        v-model="tagInput"
        @keydown="handleTagKeydown"
        type="text"
        placeholder="Dodaj tag (pritisni Enter)"
        :disabled="modelValue.length >= 5"
        class="flex-1 border border-gray-200 rounded-lg px-4 py-2.5 text-slate-800 placeholder-gray-400 bg-white focus:outline-none focus:ring-2 focus:ring-orange-400 transition-all disabled:opacity-50"
      />
      <button
        type="button"
        @click="addTag"
        :disabled="modelValue.length >= 5"
        class="px-4 py-2.5 bg-gray-100 hover:bg-gray-200 border border-gray-200 rounded-lg text-slate-600 transition-colors disabled:opacity-50"
      >
        +
      </button>
    </div>
    
    <div v-if="modelValue.length > 0" class="flex flex-wrap gap-2 mt-2">
      <span
        v-for="(tag, index) in modelValue"
        :key="index"
        class="flex items-center gap-1.5 bg-orange-50 text-orange-600 border border-orange-200 px-3 py-1 rounded-full text-sm"
      >
        {{ tag }}
        <button type="button" @click="removeTag(index)" class="hover:text-orange-800 transition-colors">×</button>
      </span>
    </div>
    <p class="text-slate-400 text-xs mt-1">Dodajte tagove da bi vaša tema bila lakše pronađena (maksimalno 5 tagova)</p>
  </div>
</template>