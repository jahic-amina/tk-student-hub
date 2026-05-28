<template>
    <div class="max-w-2xl mx-auto py-8 px-4">
        <!-- Nazad dugme -->
        <button @click="goBack()"
            class="inline-flex items-center gap-2 bg-primary text-white font-semibold px-5 py-2.5 rounded-lg shadow-sm hover:bg-primary/90 active:scale-[0.98] transition mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24"
                stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            <span>NAZAD</span>
        </button>

        <SuccessMessage :message="successMessage" :title="successTitle" :icon="successIcon"
            @close="() => { successMessage = ''; goBack() }" />

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
            <div v-if="isAdmin && material.status === 'pending'" class="flex w-full gap-4 mb-6">
                <button @click="handleApprove"
                    class="flex-1 justify-center py-2.5 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2 font-medium">
                    <span>✓</span> Odobri
                </button>

                <button @click="handleReject"
                    class="flex-1 justify-center py-2.5 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2 font-medium">
                    <span>✕</span> Odbij
                </button>
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
import { useRoute, useRouter } from 'vue-router'
import DownloadButton from '../../components/DownloadButton.vue'
import { getMaterial, approveMaterial, rejectMaterial } from '../../services/api'
import SuccessMessage from '../../components/SuccessMessage.vue'

const route = useRoute()
const router = useRouter()
const material = ref(null)
const loading = ref(true)
const hoverRating = ref(0)
const selectedRating = ref(0)
const isAdmin = localStorage.getItem('role') === 'admin'
const successMessage = ref('')
const successTitle = ref('')
const successIcon = ref('')

onMounted(async () => {
    material.value = await getMaterial(route.params.id)
    loading.value = false
})

async function handleApprove() {
    try {
        await approveMaterial(material.value.id)
        successMessage.value = 'Materijal odobren!'
        successTitle.value = 'Uspjeh!'
        successIcon.value = '✅'
    } catch (error) {
        console.error('Greška prilikom odobravanja materijala:', error)
    }
}

async function handleReject() {
    try {
        await rejectMaterial(material.value.id)
        successMessage.value = 'Materijal odbijen!'
        successTitle.value = 'Odbijeno'
        successIcon.value = '❌'
    } catch (error) {
        console.error('Greška prilikom odbijanja materijala:', error)
    }
}

function goBack() {
    if (window.history.length > 1) {
        router.back();
    } else {
        router.push('/materials');
    }
}

function formatDate(dateStr) {
    if (!dateStr) return 'N/A'
    const date = new Date(dateStr)
    return date.toLocaleDateString('bs-BA')
}
</script>