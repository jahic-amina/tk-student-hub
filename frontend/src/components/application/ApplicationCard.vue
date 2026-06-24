<template>
  <div
    class="rounded-2xl border bg-white dark:bg-slate-800 p-5 shadow-sm transition-all duration-200 border-gray-100 dark:border-slate-700"
    :class="cardBorderClass"
  >
    <!-- Header -->
    <div class="flex items-start justify-between mb-4">
      <div>
        <p class="text-sm font-bold text-gray-900 dark:text-slate-100">Aplikant #{{ application.user_id }}</p>
        <p v-if="application.created_at" class="text-xs text-gray-400 dark:text-slate-500 mt-0.5">
          {{ formatDate(application.created_at) }}
        </p>
      </div>
      <span class="text-xs font-semibold px-3 py-1.5 rounded-full" :class="statusBadgeClass">
        {{ statusLabel }}
      </span>
    </div>

    <!-- Info -->
    <div class="space-y-2 mb-5">
      <div v-if="application.phone" class="flex items-center gap-2 text-sm">
        <span class="text-gray-400">📞</span>
        <span class="text-gray-700 dark:text-slate-300 font-medium">{{ application.phone }}</span>
      </div>
      <div v-if="application.linkedin_url" class="flex items-center gap-2 text-sm">
        <span class="text-gray-400">🔗</span>
        <a
          :href="application.linkedin_url"
          target="_blank"
          rel="noopener"
          class="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-medium hover:underline truncate max-w-[200px]"
        >
          LinkedIn profil
        </a>
      </div>
      <div v-if="application.github_url" class="flex items-center gap-2 text-sm">
        <span class="text-gray-400">🐙</span>
        <a
          :href="application.github_url"
          target="_blank"
          rel="noopener"
          class="text-gray-700 dark:text-slate-300 hover:text-gray-900 dark:hover:text-slate-100 font-medium hover:underline truncate max-w-[200px]"
        >
          GitHub profil
        </a>
      </div>
      <div v-if="application.cv_path" class="flex items-center gap-2 text-sm">
        <span class="text-gray-400">📄</span>
        <button
          @click="openPdf(cvUrl, 'CV')"
          class="text-orange-600 dark:text-orange-400 hover:text-orange-700 dark:hover:text-orange-300 font-semibold hover:underline"
        >
          Preuzmi CV
        </button>
      </div>
      <div v-if="application.motivational_letter_path" class="flex items-center gap-2 text-sm">
        <span class="text-gray-400">✉️</span>
        <button
          @click="openPdf(motivationalLetterUrl, 'Propratno pismo')"
          class="text-orange-600 dark:text-orange-400 hover:text-orange-700 dark:hover:text-orange-300 font-semibold hover:underline"
        >
          Propratno pismo
        </button>
      </div>
    </div>

    <!-- Rating -->
    <div class="mb-5">
      <p class="text-xs font-semibold text-gray-500 dark:text-slate-400 mb-1.5">Ocjena kandidata</p>
      <div class="flex items-center gap-1">
        <button
          v-for="star in 5"
          :key="star"
          @click="handleRating(star)"
          @mouseenter="hoveredRating = star"
          @mouseleave="hoveredRating = 0"
          :disabled="ratingLoading"
          class="text-2xl transition-transform duration-100 hover:scale-110 disabled:opacity-50 disabled:cursor-not-allowed leading-none"
          :title="`Ocijeni sa ${star}`"
        >
          <span :class="star <= (hoveredRating || currentRating) ? 'text-amber-400' : 'text-gray-200 dark:text-slate-600'">
            ★
          </span>
        </button>
        <button
          v-if="currentRating"
          @click="handleRating(null)"
          :disabled="ratingLoading"
          class="ml-2 text-xs text-gray-400 dark:text-slate-500 hover:text-red-400 dark:hover:text-red-400 transition disabled:opacity-50"
          title="Ukloni ocjenu"
        >
          ✕
        </button>
        <span v-if="ratingLoading" class="ml-2 text-xs text-gray-400 dark:text-slate-500">Čuvanje...</span>
      </div>
    </div>

    <!-- Existing admin feedback -->
    <div
      v-if="application.admin_feedback && application.status === 'rejected'"
      class="mb-4 rounded-xl bg-red-50 dark:bg-red-950/30 border border-red-100 dark:border-red-900/50 p-3 text-xs text-red-700 dark:text-red-400"
    >
      <span class="font-semibold block mb-1">Povratna informacija:</span>
      {{ application.admin_feedback }}
    </div>

    <!-- Reject feedback textarea -->
    <div v-if="showRejectForm" class="mb-4">
      <textarea
        v-model="feedback"
        placeholder="Povratna informacija za kandidata (opciono)..."
        rows="3"
        class="w-full rounded-xl border border-gray-200 dark:border-slate-600 bg-gray-50 dark:bg-slate-700/50 px-3 py-2 text-sm text-gray-800 dark:text-slate-100 resize-none focus:outline-none focus:border-orange-300 dark:focus:border-orange-500 focus:ring-2 focus:ring-orange-100 dark:focus:ring-orange-950/50 transition"
      />
    </div>

    <!-- Actions -->
    <div v-if="application.status === 'pending'" class="space-y-2">
      <div class="flex gap-2">
        <button
          @click="handleAccept"
          :disabled="loading"
          class="flex-1 bg-green-50 dark:bg-green-950/40 hover:bg-green-100 dark:hover:bg-green-900/40 disabled:opacity-50 text-green-700 dark:text-green-400 font-bold py-2.5 rounded-xl text-sm transition"
        >
          <span v-if="loading && accepting">...</span>
          <span v-else>✓ Prihvati</span>
        </button>
        <button
          @click="toggleRejectForm"
          :disabled="loading"
          class="flex-1 font-bold py-2.5 rounded-xl text-sm transition disabled:opacity-50"
          :class="showRejectForm
            ? 'bg-gray-100 dark:bg-slate-700 text-gray-600 dark:text-slate-300 hover:bg-gray-200 dark:hover:bg-slate-600'
            : 'bg-red-50 dark:bg-red-950/40 text-red-600 dark:text-red-400 hover:bg-red-100 dark:hover:bg-red-900/40'"
        >
          {{ showRejectForm ? '✕ Odustani' : '✗ Odbij' }}
        </button>
      </div>
      <button
        v-if="showRejectForm"
        @click="handleReject"
        :disabled="loading"
        class="w-full bg-red-500 hover:bg-red-600 disabled:opacity-50 text-white font-bold py-2.5 rounded-xl text-sm transition"
      >
        <span v-if="loading && !accepting">Slanje...</span>
        <span v-else>Potvrdi odbijanje</span>
      </button>
    </div>

    <div v-else class="text-xs text-gray-400 dark:text-slate-500 text-center pt-1">
      Odluka je već donesena za ovu prijavu.
    </div>

    <!-- PDF Modal -->
    <Teleport to="body">
      <div
        v-if="pdfModal.open"
        class="fixed inset-0 z-50 flex items-center justify-center"
        @click.self="closePdf"
      >
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="closePdf" />
        <div class="relative z-10 flex flex-col bg-white dark:bg-slate-800 rounded-2xl shadow-2xl w-[90vw] max-w-4xl h-[90vh] border border-transparent dark:border-slate-700">
          <div class="flex items-center justify-between px-5 py-4 border-b border-gray-100 dark:border-slate-700 shrink-0">
            <p class="font-bold text-gray-900 dark:text-slate-100 text-sm">{{ pdfModal.title }}</p>
            <div class="flex items-center gap-3">
              <a
                :href="pdfModal.url"
                target="_blank"
                rel="noopener"
                class="text-xs font-semibold text-orange-600 dark:text-orange-400 hover:text-orange-700 dark:hover:text-orange-300 transition"
              >
                Otvori u novom tabu ↗
              </a>
              <button
                @click="closePdf"
                class="flex items-center justify-center w-8 h-8 rounded-full hover:bg-gray-100 dark:hover:bg-slate-700 text-gray-500 dark:text-slate-400 hover:text-gray-800 dark:hover:text-slate-200 transition"
                title="Zatvori"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
          <iframe
            :src="pdfModal.url"
            class="flex-1 w-full rounded-b-2xl bg-white dark:bg-slate-100"
            frameborder="0"
          />
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script>
import { updateApplicationStatus } from '../../services/api.js'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export default {
  name: 'ApplicationCard',
  props: {
    application: { type: Object, required: true },
    token: { type: String, required: true },
    isCompany: { type: Boolean, default: true }
  },
  emits: ['updated'],
  data() {
    return {
      loading: false,
      accepting: false,
      showRejectForm: false,
      feedback: '',
      // Rating
      currentRating: this.application.rating || null,
      hoveredRating: 0,
      ratingLoading: false,
      pdfModal: {
        open: false,
        url: '',
        title: ''
      }
    }
  },
  computed: {
    cvUrl() {
      return `${BASE_URL}/${this.application.cv_path}`
    },
    motivationalLetterUrl() {
      return `${BASE_URL}/${this.application.motivational_letter_path}`
    },
    statusLabel() {
      const map = {
        pending: 'Na čekanju',
        accepted: 'Prihvaćen',
        rejected: 'Odbijen',
        under_review: 'U pregledu'
      }
      return map[this.application.status] || this.application.status
    },
    statusBadgeClass() {
      const map = {
        pending: 'bg-amber-50 text-amber-600 dark:bg-amber-950/40 dark:text-amber-400',
        accepted: 'bg-green-50 text-green-600 dark:bg-green-950/40 dark:text-green-400',
        rejected: 'bg-red-50 text-red-600 dark:bg-red-950/40 dark:text-red-400',
        under_review: 'bg-blue-50 text-blue-600 dark:bg-blue-950/40 dark:text-blue-400'
      }
      return map[this.application.status] || 'bg-gray-100 text-gray-600 dark:bg-slate-700 dark:text-slate-300'
    },
    cardBorderClass() {
      const map = {
        accepted: 'border-green-200 dark:border-green-900/60',
        rejected: 'border-red-100 dark:border-red-900/40',
        pending: 'border-gray-100 dark:border-slate-700',
        under_review: 'border-blue-100 dark:border-blue-900/40'
      }
      return map[this.application.status] || 'border-gray-100 dark:border-slate-700'
    }
  },
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return ''
      return new Date(dateStr).toLocaleDateString('bs-BA', {
        day: '2-digit', month: '2-digit', year: 'numeric'
      })
    },
    openPdf(url, title) {
      this.pdfModal = { open: true, url, title }
      document.body.style.overflow = 'hidden'
    },
    closePdf() {
      this.pdfModal = { open: false, url: '', title: '' }
      document.body.style.overflow = ''
    },
    toggleRejectForm() {
      this.showRejectForm = !this.showRejectForm
      if (!this.showRejectForm) this.feedback = ''
    },
    async handleRating(value) {
      // Klik na istu zvjezdicu uklanja ocjenu
      if (value === this.currentRating) value = null

      this.ratingLoading = true
      try {
        const endpoint = this.isCompany
          ? `${BASE_URL}/applications/company/${this.application.id}`
          : `${BASE_URL}/applications/${this.application.id}`

        const res = await fetch(endpoint, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${this.token}`
          },
          body: JSON.stringify({ rating: value })
        })

        if (!res.ok) throw new Error('Greška pri čuvanju ocjene.')

        const updated = await res.json()
        this.currentRating = updated.rating
        this.$emit('updated', this.application.id, updated.status, updated)
      } catch (err) {
        console.error('Rating error:', err)
        alert('Greška pri čuvanju ocjene. Pokušaj ponovo.')
      } finally {
        this.ratingLoading = false
      }
    },
    async handleAccept() {
      this.loading = true
      this.accepting = true
      try {
        await updateApplicationStatus(this.application.id, 'accepted', null, this.token, this.isCompany)
        this.$emit('updated', this.application.id, 'accepted')
      } catch (err) {
        console.error('Failed to accept application:', err)
        alert('Greška pri prihvatanju prijave. Pokušaj ponovo.')
      } finally {
        this.loading = false
        this.accepting = false
      }
    },
    async handleReject() {
      this.loading = true
      this.accepting = false
      try {
        await updateApplicationStatus(
          this.application.id, 'rejected',
          this.feedback || null, this.token, this.isCompany
        )
        this.$emit('updated', this.application.id, 'rejected')
        this.showRejectForm = false
        this.feedback = ''
      } catch (err) {
        console.error('Failed to reject application:', err)
        alert('Greška pri odbijanju prijave. Pokušaj ponovo.')
      } finally {
        this.loading = false
      }
    }
  },
  beforeUnmount() {
    document.body.style.overflow = ''
  }
}
</script>