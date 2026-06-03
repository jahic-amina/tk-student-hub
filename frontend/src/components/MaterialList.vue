<template>
  <div class="max-w-7xl mx-auto flex flex-col md:flex-row gap-8 items-start justify-start p-6 w-full">
    
    <MaterialFilter @change="handleFilterChange" />

    <div class="flex-grow min-w-0">
      <MaterialTabs 
        v-if="userRole !== 'admin'" 
        :activeTab="currentTab" 
        @tab-change="handleTabChange" 
      />

      <h1 class="text-2xl font-bold uppercase mb-1">Pregled materijala</h1>
      <p class="text-sm text-gray-500 mb-6">Dostupni materijal</p>

      <div v-if="loading">Učitavanje...</div>

      <div v-else>
        <div v-if="filteredMaterials.length > 0" class="flex flex-col gap-4">
          <MaterialCard 
            v-for="material in filteredMaterials" 
            :key="material.id" 
            :material="material"
            @click="$router.push(`/materials/${$event}`)"
            @deleted="handleDelete"
          />
        </div>

        <div v-else class="w-full py-20 text-left"> 
          <p class="text-gray-500 text-lg">Nema materijala za ovaj prikaz.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import MaterialCard from './MaterialCard.vue'
import { getMaterials } from '../services/api'
import MaterialFilter from './MaterialFilter.vue'
import MaterialTabs from './MaterilaTab.vue'

const materials = ref([])
const loading = ref(true)
const currentTab = ref('all')

const userRaw = localStorage.getItem('user');
const currentUser = userRaw ? JSON.parse(userRaw) : null;
const currentUserId = ref(currentUser ? currentUser.id : null);
const userRole = ref(localStorage.getItem('role') || 'member');

async function loadMaterials(filters = {}) {
    loading.value = true
    materials.value = await getMaterials(filters)
    loading.value = false
}

onMounted(() => { 
    loadMaterials();
    console.log("Ulogovan korisnik ID:", currentUserId.value);
})

function handleTabChange(tabId) {
    currentTab.value = tabId;
}
const filteredMaterials = computed(() => {
  if (currentTab.value === 'mine') {
    return materials.value.filter(m => {
      const autorId = m.user?.id; 
      const mojId = currentUserId.value;

      return Number(autorId) === Number(mojId);
    });
  }
  
  if (currentTab.value === 'favorites') {
    return []; 
  }

  return materials.value;
});
async function handleFilterChange(newFilters) {
    await loadMaterials(newFilters);
}

function handleDelete(deletedMaterialId) {
    materials.value = materials.value.filter(m => m.id !== deletedMaterialId)
}
</script>