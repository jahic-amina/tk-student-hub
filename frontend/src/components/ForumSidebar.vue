<script setup>
import { ref, onMounted } from 'vue'
import { getCategories } from '../services/forum.js' 

const emit = defineEmits(['kategorija-izabrana'])

defineProps({
  aktivnaKategorijaId: {
    type: Number,
    default: null
  }
})

const categories = ref([])
const loading = ref(true)

const fetchCategories = async () => {
  try {
    categories.value = await getCategories()
  } catch (error) {
    console.error('Greška:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCategories()
})
</script>

<template>
  <div class="w-full bg-white dark:bg-slate-800 p-6 rounded-2xl border border-gray-100 dark:border-slate-700/50 shadow-sm transition-colors duration-200">
    <h2 class="text-xl font-extrabold text-slate-800 dark:text-white mb-6 flex items-center">
      <span class="w-1.5 h-6 bg-[#ff7a00] mr-3 rounded-full"></span>
      Kategorije
    </h2>

    <div v-if="loading" class="space-y-4">
      <div v-for="i in 5" :key="i" class="h-10 bg-gray-100 dark:bg-slate-700 rounded-lg animate-pulse"></div>
    </div>

    <ul v-else class="space-y-1">
      <li 
        @click="emit('kategorija-izabrana', null)"
        class="flex items-center justify-between p-3 rounded-xl hover:bg-orange-50 dark:hover:bg-orange-950/20 transition-all cursor-pointer group"
        :class="{ 'bg-orange-50 dark:bg-orange-950/30 text-[#ff7a00]': aktivnaKategorijaId === null }"
      >
        <div class="flex items-center space-x-3">
          <span 
            class="w-2.5 h-2.5 rounded-full ring-2 ring-white dark:ring-slate-800 shadow-sm bg-slate-400"
            :class="{ '!bg-[#ff7a00]': aktivnaKategorijaId === null }"
          ></span>
          <span 
            class="text-[14px] font-bold text-slate-700 dark:text-slate-300 group-hover:text-[#ff7a00] transition-colors"
            :class="{ 'text-[#ff7a00]': aktivnaKategorijaId === null }"
          >
            Sve teme
          </span>
        </div>
      </li>

      <li 
        v-for="category in categories" 
        :key="category.id"
        @click="emit('kategorija-izabrana', category.id)"
        class="flex items-center justify-between p-3 rounded-xl hover:bg-orange-50 dark:hover:bg-orange-950/20 transition-all cursor-pointer group"
        :class="{ 'bg-orange-50 dark:bg-orange-950/30 text-[#ff7a00]': aktivnaKategorijaId === category.id }"
      >
        <div class="flex items-center space-x-3">
          <span 
            class="w-2.5 h-2.5 rounded-full ring-2 ring-white dark:ring-slate-800 shadow-sm" 
            :style="{ backgroundColor: category.color || '#ff7a00' }"
          ></span>
          
          <div class="flex flex-col">
            <span 
              class="text-[14px] font-bold text-slate-700 dark:text-slate-300 group-hover:text-[#ff7a00] transition-colors"
              :class="{ 'text-[#ff7a00]': aktivnaKategorijaId === category.id }"
            >
              {{ category.name }}
            </span>
          </div>
        </div>

        <span class="text-[11px] font-black bg-gray-100 dark:bg-slate-700 text-slate-500 dark:text-slate-400 px-2 py-1 rounded-lg group-hover:bg-[#ffb380] dark:group-hover:bg-orange-500 group-hover:text-white transition-colors">
          {{ category.topic_count || 0 }}
        </span>
      </li>
    </ul>

    <div class="mt-8 pt-6 border-t border-gray-100 dark:border-slate-700">
      <h3 class="text-xs font-black text-slate-400 dark:text-slate-500 uppercase tracking-widest mb-4">Popularni tagovi</h3>
      <div class="flex flex-wrap gap-2">
        <span class="text-[11px] font-bold bg-white dark:bg-slate-700 border border-gray-200 dark:border-slate-600 text-slate-500 dark:text-slate-300 px-3 py-1.5 rounded-full hover:border-[#ff7a00] hover:text-[#ff7a00] dark:hover:border-[#ff7a00] cursor-pointer transition-all">
          #telekomunikacije
        </span>
        <span class="text-[11px] font-bold bg-white dark:bg-slate-700 border border-gray-200 dark:border-slate-600 text-slate-500 dark:text-slate-300 px-3 py-1.5 rounded-full hover:border-[#ff7a00] hover:text-[#ff7a00] dark:hover:border-[#ff7a00] cursor-pointer transition-all">
          #mreze
        </span>
      </div>
    </div>
  </div>
</template>