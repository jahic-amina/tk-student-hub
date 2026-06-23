<template>
  <div class="min-h-screen bg-gray-50 dark:bg-slate-900 py-10 px-4 font-sans transition-colors duration-200">
    <div class="max-w-6xl mx-auto">

      <div class="mb-8">
        <h1 class="text-2xl sm:text-3xl font-black text-gray-900 dark:text-slate-100">Upravljanje kompanijama</h1>
        <p class="text-gray-500 dark:text-slate-400 mt-1 text-sm">Pregled i odobravanje registrovanih kompanija.</p>
      </div>

      <div v-if="loading" class="text-center py-12 text-gray-500 dark:text-slate-400 text-sm font-medium">
        Učitavanje kompanija...
      </div>

      <div v-else-if="errorMessage" class="p-6 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/50 rounded-2xl text-red-700 dark:text-red-400 text-sm">
        {{ errorMessage }}
      </div>

      <template v-else>
        <div class="flex gap-3 mb-6 flex-wrap">
          <button
            v-for="filter in ['Sve', 'Na čekanju', 'Odobrene', 'Odbijene', 'Obrisane']"
            :key="filter"
            @click="activeFilter = filter"
            :class="['px-4 py-2 rounded-lg text-xs sm:text-sm font-semibold transition bg-transparent border cursor-pointer', activeFilter === filter ? 'bg-orange-500 dark:bg-orange-600 border-transparent text-white' : 'bg-white dark:bg-slate-800 border-gray-200 dark:border-slate-700 text-gray-600 dark:text-slate-300 hover:bg-gray-50 dark:hover:bg-slate-700/50']"
          >
            {{ filter }}
            <span class="ml-1 opacity-70">({{ filterCount(filter) }})</span>
          </button>
        </div>

        <div v-if="filteredCompanies.length === 0" class="text-center py-10 text-gray-400 dark:text-slate-500 text-sm">
          Nema kompanija u ovoj kategoriji.
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          <AdminCompanyApprovalCard
            v-for="company in filteredCompanies"
            :key="company.id"
            :company="company"
            @approve="updateStatus($event, 'approved')"
            @reject="updateStatus($event, 'denied')"
            @delete="deleteCompanyHandler($event)"
            @restore="restoreCompanyHandler($event)"
          />
        </div>
      </template>

    </div>
  </div>
</template>

<script>
import AdminCompanyApprovalCard from '../../components/company/AdminCompanyApprovalCard.vue'
import { getAdminCompanies, updateCompanyStatus, getMe, deleteCompany, restoreCompany } from '../../services/api.js'

const FILTER_TO_STATUS = {
  'Na čekanju': 'pending',
  'Odobrene': 'approved',
  'Odbijene': 'denied'
}

export default {
  name: 'AdminCompaniesView',
  components: { AdminCompanyApprovalCard },
  data() {
    return {
      companies: [],
      loading: false,
      errorMessage: '',
      activeFilter: 'Sve'
    }
  },
  computed: {
    filteredCompanies() {
      if (this.activeFilter === 'Sve') return this.companies
      if (this.activeFilter === 'Obrisane') return this.companies.filter(c => c.is_deleted)
      const status = FILTER_TO_STATUS[this.activeFilter]
      return this.companies.filter(c => !c.is_deleted && c.status === status)
    }
  },
  methods: {
    filterCount(filter) {
      if (filter === 'Sve') return this.companies.length
      if (filter === 'Obrisane') return this.companies.filter(c => c.is_deleted).length
      const status = FILTER_TO_STATUS[filter]
      return this.companies.filter(c => !c.is_deleted && c.status === status).length
    },
    async fetchCompanies() {
      this.loading = true
      this.errorMessage = ''

      const token = localStorage.getItem('token')
      let companies

      try {
        companies = await getAdminCompanies(token)
      } catch (err) {
        this.errorMessage = 'Ne mogu učitati kompanije. Provjeri da li imaš admin pristup.'
        this.loading = false
        return
      }

      this.companies = companies.map(c => ({ ...c, updating: null }))
      this.loading = false
    },
    async updateStatus(company, status) {
      const token = localStorage.getItem('token')
      company.updating = status

      try {
        const updated = await updateCompanyStatus(company.id, status, token)
        company.status = updated.status
      } catch (err) {
        this.errorMessage = `Greška pri ažuriranju statusa za ${company.company_name}.`
      } finally {
        company.updating = null
      }
    },
    async deleteCompanyHandler(company) {
      const token = localStorage.getItem('token')
      company.updating = 'deleting'

      try {
        await deleteCompany(company.id, token)
        company.is_deleted = true
      } catch (err) {
        this.errorMessage = `Greška pri brisanju kompanije ${company.company_name}.`
      } finally {
        company.updating = null
      }
    },
    async restoreCompanyHandler(company) {
      const token = localStorage.getItem('token')
      company.updating = 'restoring'

      try {
        await restoreCompany(company.id, token)
        company.is_deleted = false
      } catch (err) {
        this.errorMessage = `Greška pri vraćanju kompanije ${company.company_name}.`
      } finally {
        company.updating = null
      }
    }
  },
  async mounted() {
    const token = localStorage.getItem('token')

    try {
      const user = await getMe(token)
      if (user.role !== 'admin') {
        this.$router.push('/')
        return
      }
    } catch {
      this.$router.push('/')
      return
    }

    this.fetchCompanies()
  }
}
</script>