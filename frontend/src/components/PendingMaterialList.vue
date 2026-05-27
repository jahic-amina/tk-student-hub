<template>
    <div class="flex-1">
        <div v-if="loading" class="text-center py-10 text-gray-400">Učitavanje...</div>

        <div v-else-if="materials.length === 0" class="text-center py-10 text-gray-400">
            Nema materijala na čekanju.
        </div>

        <div v-else class="flex flex-col gap-4">
            <MaterialCard v-for="material in materials" :key="material.id" :material="material" :pending="true"
                @approve="approveMaterial" @reject="rejectMaterial" />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import MaterialCard from './MaterialCard.vue'
import { getPendingMaterials } from '../services/api'

const materials = ref([])
const loading = ref(true)

onMounted(async () => {
    materials.value = await getPendingMaterials()
    loading.value = false
})


</script>