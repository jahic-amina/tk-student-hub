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
            <p class="text-sm text-gray-500 mt-2 flex gap-2 items-center"><svg xmlns="http://www.w3.org/2000/svg"
                    width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                    stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-download w-4 h-4"
                    data-fg-d3bl133="0.8:79.665:/src/app/App.tsx:544:25:21266:32:e:Download::::::yh6"
                    data-fgid-d3bl133=":r2p:">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="7 10 12 15 17 10"></polyline>
                    <line x1="12" x2="12" y1="15" y2="3"></line>
                </svg> {{ material.number_of_downloads }} preuzimanja</p>

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
        <button
            class="w-full bg-black text-white py-3 rounded-xl font-medium hover:bg-gray-800 transition mb-6 flex items-center justify-center gap-2  ">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                class="lucide lucide-download w-4 h-4"
                data-fg-d3bl133="0.8:79.665:/src/app/App.tsx:544:25:21266:32:e:Download::::::yh6"
                data-fgid-d3bl133=":r2p:">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" x2="12" y1="15" y2="3"></line>
            </svg> PREUZMI MATERIJAL
        </button>

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
import { ref } from 'vue'

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