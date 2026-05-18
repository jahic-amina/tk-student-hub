<template>
  <div class="inline-block">
    <button 
      v-if="mozeBrisati" 
      @click.stop="prikaziModal = true"
      class="flex items-center gap-1 bg-red-100 text-red-500 px-3 py-1.5 rounded-lg text-sm font-semibold hover:bg-red-200 transition"
    >
       Obriši
    </button>

    <div v-if="prikaziModal" @click.stop class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-xl max-w-sm w-full shadow-2xl border border-gray-100 text-left">
        <h3 class="text-lg font-bold text-gray-900 mb-2">Potvrda brisanja</h3>
        <p class="text-gray-600 text-sm mb-6">Da li ste sigurni da želite obrisati ovaj materijal?</p>
        
        <div class="flex justify-end gap-3">
          <button 
            @click="prikaziModal = false" 
            class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 text-sm font-medium hover:bg-gray-50 transition"
          >
            Otkaži
          </button>
          <button 
            @click="pokreniBrisanje" 
            :disabled="loading"
            class="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 transition disabled:opacity-50"
          >
            {{ loading ? 'Brisanje...' : 'Obriši' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { deleteMaterial } from '../services/api'

const props = defineProps({
  material: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['deleted'])

const prikaziModal = ref(false)
const loading = ref(false)

const token = localStorage.getItem('token')
const userString = localStorage.getItem('user')
const currentUser = userString ? JSON.parse(userString) : null

const mozeBrisati = computed(() => {
  if (!token || !currentUser) return false
  
  if (currentUser.role === 'admin' || currentUser.is_admin === true) return true
  
  return props.material.user_id === currentUser.id
})

async function pokreniBrisanje() {
  loading.value = true
  try {
    const response = await deleteMaterial(props.material.id)
    
    if (response.status === 204 || response.ok) {
      prikaziModal.value = false
      emit('deleted', props.material.id) 
    } else {
      alert("Nemate dozvolu za brisanje ovog materijala.")
    }
  } catch (error) {
    console.error("Greška pri brisanju:", error)
    alert("Došlo je do greške prilikom brisanja.")
  } finally {
    loading.value = false
  }
}
</script>