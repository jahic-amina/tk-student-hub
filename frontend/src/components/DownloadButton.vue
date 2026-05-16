<template>
  <div>
    <!-- Glavno dugme -->
    <button
      type="button"
      @click="handleDownload"
      :disabled="!isLoggedIn || isDownloading"
      :title="isLoggedIn ? 'Preuzmi materijal' : 'Prijavi se da bi preuzeo materijal'"
      class="inline-flex items-center gap-2 bg-primary text-white font-semibold
             px-5 py-2.5 rounded-lg shadow-sm
             hover:bg-primary/90 active:scale-[0.98] transition
             disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-primary"
    >
      <!-- SVG ikona strelica (download) -->
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5"
           fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round"
              d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2M7 10l5 5 5-5M12 15V3" />
      </svg>
      <span>{{ isDownloading ? 'Preuzimanje...' : 'PREUZMI' }}</span>
    </button>

    <!-- Poruka kada korisnik nije prijavljen -->
    <p v-if="!isLoggedIn" class="text-sm text-gray-500 mt-2">
      <router-link to="/login" class="text-primary font-medium hover:underline">
        Prijavi se
      </router-link>
      da bi mogao preuzeti materijal.
    </p>

    <!-- Poruka o gresci -->
    <p v-if="errorMessage" class="text-sm text-red-600 mt-2">
      {{ errorMessage }}
    </p>
  </div>
</template>

<script>
const BASE_URL = 'http://127.0.0.1:8000'

export default {
  name: 'DownloadButton',

  // Prop koji komponenta prima izvana (od roditeljske komponente). // Kolega ce u svom view-u napisati: <DownloadButton :material-id="material.id" />
  props: {
    materialId: {
      type: [Number, String],
      required: true,
    },
  },

  data() {
    return {
      isDownloading: false,
      errorMessage: null,
    }
  },

  computed: {
    // Acceptance criterion #4: dugme dostupno samo prijavljenim
    isLoggedIn() {
      return !!localStorage.getItem('token')
    },
  },

  methods: {
    async handleDownload() {
      this.errorMessage = null
      this.isDownloading = true

      try {
        const token = localStorage.getItem('token')

        //Fetch sa Bearer tokenom u headeru
        const response = await fetch(
          `${BASE_URL}/materials/${this.materialId}/download`,
          { headers: { 'Authorization': 'Bearer ' + token } }
        )

        //Provjera HTTP statusa
        if (!response.ok) {
          if (response.status === 401) throw new Error('Morate biti prijavljeni za preuzimanje.')
          if (response.status === 403) throw new Error('Materijal nije aktivan i ne moze se preuzeti.')
          if (response.status === 404) throw new Error('Materijal ili fajl nije pronadjen.')
          throw new Error('Greska prilikom preuzimanja.')
        }

        //Izvlacenje originalnog imena fajla iz Content-Disposition headera
        const disposition = response.headers.get('Content-Disposition') || ''
        let filename = 'material-' + this.materialId
        const match = disposition.match(/filename\*?=(?:UTF-8'')?["']?([^"';]+)["']?/i)
        if (match && match[1]) {
          filename = decodeURIComponent(match[1])
        }

        //Pretvaranje response u blob (binarni podaci fajla)
        const blob = await response.blob()

        // Napravljen privremeni URL koji pokazuje na taj blob u memoriji
        const url = window.URL.createObjectURL(blob)

        //Kreiran nevidljiv <a> tag, postavi download atribut i klikni ga
        //    → browser pokrece download bez otvaranja novog taba
        const a = document.createElement('a')
        a.href = url
        a.download = filename
        document.body.appendChild(a)
        a.click()
        a.remove()

        //Oslobodi memoriju
        window.URL.revokeObjectURL(url)
      } catch (err) {
        this.errorMessage = err.message || 'Greska prilikom preuzimanja.'
      } finally {
        this.isDownloading = false
      }
    },
  },
}
</script>