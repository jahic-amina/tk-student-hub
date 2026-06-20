<template>
  <div class="w-full flex flex-col md:flex-row gap-8 items-start justify-start py-6 px-4">

    <div class="flex-grow min-w-0 w-full pr-4">
      <MaterialTabs v-if="userRole !== 'admin'" :activeTab="currentTab" @tab-change="handleTabChange" />

      <h1 class="text-2xl font-bold uppercase mb-1">Pregled materijala</h1>
      <p class="text-sm text-gray-500 mb-6">Dostupni materijal</p>

      <div v-if="loading">Učitavanje...</div>

      <div v-else>
        
        <div v-if="filteredMaterialsBookmark.length > 0" class="flex flex-col gap-4">
          <MaterialCard 
            v-for="material in prikazaniMaterijali" 
            :key="material.id" 
            :material="material"
            :user-role="userRole"
            @click="$router.push(`/materials/${$event}`)"
            @deleted="handleDelete"
            @toggle-bookmark="handleToggleBookmark"
            @downloaded="handleDownloaded"
          />

          <div v-if="ukupnoStranicaPrikaz >= 1" class="flex justify-center items-center gap-2 mt-6">
            <button
              @click="promijeniStranicu(trenutnastranica - 1)"
              :disabled="trenutnastranica === 1"
              class="px-3 py-1 rounded-lg border text-sm text-gray-600 hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              ←
            </button>
            <button
              v-for="br in ukupnoStranicaPrikaz"
              :key="br"
              @click="promijeniStranicu(br)"
              :class="[
                'px-3 py-1 rounded-lg border text-sm transition',
                br === trenutnastranica 
                  ? 'bg-primary text-white border-primary' 
                  : 'text-gray-600 hover:bg-gray-100'
              ]"
            >
              {{ br }}
            </button>
            <button
              @click="promijeniStranicu(trenutnastranica + 1)"
              :disabled="trenutnastranica === ukupnoStranicaPrikaz"
              class="px-3 py-1 rounded-lg border text-sm text-gray-600 hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              →
            </button>
          </div>
        </div>

        <div v-else class="w-full py-20 text-left">
          <p class="text-gray-500 text-lg">Nema materijala za ovaj prikaz.</p>
        </div>

      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import MaterialCard from './MaterialCard.vue'
import { getMaterials, getPublicMaterials, toggleBookmark } from '../services/api'
import MaterialFilter from './MaterialFilter.vue'
import MaterialTabs from './MaterilaTab.vue'

const materials = ref([])
const loading = ref(true)
const currentTab = ref('all')

const currentUserId = ref(Number(localStorage.getItem('user_id')) || null)
const userRole = ref(localStorage.getItem('role') || 'member');

const trenutnastranica = ref(1)
const ukupnoStranica = ref(0)
const trenutniFilteri = ref({})
const materijalaPoStranici = 10

async function loadMaterials(filters = {}, page = 1) {
  loading.value = true
  if (currentTab.value === 'favorites') {
    const rezultat = await getMaterials({ ...filters, mine_only: false }, 1, 50)
    materials.value = rezultat.items
    trenutnastranica.value = 1
  } else if (currentTab.value === 'mine') {
    const rezultat = await getMaterials({ ...filters, mine_only: true }, page)
    materials.value = rezultat.items
    ukupnoStranica.value = rezultat.total_pages
    trenutnastranica.value = rezultat.page
  } else {
    const rezultat = await getPublicMaterials(filters, page)
    materials.value = rezultat.items
    ukupnoStranica.value = rezultat.total_pages
    trenutnastranica.value = rezultat.page
  }
  loading.value = false
}

onMounted(() => {
  loadMaterials()
})

function handleTabChange(tabId) {
  currentTab.value = tabId;
  trenutnastranica.value = 1
  loadMaterials(trenutniFilteri.value, 1)
}

function promijeniStranicu(novaStr) {
  if (currentTab.value === 'all' || currentTab.value === 'mine') {
    loadMaterials(trenutniFilteri.value, novaStr)
  } else {
    trenutnastranica.value = novaStr
  }
}

async function handleFilterChange(newFilters) {
  trenutniFilteri.value = newFilters
  trenutnastranica.value = 1
  await loadMaterials(newFilters, 1);
}

function handleDelete(deletedMaterialId) {
  materials.value = materials.value.filter(m => m.id !== deletedMaterialId)
}

// Filtrirani materijali (bez paginacije) — puna lista za trenutni tab
const filteredMaterialsBookmark = computed(() => {
  if (currentTab.value === 'mine') {
    return materials.value;
  }
  if (currentTab.value === 'favorites') {
    return materials.value.filter(m => m.is_bookmarked === true);
  }
  return materials.value;
});

// Lokalna paginacija samo za "mine" i "favorites"
const ukupnoStranicaLokalno = computed(() => {
  return Math.ceil(filteredMaterialsBookmark.value.length / materijalaPoStranici)
})

const prikazaniMaterijali = computed(() => {
  if (currentTab.value === 'all' || currentTab.value === 'mine') {
    return filteredMaterialsBookmark.value
  }
  const start = (trenutnastranica.value - 1) * materijalaPoStranici
  const end = start + materijalaPoStranici
  return filteredMaterialsBookmark.value.slice(start, end)
})

const ukupnoStranicaPrikaz = computed(() => {
  if (currentTab.value === 'all' || currentTab.value === 'mine') {
    return ukupnoStranica.value
  }
  return ukupnoStranicaLokalno.value
})

async function handleToggleBookmark(materialId) {
  try {
    const res = await toggleBookmark(materialId);
    const material = materials.value.find(m => m.id === materialId);
    if (material) {
      material.is_bookmarked = res.is_bookmarked;
    }
  } catch (error) {
    console.error("Greška kod bookmarka:", error);
  }
}

async function handleDownloaded(materialId) {
  const material = materials.value.find(m => m.id === materialId)
  if (material) {
    material.number_of_downloads += 1
  }
}
</script>