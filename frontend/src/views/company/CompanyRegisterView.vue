<template>
  <div class="min-h-screen bg-gray-50 py-10 px-4 font-sans">
    <div class="max-w-4xl mx-auto">

      <div class="mb-8 text-center">
        <h1 class="text-2xl sm:text-3xl font-black text-gray-900">Registracija kompanije</h1>
        <p class="text-gray-500 mt-2 text-sm sm:text-base">Kompanije dobijaju pristup predlaganju praksi i edukacija.</p>
      </div>

      <div class="flex flex-col lg:flex-row gap-6 items-start">

        <div class="w-full lg:flex-1 bg-white rounded-2xl shadow-sm border border-gray-100 p-6 sm:p-8">

          <div v-if="submitStatus === 'success'" class="mb-6 p-4 bg-green-50 border border-green-200 rounded-xl text-green-700 text-sm font-medium">
            Registracija uspješna! Vaš zahtjev je poslan na odobravanje.
          </div>

          <div v-if="submitStatus === 'error'" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm font-medium">
            {{ serverError }}
          </div>

          <template v-if="submitStatus !== 'success'">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
              <div class="flex flex-col gap-1">
                <label for="company_name" class="text-sm font-semibold text-gray-700">Naziv kompanije</label>
                <input
                  id="company_name"
                  v-model="form.company_name"
                  type="text"
                  :class="inputClass(errors.company_name)"
                  placeholder="HT Eronet d.o.o."
                  @blur="validateField('company_name')"
                />
                <span v-if="errors.company_name" class="text-xs text-red-500">{{ errors.company_name }}</span>
              </div>
              <div class="flex flex-col gap-1">
                <label for="tin" class="text-sm font-semibold text-gray-700">TIN</label>
                <input
                  id="tin"
                  v-model="form.tin"
                  type="text"
                  :class="inputClass(errors.tin)"
                  placeholder="4200000000000"
                  @blur="validateField('tin')"
                />
                <span v-if="errors.tin" class="text-xs text-red-500">{{ errors.tin }}</span>
              </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
              <div class="flex flex-col gap-1">
                <label for="website_url" class="text-sm font-semibold text-gray-700">Web stranica</label>
                <input
                  id="website_url"
                  v-model="form.website_url"
                  type="url"
                  :class="inputClass(errors.website_url)"
                  placeholder="https://hteronet.ba"
                  @blur="validateField('website_url')"
                />
                <span v-if="errors.website_url" class="text-xs text-red-500">{{ errors.website_url }}</span>
              </div>
              <div class="flex flex-col gap-1">
                <label for="address" class="text-sm font-semibold text-gray-700">Adresa</label>
                <input
                  id="address"
                  v-model="form.address"
                  type="text"
                  :class="inputClass(errors.address)"
                  placeholder="Kneza Višeslava 1, Mostar"
                  @blur="validateField('address')"
                />
                <span v-if="errors.address" class="text-xs text-red-500">{{ errors.address }}</span>
              </div>
            </div>

            <div class="mb-4">
              <div class="flex flex-col gap-1">
                <label for="description" class="text-sm font-semibold text-gray-700">Opis kompanije</label>
                <textarea
                  id="description"
                  v-model="form.description"
                  :class="inputClass(errors.description)"
                  rows="3"
                  placeholder="Telekom operator sa fokusom na mobilne, fiksne i optičke mreže."
                  @blur="validateField('description')"
                />
                <span v-if="errors.description" class="text-xs text-red-500">{{ errors.description }}</span>
              </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
              <div class="flex flex-col gap-1">
                <label for="email" class="text-sm font-semibold text-gray-700">Email kompanije</label>
                <input
                  id="email"
                  v-model="form.email"
                  type="email"
                  :class="inputClass(errors.email)"
                  placeholder="hr@hteronet.ba"
                  @blur="validateField('email')"
                />
                <span v-if="errors.email" class="text-xs text-red-500">{{ errors.email }}</span>
              </div>
              <div class="flex flex-col gap-1">
                <label for="phone_number" class="text-sm font-semibold text-gray-700">Broj telefona</label>
                <input
                  id="phone_number"
                  v-model="form.phone_number"
                  type="tel"
                  :class="inputClass(errors.phone_number)"
                  placeholder="+387 36 000 000"
                  @blur="validateField('phone_number')"
                />
                <span v-if="errors.phone_number" class="text-xs text-red-500">{{ errors.phone_number }}</span>
              </div>
            </div>

            <div class="mb-4">
              <div class="flex flex-col gap-1">
                <label for="logo" class="text-sm font-semibold text-gray-700">Logo kompanije</label>
                <input
                  id="logo"
                  type="file"
                  accept=".png,.jpg,.jpeg,.webp"
                  :class="inputClass(errors.logo)"
                  @change="handleLogoChange"
                />
                <span v-if="logoPreview" class="mt-2">
                  <img :src="logoPreview" alt="Logo preview" class="h-16 w-16 object-contain rounded-lg border border-gray-200" />
                </span>
                <span v-if="errors.logo" class="text-xs text-red-500">{{ errors.logo }}</span>
              </div>
            </div>

            <div class="mb-6">
              <div class="flex flex-col gap-1">
                <label for="password" class="text-sm font-semibold text-gray-700">Lozinka</label>
                <input
                  id="password"
                  v-model="form.password"
                  type="password"
                  :class="inputClass(errors.password)"
                  placeholder="Minimalno 8 karaktera"
                  @blur="validateField('password')"
                />
                <span v-if="errors.password" class="text-xs text-red-500">{{ errors.password }}</span>
              </div>
            </div>

            <button
              :disabled="isLoading"
              @click="handleSubmit"
              class="w-full bg-orange-500 hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-xl transition text-sm"
            >
              <span v-if="isLoading">Slanje...</span>
              <span v-else>Registruj kompaniju</span>
            </button>
          </template>

        </div>

        <div class="w-full lg:w-72 bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <h3 class="text-base font-bold text-gray-900 mb-4">Nakon registracije</h3>
          <div v-for="(step, i) in steps" :key="i" class="flex gap-3 mb-4 last:mb-0">
            <div class="flex-shrink-0 w-7 h-7 rounded-full bg-orange-100 text-orange-600 text-xs font-bold flex items-center justify-center">
              {{ i + 1 }}
            </div>
            <p class="text-sm text-gray-600 leading-relaxed">{{ step }}</p>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { registerCompany } from '../../services/api.js'

const ALLOWED_TYPES = ['image/png', 'image/jpeg', 'image/webp']

const form = reactive({
  company_name: '',
  tin: '',
  website_url: '',
  address: '',
  description: '',
  email: '',
  phone_number: '',
  password: '',
})

const errors = reactive({
  company_name: '',
  tin: '',
  website_url: '',
  address: '',
  description: '',
  email: '',
  phone_number: '',
  logo: '',
  password: '',
})

const logoFile = ref(null)
const logoPreview = ref(null)
const isLoading = ref(false)
const submitStatus = ref(null)
const serverError = ref('')

const steps = [
  'Predlažete praksu ili edukaciju.',
  'Administrator odobrava sadržaj prije objave.',
  'Pratite statuse prijedloga i prijave studenata.',
]

const inputClass = (error) =>
  `w-full px-4 py-2.5 bg-gray-50 border rounded-lg text-sm focus:outline-none focus:border-orange-400 ${
    error ? 'border-red-400' : 'border-gray-200'
  }`

const handleLogoChange = (e) => {
  const file = e.target.files[0]
  if (!file) return

  if (!ALLOWED_TYPES.includes(file.type)) {
    errors.logo = 'Logo mora biti PNG, JPG, JPEG ili WebP.'
    logoFile.value = null
    logoPreview.value = null
    return
  }

  errors.logo = ''
  logoFile.value = file
  logoPreview.value = URL.createObjectURL(file)
}

const validators = {
  company_name: (v) => v.trim() ? '' : 'Naziv kompanije je obavezan.',
  tin: (v) => {
    if (!v.trim()) return 'TIN je obavezan.'
    if (!/^\d{13}$/.test(v.trim())) return 'TIN mora sadržavati tačno 13 cifara.'
    return ''
  },
  website_url: (v) => {
    if (!v.trim()) return 'Web stranica je obavezna.'
    try { new URL(v.trim()); return '' }
    catch { return 'Unesite validan URL (npr. https://kompanija.ba).' }
  },
  address: (v) => v.trim() ? '' : 'Adresa je obavezna.',
  description: (v) => v.trim() ? '' : 'Opis kompanije je obavezan.',
  email: (v) => {
    if (!v.trim()) return 'Email je obavezan.'
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim())) return 'Unesite validan email.'
    return ''
  },
  phone_number: (v) => v.trim() ? '' : 'Broj telefona je obavezan.',
  password: (v) => {
    if (!v.trim()) return 'Lozinka je obavezna.'
    if (v.length < 8) return 'Lozinka mora imati najmanje 8 karaktera.'
    return ''
  },
}

const validateField = (field) => {
  errors[field] = validators[field](form[field])
}

const handleSubmit = async () => {
  Object.keys(validators).forEach(field => validateField(field))

  if (!logoFile.value) {
    errors.logo = 'Logo je obavezan.'
  }

  if (Object.values(errors).some(e => e !== '')) return

  isLoading.value = true
  try {
    await registerCompany({ ...form }, logoFile.value)
    submitStatus.value = 'success'
  } catch (err) {
    submitStatus.value = 'error'
    serverError.value = err.message || 'Došlo je do greške. Pokušajte ponovo.'
  } finally {
    isLoading.value = false
  }
}
</script>