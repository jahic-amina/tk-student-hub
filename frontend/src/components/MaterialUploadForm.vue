<template>
  <div>
    
  <button
  @click="handleDodajKlik"
  class="bg-primary text-white px-6 py-3 rounded-lg font-semibold
         hover:bg-orange-600 hover:shadow-md transition-all duration-200"
>
  + DODAJTE MATERIJAL
</button>

    
    <div v-if="showForm" class="bg-white rounded-lg shadow p-6 mt-6">
      
      <!-- Naslov -->
      <h2 class="text-xl font-bold mb-6">Dodajte novi materijal</h2>

<!-- Opšta poruka greške -->
<div v-if="formError" class="bg-red-50 border border-red-300 text-red-700 px-4 py-3 rounded-lg mb-4 text-sm">
  {{ formError }}
</div>

      <!-- Polja forme -->
<div class="space-y-4">

  <!-- Naziv materijala -->
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-1">
      Naziv materijala <span class="text-red-500">*</span>
    </label>
    <input
      v-model="title"
      type="text"
      placeholder="Unesite naziv materijala..."
      :class="[
                'w-full border rounded-lg px-3 py-2 focus:outline-none',
                errors.title ? 'border-red-500 bg-red-50' : 'border-gray-200 bg-gray-50 focus:border-primary focus:bg-white'
              ]"
    />
  </div>

  <!-- Opis materijala -->
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-1">
      Opis materijala <span class="text-red-500">*</span>
    </label>
    <textarea
      v-model="description"
      rows="3"
      placeholder="Napisite detaljan opis materijala..."
     :class="[
              'w-full border rounded-lg px-3 py-2 focus:outline-none',
              errors.description ? 'border-red-500 bg-red-50' : 'border-gray-200 bg-gray-50 focus:border-primary focus:bg-white'
            ]"
    ></textarea>
  </div>

<!-- Tip materijala -->
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-1">
      Tip materijala <span class="text-red-500">*</span>
    </label>
    <select
      v-model="materialType"
     :class="[
              'w-full border rounded-lg px-3 py-2 focus:outline-none',
              errors.materialType ? 'border-red-500 bg-red-50' : 'border-gray-200 bg-gray-50 focus:border-primary focus:bg-white'
            ]"
>
      <option value="">Odaberite tip</option>
      <option value="skripta">Skripta</option>
      <option value="auditorne_vježbe">Auditorne vježbe</option>
      <option value="laboratorijske_vježbe">Laboratorijske vježbe</option>
      <option value="ispiti">Ispiti</option>
      <option value="projekat">Projekat</option>
    </select>
  </div>

  <!-- Godina studija -->
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-1">
      Godina studija <span class="text-red-500">*</span>
    </label>
    <select
      v-model="studyYear"
     :class="[
              'w-full border rounded-lg px-3 py-2 focus:outline-none',
              errors.studyYear ? 'border-red-500 bg-red-50' : 'border-gray-200 bg-gray-50 focus:border-primary focus:bg-white'
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
    <label class="block text-sm font-medium text-gray-700 mb-1">
      Predmet <span class="text-red-500">*</span>
    </label>
    <select
      v-model="subjectId"
     :class="[
              'w-full border rounded-lg px-3 py-2 focus:outline-none',
              errors.subjectId ? 'border-red-500 bg-red-50' : 'border-gray-200 bg-gray-50 focus:border-primary focus:bg-white'
            ]"
>
      <option value="">Odaberite predmet</option>
      <!-- TODO: zamijeniti sa GET /subjects kad kolegica to napravi -->
      <option value="1">Telekomunikacione mreže</option>
      <option value="2">Telekomunikacijski protokoli</option>
      <option value="3">Razvoj telekomunikacijske programske podrške </option>
      <option value="4">Matematika I</option>
    </select>
  </div>

  <!-- Priloži fajl — drag & drop zona -->
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-1">
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
                    ? 'border-red-500 bg-red-50'
                    : (isDragging ? 'border-primary bg-orange-50' : 'border-gray-300 bg-gray-50')
                ]"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 mx-auto mb-2 text-gray-400"
           fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
        <path stroke-linecap="round" stroke-linejoin="round"
              d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2M7 10l5-5 5 5M12 5v10" />
      </svg>
      <p class="text-gray-700 font-medium">
        Prevucite fajl ovdje ili kliknite da odaberete
      </p>
      <p class="text-sm text-gray-500 mt-1">
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

      <!-- NEDOVRŠENO:poruka uspjeha -->
      <p v-if="successMessage" class="text-green-600 font-medium mb-4">
        {{ successMessage }}
      </p>

      <!-- NEDOVRŠENO: greška -->
      <p v-if="uploadError" class="text-red-500 font-medium mb-4">
        {{ uploadError }}
      </p>

      
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
          @click="showForm = false"
          class="border border-gray-300 px-6 py-2 rounded-lg
                 hover:bg-gray-50 transition-all duration-200"
        >
          Odustani
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const showForm = ref(false)
const successMessage = ref('')
const uploadError = ref('')
const isSubmitting = ref(false)

function handleDodajKlik() {
  const isLoggedIn = !!localStorage.getItem('token')
  if (!isLoggedIn) {
    window.location.href = '/login'
  } else {
    showForm.value = true
  }
}

// === Polja forme — Marinela ===
const title = ref('')
const description = ref('')
const studyYear = ref('')
const materialType = ref('')
const subjectId = ref('')
const selectedFile = ref(null)

// === Drag & drop state ===
const isDragging = ref(false)
const fileInput = ref(null)

// Klik na drag zonu — programski klikne hidden <input type="file">
function triggerFileInput() {
  fileInput.value.click()
}

// Handler za standardni file picker
function onFileChange(event) {
  selectedFile.value = event.target.files[0] || null
}

// Handler za drag & drop
function onFileDrop(event) {
  isDragging.value = false
  const files = event.dataTransfer.files
  if (files.length > 0) {
    selectedFile.value = files[0]
  }
}

// === Validacija ===
const errors = ref({})         
const formError = ref('')       
const emit = defineEmits(['submit'])

// Provjeri sva polja, popuni errors, vrati true/false
function validateForm() {
  const e = {}
  if (!title.value.trim()) e.title = true
  if (!description.value.trim()) e.description = true
  if (!studyYear.value) e.studyYear = true
  if (!subjectId.value) e.subjectId = true
  if (!materialType.value) e.materialType = true
  if (!selectedFile.value) e.file = true

  errors.value = e

  const valid = Object.keys(e).length === 0
  formError.value = valid ? '' : 'Molimo ispravite greške u formi i pokušajte ponovo.'
  return valid
}

// Klik na "Dodaj materijal" — prvo validira, pa emit
function handleSubmit() {
  if (!validateForm()) return
  emit('submit')
}

// Watch — kad korisnik promijeni bilo koje polje, ako je validacija već
// triggerovana, ponovo validiraj (greske se same brišu kad popuni polje)
watch(
  [title, description, studyYear, subjectId, materialType, selectedFile],
  () => {
    if (formError.value) validateForm()
  }
)
</script>