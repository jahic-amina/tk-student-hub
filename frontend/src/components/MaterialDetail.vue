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
                        :class="star <= hoverRating || star <= selectedRating ? 'text-yellow-400' : 'text-gray-300'"
                        @mouseover="hoverRating = star" @mouseleave="hoverRating = 0"
                        @click="selectedRating = star">★</span>
                </div>
            </div>
        </div>

        <!-- Preuzmi dugme -->
        <div class="mb-6">
            <DownloadButton :material-id="material.id" :full-width="true" />
        </div>

        <!-- Komentari -->
        <CommentList :material-id="material.id" />

    </div>
</template>

<script setup>
import { ref } from 'vue'
import DownloadButton from './DownloadButton.vue'
import CommentList from './CommentList.vue'

defineProps({
    material: {
        type: Object,
        required: true
    }
})

defineEmits(['close'])

const hoverRating = ref(0)
const selectedRating = ref(0)
const loading = ref(false)

function formatDate(dateStr) {
    const date = new Date(dateStr)
    return date.toLocaleDateString('bs-BA')
}
</script>