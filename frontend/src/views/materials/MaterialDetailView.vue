<template>
    <div class="max-w-2xl mx-auto py-8 px-4">
        <!-- Nazad dugme -->
        <button @click="$router.back()" class="text-sm text-gray-500 mb-6 hover:text-gray-700">← Nazad</button>

        <div v-if="loading" class="text-gray-400">Učitavanje...</div>

        <div v-else-if="material">
            <!-- Header -->
            <div class="flex justify-between items-start mb-4">
                <div>
                    <h2 class="text-xl font-bold">{{ material.title }}</h2>
                    <p class="text-sm text-gray-400">
                        Postavio: {{ material.user?.full_name }} • {{ formatDate(material.created_at) }}
                    </p>
                </div>
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

            <!-- Preuzmi -->
            <div class="mb-6">
                <DownloadButton :material-id="material.id" :full-width="true" />
            </div>

            <!-- Komentari -->
            <div>
                <h3 class="font-semibold mb-4">Komentari ({{ material.comments?.length ?? 0 }})</h3>
                <div class="flex flex-col gap-4">
                    <div v-for="comment in material.comments" :key="comment.id" class="border rounded-lg p-3">
                        <div class="flex justify-between text-sm text-gray-500 mb-1">
                            <span class="font-medium text-gray-700">{{ comment.user?.full_name }}</span>
                            <span>{{ formatDate(comment.created_at) }}</span>
                        </div>
                        <p class="text-sm text-gray-600">{{ comment.content }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import DownloadButton from '../../components/DownloadButton.vue'
import { getMaterial } from '../../services/api'

const route = useRoute()
const material = ref(null)
const loading = ref(true)
const hoverRating = ref(0)
const selectedRating = ref(0)

onMounted(async () => {
    material.value = await getMaterial(route.params.id)
    loading.value = false
})

function formatDate(dateStr) {
    if (!dateStr) return 'N/A'
    const date = new Date(dateStr)
    return date.toLocaleDateString('bs-BA')
}
</script>