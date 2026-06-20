<template>
  <div>
    <div v-if="isAdmin" class="flex gap-6 border-b mb-6 px-4 dark:border-slate-700">
      <button @click="activeTab = 'pregled'"
        :class="activeTab === 'pregled' ? 'border-b-2 border-black dark:border-white font-medium text-black dark:text-white' : 'text-gray-400'"
        class="pb-2">Pregled materijala</button>
      <button @click="activeTab = 'odobravanje'"
        :class="activeTab === 'odobravanje' ? 'border-b-2 border-black dark:border-white font-medium text-black dark:text-white' : 'text-gray-400'"
        class="pb-2">Odobri materijal</button>
    </div>
    <MaterialUploadForm @submit="refreshList" />
    <MaterialList v-if="activeTab === 'pregled'" :key="listKey" @open="openMaterial" />
    <PendingMaterialList v-if="activeTab === 'odobravanje' && isAdmin" :key="listKey" @open="openMaterial" />
  </div>
</template>

<script setup>
import MaterialUploadForm from '../../components/MaterialUploadForm.vue'
import { ref, computed, watch } from 'vue'
import MaterialList from '../../components/MaterialList.vue'
import PendingMaterialList from '../../components/PendingMaterialList.vue'
import { useRouter } from 'vue-router'
import MaterialDetail from '../../components/MaterialDetail.vue'
import { getMaterial } from '../../services/api'
const selectedMaterialId = ref(null)

const router = useRouter()

const activeTab = ref(router.currentRoute.value.path.includes('pending') ? 'odobravanje' : 'pregled')
const isAdmin = localStorage.getItem('role') === 'admin'

const listKey = ref(0);

watch(activeTab, (newTab) => {
  if (newTab === 'odobravanje') {
    router.push('/materials/pending');
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
//----------------------------------------------------
// Osvježavanje liste i ocjene nakon ocjenjivanja - Marinela
async function refreshMaterial(id) {
  selectedMaterialId.value = await getMaterial(id)
  listKey.value += 1  // osvježava kartice na listi
}
//----------------------------------------------------
</script>