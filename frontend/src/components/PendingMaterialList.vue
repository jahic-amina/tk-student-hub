<template>
    <div class="flex-1">
        <div v-if="loading" class="text-center py-10 text-gray-400">Učitavanje...</div>

        <div v-else-if="materials.length === 0" class="text-center py-10 text-gray-400">
            Nema materijala na čekanju.
        </div>

        <div v-else class="flex flex-col gap-4">
            <MaterialCard v-for="material in materials" :key="material.id" :material="material" :pending="true"
                @approve="handleApprove" @reject="handleReject" @click="$emit('open', $event)" />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import MaterialCard from './MaterialCard.vue'
import { getPendingMaterials, approveMaterial, rejectMaterial } from '../services/api'

defineEmits(['open'])

const materials = ref([])
const loading = ref(true)

onMounted(async () => {
    materials.value = await getPendingMaterials()
    loading.value = false
})

async function handleApprove(id) {
    try {
        await approveMaterial(id)
        materials.value = materials.value.filter(m => m.id !== id)
    } catch (error) {
        console.error('Greška prilikom odobravanja materijala:', error)
    }
}

async function handleReject(id) {
    try {
        await rejectMaterial(id)
        materials.value = materials.value.filter(m => m.id !== id)
    } catch (error) {
        console.error('Greška prilikom odbijanja materijala:', error)
    }
}

</script>