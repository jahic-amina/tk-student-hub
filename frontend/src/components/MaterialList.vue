<template>
  <div class="max-w-7xl mx-auto flex flex-col md:flex-row gap-8 items-start justify-start p-6 w-full">
    
    <MaterialFilter @change="handleFilterChange" />

    <div class="flex-grow min-w-0">
      <h1 class="text-2xl font-bold uppercase mb-1">Pregled materijala</h1>
      <p class="text-sm text-gray-500 mb-6">Dostupni materijal</p>

      <div v-if="loading">Učitavanje...</div>

      <div v-else>
        <div v-if="materials.length > 0" class="flex flex-col gap-4">
          <MaterialCard 
            v-for="material in materials" 
            :key="material.id" 
            :material="material"
          />
        </div>

        <div v-else class="w-full py-20 text-left"> 
          <p class="text-gray-500 text-lg">Nema materijala za odabrane filtere.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import MaterialCard from './MaterialCard.vue'
import { getMaterials } from '../services/api'
import MaterialFilter from './MaterialFilter.vue'
defineEmits(['open', 'deleted'])

const materials = ref([])
const loading = ref(true)

async function loadMaterials(filters = {}) {
    loading.value = true
    materials.value = await getMaterials(filters)
    loading.value = false
}

//onMounted(async () => {
    //materials.value = await getMaterials()
  //  loading.value = false
//})
onMounted(() => { loadMaterials() })

async function handleFilterChange(newFilters) {
    console.log("Filteri primljeni od djeteta:", newFilters); // PROVJERI OVO U KONZOLI
    await loadMaterials(newFilters);
}
function handleDelete(deletedMaterialId) {
    materials.value = materials.value.filter(m => m.id !== deletedMaterialId)
}
</script>