<template>
  <div class="bg-white p-5 rounded-lg shadow-sm border border-gray-100 w-64 min-w-[256px] max-w-[256px] flex-shrink-0 h-fit">
    <h2 class="text-lg font-bold mb-4 uppercase text-gray-800 border-b pb-2">Filteri</h2>

    <div class="mb-6">
      <h3 class="text-xs font-bold text-gray-400 uppercase mb-2">Godina studija</h3>
      <div class="flex flex-col gap-2">
        <label v-for="year in [1, 2, 3, 4]" :key="year" class="flex items-center gap-2 cursor-pointer hover:bg-gray-50 p-1 rounded transition-colors">
          <input type="checkbox" :value="year" v-model="filters.years" @change="update" class="rounded text-orange-500 focus:ring-orange-500">
          <span class="text-gray-700 text-sm font-medium">{{ year }}. godina</span>
        </label>
      </div>
    </div>

    <div class="mb-6">
      <h3 class="text-xs font-bold text-gray-400 uppercase mb-2">Tip materijala</h3>
      <div class="flex flex-col gap-2">
        <label v-for="(label, val) in typesMap" :key="val" class="flex items-center gap-2 cursor-pointer hover:bg-gray-50 p-1 rounded transition-colors">
          <input type="checkbox" :value="val" v-model="filters.types" @change="update" class="rounded text-orange-500 focus:ring-orange-500">
          <span class="text-gray-700 uppercase text-xs font-medium">{{ label }}</span>
        </label>
      </div>
    </div>

    <div>
      <h3 class="text-xs font-bold text-gray-400 uppercase mb-2">Odaberi predmet</h3>
      <select v-model="filters.subject_id" @change="update" class="w-full p-2 border border-gray-200 rounded text-sm outline-none focus:border-orange-500 transition-colors bg-gray-50">
        <option :value="null">Svi predmeti</option>
        <option v-for="s in subjects" :key="s.id" :value="s.id">{{ s.name }}</option>
      </select>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getSubjects } from '../services/api'

const emit = defineEmits(['change'])
const subjects = ref([])

// Ključevi (lijevo) MORAJU odgovarati vrijednostima u bazi (kolona file_type)
const typesMap = {
  'skripta': 'Skripte',
  'biljeske': 'Bilješke',
  'auditorne_vjezbe': 'Auditorne vježbe',
  'ispiti': 'Ispiti'
}

const filters = reactive({ 
  years: [], 
  types: [], 
  subject_id: null 
})

onMounted(async () => { 
  try {
    subjects.value = await getSubjects() 
  } catch (e) {
    console.error("Greška pri učitavanju predmeta:", e)
  }
})

function update() { 
  // Šaljemo kopiju roditelju
  emit('change', JSON.parse(JSON.stringify(filters))) 
}
</script>