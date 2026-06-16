<template>
    <div class="max-w-2xl mx-auto py-8 px-4">
        <!-- Nazad dugme -->

        <div class="flex gap-3 mb-6">
            <button @click="goBack()"
                class="inline-flex items-center gap-2 bg-primary text-white font-medium px-4 py-2 rounded-lg hover:bg-primary/90 active:scale-[0.98] transition text-sm">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                <span>NAZAD</span>
            </button>
            <button v-if="material?.user?.id === currentUserId" @click="toggleEdit()"
                class="inline-flex items-center gap-2 bg-white border border-gray-300 text-gray-700 font-medium px-4 py-2 rounded-lg hover:bg-gray-50 active:scale-[0.98] transition text-sm">
                <svg v-if="!isEditing" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
                <span>{{ isEditing ? 'SPREMI' : 'UREDI' }}</span>
            </button>

            <button v-if="isEditing" @click="cancelEdit()"
                class="inline-flex items-center gap-2 bg-red-500 text-white font-medium px-4 py-2 rounded-lg hover:bg-red-600 active:scale-[0.98] transition text-sm">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
                <span>ODUSTANI</span>
            </button>
        </div>

        <SuccessMessage :message="successMessage" :title="successTitle" :icon="successIcon"
            @close="() => { successMessage = ''; goBack() }" />

        <div v-if="loading" class="text-gray-400">Učitavanje...</div>

        <div v-else-if="material">
            <!-- Header -->
            <div class="flex justify-between items-start mb-4">
                <div class="w-full">
                    <template v-if="isEditing">
                        <input v-model="material.title"
                            class="w-full border border-gray-300 rounded-lg px-3 py-1.5 mb-1 focus:outline-none focus:border-primary" />
                    </template>
                    <template v-else>
                        <h2 class="text-xl font-bold">{{ material.title }}</h2>
                    </template>
                    <p class="text-sm text-gray-400">
                        Postavio: {{ material.user?.full_name }} • {{ formatDate(material.created_at) }}
                    </p>
                </div>
            </div>

            <hr class="mb-4" />

            <!-- Opis -->
            <div class="mb-6">
                <h3 class="font-semibold mb-2">Detaljan opis</h3>
                <template v-if="isEditing">
                    <textarea v-model="material.description" rows="4"
                        class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-600 focus:outline-none focus:border-primary resize-none" />
                </template>
                <template v-else>
                    <p class="text-gray-600 text-sm">{{ material.description }}</p>
                </template>
            </div>

            <!-- Ocjena -->
            <MaterialRating :material-id="material.id" />

            <!-- Preuzmi -->
            <div class="mb-6">
                <p class="text-sm text-gray-500 mb-2">Broj preuzimanja: {{ material.number_of_downloads }}</p>
                <DownloadButton :material-id="material.id" :full-width="true" @downloaded="updateDownloadCount" />
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
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DownloadButton from '../../components/DownloadButton.vue'
import { getMaterial, approveMaterial, rejectMaterial } from '../../services/api'
import SuccessMessage from '../../components/SuccessMessage.vue'
import CommentList from '../../components/CommentList.vue'
import MaterialRating from '../../components/MaterialRating.vue'

const route = useRoute()
const router = useRouter()
const material = ref(null)
const loading = ref(true)
const isAdmin = localStorage.getItem('role') === 'admin'
const currentUserId = Number(localStorage.getItem('user_id'))
const successMessage = ref('')
const successTitle = ref('')
const successIcon = ref('')
const isEditing = ref(false)
const originalTitle = ref('')
const originalDescription = ref('')

function toggleEdit() {
    if (!isEditing.value) {
        // Spremi originalne vrijednosti prije editovanja
        originalTitle.value = material.value.title
        originalDescription.value = material.value.description
    }
    isEditing.value = !isEditing.value
}

function cancelEdit() {
    material.value.title = originalTitle.value
    material.value.description = originalDescription.value
    isEditing.value = false
}


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