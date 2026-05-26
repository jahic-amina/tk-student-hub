<template>
  <div class="py-8 px-4 max-w-4xl mx-auto">
    <MaterialUploadForm @submit="refreshList" />
    <div class="flex gap-6">
      <MaterialList :key="listKey" @open="openMaterial" />
    </div>
  </div>
</template>

<script setup>
import MaterialUploadForm from '../../components/MaterialUploadForm.vue'
import { ref } from 'vue'
import MaterialList from '../../components/MaterialList.vue'
import { getMaterial } from '../../services/api'
import DeleteMaterialButton from '../../components/DeleteMaterialButton.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const selectedMaterialId = ref(null)

const listKey = ref(0);

function refreshList() {
  listKey.value += 1;

}

async function openMaterial(id) {
  router.push(`/materials/${id}`)
}
</script>