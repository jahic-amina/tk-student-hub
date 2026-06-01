<template>
  <div class="min-h-screen bg-gray-50 font-sans">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-8 md:py-12">

      <div class="mb-6">
        <router-link to="/ads" class="text-sm font-semibold text-orange-600 hover:text-orange-700 transition">
          ← Nazad na listu oglasa
        </router-link>
      </div>

      <div v-if="loading" class="text-center py-12 text-gray-500 text-sm font-medium">
        Učitavanje kompanije...
      </div>

      <div v-else-if="errorMessage" class="p-6 bg-red-50 border border-red-200 rounded-2xl text-red-700 text-sm">
        {{ errorMessage }}
      </div>

      <template v-else-if="company">

        <div class="bg-white rounded-3xl border border-gray-100 shadow-sm p-6 sm:p-8 mb-6">
          <div class="flex flex-col sm:flex-row gap-6 items-start">
            <div class="flex-shrink-0">
              <img
                v-if="company.logo_path"
                :src="logoUrl"
                :alt="company.company_name"
                class="w-20 h-20 object-contain rounded-2xl border border-gray-100"
              />
              <div
                v-else
                class="w-20 h-20 rounded-2xl border border-gray-100 bg-gray-50 flex items-center justify-center text-2xl font-black text-gray-300"
              >
                {{ company.company_name?.charAt(0) }}
              </div>
            </div>

            <div class="flex-1">
              <div class="flex flex-wrap items-center gap-2 mb-1">
                <h1 class="text-2xl font-black text-gray-900">{{ company.company_name }}</h1>
                <span class="text-xs font-semibold px-2.5 py-1 rounded-full bg-green-50 text-green-700">
                  Odobrena
                </span>
              </div>
              <p class="text-gray-500 text-sm leading-relaxed mt-2">{{ company.description }}</p>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-6 pt-6 border-t border-gray-100 text-sm">
            <div>
              <p class="text-xs text-gray-400 font-semibold uppercase tracking-wide mb-1">Email</p>
              <a :href="`mailto:${company.email}`" class="text-orange-500 hover:underline font-medium">
                {{ company.email }}
              </a>
            </div>
            <div>
              <p class="text-xs text-gray-400 font-semibold uppercase tracking-wide mb-1">Web</p>
              <a :href="company.website_url" target="_blank" class="text-orange-500 hover:underline font-medium">
                {{ company.website_url }}
              </a>
            </div>
            <div>
              <p class="text-xs text-gray-400 font-semibold uppercase tracking-wide mb-1">Adresa</p>
              <p class="text-gray-700 font-medium">{{ company.address }}</p>
            </div>
          </div>
        </div>

        <div>
          <h2 class="text-lg font-bold text-gray-900 mb-4">
            Oglasi kompanije
            <span class="text-gray-400 font-medium text-base ml-1">({{ ads.length }})</span>
          </h2>

          <div v-if="ads.length === 0" class="text-center py-10 px-4 bg-white rounded-2xl border border-dashed border-gray-200">
            <p class="text-gray-400 text-sm">Ova kompanija trenutno nema aktivnih oglasa.</p>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <AdCard
              v-for="ad in ads"
              :key="ad.id"
              :ad="ad"
            />
          </div>
        </div>

      </template>

    </div>
  </div>
</template>

<script>
import AdCard from '../../components/ads/AdCard.vue'
import { getCompanyById, getAdsByCompany } from '../../services/api.js'
import { mapAd } from '../../services/utils.js'

const BASE_URL = 'http://127.0.0.1:8000'

export default {
  name: 'CompanyView',
  components: { AdCard },
  data() {
    return {
      loading: false,
      errorMessage: '',
      company: null,
      ads: []
    }
  },
  computed: {
    logoUrl() {
      return `${BASE_URL}/${this.company.logo_path}`
    }
  },
  methods: {
    async fetchCompany() {
      this.loading = true
      this.errorMessage = ''

      const companyId = Number(this.$route.params.id)
      let company, ads

      try {
        [company, ads] = await Promise.all([
          getCompanyById(companyId),
          getAdsByCompany(companyId)
        ])
      } catch (err) {
        this.errorMessage = 'Ne mogu učitati podatke o kompaniji.'
        this.loading = false
        return
      }

      this.company = company
      this.ads = (ads || []).map(ad => mapAd(ad, company.company_name))
      this.loading = false
    }
  },
  mounted() {
    this.fetchCompany()
  }
}
</script>