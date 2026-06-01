<template>
  <div
    class="rounded-2xl border bg-white p-5 shadow-sm transition-all duration-200"
    :class="cardBorderClass"
  >
    <!-- Header -->
    <div class="flex items-start justify-between mb-4">
      <div>
        <p class="text-sm font-bold text-gray-900">Aplikant #{{ application.user_id }}</p>
        <p v-if="application.created_at" class="text-xs text-gray-400 mt-0.5">
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
        <span class="text-gray-700 font-medium">{{ application.phone }}</span>
      </div>
      <div v-if="application.linkedin_url" class="flex items-center gap-2 text-sm">
        <span class="text-gray-400">🔗</span>
        <a
          :href="application.linkedin_url"
          target="_blank"
          rel="noopener"
          class="text-blue-600 hover:text-blue-700 font-medium hover:underline truncate max-w-[200px]"
        >
          LinkedIn profil
        </a>
      </div>
      <div v-if="application.cv_path" class="flex items-center gap-2 text-sm">
        <span class="text-gray-400">📄</span>
        <a
          :href="cvUrl"
          target="_blank"
          rel="noopener"
          class="text-orange-600 hover:text-orange-700 font-semibold hover:underline"
        >
          Preuzmi CV
        </a>
      </div>
      <div v-if="application.motivational_letter_path" class="flex items-center gap-2 text-sm">
        <span class="text-gray-400">✉️</span>
        <a
          :href="motivationalLetterUrl"
          target="_blank"
          rel="noopener"
          class="text-orange-600 hover:text-orange-700 font-semibold hover:underline"
        >
          Propratno pismo
        </a>
      </div>
    </div>

    <!-- Existing admin feedback (if rejected with message) -->
    <div
      v-if="application.admin_feedback && application.status === 'rejected'"
      class="mb-4 rounded-xl bg-red-50 border border-red-100 p-3 text-xs text-red-700"
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
        class="w-full rounded-xl border border-gray-200 bg-gray-50 px-3 py-2 text-sm text-gray-800 resize-none focus:outline-none focus:border-orange-300 focus:ring-2 focus:ring-orange-100 transition"
      />
    </div>

    <!-- Actions — shown only when pending -->
    <div v-if="application.status === 'pending'" class="space-y-2">
      <div class="flex gap-2">
        <button
          @click="handleAccept"
          :disabled="loading"
          class="flex-1 bg-green-50 hover:bg-green-100 disabled:opacity-50 text-green-700 font-bold py-2.5 rounded-xl text-sm transition"
        >
          <span v-if="loading && accepting">...</span>
          <span v-else>✓ Prihvati</span>
        </button>
        <button
          @click="toggleRejectForm"
          :disabled="loading"
          class="flex-1 font-bold py-2.5 rounded-xl text-sm transition disabled:opacity-50"
          :class="showRejectForm
            ? 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            : 'bg-red-50 text-red-600 hover:bg-red-100'"
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

    <!-- Already decided -->
    <div v-else class="text-xs text-gray-400 text-center pt-1">
      Odluka je već donesena za ovu prijavu.
    </div>
  </div>
</template>

<script>
import { updateApplicationStatus } from '../../services/api.js'

const BASE_URL = 'http://127.0.0.1:8000'

export default {
  name: 'ApplicationCard',
  props: {
    application: {
      type: Object,
      required: true
    },
    token: {
      type: String,
      required: true
    }
  },
  emits: ['updated'],
  data() {
    return {
      loading: false,
      accepting: false,
      showRejectForm: false,
      feedback: ''
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
        pending: 'bg-amber-50 text-amber-600',
        accepted: 'bg-green-50 text-green-600',
        rejected: 'bg-red-50 text-red-600',
        under_review: 'bg-blue-50 text-blue-600'
      }
      return map[this.application.status] || 'bg-gray-100 text-gray-600'
    },
    cardBorderClass() {
      const map = {
        accepted: 'border-green-200',
        rejected: 'border-red-100',
        pending: 'border-gray-100',
        under_review: 'border-blue-100'
      }
      return map[this.application.status] || 'border-gray-100'
    }
  },
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return ''
      return new Date(dateStr).toLocaleDateString('bs-BA', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      })
    },
    toggleRejectForm() {
      this.showRejectForm = !this.showRejectForm
      if (!this.showRejectForm) this.feedback = ''
    },
    async handleAccept() {
      this.loading = true
      this.accepting = true
      try {
        await updateApplicationStatus(this.application.id, 'accepted', null, this.token, true)
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
          this.application.id,
          'rejected',
          this.feedback || null,
          this.token,
          true
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
  }
}
</script>