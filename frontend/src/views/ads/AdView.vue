<template>
  <div class="min-h-screen bg-gradient-to-b from-orange-50 via-white to-white">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-8 md:py-12">
      <div class="mb-6">
        <router-link to="/ads" class="text-sm font-semibold text-orange-600 hover:text-orange-700 transition">
          ← Nazad na listu oglasa
        </router-link>
      </div>

      <div v-if="loading" class="rounded-3xl border border-gray-100 bg-white shadow-sm p-8 text-center text-gray-500">
        Učitavanje detalja oglasa...
      </div>

      <div v-else-if="errorMessage" class="rounded-3xl border border-red-100 bg-red-50 p-8 text-red-700">
        {{ errorMessage }}
      </div>

      <div v-else-if="ad" class="grid gap-6 lg:grid-cols-[1.6fr_0.9fr]">
        <section class="rounded-3xl border border-gray-100 bg-white shadow-sm p-6 sm:p-8">
          <div class="flex flex-wrap gap-2 mb-4 text-xs font-semibold">
            <span :class="getTypeClass(ad.typeLabel)">{{ ad.typeLabel }}</span>
            <span :class="getStatusClass(ad.statusLabel)">{{ ad.statusLabel }}</span>
          </div>

          <h1 class="text-2xl sm:text-4xl font-black text-gray-900 leading-tight mb-3">
            {{ ad.title }}
          </h1>

          <p class="text-base sm:text-lg text-gray-600 font-medium mb-6">
            <router-link :to="`/companies/${ad.company_id}`" class="hover:text-orange-500 transition-colors">
              {{ ad.company }}
            </router-link>
          </p>

          <div class="grid sm:grid-cols-3 gap-3 mb-8">
            <div class="rounded-2xl bg-gray-50 border border-gray-100 p-4">
              <p class="text-xs uppercase tracking-wide text-gray-400 font-semibold mb-1">Lokacija</p>
              <p class="text-sm font-bold text-gray-900">{{ ad.location || 'Nije navedeno' }}</p>
            </div>
            <div class="rounded-2xl bg-gray-50 border border-gray-100 p-4">
              <p class="text-xs uppercase tracking-wide text-gray-400 font-semibold mb-1">Trajanje</p>
              <p class="text-sm font-bold text-gray-900">{{ ad.duration || 'Nije navedeno' }}</p>
            </div>
            <div class="rounded-2xl bg-gray-50 border border-gray-100 p-4">
              <p class="text-xs uppercase tracking-wide text-gray-400 font-semibold mb-1">Naknada</p>
              <p class="text-sm font-bold text-gray-900">{{ ad.compensation || 'Nije navedeno' }}</p>
            </div>
          </div>

          <div class="space-y-6 text-gray-700">
            <div>
              <h2 class="text-lg font-bold text-gray-900 mb-2">Opis oglasa</h2>
              <p class="leading-7 whitespace-pre-line">{{ ad.description }}</p>
            </div>

            <div v-if="ad.requirements">
              <h2 class="text-lg font-bold text-gray-900 mb-2">Uslovi</h2>
              <p class="leading-7 whitespace-pre-line">{{ ad.requirements }}</p>
            </div>

            <div v-if="ad.benefits">
              <h2 class="text-lg font-bold text-gray-900 mb-2">Benefiti</h2>
              <p class="leading-7 whitespace-pre-line">{{ ad.benefits }}</p>
            </div>
          </div>
        </section>

        <aside class="rounded-3xl border border-gray-100 bg-white shadow-sm p-6 sm:p-8 h-fit sticky top-6">
          <h2 class="text-lg font-bold text-gray-900 mb-4">Brzi pregled</h2>

          <div class="space-y-4 text-sm">
            <div>
              <p class="text-gray-400 font-semibold mb-1">Oblast</p>
              <p class="text-gray-900 font-medium">{{ ad.field || 'Nije navedeno' }}</p>
            </div>
            <div>
              <p class="text-gray-400 font-semibold mb-1">Tagovi</p>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="tag in ad.tags"
                  :key="tag"
                  class="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-xs font-semibold"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
            <div>
              <p class="text-gray-400 font-semibold mb-1">Broj mjesta</p>
              <p class="text-gray-900 font-medium">{{ ad.spots || 'Nije navedeno' }}</p>
            </div>
            <div>
              <p class="text-gray-400 font-semibold mb-1">Rok prijave</p>
              <p class="text-gray-900 font-medium">{{ ad.deadline || 'Nije navedeno' }}</p>
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
import { getAdById, getApprovedCompanies } from '../../services/api.js'

const BASE_BADGE = 'px-3 py-1.5 rounded-full'

function formatType(type) {
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
  name: 'AdDetailView',
  data() {
    return {
      loading: false,
      errorMessage: '',
      ad: null
    }
  },
  methods: {
    getTypeClass(typeLabel) {
      if (typeLabel === 'Praksa') return `bg-blue-50 text-blue-600 ${BASE_BADGE}`
      if (typeLabel === 'Edukacija') return `bg-indigo-50 text-indigo-600 ${BASE_BADGE}`
      return `bg-amber-50 text-amber-600 ${BASE_BADGE}`
    },
    getStatusClass(statusLabel) {
      if (statusLabel === 'Aktivan') return `bg-green-50 text-green-600 ${BASE_BADGE}`
      if (statusLabel === 'Istekao') return `bg-orange-50 text-orange-600 ${BASE_BADGE}`
      return `bg-red-50 text-red-600 ${BASE_BADGE}`
    },
    async fetchAd() {
      this.loading = true
      this.errorMessage = ''

      const adId = Number(this.$route.params.id)
      let found, companies

      try {
        [found, companies] = await Promise.all([
          getAdById(adId),
          getApprovedCompanies()
        ])
      } catch (err) {
        console.error('Failed to fetch ad details:', err)
        this.errorMessage = 'Ne mogu učitati detalje oglasa. Provjeri da li je API pokrenut.'
        this.loading = false
        return
      }

      if (!found) {
        this.errorMessage = 'Oglas nije pronađen.'
        this.loading = false
        return
      }

      const companiesById = new Map(
        (companies || []).map(company => [company.id, company.company_name])
      )

      this.ad = {
        id: found.id,
        title: found.title,
        company: companiesById.get(found.company_id) || `Kompanija #${found.company_id}`,
        company_id: found.company_id,
        description: found.description,
        tags: [found.field, found.location].filter(Boolean),
        typeLabel: formatType(found.type),
        compensation: formatCompensation(found.compensation, found.currency),
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
    }
  },
  mounted() {
    this.fetchAd()
  }
}
</script>