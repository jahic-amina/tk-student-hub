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
                <span>NAZAD</span>
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
                    <p class="text-sm text-gray-400 dark:text-slate-500">
                        Postavio: {{ material.user?.full_name }} • {{ formatDate(material.created_at) }}
                    </p>
                </div>
            </div>
            <hr class="mb-4 dark:border-slate-700" />

            <!-- Opis -->
            <div class="mb-6">
                <h3 class="font-semibold mb-2">Detaljan opis</h3>
                <template v-if="isEditing">
                    <textarea v-model="material.description" rows="4"
                        class="w-full border border-gray-300 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-300 rounded-lg px-3 py-2 text-sm text-gray-600 focus:outline-none focus:border-primary resize-none" />
                    <div class="mb-6">
                        <h3 class="font-semibold mb-2">Zamijeni fajl (opcionalno)</h3>
                        <div @click="fileInput.click()" @dragover.prevent="isDragging = true"
                            @dragleave.prevent="isDragging = false" @drop.prevent="onFileDrop" :class="[
                                'border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors',
                                isDragging ? 'border-primary bg-orange-50 dark:bg-orange-950' : 'border-gray-300 dark:border-slate-600 bg-gray-50 dark:bg-slate-800'
                            ]">
                            <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 mx-auto mb-2 text-gray-400"
                                fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2M7 10l5-5 5 5M12 5v10" />
                            </svg>
                            <p class="text-gray-700 dark:text-slate-300 font-medium">Prevucite fajl ovdje ili kliknite
                                da odaberete</p>
                            <p class="text-sm text-gray-500 dark:text-slate-400 mt-1">Podržani formati: PDF, DOC, DOCX,
                                TXT, PPT, PPTX, ZIP</p>
                            <p v-if="selectedFile" class="text-sm text-primary font-medium mt-3">
                                Odabran: {{ selectedFile.name }}
                            </p>
                        </div>
                        <input ref="fileInput" type="file" @change="onFileChange"
                            accept=".pdf,.doc,.docx,.ppt,.pptx,.zip,.txt" class="hidden" />
                    </div>
                    <!-- Tip materijala -->
                    <div class="mb-4">
                        <h3 class="font-semibold mb-2">Tip materijala</h3>
                        <select v-model="editMaterialType"
                            class="w-full border border-gray-300 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-200 rounded-lg px-3 py-2 focus:outline-none focus:border-primary">
                            <option value="">Odaberite tip</option>
                            <option value="skripta">Skripta</option>
                            <option value="auditorne_vježbe">Auditorne vježbe</option>
                            <option value="laboratorijske_vježbe">Laboratorijske vježbe</option>
                            <option value="ispiti">Ispiti</option>
                            <option value="projekat">Projekat</option>
                        </select>
                    </div>

                    <!-- Godina studija -->
                    <div class="mb-4">
                        <h3 class="font-semibold mb-2">Godina studija</h3>
                        <select v-model="editYear"
                            class="w-full border border-gray-300 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-200 rounded-lg px-3 py-2 focus:outline-none focus:border-primary">
                            <option value="">Odaberite godinu</option>
                            <option value="1">1. godina</option>
                            <option value="2">2. godina</option>
                            <option value="3">3. godina</option>
                            <option value="4">4. godina</option>
                        </select>
                    </div>

                    <!-- Predmet -->
                    <div class="mb-6">
                        <h3 class="font-semibold mb-2">Predmet</h3>
                        <select v-model="editSubjectId"
                            class="w-full border border-gray-300 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-200 rounded-lg px-3 py-2 focus:outline-none focus:border-primary">
                            <option value="">Odaberite predmet</option>
                            <option v-for="subject in filteredSubjects" :key="subject.id" :value="subject.id">
                                {{ subject.name }}
                            </option>
                        </select>
                    </div>
                </template>
                <template v-else>
                    <p class="text-gray-600 dark:text-slate-400 text-sm ">{{ material.description }}</p>
                </template>
            </div>

            <!-- Ocjena -->
           <MaterialRating :material-id="material.id" :key="ratingKey" />
            <!-- Preuzmi -->
            <div class="mb-6">
                <p class="text-sm text-gray-500 mb-2 dark:text-slate-400 mb-2">Broj preuzimanja: {{ material.number_of_downloads }}</p>
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
import { getMaterial, approveMaterial, rejectMaterial, getMaterialPreviewUrl, updateMaterijal, getSubjects } from '../../services/api'
import SuccessMessage from '../../components/SuccessMessage.vue'
import CommentList from '../../components/CommentList.vue'
import MaterialRating from '../../components/MaterialRating.vue'

const PREVIEWABLE = ['pdf', 'txt']

const route = useRoute()
const router = useRouter()
const material = ref(null)
const loading = ref(true)
const ratingKey = ref(0)  
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
// Ažurira broj preuzimanja lokalno nakon downloada 
function updateDownloadCount() {
    material.value.number_of_downloads += 1
    setTimeout(() => {
        ratingKey.value += 1
    }, 500)
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