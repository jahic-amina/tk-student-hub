<template>
    <div>
        <h3 class="font-semibold mb-4">Komentari</h3>

        <!-- Forma za dodavanje -->
        <CommentForm :material-id="materialId" @komentar-dodan="dodajKomentar" class="mb-6" />

        <hr class="mb-4" />

        <!-- Učitavanje -->
        <div v-if="loading" class="text-gray-400 text-sm">Učitavanje komentara...</div>

        <!-- Greška -->
        <div v-else-if="greska" class="text-red-400 text-sm">Greška pri učitavanju komentara.</div>

        <!-- Nema komentara -->
        <div v-else-if="komentari.length === 0" class="text-gray-400 text-sm italic">
            Još uvijek nema komentara. Budite prvi koji će ostaviti komentar.
        </div>

        <!-- Lista komentara -->
        <div v-else class="flex flex-col gap-3">
          <CommentCard
            v-for="komentar in komentari"
            :key="komentar.id"
            :comment="komentar"
            @obrisan="ukloniKomentar"
            />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import CommentCard from './CommentCard.vue'
import CommentForm from './CommentForm.vue'
import { getComments } from '../services/api.js'

const props = defineProps({
    materialId: {
        type: Number,
        required: true
    }
})

const komentari = ref([])
const loading = ref(false)
const greska = ref(false)

onMounted(async () => {
    loading.value = true
    greska.value = false
    try {
        komentari.value = await getComments(props.materialId)
    } catch (e) {
        greska.value = true
    } finally {
        loading.value = false
    }
})

function dodajKomentar(noviKomentar) {
    komentari.value.unshift(noviKomentar)
}

function ukloniKomentar(id) {
    komentari.value = komentari.value.filter(k => k.id !== id)
}
</script>