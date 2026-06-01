<template>
  <nav class="bg-white border-b border-gray-100 shadow-sm">
    <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
      
      <router-link to="/" class="text-xl font-bold text-primary">
        TK Student Hub
      </router-link>

      <div class="flex gap-6">
      <router-link to="/ads" class="text-gray-600 hover:text-primary font-medium transition">Prakse i edukacije</router-link>
      <span class="text-gray-400 font-medium cursor-not-allowed">Materijali</span>
      <span class="text-gray-400 font-medium cursor-not-allowed">Forum</span>
      <span class="text-gray-400 font-medium cursor-not-allowed">Profili</span>
        </div>

      <div class="flex items-center gap-4">
        <template v-if="isUserLoggedIn">
          <div v-if="isAdmin" class="relative group">
            <button class="text-gray-600 hover:text-primary font-medium transition flex items-center gap-1">
              Admin
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path></svg>
            </button>
            <div class="absolute left-0 mt-0 w-48 bg-white rounded-lg shadow-lg border border-gray-200 opacity-0 group-hover:opacity-100 invisible group-hover:visible transition z-10">
              <router-link to="/admin/companies" class="block px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 border-b border-gray-100 first:rounded-t-lg">
                Upravljanje kompanijama
              </router-link>
            </div>
          </div>
          <router-link to="/profiles" class="text-gray-600 hover:text-primary font-medium">{{ username }}</router-link>
          <button @click="logoutUser" class="border border-primary text-primary px-4 py-1.5 rounded-lg hover:bg-primary hover:text-white transition">
            Odjava
          </button>
        </template>
        <template v-else-if="isCompanyLoggedIn">
          <router-link :to="`/companies/${companyId}`" class="text-gray-600 hover:text-primary font-medium">{{ companyName }}</router-link>
          <button @click="logoutCompany" class="border border-primary text-primary px-4 py-1.5 rounded-lg hover:bg-primary hover:text-white transition">
            Odjava
          </button>
        </template>
        <template v-else>
          <div class="flex items-center gap-3">
            <router-link to="/login" class="text-gray-600 hover:text-primary font-medium">Prijava</router-link>
            <router-link to="/register" class="bg-primary text-white px-4 py-1.5 rounded-lg hover:bg-primary/90 transition">
              Registracija
            </router-link>
          </div>
          
          <div class="w-px bg-gray-200"></div>
          
          <div class="flex items-center gap-3">
            <router-link to="/company/login" class="text-gray-600 hover:text-primary font-medium">Prijava kompanije</router-link>
            <router-link to="/company/register" class="border border-primary text-primary px-4 py-1.5 rounded-lg hover:bg-primary hover:text-white transition">
              Registracija kompanija
            </router-link>
          </div>
        </template>
      </div>

    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  computed: {
    isUserLoggedIn() {
      return !!localStorage.getItem('token')
    },
    isCompanyLoggedIn() {
      return !!localStorage.getItem('company_token')
    },
    username() {
      return localStorage.getItem('username') || 'Profil'
    },
    companyName() {
      return localStorage.getItem('company_name') || 'Kompanija'
    },
    companyId() {
      return localStorage.getItem('company_id')
    },
    isAdmin() {
      return localStorage.getItem('role') === 'admin'
    }
  },
  methods: {
    logoutUser() {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('role')
      window.location.href = '/'
    },
    logoutCompany() {
      localStorage.removeItem('company_token')
      localStorage.removeItem('company_name')
      localStorage.removeItem('company_id')
      window.location.href = '/'
    }
  }
}
</script>