<template>
  <div class="max-w-7xl mx-auto py-8 px-4 font-sans bg-gray-50 min-h-screen">
    
    <div class="flex flex-col md:flex-row gap-8 items-start">
      
      <aside class="w-full md:w-64 bg-white p-6 rounded-lg shadow-sm border border-gray-100 flex-shrink-0">
        <h2 class="text-lg font-bold uppercase tracking-wider text-gray-800 mb-6 border-b pb-2">Filteri</h2>
        
        <div class="mb-6">
          <label class="block text-xs font-bold text-gray-400 uppercase mb-3">Godina studija</label>
          <div class="space-y-2">
            <label v-for="year in [1, 2, 3, 4]" :key="year" class="flex items-center text-gray-700 text-sm cursor-pointer">
              <input type="checkbox" :value="year" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500 mr-3 w-4 h-4" />
              {{ year }}
            </label>
          </div>
        </div>

        <div class="mb-6">
          <label class="block text-xs font-bold text-gray-400 uppercase mb-3">Tip materijala</label>
          <div class="space-y-2">
            <label v-for="type in ['SKRIPTE', 'BILJEŠKE', 'VJEŽBE', 'ISPITI']" :key="type" class="flex items-center text-gray-700 text-sm cursor-pointer">
              <input type="checkbox" :value="type" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500 mr-3 w-4 h-4" />
              {{ type }}
            </label>
          </div>
        </div>

        <div class="mb-6">
          <label class="block text-xs font-bold text-gray-400 uppercase mb-2">Odaberi predmet</label>
          <select class="w-full bg-gray-50 border border-gray-300 text-gray-700 py-2 px-3 rounded-lg text-sm focus:ring-blue-500 focus:border-blue-500">
            <option value="">Svi predmeti</option>
          </select>
        </div>

        <button class="w-full mt-4 bg-black text-white font-bold py-3 px-4 rounded-lg uppercase text-xs tracking-wider hover:bg-gray-800 transition shadow-md flex items-center justify-center gap-2">
          <span>+</span> Dodajte materijal
        </button>
      </aside>

      <main class="flex-1 w-full">
        <div class="mb-6">
          <h1 class="text-2xl font-bold uppercase tracking-wide text-gray-900">Pregled materijala</h1>
          <p class="text-xs text-gray-400 uppercase font-semibold mt-1">Dostupni materijal</p>
        </div>

        <div v-if="materials.length > 0" class="space-y-4">
          <div 
            v-for="material in materials" 
            :key="material.id" 
            class="bg-white p-5 rounded-xl shadow-sm border border-gray-100 flex justify-between items-center hover:shadow-md transition"
          >
            <div class="flex items-start gap-4">
              <div class="p-3 bg-red-50 text-red-500 rounded-xl">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <h3 class="font-bold text-gray-800 text-lg">{{ material.title }}</h3>
                <p class="text-gray-500 text-sm mt-1">{{ material.description || 'Nema opisa.' }}</p>
                <div class="flex gap-4 text-xs text-gray-400 mt-3">
                  <span>Ko je postavio: <strong class="text-gray-600">{{ material.user?.full_name || 'Anonimno' }}</strong></span>
                  <span>Datum postavljanja: <strong class="text-gray-600">{{ formatDate(material.created_at) }}</strong></span>
                </div>
              </div>
            </div>

            <div class="flex flex-col items-end gap-2">
              <button 
                v-if="isAdmin" 
                @click="triggerDeleteConfirmation(material.id)"
                class="px-4 py-1.5 border border-red-200 text-red-500 bg-red-50 rounded-lg text-xs font-bold uppercase tracking-wider hover:bg-red-100 transition"
              >
                Obriši
              </button>
              
              <button class="px-5 py-2 border border-gray-300 text-gray-700 bg-white rounded-lg text-xs font-bold uppercase tracking-wider hover:bg-gray-50 transition flex items-center gap-2">
                Preuzmi
              </button>
            </div>
          </div>
        </div>

        <div v-else class="bg-white border border-gray-100 rounded-xl p-12 text-center shadow-sm">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-gray-300 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
          </svg>
          <p class="text-gray-500 font-medium text-lg">Trenutno nema dostupnog materijala.</p>
          <p class="text-gray-400 text-sm mt-1">Pokušajte promijeniti filtere ili dodajte novi materijal.</p>
        </div>

      </main>
    </div>

    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50 animate-fade-in">
      <div class="bg-white p-6 rounded-xl max-w-sm w-full shadow-2xl border border-gray-100">
        <h3 class="text-lg font-bold text-gray-900 mb-2">Potvrda brisanja</h3>
        <p class="text-gray-600 text-sm mb-6">Da li ste sigurni da želite obrisati ovaj sadržaj?</p>
        <div class="flex justify-end gap-3">
          <button @click="showDeleteModal = false" class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 text-sm font-medium hover:bg-gray-50 transition">
            Otkaži
          </button>
          <button @click="confirmDelete" class="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 transition shadow-sm">
            Obriši
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getMaterials, deleteMaterial } from '../../services/api'

const materials = ref([])
const showDeleteModal = ref(false)
const materialIdToDelete = ref(null)

const isAdmin = computed(() => true)

onMounted(async () => {
  try {
    const data = await getMaterials()
    materials.value = data.filter(m => m.status !== 'deleted')
  } catch (error) {
    console.error("Greška pri učitavanju:", error)
  }
})

function triggerDeleteConfirmation(id) {
  materialIdToDelete.value = id
  showDeleteModal.value = true
}

async function confirmDelete() {
  if (!materialIdToDelete.value) return
  try {
    const response = await deleteMaterial(materialIdToDelete.value)
    
    if (response.status === 204 || response.ok) {
      materials.value = materials.value.filter(m => m.id !== materialIdToDelete.value)
      showDeleteModal.value = false
      materialIdToDelete.value = null
    }
  } catch (error) {
    alert("Došlo je do greške prilikom brisanja.")
  }
}

function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('bs-BA') 
}
</script>