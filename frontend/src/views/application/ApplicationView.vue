<template>
  <div class="min-h-screen bg-gradient-to-b from-orange-50 via-white to-white">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 py-8 md:py-12">
      <div class="mb-6">
        <button @click="$router.back()" class="text-sm font-semibold text-orange-600 hover:text-orange-700 transition">
          ← Nazad
        </button>
      </div>

      <div v-if="!ad" class="rounded-3xl border border-gray-100 bg-white shadow-sm p-8 text-center text-gray-500">
        Učitavanje detalja oglasa...
      </div>

      <div v-else>
        <div class="rounded-3xl border border-gray-100 bg-white shadow-sm p-6 sm:p-8 mb-6">
          <h1 class="text-3xl font-bold text-gray-900 mb-2">Prijava za: {{ ad.title }}</h1>
          <p class="text-gray-600">
            <router-link :to="`/companies/${ad.company_id}`" class="text-orange-600 hover:text-orange-700 font-medium">
              {{ ad.company }}
            </router-link>
          </p>
        </div>

        <div class="rounded-3xl border border-gray-100 bg-white shadow-sm p-6 sm:p-8">
          <form @submit.prevent="submitApplication" class="space-y-6">
            <!-- Errors -->
            <div v-if="error" class="rounded-2xl border border-red-200 bg-red-50 p-4 text-red-700">
              {{ error }}
            </div>

            <!-- Success Message -->
            <div v-if="successMessage" class="rounded-2xl border border-green-200 bg-green-50 p-4 text-green-700">
              {{ successMessage }}
            </div>

            <!-- Phone Number -->
            <div>
              <label class="block text-sm font-bold text-gray-900 mb-2">Telefonski broj *</label>
              <input
                v-model="form.phone"
                type="tel"
                placeholder="+387 61 234 567"
                required
                class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              />
              <p class="text-xs text-gray-500 mt-1">Npr. +387 61 123 456 ili 061 123 456</p>
            </div>

            <!-- CV Upload -->
            <div>
              <label class="block text-sm font-bold text-gray-900 mb-2">CV/Životopis *</label>
              <div
                @dragover.prevent="cvDragActive = true"
                @dragleave="cvDragActive = false"
                @drop.prevent="handleCvDrop"
                :class="[
                  'rounded-lg border-2 border-dashed p-6 text-center cursor-pointer transition',
                  cvDragActive ? 'border-orange-500 bg-orange-50' : 'border-gray-300 hover:border-orange-300'
                ]"
                @click="$refs.cvInput.click()"
              >
                <input
                  ref="cvInput"
                  type="file"
                  accept=".pdf"
                  @change="handleCvChange"
                  class="hidden"
                  required
                />
                <div v-if="!form.cvFile" class="text-gray-600">
                <div v-if="!form.cvFile" class="text-gray-600">
                  <p class="font-medium">Klikni da odabereš fajl ili povuci i pusti ovdje</p>
                  <p class="text-xs text-gray-500 mt-1">PDF (max 5MB)</p>
                <div v-else class="text-green-600">
                  <p class="font-medium">✓ {{ form.cvFile.name }}</p>
                  <button
                    type="button"
                    @click.stop="form.cvFile = null; cvUploadProgress = 0"
                    class="text-xs text-orange-600 hover:text-orange-700 mt-1 underline"
                  >
                    Ukloni
                  </button>
                </div>
                <div v-if="cvUploadProgress > 0 && cvUploadProgress < 100" class="mt-2">
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-orange-600 h-2 rounded-full transition" :style="{ width: cvUploadProgress + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Motivational Letter Upload -->
            <div>
              <label class="block text-sm font-bold text-gray-900 mb-2">Motivaciono pismo *</label>
              <div
                @dragover.prevent="letterDragActive = true"
                @dragleave="letterDragActive = false"
                @drop.prevent="handleLetterDrop"
                :class="[
                  'rounded-lg border-2 border-dashed p-6 text-center cursor-pointer transition',
                  letterDragActive ? 'border-orange-500 bg-orange-50' : 'border-gray-300 hover:border-orange-300'
                ]"
                @click="$refs.letterInput.click()"
              >
                <input
                  ref="letterInput"
                  type="file"
                  accept=".pdf"
                  @change="handleLetterChange"
                  class="hidden"
                  required
                />
                <div v-if="!form.letterFile" class="text-gray-600">
                <div v-if="!form.letterFile" class="text-gray-600">
                  <p class="font-medium">Klikni da odabereš fajl ili povuci i pusti ovdje</p>
                  <p class="text-xs text-gray-500 mt-1">PDF (max 5MB)</p>
                <div v-else class="text-green-600">
                  <p class="font-medium">✓ {{ form.letterFile.name }}</p>
                  <button
                    type="button"
                    @click.stop="form.letterFile = null; letterUploadProgress = 0"
                    class="text-xs text-orange-600 hover:text-orange-700 mt-1 underline"
                  >
                    Ukloni
                  </button>
                </div>
                <div v-if="letterUploadProgress > 0 && letterUploadProgress < 100" class="mt-2">
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-orange-600 h-2 rounded-full transition" :style="{ width: letterUploadProgress + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- LinkedIn URL -->
            <div>
              <label class="block text-sm font-bold text-gray-900 mb-2">LinkedIn profil (opciono)</label>
              <input
                v-model="form.linkedinUrl"
                type="url"
                placeholder="https://linkedin.com/in/tvoje-ime"
                class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              />
              <p class="text-xs text-gray-500 mt-1">Npr. https://linkedin.com/in/marko-markovic</p>
            </div>

            <!-- Submit Button -->
            <button
              type="submit"
              :disabled="loading || !form.cvFile || !form.letterFile || !form.phone"
              class="w-full bg-orange-600 text-white py-3 rounded-lg hover:bg-orange-700 transition font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ loading ? 'Slanje prijave...' : 'Pošalji prijavu' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getAdById, uploadFile, createApplication, getApprovedCompanies } from '../../services/api.js'

export default {
  name: 'ApplicationView',
  data() {
    return {
      ad: null,
      loading: false,
      error: '',
      successMessage: '',
      cvDragActive: false,
      letterDragActive: false,
      cvUploadProgress: 0,
      letterUploadProgress: 0,
      form: {
        phone: '',
        linkedinUrl: '',
        cvFile: null,
        letterFile: null,
        cvPath: null,
        letterPath: null
      }
    }
  },
  methods: {
    async fetchAd() {
      const adId = Number(this.$route.params.id)
      try {
        const [ad, companies] = await Promise.all([
          getAdById(adId),
          getApprovedCompanies()
        ])

        if (!ad) {
          this.error = 'Oglas nije pronađen.'
          return
        }

        const companiesById = new Map(
          (companies || []).map(company => [company.id, company.company_name])
        )

        this.ad = {
          id: ad.id,
          title: ad.title,
          company: companiesById.get(ad.company_id) || `Kompanija #${ad.company_id}`,
          company_id: ad.company_id
        }
      } catch (err) {
        console.error('Error fetching ad:', err)
        this.error = 'Ne mogu učitati detalje oglasa.'
      }
    },

    handleCvChange(event) {
      this.form.cvFile = event.target.files[0]
    },

    handleCvDrop(event) {
      this.cvDragActive = false
      const file = event.dataTransfer.files[0]
      if (file && this.isValidFile(file)) {
        this.form.cvFile = file
      } else {
        this.error = 'Molim odaberi PDF, DOC ili DOCX datoteku.'
      }
    },

    handleLetterChange(event) {
      this.form.letterFile = event.target.files[0]
    },

    handleLetterDrop(event) {
      this.letterDragActive = false
      const file = event.dataTransfer.files[0]
      if (file && this.isValidFile(file)) {
        this.form.letterFile = file
      } else {
        this.error = 'Molim odaberi PDF, DOC ili DOCX datoteku.'
      }
    },

    isValidFile(file) {
      const validTypes = ['application/pdf']
      const validExtensions = ['pdf']
      const ext = file.name.split('.').pop().toLowerCase()
      return validTypes.includes(file.type) && validExtensions.includes(ext) && file.size <= 5 * 1024 * 1024
    }

    async uploadFile(file) {
      try {
        const response = await uploadFile(file)
        return response.path
      } catch (err) {
        throw new Error(`Greška pri uploadovanju fajla: ${file.name}`)
      }
    },

    async submitApplication() {
      this.error = ''
      this.successMessage = ''

      // Validacija
      if (!this.form.phone || !this.form.cvFile || !this.form.letterFile) {
        this.error = 'Molim popuni sva obavezna polja.'
        return
      }

      if (!this.isValidFile(this.form.cvFile) || !this.isValidFile(this.form.letterFile)) {
        this.error = 'Jedan ili više fajlova nisu u validnom formatu.'
        return
      }

      this.loading = true

      try {
        // Upload CV
        this.form.cvPath = await this.uploadFile(this.form.cvFile)
        this.cvUploadProgress = 50

        // Upload motivational letter
        this.form.letterPath = await this.uploadFile(this.form.letterFile)
        this.letterUploadProgress = 50

        // Create application
        const token = localStorage.getItem('token')
        await createApplication(
          {
            ad_id: this.ad.id,
            phone: this.form.phone,
            cv_path: this.form.cvPath,
            motivational_letter_path: this.form.letterPath,
            linkedin_url: this.form.linkedinUrl || null
          },
          token
        )

        this.successMessage = 'Prijava je uspješno poslana!'
        setTimeout(() => {
          this.$router.push(`/ads/${this.ad.id}`)
        }, 2000)
      } catch (err) {
        console.error('Error submitting application:', err)
        this.error = err.message || 'Došlo je do greške pri slanju prijave.'
      } finally {
        this.loading = false
      }
    }
  },
  mounted() {
    this.fetchAd()
  }
}
</script>
