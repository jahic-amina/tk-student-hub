<template>
  <div class="rounded-2xl border border-gray-200 bg-white p-4 hover:shadow-md transition">
    <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3">
      <div class="flex-1">
        <h3 class="text-sm font-bold text-gray-900">
          {{ application.user?.full_name || 'Nepoznat korisnik' }}
        </h3>
        <p class="text-xs text-gray-500 mt-1">
          {{ formatDate(application.created_at) }}
        </p>

        <div class="flex flex-wrap gap-2 mt-3">
          <span :class="getStatusClass(application.status)">
            {{ formatStatus(application.status) }}
          </span>
        </div>
      </div>

      <div class="flex gap-2">
        <a
          v-if="application.cv_path"
          :href="getCVUrl(application.cv_path)"
          target="_blank"
          class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-blue-50 text-blue-600 hover:bg-blue-100 transition"
        >
          CV
        </a>
        <a
          v-if="application.motivational_letter_path"
          :href="getLetterUrl(application.motivational_letter_path)"
          target="_blank"
          class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-purple-50 text-purple-600 hover:bg-purple-100 transition"
        >
          Pismo
        </a>
      </div>
    </div>

    <div class="grid sm:grid-cols-3 gap-3 mt-4 text-sm">
      <div>
        <p class="text-xs text-gray-500 font-semibold">Telefonski broj</p>
        <p class="text-gray-900 font-medium">{{ application.phone }}</p>
      </div>
      <div>
        <p class="text-xs text-gray-500 font-semibold">LinkedIn</p>
        <a
          v-if="application.linkedin_url"
          :href="application.linkedin_url"
          target="_blank"
          class="text-orange-600 hover:text-orange-700 font-medium underline"
        >
          Profil
        </a>
        <p v-else class="text-gray-500">-</p>
      </div>
      <div>
        <p class="text-xs text-gray-500 font-semibold">Poslana</p>
        <p class="text-gray-900 font-medium">{{ formatShortDate(application.created_at) }}</p>
      </div>
    </div>

    <div v-if="application.admin_feedback" class="mt-4 rounded-lg bg-yellow-50 border border-yellow-200 p-3">
      <p class="text-xs font-semibold text-yellow-900 mb-1">Povratna informacija:</p>
      <p class="text-sm text-yellow-800">{{ application.admin_feedback }}</p>
    </div>

    <div v-if="canManage" class="mt-4 pt-4 border-t border-gray-100">
      <div class="mb-3">
        <label class="block text-xs font-semibold text-gray-500 mb-1">
          Povratna informacija / Napomena studentu (opcionalno)
        </label>
        <textarea
          v-model="feedback"
          rows="2"
          class="w-full text-sm rounded-xl border-gray-200 shadow-sm focus:border-orange-500 focus:ring-orange-500 p-2 border"
          placeholder="Napišite obrazloženje ili poruku..."
        ></textarea>
      </div>
      
      <div class="flex justify-end gap-2">
        <button
          @click="handleStatusUpdate('rejected')"
          :disabled="isSubmitting"
          class="px-4 py-2 text-xs font-bold rounded-xl bg-red-50 text-red-600 hover:bg-red-100 transition disabled:opacity-50"
        >
          Odbij prijavu
        </button>
        <button
          @click="handleStatusUpdate('accepted')"
          :disabled="isSubmitting"
          class="px-4 py-2 text-xs font-bold rounded-xl bg-green-600 text-white hover:bg-green-700 transition disabled:opacity-50"
        >
          Prihvati prijavu
        </button>
      </div>
      <p v-if="actionError" class="text-xs text-red-600 mt-2 text-right">{{ actionError }}</p>
    </div>
  </div>
</template>

<script>
import { updateApplicationStatus } from '../../services/api.js'

export default {
  name: 'ApplicationCard',
  props: {
    application: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      feedback: '',
      isSubmitting: false,
      actionError: '',
      isAdmin: false,
      isCompany: false
    }
  },
  computed: {
    canManage() {
      // Pravo na upravljanje imaju samo admini/kompanije i to samo za 'pending' prijave
      return (this.isAdmin || this.isCompany) && this.application.status === 'pending'
    }
  },
  mounted() {
    // Provjera uloga iz lokalne memorije pri učitavanju komponente
    this.isAdmin = !!localStorage.getItem('token') && localStorage.getItem('role') === 'admin'
    this.isCompany = !!localStorage.getItem('company_token')
  },
  methods: {
    async handleStatusUpdate(newStatus) {
      this.isSubmitting = true
      this.actionError = ''
      
      const token = localStorage.getItem('token') || localStorage.getItem('company_token')
      
      try {
        await updateApplicationStatus(
          this.application.id,
          newStatus,
          this.feedback || null,
          token,
          this.isCompany
        )
        // Obavještavamo roditeljsku komponentu (AdView) da osvježi listu prijava
        this.$emit('status-updated')
      } catch (err) {
        console.error(err)
        this.actionError = 'Greška prilikom ažuriranja statusa prijave.'
      } finally {
        this.isSubmitting = false
      }
    },
    formatStatus(status) {
      const map = {
        pending: 'Na čekanju',
        accepted: 'Prihvaćena',
        rejected: 'Odbijena'
      }
      return map[status] || status
    },
    getStatusClass(status) {
      const baseClass = 'px-2.5 py-1.5 rounded-full text-xs font-semibold'
      if (status === 'pending') return `${baseClass} bg-yellow-50 text-yellow-700`
      if (status === 'accepted') return `${baseClass} bg-green-50 text-green-700`
      if (status === 'rejected') return `${baseClass} bg-red-50 text-red-700`
      return `${baseClass} bg-gray-50 text-gray-700`
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('sr-BA', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    formatShortDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('sr-BA', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      })
    },
    getCVUrl(path) {
      return `http://127.0.0.1:8000/${path}`
    },
    getLetterUrl(path) {
      return `http://127.0.0.1:8000/${path}`
    }
  }
}
</script>