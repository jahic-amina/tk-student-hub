<<template>
  <div class="bg-white dark:bg-slate-800 p-5 rounded-lg shadow-sm border border-gray-100 dark:border-slate-700 w-64 min-w-[256px] max-w-[256px] flex-shrink-0 h-fit">
    <h2 class="text-lg font-bold mb-4 uppercase text-gray-800 dark:text-slate-100 border-b dark:border-slate-700 pb-2">Filteri</h2>
    <div class="mb-6">
      <h3 class="text-xs font-bold text-gray-400 dark:text-slate-400 uppercase mb-2">Godina studija</h3>
      <div class="flex flex-col gap-2">
        <label v-for="year in [1, 2, 3, 4]" :key="year" class="flex items-center gap-2 cursor-pointer hover:bg-gray-50 dark:hover:bg-slate-700 p-1 rounded transition-colors">
          <input type="checkbox" :value="year" v-model="filters.years" @change="update" class="rounded text-orange-500 focus:ring-orange-500">
          <span class="text-gray-700 dark:text-slate-300 text-sm font-medium">{{ year }}. godina</span>
        </label>
      </div>
    </div>
    <div class="mb-6">
      <h3 class="text-xs font-bold text-gray-400 dark:text-slate-400 uppercase mb-2">Tip materijala</h3>
      <div class="flex flex-col gap-2">
        <label v-for="(label, val) in typesMap" :key="val" class="flex items-center gap-2 cursor-pointer hover:bg-gray-50 dark:hover:bg-slate-700 p-1 rounded transition-colors">
          <input type="checkbox" :value="val" v-model="filters.types" @change="update" class="rounded text-orange-500 focus:ring-orange-500">
          <span class="text-gray-700 dark:text-slate-300 uppercase text-xs font-medium">{{ label }}</span>
        </label>
      </div>
    </div>
    <div>
      <h3 class="text-xs font-bold text-gray-400 dark:text-slate-400 uppercase mb-2">Odaberi predmet</h3>
      <select v-model="filters.subject_id" @change="update" class="w-full p-2 border border-gray-200 dark:border-slate-600 rounded text-sm outline-none focus:border-orange-500 transition-colors bg-gray-50 dark:bg-slate-700 dark:text-slate-200">
        <option :value="null">Svi predmeti</option>
        <option v-for="s in filteredSubjects" :key="s.id" :value="s.id">{{ s.name }}</option>
      </select>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { getSubjects } from '../services/api'

const emit = defineEmits(['change'])
const subjects = ref([])

const typesMap = {
  'skripta': 'Skripte',
  'auditorne_vjezbe': 'Auditorne vježbe',
  'laboratorijske_vjezbe': 'Laboratorijske vježbe',
  'ispiti': 'Ispiti',
  'projekat': 'Projekat'
}

const filters = reactive({ 
  years: [], 
  types: [], 
  subject_id: null 
})

const filteredSubjects = computed(() => {
  if (!filters.years.length) return subjects.value

  const selectedYears = filters.years.map(Number)
  return subjects.value.filter(subject => selectedYears.includes(Number(subject.study_year)))
})

watch(
  () => filters.years.slice(),
  () => {
    if (!filters.subject_id) return

    const isSelectedSubjectValid = filteredSubjects.value.some(
      subject => Number(subject.id) === Number(filters.subject_id)
    )

    if (!isSelectedSubjectValid) {
      filters.subject_id = null
      update()
    }
  }
)

onMounted(async () => { 
  try {
    subjects.value = await getSubjects() 
  } catch (e) {
    console.error("Greška pri učitavanju predmeta:", e)
  }
})

function update() { 
  
  emit('change', JSON.parse(JSON.stringify(filters))) 
}
</script>