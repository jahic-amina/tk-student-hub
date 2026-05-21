<template>
  <div class="min-h-screen bg-gradient-to-b from-orange-50 via-white to-white">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-8 md:py-12">
      <div class="mb-6">
        <router-link to="/prakse-i-edukacije" class="text-sm font-semibold text-orange-600 hover:text-orange-700 transition">
          ← Nazad na listu oglasa
        </router-link>
      </div>

      <div v-if="loading" class="rounded-3xl border border-gray-100 bg-white shadow-sm p-8 text-center text-gray-500">
        Učitavanje detalja oglasa...
      </div>

      <div v-else-if="errorMessage" class="rounded-3xl border border-red-100 bg-red-50 p-8 text-red-700">
        {{ errorMessage }}
      </div>

      <div v-else-if="oglas" class="grid gap-6 lg:grid-cols-[1.6fr_0.9fr]">
        <section class="rounded-3xl border border-gray-100 bg-white shadow-sm p-6 sm:p-8">
          <div class="flex flex-wrap gap-2 mb-4 text-xs font-semibold">
            <span :class="getTipKlasa(oglas.tip)">{{ oglas.tip }}</span>
            <span :class="getStatusKlasa(oglas.status)">{{ oglas.status }}</span>
          </div>

          <h1 class="text-2xl sm:text-4xl font-black text-gray-900 leading-tight mb-3">
            {{ oglas.naslov }}
          </h1>

          <p class="text-base sm:text-lg text-gray-600 font-medium mb-6">
            {{ oglas.kompanija }}
          </p>

          <div class="grid sm:grid-cols-3 gap-3 mb-8">
            <div class="rounded-2xl bg-gray-50 border border-gray-100 p-4">
              <p class="text-xs uppercase tracking-wide text-gray-400 font-semibold mb-1">Lokacija</p>
              <p class="text-sm font-bold text-gray-900">{{ oglas.lokacija }}</p>
            </div>
            <div class="rounded-2xl bg-gray-50 border border-gray-100 p-4">
              <p class="text-xs uppercase tracking-wide text-gray-400 font-semibold mb-1">Trajanje</p>
              <p class="text-sm font-bold text-gray-900">{{ oglas.trajanje || 'Nije navedeno' }}</p>
            </div>
            <div class="rounded-2xl bg-gray-50 border border-gray-100 p-4">
              <p class="text-xs uppercase tracking-wide text-gray-400 font-semibold mb-1">Naknada</p>
              <p class="text-sm font-bold text-gray-900">{{ oglas.dodatno || 'Nije navedeno' }}</p>
            </div>
          </div>

          <div class="space-y-6 text-gray-700">
            <div>
              <h2 class="text-lg font-bold text-gray-900 mb-2">Opis oglasa</h2>
              <p class="leading-7 whitespace-pre-line">{{ oglas.opis }}</p>
            </div>

            <div v-if="oglas.requirements">
              <h2 class="text-lg font-bold text-gray-900 mb-2">Uslovi</h2>
              <p class="leading-7 whitespace-pre-line">{{ oglas.requirements }}</p>
            </div>

            <div v-if="oglas.benefits">
              <h2 class="text-lg font-bold text-gray-900 mb-2">Benefiti</h2>
              <p class="leading-7 whitespace-pre-line">{{ oglas.benefits }}</p>
            </div>
          </div>
        </section>

        <aside class="rounded-3xl border border-gray-100 bg-white shadow-sm p-6 sm:p-8 h-fit sticky top-6">
          <h2 class="text-lg font-bold text-gray-900 mb-4">Brzi pregled</h2>

          <div class="space-y-4 text-sm">
            <div>
              <p class="text-gray-400 font-semibold mb-1">Oblast</p>
              <p class="text-gray-900 font-medium">{{ oglas.oblast || 'Nije navedeno' }}</p>
            </div>
            <div>
              <p class="text-gray-400 font-semibold mb-1">Tagovi</p>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="tag in oglas.tagovi"
                  :key="tag"
                  class="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-xs font-semibold"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
            <div>
              <p class="text-gray-400 font-semibold mb-1">Broj mjesta</p>
              <p class="text-gray-900 font-medium">{{ oglas.spots || 'Nije navedeno' }}</p>
            </div>
            <div>
              <p class="text-gray-400 font-semibold mb-1">Rok prijave</p>
              <p class="text-gray-900 font-medium">{{ oglas.deadline || 'Nije navedeno' }}</p>
            </div>
          </div>

          <div class="mt-6 rounded-2xl bg-orange-50 border border-orange-100 p-4">
            <p class="text-sm font-semibold text-orange-900 mb-1">Spreman za prijavu?</p>
            <p class="text-sm text-orange-800 leading-6">
              Ova stranica sada prikazuje kompletan opis oglasa. U sljedećem koraku možemo dodati i dugme za direktnu prijavu.
            </p>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script>
import { getApprovedCompanies, getPublicAds } from '../services/api.js'

function formatTip(type) {
  const map = {
    internship: 'Praksa',
    education: 'Edukacija',
    scholarship: 'Stipendija'
  }

  return map[type] || 'Prilika'
}

function formatStatus(status) {
  const map = {
    active: 'Aktivan',
    pending: 'Na čekanju',
    expired: 'Istekao',
    rejected: 'Odbijen',
    changes_requested: 'Potrebne izmjene'
  }

  return map[status] || 'Aktivan'
}

function formatCompensation(value, currency) {
  if (value === null || value === undefined) return ''

  return `${value} ${currency || 'BAM'}`
}

export default {
  name: 'OglasDetailView',
  data() {
    return {
      loading: false,
      errorMessage: '',
      oglas: null
    }
  },
  methods: {
    getTipKlasa(tip) {
      if (tip === 'Praksa') return 'bg-blue-50 text-blue-600 px-3 py-1.5 rounded-full'
      if (tip === 'Edukacija') return 'bg-indigo-50 text-indigo-600 px-3 py-1.5 rounded-full'
      return 'bg-amber-50 text-amber-600 px-3 py-1.5 rounded-full'
    },
    getStatusKlasa(status) {
      if (status === 'Aktivan') return 'bg-green-50 text-green-600 px-3 py-1.5 rounded-full'
      if (status === 'Istekao') return 'bg-orange-50 text-orange-600 px-3 py-1.5 rounded-full'
      return 'bg-red-50 text-red-600 px-3 py-1.5 rounded-full'
    },
    async fetchOglas() {
      this.loading = true
      this.errorMessage = ''

      try {
        const oglasId = Number(this.$route.params.id)
        const [ads, companies] = await Promise.all([
          getPublicAds(),
          getApprovedCompanies()
        ])

        const companiesById = new Map(
          (companies || []).map(company => [company.id, company.company_name])
        )

        const ad = (ads || []).find(item => Number(item.id) === oglasId)

        if (!ad) {
          this.errorMessage = 'Oglas nije pronađen.'
          this.oglas = null
          return
        }

        this.oglas = {
          id: ad.id,
          naslov: ad.title || '',
          kompanija: companiesById.get(ad.company_id) || `Kompanija #${ad.company_id}`,
          opis: ad.description || '',
          tagovi: [ad.field, ad.location].filter(Boolean),
          tip: formatTip(ad.type),
          dodatno: formatCompensation(ad.compensation, ad.currency),
          status: formatStatus(ad.status),
          lokacija: ad.location || 'Nije navedeno',
          trajanje: ad.duration_months ? `${ad.duration_months} mjeseci` : '',
          oblast: ad.field || '',
          requirements: ad.requirements || '',
          benefits: ad.benefits || '',
          spots: ad.spots || '',
          deadline: ad.deadline || ''
        }
      } catch (err) {
        console.error('Neuspješno učitavanje detalja oglasa', err)
        this.errorMessage = 'Ne mogu učitati detalje oglasa. Provjeri da li je API pokrenut na 127.0.0.1:8000.'
      } finally {
        this.loading = false
      }
    }
  },
  mounted() {
    this.fetchOglas()
  },
  watch: {
    '$route.params.id'() {
      this.fetchOglas()
    }
  }
}
</script>