<template>
  <nav class="bg-white border-b border-gray-100 shadow-sm">
    <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
      
      <router-link to="/" class="text-xl font-bold text-primary">
        TK Student Hub
      </router-link>

      <div class="flex gap-6">
      <router-link to="/prakse-i-edukacije" class="text-gray-600 hover:text-primary font-medium transition">Prakse i edukacije</router-link>
      <router-link to="/mentoring" class="text-gray-600 hover:text-primary font-medium transition">Materijali</router-link>
      <router-link to="/forum" class="text-gray-600 hover:text-primary font-medium transition">Forum</router-link>
      <router-link to="/profiles" class="text-gray-600 hover:text-primary font-medium transition">Profili</router-link>
        </div>

      <div class="flex items-center gap-4">
        <template v-if="isLoggedIn">
          <router-link to="/profiles" class="text-gray-600 hover:text-primary font-medium">{{ username }}</router-link>
          <button @click="logout" class="border border-primary text-primary px-4 py-1.5 rounded-lg hover:bg-primary hover:text-white transition">
            Odjava
          </button>
        </template>
        <template v-else>
          <router-link to="/login" class="text-gray-600 hover:text-primary font-medium">Prijava</router-link>
          <router-link to="/register" class="bg-primary text-white px-4 py-1.5 rounded-lg hover:bg-primary/90 transition">
            Registracija
          </router-link>
        </template>
      </div>

      <div class="flex items-center gap-2 border-l border-gray-200 dark:border-slate-700 pl-4 ml-2">
          <span class="text-xs font-semibold text-gray-600 dark:text-gray-300 select-none whitespace-nowrap">
            {{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}
          </span>
          <button 
            @click="toggleDarkMode"
            class="w-10 h-6 flex items-center bg-gray-300 dark:bg-primary rounded-full p-1 transition-colors duration-300 focus:outline-none flex-shrink-0"
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
export default {
  name: 'NavBar',
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem('token')
    },
    username() {
      return localStorage.getItem('username') || 'Profil'
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('role')
      this.$router.push('/login')
    }
  }
}
</script>