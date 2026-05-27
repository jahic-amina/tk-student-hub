<template>
  <div class="py-8 px-4 max-w-4xl mx-auto">
    <!-- Tabovi samo za admina -->
    <div v-if="isAdmin" class="flex gap-6 border-b mb-6">
      <button @click="activeTab = 'pregled'"
        :class="activeTab === 'pregled' ? 'border-b-2 border-black font-medium text-black' : 'text-gray-400'"
        class="pb-2">Pregled materijala</button>
      <button @click="activeTab = 'odobravanje'"
        :class="activeTab === 'odobravanje' ? 'border-b-2 border-black font-medium text-black' : 'text-gray-400'"
        class="pb-2">Odobri materijal</button>
    </div>
    <MaterialUploadForm @submit="refreshList" />
    <div class="flex gap-6">
      <MaterialList v-if="activeTab === 'pregled'" :key="listKey" @open="openMaterial" />
      <PendingMaterialList v-if="activeTab === 'odobravanje' && isAdmin" :key="listKey" @open="openMaterial" />
      <MaterialDetail v-if="selectedMaterialId" :material="selectedMaterialId" @close="selectedMaterialId = null" />
    </div>
  </div>
</template>

<script setup>
import MaterialUploadForm from '../../components/MaterialUploadForm.vue'
import { ref } from 'vue'
import MaterialList from '../../components/MaterialList.vue'
import MaterialDetail from '../../components/MaterialDetail.vue'
import { getMaterial } from '../../services/api'
import PendingMaterialList from '../../components/PendingMaterialList.vue'

const activeTab = ref('pregled')
const isAdmin = localStorage.getItem('role') === 'admin'
const selectedMaterialId = ref(null)

const listKey = ref(0);

function refreshList() {
  listKey.value += 1;

}

async function openMaterial(id) {
  selectedMaterialId.value = await getMaterial(id)
}
</script>