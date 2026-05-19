<template>
    <div class="flex-1 py-8 px-6">
        <h1 class="text-2xl font-bold uppercase mb-1">Pregled materijala</h1>
        <p class="text-sm text-gray-500 mb-6">Dostupni materijal</p>

        <div v-if="loading" class="text-center py-10 text-gray-400">Učitavanje...</div>

        <div v-else class="flex flex-col gap-4">
            <MaterialCard 
                v-for="material in materials" 
                :key="material.id" 
                :material="material"
                @click="$emit('open', $event)" 
                @deleted="handleDelete"
            />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import MaterialCard from './MaterialCard.vue'
import { getMaterials } from '../services/api'

defineEmits(['open', 'deleted'])

const materials = ref([])
const loading = ref(true)

onMounted(async () => {
    materials.value = await getMaterials()
    loading.value = false
})

function handleDelete(deletedMaterialId) {
    materials.value = materials.value.filter(m => m.id !== deletedMaterialId)
}
</script>