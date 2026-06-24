<template>
  <div>
    <div v-if="isAdmin" class="flex gap-6 border-b mb-6 px-4 dark:border-slate-700">
      <button @click="activeTab = 'pregled'"
        :class="activeTab === 'pregled' ? 'border-b-2 border-black dark:border-white font-medium text-black dark:text-white' : 'text-gray-400'"
        class="pb-2">Pregled materijala</button>
      
      <button @click="activeTab = 'odobravanje'"
        :class="activeTab === 'odobravanje' ? 'border-b-2 border-black dark:border-white font-medium text-black dark:text-white' : 'text-gray-400'"
        class="pb-2">Odobri materijal</button>

      <button @click="activeTab = 'brisanje'"
        :class="activeTab === 'brisanje' ? 'border-b-2 border-black dark:border-white font-medium text-black dark:text-white' : 'text-gray-400'"
        class="pb-2">Zahtjevi za brisanje</button>
    </div>

    <MaterialUploadForm @submit="refreshList" />
    
    <MaterialList v-if="activeTab === 'pregled'" :key="listKey" @open="openMaterial" />
    <PendingMaterialList v-if="activeTab === 'odobravanje' && isAdmin" :key="listKey" @open="openMaterial" />
    <PendingDeletionList v-if="activeTab === 'brisanje' && isAdmin" :key="listKey" @open="openMaterial" />
  </div>
</template>

<script setup>
import MaterialUploadForm from '../../components/MaterialUploadForm.vue'
import { ref, computed, watch } from 'vue'
import MaterialList from '../../components/MaterialList.vue'
import PendingMaterialList from '../../components/PendingMaterialList.vue'
import PendingDeletionList from './PendingDeletionList.vue'
import { useRouter } from 'vue-router'
import MaterialDetail from '../../components/MaterialDetail.vue'
import { getMaterial } from '../../services/api'

const selectedMaterialId = ref(null)
const router = useRouter()

const currentPath = router.currentRoute.value.path
const activeTab = ref('pregled')
if (currentPath.includes('pending-deletion')) {
  activeTab.value = 'brisanje'
} else if (currentPath.includes('pending')) {
  activeTab.value = 'odobravanje'
}

const isAdmin = localStorage.getItem('role') === 'admin'
const listKey = ref(0);

watch(activeTab, (newTab) => {
  if (newTab === 'odobravanje') {
    router.push('/materials/pending');
  } else if (newTab === 'brisanje') {
    router.push('/materials/pending-deletion');
  } else {
    router.push('/materials');
  }
})

function refreshList() {
  listKey.value += 1;
}

async function openMaterial(id) {
  router.push({ path: `/materials/${id}` })
}

async function refreshMaterial(id) {
  selectedMaterialId.value = await getMaterial(id)
  listKey.value += 1 
}
</script>