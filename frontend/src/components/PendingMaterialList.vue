<template>
    <div class="flex-1 py-8 px-6">
        <h1 class="text-2xl font-bold uppercase mb-1">Odobri materijal</h1>
        <p class="text-sm text-gray-500 mb-6">Materijali na čekanju</p>
        <div v-if="loading" class="text-center py-10 text-gray-400">Učitavanje...</div>

        <div v-else-if="materials.length === 0" class="text-center py-10 text-gray-400">
            Nema materijala na čekanju.
        </div>

        <div v-else class="flex flex-col gap-4">
            <MaterialCard 
            v-for="material in materials" 
            :key="material.id" 
            :material="material" 
            :pending="true"
            :user-role="userRole"
            :has-downloaded="downloadedMap[material.id] || false"
            @approve="handleApprove" 
            @reject="handleReject" 
            @click="$emit('open', $event)" 
        />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import MaterialCard from './MaterialCard.vue'
import { getPendingMaterials, approveMaterial, rejectMaterial, checkHasDownloaded } from '../services/api'

defineEmits(['open'])

const materials = ref([])
const loading = ref(true)

const userRole = ref(localStorage.getItem('role') || 'member')
const downloadedMap = ref({})

onMounted(async () => {
    materials.value = await getPendingMaterials()
    for (const m of materials.value) {
        try {
            const res = await checkHasDownloaded(m.id)
            downloadedMap.value[m.id] = res.has_downloaded
        } catch {
            downloadedMap.value[m.id] = false
        }
    }
    loading.value = false
})

async function handleReject(id) {
    try {
        await rejectMaterial(id)
        materials.value = materials.value.filter(m => m.id !== id)
    } catch (error) {
        console.error('Greška prilikom odbijanja materijala:', error)
    }
}
async function handleApprove(id) {
    try {
        await approveMaterial(id)
        materials.value = materials.value.filter(m => m.id !== id)
    } catch (error) {
        console.error('Greška prilikom odobravanja materijala:', error)
    }
}

</script>