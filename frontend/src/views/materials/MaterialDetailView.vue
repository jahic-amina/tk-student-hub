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
            <MaterialRating :material-id="material.id" />

            <!-- Preuzmi -->
            <div class="mb-6">
                <p class="text-sm text-gray-500 mb-2">Broj preuzimanja: {{ material.number_of_downloads }}</p>
                <div class="flex gap-3">
                    <DownloadButton :material-id="material.id" :full-width="true" @downloaded="updateDownloadCount"
                        class="flex-1" />
                    <button v-if="canPreview" @click="openPreview"
                        class="flex-1 flex items-center justify-center gap-2 bg-primary text-white font-medium px-4 py-2 rounded-lg hover:bg-primary/90 transition text-sm">
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                        PREGLEDAJ
                    </button>
                </div>
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
            <CommentList :material-id="material.id" />

        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DownloadButton from '../../components/DownloadButton.vue'
import { getMaterial, approveMaterial, rejectMaterial, getMaterialPreviewUrl } from '../../services/api'
import SuccessMessage from '../../components/SuccessMessage.vue'
import CommentList from '../../components/CommentList.vue'
import MaterialRating from '../../components/MaterialRating.vue'

const PREVIEWABLE = ['pdf', 'txt']

const route = useRoute()
const router = useRouter()
const material = ref(null)
const loading = ref(true)
const isAdmin = localStorage.getItem('role') === 'admin'
const successMessage = ref('')
const successTitle = ref('')
const successIcon = ref('')

const canPreview = computed(() => {
    if (!material.value?.file_type) return false
    const type = material.value.file_type.toLowerCase()
    return type.includes('pdf') || type.includes('text') || type.includes('text/plain');
})


onMounted(async () => {
    material.value = await getMaterial(route.params.id)
    loading.value = false
})


function openPreview() {
    const url = getMaterialPreviewUrl(material.value.id)
    window.open(url, '_blank')
}

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
// Ažurira broj preuzimanja lokalno nakon downloada - Marinela
function updateDownloadCount() {
    material.value.number_of_downloads += 1
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