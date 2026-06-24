<template>
  <div class="min-h-screen bg-gradient-to-b from-orange-50 via-white to-white dark:from-slate-900/50 dark:via-slate-900 dark:to-slate-900 transition-colors duration-200">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-8 md:py-12">
      <div class="mb-6">
        <router-link to="/ads" class="text-sm font-semibold text-orange-600 dark:text-orange-400 hover:text-orange-700 dark:hover:text-orange-300 transition">
          ← Nazad na listu oglasa
        </router-link>
      </div>

      <div v-if="loading" class="rounded-3xl border border-gray-100 dark:border-slate-800 bg-white dark:bg-slate-800 shadow-sm p-8 text-center text-gray-500 dark:text-slate-400">
        Učitavanje detalja oglasa...
      </div>

      <div v-else-if="errorMessage" class="rounded-3xl border border-red-100 dark:border-red-900/50 bg-red-50 dark:bg-red-950/20 p-8 text-red-700 dark:text-red-400">
        {{ errorMessage }}
      </div>

      <div v-else-if="ad" class="flex flex-col gap-6">
        
        <div class="grid gap-6 lg:grid-cols-[1.6fr_0.9fr] items-start">
          
          <section class="rounded-3xl border border-gray-100 dark:border-slate-800 bg-white dark:bg-slate-800 shadow-sm p-6 sm:p-8 relative">
            
            <button 
              v-if="isUserLoggedIn && !isCompanyLoggedIn && !isAdmin"
              @click.prevent="toggleBookmark" 
              class="absolute top-6 right-6 focus:outline-none transition-transform hover:scale-110 active:scale-95 z-10 bg-transparent border-none cursor-pointer"
              title="Sačuvaj oglas"
            >
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                :fill="bookmarkId ? 'currentColor' : 'none'" 
                viewBox="0 0 24 24" 
                stroke-width="1.5" 
                stroke="currentColor" 
                :class="[
                  'w-8 h-8 transition-colors duration-300', 
                  bookmarkId ? 'text-orange-500 dark:text-orange-400' : 'text-gray-300 dark:text-slate-600 hover:text-orange-400 dark:hover:text-orange-500'
                ]"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M17.593 3.322c1.1.128 1.907 1.077 1.907 2.185V21L12 17.25 4.5 21V5.507c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0111.186 0z" />
              </svg>
            </button>

            <div class="flex flex-wrap gap-2 mb-4 text-xs font-semibold pr-12">
              <span :class="getTypeClass(ad.typeLabel)">{{ ad.typeLabel }}</span>
              <span :class="getStatusClass(ad.statusLabel)">{{ ad.statusLabel }}</span>
            </div>

            <h1 class="text-2xl sm:text-4xl font-black text-gray-900 dark:text-slate-100 leading-tight mb-3 pr-12">
              {{ ad.title }}
            </h1>

            <p class="text-base sm:text-lg text-gray-600 dark:text-slate-400 font-medium mb-6">
              <router-link :to="`/companies/${ad.company_id}`" class="hover:text-orange-500 dark:hover:text-orange-400 transition-colors">
                {{ ad.company }}
              </router-link>
            </p>

            <div class="grid sm:grid-cols-3 gap-3 mb-8">
              <div class="rounded-2xl bg-gray-50 dark:bg-slate-900/50 border border-gray-100 dark:border-slate-700/50 p-4">
                <p class="text-xs uppercase tracking-wide text-gray-400 dark:text-slate-500 font-semibold mb-1">Lokacija</p>
                <p class="text-sm font-bold text-gray-990 dark:text-slate-200">{{ ad.location || 'Nije navedeno' }}</p>
              </div>
              <div class="rounded-2xl bg-gray-50 dark:bg-slate-900/50 border border-gray-100 dark:border-slate-700/50 p-4">
                <p class="text-xs uppercase tracking-wide text-gray-400 dark:text-slate-500 font-semibold mb-1">Trajanje</p>
                <p class="text-sm font-bold text-gray-900 dark:text-slate-200">{{ ad.duration || 'Nije navedeno' }}</p>
              </div>
              <div class="rounded-2xl bg-gray-50 dark:bg-slate-900/50 border border-gray-100 dark:border-slate-700/50 p-4">
                <p class="text-xs uppercase tracking-wide text-gray-400 dark:text-slate-500 font-semibold mb-1">Naknada</p>
                <p class="text-sm font-bold text-gray-900 dark:text-slate-200">{{ ad.compensation || 'Nije navedeno' }}</p>
              </div>
            </div>

            <div class="space-y-6 text-gray-700 dark:text-slate-300">
              <div>
                <h2 class="text-lg font-bold text-gray-900 dark:text-slate-100 mb-2">Opis oglasa</h2>
                <p class="leading-7 whitespace-pre-line">{{ ad.description }}</p>
              </div>

              <div v-if="ad.requirements">
                <h2 class="text-lg font-bold text-gray-900 dark:text-slate-100 mb-2">Uslovi</h2>
                <p class="leading-7 whitespace-pre-line">{{ ad.requirements }}</p>
              </div>

              <div v-if="ad.benefits">
                <h2 class="text-lg font-bold text-gray-900 dark:text-slate-100 mb-2">Benefiti</h2>
                <p class="leading-7 whitespace-pre-line">{{ ad.benefits }}</p>
              </div>
            </div>
          </section>

          <aside v-if="!isCompanyLoggedIn" class="rounded-3xl border border-gray-100 dark:border-slate-800 bg-white dark:bg-slate-800 shadow-sm p-6 sm:p-8">
            <template v-if="isUserLoggedIn && !isCompanyLoggedIn">
              <h2 class="text-lg font-bold text-gray-900 dark:text-slate-100 mb-4">Brzi pregled</h2>

              <div class="space-y-4 text-sm">
                <div>
                  <p class="text-gray-400 dark:text-slate-500 font-semibold mb-1">Oblast</p>
                  <p class="text-gray-900 dark:text-slate-200 font-medium">{{ ad.field || 'Nije navedeno' }}</p>
                </div>
                <div>
                  <p class="text-gray-400 dark:text-slate-500 font-semibold mb-1">Tagovi</p>
                  <div class="flex flex-wrap gap-2">
                    <span
                      v-for="tag in ad.tags"
                      :key="tag"
                      class="bg-gray-100 dark:bg-slate-700 text-gray-600 dark:text-slate-300 px-3 py-1 rounded-full text-xs font-semibold"
                    >
                      {{ tag }}
                    </span>
                  </div>
                </div>
                <div>
                  <p class="text-gray-400 dark:text-slate-500 font-semibold mb-1">Broj mjesta</p>
                  <p class="text-gray-900 dark:text-slate-200 font-medium">{{ ad.spots || 'Nije navedeno' }}</p>
                </div>
                <div>
                  <p class="text-gray-400 dark:text-slate-500 font-semibold mb-1">Rok prijave</p>
                  <p class="text-gray-900 dark:text-slate-200 font-medium">{{ ad.deadline || 'Nije navedeno' }}</p>
                </div>
              </div>

              <!-- Dugme otvara modal umjesto navigacije -->
              <button
                @click="openApplyModal"
                class="block w-full mt-6 bg-orange-600 text-white py-3 rounded-lg hover:bg-orange-700 transition font-semibold text-center text-sm"
              >
                Pošalji prijavu
              </button>
            </template>

            <template v-else-if="!isUserLoggedIn && !isCompanyLoggedIn">
              <h2 class="text-lg font-bold text-gray-900 dark:text-slate-100 mb-4">Zainteresovan?</h2>
              <div class="rounded-2xl bg-orange-50 dark:bg-orange-950/20 border border-orange-100 dark:border-orange-900/50 p-4 mb-4">
                <p class="text-sm font-semibold text-orange-900 dark:text-orange-400 mb-2">Prijavite se za ovu poziciju</p>
                <p class="text-sm text-orange-800 dark:text-slate-300 leading-6 mb-4">
                  Trebate biti prijavljeni da biste poslali prijavu za ovu poziciju.
                </p>
                <router-link
                  to="/login"
                  class="block bg-orange-600 text-white py-2 rounded-lg hover:bg-orange-700 transition font-semibold text-center text-sm no-underline"
                >
                  Prijavi se
                </router-link>
              </div>

              <h2 class="text-lg font-bold text-gray-900 dark:text-slate-100 mb-4 mt-6">Brzi pregled</h2>
              <div class="space-y-4 text-sm">
                <div>
                  <p class="text-gray-400 dark:text-slate-500 font-semibold mb-1">Oblast</p>
                  <p class="text-gray-900 dark:text-slate-200 font-medium">{{ ad.field || 'Nije navedeno' }}</p>
                </div>
                <div>
                  <p class="text-gray-400 dark:text-slate-500 font-semibold mb-1">Tagovi</p>
                  <div class="flex flex-wrap gap-2">
                    <span
                      v-for="tag in ad.tags"
                      :key="tag"
                      class="bg-gray-100 dark:bg-slate-700 text-gray-600 dark:text-slate-300 px-3 py-1 rounded-full text-xs font-semibold"
                    >
                      {{ tag }}
                    </span>
                  </div>
                </div>
                <div>
                  <p class="text-gray-400 dark:text-slate-500 font-semibold mb-1">Broj mjesta</p>
                  <p class="text-gray-900 dark:text-slate-200 font-medium">{{ ad.spots || 'Nije navedeno' }}</p>
                </div>
                <div>
                  <p class="text-gray-400 dark:text-slate-500 font-semibold mb-1">Rok prijave</p>
                  <p class="text-gray-900 dark:text-slate-200 font-medium">{{ ad.deadline || 'Nije navedeno' }}</p>
                </div>
              </div>
            </template>
          </aside>
        </div>

        <section v-if="isAdmin || isCompanyLoggedIn" class="rounded-3xl border border-gray-100 dark:border-slate-800 bg-white dark:bg-slate-800 shadow-sm p-6 sm:p-8 w-full">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-slate-100 mb-6">Prijave ({{ applications.length }}) · Broj mjesta: {{ ad.spots }}</h2>
          <div v-if="loadingApplications" class="text-center text-gray-500 dark:text-slate-400 py-8">
            Učitavanje prijava...
          </div>

          <div v-else-if="applicationsError" class="rounded-2xl border border-red-200 dark:border-red-900/50 bg-red-50 dark:bg-red-950/20 p-4 text-red-700 dark:text-red-400">
            {{ applicationsError }}
          </div>

          <div v-else-if="applications.length === 0" class="rounded-2xl border border-yellow-200 dark:border-yellow-900/50 bg-yellow-50 dark:bg-yellow-950/20 p-4 text-yellow-700 dark:text-yellow-400">
            <p class="text-sm font-medium">Nema prijava za ovaj oglas.</p>
          </div>

          <div v-else class="space-y-4">
            <ApplicationCard 
              v-for="app in applications" 
              :key="app.id" 
              :application="app" 
              :token="userToken"
              :is-company="isCompanyLoggedIn" 
              @updated="fetchApplications" 
            />
          </div>
        </section>

      </div>
    </div>

    <!-- Apply Modal -->
    <Teleport to="body">
      <div
        v-if="applyModalOpen"
        class="fixed inset-0 z-50 flex items-end sm:items-center justify-center"
        @click.self="closeApplyModal"
      >
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="closeApplyModal" />

        <!-- Modal panel -->
        <div class="relative z-10 w-full sm:max-w-lg bg-white dark:bg-slate-800 rounded-t-3xl sm:rounded-3xl shadow-2xl border border-gray-100 dark:border-slate-700 flex flex-col max-h-[92vh]">

          <!-- Modal header -->
          <div class="flex items-center justify-between px-6 py-5 border-b border-gray-100 dark:border-slate-700 shrink-0">
            <div>
              <p class="text-base font-bold text-gray-900 dark:text-slate-100">Pošalji prijavu</p>
              <p class="text-xs text-gray-400 dark:text-slate-500 mt-0.5">{{ ad?.title }}</p>
            </div>
            <button
              @click="closeApplyModal"
              class="flex items-center justify-center w-8 h-8 rounded-full hover:bg-gray-100 dark:hover:bg-slate-700 text-gray-400 dark:text-slate-500 hover:text-gray-700 dark:hover:text-slate-200 transition"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Modal body (scrollable) -->
          <div class="overflow-y-auto px-6 py-5 space-y-4 flex-1">

            <!-- Greška -->
            <div v-if="applyError" class="rounded-xl bg-red-50 dark:bg-red-950/30 border border-red-100 dark:border-red-900/50 p-3 text-sm text-red-700 dark:text-red-400">
              {{ applyError }}
            </div>

            <!-- Uspjeh -->
            <div v-if="applySuccess" class="rounded-xl bg-green-50 dark:bg-green-950/30 border border-green-100 dark:border-green-900/50 p-4 text-center">
              <p class="text-2xl mb-2">🎉</p>
              <p class="text-sm font-bold text-green-700 dark:text-green-400">Prijava je uspješno poslana!</p>
              <p class="text-xs text-green-600 dark:text-green-500 mt-1">Pratite status prijave u svom profilu.</p>
              <button
                @click="closeApplyModal"
                class="mt-4 bg-green-600 hover:bg-green-700 text-white text-sm font-bold py-2 px-6 rounded-xl transition"
              >
                Zatvori
              </button>
            </div>

            <template v-if="!applySuccess">
              <!-- Telefon -->
              <div>
                <label class="block text-xs font-semibold text-gray-500 dark:text-slate-400 mb-1.5">
                  Broj telefona <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="applyForm.phone"
                  type="tel"
                  placeholder="+387 61 123 456"
                  class="w-full rounded-xl border border-gray-200 dark:border-slate-600 bg-gray-50 dark:bg-slate-700/50 px-3 py-2.5 text-sm text-gray-800 dark:text-slate-100 placeholder-gray-400 dark:placeholder-slate-500 focus:outline-none focus:border-orange-300 dark:focus:border-orange-500 focus:ring-2 focus:ring-orange-100 dark:focus:ring-orange-950/50 transition"
                />
              </div>

              <!-- LinkedIn -->
              <div>
                <label class="block text-xs font-semibold text-gray-500 dark:text-slate-400 mb-1.5">
                  LinkedIn profil <span class="text-gray-400 dark:text-slate-500 font-normal">(opciono)</span>
                </label>
                <input
                  v-model="applyForm.linkedin_url"
                  type="url"
                  placeholder="https://linkedin.com/in/username"
                  class="w-full rounded-xl border border-gray-200 dark:border-slate-600 bg-gray-50 dark:bg-slate-700/50 px-3 py-2.5 text-sm text-gray-800 dark:text-slate-100 placeholder-gray-400 dark:placeholder-slate-500 focus:outline-none focus:border-orange-300 dark:focus:border-orange-500 focus:ring-2 focus:ring-orange-100 dark:focus:ring-orange-950/50 transition"
                />
              </div>

              <!-- GitHub -->
              <div>
                <label class="block text-xs font-semibold text-gray-500 dark:text-slate-400 mb-1.5">
                  GitHub profil <span class="text-gray-400 dark:text-slate-500 font-normal">(opciono)</span>
                </label>
                <input
                  v-model="applyForm.github_url"
                  type="url"
                  placeholder="https://github.com/username"
                  class="w-full rounded-xl border border-gray-200 dark:border-slate-600 bg-gray-50 dark:bg-slate-700/50 px-3 py-2.5 text-sm text-gray-800 dark:text-slate-100 placeholder-gray-400 dark:placeholder-slate-500 focus:outline-none focus:border-orange-300 dark:focus:border-orange-500 focus:ring-2 focus:ring-orange-100 dark:focus:ring-orange-950/50 transition"
                />
              </div>

              <!-- CV upload -->
              <div>
                <label class="block text-xs font-semibold text-gray-500 dark:text-slate-400 mb-1.5">
                  CV <span class="text-red-500">*</span>
                  <span class="text-gray-400 dark:text-slate-500 font-normal ml-1">(.pdf, max 5MB)</span>
                </label>
                <div
                  class="relative rounded-xl border-2 border-dashed border-gray-200 dark:border-slate-600 bg-gray-50 dark:bg-slate-700/30 hover:border-orange-300 dark:hover:border-orange-600 transition-colors cursor-pointer"
                  @click="$refs.cvInput.click()"
                >
                  <input
                    ref="cvInput"
                    type="file"
                    accept=".pdf"
                    class="hidden"
                    @change="handleCvUpload"
                  />
                  <div class="flex items-center gap-3 px-4 py-3">
                    <span class="text-xl">📄</span>
                    <div class="flex-1 min-w-0">
                      <p v-if="applyForm.cv_path" class="text-sm font-semibold text-green-600 dark:text-green-400 truncate">
                        ✓ {{ cvFileName }}
                      </p>
                      <p v-else class="text-sm text-gray-400 dark:text-slate-500">Klikni za upload CV-a</p>
                    </div>
                    <span v-if="cvUploading" class="text-xs text-gray-400 dark:text-slate-500 shrink-0">Uploading...</span>
                  </div>
                </div>
              </div>

              <!-- Motivaciono pismo upload -->
              <div>
                <label class="block text-xs font-semibold text-gray-500 dark:text-slate-400 mb-1.5">
                  Propratno pismo <span class="text-red-500">*</span>
                  <span class="text-gray-400 dark:text-slate-500 font-normal ml-1">(.pdf, max 5MB)</span>
                </label>
                <div
                  class="relative rounded-xl border-2 border-dashed border-gray-200 dark:border-slate-600 bg-gray-50 dark:bg-slate-700/30 hover:border-orange-300 dark:hover:border-orange-600 transition-colors cursor-pointer"
                  @click="$refs.letterInput.click()"
                >
                  <input
                    ref="letterInput"
                    type="file"
                    accept=".pdf"
                    class="hidden"
                    @change="handleLetterUpload"
                  />
                  <div class="flex items-center gap-3 px-4 py-3">
                    <span class="text-xl">✉️</span>
                    <div class="flex-1 min-w-0">
                      <p v-if="applyForm.motivational_letter_path" class="text-sm font-semibold text-green-600 dark:text-green-400 truncate">
                        ✓ {{ letterFileName }}
                      </p>
                      <p v-else class="text-sm text-gray-400 dark:text-slate-500">Klikni za upload propratnog pisma</p>
                    </div>
                    <span v-if="letterUploading" class="text-xs text-gray-400 dark:text-slate-500 shrink-0">Uploading...</span>
                  </div>
                </div>
              </div>
            </template>
          </div>

          <!-- Modal footer -->
          <div v-if="!applySuccess" class="px-6 py-4 border-t border-gray-100 dark:border-slate-700 shrink-0">
            <button
              @click="submitApplication"
              :disabled="applyLoading || cvUploading || letterUploading"
              class="w-full bg-orange-600 hover:bg-orange-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-3 rounded-xl text-sm transition"
            >
              <span v-if="applyLoading">Slanje...</span>
              <span v-else>Pošalji prijavu</span>
            </button>
          </div>

        </div>
      </div>
    </Teleport>
  </div>
</template>

<script>
import { getAdById, getApprovedCompanies, getApplicationsByAd, getBookmarks, addBookmark, removeBookmark } from '../../services/api.js'
import ApplicationCard from '../../components/application/ApplicationCard.vue'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
const BASE_BADGE = 'px-3 py-1.5 rounded-full'

function formatType(type) {
  const map = { internship: 'Praksa', education: 'Edukacija', scholarship: 'Stipendija' }
  return map[type] || 'Prilika'
}

function formatStatus(status) {
  const map = {
    active: 'Aktivan', pending: 'Na čekanju', expired: 'Istekao',
    rejected: 'Odbijen', changes_requested: 'Potrebne izmjene'
  }
  return map[status] || 'Aktivan'
}

function formatCompensation(value, currency) {
  if (value === null || value === undefined) return ''
  return `${value} ${currency || 'BAM'}`
}

export default {
  name: 'AdDetailView',
  components: { ApplicationCard },
  data() {
    return {
      loading: false,
      errorMessage: '',
      ad: null,
      isUserLoggedIn: false,
      isCompanyLoggedIn: false,
      userRole: null,
      applications: [],
      loadingApplications: false,
      applicationsError: '',
      companyToken: localStorage.getItem('company_token'),
      bookmarkId: null,
      // Apply modal
      applyModalOpen: false,
      applyLoading: false,
      applyError: '',
      applySuccess: false,
      cvUploading: false,
      letterUploading: false,
      cvFileName: '',
      letterFileName: '',
      applyForm: {
        phone: '',
        linkedin_url: '',
        github_url: '',
        cv_path: '',
        motivational_letter_path: ''
      }
    }
  },
  computed: {
    isAdmin() {
      return this.isUserLoggedIn && this.userRole === 'admin'
    },
    userToken() {
      return this.isCompanyLoggedIn ? this.companyToken : localStorage.getItem('token')
    }
  },
  methods: {
    getTypeClass(typeLabel) {
      if (typeLabel === 'Praksa') return `bg-blue-50 dark:bg-blue-950/40 text-blue-600 dark:text-blue-400 ${BASE_BADGE}`
      if (typeLabel === 'Edukacija') return `bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400 ${BASE_BADGE}`
      return `bg-amber-50 dark:bg-amber-950/40 text-amber-600 dark:text-amber-400 ${BASE_BADGE}`
    },
    getStatusClass(statusLabel) {
      if (statusLabel === 'Aktivan') return `bg-green-50 dark:bg-green-950/40 text-green-600 dark:text-green-400 ${BASE_BADGE}`
      if (statusLabel === 'Istekao') return `bg-orange-50 dark:bg-orange-950/40 text-orange-600 dark:text-orange-400 ${BASE_BADGE}`
      return `bg-red-50 dark:bg-red-950/40 text-red-600 dark:text-red-400 ${BASE_BADGE}`
    },

    openApplyModal() {
      this.applyForm = { phone: '', linkedin_url: '', github_url: '', cv_path: '', motivational_letter_path: '' }
      this.applyError = ''
      this.applySuccess = false
      this.cvFileName = ''
      this.letterFileName = ''
      this.applyModalOpen = true
      document.body.style.overflow = 'hidden'
    },
    closeApplyModal() {
      this.applyModalOpen = false
      document.body.style.overflow = ''
    },

    async handleCvUpload(event) {
      const file = event.target.files[0]
      if (!file) return
      this.cvUploading = true
      this.applyError = ''
      try {
        const formData = new FormData()
        formData.append('file', file)
        const token = localStorage.getItem('token')
        const res = await fetch(`${BASE_URL}/applications/upload-cv`, {
          method: 'POST',
          headers: { Authorization: `Bearer ${token}` },
          body: formData
        })
        if (!res.ok) {
          const err = await res.json()
          throw new Error(err.detail || 'Greška pri uploadu CV-a.')
        }
        const data = await res.json()
        this.applyForm.cv_path = data.path
        this.cvFileName = file.name
      } catch (err) {
        this.applyError = err.message
      } finally {
        this.cvUploading = false
      }
    },

    async handleLetterUpload(event) {
      const file = event.target.files[0]
      if (!file) return
      this.letterUploading = true
      this.applyError = ''
      try {
        const formData = new FormData()
        formData.append('file', file)
        const token = localStorage.getItem('token')
        const res = await fetch(`${BASE_URL}/applications/upload-cv`, {
          method: 'POST',
          headers: { Authorization: `Bearer ${token}` },
          body: formData
        })
        if (!res.ok) {
          const err = await res.json()
          throw new Error(err.detail || 'Greška pri uploadu propratnog pisma.')
        }
        const data = await res.json()
        this.applyForm.motivational_letter_path = data.path
        this.letterFileName = file.name
      } catch (err) {
        this.applyError = err.message
      } finally {
        this.letterUploading = false
      }
    },

    async submitApplication() {
      this.applyError = ''

      if (!this.applyForm.phone.trim()) {
        this.applyError = 'Broj telefona je obavezan.'
        return
      }
      if (!this.applyForm.cv_path) {
        this.applyError = 'CV je obavezan.'
        return
      }
      if (!this.applyForm.motivational_letter_path) {
        this.applyError = 'Propratno pismo je obavezno.'
        return
      }

      this.applyLoading = true
      try {
        const token = localStorage.getItem('token')
        const payload = {
          ad_id: this.ad.id,
          phone: this.applyForm.phone.trim(),
          cv_path: this.applyForm.cv_path,
          motivational_letter_path: this.applyForm.motivational_letter_path,
          linkedin_url: this.applyForm.linkedin_url.trim() || null,
          github_url: this.applyForm.github_url.trim() || null,
        }

        const res = await fetch(`${BASE_URL}/applications/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify(payload)
        })

        if (!res.ok) {
          const err = await res.json()
          throw new Error(err.detail || 'Greška pri slanju prijave.')
        }

        this.applySuccess = true
      } catch (err) {
        this.applyError = err.message
      } finally {
        this.applyLoading = false
      }
    },

    async fetchAd() {
      this.loading = true
      this.errorMessage = ''
      const adId = Number(this.$route.params.id)
      let found, companies
      try {
        [found, companies] = await Promise.all([getAdById(adId), getApprovedCompanies()])
      } catch (err) {
        this.errorMessage = 'Ne mogu učitati detalje oglasa. Provjeri da li je API pokrenut.'
        this.loading = false
        return
      }
      if (!found) {
        this.errorMessage = 'Oglas nije pronađen.'
        this.loading = false
        return
      }
      const companiesById = new Map((companies || []).map(c => [c.id, c.company_name]))
      this.ad = {
        id: found.id,
        title: found.title,
        company: companiesById.get(found.company_id) || `Kompanija #${found.company_id}`,
        company_id: found.company_id,
        description: found.description,
        tags: [found.field, found.location].filter(Boolean),
        typeLabel: formatType(found.type),
        compensation: found.compensation_negotiable ? 'Po dogovoru' : formatCompensation(found.compensation, found.currency),
        statusLabel: formatStatus(found.status),
        location: found.location,
        duration: found.duration_months ? `${found.duration_months} mjeseci` : null,
        field: found.field,
        requirements: found.requirements,
        benefits: found.benefits,
        spots: found.spots,
        deadline: found.deadline
      }
      this.loading = false
    },

    async fetchApplications() {
      const adId = Number(this.$route.params.id)
      if (!this.isAdmin && !this.isCompanyLoggedIn) return
      const token = this.isCompanyLoggedIn ? localStorage.getItem('company_token') : localStorage.getItem('token')
      if (!token || token === 'null' || token === 'undefined') return
      this.loadingApplications = true
      this.applicationsError = ''
      try {
        const apps = await getApplicationsByAd(adId, token, this.isCompanyLoggedIn)
        this.applications = apps || []
      } catch (err) {
        this.applicationsError = 'Ne mogu učitati prijave.'
      } finally {
        this.loadingApplications = false
      }
    },

    async checkBookmarkStatus() {
      if (!this.isUserLoggedIn || this.isCompanyLoggedIn || this.isAdmin) return
      const token = localStorage.getItem('token')
      if (!token || token === 'null' || token === 'undefined') return
      const adId = Number(this.$route.params.id)
      try {
        const bookmarks = await getBookmarks(token)
        const found = bookmarks.find(bm => bm.ad_id === adId)
        this.bookmarkId = found ? found.id : null
      } catch (err) {
        console.error('Nisam uspio provjeriti status bookmarka:', err)
      }
    },

    async toggleBookmark() {
      const token = localStorage.getItem('token')
      if (!token || token === 'null' || token === 'undefined') {
        alert('Morate biti prijavljeni da biste sačuvali oglas.')
        return
      }
      const adId = Number(this.$route.params.id)
      try {
        if (this.bookmarkId) {
          await removeBookmark(this.bookmarkId, token)
          this.bookmarkId = null
        } else {
          const nb = await addBookmark(adId, token)
          this.bookmarkId = nb.id
        }
      } catch (err) {
        alert('Došlo je do greške pri čuvanju oglasa. Molimo pokušajte ponovo.')
      }
    }
  },

  async mounted() {
    this.isUserLoggedIn = !!localStorage.getItem('token')
    this.isCompanyLoggedIn = !!localStorage.getItem('company_token')
    this.userRole = localStorage.getItem('role')
    await this.fetchAd()
    await this.fetchApplications()
    await this.checkBookmarkStatus()
  },

  beforeUnmount() {
    document.body.style.overflow = ''
  }
}
</script>