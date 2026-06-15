<template>
  <nav class="sticky top-0 z-50 bg-white dark:bg-slate-900 border-b border-gray-100 dark:border-slate-700 shadow-sm transition-colors duration-300">
    <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
      
      <router-link to="/" class="text-xl font-bold text-primary dark:text-orange-500">
        TK Student Hub
      </router-link>

      <div class="flex gap-6">
<<<<<<< HEAD
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
              <router-link to="/admin/ads" class="block px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 last:rounded-b-lg">
               Upravljanje oglasima
              </router-link>
            </div> 
          </div>

          <NotificationBell />

          <span class="text-gray-600 font-medium">{{ username }}</span>
          <button @click="logoutUser" class="border border-primary text-primary px-4 py-1.5 rounded-lg hover:bg-primary hover:text-white transition">
=======
        <router-link to="/prakse-i-edukacije" class="text-gray-600 dark:text-slate-300 hover:text-primary dark:hover:text-orange-400 font-medium transition">Prakse i edukacije</router-link>
        <router-link to="/mentoring" class="text-gray-600 dark:text-slate-300 hover:text-primary dark:hover:text-orange-400 font-medium transition">Materijali</router-link>
        <router-link to="/forum" class="text-gray-600 dark:text-slate-300 hover:text-primary dark:hover:text-orange-400 font-medium transition">Forum</router-link>
        <router-link to="/profiles" class="text-gray-600 dark:text-slate-300 hover:text-primary dark:hover:text-orange-400 font-medium transition">Profili</router-link>
      </div>

      <div class="flex items-center gap-4">
        <template v-if="isLoggedIn">
          <router-link to="/profiles" class="text-gray-600 dark:text-slate-300 hover:text-primary font-medium">{{ username }}</router-link>
          <button @click="logout" class="border border-primary text-primary dark:border-orange-500 dark:text-orange-500 px-4 py-1.5 rounded-lg hover:bg-primary dark:hover:bg-orange-500 hover:text-white dark:hover:text-white transition">
>>>>>>> main
            Odjava
          </button>
        </template>

        <template v-else-if="isCompanyLoggedIn">
          <NotificationBell />

          <router-link :to="`/companies/${companyId}`" class="text-gray-600 hover:text-primary font-medium">{{ companyName }}</router-link>
          <button @click="logoutCompany" class="border border-primary text-primary px-4 py-1.5 rounded-lg hover:bg-primary hover:text-white transition">
            Odjava
          </button>
        </template>

        <template v-else>
<<<<<<< HEAD
          <div class="flex items-center gap-3">
            <router-link to="/login" class="text-gray-600 hover:text-primary font-medium">Prijava</router-link>
            <router-link to="/register" class="bg-primary text-white px-4 py-1.5 rounded-lg hover:bg-primary/90 transition">
              Registracija
            </router-link>
          </div>
=======
          <router-link to="/login" class="text-gray-600 dark:text-slate-300 hover:text-primary font-medium">Prijava</router-link>
          <router-link to="/register" class="bg-primary text-white px-4 py-1.5 rounded-lg hover:bg-primary/90 transition">
            Registracija
          </router-link>
>>>>>>> main
        </template>
      </div>

      <div class="flex items-center gap-2 border-l border-gray-200 dark:border-slate-700 pl-4 ml-2">
        <span class="text-xs font-semibold text-gray-600 dark:text-gray-300 select-none whitespace-nowrap">
          {{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}
        </span>
        <button 
          @click="toggleDarkMode"
          class="w-10 h-6 flex items-center bg-gray-300 dark:bg-orange-500 rounded-full p-1 transition-colors duration-300 focus:outline-none flex-shrink-0"
        >
          <div 
            class="bg-white w-4 h-4 rounded-full shadow-md transform transition-transform duration-300"
            :class="{ 'translate-x-4': isDarkMode }"
          ></div>
        </button>
      </div>

    </div>
  </nav>
</template>

<script>

import NotificationBell from './NotificationBell.vue';

export default {
  name: 'NavBar',
<<<<<<< HEAD
  components: {
    NotificationBell 
  },
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
=======
  data() {
    return {
      token: localStorage.getItem('token'),
      username: localStorage.getItem('username') || 'Profil',
      role: localStorage.getItem('role') || ''
      isDarkMode: localStorage.getItem('theme') === 'dark'
    }
  },
  computed: {
    isLoggedIn() {
      return !!this.token
    },
    isAdmin() {
      return this.role === 'admin'
    }
  },
  mounted() {
    window.addEventListener('user-login', this.updateUser)
  },
  beforeUnmount() {
    window.removeEventListener('user-login', this.updateUser)
  },
  methods: {
    updateUser() {
      this.token = localStorage.getItem('token')
      this.username = localStorage.getItem('username') || 'Profil'
      this.role = localStorage.getItem('role') || ''
    if (this.isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  },
  methods: {
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
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('role')
      this.token = null
      this.username = 'Profil'
      this.role = ''
      window.dispatchEvent(new Event('user-logout'))
      this.$router.push('/login')
>>>>>>> main
    }
  }
}
</script>