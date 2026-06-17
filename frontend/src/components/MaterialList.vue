<template>
  <div class="w-full flex flex-col md:flex-row gap-8 items-start justify-start py-6 pl-0 pr-4 md:-ml-24 lg:-ml-80 bg-transparent" style="max-width: none !important;">

    <div class="w-full md:w-[280px] shrink-0 flex flex-col items-stretch justify-start gap-4 text-left">
      <MaterialFilter @change="handleFilterChange" />
    </div>

    <div class="flex-grow min-w-0 w-full pl-4">
      <MaterialTabs v-if="userRole !== 'admin'" :activeTab="currentTab" @tab-change="handleTabChange" />

      <h1 class="text-2xl font-bold uppercase mb-1">Pregled materijala</h1>
      <p class="text-sm text-gray-500 mb-6">Dostupni materijal</p>

      <div v-if="loading">Učitavanje...</div>

      <div v-else>
        <div v-if="filteredMaterialsBookmark.length > 0" class="flex flex-col gap-4">
          <div class="flex flex-col gap-4">
            <MaterialCard 
              v-for="material in filteredMaterialsBookmark" 
              :key="material.id" 
              :material="material"
              :user-role="userRole"
              @click="$router.push(`/materials/${$event}`)"
              @deleted="handleDelete"
              @toggle-bookmark="handleToggleBookmark"
            />
          </div>

          <div v-if="ukupnoStranica >= 1" class="flex justify-center items-center gap-2 mt-6">
            <button
              @click="promijeniStranicu(trenutnastranica - 1)"
              :disabled="trenutnastranica === 1"
              class="px-3 py-1 rounded-lg border text-sm text-gray-600 hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              ←
            </button>
            <button
              v-for="br in ukupnoStranica"
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
              :disabled="trenutnastranica === ukupnoStranica"
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
import { ref, onMounted, computed } from 'vue'
import MaterialCard from './MaterialCard.vue'
import { getMaterials } from '../services/api'
import MaterialFilter from './MaterialFilter.vue'
import MaterialTabs from './MaterilaTab.vue'
import { toggleBookmark } from '../services/api'

const materials = ref([])
const loading = ref(true)
const currentTab = ref('all')

const userRaw = localStorage.getItem('user');
const currentUser = userRaw ? JSON.parse(userRaw) : null;
const currentUserId = ref(currentUser ? currentUser.id : null);
const userRole = ref(localStorage.getItem('role') || 'member');

const trenutnastranica = ref(1)
const ukupnoStranica = ref(0)
const trenutniFilteri = ref({})

async function loadMaterials(filters = {}, page = 1) {
    loading.value = true
    const rezultat = await getMaterials(filters, page)
    materials.value = rezultat.items
    ukupnoStranica.value = rezultat.total_pages
    trenutnastranica.value = rezultat.page
    loading.value = false
}

onMounted(() => {
  loadMaterials();
  console.log("Ulogovan korisnik ID:", currentUserId.value);
})

function handleTabChange(tabId) {
  currentTab.value = tabId;
  trenutnastranica.value = 1
}

function promijeniStranicu(novaStr) {
    loadMaterials(trenutniFilteri.value, novaStr)
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
  trenutniFilteri.value = newFilters
  await loadMaterials(newFilters,1);
  
}

function handleDelete(deletedMaterialId) {
  materials.value = materials.value.filter(m => m.id !== deletedMaterialId)
}



const filteredMaterialsBookmark = computed(() => {
  // 1. Ako je tab "Moji materijali", filtriraj po ID-u korisnika
  if (currentTab.value === 'mine') {
    return materials.value.filter(m => Number(m.user?.id) === Number(currentUserId.value));
  }
  
  // 2. Ako je tab "Najdraži materijali", prikaži samo bookmarkovane
  if (currentTab.value === 'favorites') {
    return materials.value.filter(m => m.is_bookmarked === true);
  }

  // 3. DEFAULT (Svi materijali): Ako nije nijedan od gornjih tabova, VRATI SVE
  // Ovo je dio koji je vjerovatno falio ili se nije izvršavao
  return materials.value;
});

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
</script>