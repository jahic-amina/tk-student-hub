<template>
  <div class="w-full">
    <button 
      v-if="mozeBrisati" 
      @click.stop="prikaziModal = true"
      class="flex items-center justify-center gap-2 bg-red-100 text-red-500 w-full px-4 py-2 rounded-lg text-sm font-medium hover:bg-red-200 transition shadow-sm border border-red-200/50"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-trash-2">
        <path d="M3 6h18"></path>
        <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
        <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
        <line x1="10" x2="10" y1="11" y2="17"></line>
        <line x1="14" x2="14" y1="11" y2="17"></line>
      </svg>
      Obriši
    </button>

    <div v-if="prikaziModal" @click.stop class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-slate-800 p-6 rounded-xl max-w-sm w-full shadow-2xl border border-gray-100 dark:border-slate-700 text-left">
    <h3 class="text-lg font-bold text-gray-900 dark:text-slate-100 mb-2">Potvrda brisanja</h3>
    <p class="text-gray-600 dark:text-slate-300 text-sm mb-6">Da li ste sigurni da želite obrisati ovaj materijal?</p>
    <div class="flex justify-end gap-3">
        <button @click="prikaziModal = false" 
            class="px-4 py-2 border border-gray-300 dark:border-slate-600 rounded-lg text-gray-700 dark:text-slate-200 text-sm font-medium hover:bg-gray-50 dark:hover:bg-slate-700 transition">
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
  
  const autorId = props.material.user_id || (props.material.user && props.material.user.id);
  const ulogovaniId = currentUser.id || currentUser.user_id;

  if (autorId && ulogovaniId && autorId == ulogovaniId) {
    return true;
  }

  const trenutnoIme = localStorage.getItem('username');
  const autorIme = props.material.user?.full_name;

  if (trenutnoIme && autorIme && trenutnoIme.trim().toLowerCase() === autorIme.trim().toLowerCase()) {
    return true;
  }

  return false;
})

async function pokreniBrisanje() {
  loading.value = true
  try {
    const response = await deleteMaterial(props.material.id)
    
    if (response && (response.status === 204 || response.status === 200)) {
      prikaziModal.value = false
      emit('deleted', props.material.id) 
    } else {
      alert("Nemate dozvolu za brisanje ovog materijala.")
    }
  } catch (error) {
    if (error.response && error.response.status === 403) {
      alert("Nemate dozvolu za brisanje ovog materijala.")
    } else {
      alert("Došlo je do greške prilikom brisanja.")
    }
  } finally {
    loading.value = false
  }
}
</script>