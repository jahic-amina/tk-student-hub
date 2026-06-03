<template>
  <div>
    <!-- Glavno dugme -->
    <button
      type="button"
      @click="handleDownload"
      :disabled="isDownloading"
      :class="['inline-flex items-center gap-2 bg-primary text-white font-semibold px-5 py-2.5 rounded-lg shadow-sm hover:bg-primary/90 active:scale-[0.98] transition disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-primary', fullWidth ? 'w-full justify-center' : '']"
    >
      <!-- SVG ikona strelica (download) -->
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5"
           fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round"
              d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2M7 10l5 5 5-5M12 15V3" />
      </svg>
      <span>{{ isDownloading ? 'Preuzimanje...' : 'PREUZMI' }}</span>
    </button>

    <!-- Poruka o gresci -->
    <p v-if="errorMessage" class="text-sm text-red-600 mt-2">
      {{ errorMessage }}
    </p>
  </div>
</template>

<script>
import { downloadMaterial } from '../services/api'

export default {
  name: 'DownloadButton',

  // Prop koji komponenta prima izvana — id materijala i fullWidth za prikaz
 props: {
    materialId: {
      type: [Number, String],
      required: true,
    },
    fullWidth: {
      type: Boolean,
      default: false,
    },
  },

  data() {
    return {
      isDownloading: false, // Stanje preuzimanja — onemogućava dvostruki klik
      errorMessage: null, // Poruka greške ako download ne uspije
    }
  },

  methods: {
    async handleDownload() {
      this.errorMessage = null
      this.isDownloading = true

      try {
        // Fetch bez autentifikacije — download je javan za sve korisnike
        const response = await downloadMaterial(this.materialId)

        //Provjera HTTP statusa
        if (!response.ok) {
          if (response.status === 403) throw new Error('Materijal nije aktivan i ne može se preuzeti.')
          if (response.status === 404) throw new Error('Materijal ili fajl nije pronađen.')
          throw new Error('Greška prilikom preuzimanja.')
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
        this.errorMessage = err.message || 'Greška prilikom preuzimanja.'
      } finally {
        this.isDownloading = false
      }
    },
  },
}
</script>