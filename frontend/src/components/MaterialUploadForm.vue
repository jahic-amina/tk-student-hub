<template>
  <div>
  <!-- Dugme za otvaranje forme za upload - Lejla -->
  <button
  v-if="!showForm && !isAdmin"
  @click="handleAddClick"
  class="bg-primary text-white px-6 py-3 rounded-lg font-semibold
         hover:bg-orange-600 hover:shadow-md transition-all duration-200"
>
  + DODAJTE MATERIJAL
</button>

  <div v-if="successMessage" class="fixed inset-0 flex items-center justify-center z-50">
  <div class="bg-white dark:bg-slate-800 rounded-xl shadow-xl p-8 max-w-md w-full mx-4 text-center">
    <div class="text-5xl mb-4">✅</div>
    <h3 class="text-xl font-bold text-gray-800 dark:text-slate-100 mb-2">Materijal poslan!</h3>
    <p class="text-gray-600 dark:text-slate-300 mb-6">{{ successMessage }}</p>
    <button
    @click="successMessage = ''; emit('success')"
    class="bg-primary text-white px-6 py-2 rounded-lg hover:bg-orange-600 transition"
  >
    U redu
  </button>
  </div>
  <div class="fixed inset-0 bg-black opacity-40 -z-10"></div>
</div>

 <!-----Polja forme, validacija, drag&drop, submit — Marinela ----->
    <div v-if="showForm" class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mt-6">
      
      <!-- Naslov -->
      <h2 class="text-xl font-bold mb-6 dark:text-white">Dodajte novi materijal</h2>

<!-- Opšta poruka greške -->
<div v-if="formError" class="bg-red-50 dark:bg-red-900/20 border border-red-300 dark:border-red-700 text-red-700 dark:text-red-400 px-4 py-3 rounded-lg mb-4 text-sm">
  {{ formError }}
</div>

      <!-- Polja forme -->
<div class="space-y-4">

  <!-- Naziv materijala -->
  <div>
    <label class="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
      Naziv materijala <span class="text-red-500">*</span>
    </label>
    <input
      v-model="title"
      type="text"
      placeholder="Unesite naziv materijala..."
      class="dark:bg-gray-700 dark:text-white dark:border-gray-600"
     :class="[
    'w-full border rounded-lg px-3 py-2 focus:outline-none',
    errors.title ? 'border-red-500 bg-red-50 dark:bg-red-900/20 dark:border-red-500' : 'border-gray-200 bg-gray-50 focus:border-primary focus:bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white'
  ]"
/>
    <p v-if="errors.title && errors.title !== true" class="text-red-500 text-xs mt-1">{{ errors.title }}</p>
  </div>

  <!-- Opis materijala -->
  <div>
    <label class="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
      Opis materijala <span class="text-red-500">*</span>
    </label>
    <textarea
      v-model="description"
      rows="3"
      placeholder="Napišite detaljan opis materijala..."
      class="dark:bg-gray-700 dark:text-white dark:border-gray-600 dark:placeholder-gray-400"
      :class="[
    'w-full border rounded-lg px-3 py-2 focus:outline-none',
   errors.description ? 'border-red-500 bg-red-50 dark:bg-red-900/20 dark:border-red-500' : 'border-gray-200 bg-gray-50 focus:border-primary focus:bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white'
  ]"
    ></textarea>
    <p v-if="errors.description && errors.description !== true" class="text-red-500 text-xs mt-1">{{ errors.description }}</p>
  </div>

<!-- Tip materijala -->
  <div>
    <label class="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
      Tip materijala <span class="text-red-500">*</span>
    </label>
    <select
      v-model="materialType"
     :class="[
    'w-full border rounded-lg px-3 py-2 focus:outline-none',
    errors.materialType ? 'border-red-500 bg-red-50 dark:bg-red-900/20' : 'border-gray-200 bg-gray-50 focus:border-primary focus:bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white'
  ]"
  >
      <option value="">Odaberite tip</option>
      <option value="skripta">Skripta</option>
      <option value="auditorne_vjezbe">Auditorne vježbe</option>
      <option value="laboratorijske_vjezbe">Laboratorijske vježbe</option>
      <option value="ispiti">Ispiti</option>
      <option value="projekat">Projekat</option>
    </select>
  </div>

  <!-- Godina studija -->
  <div>
    <label class="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
      Godina studija <span class="text-red-500">*</span>
    </label>
    <select
      v-model="studyYear"
     :class="[
    'w-full border rounded-lg px-3 py-2 focus:outline-none',
    errors.studyYear ? 'border-red-500 bg-red-50 dark:bg-red-900/20' : 'border-gray-200 bg-gray-50 focus:border-primary focus:bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white'
  ]"
  >
      <option value="">Odaberite godinu</option>
      <option value="1">1. godina</option>
      <option value="2">2. godina</option>
      <option value="3">3. godina</option>
      <option value="4">4. godina</option>
    </select>
  </div>

  <!-- Predmet -->
  <div>
    <label class="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
      Predmet <span class="text-red-500">*</span>
    </label>
    <select
      v-model="subjectId"
   :class="[
    'w-full border rounded-lg px-3 py-2 focus:outline-none',
    errors.subjectId ? 'border-red-500 bg-red-50 dark:bg-red-900/20' : 'border-gray-200 bg-gray-50 focus:border-primary focus:bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white'
  ]"
>
      <option value="">Odaberite predmet</option>
<option v-for="subject in filteredSubjects" :key="subject.id" :value="subject.id">
  {{ subject.name }}
</option>
    </select>
  </div>

  <!-- Priloži fajl — drag & drop zona -->
  <div>
    <label class="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
      Priloži fajl <span class="text-red-500">*</span>
    </label>
    <div
      @click="triggerFileInput"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @drop.prevent="onFileDrop"
      :class="[
  'border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors',
  errors.file
    ? 'border-red-500 bg-red-50 dark:bg-red-900/20'
    : (isDragging ? 'border-primary bg-orange-50' : 'border-gray-300 bg-gray-50 dark:bg-gray-700 dark:border-gray-600')
]"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 mx-auto mb-2 text-gray-400"
           fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
        <path stroke-linecap="round" stroke-linejoin="round"
              d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2M7 10l5-5 5 5M12 5v10" />
      </svg>
      <p class="text-gray-700 dark:text-gray-200 font-medium">
        Prevucite fajl ovdje ili kliknite da odaberete
      </p>
      <p class="text-gray-700 dark:text-gray-200 font-medium">
        Podržani formati: PDF, DOC, DOCX, TXT, PPT, PPTX, ZIP
      </p>
      <p v-if="selectedFile" class="text-sm text-primary font-medium mt-3">
        Odabran: {{ selectedFile.name }}
      </p>
    </div>
    <!-- Skriven HTML file input — drag zona poziva njegov klik programski -->
    <input
      ref="fileInput"
      type="file"
      @change="onFileChange"
      accept=".pdf,.doc,.docx,.ppt,.pptx,.zip,.txt"
      class="hidden"
    />
  </div>

</div>

      

      <div v-if="uploadError" class="bg-red-50 dark:bg-red-900/20 border border-red-300 dark:border-red-700 text-red-700 dark:text-red-400 px-4 py-3 rounded-lg mb-4">
  ⚠️ {{ uploadError }}
</div>

      
      <div class="flex gap-3 mt-6">
        <button
          @click="handleSubmit"
          :disabled="isSubmitting"
          class="bg-primary text-white px-6 py-2 rounded-lg font-semibold
                 hover:bg-orange-600 transition-all duration-200 disabled:opacity-50"
        >
          {{ isSubmitting ? 'Slanje...' : '+Dodaj materijal' }}
        </button>
        <button
        @click="props.directShow ? router.push('/materials') : showForm = false"
        class="border border-gray-300 dark:border-gray-600 dark:text-gray-200 px-6 py-2 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-all duration-200">
        Odustani
      </button>
      </div>

    </div>
  </div>
</template>

<script setup>

// ============================================================
// Dugme "+ DODAJTE MATERIJAL" — Lejla
// Forma, validacija, drag&drop, upload na backend — Marinela
// ============================================================

import { ref, watch, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { uploadMaterial, getSubjects } from '../services/api'

const router = useRouter()
// Prop koji kontroliše da li se forma prikazuje odmah (true) ili tek nakon klika na dugme (false)
// Postavlja se na true kad se forma otvara na posebnoj stranici /materials/upload - Marinela
const props = defineProps({
  directShow: {
    type: Boolean,
    default: false
  }
})

const isAdmin = localStorage.getItem('role') === 'admin'

// Reaktivne varijable za stanje
const showForm = ref(props.directShow)
const successMessage = ref('')
const uploadError = ref('')
const isSubmitting = ref(false)

// Klik na dugme "Dodajte materijal" — neprijavljene preusmjeravas na login,
// prijavljene na stranicu za upload 
function handleAddClick() {
  const isLoggedIn = !!localStorage.getItem('token')
  if (!isLoggedIn) {
    window.location.href = '/login'
  } else {
    window.location.href = '/materials/upload' 
  }
}

// Polja forme — vezana za v-model u templatu
const title = ref('')
const description = ref('')
const studyYear = ref('')
const materialType = ref('')
const subjectId = ref('')
const selectedFile = ref(null)
const subjects = ref([]) // Lista svih predmeta sa backenda

// Filtrira predmete prema odabranoj godini studija
const filteredSubjects = computed(() => {
  if (!studyYear.value) return []
  return subjects.value.filter(s => s.study_year == studyYear.value)
})

// Učitava predmete sa backenda pri mountovanju komponente
onMounted(async () => {
  subjects.value = await getSubjects()
})

// Drag & drop — prati stanje prevlačenja fajla
const isDragging = ref(false)
const fileInput = ref(null)

// Klik na drag zonu — programski otvara file picker bez vidljivog inputa
function triggerFileInput() {
  fileInput.value.click()
}

// Korisnik odabrao fajl kroz standardni file picker
function onFileChange(event) {
  selectedFile.value = event.target.files[0] || null
}

// Korisnik prevukao fajl u drag zonu — uzima prvi fajl iz liste
function onFileDrop(event) {
  isDragging.value = false
  const files = event.dataTransfer.files
  if (files.length > 0) {
    selectedFile.value = files[0]
  }
}

// Objekti za greške po poljima (za crveni border) i opća poruka greške
const errors = ref({})         
const formError = ref('')       
const emit = defineEmits(['submit' , 'success'])

// Prolazi kroz sva polja, označava prazna kao greške, vraća true ako je sve ispravno
function validateForm() {
  const e = {}
    if (!title.value.trim()) e.title = true
  else if (title.value.trim().length < 3) e.title = 'Naziv mora imati najmanje 3 karaktera.'
  else if (title.value.trim().length > 100) e.title = 'Naziv ne može biti duži od 100 karaktera.'

    if (!description.value.trim()) e.description = true
  else if (description.value.trim().length < 10) e.description = 'Opis mora imati najmanje 10 karaktera.'
  else if (description.value.trim().length > 1000) e.description = 'Opis ne može biti duži od 1000 karaktera.'
  
  if (!studyYear.value) e.studyYear = true
  if (!subjectId.value) e.subjectId = true
  if (!materialType.value) e.materialType = true
  if (!selectedFile.value) e.file = true

  errors.value = e

  const valid = Object.keys(e).length === 0
  formError.value = valid ? '' : 'Molimo ispravite greške u formi i pokušajte ponovo.'
  return valid
}

// Validira formu, kreira FormData i šalje na backend — obradjuje greške po statusu
async function handleSubmit() {
  if (!validateForm()) return

  uploadError.value = ''
  successMessage.value = ''
  isSubmitting.value = true

  try {
    const formData = new FormData()
    formData.append('title', title.value.trim())
    formData.append('description', description.value.trim())
    formData.append('subject_id', subjectId.value)
    formData.append('file_type', materialType.value)
    formData.append('file', selectedFile.value)

    const response = await uploadMaterial(formData)

    if (!response.ok) {
  const data = await response.json().catch(() => ({}))
  if (response.status === 401) {

    // Token istekao — obriši ga i preusmjeri na login
    localStorage.removeItem('token')
    window.location.href = '/login'
    return
  }
  if (response.status === 400) throw new Error(data.detail || 'Format fajla nije podržan.')
  if (response.status === 409) throw new Error(data.detail || 'Materijal već postoji.')
  throw new Error(data.detail || 'Greška prilikom dodavanja materijala.')
}

    const created = await response.json()
    successMessage.value = 'Materijal je uspješno poslan na pregled. Status: Na čekanju.'
    
    // Resetuj sva polja nakon uspješnog slanja
    title.value = ''
    description.value = ''
    studyYear.value = ''
    subjectId.value = ''
    materialType.value = ''
    selectedFile.value = null
    errors.value = {}

    emit('submit', created)

    // Sakrij formu samo ako nije direktno prikazana na posebnoj stranici
    if (!props.directShow) {
      showForm.value = false
    }

  } catch (err) {
    uploadError.value = err.message || 'Greška prilikom dodavanja materijala.'
  } finally {
    isSubmitting.value = false
  }
}

// Automatski ponovo validira formu čim korisnik promijeni bilo koje polje
// — greške se brišu čim se polje ispravno popuni
watch(
  [title, description, studyYear, subjectId, materialType, selectedFile],
  () => {
    if (formError.value) validateForm()
  }
)
</script>