<script setup>
import { ref, onMounted } from 'vue'

import { getCategories } from '@/services/forum' 

const categories = ref([])
const loading = ref(true)

const fetchCategories = async () => {
  try {

    categories.value = await getCategories()
  } catch (error) {
    console.error('Greška pri dohvatanju kategorija:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCategories()
})
</script>

<template>
  <div class="w-full md:w-64 bg-slate-800 p-5 rounded-xl border border-slate-700/50 shadow-md">
    <h2 class="text-lg font-bold text-white mb-4 pb-2 border-b border-slate-700">
      Kategorije
    </h2>

    <div v-if="loading" class="text-sm text-slate-400 animate-pulse">
      Učitavanje kategorija...
    </div>

    <ul v-else class="space-y-2 mb-6">
      <li 
        v-for="category in categories" 
        :key="category.id"
        class="flex items-center justify-between p-2 rounded-lg hover:bg-slate-700/50 transition cursor-pointer group"
      >
        <div class="flex items-center space-x-3">
          <span 
            class="w-3 h-3 rounded-full flex-shrink-0" 
            :style="{ backgroundColor: category.color }"
          ></span>
          
          <div class="flex flex-col">
            <span class="text-sm font-medium text-slate-200 group-hover:text-blue-400 transition">
              {{ category.name }}
            </span>
            <span class="text-xs text-slate-400 line-clamp-1">
              {{ category.description }}
            </span>
          </div>
        </div>

        <span class="text-xs bg-slate-700 text-slate-300 px-2 py-1 rounded-md font-semibold">
          {{ category.topic_count }}
        </span>
      </li>
    </ul>

    <div class="mt-6 border-t border-slate-700 pt-4">
      <h3 class="text-sm font-bold text-slate-300 mb-3">Popularni tagovi</h3>
      <div class="flex flex-wrap gap-2">
        <span class="text-xs bg-slate-700/30 border border-slate-700 text-slate-400 px-2 py-1 rounded hover:border-blue-500 hover:text-blue-400 cursor-pointer transition">
          #telekomunikacije
        </span>
        <span class="text-xs bg-slate-700/30 border border-slate-700 text-slate-400 px-2 py-1 rounded hover:border-blue-500 hover:text-blue-400 cursor-pointer transition">
          #mreze
        </span>
      </div>
    </div>
  </div>
</template>