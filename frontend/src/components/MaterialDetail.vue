<template>
    <!-- Overlay -->
    <div class="fixed inset-0 bg-black/50 z-40" @click="$emit('close')" />

    <!-- Modal -->
    <div
        class="fixed inset-0 sm:inset-auto sm:top-1/2 sm:left-1/2 sm:-translate-x-1/2 sm:-translate-y-1/2 bg-white sm:rounded-xl sm:w-[600px] sm:max-h-[80vh] overflow-y-auto z-50 p-6">

        <!-- Header -->
        <div class="flex justify-between items-start mb-4">
            <div>
                <h2 class="text-xl font-bold">{{ material.title }}</h2>
                <p class="text-sm text-gray-400">
                    Postavio: {{ material.user.full_name }} • {{ formatDate(material.created_at) }}
                </p>
            </div>
            <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 text-xl">✕</button>
        </div>

        <hr class="mb-4" />

        <!-- Opis -->
        <div class="mb-6">
            <h3 class="font-semibold mb-2">Detaljan opis</h3>
            <p class="text-gray-600 text-sm">{{ material.description }}</p>
        </div>

        <!-- Ocjena -->
        <div class="mb-6">
            <h3 class="font-semibold mb-2">Ocjena materijala</h3>
            <div class="flex items-center gap-2">
                <span v-for="star in 5" :key="star" class="text-yellow-400 text-2xl">
                    {{ star <= Math.round(material.average_rating) ? '★' : '☆' }} </span>
                        <span class="text-gray-600">{{ material.average_rating }} / 5.0 ({{ material.rating_count }}
                            ocjena)</span>
            </div>
           
            <p class="text-sm text-gray-500 mt-2">Broj preuzimanja: {{ material.number_of_downloads }}</p>

            <!-- Ocijeni -->
            <div class="mt-4">
                <p class="text-sm text-gray-500 mb-1">Ocijenite ovaj materijal:</p>
                <div class="flex gap-1">
                    <span v-for="star in 5" :key="star" class="text-2xl cursor-pointer transition"
                        :class="[
                star <= hoverRating || star <= selectedRating ? 'text-yellow-400' : 'text-gray-300',
                isLoggedIn ? 'cursor-pointer' : 'cursor-not-allowed opacity-50'
            ]"
            @mouseover="isLoggedIn && (hoverRating = star)" 
            @mouseleave="hoverRating = 0"
            @click="submitRating(star)">★</span>
    </div>
    <p v-if="ratingMessage" class="text-sm text-green-600 mt-2">{{ ratingMessage }}</p>
    <p v-if="ratingError" class="text-sm text-red-600 mt-2">{{ ratingError }}</p>
    <p v-if="!isLoggedIn" class="text-sm text-gray-400 mt-2">Prijavite se da biste ocijenili materijal.</p>
    </div>
</div>

        <!-- Preuzmi dugme -->
        <div class="mb-6">
            <DownloadButton :material-id="material.id" :full-width="true" />
        </div>

        <!-- Komentari -->
        <div>
            <h3 class="font-semibold mb-4">Komentari ({{ material.comments?.length ?? 0 }})</h3>
            <div v-if="loading" class="text-gray-400 text-sm">Učitavanje...</div>
            <div v-else class="flex flex-col gap-4">
                <div v-for="comment in material.comments" :key="comment.id" class="border rounded-lg p-3">
                    <div class="flex justify-between text-sm text-gray-500 mb-1">
                        <span class="font-medium text-gray-700">{{ comment.user.full_name }}</span>
                        <span>{{ formatDate(comment.created_at) }}</span>
                    </div>
                    <p class="text-sm text-gray-600">{{ comment.content }}</p>
                </div>
            </div>
        </div>

    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import DownloadButton from './DownloadButton.vue'

const BASE_URL = 'http://127.0.0.1:8000'

const props = defineProps({
    material: {
        type: Object,
        required: true
    }
})

defineEmits(['close'])

const hoverRating = ref(0)
const selectedRating = ref(0)
const loading = ref(false)
//-----------------------------------------------------------------------------------
//Ocjenjivanje materijala - Marinela

const ratingMessage = ref('')
const ratingError = ref('')

const isLoggedIn = computed(() => !!localStorage.getItem('token'))

async function submitRating(star) {
    if (!isLoggedIn.value) return
    selectedRating.value = star
    ratingMessage.value = ''
    ratingError.value = ''

 try {
        const token = localStorage.getItem('token')
        const response = await fetch(`${BASE_URL}/materials/${props.material.id}/rate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify({ rating: star, material_id: props.material.id })
        })

        if (response.status === 409) {
            ratingError.value = 'Već ste ocijenili ovaj materijal.'
            return
        }
        if (!response.ok) {
            ratingError.value = 'Greška prilikom ocjenjivanja.'
            return
        }

        ratingMessage.value = 'Hvala na ocjeni! ⭐'
    } catch (err) {
        ratingError.value = 'Greška prilikom ocjenjivanja.'
    }
}
//----------------------------------------------------------------------------------
function formatDate(dateStr) {
    const date = new Date(dateStr)
    return date.toLocaleDateString('bs-BA')
}
</script>