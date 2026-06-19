<template>
    <div class="max-w-2xl mx-auto py-8 px-4 dark:text-slate-100">
        <!-- Nazad dugme -->

        <div class="flex gap-3 mb-6">
            <button @click="goBack()"
                class="inline-flex items-center gap-2 bg-primary text-white font-medium px-4 py-2 rounded-lg hover:bg-primary/90 active:scale-[0.98] transition text-sm">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                <span class="font-bold">NAZAD</span>
            </button>
            <button v-if="material?.user?.id === currentUserId" @click="isEditing ? saveChanges() : toggleEdit()"
                class="inline-flex items-center gap-2 bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 text-gray-700 dark:text-slate-200 font-medium px-4 py-2 rounded-lg hover:bg-gray-50 dark:hover:bg-slate-700 active:scale-[0.98] transition text-sm">
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

        <div v-if="loading" class="text-gray-400 dark:text-slate-500">Učitavanje...</div>

        <div v-else-if="material">
    <!-- Header -->
    <div class="flex justify-between items-start mb-4">
        <div class="w-full">
            <template v-if="isEditing">
                <input v-model="material.title"
                    class="w-full border border-gray-300 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-100 rounded-lg px-3 py-1.5 mb-1 focus:outline-none focus:border-primary" />
            </template>
            <template v-else>
                <h2 class="text-xl font-bold">{{ material.title }}</h2>
            </template>
            <p class="text-sm text-gray-400 dark:text-slate-400">Postavio: {{ material.user?.full_name }}</p>
            <p class="text-sm text-gray-400 dark:text-slate-400">Datum: {{ formatDate(material.created_at) }}</p>
        </div>
    </div>
    <hr class="mb-4 dark:border-slate-700" />
        <!-- Thumbnail + Opis + Ocjena -->
        <div class="flex gap-6 mb-6">
            <div v-if="material.thumbnail_path" class="shrink-0">
                <img 
                    :src="`http://127.0.0.1:8000/thumbnails/${material.thumbnail_path.split('/').pop()}`"
                    class="w-48 object-cover rounded-lg"
                    alt="thumbnail"
                />
            </div>
            <div class="flex-1">
             <p class="text-sm text-gray-500 dark:text-slate-400 mb-3">{{ material.subject?.name }} • {{ material.subject?.study_year }}. godina • {{ material.file_type }}</p>
             <h3 class="font-semibold mb-2 text-base">Detaljan opis</h3>
<template v-if="isEditing">
    <textarea v-model="material.description" rows="4"
        class="w-full border border-gray-300 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-primary resize-none mb-4" />
</template>
<template v-else>
    <p class="text-gray-600 dark:text-slate-400 text-sm mb-4">{{ material.description }}</p>
</template>
                <MaterialRating :material-id="material.id" :parent-has-downloaded="hasDownloaded" />
                </div>
            </div>
            <!-- Preuzmi -->
            <div class="mb-6">
                <p class="text-sm text-gray-500 dark:text-slate-400 mb-2">Broj preuzimanja: {{
                    material.number_of_downloads }}</p>
                <div class="flex gap-3">
                    <DownloadButton :material-id="material.id" :full-width="true" @downloaded="updateDownloadCount"
                        class="w-full" />
                    <button v-if="canPreview" @click="openPreview"
                        class="inline-flex items-center justify-center gap-2 bg-primary text-white font-semibold px-5 py-2.5 rounded-lg shadow-sm hover:bg-primary/90 transition disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-primary">
                        PREGLEDAJ
                    </button>
                </div>
            </div>

    <!-- Admin odobri/odbij -->
    <div v-if="isAdmin && material.status === 'pending'" class="flex w-full gap-4 mb-6">
        <button @click="handleApprove" class="flex-1 justify-center py-2.5 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2 font-medium">
            <span>✓</span> Odobri
        </button>
        <button @click="handleReject" class="flex-1 justify-center py-2.5 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2 font-medium">
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
import { getMaterial, approveMaterial, rejectMaterial, getMaterialPreviewUrl, updateMaterial, getSubjects } from '../../services/api'
import SuccessMessage from '../../components/SuccessMessage.vue'
import CommentList from '../../components/CommentList.vue'
import MaterialRating from '../../components/MaterialRating.vue'

const PREVIEWABLE = ['pdf', 'txt']

const route = useRoute()
const router = useRouter()
const material = ref(null)
const loading = ref(true)
const hasDownloaded = ref(false)
const isAdmin = localStorage.getItem('role') === 'admin'
const currentUserId = Number(localStorage.getItem('user_id'))
const successMessage = ref('')
const successTitle = ref('')
const successIcon = ref('')
const isEditing = ref(false)
const originalTitle = ref('')
const originalDescription = ref('')
const isDragging = ref(false)
const selectedFile = ref(null)
const fileInput = ref(null)
const subjects = ref([])
const editYear = ref('')
const editSubjectId = ref(null)
const editMaterialType = ref('')

onMounted(async () => {
    material.value = await getMaterial(route.params.id)
    subjects.value = await getSubjects()
    loading.value = false
    console.log(material.value?.file_extension)
})

const filteredSubjects = computed(() => {
    if (!editYear.value) return []
    return subjects.value.filter(subject => subject.study_year == editYear.value)
})


function onFileChange(event) {
    selectedFile.value = event.target.files[0] || null
}

function onFileDrop(event) {
    isDragging.value = false
    const files = event.dataTransfer.files
    if (files.length > 0) selectedFile.value = files[0]
}

function toggleEdit() {
    if (!isEditing.value) {
        // Spremi originalne vrijednosti prije editovanja
        originalTitle.value = material.value.title
        originalDescription.value = material.value.description
        editYear.value = material.value.subject?.study_year || ''
        editSubjectId.value = material.value.subject?.id || ''
        editMaterialType.value = material.value.file_type || ''
    }
    isEditing.value = !isEditing.value
}

function cancelEdit() {
    material.value.title = originalTitle.value
    material.value.description = originalDescription.value
    editYear.value = ''
    editSubjectId.value = ''
    editMaterialType.value = ''
    isEditing.value = false
    selectedFile.value = null
}

async function saveChanges() {
    try {
        await updateMaterial(material.value.id, material.value.title, material.value.description, selectedFile.value, editSubjectId.value, editMaterialType.value)
        material.value = await getMaterial(route.params.id) // Ponovo učitaj materijal nakon spremanja
        successMessage.value = 'Promjene su sačuvane!'
        successTitle.value = 'Uspjeh!'
        successIcon.value = '✅'
        isEditing.value = false
        selectedFile.value = null
    } catch (error) {
        console.error('Greška prilikom spremanja promjena:', error)
    }
}

const canPreview = computed(() => {
    if (!material.value?.file_type) return false
    return ['pdf', 'txt'].includes(material.value.file_extension)
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
// Ažurira broj preuzimanja lokalno nakon downloada 
function updateDownloadCount() {
    material.value.number_of_downloads += 1
    hasDownloaded.value = true
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