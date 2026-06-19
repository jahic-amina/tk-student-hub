<template>
  <nav
    class="sticky top-0 z-50 bg-white dark:bg-slate-900 border-b border-gray-100 dark:border-slate-700 shadow-sm transition-colors duration-300">
    <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">

      <router-link to="/" class="text-xl font-bold text-primary dark:text-orange-500">
        TK Student Hub
      </router-link>

      <div class="flex gap-6">
        <router-link to="/ads"
          class="text-gray-600 dark:text-slate-300 hover:text-primary dark:hover:text-orange-400 font-medium transition">Prakse
          i edukacije</router-link>
        <router-link to="/materials"
          class="text-gray-600 dark:text-slate-300 hover:text-primary dark:hover:text-orange-400 font-medium transition">Materijali</router-link>
        <router-link to="/forum"
          class="text-gray-600 dark:text-slate-300 hover:text-primary dark:hover:text-orange-400 font-medium transition">Forum</router-link>
        <router-link to="/profiles"
          class="text-gray-600 dark:text-slate-300 hover:text-primary dark:hover:text-orange-400 font-medium transition">Profili</router-link>
      </div>

      <div class="flex items-center gap-4">

        <template v-if="isUserLoggedIn">
          <div v-if="isAdmin" class="relative group">
            <button
              class="text-gray-600 dark:text-slate-300 hover:text-primary font-medium transition flex items-center gap-1">
              Admin
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3">
                </path>
              </svg>
            </button>
            <div
              class="absolute left-0 mt-0 w-48 bg-white dark:bg-slate-800 rounded-lg shadow-lg border border-gray-200 dark:border-slate-700 opacity-0 group-hover:opacity-100 invisible group-hover:visible transition z-10">
              <router-link to="/admin/companies"
                class="block px-4 py-2.5 text-sm text-gray-700 dark:text-slate-200 hover:bg-gray-50 dark:hover:bg-slate-700 border-b border-gray-100 dark:border-slate-600 first:rounded-t-lg">
                Upravljanje kompanijama
              </router-link>
              <router-link to="/admin/ads"
                class="block px-4 py-2.5 text-sm text-gray-700 dark:text-slate-200 hover:bg-gray-50 dark:hover:bg-slate-700 last:rounded-b-lg">
                Upravljanje oglasima
              </router-link>
              <router-link to="/admin/users"
                class="block px-4 py-2.5 text-sm text-gray-700 dark:text-slate-200 hover:bg-gray-50 dark:hover:bg-slate-700 last:rounded-b-lg">
                Upravljanje korisnicima
              </router-link>
            </div>
          </div>

          <NotificationBell />

          <router-link to="/profiles" class="text-gray-600 dark:text-slate-300 hover:text-primary font-medium">{{
            username }}</router-link>
          <button @click="logoutUser"
            class="border border-primary text-primary dark:border-orange-500 dark:text-orange-500 px-4 py-1.5 rounded-lg hover:bg-primary dark:hover:bg-orange-500 hover:text-white dark:hover:text-white transition">
            Odjava
          </button>
        </template>

        <template v-else-if="isCompanyLoggedIn">
          <NotificationBell />

          <router-link :to="`/companies/${companyId}`"
            class="text-gray-600 dark:text-slate-300 hover:text-primary font-medium">{{ companyName }}</router-link>
          <button @click="logoutCompany"
            class="border border-primary text-primary px-4 py-1.5 rounded-lg hover:bg-primary hover:text-white transition">
            Odjava
          </button>
        </template>

        <template v-else>
          <router-link to="/login"
            class="text-gray-600 dark:text-slate-300 hover:text-primary font-medium">Prijava</router-link>
          <router-link to="/register"
            class="bg-primary text-white px-4 py-1.5 rounded-lg hover:bg-primary/90 transition">
            Registracija
          </router-link>
        </template>
      </div>

      <div class="flex items-center gap-2 border-l border-gray-200 dark:border-slate-700 pl-4 ml-2">
        <span class="text-xs font-semibold text-gray-600 dark:text-gray-300 select-none whitespace-nowrap">
          {{ isDarkMode ? 'Dark' : 'Light' }}
        </span>
        <button @click="toggleDarkMode"
          class="w-10 h-6 flex items-center bg-gray-300 dark:bg-orange-500 rounded-full p-1 transition-colors duration-300 focus:outline-none flex-shrink-0">
          <div class="bg-white w-4 h-4 rounded-full shadow-md transform transition-transform duration-300"
            :class="{ 'translate-x-4': isDarkMode }"></div>
        </button>
      </div>

    </div>
  </nav>
</template>

<script>
import NotificationBell from './NotificationBell.vue';

export default {
  name: 'NavBar',
  components: {
    NotificationBell
  },
  data() {
    return {
      token: localStorage.getItem('token'),
      companyToken: localStorage.getItem('company_token'),
      username: localStorage.getItem('username') || 'Profil',
      companyName: localStorage.getItem('company_name') || 'Kompanija',
      companyId: localStorage.getItem('company_id'),
      role: localStorage.getItem('role') || '',
      isDarkMode: localStorage.getItem('theme') === 'dark'
    }
  },
  computed: {
    isUserLoggedIn() {
      return !!this.token
    },
    isCompanyLoggedIn() {
      return !!this.companyToken
    },
    isAdmin() {
      return this.role === 'admin'
    }
  },
  mounted() {
    // Slušamo evente za dinamički login bez osvježavanja stranice
    window.addEventListener('user-login', this.updateUser)

    // Inicijalna provjera dark mode-a pri učitavanju
    if (this.isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  },
  beforeUnmount() {
    window.removeEventListener('user-login', this.updateUser)
  },
  methods: {
    updateUser() {
      this.token = localStorage.getItem('token')
      this.companyToken = localStorage.getItem('company_token')
      this.username = localStorage.getItem('username') || 'Profil'
      this.companyName = localStorage.getItem('company_name') || 'Kompanija'
      this.companyId = localStorage.getItem('company_id')
      this.role = localStorage.getItem('role') || ''
    },
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      if (this.isDarkMode) {
        document.documentElement.classList.add('dark');
        localStorage.setItem('theme', 'dark');
      } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
      }
    },
    logoutUser() {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('role')
      localStorage.removeItem('user_id')
      this.token = null
      this.username = 'Profil'
      this.role = ''
      window.dispatchEvent(new Event('user-logout'))
      this.$router.push('/login')
    },
    logoutCompany() {
      localStorage.removeItem('company_token')
      localStorage.removeItem('company_name')
      localStorage.removeItem('company_id')
      this.companyToken = null
      this.companyName = 'Kompanija'
      this.companyId = null
      this.$router.push('/login')
    }
  }
}
</script>