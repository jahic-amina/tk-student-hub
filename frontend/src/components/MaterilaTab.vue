<template>
  <div class="w-full mb-8">
    <div class="flex gap-8 border-b border-gray-200">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        @click="$emit('tab-change', tab.id)"
        :class="[
          'pb-3 text-lg font-medium transition-all duration-200 relative',
          activeTab === tab.id 
            ? 'text-black' 
            : 'text-gray-400 hover:text-gray-600'
        ]"
      >
        {{ tab.name }}
        <div v-if="activeTab === tab.id" class="absolute bottom-0 left-0 w-full h-1 bg-black"></div>
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps(['activeTab']);
defineEmits(['tab-change']);

const tabs = [
  { id: 'all', name: 'Svi materijali' },
  { id: 'mine', name: 'Moji materijali' },
  { id: 'favorites', name: 'Najdraži materijali' }
];
</script>