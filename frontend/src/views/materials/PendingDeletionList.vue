<template>
  <div class="space-y-4 px-4">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-slate-900 dark:text-white uppercase tracking-wide">
        Odobri brisanje
      </h2>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
        Materijali na čekanju za brisanje
      </p>
    </div>

    <div v-if="loading" class="text-gray-500 dark:text-gray-400 py-4">
      Učitavanje materijala...
    </div>

    <div v-else-if="error" class="text-red-500 font-medium py-4">
      {{ error }}
    </div>

    <div v-else-if="materials.length === 0" class="text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-slate-800 p-6 rounded-lg text-center border border-dashed">
      Trenutno nema materijala koji čekaju na brisanje.
    </div>

    <div v-else class="space-y-4">
      <div 
        v-for="material in materials" 
        :key="material.id" 
        class="relative flex flex-col sm:flex-row sm:items-center justify-between border rounded-xl p-4 shadow-sm hover:shadow-md transition gap-4 dark:bg-slate-800 dark:border-slate-700"
      >
        <div class="flex flex-col sm:flex-row items-start gap-4 flex-1 cursor-pointer min-w-0" @click="$emit('open', material.id)">
          
          <div :class="['p-1 rounded-lg shrink-0 overflow-hidden w-20 h-24 flex items-center justify-center', material.thumbnail_path ? 'bg-gray-100' : 'bg-red-100 text-red-500']">
            <img 
              v-if="material.thumbnail_path" 
              :src="`http://127.0.0.1:8000/thumbnails/${material.thumbnail_path.split('/').pop()}`"
              class="w-full h-full object-contain rounded"
              alt="thumbnail"
            />
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
              class="lucide lucide-file-text w-8 h-8 text-destructive"
            >
              <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"></path>
              <path d="M14 2v4a2 2 0 0 0 2 2h4"></path>
              <path d="M10 9H8"></path>
              <path d="M16 13H8"></path>
              <path d="M16 17H8"></path>
            </svg>
          </div>
               
          <div class="min-w-0 overflow-hidden flex-1">
            <p class="font-semibold text-gray-800 dark:text-slate-100 truncate text-lg">{{ material.title }}</p>
            <p class="text-sm text-gray-500 dark:text-slate-400 mt-1">Postavio: {{ material.user?.full_name || material.user?.username || 'Nepoznato' }}</p>
            <p class="text-sm text-gray-500 dark:text-slate-400">Datum postavljanja: {{ formatDate(material.created_at) }}</p>
            <p class="text-sm text-gray-500 dark:text-slate-400 mt-1 font-medium text-slate-600 dark:text-slate-300">{{ material.subject?.name || 'Nema predmeta' }}</p>
          </div>

          <div class="flex flex-col items-start sm:items-center justify-center shrink-0 sm:px-4">
            <div class="flex items-center gap-1">
              <span v-for="star in 5" :key="star" class="text-yellow-400 text-lg">
                {{ star <= Math.round(material.average_rating || 0) ? '★' : '☆' }}
              </span>
              <span class="text-sm text-gray-500 dark:text-slate-400">({{ material.rating_count || 0 }})</span>
            </div>
            <p class="text-sm text-gray-500 dark:text-slate-400 mt-1">Broj preuzimanja: {{ material.number_of_downloads || 0 }}</p>
          </div>
        </div>

        <div class="flex flex-col gap-2 shrink-0 mr-8" @click.stop>
          <button 
            @click="handleApprove(material.id)"
            class="w-36 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors flex items-center justify-center gap-2 font-medium"
          >
            ✓ Odobri brisanje
          </button>
          <button 
            @click="handleReject(material.id)"
            class="w-36 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center justify-center gap-2 font-medium"
          >
            ✕ Odbij brisanje
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPendingDeletionMaterials, approveDeletion, rejectDeletion } from '../../services/api'

defineEmits(['open'])

const materials = ref([])
const loading = ref(true)
const error = ref(null)

async function fetchMaterials() {
  loading.value = true
  error.value = null
  try {
    const data = await getPendingDeletionMaterials()
    materials.value = Array.isArray(data) ? data : (data.materials || data.data || [])
  } catch (err) {
    error.value = err.message || 'Greška pri učitavanju materijala.'
  } finally {
    loading.value = false
  }
}

async function handleApprove(id) {
  if (confirm('Da li ste sigurni da želite odobriti BRISANJE ovog materijala?')) {
    try {
      await approveDeletion(id)
      await fetchMaterials()
    } catch (err) {
      alert('Greška pri odobravanju brisanja: ' + err.message)
    }
  }
}

async function handleReject(id) {
  if (confirm('Da li ste sigurni da želite odbiti brisanje?')) {
    try {
      await rejectDeletion(id)
      await fetchMaterials()
    } catch (err) {
      alert('Greška pri odbijanju brisanja: ' + err.message)
    }
  }
}

function formatDate(dateStr) {
  if (!dateStr) return 'N/A'
  const date = new Date(dateStr)
  return date.toLocaleDateString('bs-BA')
}

onMounted(() => {
  fetchMaterials()
})
</script>