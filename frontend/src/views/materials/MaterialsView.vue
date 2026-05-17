<template>
  <div class="py-8 px-4 max-w-4xl mx-auto">
    <MaterialUploadForm />
    <div class="flex gap-6">
      <MaterialList @open="openMaterial" />
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

const selectedMaterialId = ref(null)

async function openMaterial(id) {
  selectedMaterialId.value = await getMaterial(id)
}
</script>