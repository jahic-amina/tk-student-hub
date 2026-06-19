<template>
  <div class="w-full mb-8">
    <div class="flex gap-8 border-b border-gray-200 dark:border-slate-700">
      <button v-for="tab in tabs" :key="tab.id" @click="$emit('tab-change', tab.id)" :class="[
        'pb-3 text-lg font-medium transition-all duration-200 relative',
        activeTab === tab.id
          ? 'text-black dark:text-white'
          : 'text-gray-400 hover:text-gray-600 dark:hover:text-slate-300'
      ]">
        {{ tab.name }}
        <div v-if="activeTab === tab.id" class="absolute bottom-0 left-0 w-full h-1 bg-black dark:bg-white"></div>
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps(['activeTab']);
defineEmits(['tab-change']);

const alltabs = [
  { id: 'all', name: 'Svi materijali' },
  { id: 'mine', name: 'Moji materijali' },
  { id: 'favorites', name: 'Najdraži materijali' }
];

const isLoggedIn = !!localStorage.getItem('token')

const allTabs = [
  { id: 'all', name: 'Svi materijali' },
  { id: 'mine', name: 'Moji materijali' },
  { id: 'favorites', name: 'Najdraži materijali' }
]

const tabs = isLoggedIn ? allTabs : allTabs.filter(t => t.id === 'all')
</script>